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

    # === CARREGAR DADOS REAIS DOS ARQUIVOS ===
    @st.cache_data
    def load_planejamento_data():
        """Carrega dados do planejamento estratégico - CSV"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "data", "planejamento_estrategico_2026.csv"),
            os.path.join(os.getcwd(), "data", "planejamento_estrategico_2026.csv"),
            os.path.join("data", "planejamento_estrategico_2026.csv"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    df = pd.read_csv(path)
                    # Converter valores numéricos
                    for col in ['meta', 'valor_atual']:
                        if col in df.columns:
                            df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                    return df
                except Exception as e:
                    st.error(f"Erro ao carregar planejamento: {e}")
                    return None
        
        st.warning("Arquivo planejamento_estrategico_2026.csv não encontrado")
        return None

    @st.cache_data
    def load_kpis_historico():
        """Carrega histórico de KPIs - CSV"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "data", "kpis_historico_2026.csv"),
            os.path.join(os.getcwd(), "data", "kpis_historico_2026.csv"),
            os.path.join("data", "kpis_historico_2026.csv"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    df = pd.read_csv(path)
                    # Converter valores numéricos
                    for col in ['valor', 'meta']:
                        if col in df.columns:
                            df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                    return df
                except Exception as e:
                    st.error(f"Erro ao carregar histórico: {e}")
                    return None
        
        st.warning("Arquivo kpis_historico_2026.csv não encontrado")
        return None

    # Carregar dados
    df_planejamento_raw = load_planejamento_data()
    df_historico_raw = load_kpis_historico()
    
    if df_planejamento_raw is None or df_historico_raw is None:
        st.error("⚠️ Não foi possível carregar os dados. Verifique se os arquivos CSV estão na pasta /data")
        st.stop()

    # Filtros
    st.markdown("### 📅 Filtros de Acompanhamento")
    col_filtro1, col_filtro2, col_filtro3 = st.columns([2, 2, 2])

    # Obter anos disponíveis nos dados
    anos_disponiveis = sorted(df_planejamento_raw['ano'].dropna().unique().tolist())
    if not anos_disponiveis:
        anos_disponiveis = [2024, 2025, 2026]
    
    with col_filtro1:
        opcoes_ano = ["Todos"] + [int(a) for a in anos_disponiveis]
        ano_selecionado = st.selectbox(
            "Ano",
            options=opcoes_ano,
            index=0,
            key="plan_ano_filtro"
        )

    with col_filtro2:
        meses_lista = ["Todos", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                     "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        mes_selecionado = st.selectbox(
            "Mês",
            options=meses_lista,
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

    # Aplicar filtros
    df_planejamento = df_planejamento_raw.copy()
    df_historico = df_historico_raw.copy()
    
    # Filtrar por ano
    if ano_selecionado != "Todos":
        df_planejamento = df_planejamento[df_planejamento['ano'] == ano_selecionado]
        df_historico = df_historico[df_historico['ano'] == ano_selecionado]
    
    # Filtrar por mês
    if mes_selecionado != "Todos":
        mes_num = meses_lista.index(mes_selecionado)  # Janeiro=1, etc.
        df_planejamento = df_planejamento[df_planejamento['mes'] == mes_num]
        df_historico = df_historico[df_historico['mes'] == mes_num]
    
    # Filtrar por trimestre
    if trimestre_selecionado != "Todos":
        trimestre_map = {"Q1": [1,2,3], "Q2": [4,5,6], "Q3": [7,8,9], "Q4": [10,11,12]}
        meses_trimestre = trimestre_map[trimestre_selecionado]
        df_planejamento = df_planejamento[df_planejamento['mes'].isin(meses_trimestre)]
        df_historico = df_historico[df_historico['mes'].isin(meses_trimestre)]

    # Mostrar período selecionado
    if not df_planejamento.empty:
        periodo_info = []
        if ano_selecionado != "Todos":
            periodo_info.append(f"Ano: {ano_selecionado}")
        if mes_selecionado != "Todos":
            periodo_info.append(f"Mês: {mes_selecionado}")
        if trimestre_selecionado != "Todos":
            periodo_info.append(f"Trimestre: {trimestre_selecionado}")
        
        if periodo_info:
            st.info(f"📅 Filtros ativos: {' | '.join(periodo_info)}")
        else:
            st.info("📅 Exibindo todos os dados disponíveis")
    else:
        st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados")
        st.stop()

    st.markdown("---")

    # === FUNÇÕES DE CÁLCULO DE STATUS ===
    def calcular_status_indicador(valor, meta, tipo_calculo, tipo_indicador):
        """
        Calcula o status do indicador baseado no tipo de cálculo:
        - maior_melhor: valor >= meta é bom (ex: % trilha, % CDI)
        - menor_melhor: valor < meta é bom (ex: PMP, saldo irregularidades)
        - menor_igual_melhor: valor <= meta é bom (ex: SLA, desvio)
        - maior_igual_melhor: valor >= meta é bom (ex: CDI)
        - percentual_meta: calcular % atingido da meta (ex: cashback)
        - sim_nao: valor booleano
        """
        if tipo_indicador == 'booleano':
            valor_str = str(valor).lower().strip()
            meta_str = str(meta).lower().strip()
            atingido = valor_str in ['sim', 's', '1', 'true', 'yes']
            return {
                'atingido': atingido,
                'emoji': '✅' if atingido else '❌',
                'cor': 'green' if atingido else 'red',
                'texto': 'Sim' if atingido else 'Não',
                'progresso': 100 if atingido else 0
            }
        
        try:
            valor = float(valor)
            meta = float(meta)
        except:
            return {'atingido': False, 'emoji': '⚪', 'cor': 'gray', 'texto': 'Sem dados', 'progresso': 0}
        
        if tipo_calculo == 'maior_melhor':
            progresso = (valor / meta * 100) if meta > 0 else 0
            atingido = valor >= meta
            
        elif tipo_calculo == 'menor_melhor':
            # Quanto menor, melhor. Meta é o máximo aceitável
            if meta == 0:
                atingido = valor == 0
                progresso = 100 if valor == 0 else max(0, 100 - (valor * 10))  # Penalização
            else:
                atingido = valor < meta
                # Invertido: valor menor = progresso maior
                progresso = max(0, min(100, (1 - (valor / meta)) * 100 + 100)) if valor < meta else max(0, (meta / valor) * 100)
                
        elif tipo_calculo == 'menor_igual_melhor':
            atingido = valor <= meta
            if meta == 0:
                progresso = 100 if valor == 0 else 0
            else:
                progresso = 100 if atingido else max(0, (meta / valor) * 100)
                
        elif tipo_calculo == 'maior_igual_melhor':
            atingido = valor >= meta
            progresso = (valor / meta * 100) if meta > 0 else 0
            
        elif tipo_calculo == 'percentual_meta':
            progresso = (valor / meta * 100) if meta > 0 else 0
            atingido = valor >= meta
            
        else:
            progresso = (valor / meta * 100) if meta > 0 else 0
            atingido = progresso >= 100
        
        if atingido:
            emoji = '✅'
            cor = 'green'
        elif progresso >= 70:
            emoji = '🟡'
            cor = 'orange'
        else:
            emoji = '🔴'
            cor = 'red'
        
        return {
            'atingido': atingido,
            'emoji': emoji,
            'cor': cor,
            'progresso': min(progresso, 150),  # Cap em 150%
            'texto': f"{progresso:.0f}%"
        }

    # Processar dados por objetivo
    objetivos_unicos = df_planejamento['objetivo'].unique()
    
    # Mapa de tipo de objetivo para tipo no histórico
    obj_tipo_map = {
        'eficiência técnica': 'eficiencia_tecnica',
        'ciclo de pagamentos': 'ciclo_pagamentos',
        'acuracidade': 'acuracidade',
        'eficiência operacional': 'operacional',
        'rentabilidade': 'rentabilidade',
        'eficiência e previsibilidade': 'eficiencia_caixa',
        'prazos operacionais': 'prazos'
    }
    
    # === MOSTRAR CADA OBJETIVO COM DADOS REAIS ===
    for idx, objetivo in enumerate(objetivos_unicos, 1):
        st.markdown("<div class='strategic-section'>", unsafe_allow_html=True)
        
        # Buscar dados deste objetivo
        df_obj = df_planejamento[df_planejamento['objetivo'] == objetivo]
        
        # Mostrar nome completo do objetivo
        st.markdown(f"#### 🎯 Objetivo {idx}")
        st.markdown(f"**{objetivo}**")
        st.markdown("---")
        
        # Mostrar período dos dados
        if not df_obj.empty:
            row_exemplo = df_obj.iloc[0]
            mes_nome = meses_lista[int(row_exemplo['mes'])] if pd.notna(row_exemplo.get('mes')) else ''
            ano_dado = int(row_exemplo['ano']) if pd.notna(row_exemplo.get('ano')) else ''
            st.caption(f"📅 Dados de: {mes_nome}/{ano_dado}")
        
        # Mostrar cada resultado-chave
        for _, row in df_obj.iterrows():
            tipo_calculo = row.get('tipo_calculo', 'maior_melhor')
            tipo_indicador = row.get('tipo_indicador', 'percentual')
            
            # Calcular status corretamente
            status = calcular_status_indicador(
                row['valor_atual'], 
                row['meta'], 
                tipo_calculo, 
                tipo_indicador
            )
            
            col1, col2, col3, col4 = st.columns([3, 1.5, 1, 1])
            
            with col1:
                st.markdown(f"**📌 {row['resultado_chave']}**")
                if pd.notna(row.get('observacoes')) and str(row.get('observacoes', '')).strip():
                    st.caption(f"💬 {row['observacoes']}")
            
            with col2:
                # Mostrar valor atual com formatação correta
                if tipo_indicador == 'booleano':
                    valor_display = status['texto']
                else:
                    try:
                        valor_num = float(str(row['valor_atual']).replace(',', '.'))
                        if tipo_indicador == 'reais':
                            valor_display = f"R$ {valor_num:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                        elif tipo_indicador == 'dias':
                            valor_display = f"{valor_num:.2f} dias"
                        elif tipo_indicador == 'horas':
                            valor_display = f"{valor_num:.1f}h"
                        elif tipo_indicador == 'quantidade':
                            valor_display = f"{int(valor_num)}"
                        else:
                            valor_display = f"{valor_num:.2f}%"
                    except:
                        valor_display = str(row['valor_atual'])
                
                # Delta baseado no tipo de cálculo
                if tipo_indicador != 'booleano':
                    if tipo_calculo in ['menor_melhor', 'menor_igual_melhor']:
                        delta_txt = "✅ Dentro da meta" if status['atingido'] else "⚠️ Fora da meta"
                    else:
                        delta_txt = f"{status['progresso']:.0f}% da meta"
                    
                    st.metric(
                        label=f"{status['emoji']} Atual",
                        value=valor_display,
                        delta=delta_txt,
                        delta_color="normal" if status['atingido'] else "inverse"
                    )
                else:
                    st.metric(
                        label=f"{status['emoji']} Status",
                        value=valor_display
                    )
            
            with col3:
                # Mostrar meta com formatação correta
                try:
                    if tipo_indicador == 'booleano':
                        meta_display = "Sim"
                    else:
                        meta_num = float(str(row['meta']).replace(',', '.'))
                        if tipo_indicador == 'reais':
                            meta_display = f"R$ {meta_num:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                        elif tipo_indicador == 'dias':
                            meta_display = f"≥ {meta_num:.0f} dias"
                        elif tipo_indicador == 'horas':
                            meta_display = f"≤ {meta_num:.0f}h"
                        elif tipo_indicador == 'quantidade':
                            meta_display = f"≤ {int(meta_num)}"
                        else:
                            meta_display = f"{meta_num:.1f}%"
                except:
                    meta_display = str(row['meta'])
                
                st.metric(label="🎯 Meta", value=meta_display)
            
            with col4:
                # Barra de progresso visual
                prog = min(status['progresso'], 100)
                cor_barra = '#00FF00' if status['atingido'] else '#FFD700' if prog >= 70 else '#FF4444'
                st.markdown(f"""
                    <div style='background: #333; border-radius: 5px; height: 30px; margin-top: 25px;'>
                        <div style='background: {cor_barra}; width: {max(prog, 5)}%; height: 100%; border-radius: 5px; display: flex; align-items: center; justify-content: center;'>
                            <span style='color: black; font-weight: bold; font-size: 11px;'>{status['progresso']:.0f}%</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        # === GRÁFICOS DE EVOLUÇÃO HISTÓRICA ===
        # Identificar tipo do objetivo para buscar histórico
        obj_tipo = None
        obj_tipo_map_local = {
            'eficiência técnica': 'eficiencia_tecnica',
            'ciclo de pagamentos': 'ciclo_pagamentos',
            'acuracidade': 'acuracidade',
            'eficiência operacional': 'operacional',
            'rentabilidade': 'rentabilidade',
            'eficiência e previsibilidade': 'eficiencia_caixa',
            'prazos operacionais': 'prazos'
        }
        
        for key_word, tipo in obj_tipo_map_local.items():
            if key_word.lower() in objetivo.lower():
                obj_tipo = tipo
                break
        
        # Se encontrou tipo, mostrar gráficos de evolução
        if obj_tipo and df_historico_raw is not None:
            df_hist_obj = df_historico_raw[df_historico_raw['kpi_tipo'] == obj_tipo].copy()
            
            if not df_hist_obj.empty:
                st.markdown("### 📈 Evolução Histórica")
                
                # Criar colunas para gráficos lado a lado
                kpis_unicos = df_hist_obj['kpi_nome'].unique()
                
                if len(kpis_unicos) >= 2:
                    col_graf1, col_graf2 = st.columns(2)
                    cols_graf = [col_graf1, col_graf2]
                else:
                    cols_graf = [st.container()]
                
                for i, kpi_nome in enumerate(kpis_unicos):
                    df_kpi = df_hist_obj[df_hist_obj['kpi_nome'] == kpi_nome].sort_values(['ano', 'mes']).copy()
                    
                    if len(df_kpi) >= 1:
                        # Criar label do eixo X
                        meses_abrev = ['', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
                        df_kpi['periodo_label'] = df_kpi.apply(
                            lambda r: f"{meses_abrev[int(r['mes'])]}/{str(int(r['ano']))[-2:]}", axis=1
                        )
                        
                        fig = go.Figure()
                        
                        # Obter tipo de cálculo
                        tipo_calc = df_kpi['tipo_calculo'].iloc[0] if 'tipo_calculo' in df_kpi.columns else 'maior_melhor'
                        
                        # Linha de valores realizados
                        fig.add_trace(go.Scatter(
                            x=df_kpi['periodo_label'],
                            y=df_kpi['valor'],
                            mode='lines+markers+text',
                            name='Realizado',
                            line=dict(color='#DC143C', width=3),
                            marker=dict(size=12, color='#DC143C'),
                            text=df_kpi['valor'].apply(lambda x: f"{x:.1f}"),
                            textposition='top center',
                            textfont=dict(color='white', size=10)
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
                        
                        # Mapeamento de nomes amigáveis para os gráficos
                        nomes_amigaveis = {
                            'trilha_livia': 'Trilha Lívia',
                            'trilha_livia_percent': 'Trilha Lívia',
                            'automacoes': 'Automações',
                            'automacoes_percent': 'Automações',
                            'pmp_dias': 'PMP (dias)',
                            'cashback_mensal': 'Cashback Mensal',
                            'sla_horas': 'SLA 1ª Resposta',
                            'desvio_percentual': 'Desvio Financeiro',
                            'saldo_irregularidades': 'Saldo Irregularidades',
                            'fechamento_sem_atraso': 'Fechamento',
                            'vans_bancarias': 'Vans Bancárias',
                            'cdi_percentual': '% CDI',
                            'bolecode_implementado': 'Bolecode',
                            'conversao_caixa': 'Conversão em Caixa',
                            'tickets_caixa': 'Tickets na Caixa',
                            'sla_tickets_horas': 'SLA Tickets'
                        }
                        kpi_label = nomes_amigaveis.get(kpi_nome, kpi_nome.replace('_', ' ').title())
                        
                        # Título com indicação de lógica
                        if tipo_calc in ['menor_melhor', 'menor_igual_melhor']:
                            titulo_extra = " (↓ menor = melhor)"
                        else:
                            titulo_extra = " (↑ maior = melhor)"
                        
                        fig.update_layout(
                            title=dict(text=f"{kpi_label}{titulo_extra}", font=dict(size=14)),
                            xaxis_title="Período",
                            yaxis_title=f"Valor ({unidade})",
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='white'),
                            height=300,
                            showlegend=True,
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                            margin=dict(l=40, r=40, t=60, b=40)
                        )
                        
                        # Usar coluna apropriada
                        with cols_graf[i % len(cols_graf)]:
                            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # RESUMO EXECUTIVO
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #DC143C;'>📋 Resumo Executivo - Status Geral</h2>", unsafe_allow_html=True)
    
    # Calcular progresso geral por objetivo usando a lógica correta
    resumo_objetivos = []
    for objetivo in objetivos_unicos:
        df_obj = df_planejamento[df_planejamento['objetivo'] == objetivo]
        indicadores_atingidos = 0
        total_indicadores = 0
        
        for _, row in df_obj.iterrows():
            tipo_calculo = row.get('tipo_calculo', 'maior_melhor')
            tipo_indicador = row.get('tipo_indicador', 'percentual')
            
            status = calcular_status_indicador(
                row['valor_atual'], 
                row['meta'], 
                tipo_calculo, 
                tipo_indicador
            )
            
            total_indicadores += 1
            if status['atingido']:
                indicadores_atingidos += 1
        
        if total_indicadores > 0:
            progresso = (indicadores_atingidos / total_indicadores) * 100
            resumo_objetivos.append({
                'objetivo': objetivo[:50] + '...' if len(objetivo) > 50 else objetivo,
                'progresso': progresso,
                'atingidos': indicadores_atingidos,
                'total': total_indicadores
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
                    colorscale=[[0, '#8B0000'], [0.5, '#FFD700'], [1, '#00FF00']],
                    showscale=False
                ),
                text=[f"{int(row['atingidos'])}/{int(row['total'])} ({row['progresso']:.0f}%)" for _, row in df_resumo.iterrows()],
                textposition='outside',
                textfont=dict(color='white')
            ))
            fig_resumo.add_vline(x=100, line_dash="dash", line_color="white", annotation_text="100%")
            fig_resumo.update_layout(
                title="Metas Atingidas por Objetivo",
                xaxis_title="% Indicadores Atingidos",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400,
                xaxis=dict(range=[0, 110])
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
