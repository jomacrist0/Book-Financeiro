import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="💰 Fluxo de Caixa",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CUSTOMIZADO COM TEMA ESCURO ---
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
 

# --- SIDEBAR COM LOGO ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 15px; margin-bottom: 2rem;">
        <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQwIiB2aWV3Qm94PSIwIDAgMTAwIDQwIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8dGV4dCB4PSI1MCIgeT0iMjUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyNCIgZm9udC13ZWlnaHQ9ImJvbGQiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5BTFVOPC90ZXh0Pgo8L3N2Zz4K" style="width: 120px; height: auto;">
        <div style="color: #ccc; font-size: 12px; margin-top: 10px;">Fluxo de Caixa</div>
    </div>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #fafafa; font-weight: 700; margin-bottom: 0;">💰 Dashboard de Fluxo de Caixa</h1>
    <p style="color: #ccc; font-size: 1.1em;">Análise completa das movimentações financeiras</p>
</div>
""", unsafe_allow_html=True)

# --- FUNÇÕES ---
@st.cache_data
def load_cashflow_data():
    """Carrega e processa os dados do arquivo CSV de fluxo de caixa."""
    # Tentar múltiplos caminhos possíveis com o nome correto do arquivo
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "2Alura - Fluxo de caixa.csv"),
        os.path.join(os.getcwd(), "data", "2Alura - Fluxo de caixa.csv"),
        os.path.join("data", "2Alura - Fluxo de caixa.csv"),
        os.path.join(os.path.dirname(__file__), "..", "2Alura - Fluxo de caixa.csv"),
        os.path.join(os.getcwd(), "2Alura - Fluxo de caixa.csv"),
        "2Alura - Fluxo de caixa.csv"
    ]
    
    csv_path = None
    for path in possible_paths:
        if os.path.exists(path):
            csv_path = path
            break
    
    if csv_path is None:
        st.error("❌ Arquivo '2Alura - Fluxo de caixa.csv' não encontrado!")
        st.info(f"📂 Procurado nos seguintes locais:\n" + "\n".join(possible_paths))
        return None
    
    try:
        # Tenta ler com separador ponto e vírgula primeiro
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
        
        # Verificar se carregou corretamente
        if df.shape[1] == 1:
            # Se só tem uma coluna, tenta outros separadores
            df = pd.read_csv(csv_path, sep=',', encoding='utf-8')
        
        # Limpar nomes das colunas
        df.columns = [col.strip() for col in df.columns if col.strip()]
        
        # Remover colunas vazias
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        # Converter Data
        if 'Data' in df.columns:
            df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')
        
        # Converter Valor - tratamento para formato brasileiro
        if 'Valor' in df.columns:
            df['Valor'] = (
                df['Valor']
                .astype(str)
                .str.replace('.', '', regex=False)  # Remove separador de milhares
                .str.replace(',', '.', regex=False)  # Troca vírgula por ponto
                .str.strip()
            )
            df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)
        
        # Garantir que colunas essenciais existam
        required_columns = ['Data', 'Valor', 'Movimentação']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"❌ Colunas obrigatórias não encontradas: {missing_columns}")
            return None
        
        # Filtrar dados válidos
        df = df.dropna(subset=['Data', 'Valor'])
        
        # Remover classificações intercompany
        if 'classif' in df.columns:
            df = df[~df['classif'].str.contains('transferência intercompany', case=False, na=False)]
        
        # Criar colunas calculadas
        df['Entradas'] = df['Valor'].where(df['Valor'] > 0, 0)
        df['Saidas'] = df['Valor'].where(df['Valor'] < 0, 0).abs()
        df['Saldo_Acumulado'] = df['Valor'].cumsum()
        df['Mes_Ano'] = df['Data'].dt.to_period('M')
        df['Ano'] = df['Data'].dt.year
        df['Mes'] = df['Data'].dt.month
        df['Dia_Semana'] = df['Data'].dt.day_name()
        df['Semana_Ano'] = df['Data'].dt.to_period('W')
        
        return df
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar o arquivo: {e}")
        return None

def format_currency(value):
    """Formatar valores em moeda brasileira sem centavos."""
    return f"R$ {value:,.0f}".replace(',', '.')

def format_percentage(value):
    """Formatar valores em porcentagem."""
    return f"{value:.2f}%"

def format_label_optimized(value):
    """Formatar rótulos de dados de forma otimizada para não poluir o gráfico."""
    if pd.isna(value) or value == 0:
        return ''
    
    abs_val = abs(value)
    if abs_val >= 1000000:  # Milhões
        return f'R$ {value/1000000:.1f}M'
    elif abs_val >= 1000:  # Milhares
        return f'R$ {value/1000:.0f}k'
    else:
        return f'R$ {value:.0f}'

def calculate_cashflow_metrics(df):
    """Calcular métricas principais do fluxo de caixa."""
    total_entradas = df['Entradas'].sum()
    total_saidas = df['Saidas'].sum()
    saldo_final = df['Saldo_Acumulado'].iloc[-1] if len(df) > 0 else 0
    fluxo_liquido = total_entradas - total_saidas
    
    return {
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo_final': saldo_final,
        'fluxo_liquido': fluxo_liquido
    }

def agrupar_por_granularidade(df, granularidade):
    """Agrupa os dados conforme a granularidade selecionada."""
    if granularidade == 'Diário':
        return df.groupby('Data').agg({
            'Entradas': 'sum',
            'Saidas': 'sum',
            'Valor': 'sum'
        }).reset_index()
    elif granularidade == 'Semanal':
        grouped = df.groupby('Semana_Ano').agg({
            'Entradas': 'sum',
            'Saidas': 'sum',
            'Valor': 'sum',
            'Data': 'min'
        }).reset_index()
        grouped['Periodo_Label'] = grouped['Semana_Ano'].astype(str)
        return grouped
    elif granularidade == 'Mensal':
        grouped = df.groupby('Mes_Ano').agg({
            'Entradas': 'sum',
            'Saidas': 'sum',
            'Valor': 'sum',
            'Data': 'min'
        }).reset_index()
        grouped['Periodo_Label'] = grouped['Mes_Ano'].astype(str)
        return grouped
    elif granularidade == 'Anual':
        grouped = df.groupby('Ano').agg({
            'Entradas': 'sum',
            'Saidas': 'sum',
            'Valor': 'sum',
            'Data': 'min'
        }).reset_index()
        grouped['Periodo_Label'] = grouped['Ano'].astype(str)
        return grouped

# >>> MOVER A FUNÇÃO DE CORES PARA AQUI (ANTES DAS ABAS) <<<
def aplicar_cor_individual(variacao_val, movimentacao):
    """Retorna CSS para célula da coluna Variação conforme movimentação."""
    if variacao_val in ("∞", "N/A", "0.00%"):
        return ""
    try:
        variacao_num = float(str(variacao_val).replace('%', ''))
    except:
        return ""
    # Intensidade normalizada
    intensidade = min(abs(variacao_num) / 50, 1)
    alpha = 0.3 + intensidade * 0.4  # 0.3 a 0.7
    if movimentacao == "Entrada":
        if variacao_num > 0:
            return f"background-color: rgba(0,128,0,{alpha}); color: white;"
        else:
            return f"background-color: rgba(128,0,0,{alpha}); color: white;"
    elif movimentacao == "Saída":
        if variacao_num < 0:
            return f"background-color: rgba(0,128,0,{alpha}); color: white;"
        else:
            return f"background-color: rgba(128,0,0,{alpha}); color: white;"
    return ""

# --- CARREGAR DADOS ---
# Botão para recarregar dados
col_reload, col_info = st.columns([1, 3])
with col_reload:
    if st.button("🔄 Atualizar Dados", help="Clique para recarregar os dados do CSV"):
        st.cache_data.clear()
        st.rerun()

with col_info:
    st.info("💡 Clique em 'Atualizar Dados' após modificar o arquivo CSV para ver as mudanças")

df = load_cashflow_data()
if df is None:
    st.stop()

# Verificar se o DataFrame não está vazio
if df.empty:
    st.error("❌ Nenhum dado válido encontrado no arquivo.")
    st.stop()

# --- FILTROS ---
with st.container():
    st.markdown('<div class="compact-controls">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Filtros do Dashboard")
    
    col_config1, col_config2, col_config3, col_config4 = st.columns([2, 2, 2, 2])
    
    with col_config1:
        data_min = df['Data'].min().date()
        data_max = df['Data'].max().date()
        
        # Definir período padrão de 8 semanas (56 dias)
        periodo_fim_default = data_max
        periodo_inicio_default = (data_max - timedelta(weeks=8))
        
        # Garantir que não seja anterior à data mínima
        if periodo_inicio_default < data_min:
            periodo_inicio_default = data_min
        
        periodo_inicio = st.date_input(
            "📅 Data inicial:",
            value=periodo_inicio_default,
            min_value=data_min,
            max_value=data_max,
            key="data_inicio_fluxo"
        )
    
    with col_config2:
        periodo_fim = st.date_input(
            "📅 Data final:",
            value=periodo_fim_default,
            min_value=data_min,
            max_value=data_max,
            key="data_fim_fluxo"
        )
    
    with col_config3:
        granularidade = st.selectbox(
            "📊 Granularidade:",
            options=['Diário', 'Semanal', 'Mensal', 'Anual'],
            index=1,  # Semanal pré-selecionado
            help="Selecione a granularidade para os gráficos"
        )
    
    with col_config4:
        # Adicionar filtro de empresa - CORRIGIR para pegar todas as empresas
        if 'Empresa' in df.columns:
            # Limpar e normalizar os nomes das empresas
            df['Empresa'] = df['Empresa'].astype(str).str.strip()
            empresas_disponiveis = sorted([emp for emp in df['Empresa'].dropna().unique() if emp != 'nan' and emp != ''])
            
            # Debug: mostrar empresas encontradas
            if len(empresas_disponiveis) > 0:
                # Pré-selecionar Alura se disponível
                default_empresas = ['Alura'] if 'Alura' in empresas_disponiveis else []
                empresas_selecionadas = st.multiselect(
                    "🏢 Empresa:",
                    options=empresas_disponiveis,
                    default=default_empresas,
                    help=f"Empresas disponíveis: {', '.join(empresas_disponiveis)}",
                    key="filtro_empresa_global"
                )
            else:
                st.warning("⚠️ Nenhuma empresa encontrada na coluna 'Empresa'")
                empresas_selecionadas = []
        else:
            # Verificar se existe uma coluna similar
            colunas_empresa = [col for col in df.columns if 'empresa' in col.lower()]
            if colunas_empresa:
                st.info(f"💡 Colunas encontradas com 'empresa': {colunas_empresa}")
                # Usar a primeira coluna encontrada
                col_empresa_encontrada = colunas_empresa[0]
                df[col_empresa_encontrada] = df[col_empresa_encontrada].astype(str).str.strip()
                empresas_disponiveis = sorted([emp for emp in df[col_empresa_encontrada].dropna().unique() if emp != 'nan' and emp != ''])
                
                # Pré-selecionar Alura se disponível
                default_empresas = ['Alura'] if 'Alura' in empresas_disponiveis else []
                empresas_selecionadas = st.multiselect(
                    f"🏢 {col_empresa_encontrada}:",
                    options=empresas_disponiveis,
                    default=default_empresas,
                    help=f"Empresas disponíveis: {', '.join(empresas_disponiveis)}",
                    key="filtro_empresa_global"
                )
            else:
                st.info("ℹ️ Coluna 'Empresa' não encontrada")
                empresas_selecionadas = []
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- APLICAR FILTROS ---
df_filtrado = df[
    (df['Data'] >= pd.to_datetime(periodo_inicio)) &
    (df['Data'] <= pd.to_datetime(periodo_fim))
]

# Aplicar filtro de empresa se selecionado
if empresas_selecionadas and 'Empresa' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['Empresa'].isin(empresas_selecionadas)]

# --- MÉTRICAS PRINCIPAIS ---
metricas = calculate_cashflow_metrics(df_filtrado)

col_met1, col_met2, col_met3, col_met4 = st.columns(4)
with col_met1:
    st.metric("💚 Total Entradas", format_currency(metricas['total_entradas']))
with col_met2:
    st.metric("💸 Total Saídas", format_currency(metricas['total_saidas']))
with col_met3:
    delta_color = "normal" if metricas['fluxo_liquido'] >= 0 else "inverse"
    st.metric("💰 Fluxo Líquido", format_currency(metricas['fluxo_liquido']))
with col_met4:
    st.metric("📊 Saldo Final", format_currency(metricas['saldo_final']))
# --- ORGANIZAÇÃO COM ABAS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Visão Geral", "📊 Análise Temporal", "⚖️ Comparativo", "💚 Análise de Entradas", "💸 Análise de Saídas"])

# --- ABA 1: VISÃO GERAL ---
with tab1:
    # Filtros específicos da aba Visão Geral
    st.markdown("##### 🔧 Filtros da Visão Geral")
    col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
    
    with col_filtro1:
        if 'classif' in df_filtrado.columns:
            classif_visao_geral = df_filtrado['classif'].dropna().unique().tolist()
            classif_selecionadas_vg = st.multiselect(
                "🏷️ Classificações:",
                options=classif_visao_geral,
                default=[],
                help="Selecione as classificações para a visão geral",
                key="classif_visao_geral"
            )
        else:
            classif_selecionadas_vg = []
    
    with col_filtro2:
        if 'Categoria - Caixa' in df_filtrado.columns:
            categorias_visao_geral = df_filtrado['Categoria - Caixa'].dropna().unique().tolist()
            categorias_selecionadas_vg = st.multiselect(
                "📊 Categorias:",
                options=categorias_visao_geral,
                default=[],
                help="Selecione as categorias para a visão geral",
                key="categorias_visao_geral"
            )
        else:
            categorias_selecionadas_vg = []
    
    with col_filtro3:
        if 'Banco' in df_filtrado.columns:
            bancos_visao_geral = df_filtrado['Banco'].dropna().unique().tolist()
            bancos_selecionados_vg = st.multiselect(
                "🏦 Bancos:",
                options=bancos_visao_geral,
                default=[],
                help="Selecione os bancos para a visão geral",
                key="bancos_visao_geral"
            )
        else:
            bancos_selecionados_vg = []
    
    # Aplicar filtros específicos da aba
    df_visao_geral = df_filtrado.copy()
    
    if classif_selecionadas_vg and 'classif' in df_visao_geral.columns:
        df_visao_geral = df_visao_geral[df_visao_geral['classif'].isin(classif_selecionadas_vg)]
    
    if categorias_selecionadas_vg and 'Categoria - Caixa' in df_visao_geral.columns:
        df_visao_geral = df_visao_geral[df_visao_geral['Categoria - Caixa'].isin(categorias_selecionadas_vg)]
    
    if bancos_selecionados_vg and 'Banco' in df_visao_geral.columns:
        df_visao_geral = df_visao_geral[df_visao_geral['Banco'].isin(bancos_selecionados_vg)]
    # Usar os dados já filtrados globalmente
    df_visao_geral = df_visao_geral.copy()
    
    # Gráfico de cascata por categoria (Operacional vs Financiamento) com drill down
    st.markdown("#### 🌊 Análise de Cascata - Operacional vs Financiamento")
    
    # Controle de drill down - lado a lado
    col_drill1, col_drill2 = st.columns([1, 1])
    
    with col_drill1:
        drill_level = st.radio(
            "Nível de Detalhe:",
            options=["Categoria", "Classificação"],
            index=0,
            key="drill_level",
            horizontal=True
        )
    
    with col_drill2:
        st.info("💡 Alterne entre 'Categoria' e 'Classificação' para diferentes níveis de detalhe.")
    
    # Agrupar por categoria ou classificação baseado no drill down
    if 'Categoria - Caixa' in df_visao_geral.columns:
        if drill_level == "Categoria":
            agrupamento_col = 'Categoria - Caixa'
            titulo_waterfall = "Fluxo de Caixa por Categoria"
        else:  # Classificação
            agrupamento_col = 'classif'
            titulo_waterfall = "Fluxo de Caixa por Classificação"
        
        if agrupamento_col in df_visao_geral.columns:
            categoria_movs = df_visao_geral.groupby(agrupamento_col)['Valor'].sum().reset_index()
            categoria_movs = categoria_movs.sort_values('Valor', key=abs, ascending=False)
            
            # Preparar dados para o waterfall
            categorias = categoria_movs[agrupamento_col].tolist()
            valores = categoria_movs['Valor'].tolist()
            
            # CORRIGIR: Calcular saldo anterior baseado nos dados filtrados
            # Pegar transações anteriores ao período selecionado
            data_inicio_periodo = pd.to_datetime(periodo_inicio)
            df_anterior = df[df['Data'] < data_inicio_periodo]
            saldo_anterior = df_anterior['Valor'].sum() if len(df_anterior) > 0 else 0
            
            # Obter datas para os rótulos de saldo
            data_inicial = df_visao_geral['Data'].min().strftime('%d/%m/%Y')
            data_final = df_visao_geral['Data'].max().strftime('%d/%m/%Y')
            
            # Criar listas para o gráfico waterfall
            x_vals = [f'Saldo Inicial\n{data_inicial}'] + categorias + [f'Saldo Final\n{data_final}']
            y_vals = [saldo_anterior] + valores + [0]  # O saldo final será calculado automaticamente
            measure_vals = ['absolute'] + ['relative'] * len(valores) + ['total']
            
            # Criar rótulos de dados otimizados
            text_labels = [format_label_optimized(val) for val in y_vals]
            
            fig_waterfall = go.Figure(go.Waterfall(
                name="Fluxo de Caixa",
                orientation="v",
                measure=measure_vals,
                x=x_vals,
                y=y_vals,
                connector={"line": {"color": "rgb(63, 63, 63)"}},
                decreasing={"marker": {"color": "red"}},
                increasing={"marker": {"color": "green"}},
                totals={"marker": {"color": "blue"}},
                text=text_labels,
                textposition='outside',
                textfont=dict(size=10, color='white', family='Arial Black')
            ))
            
            fig_waterfall.update_layout(
                title=titulo_waterfall,
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis={'tickangle': 45}
            )
            
            # Formatar eixo Y para não mostrar centavos
            fig_waterfall.update_yaxes(tickformat='.0f')
            
            st.plotly_chart(fig_waterfall, use_container_width=True)
        else:
            st.info(f"ℹ️ Coluna '{agrupamento_col}' não encontrada para análise de cascata.")
    else:
        st.info("ℹ️ Coluna 'Categoria - Caixa' não encontrada para análise de cascata.")
    
    # Tabela de transações detalhadas (substituindo o Top 10)
    st.markdown("#### 📋 Transações Detalhadas")
    
    # Preparar dados para exibição - ADICIONAR EMPRESA
    colunas_exibir = ['Data', 'Descrição', 'Valor', 'Banco', 'Movimentação']
    if 'Empresa' in df_visao_geral.columns:
        colunas_exibir.insert(-1, 'Empresa')  # Inserir antes da última coluna
    if 'classif' in df_visao_geral.columns:
        colunas_exibir.insert(-1, 'classif')  # Inserir antes da última coluna
    
    df_exibir_vg = df_visao_geral[colunas_exibir].copy()
    
    # Formatar a data e o valor
    df_exibir_vg['Data'] = df_exibir_vg['Data'].dt.strftime('%d/%m/%Y')
    df_exibir_vg['Valor'] = df_exibir_vg['Valor'].apply(lambda x: f"R$ {x:,.0f}".replace(",", "."))
    
    # Ordenar por valor absoluto decrescente (maior para menor) por padrão
    df_exibir_vg_ordenado = df_visao_geral[colunas_exibir].copy()
    df_exibir_vg_ordenado = df_exibir_vg_ordenado.reindex(df_exibir_vg_ordenado['Valor'].abs().sort_values(ascending=False).index)
    
    # Aplicar formatação após ordenação
    df_exibir_vg_ordenado['Data'] = df_exibir_vg_ordenado['Data'].dt.strftime('%d/%m/%Y')
    df_exibir_vg_ordenado['Valor'] = df_exibir_vg_ordenado['Valor'].apply(lambda x: f"R$ {x:,.0f}".replace(",", "."))
    
    # Renomear colunas para exibição
    colunas_nomes = ['Data', 'Descrição', 'Valor', 'Banco']
    if 'Empresa' in df_visao_geral.columns:
        colunas_nomes.append('Empresa')
    if 'classif' in df_visao_geral.columns:
        colunas_nomes.append('Classificação')
    colunas_nomes.append('Movimentação')
    
    df_exibir_vg_ordenado.columns = colunas_nomes
    
    st.dataframe(df_exibir_vg_ordenado, use_container_width=True, height=500)
    
    # REMOVER os cards de estatísticas - comentar ou apagar esta seção
    # col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
    # 
    # with col_stats1:
    #     st.metric("📊 Total Transações", f"{len(df_visao_geral):,}")
    # with col_stats2:
    #     media_transacao = df_visao_geral['Valor'].mean()
    #     st.metric("📈 Valor Médio", format_currency(media_transacao))
    # with col_stats3:
    #     maior_entrada = df_visao_geral[df_visao_geral['Valor'] > 0]['Valor'].max() if len(df_visao_geral[df_visao_geral['Valor'] > 0]) > 0 else 0
    #     st.metric("💚 Maior Entrada", format_currency(maior_entrada))
    # with col_stats4:
    #     maior_saida = df_visao_geral[df_visao_geral['Valor'] < 0]['Valor'].min() if len(df_visao_geral[df_visao_geral['Valor'] < 0]) > 0 else 0
    #     st.metric("💸 Maior Saída", format_currency(maior_saida))

# --- ABA 2: ANÁLISE TEMPORAL ---
with tab2:
    # Filtros específicos da aba Análise Temporal (mesma lógica da Visão Geral)
    st.markdown("##### 🔧 Filtros da Análise Temporal")
    col_temp1, col_temp2, col_temp3 = st.columns(3)

    with col_temp1:
        if 'classif' in df_filtrado.columns:
            classif_temporal_opts = df_filtrado['classif'].dropna().unique().tolist()
            classif_sel_temp = st.multiselect(
                "🏷️ Classificações:",
                options=classif_temporal_opts,
                default=[],
                help="Selecione as classificações para a análise temporal",
                key="classif_temporal"
            )
        else:
            classif_sel_temp = []

    with col_temp2:
        if 'Categoria - Caixa' in df_filtrado.columns:
            cat_temporal_opts = df_filtrado['Categoria - Caixa'].dropna().unique().tolist()
            cat_sel_temp = st.multiselect(
                "📊 Categorias:",
                options=cat_temporal_opts,
                default=[],
                help="Selecione as categorias para a análise temporal",
                key="categorias_temporal"
            )
        else:
            cat_sel_temp = []

    with col_temp3:
        if 'Banco' in df_filtrado.columns:
            bancos_temporal_opts = df_filtrado['Banco'].dropna().unique().tolist()
            bancos_sel_temp = st.multiselect(
                "🏦 Bancos:",
                options=bancos_temporal_opts,
                default=[],
                help="Selecione os bancos para a análise temporal",
                key="bancos_temporal"
            )
        else:
            bancos_sel_temp = []

    # Aplicar filtros
    df_temporal = df_filtrado.copy()
    if classif_sel_temp and 'classif' in df_temporal.columns:
        df_temporal = df_temporal[df_temporal['classif'].isin(classif_sel_temp)]
    if cat_sel_temp and 'Categoria - Caixa' in df_temporal.columns:
        df_temporal = df_temporal[df_temporal['Categoria - Caixa'].isin(cat_sel_temp)]
    if bancos_sel_temp and 'Banco' in df_temporal.columns:
        df_temporal = df_temporal[df_temporal['Banco'].isin(bancos_sel_temp)]
    st.markdown("#### 📊 Entradas e Saídas por Granularidade")

    # Agrupar dados por granularidade após filtros
    df_agrupado = agrupar_por_granularidade(df_temporal, granularidade)
    
    # Separar entradas e saídas
    df_entradas = df_agrupado[df_agrupado['Valor'] >= 0].groupby('Data')['Valor'].sum().reset_index()
    df_saidas = df_agrupado[df_agrupado['Valor'] < 0].groupby('Data')['Valor'].sum().abs().reset_index()
    
    # Calcular variação em valor absoluto
    if granularidade == 'Diário':
        x_axis = df_agrupado['Data'].unique()
        x_axis = pd.Series(pd.to_datetime(x_axis)).sort_values().values
    else:
        periodo_dados = df_agrupado.groupby('Periodo_Label')['Valor'].sum().reset_index()
        x_axis = periodo_dados['Periodo_Label']
    
    # Preparar dados para o gráfico: entradas positivas, saídas negativas e fluxo líquido
    entradas_valores = []        # valores >= 0
    saidas_valores_pos = []      # magnitudes positivas (serão convertidas para negativas na plotagem)
    fluxo_liquido_valores = []   # entrada - saída

    for x in x_axis:
        if granularidade == 'Diário':
            entrada_val = df_entradas[df_entradas['Data'] == x]['Valor'].sum()
            saida_mag = df_saidas[df_saidas['Data'] == x]['Valor'].sum()
        else:
            if 'Entradas' in df_agrupado.columns and 'Saidas' in df_agrupado.columns:
                filtro = (df_agrupado['Periodo_Label'] == x)
                entrada_val = df_agrupado.loc[filtro, 'Entradas'].sum()
                saida_mag = df_agrupado.loc[filtro, 'Saidas'].sum()
            else:
                entrada_val = df_agrupado[df_agrupado['Periodo_Label'] == x]['Valor'].apply(lambda v: v if v >= 0 else 0).sum()
                saida_mag = df_agrupado[df_agrupado['Periodo_Label'] == x]['Valor'].apply(lambda v: abs(v) if v < 0 else 0).sum()

        entradas_valores.append(entrada_val)
        saidas_valores_pos.append(saida_mag)
        fluxo_liquido_valores.append(entrada_val - saida_mag)
    
    # Criar gráfico de barras empilhadas com linha de variação
    
    # --- SISTEMA DE CORES DINÂMICAS ---
    def gerar_cores_fluxo_dinamicas(empresas_selecionadas):
        """Gera cores para gráficos de fluxo baseadas na empresa principal"""
        paletas_fluxo = {
            'Alura': {  # Base azul
                'entradas': '#4caf50',    # Verde
                'saidas': '#f44336',      # Vermelho
                'fluxo_positivo': '#1976d2',  # Azul principal
                'fluxo_negativo': '#d32f2f'   # Vermelho escuro
            },
            'FIAP': {  # Base rosa
                'entradas': '#8bc34a',    # Verde claro
                'saidas': '#ff5722',      # Laranja avermelhado
                'fluxo_positivo': '#e91e63', # Rosa principal
                'fluxo_negativo': '#c62828'   # Vermelho
            },
            'PM3': {  # Base roxo
                'entradas': '#66bb6a',    # Verde médio
                'saidas': '#ff7043',      # Laranja
                'fluxo_positivo': '#9c27b0', # Roxo principal
                'fluxo_negativo': '#d84315'   # Laranja escuro
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
        
        return paletas_fluxo.get(empresa_principal, paletas_fluxo['Alura'])
    
    cores_fluxo = gerar_cores_fluxo_dinamicas(empresas_selecionadas)
    fig_temporal = go.Figure()
    
    # Barras de entradas (base) - AUMENTAR TAMANHO DOS RÓTULOS
    fig_temporal.add_trace(go.Bar(
        x=x_axis,
        y=entradas_valores,
        name='Entradas',
        marker_color=cores_fluxo['entradas'],
        opacity=0.8,
        text=[format_label_optimized(val) for val in entradas_valores],
        textposition='inside',
        textfont=dict(size=14, color='white', family="Arial Black")  # Aumentado de 10 para 14
    ))
    
    # Barras de saídas (negativas) - ADICIONAR RÓTULOS E AUMENTAR TAMANHO
    fig_temporal.add_trace(go.Bar(
        x=x_axis,
        y=[-v for v in saidas_valores_pos],
        name='Saídas',
        marker_color=cores_fluxo['saidas'],
        opacity=0.85,
        text=[format_label_optimized(val) for val in saidas_valores_pos],  # ADICIONADO rótulos nas saídas
        textposition='inside',  # MUDADO de 'outside' para 'inside'
        textfont=dict(size=14, color='white', family="Arial Black")  # Aumentado de 10 para 14
    ))
    
    # Linha de fluxo líquido (entrada - saída)
    fig_temporal.add_trace(go.Scatter(
        x=x_axis,
        y=fluxo_liquido_valores,
        mode='lines+markers+text',
        name='Fluxo Líquido',
        line=dict(color=cores_fluxo['fluxo_positivo'], width=3),
        marker=dict(size=8, color=cores_fluxo['fluxo_positivo'], line=dict(width=2, color='white')),
        text=[format_label_optimized(val) for val in fluxo_liquido_valores],
        textposition='top center',
        textfont=dict(size=9, color='white', family='Arial Black')
    ))
    
    # Layout do gráfico temporal
    fig_temporal.update_layout(
        title="Entradas (Positivas) e Saídas (Negativas)",
        xaxis_title="Período",
        yaxis_title="Valor (R$)",
        barmode='relative',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    # Linha zero destacada
    fig_temporal.add_hline(y=0, line_width=1, line_color='white', opacity=0.5)
    # Formatar eixo Y sem decimais
    fig_temporal.update_yaxes(tickformat='.0f')
    
    st.plotly_chart(fig_temporal, use_container_width=True)

# --- INSIGHTS AUTOMÁTICOS ---
with st.expander("🔍 Insights Automáticos do Fluxo de Caixa"):
    # Análises automáticas
    dias_analisados = (periodo_fim - periodo_inicio).days + 1
    fluxo_medio_diario = metricas['fluxo_liquido'] / dias_analisados if dias_analisados > 0 else 0
    
    # Maior entrada e saída
    maior_entrada = df_temporal[df_temporal['Valor'] > 0]['Valor'].max() if len(df_temporal[df_temporal['Valor'] > 0]) > 0 else 0
    maior_saida = abs(df_temporal[df_temporal['Valor'] < 0]['Valor'].min()) if len(df_temporal[df_temporal['Valor'] < 0]) > 0 else 0
    
    # Categoria mais movimentada
    if 'Categoria - Caixa' in df_temporal.columns:
        categoria_mais_movimentada = df_temporal['Categoria - Caixa'].value_counts().index[0]
    else:
        categoria_mais_movimentada = "N/A"
    
    # Banco mais usado
    if 'Banco' in df_temporal.columns:
        banco_mais_usado = df_temporal['Banco'].value_counts().index[0]
    else:
        banco_mais_usado = "N/A"
    
    st.markdown(f"""
    **📊 Resumo Executivo do Período:**
    
    - **Período Analisado**: {periodo_inicio} até {periodo_fim} ({dias_analisados} dias)
    - **Fluxo Líquido**: {format_currency(metricas['fluxo_liquido'])} ({'Positivo ✅' if metricas['fluxo_liquido'] >= 0 else 'Negativo ❌'})
    - **Fluxo Médio Diário**: {format_currency(fluxo_medio_diario)}
    - **Maior Entrada**: {format_currency(maior_entrada)}
    - **Maior Saída**: {format_currency(maior_saida)}
    - **Categoria Mais Movimentada**: {categoria_mais_movimentada}
    - **Banco Mais Utilizado**: {banco_mais_usado}
    - **Total de Transações**: {len(df_filtrado):,} movimentações
    """)

# --- FOOTER ---
st.markdown(
    """
    <div style='text-align: center; color: #666666; font-size: 0.9em; margin-top: 2rem;'>
        <div style="background: #1a1a1a; color: white; padding: 5px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; display: inline-block; margin-bottom: 10px;">ALUN</div>
        <br>
        💰 Dashboard de Fluxo de Caixa | Análise Completa das Movimentações Financeiras
    </div>
    """, 
    unsafe_allow_html=True
)

# --- ABA 3: COMPARATIVO ---
with tab3:
    st.markdown("#### ⚖️ Análise Comparativa de Períodos")
    
    # REMOVER o controle de escala de cores
    # col_cor, col_info = st.columns([1, 3])
    # with col_cor:
    #     usar_escala_cores = st.checkbox("🎨 Ativar Escala de Cores", key="escala_cores_comparativo")
    # with col_info:
    #     if usar_escala_cores:
    #         st.info("💡 Entradas: Verde (↑) / Vermelho (↓) | Saídas: Verde (↓) / Vermelho (↑)")
    
    # FORÇAR escala de cores sempre ativa
    usar_escala_cores = True
    st.info("💡 Escala de Cores: Entradas: Verde (↑) / Vermelho (↓) | Saídas: Verde (↓) / Vermelho (↑)")
    
    col_comp1, col_comp2, col_comp3, col_comp4 = st.columns(4)
    with col_comp1:
        periodo_analise_inicio = st.date_input("📅 Período Análise - Início:", value=periodo_inicio_default, min_value=data_min, max_value=data_max, key="comp_analise_inicio")
    with col_comp2:
        periodo_analise_fim = st.date_input("📅 Período Análise - Fim:", value=periodo_fim_default, min_value=data_min, max_value=data_max, key="comp_analise_fim")
    with col_comp3:
        dias_analise = (periodo_analise_fim - periodo_analise_inicio).days
        periodo_comp_fim_default = periodo_analise_inicio - timedelta(days=1)
        periodo_comp_inicio_default = periodo_comp_fim_default - timedelta(days=dias_analise)
        if periodo_comp_inicio_default < data_min:
            periodo_comp_inicio_default = data_min
        periodo_comp_inicio = st.date_input("📅 Período Comparação - Início:", value=periodo_comp_inicio_default, min_value=data_min, max_value=data_max, key="comp_comparacao_inicio")
    with col_comp4:
        periodo_comp_fim = st.date_input("📅 Período Comparação - Fim:", value=periodo_comp_fim_default, min_value=data_min, max_value=data_max, key="comp_comparacao_fim")

    df_analise = df[(df['Data'] >= pd.to_datetime(periodo_analise_inicio)) & (df['Data'] <= pd.to_datetime(periodo_analise_fim))]
    df_comparacao = df[(df['Data'] >= pd.to_datetime(periodo_comp_inicio)) & (df['Data'] <= pd.to_datetime(periodo_comp_fim))]

    if df_analise.empty or df_comparacao.empty:
        st.warning("⚠️ Um dos períodos não possui dados suficientes para comparação.")
    else:
        def calc_variacao_compare(comparacao, analise):
            analise_abs = abs(analise)
            comparacao_abs = abs(comparacao)
            if analise_abs == 0:
                return "0.00%" if comparacao_abs == 0 else "∞"
            return f"{((comparacao_abs - analise_abs)/analise_abs*100):.2f}%"

        # Obter os rótulos das datas para as colunas
        label_analise = f"{periodo_analise_inicio.strftime('%d/%m/%Y')} - {periodo_analise_fim.strftime('%d/%m/%Y')}"
        label_comparacao = f"{periodo_comp_inicio.strftime('%d/%m/%Y')} - {periodo_comp_fim.strftime('%d/%m/%Y')}"

        def create_comparison_table(df_filtered, movimentacao_tipo, titulo):
            """Criar tabela de comparação para um tipo específico de movimentação"""
            if 'classif' in df_filtered.columns and 'Movimentação' in df_filtered.columns:
                # Filtrar por tipo de movimentação
                df_analise_filtered = df_analise[df_analise['Movimentação'] == movimentacao_tipo]
                df_comparacao_filtered = df_comparacao[df_comparacao['Movimentação'] == movimentacao_tipo]
                
                if df_analise_filtered.empty and df_comparacao_filtered.empty:
                    return None
                
                analise_grp = df_analise_filtered.groupby('classif')['Valor'].sum()
                comparacao_grp = df_comparacao_filtered.groupby('classif')['Valor'].sum()
                
                chaves = sorted(set(analise_grp.index) | set(comparacao_grp.index))
                
                if not chaves:
                    return None

                linhas = {
                    'Classificação': [],
                    label_analise: [],
                    label_comparacao: [],
                    'Variação': []
                }
                
                for classif in chaves:
                    v_a = analise_grp.get(classif, 0)
                    v_c = comparacao_grp.get(classif, 0)
                    
                    linhas['Classificação'].append(classif)
                    linhas[label_analise].append(format_currency(abs(v_a)))
                    linhas[label_comparacao].append(format_currency(abs(v_c)))
                    linhas['Variação'].append(calc_variacao_compare(v_c, v_a))
                
                return pd.DataFrame(linhas)
            return None

        def apply_color_styling(df_tabela, movimentacao_tipo):
            """Aplicar estilo de cores baseado no tipo de movimentação"""
            if not usar_escala_cores or df_tabela is None:
                return df_tabela
            
            def colorir_variacao(val):
                if val in ("∞", "N/A", "0.00%"):
                    return ""
                try:
                    variacao_num = float(str(val).replace('%', ''))
                except:
                    return ""
                
                intensidade = min(abs(variacao_num) / 50, 1)
                alpha = 0.3 + intensidade * 0.4
                
                if movimentacao_tipo == "Entradas":
                    # Entradas: Verde para positivo, Vermelho para negativo
                    if variacao_num > 0:
                        return f"background-color: rgba(0,128,0,{alpha}); color: white; font-weight: bold;"
                    else:
                        return f"background-color: rgba(128,0,0,{alpha}); color: white; font-weight: bold;"
                else:  # Saídas
                    # Saídas: Verde para negativo (redução), Vermelho para positivo (aumento)
                    if variacao_num < 0:
                        return f"background-color: rgba(0,128,0,{alpha}); color: white; font-weight: bold;"
                    else:
                        return f"background-color: rgba(128,0,0,{alpha}); color: white; font-weight: bold;"
            
            return df_tabela.style.applymap(colorir_variacao, subset=['Variação'])

        # Criar tabela de ENTRADAS
        st.markdown("##### 💚 Comparativo de Entradas por Classificação")
        df_entradas_comp = create_comparison_table(df_analise, "Entradas", "Entradas")
        
        if df_entradas_comp is not None and not df_entradas_comp.empty:
            styled_entradas = apply_color_styling(df_entradas_comp, "Entradas")
            st.dataframe(styled_entradas, use_container_width=True, height=300)
            
            # Resumo das entradas
            col_ent1, col_ent2, col_ent3 = st.columns(3)
            with col_ent1:
                total_entradas_analise = df_analise[df_analise['Movimentação'] == 'Entradas']['Valor'].sum()
                st.metric(f"💚 Total Entradas - {label_analise}", format_currency(abs(total_entradas_analise)))
            with col_ent2:
                total_entradas_comparacao = df_comparacao[df_comparacao['Movimentação'] == 'Entradas']['Valor'].sum()
                st.metric(f"💚 Total Entradas - {label_comparacao}", format_currency(abs(total_entradas_comparacao)))
            with col_ent3:
                variacao_total_entradas = calc_variacao_compare(total_entradas_comparacao, total_entradas_analise)
                st.metric("📈 Variação Total", variacao_total_entradas)
        else:
            st.info("ℹ️ Nenhuma entrada encontrada para os períodos selecionados.")
        # Criar tabela de SAÍDAS
        st.markdown("##### 💸 Comparativo de Saídas por Classificação")
        df_saidas_comp = create_comparison_table(df_analise, "Saídas", "Saídas")
        
        if df_saidas_comp is not None and not df_saidas_comp.empty:
            styled_saidas = apply_color_styling(df_saidas_comp, "Saídas")
            st.dataframe(styled_saidas, use_container_width=True, height=300)
            
            # Resumo das saídas
            col_sai1, col_sai2, col_sai3 = st.columns(3)
            with col_sai1:
                total_saidas_analise = df_analise[df_analise['Movimentação'] == 'Saídas']['Valor'].sum()
                st.metric(f"💸 Total Saídas - {label_analise}", format_currency(abs(total_saidas_analise)))
            with col_sai2:
                total_saidas_comparacao = df_comparacao[df_comparacao['Movimentação'] == 'Saídas']['Valor'].sum()
                st.metric(f"💸 Total Saídas - {label_comparacao}", format_currency(abs(total_saidas_comparacao)))
            with col_sai3:
                variacao_total_saidas = calc_variacao_compare(total_saidas_comparacao, total_saidas_analise)
                st.metric("📉 Variação Total", variacao_total_saidas)
        else:
            st.info("ℹ️ Nenhuma saída encontrada para os períodos selecionados.")

# --- ABA 4: ANÁLISE DE ENTRADAS ---
with tab4:
    st.markdown("#### 💚 Análise Detalhada de Entradas")
    
    # Filtrar apenas entradas
    df_entradas = df_filtrado[df_filtrado['Valor'] > 0].copy()
    
    # Filtros
    col_search1, col_search2, col_search3 = st.columns([2, 2, 1])
    
    with col_search1:
        filtro_empresa = st.text_input(
            "🔍 Buscar por empresa/descrição:",
            placeholder="Digite o nome da empresa ou parte da descrição...",
            key="filtro_entrada_empresa"
        )
    
    with col_search2:
        # Filtro de classificações
        if 'classif' in df_entradas.columns:
            classificacoes_disponveis = df_entradas['classif'].dropna().unique().tolist()
            classificacoes_selecionadas = st.multiselect(
                "🏷️ Classificações:",
                options=sorted(classificacoes_disponveis),
                default=classificacoes_disponveis,
                key="filtro_entrada_classif"
            )
        else:
            classificacoes_selecionadas = None
    
    with col_search3:
        if st.button("🔄 Limpar Filtro", key="limpar_entrada"):
            st.rerun()
    
    # Aplicar filtros
    df_entradas_filtrado = df_entradas.copy()
    
    if filtro_empresa:
        mask = (
            df_entradas_filtrado['Descrição'].str.contains(filtro_empresa, case=False, na=False) |
            (df_entradas_filtrado['Banco'].str.contains(filtro_empresa, case=False, na=False) if 'Banco' in df_entradas_filtrado.columns else False)
        )
        df_entradas_filtrado = df_entradas_filtrado[mask]
    
    # Só filtrar por classificação se alguma foi selecionada (se não estiver vazio)
    if classificacoes_selecionadas is not None and len(classificacoes_selecionadas) > 0:
        df_entradas_filtrado = df_entradas_filtrado[df_entradas_filtrado['classif'].isin(classificacoes_selecionadas)]
    
    if df_entradas_filtrado.empty:
        st.warning("⚠️ Nenhuma entrada encontrada com os filtros aplicados.")
    else:
        # Agrupar por granularidade
        df_entradas_agrupado = agrupar_por_granularidade(df_entradas_filtrado, granularidade)
        
        # Preparar dados para o gráfico
        if granularidade == 'Diário':
            x_vals = df_entradas_agrupado['Data']
            periodo_labels = x_vals
        else:
            x_vals = df_entradas_agrupado['Periodo_Label']
            periodo_labels = x_vals
        
        y_vals = df_entradas_agrupado['Valor']
        
        # Calcular variação percentual
        variacao_pct = y_vals.pct_change() * 100
        
        # Criar gráfico combinado
        fig_entradas = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Barras para volume
        fig_entradas.add_trace(go.Bar(
            x=periodo_labels,
            y=y_vals,
            name='Volume de Entradas',
            marker_color='green',
            text=[format_label_optimized(val) for val in y_vals],
            textposition='outside',
            textfont=dict(color='white', family='Arial Black')
        ), secondary_y=False)
        
        # Linha para variação
        fig_entradas.add_trace(go.Scatter(
            x=periodo_labels,
            y=variacao_pct,
            name='Variação (%)',
            mode='lines+markers+text',
            line=dict(color='orange', width=3),
            text=[f'{v:.1f}%' if not pd.isna(v) else '' for v in variacao_pct],
            textposition='top center',
            textfont=dict(color='white', family='Arial Black'),
            connectgaps=True
        ), secondary_y=True)
        
        fig_entradas.update_yaxes(title_text='Volume (R$)', secondary_y=False)
        fig_entradas.update_yaxes(title_text='Variação (%)', secondary_y=True)
        fig_entradas.update_layout(
            height=500,
            title=f'Histórico de Entradas - {granularidade}',
            xaxis_title='Período',
            margin=dict(t=100, b=60, l=100, r=60),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_entradas, use_container_width=True)
        
        # Tabela detalhada de entradas
        st.markdown("##### 📊 Detalhamento das Entradas")
        
        colunas_entrada = ['Data', 'Descrição', 'Valor', 'Banco']
        if 'Empresa' in df_entradas_filtrado.columns:
            colunas_entrada.insert(1, 'Empresa')  # Adiciona Empresa após Data
        if 'classif' in df_entradas_filtrado.columns:
            colunas_entrada.append('classif')
        if 'Memorando' in df_entradas_filtrado.columns:
            colunas_entrada.append('Memorando')
        elif 'memorando' in df_entradas_filtrado.columns:
            colunas_entrada.append('memorando')
        
        df_entrada_exibir = df_entradas_filtrado[colunas_entrada].copy()
        df_entrada_exibir = df_entrada_exibir.sort_values('Valor', ascending=False)
        df_entrada_exibir['Data'] = df_entrada_exibir['Data'].dt.strftime('%d/%m/%Y')
        df_entrada_exibir['Valor'] = df_entrada_exibir['Valor'].apply(lambda x: f"R$ {x:,.0f}".replace(",", "."))
        
        # Renomear colunas para exibição
        colunas_exibicao = ['Data']
        if 'Empresa' in df_entrada_exibir.columns:
            colunas_exibicao.append('Empresa')
        colunas_exibicao.extend(['Descrição', 'Valor', 'Banco'])
        if 'classif' in df_entrada_exibir.columns:
            colunas_exibicao.append('Classificação')
        if 'Memorando' in df_entrada_exibir.columns:
            colunas_exibicao.append('Memorando')
        elif 'memorando' in df_entrada_exibir.columns:
            colunas_exibicao.append('Memorando')
        
        df_entrada_exibir.columns = colunas_exibicao
        
        st.dataframe(df_entrada_exibir, use_container_width=True, height=400)
        
        # Estatísticas das entradas
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            st.metric("💚 Total de Entradas", format_currency(df_entradas_filtrado['Valor'].sum()))
        with col_stat2:
            st.metric("📊 Número de Entradas", f"{len(df_entradas_filtrado):,}")
        with col_stat3:
            st.metric("📈 Ticket Médio", format_currency(df_entradas_filtrado['Valor'].mean()))
        with col_stat4:
            st.metric("🔝 Maior Entrada", format_currency(df_entradas_filtrado['Valor'].max()))

# --- ABA 5: ANÁLISE DE SAÍDAS ---
with tab5:
    st.markdown("#### 💸 Análise Detalhada de Saídas")
    
    # Filtrar apenas saídas
    df_saidas = df_filtrado[df_filtrado['Valor'] < 0].copy()
    
    # Filtros
    col_search3, col_search4, col_search5 = st.columns([2, 2, 1])
    
    with col_search3:
        filtro_empresa_saida = st.text_input(
            "🔍 Buscar por empresa/descrição:",
            placeholder="Digite o nome da empresa ou parte da descrição...",
            key="filtro_saida_empresa"
        )
    
    with col_search4:
        # Filtro de classificações
        if 'classif' in df_saidas.columns:
            classificacoes_saida_disponveis = df_saidas['classif'].dropna().unique().tolist()
            classificacoes_saida_selecionadas = st.multiselect(
                "🏷️ Classificações:",
                options=sorted(classificacoes_saida_disponveis),
                default=classificacoes_saida_disponveis,
                key="filtro_saida_classif"
            )
        else:
            classificacoes_saida_selecionadas = None
    
    with col_search5:
        if st.button("🔄 Limpar Filtro", key="limpar_saida"):
            st.rerun()
    
    # Aplicar filtros
    df_saidas_filtrado = df_saidas.copy()
    
    if filtro_empresa_saida:
        mask_saida = (
            df_saidas_filtrado['Descrição'].str.contains(filtro_empresa_saida, case=False, na=False) |
            (df_saidas_filtrado['Banco'].str.contains(filtro_empresa_saida, case=False, na=False) if 'Banco' in df_saidas_filtrado.columns else False)
        )
        df_saidas_filtrado = df_saidas_filtrado[mask_saida]
    
    # Só filtrar por classificação se alguma foi selecionada (se não estiver vazio)
    if classificacoes_saida_selecionadas is not None and len(classificacoes_saida_selecionadas) > 0:
        df_saidas_filtrado = df_saidas_filtrado[df_saidas_filtrado['classif'].isin(classificacoes_saida_selecionadas)]
    
    if df_saidas_filtrado.empty:
        st.warning("⚠️ Nenhuma saída encontrada com os filtros aplicados.")
    else:
        # Agrupar por granularidade (usando valores absolutos para saídas)
        df_saidas_agrupado = agrupar_por_granularidade(df_saidas_filtrado, granularidade)
        
        # Preparar dados para o gráfico
        if granularidade == 'Diário':
            x_vals_saida = df_saidas_agrupado['Data']
            periodo_labels_saida = x_vals_saida
        else:
            x_vals_saida = df_saidas_agrupado['Periodo_Label']
            periodo_labels_saida = x_vals_saida
        
        y_vals_saida = df_saidas_agrupado['Valor'].abs()  # Usar valores absolutos
        
        # Calcular variação percentual
        variacao_pct_saida = y_vals_saida.pct_change() * 100
        
        # Criar gráfico combinado
        fig_saidas = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Barras para volume
        fig_saidas.add_trace(go.Bar(
            x=periodo_labels_saida,
            y=y_vals_saida,
            name='Volume de Saídas',
            marker_color='red',
            text=[format_label_optimized(val) for val in y_vals_saida],
            textposition='outside',
            textfont=dict(color='white', family='Arial Black')
        ), secondary_y=False)
        
        # Linha para variação
        fig_saidas.add_trace(go.Scatter(
            x=periodo_labels_saida,
            y=variacao_pct_saida,
            name='Variação (%)',
            mode='lines+markers+text',
            line=dict(color='orange', width=3),
            text=[f'{v:.1f}%' if not pd.isna(v) else '' for v in variacao_pct_saida],
            textposition='top center',
            textfont=dict(color='white', family='Arial Black'),
            connectgaps=True
        ), secondary_y=True)
        
        fig_saidas.update_yaxes(title_text='Volume (R$)', secondary_y=False)
        fig_saidas.update_yaxes(title_text='Variação (%)', secondary_y=True)
        fig_saidas.update_layout(
            height=500,
            title=f'Histórico de Saídas - {granularidade}',
            xaxis_title='Período',
            margin=dict(t=100, b=60, l=100, r=60),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_saidas, use_container_width=True)
        
        # Tabela detalhada de saídas
        st.markdown("##### 📊 Detalhamento das Saídas")
        
        colunas_saida = ['Data', 'Descrição', 'Valor', 'Banco']
        if 'Empresa' in df_saidas_filtrado.columns:
            colunas_saida.insert(1, 'Empresa')  # Adiciona Empresa após Data
        if 'classif' in df_saidas_filtrado.columns:
            colunas_saida.append('classif')
        if 'Memorando' in df_saidas_filtrado.columns:
            colunas_saida.append('Memorando')
        elif 'memorando' in df_saidas_filtrado.columns:
            colunas_saida.append('memorando')
        
        df_saida_exibir = df_saidas_filtrado[colunas_saida].copy()
        df_saida_exibir = df_saida_exibir.sort_values('Valor', ascending=True)  # Menores valores primeiro (mais negativo)
        df_saida_exibir['Data'] = df_saida_exibir['Data'].dt.strftime('%d/%m/%Y')
        df_saida_exibir['Valor'] = df_saida_exibir['Valor'].apply(lambda x: f"R$ {x:,.0f}".replace(",", "."))
        
        # Renomear colunas para exibição
        colunas_exibicao_saida = ['Data']
        if 'Empresa' in df_saida_exibir.columns:
            colunas_exibicao_saida.append('Empresa')
        colunas_exibicao_saida.extend(['Descrição', 'Valor', 'Banco'])
        if 'classif' in df_saida_exibir.columns:
            colunas_exibicao_saida.append('Classificação')
        if 'Memorando' in df_saida_exibir.columns:
            colunas_exibicao_saida.append('Memorando')
        elif 'memorando' in df_saida_exibir.columns:
            colunas_exibicao_saida.append('Memorando')
        
        df_saida_exibir.columns = colunas_exibicao_saida
        
        st.dataframe(df_saida_exibir, use_container_width=True, height=400)
        
        # Estatísticas das saídas
        col_stat5, col_stat6, col_stat7, col_stat8 = st.columns(4)
        
        with col_stat5:
            st.metric("💸 Total de Saídas", format_currency(abs(df_saidas_filtrado['Valor'].sum())))
        with col_stat6:
            st.metric("📊 Número de Saídas", f"{len(df_saidas_filtrado):,}")
        with col_stat7:
            st.metric("📈 Ticket Médio", format_currency(abs(df_saidas_filtrado['Valor'].mean())))
        with col_stat8:
            st.metric("🔝 Maior Saída", format_currency(abs(df_saidas_filtrado['Valor'].min())))
