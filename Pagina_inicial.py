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
tab1, tab2, tab3 = st.tabs(["💰 Saldos do Ecossistema", "🎯 Planejamento Estratégico", "📊 Endividamento"])

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

    # === CARREGAR DADOS DO ARQUIVO ÚNICO ===
    @st.cache_data(ttl=60)  # Cache por apenas 60 segundos para pegar atualizações rápido
    def load_dados_mensais():
        """Carrega dados do arquivo único dados_mensais.csv"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "data", "dados_mensais.csv"),
            os.path.join(os.getcwd(), "data", "dados_mensais.csv"),
            os.path.join("data", "dados_mensais.csv"),
        ]
        
        def fix_encoding_issues(text):
            """Corrige problemas comuns de encoding"""
            if pd.isna(text):
                return text
            text = str(text)
            # Corrigir caracteres mal-decodificados
            replacements = {
                'Ã¡': 'á', 'Ã©': 'é', 'Ã­': 'í', 'Ã³': 'ó', 'Ãº': 'ú',
                'Ã¢': 'â', 'Ãª': 'ê', 'Ã´': 'ô',
                'Ã£': 'ã', 'Ãµ': 'õ',
                'Ã§': 'ç',
                'Ã': 'Á', 'Ã‰': 'É', 'Ã': 'Í', 'Ã"': 'Ó', 'Ãš': 'Ú',
                'Ã‚': 'Â', 'ÃŠ': 'Ê', 'Ã"': 'Ô',
                'Ãƒ': 'Ã', 'Ã•': 'Õ',
                'Ã‡': 'Ç',
                'Âª': 'ª', 'Âº': 'º'
            }
            for wrong, right in replacements.items():
                text = text.replace(wrong, right)
            return text
        
        for path in possible_paths:
            if os.path.exists(path):
                # Tentar múltiplos encodings (Excel BR usa ISO-8859-1 ou cp1252)
                encodings = ['utf-8', 'utf-8-sig', 'iso-8859-1', 'latin1', 'cp1252']
                for encoding in encodings:
                    try:
                        # Tentar com ponto-e-vírgula primeiro (padrão Excel BR)
                        df = pd.read_csv(path, encoding=encoding, sep=';')
                        if len(df.columns) == 1:  # Se não separou, tentar com vírgula
                            df = pd.read_csv(path, encoding=encoding, sep=',')
                        
                        # Corrigir encoding em todas as colunas de texto
                        for col in df.select_dtypes(include=['object']).columns:
                            df[col] = df[col].apply(fix_encoding_issues)
                        
                        return df
                    except (UnicodeDecodeError, Exception):
                        continue
                
                st.error(f"Não foi possível ler o arquivo com nenhum encoding. Tente salvar como UTF-8.")
                return None
        
        st.warning("Arquivo dados_mensais.csv não encontrado na pasta /data")
        return None

    # Carregar dados
    df_raw = load_dados_mensais()
    
    if df_raw is None:
        st.error("⚠️ Não foi possível carregar os dados. Verifique se o arquivo dados_mensais.csv está na pasta /data")
        st.stop()

    # === CONVERTER VALORES (vírgula para ponto) ===
    def converter_valor(valor):
        """Converte valor brasileiro (vírgula) para número"""
        if pd.isna(valor):
            return None
        valor_str = str(valor).strip().lower()
        
        # Booleanos
        if valor_str in ['sim', 's', 'yes', 'true', '1']:
            return 1
        if valor_str in ['não', 'nao', 'n', 'no', 'false', '0']:
            return 0
        
        # Números com vírgula
        try:
            valor_str = str(valor).replace(',', '.')
            return float(valor_str)
        except:
            return None

    df = df_raw.copy()
    df['VALOR_NUM'] = df['VALOR'].apply(converter_valor)
    df['META_NUM'] = df['META'].apply(converter_valor)

    # === MAPEAMENTO DE MESES ===
    meses_ordem = {
        'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4,
        'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8,
        'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
    }
    df['MES_NUM'] = df['MES'].map(meses_ordem)

    # === FILTROS ===
    st.markdown("### 📅 Filtros")
    col_f1, col_f2, col_f3 = st.columns(3)

    anos_disponiveis = sorted(df['ANO'].unique().tolist())
    meses_disponiveis = df['MES'].unique().tolist()
    # Ordenar meses
    meses_disponiveis = sorted(meses_disponiveis, key=lambda x: meses_ordem.get(x, 0))

    with col_f1:
        ano_sel = st.selectbox("Ano", ["Todos"] + anos_disponiveis, index=0, key="plan_ano")
    
    with col_f2:
        mes_sel = st.selectbox("Mês", ["Todos"] + meses_disponiveis, index=0, key="plan_mes")
    
    with col_f3:
        # Opção de ver último período
        ver_ultimo = st.checkbox("📍 Ver apenas o período mais recente", value=True)

    # Aplicar filtros
    df_filtrado = df.copy()
    
    if ver_ultimo:
        # Pegar o período mais recente
        df_filtrado = df_filtrado.sort_values(['ANO', 'MES_NUM'], ascending=[False, False])
        ultimo_ano = df_filtrado['ANO'].iloc[0]
        ultimo_mes = df_filtrado['MES'].iloc[0]
        df_filtrado = df_filtrado[(df_filtrado['ANO'] == ultimo_ano) & (df_filtrado['MES'] == ultimo_mes)]
        st.info(f"📅 Exibindo dados de: **{ultimo_mes}/{ultimo_ano}**")
    else:
        if ano_sel != "Todos":
            df_filtrado = df_filtrado[df_filtrado['ANO'] == int(ano_sel)]
        if mes_sel != "Todos":
            df_filtrado = df_filtrado[df_filtrado['MES'] == mes_sel]
        
        if df_filtrado.empty:
            st.warning("Nenhum dado encontrado para os filtros selecionados")
            st.stop()
        
        periodos = df_filtrado.groupby(['MES', 'ANO']).size().reset_index()
        periodos_str = ", ".join([f"{row['MES']}/{row['ANO']}" for _, row in periodos.iterrows()])
        st.info(f"📅 Exibindo dados de: **{periodos_str}**")

    st.markdown("---")

    # === FUNÇÃO PARA CALCULAR STATUS E GERAR OBSERVAÇÃO ===
    def calcular_status(row):
        """Calcula status e gera observação automática"""
        valor = row['VALOR_NUM']
        meta = row['META_NUM']
        indicador = row['INDICADOR']
        como_preencher = row['COMO_PREENCHER']
        
        if pd.isna(valor) or pd.isna(meta):
            return {'atingido': False, 'emoji': '⚪', 'obs': 'Sem dados', 'progresso': 0}
        
        # Determinar tipo de indicador e lógica
        eh_percentual = 'Percentual' in como_preencher
        eh_dias = 'dias' in como_preencher.lower()
        eh_horas = 'Horas' in como_preencher
        eh_reais = 'reais' in como_preencher.lower()
        eh_sim_nao = 'Sim ou Não' in como_preencher
        eh_quantidade = 'Quantidade' in como_preencher
        
        # Lógica especial por indicador
        indicador_lower = indicador.lower()
        
        # PMP: maior é melhor (queremos aumentar o prazo)
        if 'pmp' in indicador_lower or 'prazo médio' in indicador_lower:
            atingido = valor >= meta
            progresso = (valor / meta * 100) if meta > 0 else 0
            if atingido:
                obs = f"✅ {valor:.2f} dias - ATINGIU a meta de {meta:.0f} dias"
            else:
                obs = f"⚠️ {valor:.2f} dias - ABAIXO da meta de {meta:.0f} dias"
        
        # SLA, Desvio, Irregularidades, Tickets: menor é melhor
        elif any(x in indicador_lower for x in ['sla', 'desvio', 'irregularidades', 'tickets']):
            if meta == 0:  # Meta é zerar
                atingido = valor == 0
                progresso = 100 if valor == 0 else max(0, 100 - (valor / 10000 * 100))
                if atingido:
                    obs = f"✅ Zerado!"
                else:
                    obs = f"⚠️ R$ {valor:,.0f} restantes - Meta é zerar".replace(',', '.')
            else:
                atingido = valor <= meta
                progresso = (meta / valor * 100) if valor > 0 else 100
                if eh_horas:
                    if atingido:
                        obs = f"✅ {valor:.1f}h - DENTRO da meta de {meta:.0f}h"
                    else:
                        obs = f"❌ {valor:.1f}h - ACIMA da meta de {meta:.0f}h"
                elif eh_percentual:
                    if atingido:
                        obs = f"✅ {valor:.2f}% - DENTRO do limite de {meta:.1f}%"
                    else:
                        obs = f"❌ {valor:.2f}% - ACIMA do limite de {meta:.1f}%"
                else:
                    if atingido:
                        obs = f"✅ {valor:.0f} - DENTRO da meta de {meta:.0f}"
                    else:
                        obs = f"❌ {valor:.0f} - ACIMA da meta de {meta:.0f}"
        
        # Booleanos (Sim/Não)
        elif eh_sim_nao:
            atingido = valor == 1
            progresso = 100 if atingido else 0
            valor_txt = "Sim" if valor == 1 else "Não"
            if atingido:
                obs = f"✅ {valor_txt} - Concluído!"
            else:
                obs = f"❌ {valor_txt} - Pendente"
        
        # Cashback: precisa atingir a meta (valor >= meta)
        elif 'cashback' in indicador_lower:
            atingido = valor >= meta
            progresso = (valor / meta * 100) if meta > 0 else 0
            if atingido:
                obs = f"✅ R$ {valor:,.0f} - ATINGIU a meta de R$ {meta:,.0f}".replace(',', '.')
            else:
                falta = meta - valor
                obs = f"⚠️ R$ {valor:,.0f} - Faltam R$ {falta:,.0f} para a meta".replace(',', '.')
        
        # Padrão: maior é melhor (percentuais, CDI, etc)
        else:
            atingido = valor >= meta
            progresso = (valor / meta * 100) if meta > 0 else 0
            if eh_percentual:
                if atingido:
                    obs = f"✅ {valor:.1f}% - ATINGIU a meta de {meta:.0f}%"
                else:
                    obs = f"⚠️ {valor:.1f}% - Faltam {meta - valor:.1f}% para a meta"
            elif eh_reais:
                if atingido:
                    obs = f"✅ R$ {valor:,.0f}".replace(',', '.')
                else:
                    obs = f"⚠️ R$ {valor:,.0f}".replace(',', '.')
            else:
                if atingido:
                    obs = f"✅ {valor}"
                else:
                    obs = f"⚠️ {valor}"
        
        emoji = '✅' if atingido else '🟡' if progresso >= 70 else '❌'
        
        return {
            'atingido': atingido,
            'emoji': emoji,
            'obs': obs,
            'progresso': min(progresso, 150)
        }

    # === MOSTRAR OBJETIVOS ===
    objetivos = df_filtrado['OBJETIVO'].unique()
    
    for idx, objetivo in enumerate(objetivos, 1):
        st.markdown(f"<div class='strategic-section'>", unsafe_allow_html=True)
        st.markdown(f"### 🎯 Objetivo {idx}")
        st.markdown(f"**{objetivo}**")
        st.markdown("---")
        
        df_obj = df_filtrado[df_filtrado['OBJETIVO'] == objetivo]
        
        for _, row in df_obj.iterrows():
            status = calcular_status(row)
            como_preencher = row['COMO_PREENCHER']
            eh_percentual = 'Percentual' in como_preencher
            eh_sim_nao = 'Sim ou Não' in como_preencher
            
            col1, col2, col3, col4 = st.columns([3, 1.5, 1, 1.5])
            
            with col1:
                st.markdown(f"**📌 {row['INDICADOR']}**")
                st.caption(f"💬 {status['obs']}")
            
            with col2:
                # Formatar valor
                valor = row['VALOR_NUM']
                if eh_sim_nao:
                    valor_fmt = "Sim" if valor == 1 else "Não"
                elif eh_percentual:
                    valor_fmt = f"{valor:.1f}%"
                elif 'reais' in como_preencher.lower():
                    valor_fmt = f"R$ {valor:,.0f}".replace(',', '.')
                elif 'dias' in como_preencher.lower():
                    valor_fmt = f"{valor:.2f} dias"
                elif 'Horas' in como_preencher:
                    valor_fmt = f"{valor:.1f}h"
                else:
                    valor_fmt = f"{valor:.0f}"
                
                st.metric(label=f"{status['emoji']} Atual", value=valor_fmt)
            
            with col3:
                # Formatar meta
                meta = row['META_NUM']
                if eh_sim_nao:
                    meta_fmt = "Sim"
                elif eh_percentual:
                    meta_fmt = f"{meta:.0f}%"
                elif 'reais' in como_preencher.lower():
                    meta_fmt = f"R$ {meta:,.0f}".replace(',', '.')
                elif 'dias' in como_preencher.lower():
                    meta_fmt = f"{meta:.0f} dias"
                elif 'Horas' in como_preencher:
                    meta_fmt = f"≤{meta:.0f}h"
                else:
                    meta_fmt = f"{meta:.0f}"
                
                st.metric(label="🎯 Meta", value=meta_fmt)
            
            with col4:
                # Barra de progresso
                prog = min(status['progresso'], 100)
                cor = '#00FF00' if status['atingido'] else '#FFD700' if prog >= 70 else '#FF4444'
                st.markdown(f"""
                    <div style='background: #333; border-radius: 5px; height: 30px; margin-top: 25px;'>
                        <div style='background: {cor}; width: {max(prog, 5)}%; height: 100%; border-radius: 5px; display: flex; align-items: center; justify-content: center;'>
                            <span style='color: black; font-weight: bold; font-size: 11px;'>{status['progresso']:.0f}%</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        # === GRÁFICO DE EVOLUÇÃO (se não estiver vendo só último período) ===
        if not ver_ultimo:
            st.markdown("### 📈 Evolução Histórica")
            
            df_hist = df[df['OBJETIVO'] == objetivo].copy()
            df_hist = df_hist.sort_values(['ANO', 'MES_NUM'])
            df_hist['PERIODO'] = df_hist['MES'].str[:3] + '/' + df_hist['ANO'].astype(str).str[-2:]
            
            indicadores = df_hist['INDICADOR'].unique()
            
            if len(indicadores) >= 2:
                col_g1, col_g2 = st.columns(2)
                cols = [col_g1, col_g2]
            else:
                cols = [st.container()]
            
            for i, indicador in enumerate(indicadores):
                df_ind = df_hist[df_hist['INDICADOR'] == indicador]
                como = df_ind['COMO_PREENCHER'].iloc[0]
                eh_perc = 'Percentual' in como
                eh_bool = 'Sim ou Não' in como
                
                if eh_bool or len(df_ind) < 2:
                    continue
                
                fig = go.Figure()
                
                # Linha realizado
                fig.add_trace(go.Scatter(
                    x=df_ind['PERIODO'],
                    y=df_ind['VALOR_NUM'],
                    mode='lines+markers+text',
                    name='Realizado',
                    line=dict(color='#DC143C', width=3),
                    marker=dict(size=10),
                    text=df_ind['VALOR_NUM'].apply(lambda x: f"{x:.1f}%" if eh_perc else f"{x:.1f}"),
                    textposition='top center',
                    textfont=dict(color='white', size=10)
                ))
                
                # Linha meta
                fig.add_trace(go.Scatter(
                    x=df_ind['PERIODO'],
                    y=df_ind['META_NUM'],
                    mode='lines',
                    name='Meta',
                    line=dict(color='#FFD700', width=2, dash='dash')
                ))
                
                unidade = '%' if eh_perc else ''
                fig.update_layout(
                    title=indicador,
                    xaxis_title="Período",
                    yaxis_title=f"Valor ({unidade})" if unidade else "Valor",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=300,
                    showlegend=True,
                    legend=dict(orientation="h", y=1.1)
                )
                
                with cols[i % len(cols)]:
                    st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # === PAINEL DE GRÁFICOS DE KPIS ===
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #DC143C;'>📊 Painel de Indicadores</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Visualização comparativa dos principais KPIs</p>", unsafe_allow_html=True)
    
    # Preparar dados para gráficos
    df_graficos = df_filtrado.copy()
    
    # === GRÁFICO 1: Gauge de Performance Geral ===
    total_indicadores = len(df_graficos)
    indicadores_atingidos = sum(1 for _, row in df_graficos.iterrows() if calcular_status(row)['atingido'])
    perc_geral = (indicadores_atingidos / total_indicadores * 100) if total_indicadores > 0 else 0
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        # Velocímetro de performance geral
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=perc_geral,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Performance Geral", 'font': {'size': 20, 'color': 'white'}},
            delta={'reference': 100, 'increasing': {'color': "#00FF00"}, 'decreasing': {'color': "#FF4444"}},
            number={'suffix': "%", 'font': {'size': 40, 'color': 'white'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white", 'tickfont': {'color': 'white'}},
                'bar': {'color': "#DC143C"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "white",
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(255, 68, 68, 0.3)'},
                    {'range': [50, 80], 'color': 'rgba(255, 215, 0, 0.3)'},
                    {'range': [80, 100], 'color': 'rgba(0, 255, 0, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': "#FFD700", 'width': 4},
                    'thickness': 0.75,
                    'value': 100
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'},
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.caption(f"✅ {indicadores_atingidos} de {total_indicadores} indicadores atingidos")
    
    with col_g2:
        # Gráfico de Radar por Objetivo
        categorias = []
        valores = []
        for obj in df_graficos['OBJETIVO'].unique():
            df_obj = df_graficos[df_graficos['OBJETIVO'] == obj]
            ating = sum(1 for _, r in df_obj.iterrows() if calcular_status(r)['atingido'])
            total = len(df_obj)
            perc = (ating / total * 100) if total > 0 else 0
            nome_curto = obj.split()[0:3]
            categorias.append(' '.join(nome_curto) + '...')
            valores.append(perc)
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=valores + [valores[0]],
            theta=categorias + [categorias[0]],
            fill='toself',
            fillcolor='rgba(220, 20, 60, 0.3)',
            line=dict(color='#DC143C', width=2),
            name='Realizado'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[100] * (len(categorias) + 1),
            theta=categorias + [categorias[0]],
            fill='toself',
            fillcolor='rgba(255, 215, 0, 0.1)',
            line=dict(color='#FFD700', width=1, dash='dash'),
            name='Meta (100%)'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color='white')),
                bgcolor='rgba(0,0,0,0)',
                angularaxis=dict(tickfont=dict(color='white', size=10))
            ),
            showlegend=True,
            legend=dict(orientation="h", y=-0.1, font=dict(color='white')),
            paper_bgcolor='rgba(0,0,0,0)',
            title=dict(text='Performance por Objetivo', font=dict(color='white', size=16)),
            height=350,
            margin=dict(l=60, r=60, t=50, b=60)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    # === STATUS DOS INDICADORES BOOLEANOS ===
    df_bool = df_graficos[df_graficos['COMO_PREENCHER'].str.contains('Sim ou Não', na=False)].copy()
    
    if not df_bool.empty:
        st.markdown("### ✅ Status de Implementações")
        
        # Layout vertical para evitar corte de texto
        for _, row in df_bool.iterrows():
            col1, col2, col3 = st.columns([1, 4, 1])
            
            with col2:
                valor = str(row['VALOR']).lower().strip()
                implementado = valor in ['sim', 's', '1', 'true', 'yes']
                
                cor = '#00FF00' if implementado else '#FF4444'
                icone = '✅' if implementado else '❌'
                status_txt = 'Implementado' if implementado else 'Pendente'
                
                # Garantir que o indicador está em UTF-8
                indicador_nome = str(row['INDICADOR'])
                
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, {cor}22, {cor}11); 
                                border: 2px solid {cor}; border-radius: 10px; 
                                padding: 20px; text-align: center; margin-bottom: 10px;'>
                        <div style='font-size: 40px;'>{icone}</div>
                        <div style='color: white; font-weight: bold; margin-top: 10px; font-size: 16px;'>
                            {indicador_nome}
                        </div>
                        <div style='color: {cor}; font-size: 14px; margin-top: 5px;'>
                            {status_txt}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    # === RESUMO EXECUTIVO ===
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #DC143C;'>📋 Resumo Executivo</h2>", unsafe_allow_html=True)
    
    resumo = []
    for objetivo in objetivos:
        df_obj = df_filtrado[df_filtrado['OBJETIVO'] == objetivo]
        atingidos = sum(1 for _, row in df_obj.iterrows() if calcular_status(row)['atingido'])
        total = len(df_obj)
        progresso = (atingidos / total * 100) if total > 0 else 0
        resumo.append({
            'objetivo': objetivo[:45] + '...' if len(objetivo) > 45 else objetivo,
            'atingidos': atingidos,
            'total': total,
            'progresso': progresso
        })
    
    df_resumo = pd.DataFrame(resumo)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_resumo = go.Figure()
        fig_resumo.add_trace(go.Bar(
            y=df_resumo['objetivo'],
            x=df_resumo['progresso'],
            orientation='h',
            marker=dict(
                color=df_resumo['progresso'],
                colorscale=[[0, '#8B0000'], [0.5, '#FFD700'], [1, '#00FF00']],
            ),
            text=[f"{r['atingidos']}/{r['total']} ({r['progresso']:.0f}%)" for _, r in df_resumo.iterrows()],
            textposition='outside',
            textfont=dict(color='white')
        ))
        fig_resumo.add_vline(x=100, line_dash="dash", line_color="white")
        fig_resumo.update_layout(
            title="Indicadores Atingidos por Objetivo",
            xaxis_title="% Atingido",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400,
            xaxis=dict(range=[0, 110])
        )
        st.plotly_chart(fig_resumo, use_container_width=True)
    
    with col2:
        score = df_resumo['progresso'].mean()
        st.metric("🎯 Score Geral", f"{score:.0f}%")
        
        st.markdown("**Status por Objetivo:**")
        for _, r in df_resumo.iterrows():
            emoji = '✅' if r['progresso'] >= 100 else '🟡' if r['progresso'] >= 50 else '❌'
            st.markdown(f"{emoji} {r['progresso']:.0f}% - {r['objetivo'][:25]}...")

    # Footer
    st.markdown("---")
    st.markdown(f"""
        <div style='text-align: center; padding: 20px; opacity: 0.7;'>
            <p style='color: #FFFFFF; font-size: 0.9rem;'>
                🎯 Planejamento Estratégico | Dados de: {df_filtrado['MES'].iloc[0]}/{df_filtrado['ANO'].iloc[0]}
            </p>
        </div>
    """, unsafe_allow_html=True)

# ==========================
# ABA 3: ENDIVIDAMENTO
# ==========================
with tab3:
    aplicar_css_planejamento()
    
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='color: #DC143C; font-size: 2.5rem; font-weight: 800; margin-bottom: 10px;'>
                📊 Análise de Endividamento
            </h1>
            <p style='color: #FFFFFF; font-size: 1.2rem; opacity: 0.9;'>
                Evolução da Dívida Líquida e Indicadores de Alavancagem
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # === CARREGAR DADOS DE ENDIVIDAMENTO ===
    @st.cache_data(ttl=60)
    def load_endividamento():
        """Carrega dados de endividamento"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "data", "endividamento.csv"),
            os.path.join(os.getcwd(), "data", "endividamento.csv"),
            os.path.join("data", "endividamento.csv"),
        ]
        
        def fix_encoding_issues(text):
            """Corrige problemas comuns de encoding"""
            if pd.isna(text):
                return text
            text = str(text)
            replacements = {
                'Ã¡': 'á', 'Ã©': 'é', 'Ã­': 'í', 'Ã³': 'ó', 'Ãº': 'ú',
                'Ã¢': 'â', 'Ãª': 'ê', 'Ã´': 'ô',
                'Ã£': 'ã', 'Ãµ': 'õ',
                'Ã§': 'ç',
            }
            for wrong, right in replacements.items():
                text = text.replace(wrong, right)
            return text
        
        for path in possible_paths:
            if os.path.exists(path):
                encodings = ['utf-8', 'utf-8-sig', 'iso-8859-1', 'latin1', 'cp1252']
                for encoding in encodings:
                    try:
                        df = pd.read_csv(path, encoding=encoding, sep=';')
                        if len(df.columns) == 1:
                            df = pd.read_csv(path, encoding=encoding, sep=',')
                        
                        # Corrigir encoding
                        for col in df.select_dtypes(include=['object']).columns:
                            df[col] = df[col].apply(fix_encoding_issues)
                        
                        return df
                    except:
                        continue
                
                st.error("Não foi possível ler o arquivo endividamento.csv")
                return None
        
        st.warning("Arquivo endividamento.csv não encontrado na pasta /data")
        return None

    # Carregar dados
    df_endiv = load_endividamento()
    
    if df_endiv is None:
        st.error("⚠️ Não foi possível carregar os dados de endividamento")
        st.stop()

    # === PREPARAR DADOS PARA VISUALIZAÇÃO ===
    # Extrair linha de Dívida Líquida e Dívida Líquida/EBITDA
    meses_cols = [col for col in df_endiv.columns if col != 'Metrica']
    
    divida_liquida_row = df_endiv[df_endiv['Metrica'] == 'Dívida Líquida']
    ratio_row = df_endiv[df_endiv['Metrica'] == 'Dívida Líquida/EBITDA']
    
    if divida_liquida_row.empty or ratio_row.empty:
        st.error("Dados de Dívida Líquida ou Ratio não encontrados")
        st.stop()
    
    # Converter para números
    divida_valores = []
    ratio_valores = []
    
    for mes in meses_cols:
        try:
            val_divida = str(divida_liquida_row[mes].values[0]).replace(',', '.')
            divida_valores.append(float(val_divida))
        except:
            divida_valores.append(0)
        
        try:
            val_ratio = str(ratio_row[mes].values[0]).replace(',', '.')
            ratio_valores.append(float(val_ratio))
        except:
            ratio_valores.append(0)
    
    # === MÉTRICAS PRINCIPAIS ===
    col1, col2, col3, col4 = st.columns(4)
    
    ultimo_mes = meses_cols[-1]
    penultimo_mes = meses_cols[-2] if len(meses_cols) > 1 else meses_cols[-1]
    
    divida_atual = divida_valores[-1]
    divida_anterior = divida_valores[-2] if len(divida_valores) > 1 else divida_valores[-1]
    var_divida = divida_atual - divida_anterior
    var_perc = (var_divida / divida_anterior * 100) if divida_anterior != 0 else 0
    
    ratio_atual = ratio_valores[-1]
    ratio_anterior = ratio_valores[-2] if len(ratio_valores) > 1 else ratio_valores[-1]
    var_ratio = ratio_atual - ratio_anterior
    
    with col1:
        st.metric(
            label=f"💰 Dívida Líquida ({ultimo_mes})",
            value=f"R$ {divida_atual:,.0f} MM",
            delta=f"{var_divida:+,.0f} MM ({var_perc:+.1f}%)"
        )
    
    with col2:
        st.metric(
            label=f"📊 Dívida Líq./EBITDA ({ultimo_mes})",
            value=f"{ratio_atual:.2f}x",
            delta=f"{var_ratio:+.2f}x"
        )
    
    with col3:
        media_ratio = sum(ratio_valores) / len(ratio_valores)
        st.metric(
            label="📈 Média Histórica Ratio",
            value=f"{media_ratio:.2f}x"
        )
    
    with col4:
        max_ratio = max(ratio_valores)
        mes_max = meses_cols[ratio_valores.index(max_ratio)]
        st.metric(
            label="⚠️ Pico de Alavancagem",
            value=f"{max_ratio:.2f}x",
            delta=f"em {mes_max}"
        )
    
    st.markdown("---")
    
    # === GRÁFICO COMBINADO: BARRAS + LINHA (2 EIXOS Y) ===
    st.markdown("### 📊 Evolução da Dívida Líquida e Alavancagem")
    
    fig = go.Figure()
    
    # Barras: Dívida Líquida (eixo Y principal - esquerda) - vermelho vinho
    fig.add_trace(go.Bar(
        x=meses_cols,
        y=divida_valores,
        name='Dívida Líquida (R$ MM)',
        marker_color='#722F37',
        yaxis='y',
        text=[f"R$ {v:,.0f}".replace(",", ".") for v in divida_valores],
        textposition='outside',
        textfont=dict(color='white', size=9)
    ))
    
    # Linha: Dívida Líquida/EBITDA (eixo Y secundário - direita)
    fig.add_trace(go.Scatter(
        x=meses_cols,
        y=ratio_valores,
        name='Dív.Líq./EBITDA',
        mode='lines+markers',
        line=dict(color='#FF8C00', width=3),
        marker=dict(size=10, color='#FF8C00'),
        yaxis='y2',
        hovertemplate='%{y:.2f}x<extra></extra>'
    ))
    
    # Layout com dois eixos Y - sem gridlines
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        xaxis=dict(
            title='Período',
            tickangle=45,
            showgrid=False
        ),
        yaxis=dict(
            title='Dívida Líquida (R$ MM)',
            showgrid=False,
            range=[0, max(divida_valores) * 1.3]
        ),
        yaxis2=dict(
            title='Dívida Líquida / EBITDA',
            overlaying='y',
            side='right',
            showgrid=False,
            range=[0, max(ratio_valores) * 1.5]
        ),
        hovermode='x unified',
        bargap=0.3
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # === TABELA DETALHADA COM ESTILIZAÇÃO ===
    st.markdown("---")
    st.markdown("### 📋 Composição da Dívida")
    
    # Categorias principais (destacar com cor diferente)
    categorias_principais = ['Dívida Bruta', 'Caixa e Disponibilidades', 'Dívida Líquida', 'Dívida Líquida/EBITDA']
    
    # Função para formatar valores
    def formatar_valor_tabela(valor, metrica):
        try:
            if pd.isna(valor):
                return "-"
            val_str = str(valor).replace(',', '.')
            val_float = float(val_str)
            
            # Dívida Líquida/EBITDA é índice, não R$
            if 'EBITDA' in metrica and 'Dívida' in metrica:
                return f"{val_float:.2f}x"
            else:
                # Formatar como R$ MM sem vírgula para milhar (usar ponto)
                return f"R$ {val_float:,.0f}".replace(",", ".")
        except:
            return str(valor)
    
    # Criar HTML da tabela estilizada
    html_tabela = """
    <style>
        .tabela-endiv {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            background-color: #1e1e1e;
            border-radius: 8px;
            overflow: hidden;
        }
        .tabela-endiv th {
            background-color: #2d2d2d;
            color: #ffffff;
            padding: 12px 8px;
            text-align: center;
            border-bottom: 2px solid #444;
            font-weight: bold;
        }
        .tabela-endiv td {
            padding: 10px 8px;
            text-align: right;
            border-bottom: 1px solid #333;
            color: #e0e0e0;
        }
        .tabela-endiv td:first-child {
            text-align: left;
            font-weight: 500;
        }
        .tabela-endiv tr:hover {
            background-color: #2a2a2a;
        }
        .categoria-principal {
            background-color: #3d3d5c !important;
            font-weight: bold !important;
        }
        .categoria-principal td {
            color: #ffffff !important;
            font-weight: bold;
        }
    </style>
    <table class="tabela-endiv">
        <thead>
            <tr>
                <th>Métrica</th>
    """
    
    # Adicionar colunas de meses
    for mes in meses_cols:
        html_tabela += f"<th>{mes}</th>"
    html_tabela += "</tr></thead><tbody>"
    
    # Adicionar linhas
    for _, row in df_endiv.iterrows():
        metrica = row['Metrica']
        is_principal = metrica in categorias_principais
        classe = 'categoria-principal' if is_principal else ''
        
        html_tabela += f'<tr class="{classe}"><td>{metrica}</td>'
        
        for mes in meses_cols:
            valor_formatado = formatar_valor_tabela(row[mes], metrica)
            html_tabela += f"<td>{valor_formatado}</td>"
        
        html_tabela += "</tr>"
    
    html_tabela += "</tbody></table>"
    
    st.markdown(html_tabela, unsafe_allow_html=True)
    
    # Legenda da tabela
    st.markdown("""
        <div style='margin-top: 10px; font-size: 12px; color: #888;'>
            <span style='display: inline-block; width: 15px; height: 15px; background-color: #3d3d5c; margin-right: 5px; vertical-align: middle; border-radius: 3px;'></span>
            Categorias consolidadas (totais)
        </div>
    """, unsafe_allow_html=True)
    
    # Download CSV
    csv_data = df_endiv.to_csv(index=False, sep=';')
    st.download_button(
        label="📥 Baixar dados como CSV",
        data=csv_data,
        file_name="endividamento.csv",
        mime="text/csv"
    )
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
        <div style='text-align: center; padding: 20px; opacity: 0.7;'>
            <p style='color: #FFFFFF; font-size: 0.9rem;'>
                📊 Endividamento | Último período: {meses_cols[-1]}
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
