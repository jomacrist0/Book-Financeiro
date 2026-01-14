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
    page_title="📊 Análise de Aging PM3",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CUSTOMIZADO COM TEMA ESCURO ALUN ---
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
    
    /* Sidebar */
    .css-1d391kg { background-color: #262730 !important; }
    .css-1d391kg .css-6qob1r { background-color: #262730 !important; }
    
    /* Filtros compactos */
    .compact-controls {
        background: rgba(38, 39, 48, 0.3);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 1px solid #30343f;
    }
    
    /* Métricas */
    .metric-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #3b82f6;
        text-align: center;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #262730;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        border: 1px solid #30343f;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff6b35 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR COM LOGO ALUN ---
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%); 
                padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 30px;
                border: 2px solid #ff6b35;">
        <div style="background: black; color: white; padding: 8px 16px; border-radius: 8px; 
                    font-size: 24px; font-weight: bold; margin-bottom: 10px;">ALUN</div>
        <div style="color: #ff6b35; font-size: 14px; font-weight: bold;">📊 Análise de Aging PM3</div>
    </div>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='text-align: center; color: #fafafa;'>📊 Análise de Aging - PM3</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0a0a0; font-size: 1.1em;'>Análise detalhada de contas a receber com foco em inadimplência</p>", unsafe_allow_html=True)

# --- FUNÇÃO DE CARREGAMENTO DE DADOS ---
@st.cache_data
def load_aging_data():
    """Carrega e processa os dados de aging"""
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "Aging_PM3.csv"),
        os.path.join(os.getcwd(), "data", "Aging_PM3.csv"),
        os.path.join("data", "Aging_PM3.csv"),
        os.path.join(os.path.dirname(__file__), "..", "data", "4Aging.csv"),
        os.path.join(os.path.dirname(__file__), "..", "4Aging.csv"),
        os.path.join(os.getcwd(), "4Aging.csv"),
        "4Aging.csv"
    ]
    
    df = None
    separators = [';', '\t', ',']
    
    for path in possible_paths:
        if os.path.exists(path):
            for sep in separators:
                try:
                    df = pd.read_csv(path, sep=sep, encoding='utf-8')
                    if df.shape[1] > 1:  # Se tiver mais de uma coluna, provavelmente é o separador correto
                        break
                except:
                    continue
            if df is not None and df.shape[1] > 1:
                break
    
    if df is None:
        st.error("❌ Arquivo 4Aging.csv não encontrado!")
        st.stop()
    
    # Limpeza dos dados
    df.columns = df.columns.str.strip()
    
    # Verificar colunas essenciais
    required_columns = ['Cliente', 'Valor', 'Intervalo (vencimento)', 'Porte', 'Datas de análise']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"❌ Colunas obrigatórias não encontradas: {missing_columns}")
        st.stop()
    
    # Processar valores
    if df['Valor'].dtype == 'object':
        df['Valor'] = df['Valor'].astype(str).str.replace('.', '').str.replace(',', '.').astype(float)
    
    # Processar datas
    df['Datas de análise'] = pd.to_datetime(df['Datas de análise'], format='%d/%m/%Y', errors='coerce')
    
    if 'Data Emissão' in df.columns:
        df['Data Emissão'] = pd.to_datetime(df['Data Emissão'], format='%d/%m/%Y', errors='coerce')
    
    if 'Data de vencimento' in df.columns:
        df['Data de vencimento'] = pd.to_datetime(df['Data de vencimento'], format='%d/%m/%Y', errors='coerce')
    
    # Criar categorias de aging
    df['Categoria_Aging'] = df['Intervalo (vencimento)'].fillna('Sem informação')
    
    return df

# Carregar dados
df_aging = load_aging_data()

# --- FILTROS ---
st.markdown('<div class="compact-controls">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    data_min = df_aging['Datas de análise'].min()
    data_max = df_aging['Datas de análise'].max()
    data_inicio = st.date_input(
        "📅 Data Inicial",
        value=data_max - timedelta(days=30),
        min_value=data_min,
        max_value=data_max
    )

with col2:
    data_fim = st.date_input(
        "📅 Data Final",
        value=data_max,
        min_value=data_min,
        max_value=data_max
    )

with col3:
    portes_disponiveis = df_aging['Porte'].unique()
    portes_selecionados = st.multiselect(
        "🏢 Porte das Empresas",
        options=portes_disponiveis,
        default=portes_disponiveis
    )

with col4:
    categorias_aging = df_aging['Categoria_Aging'].unique()
    categorias_selecionadas = st.multiselect(
        "⏱️ Intervalos de Vencimento",
        options=categorias_aging,
        default=categorias_aging
    )

st.markdown('</div>', unsafe_allow_html=True)

# Aplicar filtros
df_filtrado = df_aging[
    (df_aging['Datas de análise'] >= pd.Timestamp(data_inicio)) &
    (df_aging['Datas de análise'] <= pd.Timestamp(data_fim)) &
    (df_aging['Porte'].isin(portes_selecionados)) &
    (df_aging['Categoria_Aging'].isin(categorias_selecionadas))
].copy()

if df_filtrado.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros aplicados.")
    st.stop()

# --- MÉTRICAS PRINCIPAIS ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_valor = df_filtrado['Valor'].sum()
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="color: white; margin: 0;">💰 Total a Receber</h3>
        <h2 style="color: #ffd700; margin: 0;">R$ {total_valor:,.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_clientes = df_filtrado['Cliente'].nunique()
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="color: white; margin: 0;">👥 Total de Clientes</h3>
        <h2 style="color: #ffd700; margin: 0;">{total_clientes:,}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    valor_medio_cliente = total_valor / total_clientes if total_clientes > 0 else 0
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="color: white; margin: 0;">📊 Valor Médio/Cliente</h3>
        <h2 style="color: #ffd700; margin: 0;">R$ {valor_medio_cliente:,.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_faturas = len(df_filtrado)
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="color: white; margin: 0;">📄 Total de Faturas</h3>
        <h2 style="color: #ffd700; margin: 0;">{total_faturas:,}</h2>
    </div>
    """, unsafe_allow_html=True)

# --- ABAS DE ANÁLISE ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Distribuição por Aging", 
    "🏢 Análise por Porte", 
    "📈 Evolução Temporal",
    "👥 Top Clientes",
    "⚠️ Inadimplência"
])

with tab1:
    st.markdown("### 📊 Distribuição de Valores por Faixas de Aging")
    
    # Gráfico de barras horizontal - Valor por intervalo de aging
    aging_valores = df_filtrado.groupby('Categoria_Aging')['Valor'].sum().sort_values(ascending=True)
    
    fig_aging_bar = go.Figure(go.Bar(
        x=aging_valores.values,
        y=aging_valores.index,
        orientation='h',
        marker_color=['#ff4757', '#ff6b35', '#ffa502', '#2ed573', '#3742fa'][0:len(aging_valores)],
        text=[f'R$ {val:,.0f}' for val in aging_valores.values],
        textposition='outside',
        textfont=dict(color='white', size=12, family="Arial Black")
    ))
    
    fig_aging_bar.update_layout(
        title='Valores por Faixas de Aging',
        xaxis_title='Valor (R$)',
        yaxis_title='Intervalos de Vencimento',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=150, r=100, t=80, b=60)
    )
    
    st.plotly_chart(fig_aging_bar, use_container_width=True)
    
    # Gráfico de pizza - Distribuição percentual
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pie_aging = px.pie(
            values=aging_valores.values,
            names=aging_valores.index,
            title="Distribuição % por Aging",
            color_discrete_sequence=['#ff4757', '#ff6b35', '#ffa502', '#2ed573', '#3742fa']
        )
        
        fig_pie_aging.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        st.plotly_chart(fig_pie_aging, use_container_width=True)
    
    with col2:
        # Tabela detalhada
        df_aging_summary = df_filtrado.groupby('Categoria_Aging').agg({
            'Valor': ['sum', 'count', 'mean'],
            'Cliente': 'nunique'
        }).round(2)
        
        df_aging_summary.columns = ['Valor Total', 'Qtd Faturas', 'Valor Médio', 'Qtd Clientes']
        df_aging_summary['Valor Total'] = df_aging_summary['Valor Total'].apply(
            lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        )
        df_aging_summary['Valor Médio'] = df_aging_summary['Valor Médio'].apply(
            lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        )
        
        st.markdown("#### 📋 Resumo por Aging")
        st.dataframe(df_aging_summary, use_container_width=True)

with tab2:
    st.markdown("### 🏢 Análise por Porte das Empresas")
    
    # Gráfico de barras - Valor por porte
    porte_valores = df_filtrado.groupby('Porte')['Valor'].sum()
    
    fig_porte = px.bar(
        x=porte_valores.index,
        y=porte_valores.values,
        title="Valores a Receber por Porte",
        color=porte_valores.values,
        color_continuous_scale='Viridis',
        text=[f'R$ {val:,.0f}' for val in porte_valores.values]
    )
    
    fig_porte.update_layout(
        xaxis_title='Porte',
        yaxis_title='Valor (R$)',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False
    )
    
    fig_porte.update_traces(
        textposition='outside',
        textfont=dict(color='white', size=12, family="Arial Black")
    )
    
    st.plotly_chart(fig_porte, use_container_width=True)
    
    # Análise cruzada: Porte vs Aging
    st.markdown("#### 📊 Análise Cruzada: Porte vs Aging")
    
    porte_aging = df_filtrado.groupby(['Porte', 'Categoria_Aging'])['Valor'].sum().reset_index()
    
    fig_heatmap = px.density_heatmap(
        porte_aging,
        x='Categoria_Aging',
        y='Porte',
        z='Valor',
        title="Mapa de Calor: Porte vs Aging",
        color_continuous_scale='RdYlBu_r'
    )
    
    fig_heatmap.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)

with tab3:
    st.markdown("### 📈 Evolução Temporal das Contas a Receber")
    
    # Evolução por data de análise
    evolucao_temporal = df_filtrado.groupby('Datas de análise')['Valor'].sum().reset_index()
    evolucao_temporal = evolucao_temporal.sort_values('Datas de análise')
    
    fig_temporal = px.line(
        evolucao_temporal,
        x='Datas de análise',
        y='Valor',
        title="Evolução do Valor Total a Receber",
        markers=True,
        line_shape='spline'
    )
    
    fig_temporal.update_traces(
        line_color='#ff6b35',
        marker_size=8,
        line_width=3
    )
    
    fig_temporal.update_layout(
        xaxis_title='Data de Análise',
        yaxis_title='Valor Total (R$)',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_temporal, use_container_width=True)
    
    # Evolução por aging ao longo do tempo
    st.markdown("#### 📊 Evolução por Faixas de Aging")
    
    evolucao_aging = df_filtrado.groupby(['Datas de análise', 'Categoria_Aging'])['Valor'].sum().reset_index()
    
    fig_aging_temporal = px.line(
        evolucao_aging,
        x='Datas de análise',
        y='Valor',
        color='Categoria_Aging',
        title="Evolução por Faixas de Aging",
        markers=True
    )
    
    fig_aging_temporal.update_layout(
        xaxis_title='Data de Análise',
        yaxis_title='Valor (R$)',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend_title="Aging"
    )
    
    st.plotly_chart(fig_aging_temporal, use_container_width=True)

with tab4:
    st.markdown("### 👥 Top Clientes Devedores")
    
    # Top 20 clientes por valor
    top_clientes = df_filtrado.groupby('Cliente').agg({
        'Valor': 'sum',
        'Categoria_Aging': lambda x: x.mode().iloc[0] if not x.mode().empty else 'N/A',
        'Porte': lambda x: x.mode().iloc[0] if not x.mode().empty else 'N/A'
    }).sort_values('Valor', ascending=False).head(20)
    
    fig_top_clientes = go.Figure(go.Bar(
        x=top_clientes['Valor'],
        y=top_clientes.index,
        orientation='h',
        marker_color='#3498db',
        text=[f'R$ {val:,.0f}' for val in top_clientes['Valor']],
        textposition='outside',
        textfont=dict(color='white', size=10, family="Arial Black")
    ))
    
    fig_top_clientes.update_layout(
        title='Top 20 Clientes - Maior Valor a Receber',
        xaxis_title='Valor (R$)',
        yaxis_title='Cliente',
        height=800,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=300, r=100, t=80, b=60)
    )
    
    st.plotly_chart(fig_top_clientes, use_container_width=True)
    
    # Tabela detalhada dos top clientes
    st.markdown("#### 📋 Detalhamento dos Top Clientes")
    
    df_top_display = top_clientes.copy()
    df_top_display['Valor'] = df_top_display['Valor'].apply(
        lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    )
    df_top_display.columns = ['Valor a Receber', 'Aging Predominante', 'Porte']
    
    st.dataframe(df_top_display, use_container_width=True)

with tab5:
    st.markdown("### ⚠️ Análise de Inadimplência")
    
    # Definir intervalos críticos (vencidos)
    intervalos_criticos = ['61-180', '181-360', '360+']
    
    df_inadimplencia = df_filtrado[df_filtrado['Categoria_Aging'].isin(intervalos_criticos)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Métricas de inadimplência
        valor_inadimplente = df_inadimplencia['Valor'].sum()
        taxa_inadimplencia = (valor_inadimplente / total_valor * 100) if total_valor > 0 else 0
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;">
            <h3 style="color: white; margin: 0;">⚠️ ALERTA DE INADIMPLÊNCIA</h3>
            <h2 style="color: #ffd700; margin: 10px 0;">R$ {valor_inadimplente:,.2f}</h2>
            <p style="color: white; font-size: 1.2em; margin: 0;">Taxa: {taxa_inadimplencia:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Gráfico de gauge da inadimplência
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = taxa_inadimplencia,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Taxa de Inadimplência (%)"},
            delta = {'reference': 10},  # Meta de 10%
            gauge = {
                'axis': {'range': [None, 50]},
                'bar': {'color': "#ff4757"},
                'steps': [
                    {'range': [0, 10], 'color': "#2ed573"},
                    {'range': [10, 20], 'color': "#ffa502"},
                    {'range': [20, 50], 'color': "#ff4757"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 15
                }
            }
        ))
        
        fig_gauge.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Top clientes inadimplentes
    st.markdown("#### 🚨 Top Clientes Inadimplentes")
    
    top_inadimplentes = df_inadimplencia.groupby('Cliente').agg({
        'Valor': 'sum',
        'Categoria_Aging': lambda x: ', '.join(x.unique())
    }).sort_values('Valor', ascending=False).head(10)
    
    fig_inadimplentes = go.Figure(go.Bar(
        x=top_inadimplentes['Valor'],
        y=top_inadimplentes.index,
        orientation='h',
        marker_color='#ff4757',
        text=[f'R$ {val:,.0f}' for val in top_inadimplentes['Valor']],
        textposition='outside',
        textfont=dict(color='white', size=10, family="Arial Black")
    ))
    
    fig_inadimplentes.update_layout(
        title='Top 10 Clientes Inadimplentes',
        xaxis_title='Valor Inadimplente (R$)',
        yaxis_title='Cliente',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=300, r=100, t=80, b=60)
    )
    
    st.plotly_chart(fig_inadimplentes, use_container_width=True)

# --- BOTÃO DE ATUALIZAÇÃO ---
if st.button("🔄 Atualizar Dados"):
    st.cache_data.clear()
    st.rerun()

# --- FOOTER ---
st.markdown(
    """
    <div style='text-align: center; color: #666666; font-size: 0.9em; margin-top: 2rem;'>
        <div style="background: #1a1a1a; color: white; padding: 5px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; display: inline-block; margin-bottom: 10px;">ALUN</div>
        <br>
        📊 Análise de Aging PM3 | Atualizado automaticamente
    </div>
    """, 
    unsafe_allow_html=True
)
