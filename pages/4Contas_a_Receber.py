import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta
import sys
sys.path.append('..')
from auth import verificar_autenticacao

# --- AUTENTICAÇÃO ---
verificar_autenticacao()

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="📊 Contas a Receber",
    page_icon="📊",
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
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR COM LOGO ALUN ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 15px; margin-bottom: 2rem;">
        <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQwIiB2aWV3Qm94PSIwIDAgMTAwIDQwIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8dGV4dCB4PSI1MCIgeT0iMjUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyNCIgZm9udC13ZWlnaHQ9ImJvbGQiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5BTFVOPC90ZXh0Pgo8L3N2Zz4K" style="width: 120px; height: auto;">
        <div style="color: #ccc; font-size: 12px; margin-top: 10px;">Contas a Receber</div>
    </div>
    """, unsafe_allow_html=True)

# --- TÍTULO DA PÁGINA ---
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #fafafa; font-size: 3rem; margin-bottom: 0.5rem;">📊 Contas a Receber</h1>
    <p style="color: #888; font-size: 1.2rem;">Análise de Aging e Inadimplência</p>
</div>
""", unsafe_allow_html=True)

# --- FUNÇÕES AUXILIARES ---
@st.cache_data
def load_aging_data():
    """Carrega os dados do arquivo 4Aging.csv"""
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "4Aging.csv"),
        os.path.join(os.getcwd(), "data", "4Aging.csv"),
        os.path.join("data", "4Aging.csv"),
        os.path.join(os.path.dirname(__file__), "..", "4Aging.csv"),
        os.path.join(os.getcwd(), "4Aging.csv"),
        "4Aging.csv"
    ]
    
    csv_path = None
    for path in possible_paths:
        if os.path.exists(path):
            csv_path = path
            break
    
    if csv_path is None:
        st.error("❌ Arquivo '4Aging.csv' não encontrado!")
        return None
    
    try:
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
        
        # Verificar se carregou corretamente
        if df.shape[1] == 1:
            df = pd.read_csv(csv_path, sep=',', encoding='utf-8')
        
        # Limpar nomes das colunas
        df.columns = [col.strip() for col in df.columns]
        
        # Converter data de análise
        if 'Data de Análise' in df.columns:
            df['Data de Análise'] = pd.to_datetime(df['Data de Análise'], format='%d/%m/%Y', errors='coerce')
        elif 'data de análise' in df.columns:
            df['data de análise'] = pd.to_datetime(df['data de análise'], format='%d/%m/%Y', errors='coerce')
            df['Data de Análise'] = df['data de análise']
        
        # Converter valor
        if 'Valor' in df.columns:
            df['Valor'] = df['Valor'].astype(str).str.replace('.', '').str.replace(',', '.').astype(float)
        elif 'valor' in df.columns:
            df['valor'] = df['valor'].astype(str).str.replace('.', '').str.replace(',', '.').astype(float)
            df['Valor'] = df['valor']
        
        return df
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar o arquivo: {e}")
        return None

def format_currency(value):
    """Formata valores em moeda brasileira"""
    if pd.isna(value) or value == 0:
        return "R$ 0"
    return f"R$ {value:,.0f}".replace(",", ".")

def format_label_optimized(value):
    """Otimiza labels dos gráficos"""
    if value >= 1_000_000:
        return f"R$ {value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"R$ {value/1_000:.0f}K"
    else:
        return f"R$ {value:.0f}"

# --- CARREGAMENTO DOS DADOS ---
# Botão para recarregar dados
col_reload, col_info = st.columns([1, 3])
with col_reload:
    if st.button("🔄 Atualizar Dados", help="Clique para recarregar os dados do CSV"):
        st.cache_data.clear()
        st.rerun()

with col_info:
    st.info("💡 Clique em 'Atualizar Dados' após modificar o arquivo CSV para ver as mudanças")

df = load_aging_data()

if df is None:
    st.stop()

# Identificar as colunas corretas
coluna_intervalo_vencimento = None
coluna_intervalo = None
for col in df.columns:
    if 'intervalo' in col.lower() and 'vencimento' in col.lower():
        coluna_intervalo_vencimento = col
    elif 'intervalo' in col.lower() and 'vencimento' not in col.lower():
        coluna_intervalo = col

coluna_data_global = None
for col in df.columns:
    if 'data' in col.lower() and ('análise' in col.lower() or 'analise' in col.lower()):
        coluna_data_global = col
        break

if coluna_data_global is None:
    st.error("❌ Coluna de data de análise não encontrada!")
    st.stop()

if coluna_intervalo_vencimento is None:
    st.error("❌ Coluna 'Intervalo (vencimento)' não encontrada!")
    st.stop()

if coluna_intervalo is None:
    st.error("❌ Coluna 'Intervalo' não encontrada!")
    st.stop()

# Converter a coluna de data se necessário
if coluna_data_global and not pd.api.types.is_datetime64_any_dtype(df[coluna_data_global]):
    try:
        df[coluna_data_global] = pd.to_datetime(df[coluna_data_global], format='%d/%m/%Y', errors='coerce')
    except:
        pass

# Definir ordem dos intervalos
ordem_intervalos = ['1-30', '31-60', '61-180', '181-360', '360+']

# --- FILTRO GLOBAL DE DATA ---
st.markdown("## 📅 Filtro Global de Data")

# Obter datas mínima e máxima
data_min = df[coluna_data_global].min()
data_max = df[coluna_data_global].max()

# Filtros de data global
col_data_global1, col_data_global2 = st.columns(2)
with col_data_global1:
    data_inicio_global = st.date_input(
        "Data Início:",
        value=data_min,
        min_value=data_min,
        max_value=data_max,
        key="data_inicio_global"
    )

with col_data_global2:
    data_fim_global = st.date_input(
        "Data Fim:",
        value=data_max,
        min_value=data_min,
        max_value=data_max,
        key="data_fim_global"
    )

# Aplicar filtro global de data
df_original = df.copy()  # Manter cópia original para comparações
df = df[(df[coluna_data_global] >= pd.to_datetime(data_inicio_global)) & 
        (df[coluna_data_global] <= pd.to_datetime(data_fim_global))]


tab1, tab2, tab3, tab4 = st.tabs(["📈 Evolução da Inadimplência", "🎯 Perfil do Aging", "🏢 Análise por Porte", "🔍 Pesquisa de Clientes"])

# --- ABA 1: EVOLUÇÃO DA INADIMPLÊNCIA ---
with tab1:
    st.markdown("### 📈 Evolução da Inadimplência")
    
    # Filtros na parte superior
    col_filtro1, col_filtro2 = st.columns(2)
    
    with col_filtro1:
        # Filtro de porte (pré-selecionado GOV, GE, PME)
        portes_disponiveis = df['Porte'].unique() if 'Porte' in df.columns else []
        portes_disponiveis = [p for p in portes_disponiveis if p != 'B2C']  # Remover B2C
        portes_selecionados = st.multiselect(
            "🏢 Selecione os Portes:",
            options=portes_disponiveis,
            default=[p for p in ['GOV', 'GE', 'PME'] if p in portes_disponiveis],
            key="filtro_porte_aba1"
        )
    
    with col_filtro2:
        # Filtro de intervalo (pré-selecionado inadimplência) - usando Intervalo (vencimento)
        intervalos_disponiveis = sorted(df[coluna_intervalo_vencimento].unique())
        intervalos_selecionados = st.multiselect(
            "📊 Selecione os Intervalos:",
            options=intervalos_disponiveis,
            default=['31-60', '61-180', '181-360', '360+'],
            key="filtro_intervalo_aba1"
        )
    
    # Filtrar dados
    df_filtrado = df.copy()
    if portes_selecionados and 'Porte' in df.columns:
        df_filtrado = df_filtrado[df_filtrado['Porte'].isin(portes_selecionados)]
    if intervalos_selecionados:
        df_filtrado = df_filtrado[df_filtrado[coluna_intervalo_vencimento].isin(intervalos_selecionados)]
    
    if df_filtrado.empty:
        st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
    else:
        # Agrupar por data de análise
        inadimplencia_por_data = df_filtrado.groupby(coluna_data_global)['Valor'].sum().reset_index()
        
        # Calcular variação percentual
        inadimplencia_por_data['Variacao'] = inadimplencia_por_data['Valor'].pct_change() * 100
        
        # Calcular escala dinâmica (margem de 10% acima e abaixo dos valores)
        valor_min = inadimplencia_por_data['Valor'].min()
        valor_max = inadimplencia_por_data['Valor'].max()
        margem = (valor_max - valor_min) * 0.1
        y_min = max(0, valor_min - margem)  # Não deixar negativo
        y_max = valor_max + margem
        
        # Criar gráfico combinado
        fig_inadimplencia = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Barras para valor total
        fig_inadimplencia.add_trace(go.Bar(
            x=inadimplencia_por_data[coluna_data_global],
            y=inadimplencia_por_data['Valor'],
            name='Inadimplência Total',
            marker_color='#3498db',
            text=[format_label_optimized(val) for val in inadimplencia_por_data['Valor']],
            textposition='outside',
            textfont=dict(color='white', family='Arial Black')
        ), secondary_y=False)
        
        # Linha para variação
        fig_inadimplencia.add_trace(go.Scatter(
            x=inadimplencia_por_data[coluna_data_global],
            y=inadimplencia_por_data['Variacao'],
            name='Variação (%)',
            mode='lines+markers+text',
            line=dict(color='orange', width=3),
            text=[f'{v:.1f}%' if not pd.isna(v) else '' for v in inadimplencia_por_data['Variacao']],
            textposition='top center',
            textfont=dict(color='white', family='Arial Black'),
            connectgaps=True
        ), secondary_y=True)
        
        fig_inadimplencia.update_yaxes(title_text='Valor da Inadimplência (R$)', secondary_y=False, range=[y_min, y_max])
        fig_inadimplencia.update_yaxes(title_text='Variação (%)', secondary_y=True)
        fig_inadimplencia.update_layout(
            height=500,
            title='Evolução da Inadimplência ao Longo do Tempo',
            xaxis_title='Data de Análise',
            margin=dict(t=100, b=60, l=100, r=60),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_inadimplencia, use_container_width=True)
    
    # --- TABELA DE COMPARAÇÃO DE INADIMPLÊNCIA ---
    st.markdown("### 📊 Análise Comparativa da Inadimplência")
    
    # Filtros para comparação de datas
    col_comp1, col_comp2, col_comp3 = st.columns(3)
    
    with col_comp1:
        datas_disponiveis_comp = sorted(df_original[coluna_data_global].dropna().unique())
        data_base = st.selectbox(
            "📅 Data Base (mais antiga):",
            options=datas_disponiveis_comp,
            index=max(0, len(datas_disponiveis_comp)-2) if len(datas_disponiveis_comp) > 1 else 0,
            format_func=lambda x: x.strftime('%d/%m/%Y'),
            key="data_base_comp"
        )
    
    with col_comp2:
        data_comparacao = st.selectbox(
            "📅 Data Comparação (mais recente):",
            options=datas_disponiveis_comp,
            index=len(datas_disponiveis_comp)-1,
            format_func=lambda x: x.strftime('%d/%m/%Y'),
            key="data_comp"
        )
    
    with col_comp3:
        portes_comp = st.multiselect(
            "🏢 Portes para Análise:",
            options=df_original['Porte'].unique(),
            default=['GE', 'PME', 'GOV'],
            key="portes_comp"
        )
    
    if data_base and data_comparacao and portes_comp:
        # Dados para as duas datas
        df_base = df_original[(df_original[coluna_data_global] == data_base) & 
                              (df_original['Porte'].isin(portes_comp)) &
                              (df_original[coluna_intervalo_vencimento].isin(['31-60', '61-180', '181-360', '360+']))]
        
        df_comp = df_original[(df_original[coluna_data_global] == data_comparacao) & 
                              (df_original['Porte'].isin(portes_comp)) &
                              (df_original[coluna_intervalo_vencimento].isin(['31-60', '61-180', '181-360', '360+']))]
        
        # Agrupar dados
        resumo_base = df_base.groupby(['Porte', coluna_intervalo_vencimento])['Valor'].sum().reset_index()
        resumo_comp = df_comp.groupby(['Porte', coluna_intervalo_vencimento])['Valor'].sum().reset_index()
        
        # Calcular totais por porte
        total_base = df_base.groupby('Porte')['Valor'].sum().reset_index()
        total_comp = df_comp.groupby('Porte')['Valor'].sum().reset_index()
        
        # Criar tabela comparativa
        tabela_comparativa = []
        
        for porte in portes_comp:
            # Dados por intervalo
            for intervalo in ['31-60', '61-180', '181-360', '360+']:
                valor_base = resumo_base[(resumo_base['Porte'] == porte) & 
                                       (resumo_base[coluna_intervalo_vencimento] == intervalo)]['Valor'].sum()
                valor_comp = resumo_comp[(resumo_comp['Porte'] == porte) & 
                                       (resumo_comp[coluna_intervalo_vencimento] == intervalo)]['Valor'].sum()
                
                # Participação
                total_porte_base = total_base[total_base['Porte'] == porte]['Valor'].sum()
                total_porte_comp = total_comp[total_comp['Porte'] == porte]['Valor'].sum()
                
                part_base = (valor_base / total_porte_base * 100) if total_porte_base > 0 else 0
                part_comp = (valor_comp / total_porte_comp * 100) if total_porte_comp > 0 else 0
                
                # Variação
                variacao = ((valor_comp - valor_base) / valor_base * 100) if valor_base > 0 else 0
                
                tabela_comparativa.append({
                    'Porte': porte,
                    'Intervalo': intervalo,
                    f'Valor ({data_base.strftime("%d/%m/%Y")})': valor_base,
                    f'Valor ({data_comparacao.strftime("%d/%m/%Y")})': valor_comp,
                    'Participação Base': part_base,
                    'Participação Comp': part_comp,
                    'Variação': variacao
                })
            
            # Total por porte
            total_porte_base_val = total_base[total_base['Porte'] == porte]['Valor'].sum()
            total_porte_comp_val = total_comp[total_comp['Porte'] == porte]['Valor'].sum()
            var_total = ((total_porte_comp_val - total_porte_base_val) / total_porte_base_val * 100) if total_porte_base_val > 0 else 0
            
            tabela_comparativa.append({
                'Porte': f'{porte} Total',
                'Intervalo': '',
                f'Valor ({data_base.strftime("%d/%m/%Y")})': total_porte_base_val,
                f'Valor ({data_comparacao.strftime("%d/%m/%Y")})': total_porte_comp_val,
                'Participação Base': 100.0,
                'Participação Comp': 100.0,
                'Variação': var_total
            })
        
        # Total geral
        total_geral_base = df_base['Valor'].sum()
        total_geral_comp = df_comp['Valor'].sum()
        var_geral = ((total_geral_comp - total_geral_base) / total_geral_base * 100) if total_geral_base > 0 else 0
        
        tabela_comparativa.append({
            'Porte': 'Total Geral',
            'Intervalo': '',
            f'Valor ({data_base.strftime("%d/%m/%Y")})': total_geral_base,
            f'Valor ({data_comparacao.strftime("%d/%m/%Y")})': total_geral_comp,
            'Participação Base': 100.0,
            'Participação Comp': 100.0,
            'Variação': var_geral
        })
        
        # Converter para DataFrame e formatar
        df_tabela = pd.DataFrame(tabela_comparativa)
        
        # Formatar valores
        df_tabela_display = df_tabela.copy()
        for col in df_tabela_display.columns:
            if 'Valor' in col:
                df_tabela_display[col] = df_tabela_display[col].apply(format_currency)
            elif 'Participação' in col or 'Variação' in col:
                df_tabela_display[col] = df_tabela_display[col].apply(lambda x: f"{x:.2f}%")
        
        # Aplicar estilo para destacar linhas de totais
        def destacar_totais(row):
            if 'Total' in str(row['Porte']):
                return ['background-color: #1976d2; color: white; font-weight: bold'] * len(row)
            return [''] * len(row)
        
        st.dataframe(
            df_tabela_display.style.apply(destacar_totais, axis=1),
            use_container_width=True
        )

# --- ABA 2: PERFIL DO AGING ---
with tab2:
    st.markdown("### 🎯 Perfil do Aging por Data Específica")
    
    # Filtros na parte superior
    col_filtro3, col_filtro4, col_filtro5 = st.columns(3)
    
    with col_filtro3:
        # Filtro de porte (incluindo B2C)
        portes_disponiveis_aging = df['Porte'].unique() if 'Porte' in df.columns else []
        portes_selecionados_aging = st.multiselect(
            "🏢 Selecione os Portes:",
            options=portes_disponiveis_aging,
            default=[p for p in ['GOV', 'GE', 'PME', 'B2C'] if p in portes_disponiveis_aging],
            key="filtro_porte_aba2"
        )
    
    with col_filtro4:
        # Filtro de data
        datas_disponiveis = sorted(df[coluna_data_global].dropna().unique())
        if datas_disponiveis:
            data_selecionada = st.selectbox(
                "📅 Selecione a Data de Análise:",
                options=datas_disponiveis,
                index=len(datas_disponiveis)-1,  # Última data por padrão
                format_func=lambda x: x.strftime('%d/%m/%Y') if pd.notna(x) else "Data inválida"
            )
        else:
            st.warning("⚠️ Nenhuma data de análise encontrada nos dados.")
            st.stop()
    
    with col_filtro5:
        # Filtro de intervalo (sem seleção inicial)
        intervalos_disponiveis_aging = [i for i in ordem_intervalos if i in df[coluna_intervalo].unique()]
        intervalos_selecionados_aging = st.multiselect(
            "📊 Selecione os Intervalos:",
            options=intervalos_disponiveis_aging,
            default=[],  # Sem seleção inicial
            key="filtro_intervalo_aba2"
        )
    
    # Filtrar dados para a aba de aging
    df_aging_filtrado = df[df[coluna_data_global] == data_selecionada]
    if portes_selecionados_aging and 'Porte' in df.columns:
        df_aging_filtrado = df_aging_filtrado[df_aging_filtrado['Porte'].isin(portes_selecionados_aging)]
    if intervalos_selecionados_aging:
        df_aging_filtrado = df_aging_filtrado[df_aging_filtrado[coluna_intervalo].isin(intervalos_selecionados_aging)]
    
    if df_aging_filtrado.empty:
        st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
    else:
        # Apenas card de Total Aging
        col_data = st.columns([1, 3])[0]  # Usar apenas primeira coluna
        
        with col_data:
            total_aging = df_aging_filtrado['Valor'].sum()
            # Agrupar por intervalo e porte
        if 'Porte' in df_aging_filtrado.columns:
            aging_por_intervalo = df_aging_filtrado.groupby([coluna_intervalo, 'Porte'])['Valor'].sum().reset_index()
            
            # Definir cores em tonalidades de azul
            cores_azul = {
                'GOV': '#1f77b4',    # Azul escuro
                'GE': '#3498db',     # Azul médio
                'PME': '#5dade2',    # Azul claro
                'B2C': '#85c1e9'     # Azul bem claro
            }
            
            # Criar gráfico de barras empilhadas (intervalo no eixo X, porte empilhado)
            fig_aging = px.bar(
                aging_por_intervalo,
                x=coluna_intervalo,
                y='Valor',
                color='Porte',
                title=f'Perfil do Aging por Intervalo - {data_selecionada.strftime("%d/%m/%Y")}',
                labels={'Valor': 'Valor (R$)', coluna_intervalo: 'Intervalo de Dias'},
                color_discrete_map=cores_azul,
                category_orders={coluna_intervalo: ordem_intervalos}
            )
        else:
            # Se não houver coluna Porte, criar gráfico simples
            aging_agrupado = df_aging_filtrado.groupby(coluna_intervalo)['Valor'].sum().reset_index()
            fig_aging = px.bar(
                aging_agrupado,
                x=coluna_intervalo,
                y='Valor',
                title=f'Perfil do Aging - {data_selecionada.strftime("%d/%m/%Y")}',
                labels={'Valor': 'Valor (R$)', coluna_intervalo: 'Intervalo de Dias'},
                color_discrete_sequence=['#3498db'],
                category_orders={coluna_intervalo: ordem_intervalos}
            )
        
        fig_aging.update_layout(
            height=500,
            xaxis_title='Intervalo de Dias',
            yaxis_title='Valor (R$)',
            margin=dict(t=100, b=60, l=100, r=60),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend_title_text='Porte da Empresa' if 'Porte' in df_aging_filtrado.columns else None
        )
        
        # Adicionar labels nos valores
        fig_aging.update_traces(
            texttemplate='%{y:,.0f}',
            textposition='inside',
            textfont=dict(color='white', size=10)
        )
        
        st.plotly_chart(fig_aging, use_container_width=True)
        
        # --- GRÁFICO DE ÁREA - PARTICIPAÇÃO POR INTERVALO ---
        st.markdown("##### 📊 Participação dos Intervalos ao Longo do Tempo")
        
        # Calcular participação por intervalo e data (usando os filtros aplicados)
        df_part_para_area = df.copy()
        if portes_selecionados_aging and 'Porte' in df.columns:
            df_part_para_area = df_part_para_area[df_part_para_area['Porte'].isin(portes_selecionados_aging)]
        
        participacao_data = df_part_para_area.groupby([coluna_data_global, coluna_intervalo])['Valor'].sum().reset_index()
        
        # Calcular total por data
        total_por_data = participacao_data.groupby(coluna_data_global)['Valor'].sum().reset_index()
        total_por_data.columns = [coluna_data_global, 'Total']
        
        # Juntar para calcular percentual
        participacao_data = participacao_data.merge(total_por_data, on=coluna_data_global)
        participacao_data['Percentual'] = (participacao_data['Valor'] / participacao_data['Total']) * 100
        
        # Criar gráfico de área
        fig_area = px.area(
            participacao_data,
            x=coluna_data_global,
            y='Percentual',
            color=coluna_intervalo,
            title='Evolução da Participação dos Intervalos no Aging (%)',
            labels={'Percentual': 'Participação (%)', coluna_data_global: 'Data de Análise'},
            category_orders={coluna_intervalo: ordem_intervalos}
        )
        
        fig_area.update_layout(
            height=400,
            xaxis_title='Data de Análise',
            yaxis_title='Participação (%)',
            margin=dict(t=80, b=60, l=100, r=60),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend_title_text='Intervalo de Dias'
        )
        
        # Melhorar rótulos de dados - mais visíveis
        fig_area.update_traces(
            texttemplate='%{y:.1f}%',
            textposition='middle center',
            textfont=dict(color='white', size=10, family="Arial Black"),
            mode='lines+text'
        )
        
        st.plotly_chart(fig_area, use_container_width=True)
        
        # Tabela detalhada do aging
        st.markdown("##### 📊 Detalhamento do Aging")
        
        if 'Porte' in df_aging_filtrado.columns:
            # Criar tabela pivot (intervalo como índice, porte como colunas)
            tabela_aging = aging_por_intervalo.pivot(index=coluna_intervalo, columns='Porte', values='Valor').fillna(0)
            # Reordenar índice conforme ordem_intervalos
            tabela_aging = tabela_aging.reindex([i for i in ordem_intervalos if i in tabela_aging.index])
        else:
            # Criar tabela simples
            aging_agrupado = aging_agrupado.set_index(coluna_intervalo)
            tabela_aging = aging_agrupado.reindex([i for i in ordem_intervalos if i in aging_agrupado.index])
        
        # Adicionar coluna de total
        if len(tabela_aging.shape) == 2:  # Se é uma tabela 2D
            tabela_aging['Total'] = tabela_aging.sum(axis=1)
        
        # Formatar valores
        for col in tabela_aging.columns:
            tabela_aging[col] = tabela_aging[col].apply(format_currency)
        
        st.dataframe(tabela_aging, use_container_width=True)

# --- ABA 3: ANÁLISE POR PORTE ---
with tab3:
    st.markdown("### 🏢 Análise de Inadimplência por Porte")
    
    # Filtros na parte superior
    col_filtro8, col_filtro9 = st.columns(2)
    
    with col_filtro8:
        # Filtro de porte com pré-seleção específica
        portes_disponiveis_porte = df['Porte'].unique() if 'Porte' in df.columns else []
        # Pré-selecionar apenas PME, GE e GOV
        portes_default = []
        for porte in ['PME', 'GE', 'GOV']:
            if porte in portes_disponiveis_porte:
                portes_default.append(porte)
        
        portes_selecionados_porte = st.multiselect(
            "🏢 Selecione os Portes:",
            options=portes_disponiveis_porte,
            default=portes_default,
            key="filtro_porte_aba4"
        )
    
    with col_filtro9:
        # Filtro de intervalo (inadimplência)
        intervalos_disponiveis_porte = sorted(df[coluna_intervalo_vencimento].unique())
        intervalos_selecionados_porte = st.multiselect(
            "📊 Selecione os Intervalos:",
            options=intervalos_disponiveis_porte,
            default=['31-60', '61-180', '181-360', '360+'],
            key="filtro_intervalo_aba4"
        )
    
    # Filtrar dados
    df_porte_filtrado = df.copy()
    if portes_selecionados_porte and 'Porte' in df.columns:
        df_porte_filtrado = df_porte_filtrado[df_porte_filtrado['Porte'].isin(portes_selecionados_porte)]
    if intervalos_selecionados_porte:
        df_porte_filtrado = df_porte_filtrado[df_porte_filtrado[coluna_intervalo_vencimento].isin(intervalos_selecionados_porte)]
    
    if df_porte_filtrado.empty:
        st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
    else:
        # Agrupar por data de análise - valor e contagem distinta de clientes
        if 'Cliente' in df_porte_filtrado.columns:
            porte_por_data = df_porte_filtrado.groupby(coluna_data_global).agg({
                'Valor': 'sum',
                'Cliente': 'nunique'
            }).reset_index()
            porte_por_data.columns = [coluna_data_global, 'Valor', 'Qtd_Clientes']
        else:
            porte_por_data = df_porte_filtrado.groupby(coluna_data_global)['Valor'].sum().reset_index()
            porte_por_data['Qtd_Clientes'] = df_porte_filtrado.groupby(coluna_data_global).size().values
        
        # Calcular escala dinâmica melhorada para o valor
        valor_min = porte_por_data['Valor'].min()
        valor_max = porte_por_data['Valor'].max()
        
        # Usar uma margem menor (5%) e garantir que não comece do zero
        margem = (valor_max - valor_min) * 0.05
        y_min = valor_min - margem
        y_max = valor_max + margem
        
        # Se a diferença for muito pequena, usar uma margem fixa
        if (valor_max - valor_min) < valor_max * 0.1:
            media_valor = (valor_min + valor_max) / 2
            y_min = media_valor * 0.9
            y_max = media_valor * 1.1
        
        # Criar gráfico combinado
        fig_porte = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Barras para valor total
        fig_porte.add_trace(go.Bar(
            x=porte_por_data[coluna_data_global],
            y=porte_por_data['Valor'],
            name='Valor Inadimplência',
            marker_color='#3498db',
            text=[format_label_optimized(val) for val in porte_por_data['Valor']],
            textposition='outside',
            textfont=dict(color='white', family='Arial Black')
        ), secondary_y=False)
        
        # Linha para quantidade de clientes
        fig_porte.add_trace(go.Scatter(
            x=porte_por_data[coluna_data_global],
            y=porte_por_data['Qtd_Clientes'],
            name='Qtd. Clientes',
            mode='lines+markers+text',
            line=dict(color='orange', width=3),
            text=[f'{int(q)}' for q in porte_por_data['Qtd_Clientes']],
            textposition='top center',
            textfont=dict(color='white', family='Arial Black'),
            connectgaps=True
        ), secondary_y=True)
        
        fig_porte.update_yaxes(title_text='Valor da Inadimplência (R$)', secondary_y=False, range=[y_min, y_max])
        fig_porte.update_yaxes(title_text='Quantidade de Clientes', secondary_y=True)
        fig_porte.update_layout(
            height=500,
            title='Evolução da Inadimplência: Valor vs Quantidade de Clientes',
            xaxis_title='Data de Análise',
            margin=dict(t=100, b=60, l=100, r=60),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_porte, use_container_width=True)

# --- ABA 4: PESQUISA DE CLIENTES ---
with tab4:
    st.markdown("### 🔍 Pesquisa de Clientes - Análise de Inadimplência")
    
    # Filtros na parte superior
    col_filtro_cliente1, col_filtro_cliente2, col_filtro_cliente3 = st.columns([2, 3, 1])
    
    with col_filtro_cliente1:
        # Filtro digitável de clientes - corrigir erro de ordenação
        if 'Cliente' in df.columns:
            # Remover valores NaN e converter para string, depois ordenar
            clientes_disponiveis = df['Cliente'].dropna().astype(str).unique()
            clientes_disponiveis = sorted([c for c in clientes_disponiveis if c != 'nan'])
            
            if clientes_disponiveis:
                cliente_selecionado = st.selectbox(
                    "👤 Cliente:",
                    options=['Todos os Clientes'] + clientes_disponiveis,
                    index=0,
                    key="filtro_cliente_pesquisa",
                    help="Selecione um cliente específico ou mantenha 'Todos os Clientes' para ver dados acumulados"
                )
            else:
                st.warning("⚠️ Nenhum cliente válido encontrado nos dados!")
                cliente_selecionado = 'Todos os Clientes'
        else:
            st.error("❌ Coluna 'Cliente' não encontrada nos dados!")
            cliente_selecionado = 'Todos os Clientes'
    
    with col_filtro_cliente2:
        # Filtro de intervalo (pré-selecionado inadimplência) - agora com mais espaço
        intervalos_disponiveis_cliente = sorted(df[coluna_intervalo_vencimento].unique())
        intervalos_selecionados_cliente = st.multiselect(
            "📊 Intervalos de Vencimento:",
            options=intervalos_disponiveis_cliente,
            default=['31-60', '61-180', '181-360', '360+'],
            key="filtro_intervalo_cliente"
        )
    
    with col_filtro_cliente3:
        # Botão de atualizar dados
        if st.button("� Atualizar", key="refresh_cliente"):
            st.cache_data.clear()
            st.rerun()
    
    if intervalos_selecionados_cliente:
        # Filtrar dados pelos intervalos selecionados
        df_cliente_filtrado = df[df[coluna_intervalo_vencimento].isin(intervalos_selecionados_cliente)]
        
        # Se cliente específico selecionado, filtrar por ele
        if cliente_selecionado != 'Todos os Clientes':
            df_cliente_filtrado = df_cliente_filtrado[df_cliente_filtrado['Cliente'].astype(str) == cliente_selecionado]
        
        if df_cliente_filtrado.empty:
            st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
        else:
            # Agrupar dados por granularidade (fixo em semanal)
            df_cliente_filtrado['Data_Parse'] = pd.to_datetime(df_cliente_filtrado[coluna_data_global], format='%d/%m/%Y', errors='coerce')
            
            # Granularidade semanal fixa
            df_cliente_filtrado['Periodo'] = df_cliente_filtrado['Data_Parse'].dt.to_period('W')
            df_cliente_filtrado['Periodo_Label'] = df_cliente_filtrado['Periodo'].dt.strftime('%Y-S%U')
            
            # Agrupar por período
            dados_agrupados = df_cliente_filtrado.groupby('Periodo_Label')['Valor'].sum().reset_index()
            dados_agrupados = dados_agrupados.sort_values('Periodo_Label')
            
            # Calcular variação percentual
            dados_agrupados['Variacao'] = dados_agrupados['Valor'].pct_change() * 100
            
            # Criar gráfico combinado de colunas e linhas (similar ao de fluxo de caixa)
            fig_cliente = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Colunas para valor de inadimplência
            fig_cliente.add_trace(go.Bar(
                x=dados_agrupados['Periodo_Label'],
                y=dados_agrupados['Valor'],
                name='Volume de Inadimplência',
                marker_color='#3498db',
                text=[format_label_optimized(val) for val in dados_agrupados['Valor']],
                textposition='outside',
                textfont=dict(color='white', size=12, family="Arial Black"),
                opacity=0.8
            ), secondary_y=False)
            
            # Linha para variação percentual
            fig_cliente.add_trace(go.Scatter(
                x=dados_agrupados['Periodo_Label'],
                y=dados_agrupados['Variacao'],
                name='Variação (%)',
                mode='lines+markers+text',
                line=dict(color='#ff6b35', width=4),
                marker=dict(size=10, color='#ff6b35', line=dict(width=2, color='white')),
                text=[f'{v:.1f}%' if not pd.isna(v) and v != 0 else '' for v in dados_agrupados['Variacao']],
                textposition='top center',
                textfont=dict(color='white', size=11, family="Arial Black"),
                connectgaps=True
            ), secondary_y=True)
            
            # Configurar eixos
            fig_cliente.update_yaxes(
                title_text='<b>Volume de Inadimplência (R$)</b>', 
                secondary_y=False,
                gridcolor='rgba(128,128,128,0.2)',
                title_font=dict(size=14, color='white')
            )
            fig_cliente.update_yaxes(
                title_text='<b>Variação (%)</b>', 
                secondary_y=True,
                gridcolor='rgba(128,128,128,0.1)',
                title_font=dict(size=14, color='white')
            )
            
            # Layout do gráfico
            titulo_grafico = f'Análise de Inadimplência - {cliente_selecionado}' if cliente_selecionado != 'Todos os Clientes' else 'Análise de Inadimplência - Visão Geral'
            
            fig_cliente.update_layout(
                height=550,
                title=dict(
                    text=f'<b>{titulo_grafico}</b>',
                    font=dict(size=18, color='white'),
                    x=0.5
                ),
                xaxis_title='<b>Período (Semanal)</b>',
                margin=dict(t=100, b=80, l=100, r=100),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(128,128,128,0.2)',
                    title_font=dict(size=14, color='white'),
                    tickfont=dict(size=12, color='white')
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    bgcolor='rgba(0,0,0,0.5)',
                    bordercolor='rgba(255,255,255,0.2)',
                    borderwidth=1
                ),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_cliente, use_container_width=True)
    else:
        st.info("⚠️ Selecione pelo menos um intervalo de vencimento para visualizar os dados.")

# --- FIM DAS ABAS ---

# --- RODAPÉ PERSONALIZADO ---
st.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <p style="color: #888; font-size: 0.9rem; margin: 0;">Desenvolvido por [Seu Nome] - Data Analysis & Visualization</p>
    <p style="color: #888; font-size: 0.8rem; margin: 0;">Fonte dos Dados: Sistema Integrado de Gestão</p>
</div>
""", unsafe_allow_html=True)