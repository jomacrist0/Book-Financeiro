import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime, date, timedelta
import numpy as np

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="📈 Taxa de Aprovação",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CUSTOMIZADO COM TEMA ESCURO ALUN ---
st.markdown("""
<style>
    .main > div { background: transparent !important; }
    .main { background-color: #0e1117 !important; }
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 { color: #fafafa !important; font-weight: 700 !important; }
    .main p, .main span, .main div, .main label, .main li, .main th, .main td { color: #fafafa !important; }
    .main [data-testid="metric-container"] { background-color: #262730 !important; border: 1px solid #30343f !important; color: #fafafa !important; border-radius: 10px !important; padding: 1rem !important; }
    .main [data-testid="metric-container"] > div { color: #fafafa !important; }
    .main [data-testid="stContainer"] { background-color: #0e1117 !important; border: 1px solid #30343f !important; border-radius: 10px !important; }
    .compact-controls { background: #262730 !important; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; border: 1px solid #30343f !important; box-shadow: 0 2px 10px rgba(14, 17, 23, 0.3) !important; }
    .main .stTabs [data-baseweb="tab-list"] { background-color: #262730 !important; border-radius: 8px !important; }
    .main .stTabs [data-baseweb="tab"] { background-color: #0e1117 !important; color: #fafafa !important; border: 1px solid #30343f !important; border-radius: 6px !important; }
    .main .stTabs [aria-selected="true"] { background-color: #ff6b35 !important; color: #ffffff !important; border: 1px solid #ff6b35 !important; }
    .main .stDataFrame { background-color: #262730 !important; color: #fafafa !important; border-radius: 8px !important; }
    .main [data-testid="stDownloadButton"] > button { background-color: #ff6b35 !important; color: #ffffff !important; border: none !important; border-radius: 8px !important; }
    .main .stAlert { background-color: #262730 !important; border: 1px solid #30343f !important; color: #fafafa !important; }
    .main .streamlit-expanderHeader { background-color: #262730 !important; color: #fafafa !important; }
    .destaque { color: #ff6b35 !important; font-weight: bold; }
    .metric-positive { color: #00ff00 !important; }
    .metric-negative { color: #ff4444 !important; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR COM LOGO ALUN ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 15px; margin-bottom: 2rem;">
        <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQwIiB2aWV3Qm94PSIwIDAgMTAwIDQwIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8dGV4dCB4PSI1MCIgeT0iMjUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyNCIgZm9udC13ZWlnaHQ9ImJvbGQiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5BTFVOPC90ZXh0Pgo8L3N2Zz4K" style="width: 120px; height: auto;">
        <div style="color: #ccc; font-size: 12px; margin-top: 10px;">Taxa de Aprovação</div>
    </div>
    """, unsafe_allow_html=True)

def show_taxa_de_aprovacao():
    # --- Header da Página ---
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #fafafa; font-weight: 700; margin-bottom: 0;">📈 Dashboard de Taxa de Aprovação</h1>
        <p style="color: #ccc; font-size: 1.1em;">Acompanhe as taxas de aprovação por categoria e meio de pagamento</p>
    </div>
    """, unsafe_allow_html=True)

    # --- CARREGAMENTO DOS DADOS ---
    # Botão para recarregar dados
    col_reload, col_info = st.columns([1, 3])
    with col_reload:
        if st.button("🔄 Atualizar Dados", help="Clique para recarregar os dados do CSV"):
            st.cache_data.clear()
            st.rerun()

    with col_info:
        st.info("💡 Clique em 'Atualizar Dados' após modificar o arquivo CSV para ver as mudanças")

    # --- Carregamento dos Dados ---
    ARQUIVO_DADOS = 'Base_taxa_de_aprovacao.csv'
    # Buscar primeiro na pasta data/
    diretorio_script = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_dados_csv = os.path.join(diretorio_script, 'data', ARQUIVO_DADOS)
    
    # Se não encontrar, tenta na raiz (fallback)
    if not os.path.exists(caminho_dados_csv):
        caminho_dados_csv = os.path.join(diretorio_script, ARQUIVO_DADOS)
    
    # Para debug: mostra onde está procurando
    # st.write(f"Procurando arquivo em: {caminho_dados_csv}")

    if not os.path.exists(caminho_dados_csv):
        st.error(f"Arquivo '{ARQUIVO_DADOS}' não encontrado na pasta do projeto.")
        st.stop()

    # Carregar dados
    try:
        separadores = [';', ',', '\t', '|']
        codificacoes = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        df = None
        for sep in separadores:
            for encoding in codificacoes:
                try:
                    df_teste = pd.read_csv(caminho_dados_csv, sep=sep, encoding=encoding, engine='python')
                    if len(df_teste.columns) > 1:
                        df = df_teste
                        break
                except Exception:
                    pass
            if df is not None:
                break

        if df is None:
            st.error("❌ Não foi possível ler o arquivo com nenhuma combinação de separador/codificação.")
            st.stop()

        df.columns = df.columns.str.strip()
        df['Data'] = None
        data_artificial = False

        data_col = None
        possiveis_colunas_data = []
        for col in df.columns:
            if col.lower() in ['data', 'date', 'data_transação', 'data transação', 'dt', 'data transacao']:
                possiveis_colunas_data.append(col)
        if len(df.columns) > 0 and df.columns[0] not in possiveis_colunas_data:
            possiveis_colunas_data.append(df.columns[0])

        for col in possiveis_colunas_data:
            formatos = [
                '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y', '%d/%m/%y', '%d-%m-%y',
                '%Y-%m-%d', '%m/%d/%Y', '%Y/%m/%d'
            ]
            conversao_ok = False
            for fmt in formatos:
                try:
                    df_temp = pd.to_datetime(df[col], format=fmt, errors='coerce')
                    datas_validas = df_temp.notna().sum()
                    if datas_validas > len(df) * 0.3:
                        df['Data'] = df_temp
                        data_col = col
                        conversao_ok = True
                        break
                except Exception:
                    pass
            if not conversao_ok:
                try:
                    df_temp = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
                    datas_validas = df_temp.notna().sum()
                    if datas_validas > len(df) * 0.3:
                        df['Data'] = df_temp
                        data_col = col
                        conversao_ok = True
                except Exception:
                    pass
            if not conversao_ok:
                try:
                    df_temp = pd.to_datetime(df[col], errors='coerce')
                    datas_validas = df_temp.notna().sum()
                    if datas_validas > len(df) * 0.3:
                        df['Data'] = df_temp
                        data_col = col
                        conversao_ok = True
                except Exception:
                    pass
            if conversao_ok:
                break

        if df['Data'].notna().sum() == 0:
            hoje = datetime.now()
            datas = [hoje - timedelta(days=i) for i in range(len(df))]
            df['Data'] = datas[:len(df)]
            data_artificial = True

        if 'Data_Temp' in df.columns:
            df = df.drop('Data_Temp', axis=1)

        col_classificacao = None
        for col in df.columns:
            if col.lower() in ['classificacao', 'classificação', 'categoria', 'tipo']:
                col_classificacao = col
                break
        if col_classificacao is None:
            col_classificacao = df.columns[1] if len(df.columns) > 1 else df.columns[0]

        col_status = None
        for col in df.columns:
            if col.lower() in ['status final', 'status_final', 'status']:
                col_status = col
                break
        if col_status is None:
            for col in df.columns:
                if 'status' in col.lower():
                    col_status = col
                    break
            if col_status is None:
                col_status = df.columns[2] if len(df.columns) > 2 else df.columns[0]

        if not any(df[col_status].astype(str).str.lower().str.strip().isin(['authorized', 'declined'])):
            map_status = {}
            status_values = df[col_status].value_counts().index.tolist()
            for status in status_values:
                status_lower = str(status).lower()
                if any(termo in status_lower for termo in ['aprovad', 'author', 'confirm', 'aceito', 'success']):
                    map_status[status] = 'authorized'
                elif any(termo in status_lower for termo in ['recusad', 'declin', 'negad', 'cancel', 'fail', 'rejeit']):
                    map_status[status] = 'declined'
                else:
                    map_status[status] = 'other'
            df['status_mapped'] = df[col_status].map(map_status)
            col_status = 'status_mapped'

        df = df.dropna(subset=['Data']).copy()
        if col_classificacao in df.columns:
            df = df[df[col_classificacao] != 'Valor 1 real'].copy()
        df_calc = df[df[col_status].astype(str).str.lower().str.strip().isin(['authorized', 'declined'])].copy()
        if len(df_calc) == 0:
            st.error("❌ Nenhum registro encontrado com status 'authorized' ou 'declined'.")
            st.stop()

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        st.stop()

    # --- Filtros ---
    col1, col2, col3 = st.columns(3)
    with col1:
        periodo_opcoes = {
            'Diário': 'D',
            'Semanal': 'W-SUN',
            'Mensal': 'M',
            'Trimestral': 'Q',
            'Anual': 'A'
        }
        periodo_selecionado = st.selectbox(
            "📅 Período de agregação:",
            options=list(periodo_opcoes.keys()),
            index=1
        )
    with col2:
        categorias_disponiveis = sorted(df_calc[col_classificacao].unique())
        categorias_selecionadas = st.multiselect(
            "📊 Categorias:",
            options=categorias_disponiveis,
            default=categorias_disponiveis
        )
    with col3:
        data_min = df_calc['Data'].min().date()
        data_max = df_calc['Data'].max().date()
        try:
            if data_max.month >= 3:
                data_inicio_default = max(data_min, date(data_max.year, data_max.month - 2, 1))
            else:
                mes_anterior = data_max.month + 10
                ano_anterior = data_max.year - 1
                data_inicio_default = max(data_min, date(ano_anterior, mes_anterior, 1))
        except Exception:
            data_inicio_default = max(data_min, data_max - timedelta(days=90))
        data_fim_default = data_max
        intervalo_datas = st.date_input(
            "📆 Período de análise:",
            value=[data_inicio_default, data_fim_default],
            min_value=data_min,
            max_value=data_max,
            help="Selecione o intervalo de datas para análise"
        )

    if len(intervalo_datas) == 2:
        data_inicio, data_fim = intervalo_datas
        if not pd.api.types.is_datetime64_any_dtype(df_calc['Data']):
            df_calc['Data'] = pd.to_datetime(df_calc['Data'], errors='coerce')
        df_filtrado_data = df_calc[
            (df_calc['Data'].dt.date >= data_inicio) &
            (df_calc['Data'].dt.date <= data_fim)
        ].copy()
    else:
        st.warning("⚠️ Selecione um intervalo de datas válido (data início e fim)")
        df_filtrado_data = df_calc.copy()

    df_filtrado = df_filtrado_data[df_filtrado_data[col_classificacao].isin(categorias_selecionadas)].copy()

    st.markdown(
        f"**Dados filtrados:** {len(df_filtrado):,} registros | "
        f"Período: {data_inicio.strftime('%d/%m/%Y') if len(intervalo_datas) == 2 else 'N/A'} a {data_fim.strftime('%d/%m/%Y') if len(intervalo_datas) == 2 else 'N/A'} | "
        f"Categorias: {len(categorias_selecionadas)} selecionadas"
    )

    if len(df_filtrado) == 0:
        st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados. Ajuste os filtros e tente novamente.")
        st.stop()

    periodo_cod = periodo_opcoes[periodo_selecionado]
    if not pd.api.types.is_datetime64_any_dtype(df_filtrado['Data']):
        df_filtrado['Data'] = pd.to_datetime(df_filtrado['Data'], errors='coerce')
    df_filtrado['periodo'] = df_filtrado['Data'].dt.to_period(periodo_cod)

    df_agrupado = df_filtrado.groupby(['periodo', col_classificacao]).agg(
        pagamentos_autorizados = (col_status, lambda x: x.astype(str).str.lower().str.strip().eq('authorized').sum()),
        pagamentos_recusados = (col_status, lambda x: x.astype(str).str.lower().str.strip().eq('declined').sum())
    ).reset_index()
    df_agrupado['total_considerado'] = df_agrupado['pagamentos_autorizados'] + df_agrupado['pagamentos_recusados']
    df_agrupado['taxa_aprovacao'] = (df_agrupado['pagamentos_autorizados'] / df_agrupado['total_considerado'] * 100).fillna(0)
    df_agrupado['data_periodo'] = df_agrupado['periodo'].dt.start_time

    st.subheader("📈 Taxa de Aprovação Histórica")
    fig = go.Figure()
    cores = ['#1F77B4', '#FF6B00', '#2CA02C', '#D62728', '#9467BD', '#8C564B', '#E377C2', '#7F7F7F', '#BCBD22', '#17BECF']
    for i, categoria in enumerate(categorias_selecionadas):
        df_cat = df_agrupado[df_agrupado[col_classificacao] == categoria]
        if not df_cat.empty:
            fig.add_trace(go.Scatter(
                x=df_cat['data_periodo'],
                y=df_cat['taxa_aprovacao'],
                mode='lines+markers',
                name=categoria,
                line=dict(width=3, color=cores[i % len(cores)]),
                marker=dict(size=8, color=cores[i % len(cores)]),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                             'Data: %{x|%d/%m/%Y}<br>' +
                             'Taxa: %{y:.1f}%<br>' +
                             '<extra></extra>'
            ))
    fig.update_layout(
        title=f'Taxa de Aprovação por Categoria - {periodo_selecionado}',
        xaxis=dict(title=f'Período ({periodo_selecionado})'),
        yaxis=dict(title='Taxa de Aprovação (%)', ticksuffix='%'),
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("💳 Taxa de Aprovação por Categoria")
    df_categoria = df_filtrado.groupby(col_classificacao).agg(
        pagamentos_autorizados = (col_status, lambda x: x.astype(str).str.lower().str.strip().eq('authorized').sum()),
        pagamentos_recusados = (col_status, lambda x: x.astype(str).str.lower().str.strip().eq('declined').sum())
    ).reset_index()
    df_categoria['total_considerado'] = df_categoria['pagamentos_autorizados'] + df_categoria['pagamentos_recusados']
    df_categoria['taxa_aprovacao'] = (df_categoria['pagamentos_autorizados'] / df_categoria['total_considerado'] * 100).fillna(0)
    df_categoria['taxa_aprovacao_fmt'] = df_categoria['taxa_aprovacao'].apply(lambda x: f"{x:.1f}%")
    df_display = df_categoria[[col_classificacao, 'pagamentos_autorizados', 'pagamentos_recusados', 'total_considerado', 'taxa_aprovacao_fmt']].copy()
    df_display.columns = ['Categoria', 'Pagamentos Autorizados', 'Pagamentos Recusados', 'Total Considerado', 'Taxa de Aprovação']
    st.dataframe(df_display, use_container_width=True, height=400, hide_index=True)

    st.subheader("📊 Distribuição por Status Final")
    df_status_todos = df[df[col_classificacao].isin(categorias_selecionadas)]

    # Garantir que a coluna Data está em datetime
    if not pd.api.types.is_datetime64_any_dtype(df_status_todos['Data']):
        df_status_todos['Data'] = pd.to_datetime(df_status_todos['Data'], errors='coerce')

    if len(intervalo_datas) == 2:
        df_status_todos = df_status_todos[
            (df_status_todos['Data'].dt.date >= data_inicio) &
            (df_status_todos['Data'].dt.date <= data_fim)
        ]
    df_status = df_status_todos.groupby([col_status, col_classificacao]).size().reset_index(name='quantidade')
    df_status_pivot = df_status.pivot(index=col_status, columns=col_classificacao, values='quantidade').fillna(0)
    df_status_pivot['Total'] = df_status_pivot.sum(axis=1)
    st.dataframe(df_status_pivot, use_container_width=True, height=400)

    col_canal_venda = None
    for col in df.columns:
        if col.lower() in ['canal de venda', 'canal_venda', 'meio de pagamento', 'meio_pagamento']:
            col_canal_venda = col
            break
    if col_canal_venda:
        st.subheader("🛒 Taxa de Aprovação por Meio de Pagamento")
        df_meio_pagamento = df_filtrado.groupby(col_canal_venda).agg(
            pagamentos_autorizados = (col_status, lambda x: x.astype(str).str.lower().str.strip().eq('authorized').sum()),
            pagamentos_recusados = (col_status, lambda x: x.astype(str).str.lower().str.strip().eq('declined').sum())
        ).reset_index()
        df_meio_pagamento['total_considerado'] = df_meio_pagamento['pagamentos_autorizados'] + df_meio_pagamento['pagamentos_recusados']
        df_meio_pagamento['taxa_aprovacao'] = (df_meio_pagamento['pagamentos_autorizados'] / df_meio_pagamento['total_considerado'] * 100).fillna(0)
        df_meio_pagamento['taxa_aprovacao_fmt'] = df_meio_pagamento['taxa_aprovacao'].apply(lambda x: f"{x:.1f}%")
        df_meio_display = df_meio_pagamento[[col_canal_venda, 'pagamentos_autorizados', 'pagamentos_recusados', 'total_considerado', 'taxa_aprovacao_fmt']].copy()
        df_meio_display.columns = ['Meio de Pagamento', 'Pagamentos Autorizados', 'Pagamentos Recusados', 'Total Considerado', 'Taxa de Aprovação']
        st.dataframe(df_meio_display, use_container_width=True, height=400, hide_index=True)

    st.markdown(
        f"📊 Relatório de Taxa de Aprovação\n\n"
        f"📅 Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        f"💡 Taxa calculada como: Pagamentos Autorizados / (Pagamentos Autorizados + Pagamentos Recusados)",
        unsafe_allow_html=True
    )

# Executar a função diretamente
show_taxa_de_aprovacao()