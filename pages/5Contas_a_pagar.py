import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="💰 Contas a Pagar",
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
    .metric-card {
        background: linear-gradient(135deg, #262730 0%, #2a2d3a 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #ff6b35;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR COM LOGO ALUN ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 15px; margin-bottom: 2rem;">
        <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQwIiB2aWV3Qm94PSIwIDAgMTAwIDQwIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8dGV4dCB4PSI1MCIgeT0iMjUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyNCIgZm9udC13ZWlnaHQ9ImJvbGQiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5BTFVOPC90ZXh0Pgo8L3N2Zz4K" style="width: 120px; height: auto;">
        <div style="color: #ccc; font-size: 12px; margin-top: 10px;">Contas a Pagar</div>
    </div>
    """, unsafe_allow_html=True)

# --- BOTÃO DE ATUALIZAÇÃO ---
col_refresh = st.columns([3, 1])
with col_refresh[1]:
    if st.button("🔄 Atualizar Dados", help="Clique para recarregar os dados"):
        st.cache_data.clear()
        st.rerun()

# --- TÍTULO DA PÁGINA ---
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #fafafa; font-weight: 700; margin-bottom: 0;">💰 Dashboard de Contas a Pagar</h1>
    <p style="color: #ccc; font-size: 1.1em;">Análise de Pagamentos e Gastos com Viagens</p>
</div>
""", unsafe_allow_html=True)

# --- FUNÇÕES AUXILIARES ---
def format_currency(value):
    """Formata valores em moeda brasileira"""
    if pd.isna(value) or value == 0:
        return "R$ 0"
    return f"R$ {value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_label_optimized(value):
    """Otimiza labels dos gráficos"""
    if pd.isna(value) or value == 0:
        return "R$ 0"
    if value >= 1_000_000:
        return f"R$ {value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"R$ {value/1_000:.0f}K"
    else:
        return f"R$ {value:.0f}"

def obter_semana_do_ano(data):
    """Retorna a semana do ano no formato 'YYYY-WXX'"""
    if pd.isna(data):
        return None
    iso = data.isocalendar()
    return f"{data.year}-W{iso.week:02d}"

def obter_intervalo_semanal(data):
    """Retorna o intervalo da semana (segunda a domingo)"""
    if pd.isna(data):
        return None
    segunda = data - timedelta(days=data.weekday())
    domingo = segunda + timedelta(days=6)
    return f"{segunda.strftime('%d/%m')} a {domingo.strftime('%d/%m/%Y')}"

def parse_data_brasileira(x):
    """Parseia datas em formato brasileiro"""
    x = str(x).strip()
    if x in ['', 'nan', 'None']:
        return pd.NaT
    formatos = ['%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d']
    for fmt in formatos:
        try:
            return datetime.strptime(x, fmt)
        except:
            continue
    try:
        return pd.to_datetime(x, dayfirst=True, errors='coerce')
    except:
        return pd.NaT

def classificar_prazo_pagamento(diferenca_dias):
    """Classifica o prazo de pagamento"""
    if pd.isna(diferenca_dias):
        return "Indefinido"
    elif diferenca_dias > 1:
        return "Atrasado"
    elif diferenca_dias == 0 or diferenca_dias == 1:
        return "No Prazo"
    else:
        return "Adiantado"

def classificar_dias_pagamento(dias):
    """Classifica os dias para pagamento em grupos"""
    if pd.isna(dias):
        return "Indefinido"
    elif dias <= 10:
        return "1-10 dias"
    elif dias <= 20:
        return "11-20 dias"
    elif dias <= 30:
        return "21-30 dias"
    elif dias <= 40:
        return "31-40 dias"
    elif dias <= 50:
        return "41-50 dias"
    elif dias <= 60:
        return "51-60 dias"
    else:
        return "60+ dias"

# --- FUNÇÕES DE CARREGAMENTO DE DADOS ---
@st.cache_data
def load_pagamentos_data():
    """Carrega dados de pagamentos do CSV"""
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "5PMP.csv"),
        os.path.join(os.getcwd(), "data", "5PMP.csv"),
        os.path.join("data", "5PMP.csv"),
        os.path.join(os.path.dirname(__file__), "..", "5PMP.csv"),
        os.path.join(os.getcwd(), "5PMP.csv"),
        "5PMP.csv"
    ]
    
    for arquivo in possible_paths:
        try:
            # Detectar separador
            with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                primeira_linha = f.readline()
            
            separators = [';', '\t', ',']
            for sep in separators:
                try:
                    df = pd.read_csv(arquivo, sep=sep, engine='python', encoding='utf-8', on_bad_lines='skip')
                    if df.shape[1] > 1:  # Se temos múltiplas colunas, encontramos o separador correto
                        # Limpar nomes das colunas
                        df.columns = [c.strip() for c in df.columns]
                        return df
                except:
                    continue
            
            st.error(f"❌ Não foi possível determinar o separador correto para '{arquivo}'")
            return None
            
        except FileNotFoundError:
            continue
        except Exception as e:
            st.error(f"❌ Erro ao carregar '{arquivo}': {e}")
            continue
    
    st.error("❌ Arquivo '5PMP.csv' não encontrado em nenhum dos caminhos esperados.")
    return None

@st.cache_data
def load_viagens_data():
    """Carrega dados de viagens do CSV"""
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "6Viagens.csv"),
        os.path.join(os.getcwd(), "data", "6Viagens.csv"),
        os.path.join("data", "6Viagens.csv"),
        os.path.join(os.path.dirname(__file__), "..", "6Viagens.csv"),
        os.path.join(os.getcwd(), "6Viagens.csv"),
        "6Viagens.csv"
    ]
    
    for arquivo in possible_paths:
        try:
            # Detectar separador
            with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                primeira_linha = f.readline()
            
            separators = [';', '\t', ',']
            for sep in separators:
                try:
                    df = pd.read_csv(arquivo, sep=sep, engine='python', encoding='utf-8', on_bad_lines='skip')
                    if df.shape[1] > 1:
                        df.columns = [c.strip() for c in df.columns]
                        return df
                except:
                    continue
            
            st.warning(f"⚠️ Não foi carregar '{arquivo}' - separador não identificado")
            return None
            
        except FileNotFoundError:
            continue
        except Exception as e:
            st.warning(f"⚠️ Erro ao carregar '{arquivo}': {e}")
            continue
    
    st.warning("⚠️ Arquivo '6Viagens.csv' não encontrado - aba de viagens não disponível.")
    return None

# --- ABAS PRINCIPAIS ---
tab_pagamentos, tab_viagens = st.tabs(["💳 Pagamentos", "✈️ Viagens"])

# =============================================================================
# ABA DE PAGAMENTOS
# =============================================================================
with tab_pagamentos:
    st.markdown("### 💳 Análise de Pagamentos Empresariais")
    
    # Carregar dados de pagamentos
    df_pagamentos = load_pagamentos_data()
    if df_pagamentos is None:
        st.stop()
    
    st.success(f"✅ Dados de pagamentos carregados: {len(df_pagamentos)} registros")
    
    # Identificar colunas importantes
    colunas_essenciais = {
        'data_baixa': ['Data da baixa', 'data da baixa', 'data_baixa', 'baixa'],
        'data_emissao': ['Data de emissão', 'data de emissão', 'data_emissao', 'emissao'],
        'data_vencimento': ['Data de vencimento', 'data de vencimento', 'data_vencimento', 'vencimento'],
        'valor_pago': ['Valor Pago da Cobrança', 'valor pago da cobrança', 'valor_pago', 'valor pago'],
        'empresa': ['Empresa', 'empresa', 'empresas'],
        'forma_pagamento': ['Forma de Pagamento (Nexxera)', 'forma de pagamento', 'forma_pagamento', 'nexxera'],
        'nome': ['Nome', 'nome', 'cliente', 'fornecedor'],
        'memorando': ['Memorando', 'memorando', 'descricao', 'descrição', 'observacao', 'observação']
    }
    
    # Mapear colunas
    colunas_mapeadas_pag = {}
    for chave, opcoes in colunas_essenciais.items():
        for col in df_pagamentos.columns:
            if any(opcao.lower() in col.lower() for opcao in opcoes):
                colunas_mapeadas_pag[chave] = col
                break
    
    # Verificar colunas obrigatórias
    obrigatorias = ['data_baixa', 'valor_pago']
    faltantes = [k for k in obrigatorias if k not in colunas_mapeadas_pag]
    if faltantes:
        st.error(f"❌ Colunas obrigatórias não encontradas: {faltantes}")
        st.info("Colunas disponíveis: " + ", ".join(df_pagamentos.columns.tolist()))
        st.stop()
    
    # Processar dados de pagamentos
    df_pag = df_pagamentos.copy()
    
    # Converter datas
    for chave in ['data_baixa', 'data_emissao', 'data_vencimento']:
        if chave in colunas_mapeadas_pag:
            col_name = colunas_mapeadas_pag[chave]
            df_pag[col_name] = df_pag[col_name].apply(parse_data_brasileira)
    
    # Converter valores
    col_valor_pago = colunas_mapeadas_pag['valor_pago']
    if df_pag[col_valor_pago].dtype == object:
        serie_limpa = (df_pag[col_valor_pago].astype(str)
                      .str.replace(r'[^\d,.\-]', '', regex=True)
                      .str.replace('.', '', regex=False)  # Remove separador de milhares
                      .str.replace(',', '.'))  # Troca vírgula decimal por ponto
        df_pag[col_valor_pago] = pd.to_numeric(serie_limpa, errors='coerce')
    
    # Calcular diferenças de datas
    col_data_baixa = colunas_mapeadas_pag['data_baixa']
    
    if 'data_emissao' in colunas_mapeadas_pag:
        col_data_emissao = colunas_mapeadas_pag['data_emissao']
        df_pag['dias_para_pagamento'] = (df_pag[col_data_baixa] - df_pag[col_data_emissao]).dt.days
        df_pag['grupo_dias_pagamento'] = df_pag['dias_para_pagamento'].apply(classificar_dias_pagamento)
    
    if 'data_vencimento' in colunas_mapeadas_pag:
        col_data_vencimento = colunas_mapeadas_pag['data_vencimento']
        df_pag['diferenca_vencimento'] = (df_pag[col_data_baixa] - df_pag[col_data_vencimento]).dt.days
        df_pag['status_prazo'] = df_pag['diferenca_vencimento'].apply(classificar_prazo_pagamento)
    
    # Criar colunas de agrupamento temporal
    df_pag['semana_ano'] = df_pag[col_data_baixa].apply(obter_semana_do_ano)
    df_pag['intervalo_semanal'] = df_pag[col_data_baixa].apply(obter_intervalo_semanal)
    df_pag['mes_ano'] = df_pag[col_data_baixa].dt.to_period('M').astype(str)
    df_pag['ano'] = df_pag[col_data_baixa].dt.year
    
    # Remover linhas sem data de baixa ou valor
    df_pag = df_pag.dropna(subset=[col_data_baixa, col_valor_pago])
    
    if df_pag.empty:
        st.error("❌ Sem dados válidos após processamento.")
        st.stop()
    
    # --- FILTROS DE PAGAMENTOS ---
    st.markdown("#### 🎛️ Filtros de Análise")
    
    with st.container():
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        
        with col_f1:
            # Filtro de Data
            data_min_pag = df_pag[col_data_baixa].min().date()
            data_max_pag = df_pag[col_data_baixa].max().date()
            
            data_inicio_pag = st.date_input(
                "📅 Data Início:",
                value=data_min_pag,
                min_value=data_min_pag,
                max_value=data_max_pag,
                key="filtro_data_inicio_pag"
            )
            
            data_fim_pag = st.date_input(
                "📅 Data Fim:",
                value=data_max_pag,
                min_value=data_min_pag,
                max_value=data_max_pag,
                key="filtro_data_fim_pag"
            )
        
        with col_f2:
            # Filtro de Granularidade
            granularidade_pag = st.selectbox(
                "📊 Granularidade:",
                ["Mensal", "Diário", "Semanal", "Anual"],
                index=0,  # Mensal pré-selecionado
                key="granularidade_pag"
            )
        
        with col_f3:
            # Filtro de Empresa (Subsidiária)
            col_empresa_pag = None
            if 'subsidiária' in df_pag.columns:
                col_empresa_pag = 'subsidiária'
            elif 'Subsidiária' in df_pag.columns:
                col_empresa_pag = 'Subsidiária'
            elif 'empresa' in colunas_mapeadas_pag:
                col_empresa_pag = colunas_mapeadas_pag['empresa']
            
            if col_empresa_pag:
                empresas_pag = sorted(df_pag[col_empresa_pag].dropna().unique())
                # Pré-selecionar apenas Alura se disponível
                default_empresas_pag = ['Alura'] if 'Alura' in empresas_pag else empresas_pag
                empresas_selecionadas_pag = st.multiselect(
                    "🏢 Empresas:",
                    options=empresas_pag,
                    default=default_empresas_pag,
                    key="filtro_empresa_pag"
                )
            else:
                empresas_selecionadas_pag = None
        
        with col_f4:
            # Filtro de Forma de Pagamento
            if 'forma_pagamento' in colunas_mapeadas_pag:
                col_forma_pag = colunas_mapeadas_pag['forma_pagamento']
                formas_pag = sorted(df_pag[col_forma_pag].dropna().unique())
                formas_selecionadas_pag = st.multiselect(
                    "💳 Forma de Pagamento:",
                    options=formas_pag,
                    default=[],
                    key="filtro_forma_pag"
                )
            else:
                formas_selecionadas_pag = None
    
    # Aplicar filtros
    df_pag_filtrado = df_pag.copy()
    
    # Filtro de data
    df_pag_filtrado = df_pag_filtrado[
        (df_pag_filtrado[col_data_baixa].dt.date >= data_inicio_pag) & 
        (df_pag_filtrado[col_data_baixa].dt.date <= data_fim_pag)
    ]
    
    # Outros filtros
    if empresas_selecionadas_pag and col_empresa_pag:
        df_pag_filtrado = df_pag_filtrado[df_pag_filtrado[col_empresa_pag].isin(empresas_selecionadas_pag)]
    
    if formas_selecionadas_pag and 'forma_pagamento' in colunas_mapeadas_pag:
        df_pag_filtrado = df_pag_filtrado[df_pag_filtrado[colunas_mapeadas_pag['forma_pagamento']].isin(formas_selecionadas_pag)]
    
    # --- ABAS INTERNAS DE PAGAMENTOS (REORDENADAS) ---
    tab_prazo_medio, tab_dist_dias, tab_volume_total = st.tabs([
        "⏱️ Prazo Médio", 
        "📊 Distribuição por Dias", 
        "💰 Volume Total"
    ])
    
    # =============================================================================
    # ABA: PRAZO MÉDIO (AGORA PRIMEIRA)
    # =============================================================================
    with tab_prazo_medio:
        st.markdown("#### ⏱️ Análise de Prazo Médio de Pagamentos")
        
        if 'dias_para_pagamento' in df_pag_filtrado.columns and 'status_prazo' in df_pag_filtrado.columns and len(df_pag_filtrado) > 0:
            # Agrupar por período para calcular médias
            df_temp = df_pag_filtrado.copy()
            
            if granularidade_pag == "Diário":
                df_temp['periodo'] = df_temp[col_data_baixa].dt.strftime('%Y-%m-%d')
                df_temp['periodo_display'] = df_temp[col_data_baixa].dt.strftime('%d/%m/%Y')
            elif granularidade_pag == "Semanal":
                df_temp['periodo'] = df_temp[col_data_baixa].dt.strftime('%Y-W%U')
                df_temp['periodo_display'] = df_temp['intervalo_semanal']
            elif granularidade_pag == "Mensal":
                df_temp['periodo'] = df_temp[col_data_baixa].dt.strftime('%Y-%m')
                df_temp['periodo_display'] = df_temp[col_data_baixa].dt.strftime('%m/%Y')
            else:  # Anual
                df_temp['periodo'] = df_temp[col_data_baixa].dt.year.astype(str)
                df_temp['periodo_display'] = df_temp[col_data_baixa].dt.year.astype(str)
            
            # Calcular métricas por período
            metricas_periodo = []
            
            for periodo in sorted(df_temp['periodo'].unique()):
                df_periodo = df_temp[df_temp['periodo'] == periodo]
                periodo_display = df_periodo['periodo_display'].iloc[0]
                
                # Prazo médio
                prazo_medio = df_periodo['dias_para_pagamento'].mean()
                
                # Percentual de atrasados
                total_periodo = len(df_periodo)
                atrasados_periodo = len(df_periodo[df_periodo['status_prazo'] == 'Atrasado'])
                perc_atrasados = (atrasados_periodo / total_periodo * 100) if total_periodo > 0 else 0
                
                metricas_periodo.append({
                    'periodo': periodo,
                    'periodo_display': periodo_display,
                    'prazo_medio': prazo_medio,
                    'perc_atrasados': perc_atrasados,
                    'total_pagamentos': total_periodo
                })
            
            df_metricas = pd.DataFrame(metricas_periodo)
            df_metricas = df_metricas.sort_values('periodo')  # Ordenar por período cronológico
            
            # Criar cards com métricas gerais (APENAS 2 CARDS)
            col_card1, col_card2 = st.columns(2)
            
            with col_card1:
                prazo_medio_geral = df_pag_filtrado['dias_para_pagamento'].mean()
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #fafafa; margin: 0;">⏱️ Prazo Médio Geral</h4>
                    <p style="color: #f39c12; font-size: 1.5rem; margin: 0; font-weight: bold;">{prazo_medio_geral:.1f} dias</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_card2:
                total_atrasados = len(df_pag_filtrado[df_pag_filtrado['status_prazo'] == 'Atrasado'])
                perc_atrasados_geral = (total_atrasados / len(df_pag_filtrado)) * 100
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #fafafa; margin: 0;">⚠️ % Atrasados Geral</h4>
                    <p style="color: #e74c3c; font-size: 1.5rem; margin: 0; font-weight: bold;">{perc_atrasados_geral:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Gráfico de barras com linha - Prazo médio vs % Atrasados
            fig_prazo_medio = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Barras - Prazo Médio
            fig_prazo_medio.add_trace(go.Bar(
                x=df_metricas['periodo_display'],
                y=df_metricas['prazo_medio'],
                name='Prazo Médio (dias)',
                marker_color='#3498db',
                text=[f'{val:.1f}d' for val in df_metricas['prazo_medio']],
                textposition='outside',
                textfont=dict(color='white', size=11, family="Arial Black"),
                opacity=0.8,
                hovertemplate='<b>Período:</b> %{x}<br><b>Prazo Médio:</b> %{y:.1f} dias<extra></extra>'
            ), secondary_y=False)
            
            # Linha - % Atrasados
            fig_prazo_medio.add_trace(go.Scatter(
                x=df_metricas['periodo_display'],
                y=df_metricas['perc_atrasados'],
                name='% Atrasados',
                mode='lines+markers+text',
                line=dict(color='#e74c3c', width=3),
                marker=dict(size=8, color='#e74c3c', line=dict(width=2, color='white')),
                text=[f'{v:.1f}%' for v in df_metricas['perc_atrasados']],
                textposition='top center',
                textfont=dict(color='white', size=10),
                connectgaps=True,
                hovertemplate='<b>Período:</b> %{x}<br><b>% Atrasados:</b> %{y:.1f}%<extra></extra>'
            ), secondary_y=True)
            
            # Configurar eixos
            fig_prazo_medio.update_yaxes(
                title_text='<b>Prazo Médio (dias)</b>', 
                secondary_y=False, 
                gridcolor='rgba(128,128,128,0.2)',
                showgrid=True
            )
            fig_prazo_medio.update_yaxes(
                title_text='<b>Percentual de Atrasados (%)</b>', 
                secondary_y=True, 
                gridcolor='rgba(128,128,128,0.1)',
                showgrid=False
            )
            
            fig_prazo_medio.update_layout(
                height=450,
                title='<b>Prazo Médio de Pagamento vs Percentual de Atrasos por Período</b>',
                xaxis_title='<b>Período</b>',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                xaxis=dict(tickangle=45),
                legend=dict(
                    orientation="h", 
                    yanchor="bottom", 
                    y=1.02, 
                    xanchor="center", 
                    x=0.5
                ),
                title_x=0.5
            )
            
            st.plotly_chart(fig_prazo_medio, use_container_width=True)
            
            # TABELA DETALHADA MOVIDA PARA CÁ
            st.markdown("#### 📋 Tabela Detalhada de Pagamentos")
            
            if len(df_pag_filtrado) > 0:
                # Preparar colunas para exibição
                colunas_exibir_pag = [col_data_baixa, col_valor_pago]
                
                # Adicionar data de vencimento se disponível
                if 'data_vencimento' in colunas_mapeadas_pag:
                    colunas_exibir_pag.insert(1, col_data_vencimento)  # Inserir após data da baixa
                
                # Adicionar colunas opcionais se disponíveis
                if col_empresa_pag:
                    colunas_exibir_pag.append(col_empresa_pag)
                if 'nome' in colunas_mapeadas_pag:
                    colunas_exibir_pag.append(colunas_mapeadas_pag['nome'])
                if 'memorando' in colunas_mapeadas_pag:
                    colunas_exibir_pag.append(colunas_mapeadas_pag['memorando'])
                if 'forma_pagamento' in colunas_mapeadas_pag:
                    colunas_exibir_pag.append(colunas_mapeadas_pag['forma_pagamento'])
                if 'status_prazo' in df_pag_filtrado.columns:
                    colunas_exibir_pag.append('status_prazo')
                if 'grupo_dias_pagamento' in df_pag_filtrado.columns:
                    colunas_exibir_pag.append('grupo_dias_pagamento')
                if 'dias_para_pagamento' in df_pag_filtrado.columns:
                    colunas_exibir_pag.append('dias_para_pagamento')
                
                df_exibir_pag = df_pag_filtrado[colunas_exibir_pag].copy()
                
                # Formatar para exibição
                df_exibir_pag[col_data_baixa] = df_exibir_pag[col_data_baixa].dt.strftime('%d/%m/%Y')
                if 'data_vencimento' in colunas_mapeadas_pag:
                    df_exibir_pag[col_data_vencimento] = df_exibir_pag[col_data_vencimento].dt.strftime('%d/%m/%Y')
                df_exibir_pag[col_valor_pago] = df_exibir_pag[col_valor_pago].apply(format_currency)
                
                # Renomear colunas para nomes amigáveis
                nomes_amigaveis_pag = {
                    col_data_baixa: 'Data da Baixa',
                    col_valor_pago: 'Valor Pago',
                    'status_prazo': 'Status Prazo',
                    'grupo_dias_pagamento': 'Dias para Pagamento',
                    'dias_para_pagamento': 'Dias Exatos'
                }
                
                if 'data_vencimento' in colunas_mapeadas_pag:
                    nomes_amigaveis_pag[col_data_vencimento] = 'Data de Vencimento'
                if col_empresa_pag:
                    nomes_amigaveis_pag[col_empresa_pag] = 'Empresa'
                if 'nome' in colunas_mapeadas_pag:
                    nomes_amigaveis_pag[colunas_mapeadas_pag['nome']] = 'Nome'
                if 'memorando' in colunas_mapeadas_pag:
                    nomes_amigaveis_pag[colunas_mapeadas_pag['memorando']] = 'Memorando'
                if 'forma_pagamento' in colunas_mapeadas_pag:
                    nomes_amigaveis_pag[colunas_mapeadas_pag['forma_pagamento']] = 'Forma de Pagamento'
                
                df_exibir_pag = df_exibir_pag.rename(columns=nomes_amigaveis_pag)
                
                # Filtro de busca
                busca_pag = st.text_input("🔍 Buscar na tabela:", placeholder="Digite para filtrar...", key="busca_pag")
                
                if busca_pag:
                    mask = df_exibir_pag.astype(str).apply(
                        lambda x: x.str.contains(busca_pag, case=False, na=False)
                    ).any(axis=1)
                    df_exibir_pag = df_exibir_pag[mask]
                
                st.dataframe(df_exibir_pag, use_container_width=True, height=400)
                
                # Download dos dados
                st.download_button(
                    label="📥 Baixar Dados de Pagamentos",
                    data=df_exibir_pag.to_csv(index=False, sep=';').encode('utf-8'),
                    file_name=f"pagamentos_{data_inicio_pag.strftime('%d%m%Y')}_a_{data_fim_pag.strftime('%d%m%Y')}.csv",
                    mime="text/csv",
                    key="download_pagamentos"
                )
                
                st.info(f"📊 Exibindo {len(df_exibir_pag)} de {len(df_pag_filtrado)} registros")
            else:
                st.warning("⚠️ Nenhum dado de pagamento disponível para exibir.")
                
        else:
            st.info("ℹ️ Dados necessários para análise de prazo médio não disponíveis.")
    
    # =============================================================================
    # ABA: DISTRIBUIÇÃO POR DIAS (SEM CARDS DE INSIGHT)
    # =============================================================================
    with tab_dist_dias:
        st.markdown("#### 📊 Distribuição - Dias para Pagamento")
        
        if 'grupo_dias_pagamento' in df_pag_filtrado.columns and len(df_pag_filtrado) > 0:
            # Calcular distribuição
            dist_dias = df_pag_filtrado['grupo_dias_pagamento'].value_counts()
            
            # Ordenar corretamente os grupos
            ordem_grupos = ["1-10 dias", "11-20 dias", "21-30 dias", "31-40 dias", "41-50 dias", "51-60 dias", "60+ dias"]
            dist_dias = dist_dias.reindex([g for g in ordem_grupos if g in dist_dias.index])
            
            # Calcular percentuais
            dist_dias_perc = (dist_dias / dist_dias.sum() * 100).round(1)
            
            fig_dias = go.Figure()
            
            colors = ['#1e3a8a', '#1976d2', '#2196f3', '#42a5f5', '#64b5f6', '#90caf9', '#bbdefb']
            
            fig_dias.add_trace(go.Bar(
                x=dist_dias.index,
                y=dist_dias.values,
                marker_color=colors[:len(dist_dias)],
                text=[f'{val}<br>({perc}%)' for val, perc in zip(dist_dias.values, dist_dias_perc.values)],
                textposition='outside',
                textfont=dict(color='white', size=12, family="Arial Black"),
                hovertemplate='<b>Grupo:</b> %{x}<br><b>Quantidade:</b> %{y}<br><b>Percentual:</b> %{customdata}%<extra></extra>',
                customdata=dist_dias_perc.values
            ))
            
            fig_dias.update_layout(
                height=500,
                title='<b>Distribuição de Pagamentos por Grupo de Dias</b>',
                xaxis_title='<b>Grupos de Dias para Pagamento</b>',
                yaxis_title='<b>Quantidade de Pagamentos</b>',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                xaxis=dict(tickangle=45),
                showlegend=False,
                title_x=0.5
            )
            
            st.plotly_chart(fig_dias, use_container_width=True)
        else:
            st.info("ℹ️ Dados de dias para pagamento não disponíveis.")
    
    # =============================================================================
    # ABA: VOLUME TOTAL (CARDS UNIFORMES, SEM ANÁLISE DE CRESCIMENTO)
    # =============================================================================
    with tab_volume_total:
        st.markdown("#### 💰 Análise de Volume Total de Pagamentos")
        
        if len(df_pag_filtrado) > 0:
            # Cards principais (TAMANHO UNIFORME)
            col_vol1, col_vol2 = st.columns(2)
            
            with col_vol1:
                total_pago = df_pag_filtrado[col_valor_pago].sum()
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #fafafa; margin: 0;">💰 Total Pago no Período</h4>
                    <p style="color: #e74c3c; font-size: 1.5rem; margin: 0; font-weight: bold;">{format_currency(total_pago)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_vol2:
                total_pagamentos = len(df_pag_filtrado)
                ticket_medio = total_pago / total_pagamentos if total_pagamentos > 0 else 0
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #fafafa; margin: 0;">💳 Total de Pagamentos</h4>
                    <p style="color: #3498db; font-size: 1.5rem; margin: 0; font-weight: bold;">{total_pagamentos:,}</p>
                    <p style="color: #f39c12; font-size: 1rem; margin: 0;">Ticket Médio: {format_currency(ticket_medio)}</p>
                </div>
                """, unsafe_allow_html=True)
            # Gráfico de Volume por Período com Variação (ORDEM CRONOLÓGICA CORRIGIDA)
            st.markdown("##### 📈 Volume de Pagamentos por Período com Variação")
            
            df_temp_vol = df_pag_filtrado.copy()
            
            # Agrupar por granularidade com ordem cronológica
            if granularidade_pag == "Diário":
                df_temp_vol['periodo'] = df_temp_vol[col_data_baixa].dt.strftime('%Y-%m-%d')
                df_temp_vol['periodo_display'] = df_temp_vol[col_data_baixa].dt.strftime('%d/%m/%Y')
            elif granularidade_pag == "Semanal":
                df_temp_vol['periodo'] = df_temp_vol[col_data_baixa].dt.strftime('%Y-W%U')
                df_temp_vol['periodo_display'] = df_temp_vol['intervalo_semanal']
            elif granularidade_pag == "Mensal":
                df_temp_vol['periodo'] = df_temp_vol[col_data_baixa].dt.strftime('%Y-%m')
                df_temp_vol['periodo_display'] = df_temp_vol[col_data_baixa].dt.strftime('%m/%Y')
            else:  # Anual
                df_temp_vol['periodo'] = df_temp_vol[col_data_baixa].dt.year.astype(str)
                df_temp_vol['periodo_display'] = df_temp_vol[col_data_baixa].dt.year.astype(str)
            
            # Calcular volume por período
            volume_periodo = df_temp_vol.groupby(['periodo', 'periodo_display']).agg({
                col_valor_pago: 'sum'
            }).reset_index()
            
            volume_periodo['qtd_pagamentos'] = df_temp_vol.groupby('periodo').size().values
            volume_periodo = volume_periodo.sort_values('periodo')  # Ordenar cronologicamente
            
            # Calcular variação percentual
            volume_periodo['variacao_pct'] = volume_periodo[col_valor_pago].pct_change() * 100
            
            # Gráfico combinado
            fig_volume = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Barras - Volume
            fig_volume.add_trace(go.Bar(
                x=volume_periodo['periodo_display'],
                y=volume_periodo[col_valor_pago],
                name='Volume de Pagamentos',
                marker_color='#3498db',
                text=[format_label_optimized(val) for val in volume_periodo[col_valor_pago]],
                textposition='outside',
                textfont=dict(color='white', size=11, family="Arial Black"),
                opacity=0.8,
                hovertemplate='<b>Período:</b> %{x}<br><b>Volume:</b> %{customdata}<br><b>Qtd Pagamentos:</b> %{meta}<extra></extra>',
                customdata=[format_currency(val) for val in volume_periodo[col_valor_pago]],
                meta=volume_periodo['qtd_pagamentos'].values
            ), secondary_y=False)
            
            # Linha - Variação %
            fig_volume.add_trace(go.Scatter(
                x=volume_periodo['periodo_display'],
                y=volume_periodo['variacao_pct'],
                name='Variação (%)',
                mode='lines+markers+text',
                line=dict(color='#e74c3c', width=3),
                marker=dict(size=8, color='#e74c3c', line=dict(width=2, color='white')),
                text=[f'{v:+.1f}%' if not pd.isna(v) else '' for v in volume_periodo['variacao_pct']],
                textposition='top center',
                textfont=dict(color='white', size=10),
                connectgaps=False,
                hovertemplate='<b>Período:</b> %{x}<br><b>Variação:</b> %{y:+.1f}%<extra></extra>'
            ), secondary_y=True)
            
            # Configurar eixos
            fig_volume.update_yaxes(
                title_text='<b>Volume de Pagamentos (R$)</b>', 
                secondary_y=False, 
                gridcolor='rgba(128,128,128,0.2)',
                showgrid=True
            )
            fig_volume.update_yaxes(
                title_text='<b>Variação Percentual (%)</b>', 
                secondary_y=True, 
                gridcolor='rgba(128,128,128,0.1)',
                showgrid=False,
                zeroline=True,
                zerolinecolor='rgba(255,255,255,0.3)',
                zerolinewidth=1
            )
            
            fig_volume.update_layout(
                height=500,
                title='<b>Volume de Pagamentos por Período com Variação Percentual</b>',
                xaxis_title='<b>Período</b>',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                xaxis=dict(tickangle=45),
                legend=dict(
                    orientation="h", 
                    yanchor="bottom", 
                    y=1.02, 
                    xanchor="center", 
                    x=0.5
                ),
                title_x=0.5
            )
            
            st.plotly_chart(fig_volume, use_container_width=True)
            
        else:
            st.warning("⚠️ Nenhum dado disponível para análise de volume.")

# =============================================================================
# ABA DE VIAGENS (mantida igual)
# =============================================================================
with tab_viagens:
    st.markdown("### ✈️ Análise de Gastos com Viagens")
    
    # Carregar dados de viagens
    df_viagens_raw = load_viagens_data()
    if df_viagens_raw is None:
        st.warning("⚠️ Dados de viagens não disponíveis.")
    else:
        # Todo o código anterior de viagens vai aqui (mantido igual)
        # [O código de viagens permanece inalterado - foi apenas movido para dentro desta aba]
        
        # Identificar e preparar colunas de viagens
        possiveis_col_data_ida = [c for c in df_viagens_raw.columns if 'data ida' in c.lower().strip().replace('_', ' ')]
        if possiveis_col_data_ida:
            col_data_viagem = possiveis_col_data_ida[0]
        else:
            st.error("❌ Coluna 'data ida' não encontrada no arquivo.")
            st.stop()
        
        candidatos_valor_viagem = [c for c in df_viagens_raw.columns if any(k in c.lower() for k in ['valor', 'preco', 'custo', 'gasto', 'total', 'price', 'cost'])]
        if candidatos_valor_viagem:
            col_valor_viagem = candidatos_valor_viagem[0]
        else:
            st.error("❌ Nenhuma coluna de valor identificada.")
            st.stop()
        
        # Mapeamento de colunas opcionais para viagens
        colunas_mapeadas_viagem = {'data': col_data_viagem, 'valor': col_valor_viagem}
        
        colunas_opcionais_viagem = {
            'tipo_viagem': ['tipo', 'tipo_viagem', 'categoria', 'modalidade'],
            'centro_custo': ['centro_custo', 'centro', 'setor', 'departamento', 'cost_center'],
            'dentro_politica': ['dentro_politica', 'politica', 'conforme', 'compliance', 'aprovado'],
            'empresa': ['empresa', 'company', 'organizacao', 'filial']
        }
        
        for chave, opcoes in colunas_opcionais_viagem.items():
            for col in df_viagens_raw.columns:
                if any(opcao.lower() in col.lower() for opcao in opcoes):
                    colunas_mapeadas_viagem[chave] = col
                    break
        
        # Processamento de dados de viagens
        df_viagens = df_viagens_raw.copy()
        
        # Converter coluna de data
        df_viagens[col_data_viagem] = df_viagens[col_data_viagem].apply(parse_data_brasileira)
        
        # Converter coluna de valor
        if df_viagens[col_valor_viagem].dtype == object:
            serie_limpa = (df_viagens[col_valor_viagem].astype(str)
                          .str.replace(r'[^\d,.\-]', '', regex=True)
                          .str.replace(',', '.'))
            df_viagens[col_valor_viagem] = pd.to_numeric(serie_limpa, errors='coerce')
        
        # Remover linhas sem data ou valor válidos
        df_viagens = df_viagens.dropna(subset=[col_data_viagem, col_valor_viagem])
        if df_viagens.empty:
            st.error("❌ Sem dados válidos após processamento.")
        else:
            # Criar colunas semanais
            df_viagens['semana_ano'] = df_viagens[col_data_viagem].apply(obter_semana_do_ano)
            df_viagens['intervalo_semanal'] = df_viagens[col_data_viagem].apply(obter_intervalo_semanal)
            
            st.success(f"✅ Dados de viagens processados: {len(df_viagens)} registros válidos para análise.")
            
            # Filtros globais para viagens
            st.markdown("#### 🎛️ Filtros de Análise de Viagens")
            
            col_filtro1, col_filtro2, col_filtro3, col_filtro4, col_filtro5 = st.columns(5)
            
            with col_filtro1:
                data_min_viagem = df_viagens[col_data_viagem].min().date()
                data_max_viagem = df_viagens[col_data_viagem].max().date()
                
                # Calcular últimas 8 semanas (56 dias)
                from datetime import date, timedelta
                data_hoje = date.today()
                data_8_semanas_atras = data_hoje - timedelta(weeks=8)
                data_inicio_default = max(data_8_semanas_atras, data_min_viagem)
                
                data_inicio_viagem = st.date_input(
                    "📅 Data Início:",
                    value=data_inicio_default,
                    min_value=data_min_viagem,
                    max_value=data_max_viagem,
                    key="filtro_data_inicio_viagem"
                )
            
            with col_filtro2:
                data_fim_viagem = st.date_input(
                    "📅 Data Fim:",
                    value=data_max_viagem,
                    min_value=data_min_viagem,
                    max_value=data_max_viagem,
                    key="filtro_data_fim_viagem"
                )
            
            with col_filtro3:
                if 'tipo_viagem' in colunas_mapeadas_viagem:
                    col_tipo_viagem = colunas_mapeadas_viagem['tipo_viagem']
                    tipos_disponiveis = sorted(df_viagens[col_tipo_viagem].dropna().unique())
                    tipos_selecionados = st.multiselect(
                        "✈️ Tipo de Viagem:",
                        options=tipos_disponiveis,
                        default=[],
                        key="filtro_tipo_viagem"
                    )
                else:
                    tipos_selecionados = None
            
            with col_filtro4:
                if 'empresa' in colunas_mapeadas_viagem:
                    col_empresa_viagem = colunas_mapeadas_viagem['empresa']
                    empresas_disponiveis = sorted(df_viagens[col_empresa_viagem].dropna().unique())
                    # Pré-selecionar apenas Alura se disponível
                    default_empresas_viagem = ['Alura'] if 'Alura' in empresas_disponiveis else []
                    empresas_selecionadas_viagem = st.multiselect(
                        "🏢 Empresa:",
                        options=empresas_disponiveis,
                        default=default_empresas_viagem,
                        key="filtro_empresa_viagem"
                    )
                else:
                    empresas_selecionadas_viagem = None
            
            with col_filtro5:
                granularidade_viagem = st.selectbox(
                    "📊 Granularidade:",
                    options=["Diário", "Semanal", "Mensal", "Anual"],
                    index=1,  # Default para Semanal
                    key="filtro_granularidade_viagem"
                )
            
            # Aplicar filtros para viagens
            df_viagens_filtrado = df_viagens.copy()
            
            df_viagens_filtrado = df_viagens_filtrado[
                (df_viagens_filtrado[col_data_viagem].dt.date >= data_inicio_viagem) & 
                (df_viagens_filtrado[col_data_viagem].dt.date <= data_fim_viagem)
            ]
            
            if tipos_selecionados and 'tipo_viagem' in colunas_mapeadas_viagem:
                df_viagens_filtrado = df_viagens_filtrado[df_viagens_filtrado[colunas_mapeadas_viagem['tipo_viagem']].isin(tipos_selecionados)]
            
            if empresas_selecionadas_viagem and 'empresa' in colunas_mapeadas_viagem:
                df_viagens_filtrado = df_viagens_filtrado[df_viagens_filtrado[colunas_mapeadas_viagem['empresa']].isin(empresas_selecionadas_viagem)]
            
            # Métricas principais de viagens
            # Métricas principais de viagens
            
            col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
            
            with col_metric1:
                total_gasto = df_viagens_filtrado[col_valor_viagem].sum()
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #fafafa; margin: 0;">💰 Gasto Total</h4>
                    <p style="color: #e74c3c; font-size: 1.3rem; margin: 0; font-weight: bold;">{format_currency(total_gasto)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_metric2:
                total_viagens = len(df_viagens_filtrado)
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #fafafa; margin: 0;">✈️ Total de Viagens</h4>
                    <p style="color: #3498db; font-size: 1.3rem; margin: 0; font-weight: bold;">{total_viagens:,}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_metric3:
                preco_medio = df_viagens_filtrado[col_valor_viagem].mean() if len(df_viagens_filtrado) > 0 else 0
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #fafafa; margin: 0;">� Preço Médio</h4>
                    <p style="color: #f39c12; font-size: 1.3rem; margin: 0; font-weight: bold;">{format_currency(preco_medio)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_metric4:
                # Calcular proporção dentro da política (apenas aéreo e hotel)
                if 'dentro_politica' in colunas_mapeadas_viagem and 'tipo_viagem' in colunas_mapeadas_viagem:
                    col_politica = colunas_mapeadas_viagem['dentro_politica']
                    col_tipo = colunas_mapeadas_viagem['tipo_viagem']
                    
                    # Filtrar apenas aéreo e hotel
                    df_aereo_hotel = df_viagens_filtrado[
                        df_viagens_filtrado[col_tipo].astype(str).str.lower().isin(['aereo', 'aéreo', 'hotel'])
                    ]
                    
                    total_aereo_hotel = len(df_aereo_hotel)
                    if total_aereo_hotel > 0:
                        dentro_politica = len(df_aereo_hotel[
                            df_aereo_hotel[col_politica].astype(str).str.upper() == 'SIM'
                        ])
                        proporcao = (dentro_politica / total_aereo_hotel * 100)
                        cor_proporcao = '#27ae60' if proporcao >= 80 else '#f39c12' if proporcao >= 60 else '#e74c3c'
                    else:
                        proporcao = 0
                        cor_proporcao = '#95a5a6'
                else:
                    proporcao = 0
                    cor_proporcao = '#95a5a6'
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #fafafa; margin: 0;">� Dentro da Política</h4>
                    <p style="color: {cor_proporcao}; font-size: 1.3rem; margin: 0; font-weight: bold;">{proporcao:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Gráfico principal de gastos semanais
            st.markdown("#### 📈 Gastos Semanais com Viagens")
            
            if len(df_viagens_filtrado) > 0:
                gastos_semanais = df_viagens_filtrado.groupby('intervalo_semanal')[col_valor_viagem].sum().reset_index()
                gastos_semanais = gastos_semanais.sort_values('intervalo_semanal')
                gastos_semanais['variacao'] = gastos_semanais[col_valor_viagem].pct_change() * 100
                
                if len(gastos_semanais) > 0:
                    fig_semanal = make_subplots(specs=[[{"secondary_y": True}]])
                    
                    fig_semanal.add_trace(go.Bar(
                        x=gastos_semanais['intervalo_semanal'],
                        y=gastos_semanais[col_valor_viagem],
                        name='Gastos Semanais',
                        marker_color='#1976d2',
                        text=[format_label_optimized(val) for val in gastos_semanais[col_valor_viagem]],
                        textposition='outside',
                        textfont=dict(color='white', size=11, family="Arial Black"),
                        opacity=0.8,
                        hovertemplate='<b>Semana:</b> %{x}<br><b>Gastos:</b> %{customdata}<extra></extra>',
                        customdata=[format_currency(val) for val in gastos_semanais[col_valor_viagem]]
                    ), secondary_y=False)
                    
                    fig_semanal.add_trace(go.Scatter(
                        x=gastos_semanais['intervalo_semanal'],
                        y=gastos_semanais['variacao'],
                        name='Variação (%)',
                        mode='lines+markers+text',
                        line=dict(color='#42a5f5', width=3),
                        marker=dict(size=8, color='#42a5f5', line=dict(width=2, color='white')),
                        text=[f'{v:.1f}%' if not pd.isna(v) else '' for v in gastos_semanais['variacao']],
                        textposition='top center',
                        textfont=dict(color='white', size=10),
                        connectgaps=False,
                        hovertemplate='<b>Semana:</b> %{x}<br><b>Variação:</b> %{y:.1f}%<extra></extra>'
                    ), secondary_y=True)
                    
                    fig_semanal.update_yaxes(title_text='<b>Gastos (R$)</b>', secondary_y=False, gridcolor='rgba(128,128,128,0.2)')
                    fig_semanal.update_yaxes(title_text='<b>Variação (%)</b>', secondary_y=True, gridcolor='rgba(128,128,128,0.1)')
                    
                    fig_semanal.update_layout(
                        height=400,
                        xaxis_title='<b>Período Semanal</b>',
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        xaxis=dict(tickangle=45),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
                    )
                    
                    # Organizar gráficos lado a lado
                    col_graf1, col_graf2 = st.columns(2)
                    
                    with col_graf1:
                        st.plotly_chart(fig_semanal, use_container_width=True)
                    
                    with col_graf2:
                        # Gráfico de setores com maiores gastos
                        st.markdown("#### 🏢 Top 5 Setores - Maiores Gastos")
                        
                        if 'centro_custo' in colunas_mapeadas_viagem and len(df_viagens_filtrado) > 0:
                            col_centro_viagem = colunas_mapeadas_viagem['centro_custo']
                            gastos_setor = (df_viagens_filtrado.groupby(col_centro_viagem)[col_valor_viagem]
                                           .sum().sort_values(ascending=True).tail(5))
                            
                            if len(gastos_setor) > 0:
                                fig_setores = go.Figure(go.Bar(
                                    x=gastos_setor.values,
                                    y=gastos_setor.index,
                                    orientation='h',
                                    marker_color='#1e88e5',
                                    text=[format_label_optimized(val) for val in gastos_setor.values],
                                    textposition='outside',
                                    textfont=dict(color='white', size=11, family="Arial Black"),
                                    hovertemplate='<b>Setor:</b> %{y}<br><b>Gastos:</b> %{customdata}<extra></extra>',
                                    customdata=[format_currency(val) for val in gastos_setor.values]
                                ))
                                
                                fig_setores.update_layout(
                                    height=400,
                                    xaxis_title='<b>Gastos (R$)</b>',
                                    yaxis_title='<b>Setor/Centro de Custo</b>',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    font=dict(color='white'),
                                    margin=dict(l=150, r=50, t=50, b=50)
                                )
                                
                                st.plotly_chart(fig_setores, use_container_width=True)
                            else:
                                st.warning("⚠️ Nenhum dado de setor disponível.")
                        else:
                            st.info("ℹ️ Coluna de Centro de Custo/Setor não identificada ou sem dados.")
                else:
                    st.warning("⚠️ Nenhum dado semanal disponível.")
            else:
                st.warning("⚠️ Nenhum dado disponível para o período selecionado.")
            
            # Tabela detalhada de viagens
            st.markdown("#### 📋 Dados Detalhados de Viagens")
            
            if len(df_viagens_filtrado) > 0:
                df_exibicao_viagem = df_viagens_filtrado.copy()
                df_exibicao_viagem[col_valor_viagem] = df_exibicao_viagem[col_valor_viagem].apply(format_currency)
                df_exibicao_viagem[col_data_viagem] = df_exibicao_viagem[col_data_viagem].dt.strftime('%d/%m/%Y')
                
                colunas_exibir_viagem = [col_data_viagem, col_valor_viagem]
                for chave in ['tipo_viagem', 'centro_custo', 'dentro_politica', 'empresa']:
                    if chave in colunas_mapeadas_viagem:
                        colunas_exibir_viagem.append(colunas_mapeadas_viagem[chave])
                
                df_exibicao_final_viagem = df_exibicao_viagem[colunas_exibir_viagem]
                
                nomes_amigaveis_viagem = {
                    col_data_viagem: 'Data Ida',
                    col_valor_viagem: 'Valor'
                }
                
                if 'tipo_viagem' in colunas_mapeadas_viagem:
                    nomes_amigaveis_viagem[colunas_mapeadas_viagem['tipo_viagem']] = 'Tipo'
                if 'centro_custo' in colunas_mapeadas_viagem:
                    nomes_amigaveis_viagem[colunas_mapeadas_viagem['centro_custo']] = 'Setor'
                if 'dentro_politica' in colunas_mapeadas_viagem:
                    nomes_amigaveis_viagem[colunas_mapeadas_viagem['dentro_politica']] = 'Política'
                if 'empresa' in colunas_mapeadas_viagem:
                    nomes_amigaveis_viagem[colunas_mapeadas_viagem['empresa']] = 'Empresa'
                
                df_exibicao_final_viagem = df_exibicao_final_viagem.rename(columns=nomes_amigaveis_viagem)
                
                # Filtro de busca na tabela
                busca_tabela_viagem = st.text_input("🔍 Buscar na tabela:", placeholder="Digite para filtrar...")
                
                if busca_tabela_viagem:
                    # Filtrar todas as colunas de texto
                    mask = df_exibicao_final_viagem.astype(str).apply(
                        lambda x: x.str.contains(busca_tabela_viagem, case=False, na=False)
                    ).any(axis=1)
                    df_exibicao_final_viagem = df_exibicao_final_viagem[mask]
                
                st.dataframe(
                    df_exibicao_final_viagem, 
                    use_container_width=True,
                    height=400
                )
                
                # Download dos dados
                st.download_button(
                    label="📥 Baixar Dados de Viagens",
                    data=df_exibicao_final_viagem.to_csv(index=False, sep=';').encode('utf-8'),
                    file_name=f"viagens_{data_inicio_viagem.strftime('%d%m%Y')}_a_{data_fim_viagem.strftime('%d%m%Y')}.csv",
                    mime="text/csv",
                    key="download_viagens"
                )
                
                st.info(f"📊 Exibindo {len(df_exibicao_final_viagem)} de {len(df_viagens_filtrado)} registros")
            else:
                st.warning("⚠️ Nenhum dado disponível para exibir.")