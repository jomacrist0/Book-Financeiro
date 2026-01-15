"""
POSIÇÃO DE INVESTIMENTOS - Dashboard Streamlit
Versão: 1.0.0 (PRE-RELEASE - NÃO COMMITADO NO GITHUB)

Carrega arquivo de posição de investimentos e exibe análise completa com:
- Composição por Empresa, Tipo, Status
- KPIs detalhados
- Tabela filtrável com cálculos de liquidação
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from parsers import parse_posicao_file, parse_brl, parse_data, parse_dias_cotizacao, parse_dias_liquidacao
from dates import add_business_days, business_days_between, add_calendar_days, FERIADOS_2026_2027, is_business_day
from metrics import calcular_metricas, classificar_posicao

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="💼 Posição de Investimentos",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CUSTOMIZADO ---
st.markdown("""
<style>
    .main { background-color: #0e1117 !important; }
    .main h1, .main h2, .main h3 { color: #fafafa !important; font-weight: 700 !important; }
    .main p, .main span, .main div, .main label { color: #fafafa !important; }
    
    .metric-card {
        background: linear-gradient(135deg, #1f6feb 0%, #238636 100%) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 12px rgba(14, 17, 23, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 💼 Posição de Investimentos")
    st.markdown("---")
    
    source = st.radio("Origem dos dados:", ["📁 Local", "🌐 GitHub"])
    
    if source == "🌐 GitHub":
        github_url = st.text_input(
            "Cole a URL RAW do GitHub:",
            placeholder="https://raw.githubusercontent.com/.../posicao.xlsx"
        )
        if github_url:
            try:
                df = parse_posicao_file(github_url)
                st.success("✅ Arquivo carregado do GitHub!")
            except Exception as e:
                st.error(f"❌ Erro ao carregar: {e}")
                df = None
    else:
        local_file = st.file_uploader("Envie seu arquivo (XLSX/CSV):", type=["xlsx", "csv"])
        if local_file:
            try:
                df = parse_posicao_file(local_file)
                st.success("✅ Arquivo carregado!")
            except Exception as e:
                st.error(f"❌ Erro ao carregar: {e}")
                df = None
        else:
            # Tentar carregar arquivo padrão
            default_path = Path(__file__).parent.parent / "data" / "posicao.xlsx"
            if default_path.exists():
                try:
                    df = parse_posicao_file(str(default_path))
                    st.info("📂 Usando arquivo local padrão")
                except:
                    df = None
            else:
                st.warning("📌 Envie um arquivo ou configure GitHub")
                df = None

# --- MAIN CONTENT ---
if df is not None and not df.empty:
    
    # Calcular métricas
    metricas = calcular_metricas(df)
    
    # --- HEADER ---
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #fafafa; margin-bottom: 0;">💼 Posição de Investimentos</h1>
        <p style="color: #ccc; font-size: 1.1em;">Análise consolidada da carteira</p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- KPIs ---
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "💰 Total Carteira",
            f"R$ {metricas['total_carteira']:,.0f}",
            delta=f"Atualizado em {datetime.now().strftime('%d/%m')}"
        )
    
    with col2:
        st.metric(
            "📌 Total Aplicado",
            f"R$ {metricas['total_aplicado']:,.0f}",
            help="Status != Resgatado e não fechado"
        )
    
    with col3:
        st.metric(
            "⏳ Em Resgate",
            f"R$ {metricas['total_em_resgate']:,.0f}",
            help="Aguardando liquidação"
        )
    
    with col4:
        st.metric(
            "✅ Resgate Liquidado",
            f"R$ {metricas['total_resgate_liquidado']:,.0f}",
            help="Disponível para saque"
        )
    
    with col5:
        st.metric(
            "🔒 Fechado/Indisponível",
            f"R$ {metricas['total_fechado']:,.0f}",
            help="Sem cotação ou resgate"
        )
    
    st.markdown("---")
    
    # --- GRÁFICOS DE COMPOSIÇÃO ---
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.markdown("### Composição por Empresa")
        comp_empresa = df.groupby('Empresa')['Posicao_Numerica'].sum().sort_values(ascending=False)
        fig_empresa = go.Figure(
            data=[go.Pie(labels=comp_empresa.index, values=comp_empresa.values, hole=0.3)]
        )
        fig_empresa.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig_empresa, use_container_width=True)
    
    with col_graf2:
        st.markdown("### Composição por Tipo")
        comp_tipo = df.groupby('Tipo')['Posicao_Numerica'].sum().sort_values(ascending=False)
        fig_tipo = go.Figure(
            data=[go.Pie(labels=comp_tipo.index, values=comp_tipo.values, hole=0.3)]
        )
        fig_tipo.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig_tipo, use_container_width=True)
    
    st.markdown("---")
    
    # --- TABELA DETALHADA ---
    st.markdown("### 📊 Posições Detalhadas")
    
    # Filtros
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        empresas_filter = st.multiselect(
            "Empresa:",
            options=sorted(df['Empresa'].unique()),
            default=sorted(df['Empresa'].unique())
        )
    
    with col_filter2:
        tipos_filter = st.multiselect(
            "Tipo:",
            options=sorted(df['Tipo'].unique()),
            default=sorted(df['Tipo'].unique())
        )
    
    with col_filter3:
        status_filter = st.multiselect(
            "Status:",
            options=sorted(df['Status'].unique()),
            default=sorted(df['Status'].unique())
        )
    
    # Aplicar filtros
    df_filtrado = df[
        (df['Empresa'].isin(empresas_filter)) &
        (df['Tipo'].isin(tipos_filter)) &
        (df['Status'].isin(status_filter))
    ].copy()
    
    # Preparar exibição
    df_exibicao = df_filtrado[[
        'Fundo_Ativo',
        'Empresa',
        'Tipo',
        'Status',
        'Atualizacao',
        'Posicao_Formatada',
        'Posicao_Numerica',
        'Dias_Cotizacao_Display',
        'Dias_Liquidacao_Display',
        'Data_Cotizacao',
        'Data_Disponibilidade',
        'Disponivel_Hoje',
        'Dias_Restantes_Cotizacao',
        'Dias_Uteis_Restantes_Liquidacao',
        'Classificacao_Operacional'
    ]].copy()
    
    df_exibicao.columns = [
        'Fundo/Ativo',
        'Empresa',
        'Tipo',
        'Status',
        'Atualização',
        'Posição (Text)',
        'Posição (R$)',
        'Dias Cotiz.',
        'Dias Liq.',
        'Data Cotização',
        'Data Disponibilidade',
        'Disponível Hoje?',
        'Dias Restantes',
        'Dias Úteis Rest.',
        'Classificação'
    ]
    
    # Exibir tabela
    st.dataframe(
        df_exibicao,
        use_container_width=True,
        height=500,
        hide_index=True
    )
    
    st.markdown("---")
    
    # --- RESUMO POR CLASSIFICAÇÃO ---
    st.markdown("### 📈 Resumo por Classificação Operacional")
    
    resumo_classe = df_filtrado.groupby('Classificacao_Operacional')['Posicao_Numerica'].sum().sort_values(ascending=False)
    
    col_resumo = st.columns(len(resumo_classe))
    for idx, (classe, valor) in enumerate(resumo_classe.items()):
        with col_resumo[idx]:
            st.metric(classe, f"R$ {valor:,.0f}")
    
    # --- DOWNLOAD ---
    st.markdown("---")
    st.markdown("### 📥 Exportar Dados")
    
    csv = df_filtrado.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 Baixar como CSV",
        data=csv,
        file_name=f"posicao_investimentos_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

else:
    st.warning("⚠️ Nenhum arquivo carregado. Configure um arquivo local ou GitHub para começar.")

# --- FOOTER ---
st.markdown("""
---
<div style='text-align: center; color: #666666; font-size: 0.9em; margin-top: 2rem;'>
    <p>💼 Dashboard de Posição de Investimentos | v1.0.0 (PRE-RELEASE)</p>
    <p style="font-size: 0.8em; color: #555;">⚠️ Em desenvolvimento - não publicado no GitHub</p>
</div>
""", unsafe_allow_html=True)
