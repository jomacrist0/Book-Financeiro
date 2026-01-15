import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
sys.path.append('..')
from auth import verificar_autenticacao

# --- AUTENTICAÇÃO ---
verificar_autenticacao()

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="💳 Análise dos Meios de Pagamento",
    page_icon="💳",
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
        <div style="color: #ccc; font-size: 12px; margin-top: 10px;">Meios de Pagamento</div>
    </div>
    """, unsafe_allow_html=True)

# --- BOTÃO DE ATUALIZAÇÃO ---
col_refresh = st.columns([3, 1])
with col_refresh[1]:
    if st.button("🔄 Atualizar Dados", type="primary"):
        st.cache_data.clear()
        st.success("✅ Cache limpo! Dados serão recarregados.")
        st.rerun()

# --- HEADER ---
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #fafafa; font-weight: 700; margin-bottom: 0;">💳 Dashboard de Meios de Pagamento</h1>
    <p style="color: #ccc; font-size: 1.1em;">Análise completa dos métodos de pagamento</p>
</div>
""", unsafe_allow_html=True)

# ============ HELPERS ============
@st.cache_data(show_spinner=False)
def load_data():
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "3Streamlit - Ecossistema - Análise dos meios de pagamento.csv"),
        os.path.join(os.getcwd(), "data", "3Streamlit - Ecossistema - Análise dos meios de pagamento.csv"),
        os.path.join("data", "3Streamlit - Ecossistema - Análise dos meios de pagamento.csv"),
        os.path.join(os.path.dirname(__file__), "..", "3Streamlit - Ecossistema - Análise dos meios de pagamento.csv"),
        os.path.join(os.getcwd(), "3Streamlit - Ecossistema - Análise dos meios de pagamento.csv")
    ]
    
    path = None
    for p in possible_paths:
        if os.path.exists(p):
            path = p
            break
    
    if path is None:
        return pd.DataFrame()
    for sep in [';','\t',',']:
        df = pd.read_csv(path, sep=sep, encoding='utf-8')
        if df.shape[1] > 1 or sep == ',':
            break
    df.columns = [c.strip() for c in df.columns]
    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')
    for col in ['Valor Original','Valor da taxa']:
        if col in df.columns:
            df[col] = (df[col].astype(str)
                                 .str.replace('R$','', regex=False)
                                 .str.replace('R$ ','', regex=False)
                                 .str.replace('.','', regex=False)
                                 .str.replace(',','.', regex=False)
                                 .str.strip())
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    if 'Parcelas' in df.columns:
        df['Parcelas'] = pd.to_numeric(df['Parcelas'], errors='coerce').fillna(1)
    if 'Empresa' not in df.columns:
        df['Empresa'] = 'Empresa Única'
    return df

def fmt_cur(v: float) -> str:
    try:
        return f"R$ {v:,.0f}".replace(',', 'X').replace('.', ',').replace('X','.')
    except:  # noqa
        return 'R$ 0'

def agrupar(df: pd.DataFrame, gran: str) -> pd.DataFrame:
    if df.empty or 'Data' not in df.columns: return df
    if gran == 'Diário': 
        # Para o gráfico diário, vamos criar um range completo de datas
        df_sorted = df.sort_values('Data')
        date_range = pd.date_range(start=df_sorted['Data'].min(), end=df_sorted['Data'].max(), freq='D')
        daily_data = df.groupby(df['Data'].dt.date).agg({'Valor Original':'sum','Valor da taxa':'sum'}).reset_index()
        daily_data['Data'] = pd.to_datetime(daily_data['Data'])
        
        # Criar DataFrame com todas as datas no range
        complete_range = pd.DataFrame({'Data': date_range})
        result = complete_range.merge(daily_data, on='Data', how='left').fillna(0)
        return result
        
    freq = {'Semanal':'W-SUN','Mensal':'M','Anual':'Y'}.get(gran,'W-SUN')
    g = df.groupby(pd.Grouper(key='Data', freq=freq)).agg({'Valor Original':'sum','Valor da taxa':'sum'}).reset_index()
    if gran=='Semanal': g['Periodo']=g['Data'].dt.strftime('Sem %U - %d/%m')
    elif gran=='Mensal': g['Periodo']=g['Data'].dt.strftime('%b/%Y')
    else: g['Periodo']=g['Data'].dt.strftime('%Y')
    return g

def aplicar(df, metodo=None, prov=None, tipo=None, band=None):
    d = df.copy()
    if metodo: d = d[d['Método de Pagamento'].isin(metodo)]
    if prov: d = d[d['Provedor'].isin(prov)]
    if tipo: d = d[d['Tipo de pagamento'].isin(tipo)]
    if band: d = d[d['Bandeira do cartão'].isin(band)]
    return d

# ============ LOAD DATA ============
df = load_data()
if df.empty:
    st.error('Arquivo não encontrado ou vazio.')
    st.stop()

# ============ GLOBAL FILTERS ============
st.markdown('<div class="compact-controls">', unsafe_allow_html=True)
st.markdown("### 🔧 Filtros Globais")

data_min = df['Data'].min().date() if 'Data' in df.columns else None
data_max = df['Data'].max().date() if 'Data' in df.columns else None

# Calcular data inicial como 8 semanas antes da data final
if data_max:
    data_inicial_default = data_max - pd.Timedelta(weeks=8)
    if data_inicial_default < data_min:
        data_inicial_default = data_min
else:
    data_inicial_default = data_min

# Primeira linha de filtros
g1,g2,g3,g4 = st.columns(4)
with g1:
    if data_min and data_max:
        periodo_inicio = st.date_input('📅 Data inicial', data_inicial_default, min_value=data_min, max_value=data_max, key='g_ini')
with g2:
    if data_min and data_max:
        periodo_fim = st.date_input('📅 Data final', data_max, min_value=data_min, max_value=data_max, key='g_fim')
with g3:
    if data_min and data_max:
        granularidade = st.selectbox('📊 Granularidade', ['Diário','Semanal','Mensal','Anual'], index=1, key='g_gran')
with g4:
    empresas = sorted(df['Empresa'].unique())
    # Pré-selecionar Alura se disponível
    empresas_default = ['Alura'] if 'Alura' in empresas else []
    empresas_sel = st.multiselect('🏢 Empresas', empresas, default=empresas_default, key='g_emp')

# Segunda linha de filtros
g5,g6 = st.columns(2)
with g5:
    # Método global com pré-seleção
    metodos_globais = sorted(df['Método de Pagamento'].dropna().unique())
    metodos_default = []
    for metodo in ['Cartão de Crédito', 'Nupay', 'Paypal']:
        if metodo in metodos_globais:
            metodos_default.append(metodo)
    metodos_sel = st.multiselect('💳 Métodos', metodos_globais, default=metodos_default, key='g_met')
with g6:
    # Tipo global com pré-seleção para "parcelado"
    tipos_globais = sorted(df['Tipo de pagamento'].dropna().unique())
    tipos_default = [tipo for tipo in tipos_globais if 'parcelado' in tipo.lower()]
    tipos_sel = st.multiselect('🎯 Tipos', tipos_globais, default=tipos_default, key='g_tipo')

st.markdown('</div>', unsafe_allow_html=True)

df_base = df.copy()
if data_min and data_max and 'Data' in df_base.columns:
    df_base = df_base[(df_base['Data']>=pd.to_datetime(periodo_inicio)) & (df_base['Data']<=pd.to_datetime(periodo_fim))]
if empresas_sel:
    df_base = df_base[df_base['Empresa'].isin(empresas_sel)]
if metodos_sel:
    df_base = df_base[df_base['Método de Pagamento'].isin(metodos_sel)]
if tipos_sel:
    df_base = df_base[df_base['Tipo de pagamento'].isin(tipos_sel)]
if df_base.empty:
    st.warning('⚠️ Nenhum dado para os filtros gerais.')
    st.stop()

# --- SISTEMA DE CORES DINÂMICAS ---
def gerar_cores_pagamento_dinamicas(empresas_sel):
    """Gera cores para gráficos de pagamento baseadas na empresa principal"""
    paletas_pagamento = {
        'Alura': {  # Base azul
            'primary': '#1976d2',      # Azul principal
            'secondary': '#42a5f5',    # Azul claro
            'accent': '#ff6b35',       # Laranja complementar
            'success': '#4caf50',      # Verde
            'warning': '#ffc107',      # Amarelo
            'info': '#00bcd4'          # Ciano
        },
        'FIAP': {  # Base rosa
            'primary': '#e91e63',      # Rosa principal
            'secondary': '#f06292',    # Rosa claro
            'accent': '#2196f3',       # Azul complementar
            'success': '#8bc34a',      # Verde claro
            'warning': '#ff9800',      # Laranja
            'info': '#00acc1'          # Ciano escuro
        },
        'PM3': {  # Base roxo
            'primary': '#9c27b0',      # Roxo principal
            'secondary': '#ba68c8',    # Roxo claro
            'accent': '#ff5722',       # Laranja avermelhado
            'success': '#66bb6a',      # Verde médio
            'warning': '#ffb74d',      # Laranja claro
            'info': '#26c6da'          # Ciano claro
        }
    }
    
    # Determinar empresa principal
    empresa_principal = 'Alura'
    if empresas_sel:
        if 'Alura' in empresas_sel:
            empresa_principal = 'Alura'
        elif 'FIAP' in empresas_sel:
            empresa_principal = 'FIAP'
        elif 'PM3' in empresas_sel:
            empresa_principal = 'PM3'
    
    return paletas_pagamento.get(empresa_principal, paletas_pagamento['Alura'])

# Gerar paleta dinâmica
cores_pagamento = gerar_cores_pagamento_dinamicas(empresas_sel)

# ============ METRICS ============
vol_total = df_base['Valor Original'].sum()
taxa_total = df_base['Valor da taxa'].sum() if 'Valor da taxa' in df_base.columns else 0
custo_pct = (taxa_total/vol_total*100) if vol_total>0 else 0
parcelas_med = df_base['Parcelas'].mean() if 'Parcelas' in df_base.columns else 1
if 'Status' in df_base.columns:
    aprov = df_base['Status'].str.contains('aprovado|sucesso', case=False, na=False).sum()
    taxa_apr = aprov/len(df_base)*100 if len(df_base)>0 else 0
elif 'Aprovado' in df_base.columns:
    taxa_apr = df_base['Aprovado'].mean()*100
else:
    taxa_apr = 100
m1,m2,m3,m4 = st.columns(4)
m1.metric('💰 Volume Total', fmt_cur(vol_total))
m2.metric('💸 Custo de Transação', f'{custo_pct:.2f}%')
m3.metric('💳 Parcelamento Médio', f'{parcelas_med:.1f}x')
m4.metric('✅ Taxa de Aprovação', f'{taxa_apr:.1f}%')

st.markdown('---')
tab_vol, tab_custo, tab_parc, tab_apr, tab_participacao = st.tabs(['📈 Volume','💸 Custo','🧮 Parcelamento','✅ Aprovação','📊 Participação'])

# ============ TAB VOLUME ============
with tab_vol:
    st.subheader('📈 Volume')
    c1,c2,c3,c4 = st.columns(4)
    with c1: met_v = st.multiselect('Método', sorted(df_base['Método de Pagamento'].dropna().unique()), key='vol_met')
    with c2: prov_v = st.multiselect('Provedor', sorted(df_base['Provedor'].dropna().unique()), key='vol_prov')
    with c3: tipo_v = st.multiselect('Tipo', sorted(df_base['Tipo de pagamento'].dropna().unique()), key='vol_tipo')
    with c4: band_v = st.multiselect('Bandeira', sorted(df_base['Bandeira do cartão'].dropna().unique()), key='vol_band')
    dvol = aplicar(df_base, met_v, prov_v, tipo_v, band_v)
    if dvol.empty:
        st.info('Sem dados.')
    else:
        if 'Data' in dvol.columns:
            g = agrupar(dvol, granularidade)
            x = g['Data'] if granularidade=='Diário' else g['Periodo']
            
            # Gráfico combinado de barras e linha
            fig = make_subplots(specs=[[{"secondary_y":True}]])
            
            # Barras para volume
            fig.add_trace(go.Bar(
                x=x, 
                y=g['Valor Original'], 
                name='Volume (R$)', 
                marker_color=cores_pagamento['primary'],
                text=[fmt_cur(v) for v in g['Valor Original']],
                textposition='outside',
                textfont=dict(color='white', family='Arial Black')
            ), secondary_y=False)
            
            # Linha para variação percentual
            variacao = g['Valor Original'].pct_change() * 100
            fig.add_trace(go.Scatter(
                x=x, 
                y=variacao, 
                name='Variação (%)', 
                mode='lines+markers+text',
                line=dict(color=cores_pagamento['accent']),
                text=[f'{v:.1f}%' if not pd.isna(v) else '' for v in variacao],
                textposition='top center',
                textfont=dict(color='white', family='Arial Black'),
                connectgaps=True
            ), secondary_y=True)
            
            fig.update_yaxes(title_text='Volume (R$)', secondary_y=False)
            fig.update_yaxes(title_text='Variação (%)', secondary_y=True)
            fig.update_layout(
                height=500, 
                title=f'Volume e Variação - {granularidade}', 
                xaxis_title='Período',
                margin=dict(t=80, b=60, l=100, r=60),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('#### Provedores')
        tbl = dvol.groupby('Provedor')['Valor Original'].agg(['sum','count','mean']).round(2)
        tbl.columns = ['Volume Total','Qtd','Ticket Médio']
        tbl['Participação (%)'] = (tbl['Volume Total']/tbl['Volume Total'].sum()*100).round(2)
        disp = tbl.copy()
        disp['Volume Total'] = disp['Volume Total'].apply(fmt_cur)
        disp['Ticket Médio'] = disp['Ticket Médio'].apply(fmt_cur)
        disp['Participação (%)'] = disp['Participação (%)'].apply(lambda v:f'{v:.2f}%')
        st.dataframe(disp, use_container_width=True, height=360)

# ============ TAB CUSTO ============
with tab_custo:
    st.subheader('💸 Custo')
    c1,c2,c3,c4 = st.columns(4)
    with c1: met_c = st.multiselect('Método', sorted(df_base['Método de Pagamento'].dropna().unique()), key='c_met')
    with c2: prov_c = st.multiselect('Provedor', sorted(df_base['Provedor'].dropna().unique()), key='c_prov')
    with c3: tipo_c = st.multiselect('Tipo', sorted(df_base['Tipo de pagamento'].dropna().unique()), key='c_tipo')
    with c4: band_c = st.multiselect('Bandeira', sorted(df_base['Bandeira do cartão'].dropna().unique()), key='c_band')
    dcusto = aplicar(df_base, met_c, prov_c, tipo_c, band_c)
    if dcusto.empty:
        st.info('Sem dados.')
    else:
        if 'Data' in dcusto.columns:
            g = agrupar(dcusto, granularidade)
            g['Custo (%)'] = (g['Valor da taxa']/g['Valor Original']*100).fillna(0)
            x = g['Data'] if granularidade=='Diário' else g['Periodo']
            
            # Gráfico combinado de barras e linha
            fig = make_subplots(specs=[[{"secondary_y":True}]])
            
            # Barras para custo percentual
            fig.add_trace(go.Bar(
                x=x, 
                y=g['Custo (%)'], 
                name='Custo (%)', 
                marker_color='#ff6b35',
                text=[f'{v:.2f}%' for v in g['Custo (%)']],
                textposition='outside',
                textfont=dict(color='white', family='Arial Black')
            ), secondary_y=False)
            
            # Linha para variação percentual do custo
            variacao = g['Custo (%)'].pct_change() * 100
            fig.add_trace(go.Scatter(
                x=x, 
                y=variacao, 
                name='Variação (%)', 
                mode='lines+markers+text',
                line=dict(color='#2ca02c'),
                text=[f'{v:.1f}%' if not pd.isna(v) else '' for v in variacao],
                textposition='top center',
                textfont=dict(color='white', family='Arial Black'),
                connectgaps=True
            ), secondary_y=True)
            
            fig.update_yaxes(title_text='Custo (%)', secondary_y=False)
            fig.update_yaxes(title_text='Variação (%)', secondary_y=True)
            fig.update_layout(
                height=400, 
                title=f'Custo e Variação - {granularidade}', 
                xaxis_title='Período',
                margin=dict(t=80, b=60, l=60, r=60),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('#### Provedores')
        prov_tbl = dcusto.groupby('Provedor').agg({'Valor da taxa':'sum','Valor Original':'sum'}).round(2)
        prov_tbl['Custo (%)'] = (prov_tbl['Valor da taxa']/prov_tbl['Valor Original']*100).round(2)
        disp = prov_tbl.copy()
        disp['Valor da taxa'] = disp['Valor da taxa'].apply(fmt_cur)
        disp['Valor Original'] = disp['Valor Original'].apply(fmt_cur)
        disp['Custo (%)'] = disp['Custo (%)'].apply(lambda v:f'{v:.2f}%')
        st.dataframe(disp, use_container_width=True, height=360)

# ============ TAB PARCELAMENTO ============
with tab_parc:
    st.subheader('🧮 Parcelamento')
    c1,c2,c3,c4 = st.columns(4)
    
    # Pré-seleção para métodos
    metodos_parc_default = []
    metodos_parc_disponiveis = sorted(df_base['Método de Pagamento'].dropna().unique())
    for metodo in ['Cartão de Crédito', 'Nupay', 'Paypal']:
        if metodo in metodos_parc_disponiveis:
            metodos_parc_default.append(metodo)
    
    # Pré-seleção para tipo parcelado
    tipos_parc_disponiveis = sorted(df_base['Tipo de pagamento'].dropna().unique())
    tipos_parc_default = [tipo for tipo in tipos_parc_disponiveis if 'parcelado' in tipo.lower()]
    
    with c1: met_p = st.multiselect('Método', metodos_parc_disponiveis, default=metodos_parc_default, key='p_met')
    with c2: prov_p = st.multiselect('Provedor', sorted(df_base['Provedor'].dropna().unique()), key='p_prov')
    with c3: tipo_p = st.multiselect('Tipo', tipos_parc_disponiveis, default=tipos_parc_default, key='p_tipo')
    with c4: band_p = st.multiselect('Bandeira', sorted(df_base['Bandeira do cartão'].dropna().unique()), key='p_band')
    
    dparc = aplicar(df_base, met_p, prov_p, tipo_p, band_p)
    if dparc.empty:
        st.info('Sem dados.')
    else:
        if 'Data' in dparc.columns:
            # Calcular parcelamento médio por período
            if granularidade == 'Diário':
                g_parc = dparc.groupby(dparc['Data'].dt.date).agg({
                    'Parcelas': 'mean',
                    'Valor Original': 'sum'
                }).reset_index()
                g_parc['Data'] = pd.to_datetime(g_parc['Data'])
                x = g_parc['Data']
            else:
                freq = {'Semanal':'W-SUN','Mensal':'M','Anual':'Y'}.get(granularidade,'W-SUN')
                g_parc = dparc.groupby(pd.Grouper(key='Data', freq=freq)).agg({
                    'Parcelas': 'mean',
                    'Valor Original': 'sum'
                }).reset_index()
                if granularidade=='Semanal': g_parc['Periodo']=g_parc['Data'].dt.strftime('Sem %U - %d/%m')
                elif granularidade=='Mensal': g_parc['Periodo']=g_parc['Data'].dt.strftime('%b/%Y')
                else: g_parc['Periodo']=g_parc['Data'].dt.strftime('%Y')
                x = g_parc['Periodo']
            
            # Gráfico combinado
            fig = make_subplots(specs=[[{"secondary_y":True}]])
            
            # Barras para parcelamento médio
            fig.add_trace(go.Bar(
                x=x, 
                y=g_parc['Parcelas'], 
                name='Parcelas Médias', 
                marker_color='#1f77b4',
                text=[f'{v:.1f}x' for v in g_parc['Parcelas']],
                textposition='outside',
                textfont=dict(color='white', family='Arial Black')
            ), secondary_y=False)
            
            # Linha para variação percentual das parcelas
            variacao = g_parc['Parcelas'].pct_change() * 100
            fig.add_trace(go.Scatter(
                x=x, 
                y=variacao, 
                name='Variação (%)', 
                mode='lines+markers+text',
                line=dict(color='#ff6b35'),
                text=[f'{v:.1f}%' if not pd.isna(v) else '' for v in variacao],
                textposition='top center',
                textfont=dict(color='white', family='Arial Black'),
                connectgaps=True
            ), secondary_y=True)
            
            fig.update_yaxes(title_text='Parcelas Médias', secondary_y=False)
            fig.update_yaxes(title_text='Variação (%)', secondary_y=True)
            fig.update_layout(
                height=400, 
                title='Parcelamento Médio e Variação',
                margin=dict(t=80, b=60, l=60, r=60),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('#### Métodos')
        tbl = dparc.groupby('Método de Pagamento').agg({'Valor Original':['sum','count','mean','max'],'Parcelas':'mean'}).round(2)
        tbl.columns = ['Valor Total','Qtd','Ticket Médio','Maior Transação','Parcelas Médias']
        soma = tbl['Valor Total'].sum()
        tbl['Participação (%)'] = (tbl['Valor Total']/soma*100).round(2) if soma>0 else 0
        disp = tbl.copy()
        for c in ['Valor Total','Ticket Médio','Maior Transação']: disp[c] = disp[c].apply(fmt_cur)
        disp['Parcelas Médias'] = disp['Parcelas Médias'].apply(lambda v:f'{v:.1f}x')
        disp['Participação (%)'] = disp['Participação (%)'].apply(lambda v:f'{v:.2f}%')
        st.dataframe(disp, use_container_width=True, height=360)
        st.download_button('📥 Baixar Análise de Parcelamento (CSV)', data=tbl.to_csv(), file_name=f'analise_parcelamento_{periodo_inicio}_{periodo_fim}.csv', mime='text/csv')

# ============ TAB APROVAÇÃO ============
with tab_apr:
    st.subheader('✅ Aprovação')
    c1,c2,c3,c4 = st.columns(4)
    with c1: met_a = st.multiselect('Método', sorted(df_base['Método de Pagamento'].dropna().unique()), key='a_met')
    with c2: prov_a = st.multiselect('Provedor', sorted(df_base['Provedor'].dropna().unique()), key='a_prov')
    with c3: tipo_a = st.multiselect('Tipo', sorted(df_base['Tipo de pagamento'].dropna().unique()), key='a_tipo')
    with c4: band_a = st.multiselect('Bandeira', sorted(df_base['Bandeira do cartão'].dropna().unique()), key='a_band')
    dapr = aplicar(df_base, met_a, prov_a, tipo_a, band_a)
    if dapr.empty:
        st.info('Sem dados.')
    else:
        if 'Data' in dapr.columns and ('Status' in dapr.columns or 'Aprovado' in dapr.columns):
            base = dapr.copy()
            if 'Status' in base.columns:
                base['Aprovada'] = base['Status'].str.contains('aprovado|sucesso', case=False, na=False)
            elif 'Aprovado' in base.columns:
                base['Aprovada'] = base['Aprovado'].astype(bool)
            if 'Aprovada' in base.columns:
                if granularidade=='Diário':
                    serie = base.groupby(base['Data'].dt.date)['Aprovada'].mean()*100
                    x = serie.index
                else:
                    base['Periodo'] = agrupar(base, granularidade)['Periodo']
                    serie = base.groupby(base['Periodo'])['Aprovada'].mean()*100
                    x = serie.index
                fig = go.Figure(go.Scatter(x=x, y=serie.values, mode='lines+markers', line=dict(color='#2ca02c'), connectgaps=True))
                fig.update_layout(
                    height=360, 
                    title='Taxa de Aprovação Temporal', 
                    xaxis_title='Período', 
                    yaxis_title='Taxa (%)',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig, use_container_width=True)
        st.markdown('#### Métodos')
        if 'Status' in dapr.columns:
            met = dapr.groupby('Método de Pagamento')['Status'].apply(lambda s: (s.str.contains('aprovado|sucesso', case=False, na=False).sum()/len(s)*100) if len(s)>0 else 0).reset_index(name='Taxa (%)')
        elif 'Aprovado' in dapr.columns:
            met = dapr.groupby('Método de Pagamento')['Aprovado'].mean()*100
            met = met.reset_index().rename(columns={'Aprovado':'Taxa (%)'})
        else:
            met = pd.DataFrame(columns=['Método de Pagamento','Taxa (%)'])
        if not met.empty:
            figm = px.bar(met, x='Método de Pagamento', y='Taxa (%)', title='Taxa por Método')
            st.plotly_chart(figm, use_container_width=True)
            st.dataframe(met, use_container_width=True, height=360)
        else:
            st.info('Sem coluna de aprovação.')

# ============ TAB PARTICIPAÇÃO ============
with tab_participacao:
    st.subheader('📊 Participação dos Provedores')
    
    # Filtros com pré-seleção para métodos
    metodos_default = []
    metodos_disponiveis = sorted(df_base['Método de Pagamento'].dropna().unique())
    for metodo in ['Cartão de Crédito', 'Nupay', 'Paypal']:
        if metodo in metodos_disponiveis:
            metodos_default.append(metodo)
    
    # Todos os filtros em uma linha
    c1,c2,c3 = st.columns(3)
    with c1: 
        met_part = st.multiselect('💳 Método', metodos_disponiveis, default=metodos_default, key='part_met')
    with c2: 
        tipo_part = st.multiselect('🎯 Tipo', sorted(df_base['Tipo de pagamento'].dropna().unique()), key='part_tipo')
    with c3: 
        if 'Bandeira do cartão' in df_base.columns:
            band_part = st.multiselect('🏦 Bandeira', sorted(df_base['Bandeira do cartão'].dropna().unique()), key='part_band')
        else:
            band_part = []
            st.write("")  # Espaço em branco para manter alinhamento
    
    # Aplicar filtros sem provedor
    dpart = df_base.copy()
    if met_part:
        dpart = dpart[dpart['Método de Pagamento'].isin(met_part)]
    if tipo_part:
        dpart = dpart[dpart['Tipo de pagamento'].isin(tipo_part)]
    if band_part and 'Bandeira do cartão' in dpart.columns:
        dpart = dpart[dpart['Bandeira do cartão'].isin(band_part)]
    
    if dpart.empty:
        st.info('Sem dados para os filtros selecionados.')
    else:
        if 'Data' in dpart.columns:
            # Criar gráfico temporal de participação por provedor
            g = agrupar(dpart, granularidade)
            
            if granularidade == 'Diário':
                # Agrupar por data e provedor para calcular participação diária
                daily_provider = dpart.groupby([dparc['Data'].dt.date, 'Provedor'])['Valor Original'].sum().unstack(fill_value=0)
                daily_total = daily_provider.sum(axis=1)
                daily_participation = daily_provider.div(daily_total, axis=0) * 100
                
                fig = go.Figure()
                colors = px.colors.qualitative.Set1
                for i, provedor in enumerate(daily_participation.columns):
                    fig.add_trace(go.Scatter(
                        x=daily_participation.index, 
                        y=daily_participation[provedor], 
                        mode='lines+markers+text',
                        name=provedor,
                        line=dict(color=colors[i % len(colors)]),
                        text=[f'{v:.1f}%' for v in daily_participation[provedor]],
                        textposition='top center',
                        textfont=dict(color='white', family='Arial Black'),
                        connectgaps=True
                    ))
                
                fig.update_layout(
                    height=500, 
                    title=f'Participação dos Provedores - {granularidade}',
                    xaxis_title='Período', 
                    yaxis_title='Participação (%)',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(t=120, b=60, l=60, r=60),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            else:
                # Para outras granularidades (semanal, mensal, anual)
                if granularidade == 'Semanal':
                    periodo_col = dpart['Data'].dt.to_period('W-SUN')
                elif granularidade == 'Mensal':
                    periodo_col = dpart['Data'].dt.to_period('M')
                else:  # Anual
                    periodo_col = dpart['Data'].dt.to_period('Y')
                
                period_provider = dpart.groupby([periodo_col, 'Provedor'])['Valor Original'].sum().unstack(fill_value=0)
                period_total = period_provider.sum(axis=1)
                period_participation = period_provider.div(period_total, axis=0) * 100
                
                fig = go.Figure()
                colors = px.colors.qualitative.Set1
                for i, provedor in enumerate(period_participation.columns):
                    x_labels = period_participation.index.astype(str)
                    fig.add_trace(go.Scatter(
                        x=x_labels, 
                        y=period_participation[provedor], 
                        mode='lines+markers+text',
                        name=provedor,
                        line=dict(color=colors[i % len(colors)]),
                        text=[f'{v:.1f}%' for v in period_participation[provedor]],
                        textposition='top center',
                        textfont=dict(color='white', family='Arial Black'),
                        connectgaps=True
                    ))
                
                fig.update_layout(
                    height=500, 
                    title=f'Participação dos Provedores - {granularidade}',
                    xaxis_title='Período', 
                    yaxis_title='Participação (%)',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(t=120, b=60, l=60, r=60),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('#### Participação Geral dos Provedores')
        # Tabela de participação geral
        tbl_part = dpart.groupby('Provedor')['Valor Original'].agg(['sum','count','mean']).round(2)
        tbl_part.columns = ['Volume Total','Qtd Transações','Ticket Médio']
        total_volume = tbl_part['Volume Total'].sum()
        tbl_part['Participação (%)'] = (tbl_part['Volume Total']/total_volume*100).round(2) if total_volume > 0 else 0
        tbl_part = tbl_part.sort_values('Participação (%)', ascending=False)
        
        # Formatação para exibição
        disp_part = tbl_part.copy()
        disp_part['Volume Total'] = disp_part['Volume Total'].apply(fmt_cur)
        disp_part['Ticket Médio'] = disp_part['Ticket Médio'].apply(fmt_cur)
        disp_part['Participação (%)'] = disp_part['Participação (%)'].apply(lambda v:f'{v:.2f}%')
        
        st.dataframe(disp_part, use_container_width=True, height=360)
