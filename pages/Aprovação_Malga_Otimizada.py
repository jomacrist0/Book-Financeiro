# -*- coding: utf-8 -*-
"""
Dashboard Otimizado - Malga Payment Approval Analytics
Versão com consulta a banco SQLite local (dados pré-processados pelo Worker)
Performance: Milissegundos ao invés de segundos
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
sys.path.append('..')
from auth import verificar_autenticacao

# --- AUTENTICAÇÃO ---
verificar_autenticacao()
import plotly.express as px
from datetime import datetime, timedelta
import pytz
import time
import sys
import os

# Adiciona o diretório pai ao path para importar módulos customizados
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'worker'))

from worker.config import *
from worker.malga_database import MalgaDatabase

# --- TIMEZONE BRASÍLIA (GMT-3) ---
BRASILIA_TZ = pytz.timezone('America/Sao_Paulo')

# --- CONFIGURAÇÃO DE AUTO-REFRESH ---
AUTO_REFRESH_INTERVAL = 10  # Atualiza a cada 10 segundos

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="[OTIMIZADO] Aprovação Malga",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS DARK THEME (ALUN BRAND) ---
st.markdown("""
<style>
    /* Background e tema geral */
    .stApp {
        background-color: #0e1117;
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 100%;
    }
    
    /* Sidebar com gradiente ALUN */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e2128 0%, #0e1117 100%);
        border-right: 2px solid #30343f;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    /* Logo ALUN na sidebar */
    .alun-logo {
        background-color: #000;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(255,107,53,0.3);
    }
    
    .alun-logo h1 {
        color: white;
        font-size: 2.2em;
        font-weight: bold;
        margin: 0;
        letter-spacing: 2px;
    }
    
    /* Cabeçalho principal */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #ff6b35 0%, #ff8c42 100%);
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(255,107,53,0.4);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5em;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: #f0f0f0;
        font-size: 1.1em;
        margin-top: 10px;
    }
    
    /* Métricas */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #262730 0%, #1e2128 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #30343f;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    div[data-testid="metric-container"] label {
        color: #ff6b35 !important;
        font-weight: 600;
        font-size: 1em;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: white;
        font-size: 2em;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1e2128;
        border-radius: 8px;
        padding: 0.5rem;
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #262730;
        color: white;
        border-radius: 6px;
        padding: 0.8rem 1.5rem;
        font-weight: 500;
        border: 1px solid #30343f;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #ff6b35 !important;
        color: white !important;
        border-color: #ff6b35 !important;
        box-shadow: 0 2px 8px rgba(255,107,53,0.4);
    }
    
    /* Filtros compactos */
    .compact-controls {
        background-color: #1e2128;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 1px solid #30343f;
    }
    
    /* Botões */
    .stButton > button {
        background: linear-gradient(90deg, #ff6b35 0%, #ff8c42 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 2px 6px rgba(255,107,53,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255,107,53,0.5);
    }
    
    /* DataFrames */
    .dataframe {
        border: 1px solid #30343f !important;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .dataframe thead tr th {
        background-color: #ff6b35 !important;
        color: white !important;
        font-weight: 600;
        padding: 12px !important;
    }
    
    .dataframe tbody tr {
        background-color: #1e2128;
        color: white;
    }
    
    .dataframe tbody tr:hover {
        background-color: #262730;
    }
</style>

<script>
// Auto-refresh da dashboard a cada 10 segundos
setTimeout(function() {
    window.location.reload();
}, 10000); // 10000ms = 10 segundos
</script>
""", unsafe_allow_html=True)

# --- ARMAZENA HORÁRIO DO ÚLTIMO REFRESH ---
if 'last_refresh_time' not in st.session_state:
    st.session_state.last_refresh_time = datetime.now(BRASILIA_TZ)
else:
    # Atualiza o horário a cada refresh
    st.session_state.last_refresh_time = datetime.now(BRASILIA_TZ)

# --- SIDEBAR COM LOGO ALUN ---
with st.sidebar:
    st.markdown("""
    <div class="alun-logo">
        <h1>ALUN</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚡ Dashboard Otimizado")
    st.markdown("---")
    
    # Status do Worker
    st.markdown("#### 🔄 Status do Sistema")
    
    db = MalgaDatabase()
    sync_info = db.get_last_sync_info()
    stats = db.get_database_stats()
    
    if sync_info:
        # Converte string para datetime COM timezone
        last_sync_str = sync_info[1]
        
        try:
            if isinstance(last_sync_str, str):
                # Parse com timezone awareness
                last_sync_time = pd.to_datetime(last_sync_str, format='mixed', utc=True)
            else:
                last_sync_time = last_sync_str
            
            # Garante que tem timezone
            if last_sync_time.tzinfo is None:
                last_sync_time = pytz.UTC.localize(last_sync_time)
            
            # Converte ambos para UTC para cálculo preciso
            last_sync_utc = last_sync_time.astimezone(pytz.UTC) if hasattr(last_sync_time, 'astimezone') else last_sync_time
            now_utc = datetime.now(pytz.UTC)
            
            # Calcula diferença em UTC (sem problemas de DST)
            time_diff = now_utc - last_sync_utc
            minutes_ago = max(0, int(time_diff.total_seconds() / 60))  # Evita negativo
            
            # Converte para Brasília só para exibição
            last_sync_brasilia = last_sync_utc.astimezone(BRASILIA_TZ)
            now_brasilia = now_utc.astimezone(BRASILIA_TZ)
            
            # Status baseado no tempo real
            if minutes_ago <= SYNC_INTERVAL_MINUTES:
                st.success(f"✅ Sincronizado há {minutes_ago} min")
            elif minutes_ago <= SYNC_INTERVAL_MINUTES * 3:
                st.warning(f"⚠️ Última sync: {minutes_ago} min atrás")
            else:
                st.error(f"❌ Worker parado! {minutes_ago} min atrás")
                
                # Alerta visual mais forte
                st.markdown("""
                <div style="background-color: #3d1e1e; padding: 12px; border-radius: 8px; 
                     border-left: 4px solid #ff1744; margin-top: 10px; animation: pulse 2s infinite;">
                    <p style="margin: 0; color: #ff1744; font-weight: bold; font-size: 0.9em;">
                        ⚠️ WORKER PARADO!
                    </p>
                    <p style="margin: 5px 0 0 0; color: #ffcdd2; font-size: 0.85em;">
                        Execute: <code style="background: #1e1e1e; padding: 2px 6px; border-radius: 3px;">
                        python run_worker.py</code>
                    </p>
                </div>
                <style>
                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.7; }
                }
                </style>
                """, unsafe_allow_html=True)
            
            # Mostra horários em Brasília
            st.caption(f"🕐 Última: {last_sync_brasilia.strftime('%d/%m/%Y %H:%M:%S')}")
            st.caption(f"⏰ Agora: {now_brasilia.strftime('%d/%m/%Y %H:%M:%S')}")
            st.info(f"📊 {stats['total_transactions']:,} transações")
            
        except Exception as e:
            st.error(f"❌ Erro ao calcular tempo: {str(e)}")
            st.caption(f"Raw: {last_sync_str}")
    else:
        st.error("❌ Worker não inicializado")
    
    st.markdown("---")
    
    # Informações de auto-refresh
    st.markdown("#### ⏱️ Auto-Refresh Dashboard")
    
    # Mostra horário do último refresh com destaque
    last_refresh = st.session_state.get('last_refresh_time', datetime.now(BRASILIA_TZ))
    refresh_time_str = last_refresh.strftime('%H:%M:%S')
    
    # Container com destaque visual
    refresh_html = f"""
    <div style="background-color: #1e3a1e; padding: 10px; border-radius: 5px; border-left: 4px solid #4caf50;">
        <p style="margin: 0; color: #4caf50; font-weight: bold;">🔄 Último Refresh</p>
        <p style="margin: 5px 0 0 0; font-size: 18px; color: white;">{refresh_time_str}</p>
    </div>
    """
    st.markdown(refresh_html, unsafe_allow_html=True)
    
    st.caption(f"⏰ Próximo refresh em: **{AUTO_REFRESH_INTERVAL} segundos**")
    st.caption("🔄 A página recarrega automaticamente")
    
    st.markdown("---")
    
    # Botão de atualização manual
    if st.button("🔄 Atualizar Agora"):
        st.cache_data.clear()
        st.rerun()

# --- CABEÇALHO PRINCIPAL ---
st.markdown("""
<div class="main-header">
    <h1>⚡ Malga Payment Analytics - Otimizado</h1>
    <p>Dashboard de alta performance com dados pré-processados | 🔄 Atualização automática a cada 10s | 🕐 Horário de Brasília (GMT-3)</p>
</div>
""", unsafe_allow_html=True)

# --- FUNÇÕES DE CARREGAMENTO DE DADOS ---

@st.cache_data(ttl=10, show_spinner=False)
def load_metrics_by_period(period='hour', date_from=None, date_to=None):
    """Carrega métricas agregadas do banco"""
    db = MalgaDatabase()
    result = db.get_metrics_by_period(
        period=period,
        start_date=date_from,
        end_date=date_to
    )
    db.close()
    return result

# SEM CACHE para garantir dados sempre frescos
def load_transactions(limit=1000):
    """Carrega transações brutas para análise detalhada - SEM CACHE"""
    db = MalgaDatabase()
    conn = db.connect()
    
    query = """
    SELECT 
        id, created_at, amount, status, payment_method, card_brand,
        description, declined_code, network_denied_reason
    FROM transactions
    ORDER BY created_at DESC
    LIMIT ?
    """
    
    df = pd.read_sql_query(query, conn, params=(limit,))
    
    if not df.empty:
        # Usa format='mixed' e utc=True para lidar com timezones
        df['created_at'] = pd.to_datetime(df['created_at'], format='mixed', utc=True)
        # Remove timezone para simplificar
        df['created_at'] = df['created_at'].dt.tz_localize(None)
    
    db.close()
    return df

# SEM CACHE para garantir dados sempre frescos
def load_transactions_by_period(date_from, date_to):
    """Carrega transações filtradas por período - SEM CACHE"""
    db = MalgaDatabase()
    conn = db.connect()
    
    query = """
    SELECT 
        id, created_at, amount, status, payment_method, card_brand,
        description, declined_code, network_denied_reason
    FROM transactions
    WHERE date(created_at) BETWEEN ? AND ?
    ORDER BY created_at DESC
    """
    
    df = pd.read_sql_query(query, conn, params=(date_from, date_to))
    
    if not df.empty:
        # Usa format='mixed' e utc=True para lidar com timezones
        df['created_at'] = pd.to_datetime(df['created_at'], format='mixed', utc=True)
        # Remove timezone para simplificar
        df['created_at'] = df['created_at'].dt.tz_localize(None)
    
    db.close()
    return df

# --- CONTROLES DE FILTRO ---
st.markdown('<div class="compact-controls">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    # Data inicial (últimas 8 semanas por padrão)
    default_start = datetime.now() - timedelta(weeks=8)
    date_from = st.date_input(
        "📅 Data inicial",
        value=default_start,
        max_value=datetime.now()
    )

with col2:
    # Data final - inclui hoje e ontem como opções
    date_to = st.date_input(
        "📅 Data final",
        value=datetime.now(),
        max_value=datetime.now()
    )

with col3:
    period_options = {
        "Por Minuto": "minute",
        "Por Hora": "hour",
        "Por Dia": "day"
    }
    period_label = st.selectbox(
        "📊 Granularidade",
        options=list(period_options.keys()),
        index=1  # Default: Por Hora
    )
    period = period_options[period_label]

with col4:
    st.markdown("### 🔍")
    show_details = st.checkbox("Mostrar transações", value=False)

st.markdown('</div>', unsafe_allow_html=True)

# --- CARREGA DADOS ---
with st.spinner("⚡ Carregando dados otimizados..."):
    df_metrics = load_metrics_by_period(
        period=period,
        date_from=date_from,
        date_to=date_to
    )

# --- VERIFICA SE HÁ DADOS ---
if df_metrics.empty:
    st.error("❌ Nenhum dado retornado pela query!")
    
    # Debug: mostra info da query
    st.code(f"""
    Período: {period}
    Data Inicial: {date_from}
    Data Final: {date_to}
    """)
    
    # Tenta descobrir qual período tem dados (SEM filtro de data)
    st.info("🔍 Verificando dados disponíveis no banco...")
    db_check = MalgaDatabase()
    df_check = db_check.get_metrics_by_period(period=period)  # SEM filtro
    db_check.close()
    
    st.write(f"Total de registros no banco (sem filtro): {len(df_check)}")
    
    if not df_check.empty:
        date_col = 'date' if period == 'day' else 'timestamp'
        min_date = df_check[date_col].min()
        max_date = df_check[date_col].max()
        
        st.warning(f"⚠️ Nenhum dado encontrado entre **{date_from}** e **{date_to}**.")
        st.success(f"✅ Banco tem {len(df_check)} registros de **{min_date}** até **{max_date}**")
        st.info("� **Ajuste o filtro de datas** para ver os dados ou aguarde o Worker sincronizar dados mais recentes.")
    else:
        # Debug adicional
        from worker.config import DB_PATH
        import os
        
        st.warning("⚠️ Banco está vazio. Aguarde o Worker sincronizar as métricas.")
        st.code(f"Banco: {DB_PATH}")
        st.code(f"Instância: {db_check.db_path}")
        
        if os.path.exists(DB_PATH):
            size_mb = os.path.getsize(DB_PATH) / (1024 * 1024)
            st.info(f"Arquivo existe: {size_mb:.2f} MB")
        else:
            st.error("Arquivo NÃO existe!")
        
        st.info("🔄 O Worker sincroniza a cada 1 minuto.")
    
    # Botão para limpar cache
    if st.button("🔄 Limpar Cache e Recarregar"):
        st.cache_data.clear()
        st.rerun()
    
    st.stop()

# Cria coluna period_start baseada no tipo de agregação
if 'timestamp' in df_metrics.columns:
    df_metrics['period_start'] = pd.to_datetime(df_metrics['timestamp'])
elif 'date' in df_metrics.columns:
    df_metrics['period_start'] = pd.to_datetime(df_metrics['date'])

# --- CÁLCULO DA TAXA DE APROVAÇÃO (NOVA FÓRMULA) ---
# Fórmula: (authorized + canceled) / (authorized + canceled + failed)
total_transactions = df_metrics['total_transactions'].sum()
total_approved = df_metrics['approved_count'].sum()
total_canceled = df_metrics['cancelled_count'].sum()
total_failed = df_metrics['failed_count'].sum()
total_amount = df_metrics['total_amount'].sum()

# Nova fórmula da taxa de aprovação
denominator = total_approved + total_canceled + total_failed
avg_approval_rate = ((total_approved + total_canceled) / denominator * 100) if denominator > 0 else 0

# --- ALERTA CRÍTICO DE TAXA BAIXA ---
ALERT_THRESHOLD = 40.0  # Limite mínimo de 40%

if avg_approval_rate < ALERT_THRESHOLD:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #ff1744 0%, #c62828 100%);
        padding: 25px;
        border-radius: 12px;
        border-left: 8px solid #d50000;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(255,23,68,0.4);
        animation: pulse 2s ease-in-out infinite;
    ">
        <h2 style="color: white; margin: 0 0 15px 0; font-size: 1.8em; text-align: center;">
            🚨 ALERTA CRÍTICO: Taxa de Aprovação Muito Baixa!
        </h2>
        <div style="background: rgba(255,255,255,0.15); padding: 20px; border-radius: 8px; backdrop-filter: blur(10px);">
            <p style="color: white; font-size: 1.5em; margin: 0; text-align: center; font-weight: bold;">
                Taxa Atual: {avg_approval_rate:.1f}%
            </p>
            <p style="color: #ffcdd2; font-size: 1.2em; margin: 10px 0 0 0; text-align: center;">
                Limite Esperado: {ALERT_THRESHOLD}% | Diferença: <strong>-{ALERT_THRESHOLD - avg_approval_rate:.1f} pontos</strong>
            </p>
        </div>
        <div style="margin-top: 20px; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
            <p style="color: white; margin: 0 0 10px 0; font-size: 1.1em; font-weight: bold;">⚠️ Ações Recomendadas:</p>
            <ul style="color: #ffcdd2; margin: 0; padding-left: 20px; line-height: 1.8;">
                <li>Verificar integrações com adquirentes</li>
                <li>Analisar configurações do antifraude</li>
                <li>Revisar logs de erro da plataforma</li>
                <li>Verificar tentativas de fraude aumentadas</li>
            </ul>
        </div>
    </div>
    
    <style>
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); box-shadow: 0 6px 20px rgba(255,23,68,0.4); }}
        50% {{ transform: scale(1.01); box-shadow: 0 8px 30px rgba(255,23,68,0.6); }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- MÉTRICAS GLOBAIS ---
st.markdown("### 📊 Métricas Globais do Período")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "💳 Total de Transações",
        f"{total_transactions:,}",
        help="Quantidade total de transações no período"
    )

with col2:
    st.metric(
        "✅ Aprovadas + Canceladas",
        f"{total_approved + total_canceled:,}",
        help=f"Aprovadas: {total_approved:,} | Canceladas: {total_canceled:,}"
    )

with col3:
    st.metric(
        "❌ Falhadas",
        f"{total_failed:,}",
        help="Transações falhadas/reprovadas (denominador da fórmula)"
    )

with col4:
    # Altera cor do delta se estiver abaixo do threshold
    if avg_approval_rate < ALERT_THRESHOLD:
        delta_value = f"{avg_approval_rate - ALERT_THRESHOLD:.1f}% do limite"
        delta_color = "inverse"
    else:
        delta_value = None
        delta_color = "normal"
    
    st.metric(
        "📈 Taxa de Aprovação",
        f"{avg_approval_rate:.1f}%",
        delta=delta_value,
        delta_color=delta_color,
        help=f"Fórmula: (Aprovadas + Canceladas) / (Aprovadas + Canceladas + Falhadas) × 100\nLimite de alerta: {ALERT_THRESHOLD}%"
    )

with col5:
    amount_formatted = f"R$ {total_amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    st.metric(
        "💰 Volume Total",
        amount_formatted,
        help="Volume financeiro total"
    )

st.markdown("---")

# --- TABS DE ANÁLISE ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Evolução Temporal",
    "💳 Por Método de Pagamento",
    "🏦 Por Bandeira",
    "📊 Análise de Status"
])

# --- TAB 1: EVOLUÇÃO TEMPORAL ---
with tab1:
    st.markdown("### 📈 Evolução da Taxa de Aprovação")
    
    # Gráfico de linha com taxa de aprovação
    fig_evolution = go.Figure()
    
    fig_evolution.add_trace(go.Scatter(
        x=df_metrics['period_start'],
        y=df_metrics['approval_rate'],
        mode='lines+markers',
        name='Taxa de Aprovação',
        line=dict(color='#ff6b35', width=3),
        marker=dict(size=8, color='#ff6b35'),
        hovertemplate='<b>%{x}</b><br>Taxa: %{y:.1f}%<extra></extra>'
    ))
    
    fig_evolution.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis_title='Período',
        yaxis_title='Taxa de Aprovação (%)',
        hovermode='x unified',
        height=450,
        margin=dict(t=30, b=60, l=60, r=30)
    )
    
    st.plotly_chart(fig_evolution, use_container_width=True)
    
    # Gráfico de barras com volume
    st.markdown("### 💰 Volume de Transações")
    
    fig_volume = go.Figure()
    
    fig_volume.add_trace(go.Bar(
        x=df_metrics['period_start'],
        y=df_metrics['total_transactions'],
        name='Transações',
        marker=dict(color='#ff6b35'),
        hovertemplate='<b>%{x}</b><br>Transações: %{y}<extra></extra>'
    ))
    
    fig_volume.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis_title='Período',
        yaxis_title='Quantidade',
        height=400,
        margin=dict(t=30, b=60, l=60, r=30)
    )
    
    st.plotly_chart(fig_volume, use_container_width=True)

# --- TAB 2: POR MÉTODO DE PAGAMENTO ---
with tab2:
    st.markdown("### 💳 Análise por Método de Pagamento")
    
    # Carrega transações do período
    df_transactions_period = load_transactions_by_period(date_from, date_to)
    
    if not df_transactions_period.empty:
        # Define status de aprovação
        df_transactions_period['is_approved'] = df_transactions_period['status'].isin(APPROVED_STATUSES)
        df_transactions_period['is_failed'] = df_transactions_period['status'].isin(FAILED_STATUSES)
        
        # Agrupa por método
        df_by_method = df_transactions_period.groupby('payment_method').agg({
            'id': 'count',
            'is_approved': 'sum',
            'is_failed': 'sum',
            'amount': 'sum'
        }).reset_index()
        
        df_by_method.columns = ['payment_method', 'total_transactions', 'approved_count', 'failed_count', 'total_amount']
        
        df_by_method['approval_rate'] = (
            df_by_method['approved_count'] / df_by_method['total_transactions'] * 100
        ).round(2)
        
        # Ordena por volume
        df_by_method = df_by_method.sort_values('total_transactions', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de pizza
            fig_pie = px.pie(
                df_by_method,
                values='total_transactions',
                names='payment_method',
                title='Distribuição de Transações',
                color_discrete_sequence=px.colors.sequential.Oranges_r
            )
            
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Gráfico de barras com taxa de aprovação
            fig_bar = go.Figure()
            
            fig_bar.add_trace(go.Bar(
                x=df_by_method['payment_method'],
                y=df_by_method['approval_rate'],
                marker=dict(color='#ff6b35'),
                text=df_by_method['approval_rate'].apply(lambda x: f'{x:.1f}%'),
                textposition='outside'
            ))
            
            fig_bar.update_layout(
                title='Taxa de Aprovação por Método',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title='Método',
                yaxis_title='Taxa (%)',
                height=400,
                margin=dict(t=60, b=60, l=60, r=30)
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Tabela detalhada
        st.markdown("#### 📋 Detalhamento")
        
        df_method_display = df_by_method.copy()
        df_method_display['total_amount'] = df_method_display['total_amount'].apply(
            lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        )
        df_method_display.columns = [
            'Método', 'Total Trans.', 'Aprovadas', 'Reprovadas', 'Volume (R$)', 'Taxa (%)'
        ]
        
        st.dataframe(df_method_display, use_container_width=True, hide_index=True)
    else:
        st.info("ℹ️ Sem transações no período selecionado")

# --- TAB 3: POR BANDEIRA ---
with tab3:
    st.markdown("### 🏦 Análise por Bandeira de Cartão")
    
    # Usa transações do período já carregadas
    if not df_transactions_period.empty:
        # Filtra apenas transações com bandeira
        df_with_brand = df_transactions_period[df_transactions_period['card_brand'].notna()].copy()
        
        if not df_with_brand.empty:
            # Define status de aprovação
            df_with_brand['is_approved'] = df_with_brand['status'].isin(APPROVED_STATUSES)
            df_with_brand['is_failed'] = df_with_brand['status'].isin(FAILED_STATUSES)
            
            # Agrupa por bandeira
            df_by_brand = df_with_brand.groupby('card_brand').agg({
                'id': 'count',
                'is_approved': 'sum',
                'is_failed': 'sum',
                'amount': 'sum'
            }).reset_index()
            
            df_by_brand.columns = ['card_brand', 'total_transactions', 'approved_count', 'failed_count', 'total_amount']
            
            df_by_brand['approval_rate'] = (
                df_by_brand['approved_count'] / df_by_brand['total_transactions'] * 100
            ).round(2)
            
            df_by_brand = df_by_brand.sort_values('total_transactions', ascending=False)
            
            # Gráfico de barras horizontais
            fig_brand = go.Figure()
            
            fig_brand.add_trace(go.Bar(
                y=df_by_brand['card_brand'],
                x=df_by_brand['total_transactions'],
                orientation='h',
                marker=dict(color='#ff6b35'),
                text=df_by_brand['approval_rate'].apply(lambda x: f'{x:.1f}%'),
                textposition='inside'
            ))
            
            fig_brand.update_layout(
                title='Volume e Taxa de Aprovação por Bandeira',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title='Transações',
                yaxis_title='Bandeira',
                height=400,
                margin=dict(t=60, b=60, l=120, r=30)
            )
            
            st.plotly_chart(fig_brand, use_container_width=True)
            
            # Tabela
            df_brand_display = df_by_brand.copy()
            df_brand_display['total_amount'] = df_brand_display['total_amount'].apply(
                lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            )
            df_brand_display.columns = [
                'Bandeira', 'Total Trans.', 'Aprovadas', 'Reprovadas', 'Volume (R$)', 'Taxa (%)'
            ]
            
            st.dataframe(df_brand_display, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ Sem dados de bandeira disponíveis no período")
    else:
        st.info("ℹ️ Sem transações no período selecionado")

# --- TAB 4: ANÁLISE DE STATUS ---
with tab4:
    st.markdown("### 📊 Distribuição por Status")
    
    if not df_transactions_period.empty:
        # Agrupa por status
        df_by_status = df_transactions_period.groupby('status').agg({
            'id': 'count',
            'amount': 'sum'
        }).reset_index()
        
        df_by_status.columns = ['status', 'total_transactions', 'total_amount']
        df_by_status = df_by_status.sort_values('total_transactions', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de pizza por status
            fig_status = px.pie(
                df_by_status,
                values='total_transactions',
                names='status',
                title='Transações por Status',
                color_discrete_sequence=px.colors.sequential.Oranges_r
            )
            
            fig_status.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400
            )
            
            st.plotly_chart(fig_status, use_container_width=True)
        
        with col2:
            # Gráfico de barras
            fig_status_bar = go.Figure()
            
            fig_status_bar.add_trace(go.Bar(
                x=df_by_status['status'],
                y=df_by_status['total_transactions'],
                marker=dict(color='#ff6b35')
            ))
            
            fig_status_bar.update_layout(
                title='Volume por Status',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title='Status',
                yaxis_title='Transações',
                height=400,
                margin=dict(t=60, b=60, l=60, r=30)
            )
            
            st.plotly_chart(fig_status_bar, use_container_width=True)
    else:
        st.info("ℹ️ Sem transações no período selecionado")

# --- SEÇÃO DE TRANSAÇÕES DETALHADAS (OPCIONAL) ---
if show_details:
    st.markdown("---")
    st.markdown("### 🔍 Transações Recentes (Últimas 1000)")
    
    with st.spinner("Carregando transações..."):
        df_transactions = load_transactions(limit=1000)
    
    if not df_transactions.empty:
        # Formatação
        df_display = df_transactions.copy()
        
        # created_at já vem como datetime sem timezone das funções de load
        df_display['created_at'] = df_display['created_at'].dt.strftime('%d/%m/%Y %H:%M:%S')
        df_display['amount'] = df_display['amount'].apply(
            lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        )
        
        # Renomeia colunas
        df_display.columns = [
            'ID', 'Data/Hora', 'Valor', 'Status', 'Método', 'Bandeira',
            'Descrição', 'Código Recusa', 'Motivo Recusa'
        ]
        
        st.dataframe(df_display, use_container_width=True, hide_index=True, height=400)
        
        # Botão de download
        csv = df_display.to_csv(index=False, sep=';', encoding='utf-8-sig')
        st.download_button(
            label="📥 Baixar transações (CSV)",
            data=csv,
            file_name=f"malga_transacoes_{date_from}_{date_to}.csv",
            mime="text/csv"
        )

# --- RODAPÉ ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 20px;">
    <p>⚡ Dashboard Otimizado | Dados atualizados a cada {interval} minuto(s)</p>
    <p>💾 Arquitetura: Worker + SQLite + Streamlit</p>
</div>
""".format(interval=SYNC_INTERVAL_MINUTES), unsafe_allow_html=True)
