import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from auth import verificar_autenticacao

# --- AUTENTICAÇÃO ---
verificar_autenticacao()

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="🎯 Planejamento Estratégico",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CUSTOMIZADO COM TEMA PRETO E VERMELHO ---
st.markdown("""
<style>
    /* Layout Principal - Fundo Preto */
    .main > div { background: transparent !important; }
    .main { background-color: #000000 !important; }
    [data-testid="stAppViewContainer"] { background-color: #000000 !important; }
    section[data-testid="stSidebar"] { background-color: #1a1a1a !important; }
    
    /* Textos em Branco para Contraste */
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6,
    .main p, .main span, .main div, .main label { color: #FFFFFF !important; }
    
    /* Cards de Métricas */
    [data-testid="stMetricValue"] { 
        color: #FFFFFF !important; 
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] { 
        color: #FFD700 !important; 
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    [data-testid="stMetricDelta"] { 
        color: #90EE90 !important;
        font-weight: 600 !important;
    }
    
    /* Container de Métricas */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Gráficos */
    .js-plotly-plot { 
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label { color: #FFFFFF !important; }
    
    /* Seções Estratégicas */
    .strategic-section {
        background: linear-gradient(135deg, rgba(255,215,0,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-left: 4px solid #FFD700;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    /* Seções Estratégicas */
    .strategic-section {
        background: linear-gradient(135deg, rgba(139,0,0,0.15) 0%, rgba(255,0,0,0.05) 100%);
        border-left: 4px solid #DC143C;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    .strategic-title {
        color: #DC143C !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 15px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .objetivo-tag {
        background: rgba(220, 20, 60, 0.2);
        border: 1px solid #DC143C;
        color: #FF6B6B;
        padding: 8px 15px;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 15px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: #DC143C; font-size: 3rem; font-weight: 800; margin-bottom: 10px;'>
            🎯 Planejamento Estratégico da Tesouraria 2026
        </h1>
        <p style='color: #FFFFFF; font-size: 1.2rem; opacity: 0.9;'>
            Acompanhamento de Metas e Objetivos Estratégicos
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- FILTROS DE PERÍODO ---
st.markdown("### 📅 Filtros de Acompanhamento")
col_filtro1, col_filtro2, col_filtro3 = st.columns([2, 2, 2])

with col_filtro1:
    ano_selecionado = st.selectbox(
        "Ano",
        options=[2024, 2025, 2026, 2027],
        index=2,  # 2026 como padrão
        key="ano_filtro"
    )

with col_filtro2:
    mes_selecionado = st.selectbox(
        "Mês",
        options=["Todos", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                 "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
        index=0,
        key="mes_filtro"
    )

with col_filtro3:
    trimestre_selecionado = st.selectbox(
        "Trimestre",
        options=["Todos", "Q1", "Q2", "Q3", "Q4"],
        index=0,
        key="trimestre_filtro"
    )

st.markdown("---")

# --- DADOS MOCKADOS (Em produção, buscar de fonte real filtrada por período) ---
# Aqui você integraria com sua fonte de dados real
dados_estrategicos = {
    'eficiencia_tecnica': {
        'equipe': [
            {'nome': 'Ana Silva', 'trilha_livia': 100, 'automacoes': 1},
            {'nome': 'Carlos Santos', 'trilha_livia': 80, 'automacoes': 1},
            {'nome': 'Maria Oliveira', 'trilha_livia': 60, 'automacoes': 0},
            {'nome': 'João Pereira', 'trilha_livia': 90, 'automacoes': 1},
        ],
        'meta_trilha': 100,
        'meta_automacoes': 1
    },
    'ciclo_pagamentos': {
        'pmp_atual': 22,
        'pmp_meta_q1': 20,
        'pmp_meta_q2': 25,
        'pmp_meta_q3': 30,
        'cashback_mensal': [
            {'mes': 'Jan', 'valor': 45000},
            {'mes': 'Fev', 'valor': 52000},
            {'mes': 'Mar', 'valor': 48000},
            {'mes': 'Abr', 'valor': 58000},
            {'mes': 'Mai', 'valor': 62000}
        ],
        'cashback_meta_aumento': 20,  # % de aumento
        'sla_horas': 18.5  # horas médias de primeira resposta
    },
    'acuracidade': {
        'desvio_atual': 0.08,
        'desvio_meta': 0.1,
    },
    'operacional': {
        'fechamentos': 8,
        'fechamentos_total': 8,
        'vans_bancarias': 'Implementado'
    },
    'rentabilidade': {
        'cdi_caixa': 98,
        'cdi_meta': 100,
        'bolecode_status': 'Em Implementação',
        'conversao_caixa_2anos': 87.5
    },
    'prazos': {
        'tickets_caixa': 12,
        'sla_horas_media': 18.5
    }
}

# --- OBJETIVO 1: AUMENTAR EFICIÊNCIA TÉCNICA ---
st.markdown("<div class='strategic-section'>", unsafe_allow_html=True)
st.markdown("<div class='objetivo-tag'>📊 OBJETIVO: Aumentar eficiência técnica da Tesouraria para automações e análise de dados</div>", unsafe_allow_html=True)
st.markdown("<p class='strategic-title'>⚙️ Eficiência Técnica do Time</p>", unsafe_allow_html=True)

# Calcular médias do time
equipe = dados_estrategicos['eficiencia_tecnica']['equipe']
media_trilha = sum([p['trilha_livia'] for p in equipe]) / len(equipe)
total_automacoes = sum([p['automacoes'] for p in equipe])

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="📚 Média - Trilha da Lívia",
        value=f"{media_trilha:.1f}%",
        delta=f"{media_trilha - 100:.1f}% vs Meta (100%)",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="🤖 Total de Automações",
        value=f"{total_automacoes}",
        delta=f"Meta: {len(equipe)} (1/pessoa por trimestre)",
        delta_color="off"
    )

with col3:
    progresso_geral = (media_trilha + (total_automacoes/len(equipe)*100)) / 2
    st.metric(
        label="📊 Progresso Geral",
        value=f"{progresso_geral:.1f}%",
        delta=f"{progresso_geral - 100:.1f}% vs Meta"
    )

# Gráficos de Pizza - Individual por pessoa
st.markdown("**👥 Progresso Individual do Time:**")
col_pizza1, col_pizza2 = st.columns(2)

with col_pizza1:
    # Pizza para Trilha da Lívia
    df_trilha = pd.DataFrame(equipe)
    fig_trilha = go.Figure(data=[go.Pie(
        labels=df_trilha['nome'],
        values=df_trilha['trilha_livia'],
        marker=dict(colors=['#DC143C', '#FF6B6B', '#8B0000', '#CD5C5C']),
        hole=0.4,
        textinfo='label+percent',
        textfont=dict(color='white', size=12)
    )])
    fig_trilha.update_layout(
        title="📚 Trilha da Lívia - % Conclusão por Pessoa",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=350,
        showlegend=True,
        legend=dict(font=dict(color='white'))
    )
    st.plotly_chart(fig_trilha, use_container_width=True)

with col_pizza2:
    # Pizza para Automações
    df_auto = pd.DataFrame(equipe)
    df_auto['status'] = df_auto['automacoes'].apply(lambda x: 'Concluído' if x >= 1 else 'Pendente')
    status_count = df_auto['status'].value_counts()
    
    fig_auto = go.Figure(data=[go.Pie(
        labels=status_count.index,
        values=status_count.values,
        marker=dict(colors=['#DC143C', '#8B0000']),
        hole=0.4,
        textinfo='label+value',
        textfont=dict(color='white', size=14, weight='bold')
    )])
    fig_auto.update_layout(
        title="🤖 Automações - Status do Time",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=350,
        showlegend=True,
        legend=dict(font=dict(color='white'))
    )
    st.plotly_chart(fig_auto, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- OBJETIVO 2: OTIMIZAR CICLO DE PAGAMENTOS ---
st.markdown("<div class='strategic-section'>", unsafe_allow_html=True)
st.markdown("<div class='objetivo-tag'>💳 OBJETIVO: Otimizar ciclo de pagamentos do grupo</div>", unsafe_allow_html=True)
st.markdown("<p class='strategic-title'>💳 Ciclo de Pagamentos</p>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    pmp_atual = dados_estrategicos['ciclo_pagamentos']['pmp_atual']
    pmp_meta = dados_estrategicos['ciclo_pagamentos']['pmp_meta_q1']
    st.metric(
        label="📅 PMP Atual",
        value=f"{pmp_atual} dias",
        delta=f"Meta Q1: {pmp_meta} dias",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="🎯 Meta Q2",
        value=f"{dados_estrategicos['ciclo_pagamentos']['pmp_meta_q2']} dias"
    )

with col3:
    st.metric(
        label="🎯 Meta Q3",
        value=f"{dados_estrategicos['ciclo_pagamentos']['pmp_meta_q3']} dias"
    )

with col4:
    sla_horas = dados_estrategicos['ciclo_pagamentos']['sla_horas']
    st.metric(
        label="⏱️ SLA 1ª Resposta",
        value=f"{sla_horas:.1f}h",
        delta="Meta: 24h",
        delta_color="normal",
        help="Tempo médio de primeira resposta ao cliente interno"
    )

# Gráfico de Cashback
st.markdown("**💰 Evolução do Cashback via Cartão de Crédito:**")
df_cashback = pd.DataFrame(dados_estrategicos['ciclo_pagamentos']['cashback_mensal'])
cashback_inicial = df_cashback['valor'].iloc[0]
cashback_atual = df_cashback['valor'].iloc[-1]
aumento_percentual = ((cashback_atual - cashback_inicial) / cashback_inicial) * 100

col_cb1, col_cb2 = st.columns([2, 1])

with col_cb1:
    fig_cashback = go.Figure()
    fig_cashback.add_trace(go.Bar(
        x=df_cashback['mes'],
        y=df_cashback['valor'],
        marker_color='#DC143C',
        text=[f"R$ {v/1000:.0f}K" for v in df_cashback['valor']],
        textposition='outside',
        textfont=dict(color='white')
    ))
    fig_cashback.update_layout(
        title="Cashback Mensal via Cartão de Crédito",
        yaxis_title="Valor (R$)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=350,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig_cashback, use_container_width=True)

with col_cb2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.metric(
        label="📈 Aumento Acumulado",
        value=f"{aumento_percentual:.1f}%",
        delta=f"Meta: +{dados_estrategicos['ciclo_pagamentos']['cashback_meta_aumento']}%",
        delta_color="normal"
    )
    st.metric(
        label="💵 Cashback Atual",
        value=f"R$ {cashback_atual/1000:.0f}K/mês"
    )

# Gráfico PMP
st.markdown("**📊 Evolução do Prazo Médio de Pagamento:**")
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
pmp_real = [22, 21, 20, None, None, None, None, None, None, None, None, None]
pmp_projetado = [None, None, 20, 22, 25, 28, 30, 30, 30, 30, 30, 30]

fig_pmp = go.Figure()
fig_pmp.add_trace(go.Scatter(
    x=meses[:3], y=pmp_real[:3],
    mode='lines+markers',
    name='PMP Real',
    line=dict(color='#DC143C', width=3),
    marker=dict(size=10)
))
fig_pmp.add_trace(go.Scatter(
    x=meses[2:], y=pmp_projetado[2:],
    mode='lines+markers',
    name='PMP Projetado',
    line=dict(color='#FF6B6B', width=3, dash='dash'),
    marker=dict(size=8)
))
fig_pmp.update_layout(
    title="Evolução do PMP - 2026",
    xaxis_title="Mês",
    yaxis_title="Dias",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    height=350
)
st.plotly_chart(fig_pmp, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- OBJETIVO 3: GARANTIR ACURACIDADE CONTAS A RECEBER ---
st.markdown("<div class='strategic-section'>", unsafe_allow_html=True)
st.markdown("<div class='objetivo-tag'>📊 OBJETIVO: Garantir a acuracidade e integridade das informações de Contas a Receber</div>", unsafe_allow_html=True)
st.markdown("<p class='strategic-title'>📊 Acuracidade Contas a Receber</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    desvio_atual = dados_estrategicos['acuracidade']['desvio_atual']
    desvio_meta = dados_estrategicos['acuracidade']['desvio_meta']
    desvio_status = "✅" if desvio_atual <= desvio_meta else "⚠️"
    st.metric(
        label=f"{desvio_status} Desvio Financeiro vs Contábil",
        value=f"{desvio_atual:.2f}%",
        delta=f"Meta: ≤ {desvio_meta:.1f}%",
        delta_color="inverse"
    )

with col2:
    acuracidade_pct = 100 - desvio_atual
    st.metric(
        label="✨ Acuracidade Geral",
        value=f"{acuracidade_pct:.2f}%",
        delta="+0.15% vs mês anterior",
        delta_color="normal"
    )

# Gráfico de evolução do desvio
df_desvio = pd.DataFrame({
    'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
    'Desvio (%)': [0.12, 0.10, 0.09, 0.08, 0.08]
})
fig_desvio = go.Figure()
fig_desvio.add_trace(go.Bar(
    x=df_desvio['Mês'],
    y=df_desvio['Desvio (%)'],
    marker_color=['#DC143C' if x <= 0.1 else '#8B0000' for x in df_desvio['Desvio (%)']],
    text=[f"{x:.2f}%" for x in df_desvio['Desvio (%)']],
    textposition='outside',
    textfont=dict(color='white')
))
fig_desvio.add_hline(y=0.1, line_dash="dash", line_color="white", annotation_text="Meta: 0.1%")
fig_desvio.update_layout(
    title="Evolução do Desvio 2026",
    yaxis_title="Desvio (%)",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    height=350,
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
)
st.plotly_chart(fig_desvio, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- OBJETIVO 4: AUMENTAR EFICIÊNCIA OPERACIONAL ---
st.markdown("<div class='strategic-section'>", unsafe_allow_html=True)
st.markdown("<div class='objetivo-tag'>⚙️ OBJETIVO: Aumentar a eficiência operacional da Tesouraria para fechamentos</div>", unsafe_allow_html=True)
st.markdown("<p class='strategic-title'>🏭 Eficiência Operacional</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fechamentos = dados_estrategicos['operacional']['fechamentos']
    fechamentos_total = dados_estrategicos['operacional']['fechamentos_total']
    fechamento_status = "✅" if fechamentos == fechamentos_total else "⚠️"
    st.metric(
        label=f"{fechamento_status} Fechamentos Mensais",
        value=f"{fechamentos}/{fechamentos_total}",
        delta="Meta: 8/8 sem atrasos",
        delta_color="off"
    )

with col2:
    vans_status = "✅" if dados_estrategicos['operacional']['vans_bancarias'] == 'Implementado' else "🔄"
    st.metric(
        label=f"{vans_status} Vans Bancárias",
        value=dados_estrategicos['operacional']['vans_bancarias'],
        delta="Status de Implementação",
        delta_color="off"
    )
st.markdown('</div>', unsafe_allow_html=True)

# --- OBJETIVO 5 E 6: RENTABILIDADE E EFICIÊNCIA DE CAIXA ---
st.markdown("<div class='strategic-section'>", unsafe_allow_html=True)
st.markdown("<div class='objetivo-tag'>💰 OBJETIVOS: Rentabilidade e Eficiência de Caixa</div>", unsafe_allow_html=True)
st.markdown("<p class='strategic-title'>💎 Rentabilidade e Gestão de Caixa</p>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    cdi_atual = dados_estrategicos['rentabilidade']['cdi_caixa']
    cdi_meta = dados_estrategicos['rentabilidade']['cdi_meta']
    st.metric(
        label="📈 % CDI do Caixa",
        value=f"{cdi_atual}%",
        delta=f"Meta: {cdi_meta}%",
        delta_color="normal",
        help="Rentabilidade do caixa comparada ao CDI"
    )

with col2:
    st.metric(
        label="🎫 Bolecode",
        value=dados_estrategicos['rentabilidade']['bolecode_status'],
        help="Status da implementação do Bolecode"
    )

with col3:
    conversao = dados_estrategicos['rentabilidade']['conversao_caixa_2anos']
    st.metric(
        label="💵 Conversão em Caixa",
        value=f"{conversao:.1f}%",
        delta="Últimos 2 anos",
        help="% de recebíveis convertidos em caixa nos últimos 2 anos"
    )

with col4:
    # Score simplificado: média entre CDI e Conversão
    score_rentabilidade = (cdi_atual + conversao) / 2
    st.metric(
        label="🏆 Score Geral",
        value=f"{score_rentabilidade:.1f}%",
        delta="+2.3% vs trimestre anterior",
        help="Média ponderada entre rentabilidade CDI e conversão em caixa"
    )

# Gráfico de rentabilidade vs CDI
df_rent = pd.DataFrame({
    'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
    '% CDI': [96.5, 97.2, 97.8, 98.0, 98.5],
    'CDI': [100, 100, 100, 100, 100]
})

fig_rent = go.Figure()
fig_rent.add_trace(go.Scatter(
    x=df_rent['Mês'],
    y=df_rent['% CDI'],
    mode='lines+markers',
    name='Rentabilidade Atual',
    line=dict(color='#DC143C', width=3),
    marker=dict(size=10)
))
fig_rent.add_trace(go.Scatter(
    x=df_rent['Mês'],
    y=df_rent['CDI'],
    mode='lines',
    name='Meta CDI (100%)',
    line=dict(color='white', width=2, dash='dash')
))
fig_rent.update_layout(
    title="Evolução da Rentabilidade vs CDI",
    yaxis_title="% do CDI",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    height=350,
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', range=[95, 101])
)
st.plotly_chart(fig_rent, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- OBJETIVO 7: OTIMIZAR PRAZOS OPERACIONAIS ---
st.markdown("<div class='strategic-section'>", unsafe_allow_html=True)
st.markdown("<div class='objetivo-tag'>⏰ OBJETIVO: Otimizar prazos operacionais e de retorno</div>", unsafe_allow_html=True)
st.markdown("<p class='strategic-title'>⏱️ Gestão de Prazos e Tickets</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    tickets = dados_estrategicos['prazos']['tickets_caixa']
    st.metric(
        label="📋 Tickets na Caixa",
        value=f"{tickets}",
        delta="Meta: Reduzir média",
        delta_color="inverse",
        help="Quantidade média de tickets aguardando processamento"
    )

with col2:
    sla_horas = dados_estrategicos['prazos']['sla_horas_media']
    st.metric(
        label="⏱️ SLA 1ª Resposta",
        value=f"{sla_horas:.1f}h",
        delta="Meta: ≤ 24h",
        delta_color="normal",
        help="Tempo médio de primeira resposta ao cliente"
    )

with col3:
    cumprimento_sla = (24 / sla_horas) * 100 if sla_horas > 0 else 100
    st.metric(
        label="✅ Taxa de Cumprimento",
        value=f"{min(cumprimento_sla, 100):.1f}%",
        help="% de tickets respondidos dentro do SLA de 24h"
    )

# Gráfico de evolução de tickets
df_tickets = pd.DataFrame({
    'Semana': ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'Sem 5'],
    'Tickets': [15, 13, 12, 11, 12],
    'SLA (h)': [22, 20, 18.5, 17, 18.5]
})

fig_tickets = go.Figure()
fig_tickets.add_trace(go.Bar(
    x=df_tickets['Semana'],
    y=df_tickets['Tickets'],
    name='Qtd. Tickets',
    marker_color='#DC143C',
    yaxis='y',
    text=df_tickets['Tickets'],
    textposition='outside'
))
fig_tickets.add_trace(go.Scatter(
    x=df_tickets['Semana'],
    y=df_tickets['SLA (h)'],
    name='SLA Médio (h)',
    line=dict(color='#FF6B6B', width=3),
    marker=dict(size=10),
    yaxis='y2'
))
fig_tickets.update_layout(
    title="Evolução de Tickets e SLA",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    height=350,
    xaxis=dict(showgrid=False),
    yaxis=dict(title='Qtd. Tickets', showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
    yaxis2=dict(title='SLA (horas)', overlaying='y', side='right', showgrid=False),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig_tickets, use_container_width=True)
st.markdown("<div class='strategic-section'>", unsafe_allow_html=True)
st.markdown("<p class='strategic-title'>💳 Ciclo de Pagamentos</p>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📅 PMP Atual",
        value=f"{dados_estrategicos['ciclo_pagamentos']['pmp_atual']} dias",
        delta=f"Meta Q1: {dados_estrategicos['ciclo_pagamentos']['pmp_meta_q1']} dias"
    )

with col2:
    st.metric(
        label="💰 Cashback Cartão",
        value=f"{dados_estrategicos['ciclo_pagamentos']['cashback']}%",
        delta=f"+{dados_estrategicos['ciclo_pagamentos']['cashback'] - 15}% vs anterior"
    )

with col3:
    st.metric(
        label="⏱️ SLA 24h",
        value=f"{dados_estrategicos['ciclo_pagamentos']['sla_24h']}%",
        delta="Meta: 95%"
    )

with col4:
    meta_progress = (dados_estrategicos['ciclo_pagamentos']['cashback'] / 
                     dados_estrategicos['ciclo_pagamentos']['cashback_meta'] * 100)
    st.metric(
        label="🎯 Progresso Cashback",
        value=f"{meta_progress:.0f}%",
        delta=f"{dados_estrategicos['ciclo_pagamentos']['cashback'] - dados_estrategicos['ciclo_pagamentos']['cashback_meta']}% vs Meta"
    )

# Gráfico de evolução PMP
fig_pmp = go.Figure()
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
pmp_real = [22, 21, 20, None, None, None, None, None, None, None, None, None]
pmp_projetado = [None, None, 20, 22, 25, 28, 30, 30, 30, 30, 30, 30]

fig_pmp.add_trace(go.Scatter(
    x=meses[:3], y=pmp_real[:3],
    mode='lines+markers',
    name='PMP Real',
    line=dict(color='#FFD700', width=3),
    marker=dict(size=10)
))
fig_pmp.add_trace(go.Scatter(
    x=meses[2:], y=pmp_projetado[2:],
    mode='lines+markers',
    name='PMP Projetado',
    line=dict(color='#90EE90', width=3, dash='dash'),
    marker=dict(size=8)
))
fig_pmp.update_layout(
    title="Evolução do Prazo Médio de Pagamento (PMP) - 2026",
    xaxis_title="Mês",
    yaxis_title="Dias",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    height=400
)
st.plotly_chart(fig_pmp, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- RESUMO EXECUTIVO ---
st.markdown("---")
st.markdown("<h2 style='text-align: center; color: #DC143C;'>📋 Resumo Executivo - Status Geral</h2>", unsafe_allow_html=True)

# Calcular score geral (média dos principais indicadores)
scores = {
    'Eficiência Técnica': media_trilha,
    'Ciclo Pagamentos (PMP)': min(100, (pmp_meta / pmp_atual) * 100),
    'Acuracidade': 100 - desvio_atual,
    'Rentabilidade (CDI)': cdi_atual,
    'SLA Prazos': min(100, (24 / sla_horas) * 100) if sla_horas > 0 else 100
}

col1, col2 = st.columns([2, 1])

with col1:
    # Gráfico radar
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=list(scores.values()),
        theta=list(scores.keys()),
        fill='toself',
        marker_color='#DC143C',
        line_color='#DC143C',
        opacity=0.7
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(255,255,255,0.3)'),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.3)')
        ),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title="Radar de Performance Estratégica",
        height=500
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col2:
    st.markdown("<div style='padding: 20px;'>", unsafe_allow_html=True)
    score_geral = sum(scores.values()) / len(scores)
    
    st.metric(
        label="🎯 Score Geral",
        value=f"{score_geral:.1f}%",
        delta="+3.2% vs mês anterior"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**🔍 Status por Área:**", unsafe_allow_html=True)
    for area, score in scores.items():
        emoji = "✅" if score >= 90 else "⚠️" if score >= 70 else "🔴"
        st.markdown(f"{emoji} **{area}**: {score:.1f}%")
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px; opacity: 0.7;'>
        <p style='color: #FFFFFF; font-size: 0.9rem;'>
            🎯 Planejamento Estratégico da Tesouraria | Atualizado em: {date}
        </p>
    </div>
""".format(date=datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)

