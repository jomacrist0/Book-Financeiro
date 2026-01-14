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
    page_title="📈 Investimentos",
    page_icon="📈",
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
    
    /* Card de Métricas Customizado */
    .metric-card {
        background: linear-gradient(135deg, #262730 0%, #2a2d3a 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #30343f;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(14, 17, 23, 0.4);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(14, 17, 23, 0.6);
    }
    .metric-card h4 {
        margin: 0 0 1rem 0 !important;
        font-size: 1rem !important;
        opacity: 0.9;
    }
    .metric-card p {
        margin: 0 !important;
        font-weight: 700 !important;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.1) !important;
    }
    .metric-card small {
        font-size: 0.85rem !important;
        opacity: 0.7 !important;
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
        .metric-card {
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
        <div style="color: #ccc; font-size: 12px; margin-top: 10px;">Investimentos</div>
    </div>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #fafafa; font-weight: 700; margin-bottom: 0;">📈 Dashboard de Investimentos</h1>
    <p style="color: #ccc; font-size: 1.1em;">Análise de Rendimento x CDI por Empresa</p>
</div>
""", unsafe_allow_html=True)

# --- FUNÇÕES ---
def format_currency(value):
    """Formata valor como moeda brasileira"""
    if pd.isna(value) or value == 0:
        return "R$ 0,00"
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def format_percentage(value):
    """Formata valor como porcentagem brasileira"""
    if pd.isna(value):
        return "0,00%"
    return f"{value:.2f}%".replace('.', ',')

@st.cache_data
def load_investment_data():
    """Carrega dados de investimentos"""
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "7Rendimento_dos_investimentos.csv"),
        os.path.join(os.getcwd(), "data", "7Rendimento_dos_investimentos.csv"),
        os.path.join("data", "7Rendimento_dos_investimentos.csv"),
        os.path.join(os.path.dirname(__file__), "..", "7Rendimento_dos_investimentos.csv"),
        os.path.join(os.getcwd(), "7Rendimento_dos_investimentos.csv"),
        "7Rendimento_dos_investimentos.csv"
    ]
    
    df = None
    for path in possible_paths:
        if os.path.exists(path):
            try:
                for sep in [';', '\t', ',']:
                    try:
                        df = pd.read_csv(path, sep=sep, encoding='utf-8')
                        if len(df.columns) > 1:
                            break
                    except:
                        try:
                            df = pd.read_csv(path, sep=sep, encoding='latin-1')
                            if len(df.columns) > 1:
                                break
                        except:
                            continue
                if df is not None and len(df.columns) > 1:
                    break
            except Exception as e:
                st.error(f"Erro ao carregar {path}: {e}")
                continue
    
    if df is None:
        st.error("❌ Arquivo de investimentos não encontrado!")
        st.stop()
    
    # Limpar nomes das colunas
    df.columns = df.columns.str.strip()
    
    # Verificar colunas essenciais
    required_cols = ['Empresa', 'Mês/Ano', 'Rendimento x CDI', 'Média de disponibilidade']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"❌ Colunas obrigatórias não encontradas: {missing_cols}")
        st.info(f"📊 Colunas disponíveis: {list(df.columns)}")
        st.stop()
    
    # Processar dados
    try:
        # Converter Rendimento x CDI para numérico
        if df['Rendimento x CDI'].dtype == 'object':
            df['Rendimento x CDI'] = df['Rendimento x CDI'].str.replace('%', '').str.replace(',', '.').astype(float)
        
        # Converter média de disponibilidade
        if df['Média de disponibilidade'].dtype == 'object':
            df['Média de disponibilidade'] = df['Média de disponibilidade'].str.replace('.', '').str.replace(',', '.').astype(float)
        
        # Criar coluna de data - processar formato brasileiro mês/ano
        def converter_mes_ano(mes_ano_str):
            """Converte formato 'jan/23' para data"""
            try:
                # Mapear meses em português
                meses_pt = {
                    'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04', 
                    'mai': '05', 'jun': '06', 'jul': '07', 'ago': '08',
                    'set': '09', 'out': '10', 'nov': '11', 'dez': '12'
                }
                
                mes, ano = mes_ano_str.lower().split('/')
                mes_num = meses_pt.get(mes, '01')
                
                # Assumir século 21 para anos 00-30, século 20 para 31-99
                if len(ano) == 2:
                    if int(ano) <= 30:
                        ano_completo = '20' + ano
                    else:
                        ano_completo = '19' + ano
                else:
                    ano_completo = ano
                
                return pd.to_datetime(f"{ano_completo}-{mes_num}-01")
            except:
                return pd.NaT
        
        # Aplicar conversão
        df['Data'] = df['Mês/Ano'].apply(converter_mes_ano)
        
        # Criar colunas auxiliares para análise
        df['Ano'] = df['Data'].dt.year.astype(int)  # Converter para int para remover .0
        df['Mês'] = df['Data'].dt.strftime('%b')
        df['Mês_Num'] = df['Data'].dt.month
        df['Mês_Nome'] = df['Data'].dt.month.map({
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        })
        
        # Remover linhas com datas inválidas
        df = df.dropna(subset=['Data'])
        
        return df.sort_values(['Empresa', 'Data'])
        
    except Exception as e:
        st.error(f"❌ Erro ao processar dados: {e}")
        st.stop()

# --- CARREGAMENTO DOS DADOS ---
# Botão para recarregar dados
if st.button("🔄 Atualizar Dados", help="Clique para recarregar os dados"):
    st.cache_data.clear()
    st.rerun()

# Carregamento de dados
df = load_investment_data()

if df is None or len(df) == 0:
    st.warning("⚠️ Nenhum dado encontrado!")
    st.stop()

# --- CONTROLES ---
# Obter dados para filtros depois de carregar o DataFrame
if not df.empty:
    empresas_disponiveis = sorted(df['Empresa'].unique())
    data_min = df['Data'].min()
    data_max = df['Data'].max()
    
    # Definir valores padrão
    data_inicial_default = data_min if data_min else pd.Timestamp.now()
    data_final_max = data_max if data_max else pd.Timestamp.now()
    data_inicial_min = data_min if data_min else pd.Timestamp.now()
else:
    empresas_disponiveis = []
    data_min = pd.Timestamp.now()
    data_max = pd.Timestamp.now()
    data_inicial_default = data_min
    data_final_max = data_max
    data_inicial_min = data_min

# Adicionar separador visual
col1, col2, col3 = st.columns(3)

with col1:
    empresas_selecionadas = st.multiselect(
        "🏢 Empresas:",
        options=empresas_disponiveis,
        default=['Alura'] if 'Alura' in empresas_disponiveis else [empresas_disponiveis[0]],
        key="filtro_empresas"
    )

with col2:
    data_inicio = st.date_input(
        "📅 Data Inicial:",
        value=datetime(2023, 1, 1),
        min_value=data_min,
        max_value=data_max,
        key="data_inicio_invest"
    )

with col3:
    data_fim = st.date_input(
        "📅 Data Final:",
        value=data_max,
        min_value=data_min,
        max_value=data_max,
        key="data_fim_invest"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Filtrar dados
df_filtrado = df[
    (df['Empresa'].isin(empresas_selecionadas)) &
    (df['Data'] >= pd.to_datetime(data_inicio)) &
    (df['Data'] <= pd.to_datetime(data_fim))
].copy()

if len(df_filtrado) == 0:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados!")
    st.stop()

# Obter último mês do período filtrado
ultimo_mes_data = df_filtrado['Data'].max()
df_ultimo_mes = df_filtrado[df_filtrado['Data'] == ultimo_mes_data]

# --- CORES DINÂMICAS BASEADAS NA SELEÇÃO ---
# Cores das empresas (mesmo padrão do saldos do ecossistema)
cores_empresas = {
    'Alura': '#1976d2',
    'FIAP': '#e91e63',
    'PM3': '#9c27b0',
    'Empresa Geral': '#4ECDC4',
    'Casa do Código': '#45B7D1',
    'Caelum': '#FFA07A',
    'INSTITUTO FIAP': '#e91e63'
}

# Função para gerar cores dinâmicas baseadas nas empresas selecionadas
def gerar_cores_dinamicas(empresas_selecionadas, cores_empresas):
    """Gera uma lista de cores baseada nas empresas selecionadas"""
    if len(empresas_selecionadas) == 1:
        # Se apenas uma empresa, usar variações da cor base
        cor_base = cores_empresas.get(empresas_selecionadas[0], '#1976d2')
        return [cor_base]
    else:
        # Se múltiplas empresas, usar a cor específica de cada uma
        return [cores_empresas.get(empresa, '#1976d2') for empresa in empresas_selecionadas]

# Gerar paleta de cores dinâmica
cores_dinamicas = gerar_cores_dinamicas(empresas_selecionadas, cores_empresas)

# --- MÉTRICAS PRINCIPAIS ---
col_metric1, col_metric2 = st.columns(2)

with col_metric1:
    rendimento_ultimo_mes = df_ultimo_mes['Rendimento x CDI'].mean() if len(df_ultimo_mes) > 0 else 0
    # Usar cor dinâmica no card baseada na primeira empresa selecionada
    cor_card = cores_dinamicas[0] if cores_dinamicas else '#1976d2'
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color: #fafafa; margin: 0;">📈 Rendimento x CDI (Último Mês)</h4>
        <p style="color: {cor_card}; font-size: 2rem; margin: 0; font-weight: bold;">{format_percentage(rendimento_ultimo_mes)}</p>
        <small style="color: #ccc;">Referente a {ultimo_mes_data.strftime('%b/%Y')}</small>
    </div>
    """, unsafe_allow_html=True)

with col_metric2:
    disponibilidade_ultimo_mes = df_ultimo_mes['Média de disponibilidade'].mean() if len(df_ultimo_mes) > 0 else 0
    # Usar cor dinâmica alternativa ou secundária
    cor_card2 = cores_dinamicas[1] if len(cores_dinamicas) > 1 else (cores_dinamicas[0] if cores_dinamicas else '#e91e63')
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color: #fafafa; margin: 0;">💰 Média de Disponibilidade (Último Mês)</h4>
        <p style="color: {cor_card2}; font-size: 2rem; margin: 0; font-weight: bold;">{format_currency(disponibilidade_ultimo_mes)}</p>
        <small style="color: #ccc;">Referente a {ultimo_mes_data.strftime('%b/%Y')}</small>
    </div>
    """, unsafe_allow_html=True)
# --- GRÁFICO PRINCIPAL - RENDIMENTO x CDI ---
st.markdown("### 📈 Evolução do Rendimento x CDI")

# Criar figura
fig = go.Figure()

# Para cada empresa e ano, criar uma linha
for idx_empresa, empresa in enumerate(empresas_selecionadas):
    df_empresa = df_filtrado[df_filtrado['Empresa'] == empresa]
    anos_disponiveis = sorted(df_empresa['Ano'].unique())
    
    # Usar cor dinâmica baseada na seleção
    cor_base = cores_dinamicas[idx_empresa] if idx_empresa < len(cores_dinamicas) else '#1976d2'
    
    for i, ano in enumerate(anos_disponiveis):
        df_ano = df_empresa[df_empresa['Ano'] == ano].sort_values('Data')  # Ordenar por data completa
        
        if len(df_ano) == 0:
            continue
            
        # Variar a intensidade da cor por ano (mais escuro = mais recente)
        if len(anos_disponiveis) == 1:
            # Se só tem um ano, usar cor normal
            linha_style = dict(color=cor_base, width=3)
            opacidade = 1.0
        else:
            # Se múltiplos anos, variar estilo
            if i == 0:  # Primeiro ano - mais transparente
                linha_style = dict(color=cor_base, width=2, dash='dot')
                opacidade = 0.6
            elif i == 1:  # Segundo ano - opacidade média
                linha_style = dict(color=cor_base, width=2, dash='dash')
                opacidade = 0.8
            else:  # Terceiro ano ou mais recente - opaco
                linha_style = dict(color=cor_base, width=3)
                opacidade = 1.0
        
        fig.add_trace(go.Scatter(
            x=df_ano['Mês_Nome'],  # Usar Mês_Nome em vez de Mês
            y=df_ano['Rendimento x CDI'],
            mode='lines+markers+text',  # Adicionar texto aos pontos
            name=f'{empresa} ({ano})',  # Ano já é int, não terá .0
            line=linha_style,
            marker=dict(size=6, color=cor_base, opacity=opacidade),
            text=[f'{v:.1f}%' for v in df_ano['Rendimento x CDI']],  # Rótulos de dados
            textposition='top center',  # Posição dos rótulos
            textfont=dict(color='white', size=9, family="Arial"),  # Estilo dos rótulos
            opacity=opacidade,
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'Mês: %{x}<br>' +
                         'Rendimento x CDI: %{y:.2f}%<br>' +
                         '<extra></extra>',
            connectgaps=True  # Conectar pontos mesmo se houver gaps
        ))

fig.update_layout(
    height=500,
    xaxis_title='<b>Mês</b>',
    yaxis_title='<b>Rendimento x CDI (%)</b>',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    hovermode='x unified',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        bgcolor="rgba(38, 39, 48, 0.8)",
        bordercolor="rgba(48, 52, 63, 1)",
        borderwidth=1
    ),
    xaxis=dict(
        gridcolor='rgba(255,255,255,0.1)',
        categoryorder='array',
        categoryarray=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ),
    yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
    # Ajustar margem superior para acomodar rótulos de dados
    margin=dict(t=80, b=60, l=60, r=60)
)

st.plotly_chart(fig, use_container_width=True)

# --- TABELA DETALHADA ---
st.markdown("### 📋 Dados Detalhados")

# Preparar dados para exibição
df_exibicao = df_filtrado.copy()
df_exibicao['Data Formatada'] = df_exibicao['Mês/Ano']  # Usar o campo original em vez de reformatar
df_exibicao['Rendimento x CDI Formatado'] = df_exibicao['Rendimento x CDI'].apply(format_percentage)
df_exibicao['Disponibilidade Formatada'] = df_exibicao['Média de disponibilidade'].apply(format_currency)

# Colunas para exibir
colunas_exibir = ['Empresa', 'Data Formatada', 'Rendimento x CDI Formatado', 'Disponibilidade Formatada', 'Ano']
nomes_colunas = {
    'Empresa': 'Empresa',
    'Data Formatada': 'Mês/Ano',
    'Rendimento x CDI Formatado': 'Rendimento x CDI',
    'Disponibilidade Formatada': 'Média de Disponibilidade',
    'Ano': 'Ano'
}

df_final = df_exibicao[colunas_exibir].rename(columns=nomes_colunas)

# Filtro de busca na tabela
busca_tabela = st.text_input("🔍 Buscar na tabela:", placeholder="Digite para filtrar...")

if busca_tabela:
    mask = df_final.astype(str).apply(
        lambda x: x.str.contains(busca_tabela, case=False, na=False)
    ).any(axis=1)
    df_final = df_final[mask]

st.dataframe(df_final, use_container_width=True, hide_index=True, height=400)

# Download dos dados
st.download_button(
    label="📥 Baixar Dados de Investimentos",
    data=df_final.to_csv(index=False, sep=';').encode('utf-8'),
    file_name=f"investimentos_{data_inicio.strftime('%d%m%Y')}_a_{data_fim.strftime('%d%m%Y')}.csv",
    mime="text/csv",
    key="download_investimentos"
)

st.info(f"📊 Exibindo {len(df_final)} de {len(df_filtrado)} registros")
