# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta

st.set_page_config(
    page_title="ALUN - Dashboard Financeiro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === AUTENTICAÇÃO ===
SENHA_CORRETA = "saldosalun2026"

def verificar_autenticacao():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    
    if not st.session_state.autenticado:
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column;">
            <h1 style="color: #ff6b35; text-align: center;">Acesso Restrito</h1>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown("### Digite a senha para continuar")
            senha = st.text_input("Senha:", type="password")
            
            if st.button("Acessar", use_container_width=True):
                if senha == SENHA_CORRETA:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("Senha incorreta!")
        
        st.stop()

verificar_autenticacao()

# === CSS DINÂMICO (muda com a aba selecionada) ===
def aplicar_css_saldos():
    st.markdown("""
    <style>
        .main > div { background: transparent !important; }
        .main { background-color: #630330 !important; }
        [data-testid="stAppViewContainer"] { background-color: #630330 !important; }
        .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 { 
            color: #fafafa !important; 
            font-weight: 700 !important; 
        }
        .main p, .main span, .main div, .main label { 
            color: #fafafa !important; 
        }
        .main [data-testid="metric-container"] { 
            background: linear-gradient(135deg, #7a0440 0%, #8b0550 100%) !important;
            border: 1px solid #9a0660 !important; 
            color: #fafafa !important; 
            border-radius: 12px !important; 
            padding: 1.5rem !important;
        }
        section[data-testid="stSidebar"] { 
            background-color: #1a1a1a !important; 
        }
        section[data-testid="stSidebar"] * { 
            color: #fafafa !important; 
        }
        /* Estilo das abas */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 5px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 10px 20px;
            color: white !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #7a0440 !important;
        }
    </style>
    """, unsafe_allow_html=True)

def aplicar_css_planejamento():
    st.markdown("""
    <style>
        .main > div { background: transparent !important; }
        .main { background-color: #000000 !important; }
        [data-testid="stAppViewContainer"] { background-color: #000000 !important; }
        .main h1, .main h2, .main h3, .main h4, .main h5, .main h6,
        .main p, .main span, .main div, .main label { color: #FFFFFF !important; }
        
        [data-testid="stMetricValue"] { 
            color: #FFFFFF !important; 
            font-size: 2rem !important;
            font-weight: 700 !important;
        }
        [data-testid="stMetricLabel"] { 
            color: #FFD700 !important; 
            font-weight: 600 !important;
        }
        div[data-testid="metric-container"] {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 2px solid rgba(255, 215, 0, 0.3) !important;
            border-radius: 12px !important;
            padding: 20px !important;
        }
        section[data-testid="stSidebar"] { background-color: #1a1a1a !important; }
        section[data-testid="stSidebar"] * { color: #FFFFFF !important; }
        
        /* Estilo das abas */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 5px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 10px 20px;
            color: white !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #DC143C !important;
        }
        
        .strategic-section {
            background: linear-gradient(135deg, rgba(139,0,0,0.15) 0%, rgba(255,0,0,0.05) 100%);
            border-left: 4px solid #DC143C;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
    </style>
    """, unsafe_allow_html=True)

# === CSS BASE ===
st.markdown("""
<style>
    section[data-testid="stSidebar"] { 
        background-color: #1a1a1a !important; 
    }
    section[data-testid="stSidebar"] * { 
        color: #fafafa !important; 
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(0,0,0,0.3);
        border-radius: 10px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 10px 20px;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #7a0440 !important;
    }
</style>
""", unsafe_allow_html=True)

# === SIDEBAR ===
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 15px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">ALUN</h1>
        <div style="color: #ccc; font-size: 14px; margin-top: 10px;">Dashboard Financeiro</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Botão de atualização
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.success("Cache limpo!")
        st.rerun()

# === NAVEGAÇÃO POR ABAS ===
tab1, tab2 = st.tabs(["💰 Saldos do Ecossistema", "🎯 Planejamento Estratégico"])

# ==========================
# ABA 1: SALDOS DO ECOSSISTEMA
# ==========================
with tab1:
    aplicar_css_saldos()
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #fafafa; font-weight: 700; margin-bottom: 0;">Dashboard de Saldos do Ecossistema</h1>
        <p style="color: #ccc; font-size: 1.1em;">Análise Financeira Integrada do Ecossistema</p>
    </div>
    """, unsafe_allow_html=True)

    # Função para carregar dados
    @st.cache_data
    def load_data():
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "data", "1Saldos - ecossistema.xlsx"),
            os.path.join(os.getcwd(), "data", "1Saldos - ecossistema.xlsx"),
            os.path.join("data", "1Saldos - ecossistema.xlsx"),
        ]
        
        xlsx_path = None
        for path in possible_paths:
            if os.path.exists(path):
                xlsx_path = path
                break
        
        if xlsx_path is None:
            st.error("Arquivo '1Saldos - ecossistema.xlsx' não encontrado em /data")
            return None
        
        try:
            df = pd.read_excel(xlsx_path)
            df.columns = [col.strip().replace('\n', '').replace('\r', '') for col in df.columns]
            
            col_data = next((c for c in df.columns if 'data' in c.lower()), None)
            col_empresa = next((c for c in df.columns if 'empresa' in c.lower()), None)
            col_saldo = next((c for c in df.columns if 'saldo' in c.lower() and 'final' in c.lower()), None)
            
            if not col_data or not col_saldo:
                st.error("Colunas esperadas não encontradas no Excel.")
                return None
            
            if not col_empresa:
                df['Empresa'] = 'Empresa Geral'
                col_empresa = 'Empresa'
            
            df[col_data] = pd.to_datetime(df[col_data], errors='coerce', dayfirst=True)
            
            if df[col_saldo].dtype not in ['int64', 'float64']:
                df[col_saldo] = (
                    df[col_saldo]
                    .astype(str)
                    .str.replace('.', '', regex=False)
                    .str.replace(',', '.', regex=False)
                )
            df[col_saldo] = pd.to_numeric(df[col_saldo], errors='coerce').fillna(0)
            
            df = df.rename(columns={
                col_data: 'Data',
                col_empresa: 'Empresa',
                col_saldo: 'Saldo_Final'
            }).dropna(subset=['Data'])
            
            return df
            
        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {e}")
            return None

    def process_data(df):
        df_empresa_dia = (
            df.groupby(['Empresa', 'Data'], as_index=False)['Saldo_Final']
            .sum()
            .rename(columns={'Saldo_Final': 'Saldo_do_Dia'})
        )
        df_ecossistema = (
            df_empresa_dia.groupby('Data', as_index=False)['Saldo_do_Dia']
            .sum()
        )
        df_ecossistema['Empresa'] = 'Saldo do Ecossistema'
        df_consolidado = pd.concat([df_empresa_dia, df_ecossistema], ignore_index=True)
        return df_consolidado, df_empresa_dia, df_ecossistema

    def agregar_por_granularidade(df, granularidade):
        df_temp = df.copy()
        
        if granularidade == "Semanal":
            df_temp['Periodo'] = df_temp['Data'].dt.to_period('W').apply(lambda x: x.start_time)
            periodo_label = "Semana"
        elif granularidade == "Mensal":
            df_temp['Periodo'] = df_temp['Data'].dt.to_period('M').apply(lambda x: x.start_time)
            periodo_label = "Mês"
        else:
            df_temp['Periodo'] = df_temp['Data']
            periodo_label = "Dia"
        
        df_agrupado = (
            df_temp.sort_values(['Empresa', 'Data'])
            .groupby(['Periodo', 'Empresa'], as_index=False)
            .tail(1)
            [['Periodo', 'Empresa', 'Saldo_do_Dia']]
        )
        
        return df_agrupado, periodo_label

    df = load_data()

    if df is not None:
        result = process_data(df)
        df_consolidado, df_empresa_dia, df_ecossistema = result

        datas_unicas = df_consolidado['Data'].drop_duplicates().sort_values(ascending=False)
        datas_15_mais_recentes = datas_unicas.head(15)
        data_mais_antiga_dos_15 = datas_15_mais_recentes.min()
        data_mais_recente = datas_15_mais_recentes.max()
        data_mais_antiga_disponivel = datas_unicas.min()
        data_mais_recente_disponivel = datas_unicas.max()

        st.markdown('<h4>Configurações do Dashboard</h4>', unsafe_allow_html=True)

        col_config1, col_config2, col_config3, col_config4 = st.columns([2, 2, 2, 2])

        with col_config1:
            st.markdown("**Data Inicial**")
            periodo_inicio = st.date_input(
                "Período inicial",
                value=data_mais_antiga_dos_15.date(),
                min_value=data_mais_antiga_disponivel.date(),
                max_value=data_mais_recente_disponivel.date(),
                key="saldos_data_inicio",
                label_visibility="collapsed"
            )

        with col_config2:
            st.markdown("**Data Final**")
            periodo_fim = st.date_input(
                "Período final",
                value=data_mais_recente_disponivel.date(),
                min_value=data_mais_antiga_disponivel.date(),
                max_value=data_mais_recente_disponivel.date(),
                key="saldos_data_fim",
                label_visibility="collapsed"
            )

        with col_config3:
            st.markdown("**Empresas**")
            empresas_disponveis = df_consolidado['Empresa'].unique().tolist()
            default_empresas = ['Alura']
            empresas_selecionadas = st.multiselect(
                "Selecionar Empresas",
                options=empresas_disponveis,
                default=[emp for emp in default_empresas if emp in empresas_disponveis],
                label_visibility="collapsed",
                key="saldos_empresas"
            )

        with col_config4:
            st.markdown("**Granularidade**")
            granularidade = st.selectbox(
                "Granularidade:",
                options=["Diário", "Semanal", "Mensal"],
                index=0,
                label_visibility="collapsed",
                key="saldos_granularidade"
            )

        st.info(f"Período selecionado: {periodo_inicio.strftime('%d/%m/%Y')} até {periodo_fim.strftime('%d/%m/%Y')}")

        df_filtrado = df_consolidado[
            (df_consolidado['Data'] >= pd.to_datetime(periodo_inicio)) &
            (df_consolidado['Data'] <= pd.to_datetime(periodo_fim)) &
            (df_consolidado['Empresa'].isin(empresas_selecionadas))
        ].copy()

        df_plot, periodo_label = agregar_por_granularidade(df_filtrado, granularidade)

        if not df_plot.empty:
            df_todas_empresas = df_consolidado[
                (df_consolidado['Data'] >= pd.to_datetime(periodo_inicio)) &
                (df_consolidado['Data'] <= pd.to_datetime(periodo_fim))
            ].copy()
            
            df_plot_todas, _ = agregar_por_granularidade(df_todas_empresas, granularidade)
            ultima_data_todas = df_plot_todas['Periodo'].max()
            dados_ultimo_periodo_todas = df_plot_todas[df_plot_todas['Periodo'] == ultima_data_todas]
            
            def buscar_saldo_geral(empresa):
                dados_empresa = dados_ultimo_periodo_todas[dados_ultimo_periodo_todas['Empresa'] == empresa]
                return dados_empresa['Saldo_do_Dia'].iloc[0] if len(dados_empresa) > 0 else 0
            
            saldo_ecossistema = buscar_saldo_geral('Saldo do Ecossistema')
            saldo_alura = buscar_saldo_geral('Alura')
            saldo_fiap = buscar_saldo_geral('FIAP')
            saldo_pm3 = buscar_saldo_geral('PM3')
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Ecossistema", f"R$ {saldo_ecossistema/1_000_000:.1f}M")
            with col2:
                st.metric("Alura", f"R$ {saldo_alura/1_000_000:.1f}M")
            with col3:
                st.metric("FIAP", f"R$ {saldo_fiap/1_000_000:.1f}M")
            with col4:
                st.metric("PM3", f"R$ {saldo_pm3/1_000_000:.1f}M")

        if not df_plot.empty:
            st.markdown(f"### Evolução dos Saldos ({granularidade})")
            
            cores_empresas = {
                'Saldo do Ecossistema': '#ffffff',
                'Alura': '#1a5490',
                'FIAP': '#cc0000',
                'PM3': '#663399',
            }
            
            fig_line = px.line(
                df_plot,
                x='Periodo',
                y='Saldo_do_Dia',
                color='Empresa',
                markers=True,
                color_discrete_map=cores_empresas,
                text=df_plot['Saldo_do_Dia'].apply(lambda x: f"R$ {x/1_000_000:.1f}M")
            )
            
            fig_line.update_layout(
                xaxis_title=periodo_label,
                yaxis_title="Saldo (R$)",
                hovermode='x unified',
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)')
            )
            
            fig_line.update_traces(
                mode='lines+markers+text',
                line=dict(width=3),
                marker=dict(size=8, color='white'),
                textposition="top center",
                textfont=dict(size=10, color='white'),
            )
            
            st.plotly_chart(fig_line, use_container_width=True)
            
            st.markdown("### Dados Consolidados")
            
            df_tabela = df_plot.copy()
            df_tabela['Data'] = df_tabela['Periodo'].dt.strftime('%d/%m/%Y')
            df_tabela['Saldo_Formatado'] = df_tabela['Saldo_do_Dia'].apply(lambda x: f"R$ {x:,.0f}")
            df_tabela = df_tabela.sort_values('Periodo', ascending=False)
            
            st.dataframe(
                df_tabela[['Data', 'Empresa', 'Saldo_Formatado']].rename(columns={
                    'Data': 'Data',
                    'Empresa': 'Empresa',
                    'Saldo_Formatado': 'Saldo (R$)'
                }),
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            csv_data = df_tabela[['Data', 'Empresa', 'Saldo_Formatado']].to_csv(index=False)
            st.download_button(
                label="📥 Baixar dados como CSV",
                data=csv_data,
                file_name=f"saldos_ecossistema_{periodo_inicio}_{periodo_fim}.csv",
                mime="text/csv"
            )
        else:
            st.warning("Nenhum dado encontrado para os filtros selecionados.")

# ==========================
# ABA 2: PLANEJAMENTO ESTRATÉGICO
# ==========================
with tab2:
    aplicar_css_planejamento()
    
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='color: #DC143C; font-size: 2.5rem; font-weight: 800; margin-bottom: 10px;'>
                🎯 Planejamento Estratégico da Tesouraria 2026
            </h1>
            <p style='color: #FFFFFF; font-size: 1.2rem; opacity: 0.9;'>
                Acompanhamento de Metas e Objetivos Estratégicos
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Filtros
    st.markdown("### 📅 Filtros de Acompanhamento")
    col_filtro1, col_filtro2, col_filtro3 = st.columns([2, 2, 2])

    with col_filtro1:
        ano_selecionado = st.selectbox(
            "Ano",
            options=[2024, 2025, 2026, 2027],
            index=2,
            key="plan_ano_filtro"
        )

    with col_filtro2:
        mes_selecionado = st.selectbox(
            "Mês",
            options=["Todos", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                     "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
            index=0,
            key="plan_mes_filtro"
        )

    with col_filtro3:
        trimestre_selecionado = st.selectbox(
            "Trimestre",
            options=["Todos", "Q1", "Q2", "Q3", "Q4"],
            index=0,
            key="plan_trimestre_filtro"
        )

    st.markdown("---")

    # === CARREGAR DADOS REAIS DOS ARQUIVOS ===
    @st.cache_data
    def load_planejamento_data():
        """Carrega dados do planejamento estratégico"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "data", "planejamento_estrategico_2026.xlsx"),
            os.path.join(os.getcwd(), "data", "planejamento_estrategico_2026.xlsx"),
            os.path.join("data", "planejamento_estrategico_2026.xlsx"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    # Ler Excel pulando a primeira linha (formato)
                    df = pd.read_excel(path, skiprows=1)
                    return df
                except Exception as e:
                    st.error(f"Erro ao carregar planejamento: {e}")
                    return None
        
        st.warning("Arquivo planejamento_estrategico_2026.xlsx não encontrado")
        return None

    @st.cache_data
    def load_kpis_historico():
        """Carrega histórico de KPIs"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "data", "kpis_historico_2026.xlsx"),
            os.path.join(os.getcwd(), "data", "kpis_historico_2026.xlsx"),
            os.path.join("data", "kpis_historico_2026.xlsx"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    # Ler Excel pulando a primeira linha (formato)
                    df = pd.read_excel(path, skiprows=1)
                    # Converter valores com vírgula para ponto
                    if 'valor' in df.columns:
                        df['valor'] = df['valor'].astype(str).str.replace(',', '.', regex=False)
                        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
                    if 'meta' in df.columns:
                        df['meta'] = df['meta'].astype(str).str.replace(',', '.', regex=False)
                        df['meta'] = pd.to_numeric(df['meta'], errors='coerce')
                    return df
                except Exception as e:
                    st.error(f"Erro ao carregar histórico: {e}")
                    return None
        
        st.warning("Arquivo kpis_historico_2026.xlsx não encontrado")
        return None

    # Carregar dados
    df_planejamento = load_planejamento_data()
    df_historico = load_kpis_historico()
    
    if df_planejamento is None or df_historico is None:
        st.error("⚠️ Não foi possível carregar os dados. Verifique se os arquivos estão na pasta /data")
        st.stop()
    
    # Processar dados por objetivo
    objetivos_unicos = df_planejamento['objetivo'].unique()
    
    # === MOSTRAR CADA OBJETIVO COM DADOS REAIS ===
    for idx, objetivo in enumerate(objetivos_unicos, 1):
        st.markdown("<div class='strategic-section'>", unsafe_allow_html=True)
        
        # Buscar dados deste objetivo
        df_obj = df_planejamento[df_planejamento['objetivo'] == objetivo]
        
        # Mostrar nome completo do objetivo
        st.markdown(f"#### 🎯 Objetivo {idx}")
        st.markdown(f"**{objetivo}**")
        st.markdown("---")
        
        # Mostrar cada resultado-chave
        for _, row in df_obj.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**📌 {row['resultado_chave']}**")
            
            with col2:
                # Calcular progresso
                try:
                    meta = float(str(row['meta']).replace(',', '.'))
                    valor = float(str(row['valor_atual']).replace(',', '.'))
                    if meta > 0:
                        progresso = (valor / meta) * 100
                    else:
                        progresso = 0
                    
                    # Determinar cor
                    if progresso >= 100:
                        cor = "🟢"
                    elif progresso >= 70:
                        cor = "🟡"
                    else:
                        cor = "🔴"
                    
                    st.metric(
                        label="Atual",
                        value=f"{valor:.2f}".replace('.', ','),
                        delta=f"{progresso:.0f}% da meta"
                    )
                except:
                    st.metric(label="Atual", value=str(row['valor_atual']))
            
            with col3:
                st.metric(label="Meta", value=str(row['meta']))
        
        # Buscar histórico deste objetivo (se houver)
        obj_tipo_map = {
            'Aumentar eficiência técnica': 'eficiencia_tecnica',
            'Otimizar ciclo de pagamentos': 'ciclo_pagamentos',
            'Garantir a acuracidade': 'acuracidade',
            'Aumentar a eficiência operacional': 'operacional',
            'Aumentar rentabilidade': 'rentabilidade',
            'Aumentar a eficiência e previsibilidade': 'eficiencia_caixa',
            'Otimizar prazos': 'prazos'
        }
        
        # Identificar tipo do objetivo
        obj_tipo = None
        for key_word, tipo in obj_tipo_map.items():
            if key_word.lower() in objetivo.lower():
                obj_tipo = tipo
                break
        
        # Se encontrou tipo, mostrar gráfico de evolução
        if obj_tipo and df_historico is not None:
            df_hist_obj = df_historico[df_historico['kpi_tipo'] == obj_tipo]
            
            if not df_hist_obj.empty:
                st.markdown("**📈 Evolução Histórica:**")
                
                # Agrupar por KPI
                for kpi_nome in df_hist_obj['kpi_nome'].unique():
                    df_kpi = df_hist_obj[df_hist_obj['kpi_nome'] == kpi_nome].sort_values(['ano', 'mes'])
                    
                    if len(df_kpi) > 1:  # Só plotar se tiver mais de 1 ponto
                        fig = go.Figure()
                        
                        # Criar label do eixo X
                        df_kpi['periodo_label'] = df_kpi['mes'].astype(str) + '/' + df_kpi['ano'].astype(str)
                        
                        # Linha de valores
                        fig.add_trace(go.Scatter(
                            x=df_kpi['periodo_label'],
                            y=df_kpi['valor'],
                            mode='lines+markers',
                            name='Realizado',
                            line=dict(color='#DC143C', width=3),
                            marker=dict(size=10)
                        ))
                        
                        # Linha de meta
                        fig.add_trace(go.Scatter(
                            x=df_kpi['periodo_label'],
                            y=df_kpi['meta'],
                            mode='lines',
                            name='Meta',
                            line=dict(color='#FFD700', width=2, dash='dash')
                        ))
                        
                        unidade = df_kpi['unidade'].iloc[0] if 'unidade' in df_kpi.columns else ''
                        kpi_label = kpi_nome.replace('_', ' ').title()
                        
                        fig.update_layout(
                            title=f"{kpi_label}",
                            xaxis_title="Período",
                            yaxis_title=f"Valor ({unidade})",
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='white'),
                            height=300,
                            showlegend=True,
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # RESUMO EXECUTIVO
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #DC143C;'>📋 Resumo Executivo - Status Geral</h2>", unsafe_allow_html=True)
    
    # Calcular progresso geral por objetivo
    resumo_objetivos = []
    for objetivo in objetivos_unicos:
        df_obj = df_planejamento[df_planejamento['objetivo'] == objetivo]
        progressos = []
        
        for _, row in df_obj.iterrows():
            try:
                meta = float(str(row['meta']).replace(',', '.'))
                valor = float(str(row['valor_atual']).replace(',', '.'))
                if meta > 0:
                    prog = (valor / meta) * 100
                    progressos.append(min(prog, 150))  # Cap em 150% para não distorcer média
            except:
                pass
        
        if progressos:
            media_prog = sum(progressos) / len(progressos)
            resumo_objetivos.append({
                'objetivo': objetivo[:50] + '...' if len(objetivo) > 50 else objetivo,  # Truncar nome longo
                'progresso': media_prog
            })
    
    if resumo_objetivos:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de barras com progresso por objetivo
            df_resumo = pd.DataFrame(resumo_objetivos)
            
            fig_resumo = go.Figure()
            fig_resumo.add_trace(go.Bar(
                y=df_resumo['objetivo'],
                x=df_resumo['progresso'],
                orientation='h',
                marker=dict(
                    color=df_resumo['progresso'],
                    colorscale=[[0, '#8B0000'], [0.7, '#FFD700'], [1, '#00FF00']],
                    showscale=False
                ),
                text=[f"{p:.0f}%" for p in df_resumo['progresso']],
                textposition='outside',
                textfont=dict(color='white')
            ))
            fig_resumo.add_vline(x=100, line_dash="dash", line_color="white", annotation_text="Meta: 100%")
            fig_resumo.update_layout(
                title="Progresso por Objetivo Estratégico",
                xaxis_title="Progresso (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400,
                xaxis=dict(range=[0, max(df_resumo['progresso'].max(), 100) + 20])
            )
            st.plotly_chart(fig_resumo, use_container_width=True)
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Score geral
            score_geral = df_resumo['progresso'].mean()
            st.metric(
                label="🎯 Score Geral",
                value=f"{score_geral:.1f}%",
                delta=f"{score_geral - 100:.1f}% vs Meta"
            )
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("**📊 Status por Área:**")
            for _, row in df_resumo.iterrows():
                prog = row['progresso']
                if prog >= 100:
                    emoji = "✅"
                    cor = "green"
                elif prog >= 70:
                    emoji = "🟡"
                    cor = "orange"
                else:
                    emoji = "🔴"
                    cor = "red"
                
                st.markdown(f"{emoji} **{prog:.0f}%** - {row['objetivo'][:30]}...")
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
        <div style='text-align: center; padding: 20px; opacity: 0.7;'>
            <p style='color: #FFFFFF; font-size: 0.9rem;'>
                🎯 Planejamento Estratégico da Tesouraria | Atualizado em: {datetime.now().strftime("%d/%m/%Y %H:%M")}
            </p>
        </div>
    """, unsafe_allow_html=True)

# === FOOTER GERAL ===
st.markdown("""
<div style='text-align: center; color: #666666; font-size: 0.9em; margin-top: 2rem;'>
    <div style="background: #1a1a1a; color: white; padding: 5px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; display: inline-block;">ALUN</div>
    <br>Dashboard Financeiro | Atualizado automaticamente
</div>
""", unsafe_allow_html=True)

    with col1:
        st.metric(
            label="📚 Média - Trilha da Lívia",
            value=f"{media_trilha:.1f}%",
            delta=f"{media_trilha - 100:.1f}% vs Meta (100%)"
        )

    with col2:
        st.metric(
            label="🤖 Total de Automações",
            value=f"{total_automacoes}",
            delta=f"Meta: {len(equipe)} (1/pessoa)"
        )

    with col3:
        progresso_geral = (media_trilha + (total_automacoes/len(equipe)*100)) / 2
        st.metric(
            label="📊 Progresso Geral",
            value=f"{progresso_geral:.1f}%",
            delta=f"{progresso_geral - 100:.1f}% vs Meta"
        )

    col_pizza1, col_pizza2 = st.columns(2)

    with col_pizza1:
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
            title="📚 Trilha da Lívia - % Conclusão",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=350
        )
        st.plotly_chart(fig_trilha, use_container_width=True)

    with col_pizza2:
        df_auto = pd.DataFrame(equipe)
        df_auto['status'] = df_auto['automacoes'].apply(lambda x: 'Concluído' if x >= 1 else 'Pendente')
        status_count = df_auto['status'].value_counts()
        
        fig_auto = go.Figure(data=[go.Pie(
            labels=status_count.index,
            values=status_count.values,
            marker=dict(colors=['#DC143C', '#8B0000']),
            hole=0.4,
            textinfo='label+value',
            textfont=dict(color='white', size=14)
        )])
        fig_auto.update_layout(
            title="🤖 Automações - Status",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=350
        )
        st.plotly_chart(fig_auto, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # OBJETIVO 2: CICLO DE PAGAMENTOS
    st.markdown("<div class='strategic-section'>", unsafe_allow_html=True)
    st.markdown("#### 💳 Ciclo de Pagamentos")
    st.caption("💳 OBJETIVO: Otimizar ciclo de pagamentos do grupo")

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
            delta="Meta: 24h"
        )

    # Gráfico Cashback
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
            height=350
        )
        st.plotly_chart(fig_cashback, use_container_width=True)

    with col_cb2:
        st.metric(
            label="📈 Aumento Acumulado",
            value=f"{aumento_percentual:.1f}%",
            delta=f"Meta: +{dados_estrategicos['ciclo_pagamentos']['cashback_meta_aumento']}%"
        )
        st.metric(
            label="💵 Cashback Atual",
            value=f"R$ {cashback_atual/1000:.0f}K/mês"
        )

    # Gráfico PMP
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

    # OBJETIVO 3: ACURACIDADE
    st.markdown("<div class='strategic-section'>", unsafe_allow_html=True)
    st.markdown("#### 📊 Acuracidade Contas a Receber")
    st.caption("📊 OBJETIVO: Garantir a acuracidade e integridade das informações de Contas a Receber")

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
            delta="+0.15% vs mês anterior"
        )

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
        height=350
    )
    st.plotly_chart(fig_desvio, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # OBJETIVO 4: EFICIÊNCIA OPERACIONAL
    st.markdown("<div class='strategic-section'>", unsafe_allow_html=True)
    st.markdown("#### 🏭 Eficiência Operacional")
    st.caption("⚙️ OBJETIVO: Aumentar a eficiência operacional da Tesouraria para fechamentos")

    col1, col2 = st.columns(2)

    with col1:
        fechamentos = dados_estrategicos['operacional']['fechamentos']
        fechamentos_total = dados_estrategicos['operacional']['fechamentos_total']
        fechamento_status = "✅" if fechamentos == fechamentos_total else "⚠️"
        st.metric(
            label=f"{fechamento_status} Fechamentos Mensais",
            value=f"{fechamentos}/{fechamentos_total}",
            delta="Meta: 8/8 sem atrasos"
        )

    with col2:
        vans_status = "✅" if dados_estrategicos['operacional']['vans_bancarias'] == 'Implementado' else "🔄"
        st.metric(
            label=f"{vans_status} Vans Bancárias",
            value=dados_estrategicos['operacional']['vans_bancarias'],
            delta="Status de Implementação"
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # OBJETIVO 5: RENTABILIDADE
    st.markdown("<div class='strategic-section'>", unsafe_allow_html=True)
    st.markdown("#### 💎 Rentabilidade e Gestão de Caixa")
    st.caption("💰 OBJETIVOS: Rentabilidade e Eficiência de Caixa")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        cdi_atual = dados_estrategicos['rentabilidade']['cdi_caixa']
        cdi_meta = dados_estrategicos['rentabilidade']['cdi_meta']
        st.metric(
            label="📈 % CDI do Caixa",
            value=f"{cdi_atual}%",
            delta=f"Meta: {cdi_meta}%"
        )

    with col2:
        st.metric(
            label="🎫 Bolecode",
            value=dados_estrategicos['rentabilidade']['bolecode_status']
        )

    with col3:
        conversao = dados_estrategicos['rentabilidade']['conversao_caixa_2anos']
        st.metric(
            label="💵 Conversão em Caixa",
            value=f"{conversao:.1f}%",
            delta="Últimos 2 anos"
        )

    with col4:
        score_rentabilidade = (cdi_atual + conversao) / 2
        st.metric(
            label="🏆 Score Geral",
            value=f"{score_rentabilidade:.1f}%",
            delta="+2.3% vs trimestre anterior"
        )

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
        yaxis=dict(range=[95, 101])
    )
    st.plotly_chart(fig_rent, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # OBJETIVO 6: PRAZOS
    st.markdown("<div class='strategic-section'>", unsafe_allow_html=True)
    st.markdown("#### ⏱️ Gestão de Prazos e Tickets")
    st.caption("⏰ OBJETIVO: Otimizar prazos operacionais e de retorno")

    col1, col2, col3 = st.columns(3)

    with col1:
        tickets = dados_estrategicos['prazos']['tickets_caixa']
        st.metric(
            label="📋 Tickets na Caixa",
            value=f"{tickets}",
            delta="Meta: Reduzir média",
            delta_color="inverse"
        )

    with col2:
        sla_horas = dados_estrategicos['prazos']['sla_horas_media']
        st.metric(
            label="⏱️ SLA 1ª Resposta",
            value=f"{sla_horas:.1f}h",
            delta="Meta: ≤ 24h"
        )

    with col3:
        cumprimento_sla = (24 / sla_horas) * 100 if sla_horas > 0 else 100
        st.metric(
            label="✅ Taxa de Cumprimento",
            value=f"{min(cumprimento_sla, 100):.1f}%"
        )

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
        yaxis=dict(title='Qtd. Tickets'),
        yaxis2=dict(title='SLA (horas)', overlaying='y', side='right'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_tickets, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # RESUMO EXECUTIVO
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #DC143C;'>📋 Resumo Executivo - Status Geral</h2>", unsafe_allow_html=True)

    scores = {
        'Eficiência Técnica': media_trilha,
        'Ciclo Pagamentos (PMP)': min(100, (pmp_meta / pmp_atual) * 100),
        'Acuracidade': 100 - desvio_atual,
        'Rentabilidade (CDI)': cdi_atual,
        'SLA Prazos': min(100, (24 / sla_horas) * 100) if sla_horas > 0 else 100
    }

    col1, col2 = st.columns([2, 1])

    with col1:
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
        score_geral = sum(scores.values()) / len(scores)
        
        st.metric(
            label="🎯 Score Geral",
            value=f"{score_geral:.1f}%",
            delta="+3.2% vs mês anterior"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**🔍 Status por Área:**")
        for area, score in scores.items():
            emoji = "✅" if score >= 90 else "⚠️" if score >= 70 else "🔴"
            st.markdown(f"{emoji} **{area}**: {score:.1f}%")

    # Footer
    st.markdown("---")
    st.markdown(f"""
        <div style='text-align: center; padding: 20px; opacity: 0.7;'>
            <p style='color: #FFFFFF; font-size: 0.9rem;'>
                🎯 Planejamento Estratégico da Tesouraria | Atualizado em: {datetime.now().strftime("%d/%m/%Y %H:%M")}
            </p>
        </div>
    """, unsafe_allow_html=True)

# === FOOTER GERAL ===
st.markdown("""
<div style='text-align: center; color: #666666; font-size: 0.9em; margin-top: 2rem;'>
    <div style="background: #1a1a1a; color: white; padding: 5px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; display: inline-block;">ALUN</div>
    <br>Dashboard Financeiro | Atualizado automaticamente
</div>
""", unsafe_allow_html=True)
