import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
from datetime import datetime, timedelta
import re
import sys
sys.path.append('..')
from auth import verificar_autenticacao

# --- AUTENTICAÇÃO ---
verificar_autenticacao()

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="🚗 Análise Uber Corporativo",
    page_icon="🚗",
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
    
    /* Alertas customizados */
    .uber-alert {
        background: linear-gradient(135deg, #000000 0%, #434343 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ff6b35;
        margin: 1rem 0;
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
        <div style="color: #ff6b35; font-size: 14px; font-weight: bold;">🚗 Análise Uber Corporativo</div>
    </div>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='text-align: center; color: #fafafa;'>🚗 Análise Uber Corporativo</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0a0a0; font-size: 1.1em;'>Dashboard completo de mobilidade corporativa e gestão de viagens</p>", unsafe_allow_html=True)

# --- FUNÇÃO DE CARREGAMENTO DE DADOS ---
@st.cache_data
def load_uber_data():
    """Carrega e processa os dados do Uber"""
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "Base - Uber.csv"),
        os.path.join(os.getcwd(), "data", "Base - Uber.csv"),
        os.path.join("data", "Base - Uber.csv"),
        os.path.join(os.path.dirname(__file__), "..", "Base - Uber.csv"),
        os.path.join(os.getcwd(), "Base - Uber.csv"),
        "Base - Uber.csv"
    ]
    
    df = None
    separators = [';', ',', '\t']
    
    for path in possible_paths:
        if os.path.exists(path):
            for sep in separators:
                try:
                    df = pd.read_csv(path, sep=sep, encoding='utf-8')
                    if df.shape[1] > 10:  # Se tiver muitas colunas, provavelmente é o separador correto
                        break
                except:
                    try:
                        df = pd.read_csv(path, sep=sep, encoding='latin-1')
                        if df.shape[1] > 10:
                            break
                    except:
                        continue
            if df is not None and df.shape[1] > 10:
                break
    
    if df is None:
        st.error("❌ Arquivo Base - Uber.csv não encontrado!")
        st.stop()
    
    # Limpeza dos dados
    df.columns = df.columns.str.strip()
    
    # Remover linhas vazias
    df = df.dropna(subset=['Data da transação', 'Valor da transação em BRL (com tributos)'])
    
    # Processar datas
    df['Data da transação'] = pd.to_datetime(df['Data da transação'], format='%d/%m/%Y', errors='coerce')
    
    # Processar valores monetários
    valor_col = 'Valor da transação em BRL (com tributos)'
    if df[valor_col].dtype == 'object':
        df[valor_col] = df[valor_col].astype(str).str.replace(',', '.').astype(float)
    
    # Processar distância e duração
    if 'Distância (mi)' in df.columns:
        df['Distância (mi)'] = pd.to_numeric(df['Distância (mi)'], errors='coerce')
        df['Distância (km)'] = df['Distância (mi)'] * 1.60934  # Converter para km
    
    if 'Duração (min)' in df.columns:
        df['Duração (min)'] = pd.to_numeric(df['Duração (min)'], errors='coerce')
    
    # Criar colunas auxiliares
    df['Nome Completo'] = df['Nome'].str.title() + ' ' + df['Sobrenome'].str.title()
    df['Valor por KM'] = np.where(df['Distância (km)'] > 0, df[valor_col] / df['Distância (km)'], 0)
    df['Mês'] = df['Data da transação'].dt.to_period('M')
    df['Dia da Semana'] = df['Data da transação'].dt.day_name()
    df['Hora'] = df['Data da transação'].dt.hour
    
    # Categorizar por tipo de viagem (aeroporto, hotel, etc.)
    df['Tipo de Destino'] = 'Outros'
    df.loc[df['Endereço de destino'].str.contains('Airport|Aeroporto', case=False, na=False), 'Tipo de Destino'] = 'Aeroporto'
    df.loc[df['Endereço de partida'].str.contains('Airport|Aeroporto', case=False, na=False), 'Tipo de Destino'] = 'Aeroporto'
    df.loc[df['Endereço de destino'].str.contains('Hotel', case=False, na=False), 'Tipo de Destino'] = 'Hotel'
    df.loc[df['Endereço de partida'].str.contains('Hotel', case=False, na=False), 'Tipo de Destino'] = 'Hotel'
    
    return df

# --- FUNÇÃO PARA FORMATAR MOEDA ---
def format_currency(value):
    """Formatar valores em moeda brasileira"""
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Carregar dados
df_uber = load_uber_data()

# --- FILTROS ---
st.markdown('<div class="compact-controls">', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    data_min = df_uber['Data da transação'].min()
    data_max = df_uber['Data da transação'].max()
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
    funcionarios_disponiveis = df_uber['Nome Completo'].unique()
    funcionarios_selecionados = st.multiselect(
        "👥 Funcionários",
        options=funcionarios_disponiveis,
        default=funcionarios_disponiveis[:10]  # Primeiros 10 para não sobrecarregar
    )

with col4:
    cidades_disponiveis = df_uber['Cidade'].unique()
    cidades_selecionadas = st.multiselect(
        "🏙️ Cidades",
        options=cidades_disponiveis,
        default=cidades_disponiveis
    )

with col5:
    servicos_disponiveis = df_uber['Serviço'].unique()
    servicos_selecionados = st.multiselect(
        "🚗 Tipos de Serviço",
        options=servicos_disponiveis,
        default=servicos_disponiveis
    )

st.markdown('</div>', unsafe_allow_html=True)

# Aplicar filtros
df_filtrado = df_uber[
    (df_uber['Data da transação'] >= pd.Timestamp(data_inicio)) &
    (df_uber['Data da transação'] <= pd.Timestamp(data_fim)) &
    (df_uber['Nome Completo'].isin(funcionarios_selecionados)) &
    (df_uber['Cidade'].isin(cidades_selecionadas)) &
    (df_uber['Serviço'].isin(servicos_selecionados))
].copy()

if df_filtrado.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros aplicados.")
    st.stop()

# --- MÉTRICAS PRINCIPAIS ---
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_gasto = df_filtrado['Valor da transação em BRL (com tributos)'].sum()
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="color: white; margin: 0;">💰 Total Gasto</h3>
        <h2 style="color: #ffd700; margin: 0;">{format_currency(total_gasto)}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_viagens = len(df_filtrado)
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="color: white; margin: 0;">🚗 Total de Viagens</h3>
        <h2 style="color: #ffd700; margin: 0;">{total_viagens:,}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    distancia_total = df_filtrado['Distância (km)'].sum()
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="color: white; margin: 0;">📏 Distância Total</h3>
        <h2 style="color: #ffd700; margin: 0;">{distancia_total:,.1f} km</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    tempo_total = df_filtrado['Duração (min)'].sum()
    horas_total = tempo_total / 60
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="color: white; margin: 0;">⏱️ Tempo Total</h3>
        <h2 style="color: #ffd700; margin: 0;">{horas_total:,.1f}h</h2>
    </div>
    """, unsafe_allow_html=True)

with col5:
    valor_medio = total_gasto / total_viagens if total_viagens > 0 else 0
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="color: white; margin: 0;">📊 Valor Médio</h3>
        <h2 style="color: #ffd700; margin: 0;">{format_currency(valor_medio)}</h2>
    </div>
    """, unsafe_allow_html=True)

# --- ABAS DE ANÁLISE ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Visão Geral", 
    "👥 Análise por Funcionário", 
    "🏙️ Análise Geográfica",
    "⏰ Análise Temporal",
    "💰 Análise de Custos",
    "🎯 Insights e Otimização"
])

with tab1:
    st.markdown("### 📊 Visão Geral das Viagens Corporativas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de pizza - Distribuição por tipo de serviço
        servicos_valores = df_filtrado.groupby('Serviço')['Valor da transação em BRL (com tributos)'].sum()
        
        fig_servicos = px.pie(
            values=servicos_valores.values,
            names=servicos_valores.index,
            title="Distribuição de Gastos por Tipo de Serviço",
            color_discrete_sequence=['#ff6b35', '#3498db', '#2ecc71', '#e74c3c', '#f39c12']
        )
        
        fig_servicos.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        st.plotly_chart(fig_servicos, use_container_width=True)
    
    with col2:
        # Gráfico de barras - Top cidades por gasto
        cidades_gastos = df_filtrado.groupby('Cidade')['Valor da transação em BRL (com tributos)'].sum().sort_values(ascending=False).head(10)
        
        fig_cidades = go.Figure(go.Bar(
            x=cidades_gastos.values,
            y=cidades_gastos.index,
            orientation='h',
            marker_color='#3498db',
            text=[format_currency(val) for val in cidades_gastos.values],
            textposition='outside',
            textfont=dict(color='white', size=10)
        ))
        
        fig_cidades.update_layout(
            title='Top 10 Cidades por Gasto',
            xaxis_title='Valor (R$)',
            yaxis_title='Cidade',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=100, r=50, t=50, b=50)
        )
        
        st.plotly_chart(fig_cidades, use_container_width=True)
    
    # Tabela resumo
    st.markdown("#### 📋 Resumo por Cidade")
    resumo_cidades = df_filtrado.groupby('Cidade').agg({
        'Valor da transação em BRL (com tributos)': ['sum', 'mean', 'count'],
        'Distância (km)': ['sum', 'mean'],
        'Duração (min)': ['sum', 'mean']
    }).round(2)
    
    resumo_cidades.columns = ['Total Gasto', 'Gasto Médio', 'Qtd Viagens', 'Distância Total (km)', 'Distância Média (km)', 'Tempo Total (min)', 'Tempo Médio (min)']
    
    # Formatar valores monetários
    resumo_cidades['Total Gasto'] = resumo_cidades['Total Gasto'].apply(format_currency)
    resumo_cidades['Gasto Médio'] = resumo_cidades['Gasto Médio'].apply(format_currency)
    
    st.dataframe(resumo_cidades, use_container_width=True)

with tab2:
    st.markdown("### 👥 Análise por Funcionário")
    
    # Ranking de funcionários por gasto
    funcionarios_ranking = df_filtrado.groupby('Nome Completo').agg({
        'Valor da transação em BRL (com tributos)': ['sum', 'count', 'mean'],
        'Distância (km)': 'sum',
        'Duração (min)': 'sum'
    }).round(2)
    
    funcionarios_ranking.columns = ['Total Gasto', 'Qtd Viagens', 'Gasto Médio', 'Distância Total', 'Tempo Total']
    funcionarios_ranking = funcionarios_ranking.sort_values('Total Gasto', ascending=False).head(15)
    
    # Gráfico de barras horizontal - Top funcionários
    fig_funcionarios = go.Figure(go.Bar(
        x=funcionarios_ranking['Total Gasto'],
        y=funcionarios_ranking.index,
        orientation='h',
        marker_color='#ff6b35',
        text=[format_currency(val) for val in funcionarios_ranking['Total Gasto']],
        textposition='outside',
        textfont=dict(color='white', size=10)
    ))
    
    fig_funcionarios.update_layout(
        title='Top 15 Funcionários por Gasto Total',
        xaxis_title='Valor Total (R$)',
        yaxis_title='Funcionário',
        height=600,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=200, r=100, t=80, b=60)
    )
    
    st.plotly_chart(fig_funcionarios, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Scatter plot - Gasto vs Quantidade de viagens
        fig_scatter = px.scatter(
            funcionarios_ranking.reset_index(),
            x='Qtd Viagens',
            y='Total Gasto',
            text='Nome Completo',
            title="Relação: Quantidade vs Valor Total",
            size='Gasto Médio'
        )
        
        fig_scatter.update_traces(
            textposition="top center",
            marker_color='#2ecc71'
        )
        
        fig_scatter.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # Histograma - Distribuição de gastos médios
        fig_hist = px.histogram(
            funcionarios_ranking,
            x='Gasto Médio',
            title="Distribuição de Gastos Médios por Funcionário",
            nbins=20,
            color_discrete_sequence=['#e74c3c']
        )
        
        fig_hist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)

with tab3:
    st.markdown("### 🏙️ Análise Geográfica")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Mapa de calor por cidade e tipo de destino
        mapa_dados = df_filtrado.groupby(['Cidade', 'Tipo de Destino'])['Valor da transação em BRL (com tributos)'].sum().reset_index()
        
        fig_heatmap = px.density_heatmap(
            mapa_dados,
            x='Tipo de Destino',
            y='Cidade',
            z='Valor da transação em BRL (com tributos)',
            title="Mapa de Calor: Cidade vs Tipo de Destino",
            color_continuous_scale='Viridis'
        )
        
        fig_heatmap.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with col2:
        # Gráfico de rosca - Distribuição por tipo de destino
        destinos_valores = df_filtrado.groupby('Tipo de Destino')['Valor da transação em BRL (com tributos)'].sum()
        
        fig_destinos = go.Figure(data=[go.Pie(
            labels=destinos_valores.index,
            values=destinos_valores.values,
            hole=.3,
            marker_colors=['#ff6b35', '#3498db', '#2ecc71']
        )])
        
        fig_destinos.update_layout(
            title="Distribuição por Tipo de Destino",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        st.plotly_chart(fig_destinos, use_container_width=True)
    
    # Análise de eficiência por distância
    st.markdown("#### 📏 Análise de Eficiência por Distância")
    
    # Criar faixas de distância
    df_filtrado['Faixa_Distancia'] = pd.cut(
        df_filtrado['Distância (km)'],
        bins=[0, 5, 10, 20, 50, float('inf')],
        labels=['0-5km', '5-10km', '10-20km', '20-50km', '50km+']
    )
    
    eficiencia_distancia = df_filtrado.groupby('Faixa_Distancia').agg({
        'Valor da transação em BRL (com tributos)': ['sum', 'mean', 'count'],
        'Valor por KM': 'mean'
    }).round(2)
    
    eficiencia_distancia.columns = ['Total Gasto', 'Gasto Médio', 'Qtd Viagens', 'Valor Médio por KM']
    
    fig_eficiencia = px.bar(
        eficiencia_distancia.reset_index(),
        x='Faixa_Distancia',
        y='Valor Médio por KM',
        title="Valor Médio por KM por Faixa de Distância",
        color='Valor Médio por KM',
        color_continuous_scale='RdYlBu_r'
    )
    
    fig_eficiencia.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )
    
    st.plotly_chart(fig_eficiencia, use_container_width=True)

with tab4:
    st.markdown("### ⏰ Análise Temporal")
    
    # Evolução mensal dos gastos
    evolucao_mensal = df_filtrado.groupby('Mês')['Valor da transação em BRL (com tributos)'].sum()
    
    fig_mensal = px.line(
        x=evolucao_mensal.index.astype(str),
        y=evolucao_mensal.values,
        title="Evolução Mensal dos Gastos",
        markers=True
    )
    
    fig_mensal.update_traces(
        line_color='#ff6b35',
        marker_size=8,
        line_width=3
    )
    
    fig_mensal.update_layout(
        xaxis_title='Mês',
        yaxis_title='Valor Total (R$)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )
    
    st.plotly_chart(fig_mensal, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Análise por dia da semana
        dia_semana_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dias_gastos = df_filtrado.groupby('Dia da Semana')['Valor da transação em BRL (com tributos)'].agg(['sum', 'count']).reindex(dia_semana_order)
        
        fig_dias = px.bar(
            x=['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
            y=dias_gastos['sum'].values,
            title="Gastos por Dia da Semana",
            color=dias_gastos['sum'].values,
            color_continuous_scale='Blues'
        )
        
        fig_dias.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)', 
            font=dict(color='white'),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_dias, use_container_width=True)
    
    with col2:
        # Análise por hora do dia (assumindo que temos hora)
        if 'Hora' in df_filtrado.columns:
            horas_gastos = df_filtrado.groupby('Hora')['Valor da transação em BRL (com tributos)'].sum()
            
            fig_horas = px.line(
                x=horas_gastos.index,
                y=horas_gastos.values,
                title="Gastos por Hora do Dia",
                markers=True
            )
            
            fig_horas.update_traces(
                line_color='#2ecc71',
                marker_size=6
            )
            
            fig_horas.update_layout(
                xaxis_title='Hora',
                yaxis_title='Valor Total (R$)',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400
            )
            
            st.plotly_chart(fig_horas, use_container_width=True)

with tab5:
    st.markdown("### 💰 Análise de Custos e Eficiência")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Box plot - Distribuição de valores por tipo de serviço
        fig_box = px.box(
            df_filtrado,
            x='Serviço',
            y='Valor da transação em BRL (com tributos)',
            title="Distribuição de Valores por Tipo de Serviço",
            color='Serviço'
        )
        
        fig_box.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col2:
        # Scatter - Distância vs Valor
        fig_scatter_dist = px.scatter(
            df_filtrado,
            x='Distância (km)',
            y='Valor da transação em BRL (com tributos)',
            color='Serviço',
            title="Relação: Distância vs Valor",
            size='Duração (min)'
        )
        
        fig_scatter_dist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        st.plotly_chart(fig_scatter_dist, use_container_width=True)
    
    # Análise de outliers
    st.markdown("#### 🚨 Detecção de Outliers (Viagens Mais Caras)")
    
    # Calcular percentil 95 para identificar outliers
    percentil_95 = df_filtrado['Valor da transação em BRL (com tributos)'].quantile(0.95)
    outliers = df_filtrado[df_filtrado['Valor da transação em BRL (com tributos)'] > percentil_95].copy()
    
    if len(outliers) > 0:
        st.markdown(f"""
        <div class="uber-alert">
            <strong>⚠️ Identificadas {len(outliers)} viagens com valores acima do percentil 95 ({format_currency(percentil_95)})</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabela de outliers
        outliers_display = outliers[['Nome Completo', 'Cidade', 'Serviço', 'Distância (km)', 'Duração (min)', 'Valor da transação em BRL (com tributos)']].copy()
        outliers_display['Valor da transação em BRL (com tributos)'] = outliers_display['Valor da transação em BRL (com tributos)'].apply(format_currency)
        outliers_display = outliers_display.sort_values('Valor da transação em BRL (com tributos)', ascending=False)
        
        st.dataframe(outliers_display, use_container_width=True, hide_index=True)

with tab6:
    st.markdown("### 🎯 Insights e Oportunidades de Otimização")
    
    # Calcular alguns insights automáticos
    total_funcionarios = df_filtrado['Nome Completo'].nunique()
    gasto_medio_funcionario = total_gasto / total_funcionarios
    viagem_mais_cara = df_filtrado['Valor da transação em BRL (com tributos)'].max()
    cidade_mais_cara = df_filtrado.groupby('Cidade')['Valor da transação em BRL (com tributos)'].mean().idxmax()
    servico_mais_usado = df_filtrado['Serviço'].mode().iloc[0]
    
    # Insights em cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="uber-alert">
            <h4>💡 Insights Principais</h4>
            <ul>
                <li><strong>Gasto médio por funcionário:</strong> {format_currency(gasto_medio_funcionario)}</li>
                <li><strong>Viagem mais cara:</strong> {format_currency(viagem_mais_cara)}</li>
                <li><strong>Cidade com maior custo médio:</strong> {cidade_mais_cara}</li>
                <li><strong>Serviço mais utilizado:</strong> {servico_mais_usado}</li>
                <li><strong>Distância média por viagem:</strong> {df_filtrado['Distância (km)'].mean():.1f} km</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Calcular potencial de economia
        valor_mediano = df_filtrado['Valor da transação em BRL (com tributos)'].median()
        viagens_acima_mediana = df_filtrado[df_filtrado['Valor da transação em BRL (com tributos)'] > valor_mediano]
        economia_potencial = (viagens_acima_mediana['Valor da transação em BRL (com tributos)'] - valor_mediano).sum()
        
        st.markdown(f"""
        <div class="uber-alert">
            <h4>💰 Oportunidades de Economia</h4>
            <ul>
                <li><strong>Valor mediano por viagem:</strong> {format_currency(valor_mediano)}</li>
                <li><strong>Viagens acima da mediana:</strong> {len(viagens_acima_mediana)}</li>
                <li><strong>Economia potencial estimada:</strong> {format_currency(economia_potencial)}</li>
                <li><strong>% de economia:</strong> {(economia_potencial/total_gasto*100):.1f}%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Recomendações baseadas em dados
    st.markdown("#### 📋 Recomendações Estratégicas")
    
    # Top 3 funcionários que mais gastam
    top_gastadores = df_filtrado.groupby('Nome Completo')['Valor da transação em BRL (com tributos)'].sum().nlargest(3)
    
    # Cidade com melhor relação custo-benefício
    cidade_eficiente = df_filtrado.groupby('Cidade')['Valor por KM'].mean().idxmin()
    
    recomendacoes = f"""
    <div style="background: #2c3e50; padding: 20px; border-radius: 10px; border-left: 5px solid #3498db;">
        <h4 style="color: #3498db;">🎯 Ações Recomendadas:</h4>
        <ol style="color: white;">
            <li><strong>Política de Viagens:</strong> Revisar gastos dos top 3 funcionários: {', '.join(top_gastadores.index[:3])}</li>
            <li><strong>Benchmark de Cidades:</strong> {cidade_eficiente} tem o melhor custo por km - usar como referência</li>
            <li><strong>Otimização de Rotas:</strong> {len(df_filtrado[df_filtrado['Distância (km)'] < 3])} viagens curtas (<3km) podem ser substituídas por outros meios</li>
            <li><strong>Negociação:</strong> Concentrar {(df_filtrado['Serviço'].value_counts().iloc[0]/len(df_filtrado)*100):.1f}% das viagens em {servico_mais_usado} permite melhor negociação</li>
            <li><strong>Horário de Pico:</strong> Evitar horários de maior demanda para reduzir custos dinâmicos</li>
        </ol>
    </div>
    """
    
    st.markdown(recomendacoes, unsafe_allow_html=True)
    
    # Gráfico de tendência de economia
    st.markdown("#### 📈 Simulação de Economia por Otimização")
    
    cenarios = ['Atual', 'Otimização Leve (-10%)', 'Otimização Moderada (-20%)', 'Otimização Agressiva (-30%)']
    valores_cenarios = [total_gasto, total_gasto*0.9, total_gasto*0.8, total_gasto*0.7]
    
    fig_cenarios = go.Figure(data=[
        go.Bar(
            x=cenarios,
            y=valores_cenarios,
            marker_color=['#e74c3c', '#f39c12', '#2ecc71', '#27ae60'],
            text=[format_currency(val) for val in valores_cenarios],
            textposition='outside'
        )
    ])
    
    fig_cenarios.update_layout(
        title='Cenários de Otimização de Custos',
        yaxis_title='Valor Total (R$)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )
    
    st.plotly_chart(fig_cenarios, use_container_width=True)

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
        🚗 Análise Uber Corporativo | Gestão Inteligente de Mobilidade
    </div>
    """, 
    unsafe_allow_html=True
)