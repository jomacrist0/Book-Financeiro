import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta
import base64
import hashlib

# --- CONFIGURAÇÃO DA PÁGINA (DEVE SER PRIMEIRO) ---
st.set_page_config(
    page_title="💰 Saldos do Ecossistema",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- AUTENTICAÇÃO ---
SENHA_CORRETA = "saldosalun2026"

def verificar_autenticacao():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    
    if not st.session_state.autenticado:
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column;">
            <h1 style="color: #ff6b35; text-align: center;">🔐 Acesso Restrito</h1>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown("### Digite a senha para continuar")
            senha = st.text_input("Senha:", type="password")
            
            if st.button("Acessar", use_container_width=True):
                if senha == SENHA_CORRETA:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("❌ Senha incorreta!")
        
        st.stop()

verificar_autenticacao()

# --- CSS CUSTOMIZADO COM TEMA VERMELHO VINHO ---
st.markdown("""
<style>
    .main > div { background: transparent !important; }
    .main { background-color: #630330 !important; }
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 { 
        color: #fafafa !important; 
        font-weight: 700 !important; 
    }
    .main p, .main span, .main div, .main label { 
        color: #fafafa !important; 
    }
    .main [data-testid="metric-container"] { 
        background: linear-gradient(135deg, #7a0440 0%, #8b0550 100%) !important;
        border: 1px solid #9a0660 !important; 
        color: #fafafa !important; 
        border-radius: 12px !important; 
        padding: 1.5rem !important;
    }
    section[data-testid="stSidebar"] { 
        background-color: #1a1a1a !important; 
    }
    section[data-testid="stSidebar"] * { 
        color: #fafafa !important; 
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR COM LOGO ALUN ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 15px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 2rem;">ALUN</h1>
        <div style="color: #ccc; font-size: 12px; margin-top: 10px;">Saldos do Ecossistema</div>
    </div>
    """, unsafe_allow_html=True)

# --- BOTÃO DE ATUALIZAÇÃO ---
col_refresh = st.columns([3, 1])
with col_refresh[1]:
    if st.button("🔄 Atualizar Dados", type="primary"):
        st.cache_data.clear()
        st.success("✅ Cache limpo!")
        st.rerun()

# --- HEADER ---
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #fafafa; font-weight: 700; margin-bottom: 0;">💰 Dashboard de Saldos do Ecossistema</h1>
    <p style="color: #ccc; font-size: 1.1em;">Análise Financeira Integrada do Ecossistema</p>
</div>
""", unsafe_allow_html=True)

# --- FUNÇÕES ---
def load_data():
    """Carrega e processa os dados do arquivo XLSX."""
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "data", "1Saldos - ecossistema.xlsx"),
        os.path.join(os.getcwd(), "data", "1Saldos - ecossistema.xlsx"),
        os.path.join("data", "1Saldos - ecossistema.xlsx"),
    ]
    
    xlsx_path = None
    for path in possible_paths:
        if os.path.exists(path):
            xlsx_path = path
            break
    
    if xlsx_path is None:
        st.error("❌ Arquivo '1Saldos - ecossistema.xlsx' não encontrado em /data")
        return None
    
    try:
        df = pd.read_excel(xlsx_path)
        df.columns = [col.strip().replace('\n', '').replace('\r', '') for col in df.columns]
        
        col_data = next((c for c in df.columns if 'data' in c.lower()), None)
        col_empresa = next((c for c in df.columns if 'empresa' in c.lower()), None)
        col_saldo = next((c for c in df.columns if 'saldo' in c.lower() and 'final' in c.lower()), None)
        
        if not col_data or not col_saldo:
            st.error("❌ Colunas esperadas não encontradas no Excel.")
            return None
        
        if not col_empresa:
            df['Empresa'] = 'Empresa Geral'
            col_empresa = 'Empresa'
        
        df[col_data] = pd.to_datetime(df[col_data], errors='coerce', dayfirst=True)
        
        if df[col_saldo].dtype not in ['int64', 'float64']:
            df[col_saldo] = (
                df[col_saldo]
                .astype(str)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
            )
        df[col_saldo] = pd.to_numeric(df[col_saldo], errors='coerce').fillna(0)
        
        df = df.rename(columns={
            col_data: 'Data',
            col_empresa: 'Empresa',
            col_saldo: 'Saldo_Final'
        }).dropna(subset=['Data'])
        
        return df
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar o arquivo: {e}")
        return None

def process_data(df):
    """Processa os dados para agregação por empresa e ecossistema."""
    df_empresa_dia = (
        df.groupby(['Empresa', 'Data'], as_index=False)['Saldo_Final']
        .sum()
        .rename(columns={'Saldo_Final': 'Saldo_do_Dia'})
    )
    df_ecossistema = (
        df_empresa_dia.groupby('Data', as_index=False)['Saldo_do_Dia']
        .sum()
    )
    df_ecossistema['Empresa'] = 'Saldo do Ecossistema'
    df_consolidado = pd.concat([df_empresa_dia, df_ecossistema], ignore_index=True)
    return df_consolidado, df_empresa_dia, df_ecossistema

def agregar_por_granularidade(df, granularidade):
    """Agrega dados conforme a granularidade selecionada."""
    df_temp = df.copy()
    
    if granularidade == "Semanal":
        df_temp['Periodo'] = df_temp['Data'].dt.to_period('W').apply(lambda x: x.start_time)
        periodo_label = "Semana"
    elif granularidade == "Mensal":
        df_temp['Periodo'] = df_temp['Data'].dt.to_period('M').apply(lambda x: x.start_time)
        periodo_label = "Mês"
    else:
        df_temp['Periodo'] = df_temp['Data']
        periodo_label = "Dia"
    
    df_agrupado = (
        df_temp.sort_values(['Empresa', 'Data'])
        .groupby(['Periodo', 'Empresa'], as_index=False)
        .tail(1)
        [['Periodo', 'Empresa', 'Saldo_do_Dia']]
    )
    
    return df_agrupado, periodo_label

# --- CARREGAR DADOS ---
df = load_data()

if df is None:
    st.stop()

result = process_data(df)
df_consolidado, df_empresa_dia, df_ecossistema = result

# Datas disponíveis
datas_unicas = df_consolidado['Data'].drop_duplicates().sort_values(ascending=False)
datas_15_mais_recentes = datas_unicas.head(15)
data_mais_antiga_dos_15 = datas_15_mais_recentes.min()
data_mais_recente = datas_15_mais_recentes.max()
data_mais_antiga_disponivel = datas_unicas.min()
data_mais_recente_disponivel = datas_unicas.max()

# --- CONFIGURAÇÕES ---
st.markdown('<h4>⚙️ Configurações do Dashboard</h4>', unsafe_allow_html=True)

col_config1, col_config2, col_config3, col_config4 = st.columns([2, 2, 2, 2])

with col_config1:
    st.markdown("**📅 Data Inicial**")
    periodo_inicio = st.date_input(
        "Período inicial",
        value=data_mais_antiga_dos_15.date(),
        min_value=data_mais_antiga_disponivel.date(),
        max_value=data_mais_recente_disponivel.date(),
        key="data_inicio",
        label_visibility="collapsed"
    )

with col_config2:
    st.markdown("**📅 Data Final**")
    periodo_fim = st.date_input(
        "Período final",
        value=data_mais_recente_disponivel.date(),
        min_value=data_mais_antiga_disponivel.date(),
        max_value=data_mais_recente_disponivel.date(),
        key="data_fim",
        label_visibility="collapsed"
    )

with col_config3:
    st.markdown("**🏢 Empresas**")
    empresas_disponveis = df_consolidado['Empresa'].unique().tolist()
    default_empresas = ['Alura']
    empresas_selecionadas = st.multiselect(
        "Selecionar Empresas",
        options=empresas_disponveis,
        default=[emp for emp in default_empresas if emp in empresas_disponveis],
        label_visibility="collapsed"
    )

with col_config4:
    st.markdown("**📊 Granularidade**")
    granularidade = st.selectbox(
        "Granularidade:",
        options=["Diário", "Semanal", "Mensal"],
        index=0,
        label_visibility="collapsed"
    )

# --- INFO DO PERÍODO ---
st.info(f"📅 **Período selecionado:** {periodo_inicio.strftime('%d/%m/%Y')} até {periodo_fim.strftime('%d/%m/%Y')}")

# --- FILTRAR DADOS ---
df_filtrado = df_consolidado[
    (df_consolidado['Data'] >= pd.to_datetime(periodo_inicio)) &
    (df_consolidado['Data'] <= pd.to_datetime(periodo_fim)) &
    (df_consolidado['Empresa'].isin(empresas_selecionadas))
].copy()

df_plot, periodo_label = agregar_por_granularidade(df_filtrado, granularidade)

# --- MÉTRICAS PRINCIPAIS ---
if not df_plot.empty:
    df_todas_empresas = df_consolidado[
        (df_consolidado['Data'] >= pd.to_datetime(periodo_inicio)) &
        (df_consolidado['Data'] <= pd.to_datetime(periodo_fim))
    ].copy()
    
    df_plot_todas, _ = agregar_por_granularidade(df_todas_empresas, granularidade)
    ultima_data_todas = df_plot_todas['Periodo'].max()
    dados_ultimo_periodo_todas = df_plot_todas[df_plot_todas['Periodo'] == ultima_data_todas]
    
    def buscar_saldo_geral(empresa):
        dados_empresa = dados_ultimo_periodo_todas[dados_ultimo_periodo_todas['Empresa'] == empresa]
        return dados_empresa['Saldo_do_Dia'].iloc[0] if len(dados_empresa) > 0 else 0
    
    saldo_ecossistema = buscar_saldo_geral('Saldo do Ecossistema')
    saldo_alura = buscar_saldo_geral('Alura')
    saldo_fiap = buscar_saldo_geral('FIAP')
    saldo_pm3 = buscar_saldo_geral('PM3')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌐 Ecossistema", f"R$ {saldo_ecossistema/1_000_000:.1f}M")
    with col2:
        st.metric("🎓 Alura", f"R$ {saldo_alura/1_000_000:.1f}M")
    with col3:
        st.metric("🏫 FIAP", f"R$ {saldo_fiap/1_000_000:.1f}M")
    with col4:
        st.metric("💼 PM3", f"R$ {saldo_pm3/1_000_000:.1f}M")

# --- GRÁFICO ---
if not df_plot.empty:
    st.markdown(f"### 📈 Evolução dos Saldos ({granularidade})")
    
    cores_empresas = {
        'Saldo do Ecossistema': '#ffffff',
        'Alura': '#1a5490',
        'FIAP': '#cc0000',
        'PM3': '#663399',
    }
    
    fig_line = px.line(
        df_plot,
        x='Periodo',
        y='Saldo_do_Dia',
        color='Empresa',
        markers=True,
        color_discrete_map=cores_empresas,
        text=df_plot['Saldo_do_Dia'].apply(lambda x: f"R$ {x/1_000_000:.1f}M")
    )
    
    fig_line.update_layout(
        xaxis_title=periodo_label,
        yaxis_title="Saldo (R$)",
        hovermode='x unified',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)')
    )
    
    fig_line.update_traces(
        mode='lines+markers+text',
        line=dict(width=3),
        marker=dict(size=8, color='white'),
        textposition="top center",
        textfont=dict(size=10, color='white'),
    )
    
    st.plotly_chart(fig_line, use_container_width=True)
    
    # --- TABELA ---
    st.markdown("### 🗃️ Dados Consolidados")
    
    df_tabela = df_plot.copy()
    df_tabela['Data'] = df_tabela['Periodo'].dt.strftime('%d/%m/%Y')
    df_tabela['Saldo_Formatado'] = df_tabela['Saldo_do_Dia'].apply(lambda x: f"R$ {x:,.0f}")
    df_tabela = df_tabela.sort_values('Periodo', ascending=False)
    
    st.dataframe(
        df_tabela[['Data', 'Empresa', 'Saldo_Formatado']].rename(columns={
            'Data': 'Data',
            'Empresa': 'Empresa',
            'Saldo_Formatado': 'Saldo (R$)'
        }),
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # Download
    csv_data = df_tabela[['Data', 'Empresa', 'Saldo_Formatado']].to_csv(index=False)
    st.download_button(
        label="📥 Baixar dados como CSV",
        data=csv_data,
        file_name=f"saldos_ecossistema_{periodo_inicio}_{periodo_fim}.csv",
        mime="text/csv"
    )
else:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")

# --- FOOTER ---
st.markdown("""
<div style='text-align: center; color: #666666; font-size: 0.9em; margin-top: 2rem;'>
    <div style="background: #1a1a1a; color: white; padding: 5px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; display: inline-block;">ALUN</div>
    <br>📊 Dashboard de Saldos do Ecossistema | Atualizado automaticamente
</div>
""", unsafe_allow_html=True)
