import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta
import base64
import sys
sys.path.append('..')
from auth import verificar_autenticacao

# --- AUTENTICAÇÃO ---
verificar_autenticacao()

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="💰 Saldos do Ecossistema",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CUSTOMIZADO COM TEMA ESCURO ALUN E MELHORIAS DE LAYOUT ---
st.markdown("""
<style>
    /* Layout Principal */
    .main > div { background: transparent !important; }
    .main { background-color: #0e1117 !important; }
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 { 
        color: #fafafa !important; 
        font-weight: 700 !important; 
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    .main h1 { font-size: 2.5rem !important; }
    .main h2 { font-size: 2rem !important; }
    .main h3 { font-size: 1.5rem !important; }
    
    /* Textos e Elementos */
    .main p, .main span, .main div, .main label, .main li, .main th, .main td { 
        color: #fafafa !important; 
        line-height: 1.6 !important;
    }
    
    /* Cards de Métricas Melhorados */
    .main [data-testid="metric-container"] { 
        background: linear-gradient(135deg, #262730 0%, #2a2d3a 100%) !important;
        border: 1px solid #30343f !important; 
        color: #fafafa !important; 
        border-radius: 12px !important; 
        padding: 1.5rem !important;
        box-shadow: 0 4px 12px rgba(14, 17, 23, 0.4) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    .main [data-testid="metric-container"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(14, 17, 23, 0.6) !important;
    }
    .main [data-testid="metric-container"] > div { color: #fafafa !important; }
    
    /* Containers Melhorados */
    .main [data-testid="stContainer"] { 
        background: linear-gradient(135deg, #262730 0%, #2a2d3a 100%) !important;
        border: 1px solid #30343f !important; 
        border-radius: 15px !important;
        box-shadow: 0 4px 12px rgba(14, 17, 23, 0.3) !important;
        margin: 1rem 0 !important;
    }
    
    /* Área de Controles Refinada */
    .compact-controls { 
        background: linear-gradient(135deg, #262730 0%, #2a2d3a 100%) !important;
        padding: 2rem; 
        border-radius: 20px; 
        margin-bottom: 2.5rem; 
        border: 1px solid #30343f !important; 
        box-shadow: 0 8px 25px rgba(14, 17, 23, 0.4) !important;
    }
    .compact-controls h4 {
        color: #ff6b35 !important;
        font-weight: 600 !important;
        margin-bottom: 1.5rem !important;
        font-size: 1.2rem !important;
    }
    
    /* Abas Elegantes */
    .main .stTabs [data-baseweb="tab-list"] { 
        background: linear-gradient(135deg, #262730 0%, #2a2d3a 100%) !important;
        border-radius: 12px !important; 
        padding: 0.5rem !important;
        margin-bottom: 2rem !important;
        box-shadow: inset 0 2px 8px rgba(14, 17, 23, 0.3) !important;
    }
    .main .stTabs [data-baseweb="tab"] { 
        background-color: transparent !important; 
        color: #ccc !important; 
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        margin: 0 0.25rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    .main .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 107, 53, 0.1) !important;
        color: #ff6b35 !important;
    }
    .main .stTabs [aria-selected="true"] { 
        background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%) !important;
        color: #ffffff !important; 
        border: none !important;
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3) !important;
    }
    
    /* DataFrames Elegantes */
    .main .stDataFrame { 
        background: linear-gradient(135deg, #262730 0%, #2a2d3a 100%) !important;
        color: #fafafa !important; 
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 12px rgba(14, 17, 23, 0.3) !important;
    }
    
    /* Botões Aprimorados */
    .main [data-testid="stDownloadButton"] > button,
    .main .stButton > button { 
        background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%) !important;
        color: #ffffff !important; 
        border: none !important; 
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3) !important;
    }
    .main [data-testid="stDownloadButton"] > button:hover,
    .main .stButton > button:hover {
        background: linear-gradient(135deg, #ff8c42 0%, #ffab42 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(255, 107, 53, 0.4) !important;
    }
    
    /* Alertas Melhorados */
    .main .stAlert { 
        background: linear-gradient(135deg, #262730 0%, #2a2d3a 100%) !important;
        border: 1px solid #30343f !important; 
        color: #fafafa !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(14, 17, 23, 0.3) !important;
    }
    .main .stSuccess {
        border-left: 4px solid #4caf50 !important;
    }
    .main .stWarning {
        border-left: 4px solid #ff9800 !important;
    }
    .main .stError {
        border-left: 4px solid #f44336 !important;
    }
    .main .stInfo {
        border-left: 4px solid #2196f3 !important;
    }
    
    /* Expanderes Refinados */
    .main .streamlit-expanderHeader { 
        background: linear-gradient(135deg, #262730 0%, #2a2d3a 100%) !important;
        color: #fafafa !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    
    /* Classes Utilitárias */
    .destaque { 
        color: #ff6b35 !important; 
        font-weight: bold !important;
        text-shadow: 0 0 10px rgba(255, 107, 53, 0.3) !important;
    }
    .metric-positive { 
        color: #4caf50 !important;
        text-shadow: 0 0 10px rgba(76, 175, 80, 0.3) !important;
    }
    .metric-negative { 
        color: #f44336 !important;
        text-shadow: 0 0 10px rgba(244, 67, 54, 0.3) !important;
    }
    
    /* Espaçamento e Separadores */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #30343f 50%, transparent 100%);
        margin: 3rem 0;
        border: none;
    }
    
    /* Responsividade Aprimorada */
    @media (max-width: 768px) {
        .compact-controls {
            padding: 1.5rem !important;
        }
        .main h1 { font-size: 2rem !important; }
        .main h2 { font-size: 1.5rem !important; }
        .main h3 { font-size: 1.25rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR COM LOGO ALUN ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 15px; margin-bottom: 2rem;">
        <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQwIiB2aWV3Qm94PSIwIDAgMTAwIDQwIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8dGV4dCB4PSI1MCIgeT0iMjUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyNCIgZm9udC13ZWlnaHQ9ImJvbGQiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5BTFVOPC90ZXh0Pgo8L3N2Zz4K" style="width: 120px; height: auto;">
        <div style="color: #ccc; font-size: 12px; margin-top: 10px;">Saldos do Ecossistema</div>
    </div>
    """, unsafe_allow_html=True)

# --- BOTÃO DE ATUALIZAÇÃO ---
col_refresh = st.columns([3, 1])
with col_refresh[1]:
    if st.button("🔄 Atualizar Dados", type="primary"):
        st.cache_data.clear()
        st.success("✅ Cache limpo! Dados serão recarregados.")
        st.rerun()

# --- FUNÇÕES DE CARREGAMENTO DE DADOS ---
# --- FUNÇÕES DE CARREGAMENTO DE DADOS ---

# --- HEADER ---
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #fafafa; font-weight: 700; margin-bottom: 0;">💰 Dashboard de Saldos do Ecossistema</h1>
    <p style="color: #ccc; font-size: 1.1em;">Análise Financeira Integrada do Ecossistema</p>
</div>
""", unsafe_allow_html=True)

# --- FUNÇÕES ---
@st.cache_data(ttl=30)  # Cache de 30 segundos apenas
def load_data():
    """Carrega e processa os dados do arquivo XLSX - Cache curto para atualização rápida."""
    # Tentar múltiplos caminhos possíveis com o nome correto do arquivo
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "1Saldos - ecossistema.xlsx"),
        os.path.join(os.getcwd(), "data", "1Saldos - ecossistema.xlsx"),
        os.path.join("data", "1Saldos - ecossistema.xlsx"),
        os.path.join(os.path.dirname(__file__), "..", "1Saldos - ecossistema.xlsx"),
        os.path.join(os.getcwd(), "1Saldos - ecossistema.xlsx"),
        "1Saldos - ecossistema.xlsx"
    ]
    
    xlsx_path = None
    for path in possible_paths:
        if os.path.exists(path):
            xlsx_path = path
            st.session_state.arquivo_carregado = f"✅ Arquivo encontrado em: {path}"
            break
    
    if xlsx_path is None:
        st.error("❌ Arquivo '1Saldos - ecossistema.xlsx' não encontrado!")
        st.error(f"Caminhos procurados:\n" + "\n".join(possible_paths))
        return None
    
    try:
        df = pd.read_excel(xlsx_path)
        
        # Limpar nomes de colunas
        df.columns = [col.strip().replace('\n', '').replace('\r', '') for col in df.columns]

        col_data = None
        col_empresa = None
        col_saldo = None

        # Detectar colunas com busca case-insensitive
        for col in df.columns:
            col_lower = col.lower().strip()
            
            # Procurar por Data
            if 'data' in col_lower and col_data is None:
                col_data = col
            
            # Procurar por Empresa
            if 'empresa' in col_lower and col_empresa is None:
                col_empresa = col
            
            # Procurar por Saldo Final (com espaço também)
            if ('saldo' in col_lower and 'final' in col_lower) and col_saldo is None:
                col_saldo = col

        # Se não encontrou, mostrar erro com debug
        if not col_data:
            st.error(f"❌ Coluna de Data não encontrada! Colunas: {list(df.columns)}")
            return None
        
        if not col_saldo:
            st.error(f"❌ Coluna de Saldo Final não encontrada! Colunas: {list(df.columns)}")
            return None
        
        if not col_empresa:
            st.warning("⚠️ Coluna 'Empresa' não encontrada. Criando coluna genérica.")
            df['Empresa'] = 'Empresa Geral'
            col_empresa = 'Empresa'

        try:
            if col_data and col_data in df.columns:
                df[col_data] = pd.to_datetime(df[col_data], format='%d/%m/%Y', errors='coerce')
            if col_empresa and col_empresa in df.columns:
                df[col_empresa] = df[col_empresa].astype(str)
            if col_saldo and col_saldo in df.columns:
                # Verificar se o valor já é numérico (Excel pode já ter convertido)
                if df[col_saldo].dtype in ['int64', 'float64']:
                    # Se já é numérico, apenas garantir que seja float
                    df[col_saldo] = pd.to_numeric(df[col_saldo], errors='coerce').fillna(0)
                else:
                    # Se é texto, tratar formato português (vírgula decimal, ponto milhar)
                    df[col_saldo] = (
                        df[col_saldo]
                        .astype(str)
                        .str.replace('.', '', regex=False)  # Remove separador de milhares (pontos)
                        .str.replace(',', '.', regex=False)  # Troca vírgula decimal por ponto
                    )
                    df[col_saldo] = pd.to_numeric(df[col_saldo], errors='coerce').fillna(0)
        except Exception as e:
            st.error(f"❌ Erro na conversão de tipos: {e}")
            return None

        rename_dict = {}
        if col_data: rename_dict[col_data] = 'Data'
        if col_empresa: rename_dict[col_empresa] = 'Empresa'
        if col_saldo: rename_dict[col_saldo] = 'Saldo_Final'
        
        df_renamed = df.rename(columns=rename_dict).dropna(subset=['Data'])
        return df_renamed
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar o arquivo: {e}")
        return None

def process_data(df):
    """Processa os dados para agregação por empresa e ecossistema - SEM CACHE."""
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

def filtrar_dias_uteis(df):
    """Remove sábados e domingos do DataFrame."""
    return df[df['Data'].dt.dayofweek < 5]  # 0-4 = Segunda a Sexta

def agregar_por_granularidade(df, granularidade):
    """Agrega dados conforme a granularidade selecionada - retorna último valor do período."""
    df_temp = df.copy()
    
    if granularidade == "Semanal":
        df_temp['Periodo'] = df_temp['Data'].dt.to_period('W').apply(lambda x: x.start_time)
        periodo_label = "Semana"
        # Pegar último dia de cada semana POR EMPRESA separadamente
        df_agrupado = (
            df_temp.sort_values(['Empresa', 'Data'])
            .groupby(['Periodo', 'Empresa'])
            .tail(1)  # Pega o último registro de cada grupo
            .reset_index(drop=True)
            [['Periodo', 'Empresa', 'Saldo_do_Dia']]
        )
    elif granularidade == "Mensal":
        df_temp['Periodo'] = df_temp['Data'].dt.to_period('M').apply(lambda x: x.start_time)
        periodo_label = "Mês"
        # Pegar último dia de cada mês POR EMPRESA separadamente
        df_agrupado = (
            df_temp.sort_values(['Empresa', 'Data'])
            .groupby(['Periodo', 'Empresa'])
            .tail(1)  # Pega o último registro de cada grupo
            .reset_index(drop=True)
            [['Periodo', 'Empresa', 'Saldo_do_Dia']]
        )
    else:
        df_temp['Periodo'] = df_temp['Data']
        periodo_label = "Dia"
        # Para diário, manter como está
        df_agrupado = df_temp[['Periodo', 'Empresa', 'Saldo_do_Dia']].copy()
    
    return df_agrupado, periodo_label

def formatar_milhao(valor):
    """Formata valores em milhões."""
    return f"{valor/1_000_000:.1f}M"

# --- CARREGAR DADOS DO ARQUIVO LOCAL ---
if "arquivo_carregado" not in st.session_state:
    st.session_state.arquivo_carregado = None

# Botão para forçar atualização
if st.button("🔄 Atualizar Dados", help="Limpar cache e recarregar dados do Excel"):
    st.cache_data.clear()
    st.rerun()

df = load_data()

if df is None:
    st.stop()

# Validar colunas obrigatórias
required_columns = ['Data', 'Empresa', 'Saldo_Final']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    st.error(f"❌ Colunas obrigatórias não encontradas: {missing_columns}")
    st.error(f"Colunas encontradas: {list(df.columns)}")
    st.stop()

result = process_data(df)
if result[0] is None:
    st.stop()

df_consolidado, df_empresa_dia, df_ecossistema = result

# Buscar os 15 dias mais recentes que realmente contêm dados (definir antes das configurações)
datas_unicas = df_consolidado['Data'].drop_duplicates().sort_values(ascending=False)
datas_15_mais_recentes = datas_unicas.head(15)
data_mais_antiga_dos_15 = datas_15_mais_recentes.min()
data_mais_recente = datas_15_mais_recentes.max()

# Buscar a data mais antiga disponível nos dados para permitir seleção
data_mais_antiga_disponivel = datas_unicas.min()
data_mais_recente_disponivel = datas_unicas.max()

# --- CONFIGURAÇÕES COMPACTAS NO TOPO ---
with st.container():
    st.markdown('<div class="compact-controls">', unsafe_allow_html=True)
    st.markdown('<h4>⚙️ Configurações do Dashboard</h4>', unsafe_allow_html=True)
    
    col_config1, col_config2, col_config3, col_config4 = st.columns([2, 2, 2, 2])
    
    with col_config1:
        st.markdown("**📅 Data Inicial**")
        # Permitir seleção de qualquer data disponível, mas padrão nos 15 dias mais recentes
        periodo_inicio = st.date_input(
            "Período inicial",
            value=data_mais_antiga_dos_15.date(),
            min_value=data_mais_antiga_disponivel.date(),
            max_value=data_mais_recente_disponivel.date(),
            key="data_inicio",
            help="Pré-selecionado para os últimos 15 dias, mas pode escolher qualquer data disponível",
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
            help="Pré-selecionado para os últimos 15 dias, mas pode escolher qualquer data disponível",
            label_visibility="collapsed"
        )
    
    with col_config3:
        st.markdown("**🏢 Empresas**")
        empresas_disponveis = df_consolidado['Empresa'].unique().tolist()
        # Deixar apenas Alura pré-selecionado, remover Ecossistema da seleção padrão
        default_empresas = ['Alura']
        empresas_selecionadas = st.multiselect(
            "Selecionar Empresas",
            options=empresas_disponveis,
            default=[emp for emp in default_empresas if emp in empresas_disponveis],
            help="Selecione as empresas que deseja visualizar",
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

st.markdown('</div>', unsafe_allow_html=True)

# --- PROCESSAMENTO COM FILTROS ---
# Informar ao usuário sobre o período selecionado
if (pd.to_datetime(periodo_inicio) >= pd.to_datetime(data_mais_antiga_dos_15.date()) and 
    pd.to_datetime(periodo_fim) <= pd.to_datetime(data_mais_recente.date())):
    st.info(f"📅 **Período selecionado (últimos 15 dias):** {periodo_inicio.strftime('%d/%m/%Y')} até {periodo_fim.strftime('%d/%m/%Y')}")
else:
    st.info(f"📅 **Período selecionado:** {periodo_inicio.strftime('%d/%m/%Y')} até {periodo_fim.strftime('%d/%m/%Y')}")

# Aplicar filtros de data selecionados pelo usuário
df_filtrado = df_consolidado[
    (df_consolidado['Data'] >= pd.to_datetime(periodo_inicio)) &
    (df_consolidado['Data'] <= pd.to_datetime(periodo_fim)) &
    (df_consolidado['Empresa'].isin(empresas_selecionadas))
].copy()

df_plot, periodo_label = agregar_por_granularidade(df_filtrado, granularidade)

# --- MÉTRICAS PRINCIPAIS (SALDOS POR EMPRESA) - SEMPRE MOSTRAR TODAS ---
if not df_plot.empty:
    # Buscar dados do período selecionado (sem filtro de empresa)
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

    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🌐 Ecossistema", f"R$ {saldo_ecossistema/1_000_000:.1f}M", help="Saldo total do ecossistema")
        with col2:
            st.metric("🎓 Alura", f"R$ {saldo_alura/1_000_000:.1f}M", help="Saldo da Alura")
        with col3:
            st.metric("🏫 FIAP", f"R$ {saldo_fiap/1_000_000:.1f}M", help="Saldo da FIAP")
        with col4:
            st.metric("💼 PM3", f"R$ {saldo_pm3/1_000_000:.1f}M", help="Saldo da PM3")

# Reduzir espaçamento antes das abas
st.markdown('<div style="margin: 0.5rem 0;"></div>', unsafe_allow_html=True)

# --- ORGANIZAÇÃO COM ABAS (APENAS 2 ABAS) ---
tab1, tab2 = st.tabs(["📈 Gráfico e Dados", "📊 Análise por Empresa"])

# --- ABA 1: GRÁFICO PRINCIPAL E DADOS TABULARES ---
with tab1:
    if not df_plot.empty:
        with st.container(border=True):
            st.markdown(f"### 📈 Evolução dos Saldos ({granularidade})")
            
            # --- SISTEMA DE CORES DINÂMICAS ---
            def gerar_paleta_dinamica(empresas_selecionadas):
                """Gera paleta de cores dinâmica baseada nas empresas selecionadas"""
                # Paletas complementares para cada empresa principal
                paletas_complementares = {
                    'Alura': {  # Base azul
                        'Saldo do Ecossistema': '#1a1a1a',
                        'Alura': '#1976d2',
                        'FIAP': '#ff6b35',      # Laranja complementar
                        'PM3': '#4caf50',       # Verde
                        'Empresa Geral': '#ffc107', # Amarelo
                        'Casa do Código': '#795548', # Marrom
                        'Caelum': '#607d8b',    # Azul acinzentado
                        'INSTITUTO FIAP': '#ff6b35'
                    },
                    'FIAP': {  # Base rosa
                        'Saldo do Ecossistema': '#1a1a1a',
                        'Alura': '#2196f3',     # Azul complementar
                        'FIAP': '#e91e63',
                        'PM3': '#8bc34a',       # Verde claro
                        'Empresa Geral': '#ff9800', # Laranja
                        'Casa do Código': '#5d4037', # Marrom escuro
                        'Caelum': '#455a64',    # Cinza escuro
                        'INSTITUTO FIAP': '#e91e63'
                    },
                    'PM3': {  # Base roxo
                        'Saldo do Ecossistema': '#1a1a1a',
                        'Alura': '#00bcd4',     # Ciano
                        'FIAP': '#ff5722',      # Laranja avermelhado
                        'PM3': '#9c27b0',
                        'Empresa Geral': '#cddc39', # Lima
                        'Casa do Código': '#6d4c41', # Marrom médio
                        'Caelum': '#37474f',    # Cinza azulado
                        'INSTITUTO FIAP': '#ff5722'
                    }
                }
                
                # Determinar empresa principal (primeira selecionada ou Alura como padrão)
                empresa_principal = 'Alura'  # Padrão
                if empresas_selecionadas:
                    if 'Alura' in empresas_selecionadas:
                        empresa_principal = 'Alura'
                    elif 'FIAP' in empresas_selecionadas:
                        empresa_principal = 'FIAP'
                    elif 'PM3' in empresas_selecionadas:
                        empresa_principal = 'PM3'
                    else:
                        empresa_principal = empresas_selecionadas[0]
                
                # Retornar paleta baseada na empresa principal
                return paletas_complementares.get(empresa_principal, paletas_complementares['Alura'])
            
            # Gerar paleta dinâmica
            cores_empresas = gerar_paleta_dinamica(empresas_selecionadas)

            # Gráfico de linha com rótulos de dados abreviados em negrito (ex: R$ 1.2M)
            fig_line = px.line(
                df_plot,
                x='Periodo',
                y='Saldo_do_Dia',
                color='Empresa',
                markers=True,
                title=None,
                labels={'Saldo_do_Dia': 'Saldo (R$)', 'Periodo': periodo_label},
                color_discrete_map=cores_empresas,
                text=df_plot['Saldo_do_Dia'].apply(lambda x: f"<b>R$ {x/1_000_000:.1f}M</b>")
            )

            fig_line.update_layout(
                xaxis_title=f"{periodo_label}",
                yaxis_title="Saldo (R$)",
                legend_title="Empresa/Consolidado",
                hovermode='x unified',
                height=600,
                margin=dict(l=20, r=20, t=20, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=True,
                font=dict(family="Arial Black", size=12, color='white'),
                xaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)')
            )

            fig_line.update_traces(
                mode='lines+markers+text',
                line=dict(width=3),
                marker=dict(size=8),
                textposition="top center",
                textfont=dict(size=11, family="Arial Black", color='white'),
                showlegend=True
            )

            st.plotly_chart(fig_line, use_container_width=True)

        # --- DADOS TABULARES ORDENADOS POR DATA (MAIS RECENTE PRIMEIRO) ---
        st.markdown("### 🗃️ Dados Consolidados")
        
        # Preparar dados para tabela com data
        df_tabela = df_plot.copy()
        df_tabela['Data_Original'] = pd.to_datetime(df_tabela['Periodo'])
        df_tabela = df_tabela.sort_values(['Data_Original', 'Empresa'], ascending=[False, True])  # Data desc, empresa asc
        
        df_tabela['Data'] = df_tabela['Data_Original'].dt.strftime('%d/%m/%Y')
        df_tabela['Saldo_Formatado'] = df_tabela['Saldo_do_Dia'].apply(lambda x: f"R$ {x:,.0f}")
        
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
        
        # Botão de download
        csv_data = df_tabela[['Data', 'Empresa', 'Saldo_Formatado']].to_csv(index=False)
        st.download_button(
            label="📥 Baixar dados como CSV",
            data=csv_data,
            file_name=f"saldos_ecossistema_{periodo_inicio}_{periodo_fim}.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")

# --- ABA 2: ANÁLISE POR EMPRESA (MODIFICADA PARA MOSTRAR BANCOS) ---
with tab2:
    if not df_plot.empty:
        empresas_individuais = [emp for emp in empresas_selecionadas if emp != 'Saldo do Ecossistema']
        
        if empresas_individuais:
            with st.container(border=True):
                st.markdown("### 🏢 Saldos por Banco por Empresa")
                
                # Buscar dados originais (não agregados) do período selecionado para mostrar por banco
                df_banco_detalhado = df[
                    (df['Data'] >= pd.to_datetime(periodo_inicio)) &
                    (df['Data'] <= pd.to_datetime(periodo_fim)) &
                    (df['Empresa'].isin(empresas_individuais))
                ].copy()
                
                if not df_banco_detalhado.empty:
                    # Pegar última data de cada empresa/banco
                    ultima_data_por_empresa = df_banco_detalhado.groupby('Empresa')['Data'].max().reset_index()
                    
                    # Filtrar apenas os dados da última data de cada empresa
                    df_ultimo_dia_bancos = []
                    for _, row in ultima_data_por_empresa.iterrows():
                        empresa = row['Empresa']
                        ultima_data = row['Data']
                        dados_empresa = df_banco_detalhado[
                            (df_banco_detalhado['Empresa'] == empresa) & 
                            (df_banco_detalhado['Data'] == ultima_data)
                        ]
                        df_ultimo_dia_bancos.append(dados_empresa)
                    
                    if df_ultimo_dia_bancos:
                        df_bancos_final = pd.concat(df_ultimo_dia_bancos, ignore_index=True)
                        
                        # Verificar se existe coluna de banco
                        colunas_banco = [col for col in df_bancos_final.columns if 'banco' in col.lower()]
                        
                        if colunas_banco:
                            col_banco = colunas_banco[0]
                            
                            # Gráfico de barras empilhadas por banco
                            def gerar_cores_bancos_dinamicas(empresas_selecionadas):
                                """Gera cores de bancos baseadas na empresa principal selecionada"""
                                paletas_bancos = {
                                    'Alura': {  # Tons azuis e complementares
                                        'Itaú': '#1976d2',      # Azul principal
                                        'Bradesco': '#1565c0',  # Azul escuro
                                        'Santander': '#42a5f5', # Azul claro
                                        'Banco do Brasil': '#64b5f6', # Azul muito claro
                                        'Caixa': '#0d47a1',     # Azul muito escuro
                                        'BTG': '#2196f3',       # Azul médio
                                        'Inter': '#03a9f4',     # Azul ciano
                                        'Nubank': '#00bcd4',    # Ciano
                                        'C6 Bank': '#006064',   # Verde azulado escuro
                                        'Mercado Pago': '#0097a7' # Verde azulado
                                    },
                                    'FIAP': {  # Tons rosa e complementares
                                        'Itaú': '#e91e63',      # Rosa principal
                                        'Bradesco': '#c2185b',  # Rosa escuro
                                        'Santander': '#f06292', # Rosa claro
                                        'Banco do Brasil': '#f48fb1', # Rosa muito claro
                                        'Caixa': '#ad1457',     # Rosa muito escuro
                                        'BTG': '#ec407a',       # Rosa médio
                                        'Inter': '#e1bee7',     # Rosa claro violeta
                                        'Nubank': '#9c27b0',    # Roxo
                                        'C6 Bank': '#673ab7',   # Roxo escuro
                                        'Mercado Pago': '#3f51b5' # Azul violeta
                                    },
                                    'PM3': {  # Tons roxo e complementares
                                        'Itaú': '#9c27b0',      # Roxo principal
                                        'Bradesco': '#7b1fa2',  # Roxo escuro
                                        'Santander': '#ba68c8', # Roxo claro
                                        'Banco do Brasil': '#ce93d8', # Roxo muito claro
                                        'Caixa': '#4a148c',     # Roxo muito escuro
                                        'BTG': '#ab47bc',       # Roxo médio
                                        'Inter': '#8e24aa',     # Roxo escuro médio
                                        'Nubank': '#6a1b9a',    # Roxo escuro
                                        'C6 Bank': '#4527a0',   # Roxo azulado
                                        'Mercado Pago': '#311b92' # Roxo muito escuro
                                    }
                                }
                                
                                # Determinar empresa principal
                                empresa_principal = 'Alura'
                                if empresas_selecionadas:
                                    if 'Alura' in empresas_selecionadas:
                                        empresa_principal = 'Alura'
                                    elif 'FIAP' in empresas_selecionadas:
                                        empresa_principal = 'FIAP'
                                    elif 'PM3' in empresas_selecionadas:
                                        empresa_principal = 'PM3'
                                
                                return paletas_bancos.get(empresa_principal, paletas_bancos['Alura'])
                            
                            cores_bancos = gerar_cores_bancos_dinamicas(empresas_selecionadas)
                            
                            fig_stacked = px.bar(
                                df_bancos_final,
                                x='Empresa',
                                y='Saldo_Final',
                                color=col_banco,
                                title="Saldos por Banco (Empilhado)",
                                color_discrete_map=cores_bancos
                            )
                            
                            # Remover os rótulos de dados das barras
                            fig_stacked.update_traces(
                                texttemplate=None,
                                textposition=None
                            )
                            
                            fig_stacked.update_layout(
                                yaxis_title="Saldo (R$)",
                                xaxis_title="Empresa",
                                legend_title="Banco",
                                height=500,
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(family="Arial Black", size=12, color='white'),
                                xaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)'),
                                yaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)'),
                                showlegend=True
                            )
                            
                            st.plotly_chart(fig_stacked, use_container_width=True)
                            
                            # Tabela detalhada por banco
                            with st.expander("📋 Ver Saldos Detalhados por Banco"):
                                # Preparar dados para tabela
                                df_tabela_bancos = df_bancos_final.copy()
                                df_tabela_bancos['Data_Formatada'] = df_tabela_bancos['Data'].dt.strftime('%d/%m/%Y')
                                df_tabela_bancos['Saldo_Formatado'] = df_tabela_bancos['Saldo_Final'].apply(lambda x: f"R$ {x:,.0f}")
                                
                                # Ordenar por empresa e banco
                                df_tabela_bancos = df_tabela_bancos.sort_values(['Empresa', col_banco])
                                
                                # Criar tabela resumo por empresa
                                st.markdown("**Resumo por Empresa:**")
                                df_resumo_empresa = df_tabela_bancos.groupby('Empresa')['Saldo_Final'].sum().reset_index()
                                df_resumo_empresa['Saldo_Formatado'] = df_resumo_empresa['Saldo_Final'].apply(lambda x: f"R$ {x:,.0f}")
                                df_resumo_empresa['Participação'] = (df_resumo_empresa['Saldo_Final'] / df_resumo_empresa['Saldo_Final'].sum() * 100).round(2)
                                df_resumo_empresa['Participação'] = df_resumo_empresa['Participação'].apply(lambda x: f"{x}%")
                                
                                st.dataframe(
                                    df_resumo_empresa[['Empresa', 'Saldo_Formatado', 'Participação']].rename(columns={
                                        'Saldo_Formatado': 'Saldo Total (R$)',
                                        'Participação': 'Participação (%)'
                                    }),
                                    use_container_width=True,
                                    hide_index=True
                                )
                                
                                st.markdown("**Detalhamento por Banco:**")
                                st.dataframe(
                                    df_tabela_bancos[['Empresa', col_banco, 'Data_Formatada', 'Saldo_Formatado']].rename(columns={
                                        'Empresa': 'Empresa',
                                        col_banco: 'Banco',
                                        'Data_Formatada': 'Data',
                                        'Saldo_Formatado': 'Saldo (R$)'
                                    }),
                                    use_container_width=True,
                                    hide_index=True,
                                    height=400
                                )
                                
                                # Botão de download dos dados detalhados
                                csv_bancos = df_tabela_bancos[['Empresa', col_banco, 'Data_Formatada', 'Saldo_Formatado']].to_csv(index=False)
                                st.download_button(
                                    label="📥 Baixar dados por banco como CSV",
                                    data=csv_bancos,
                                    file_name=f"saldos_bancos_{periodo_inicio}_{periodo_fim}.csv",
                                    mime="text/csv"
                                )
                        else:
                            # Fallback: se não há coluna de banco, mostrar como antes
                            st.warning("⚠️ Coluna de banco não encontrada. Mostrando saldos totais por empresa.")
                            
                            df_empresas = df_plot[df_plot['Empresa'].isin(empresas_individuais)]
                            if not df_empresas.empty:
                                df_ultimo_periodo = df_empresas.groupby('Empresa')['Saldo_do_Dia'].last().reset_index()
                                
                                fig_bar = px.bar(
                                    df_ultimo_periodo,
                                    x='Empresa',
                                    y='Saldo_do_Dia',
                                    title="Saldo Atual por Empresa",
                                    color='Empresa',
                                    color_discrete_map=cores_empresas
                                )
                                
                                fig_bar.update_layout(
                                    yaxis_title="Saldo (R$)",
                                    showlegend=False,
                                    height=400,
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    font=dict(family="Arial Black", size=12, color='white'),
                                    xaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)'),
                                    yaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)')
                                )
                                
                                st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.warning("⚠️ Nenhum dado encontrado para as empresas selecionadas.")
        else:
            st.info("📋 Selecione empresas individuais nos filtros para ver o comparativo por banco.")

# --- FOOTER ---
st.markdown(
    """
    <div style='text-align: center; color: #666666; font-size: 0.9em; margin-top: 2rem;'>
        <div style="background: #1a1a1a; color: white; padding: 5px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; display: inline-block; margin-bottom: 10px;">ALUN</div>
        <br>
        📊 Dashboard de Saldos do Ecossistema | Atualizado automaticamente
    </div>
    """, 
    unsafe_allow_html=True
)