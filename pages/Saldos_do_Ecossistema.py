import os
import sys
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from auth import verificar_autenticacao

st.set_page_config(
    page_title="💰 Saldos do Ecossistema",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

verificar_autenticacao()

st.markdown(
    """
    <div style="text-align: center; margin-bottom: 1rem;">
        <h1 style="color: #fafafa; font-weight: 700; margin-bottom: 0;">💰 Dashboard de Saldos do Ecossistema</h1>
        <p style="color: #ccc; font-size: 1.05em;">Análise Financeira Integrada do Ecossistema</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def load_data():
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "1Saldos - ecossistema.xlsx"),
        os.path.join(os.getcwd(), "data", "1Saldos - ecossistema.xlsx"),
        os.path.join("data", "1Saldos - ecossistema.xlsx"),
    ]

    xlsx_path = next((p for p in possible_paths if os.path.exists(p)), None)
    if not xlsx_path:
        st.error("❌ Arquivo '1Saldos - ecossistema.xlsx' não encontrado em /data")
        st.stop()

    df = pd.read_excel(xlsx_path)
    df.columns = [col.strip().replace("\n", "").replace("\r", "") for col in df.columns]

    col_data = next((c for c in df.columns if "data" in c.lower()), None)
    col_empresa = next((c for c in df.columns if "empresa" in c.lower()), None)
    col_saldo = next((c for c in df.columns if "saldo" in c.lower() and "final" in c.lower()), None)

    if not col_data or not col_saldo:
        st.error("❌ Colunas esperadas não encontradas no Excel.")
        st.stop()

    if not col_empresa:
        df["Empresa"] = "Empresa Geral"
        col_empresa = "Empresa"

    df[col_data] = pd.to_datetime(df[col_data], errors="coerce", dayfirst=True)
    df[col_saldo] = (
        df[col_saldo]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    df[col_saldo] = pd.to_numeric(df[col_saldo], errors="coerce").fillna(0)

    df = df.rename(
        columns={
            col_data: "Data",
            col_empresa: "Empresa",
            col_saldo: "Saldo_Final",
        }
    ).dropna(subset=["Data"])

    return df


def process_data(df):
    df_empresa_dia = (
        df.groupby(["Empresa", "Data"], as_index=False)["Saldo_Final"]
        .sum()
        .rename(columns={"Saldo_Final": "Saldo_do_Dia"})
    )
    df_ecossistema = (
        df_empresa_dia.groupby("Data", as_index=False)["Saldo_do_Dia"]
        .sum()
        .assign(Empresa="Saldo do Ecossistema")
    )
    return pd.concat([df_empresa_dia, df_ecossistema], ignore_index=True)


def agregar_por_granularidade(df, granularidade):
    df_temp = df.copy()
    if granularidade == "Semanal":
        df_temp["Periodo"] = df_temp["Data"].dt.to_period("W").apply(lambda x: x.start_time)
        label = "Semana"
    elif granularidade == "Mensal":
        df_temp["Periodo"] = df_temp["Data"].dt.to_period("M").apply(lambda x: x.start_time)
        label = "Mês"
    else:
        df_temp["Periodo"] = df_temp["Data"]
        label = "Dia"

    df_agrupado = (
        df_temp.sort_values(["Empresa", "Data"])
        .groupby(["Periodo", "Empresa"], as_index=False)
        .tail(1)
        [["Periodo", "Empresa", "Saldo_do_Dia"]]
    )
    return df_agrupado, label


df_raw = load_data()

df_consolidado = process_data(df_raw)

col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    st.markdown("**📅 Data Inicial**")
    data_inicio = st.date_input(
        "Data Inicial",
        value=df_consolidado["Data"].min().date(),
        min_value=df_consolidado["Data"].min().date(),
        max_value=df_consolidado["Data"].max().date(),
        label_visibility="collapsed",
    )

with col2:
    st.markdown("**📅 Data Final**")
    data_fim = st.date_input(
        "Data Final",
        value=df_consolidado["Data"].max().date(),
        min_value=df_consolidado["Data"].min().date(),
        max_value=df_consolidado["Data"].max().date(),
        label_visibility="collapsed",
    )

with col3:
    st.markdown("**📊 Granularidade**")
    granularidade = st.selectbox(
        "Granularidade",
        options=["Diário", "Semanal", "Mensal"],
        index=0,
        label_visibility="collapsed",
    )

empresas_disponiveis = sorted(df_consolidado["Empresa"].unique().tolist())
empresas_selecionadas = st.multiselect(
    "🏢 Empresas",
    options=empresas_disponiveis,
    default=[e for e in ["Alura", "FIAP", "PM3", "Saldo do Ecossistema"] if e in empresas_disponiveis],
)

filtro = (
    (df_consolidado["Data"] >= pd.to_datetime(data_inicio))
    & (df_consolidado["Data"] <= pd.to_datetime(data_fim))
    & (df_consolidado["Empresa"].isin(empresas_selecionadas))
)

df_filtrado = df_consolidado[filtro].copy()

df_plot, periodo_label = agregar_por_granularidade(df_filtrado, granularidade)

if df_plot.empty:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

fig = px.line(
    df_plot,
    x="Periodo",
    y="Saldo_do_Dia",
    color="Empresa",
    markers=True,
    labels={"Saldo_do_Dia": "Saldo (R$)", "Periodo": periodo_label},
)
fig.update_layout(
    xaxis_title=periodo_label,
    yaxis_title="Saldo (R$)",
    height=550,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🗃️ Dados Consolidados")

df_tabela = df_plot.copy()
_df = df_tabela.copy()
_df["Data"] = _df["Periodo"].dt.strftime("%d/%m/%Y")
_df["Saldo_Formatado"] = _df["Saldo_do_Dia"].apply(lambda x: f"R$ {x:,.0f}")

st.dataframe(
    _df[["Data", "Empresa", "Saldo_Formatado"]].rename(columns={"Saldo_Formatado": "Saldo (R$)"}),
    use_container_width=True,
    hide_index=True,
    height=400,
)

st.download_button(
    label="📥 Baixar dados como CSV",
    data=_df[["Data", "Empresa", "Saldo_Formatado"]].to_csv(index=False),
    file_name=f"saldos_ecossistema_{data_inicio}_{data_fim}.csv",
    mime="text/csv",
)
