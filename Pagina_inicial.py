import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai
import json
import numpy as np

st.set_page_config(
    layout='wide',
    page_title="📊 Dashboard ALUN - Análise Financeira",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# --- CSS CUSTOMIZADO COM TEMA ESCURO ALUN ---
st.markdown("""
<style>
    .main > div { background: transparent !important; }
    .main { background-color: #0e1117 !important; }
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 { color: #fafafa !important; font-weight: 700 !important; }
    .main p, .main span, .main div, .main label, .main li, .main th, .main td { color: #fafafa !important; }
    .main [data-testid="metric-container"] { background-color: #262730 !important; border: 1px solid #30343f !important; color: #fafafa !important; border-radius: 10px !important; padding: 1rem !important; }
    .main [data-testid="metric-container"] > div { color: #fafafa !important; }
    .main [data-testid="stContainer"] { background-color: #0e1117 !important; border: 1px solid #30343f !important; border-radius: 10px !important; }
    .compact-controls { background: #262730 !important; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; border: 1px solid #30343f !important; box-shadow: 0 2px 10px rgba(14, 17, 23, 0.3) !important; }
    .main .stTabs [data-baseweb="tab-list"] { background-color: #262730 !important; border-radius: 8px !important; }
    .main .stTabs [data-baseweb="tab"] { background-color: #0e1117 !important; color: #fafafa !important; border: 1px solid #30343f !important; border-radius: 6px !important; }
    .main .stTabs [aria-selected="true"] { background-color: #ff6b35 !important; color: #ffffff !important; border: 1px solid #ff6b35 !important; }
    .main .stDataFrame { background-color: #262730 !important; color: #fafafa !important; border-radius: 8px !important; }
    .main [data-testid="stDownloadButton"] > button { background-color: #ff6b35 !important; color: #ffffff !important; border: none !important; border-radius: 8px !important; }
    .main .stAlert { background-color: #262730 !important; border: 1px solid #30343f !important; color: #fafafa !important; }
    .main .streamlit-expanderHeader { background-color: #262730 !important; color: #fafafa !important; }
    .destaque { color: #ff6b35 !important; font-weight: bold; }
    .metric-positive { color: #00ff00 !important; }
    .metric-negative { color: #ff4444 !important; }
    
    /* CSS para o Chat do Agente */
    .chat-container {
        background: linear-gradient(135deg, #262730 0%, #2a2d3a 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid #30343f;
        box-shadow: 0 8px 25px rgba(14, 17, 23, 0.4);
    }
    .agent-header {
        text-align: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #ff6b35;
    }
    .chat-message-user {
        background: rgba(255, 107, 53, 0.1);
        border-left: 4px solid #ff6b35;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 10px;
    }
    .chat-message-assistant {
        background: rgba(76, 175, 80, 0.1);
        border-left: 4px solid #4caf50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DO GEMINI AI ---
@st.cache_data(show_spinner=False)
def configurar_gemini():
    """Configura a API do Gemini Pro"""
    # Configurar a API key
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    if not api_key:
        # Fallback: tentar variável de ambiente
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return None
    
    try:
        genai.configure(api_key=api_key)
        
        # Tentar versões do Gemini em ordem de preferência
        models_to_try = [
            'gemini-2.5-flash',  # Versão experimental mais recente
            'gemini-2.0-flash',        # Versão estável mais avançada
            'gemini-1.5-flash',      # Versão rápida
            'gemini-pro'             # Versão básica
        ]
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                return model
            except Exception:
                continue
        
        # Se nenhum modelo funcionar, retornar erro
        return None
        
    except Exception as e:
        st.error(f"Erro ao configurar Gemini: {e}")
        return None

# --- FUNÇÕES PARA CARREGAR DADOS ---
@st.cache_data(show_spinner=False)
def carregar_dados_dashboard():
    """Carrega todos os dados necessários para o agente especialista"""
    dados = {}
    
    # Carregar dados de saldos
    try:
        saldos_path = "1Saldos - ecossistema.xlsx"
        if os.path.exists(saldos_path):
            dados['saldos'] = pd.read_excel(saldos_path)
    except:
        dados['saldos'] = None
    
    # Carregar dados de fluxo de caixa
    try:
        fluxo_path = "2Alura - Fluxo de caixa.csv"
        if os.path.exists(fluxo_path):
            dados['fluxo'] = pd.read_csv(fluxo_path, sep=';')
    except:
        dados['fluxo'] = None
    
    # Carregar dados de meios de pagamento
    try:
        pagamentos_path = "3Streamlit - Ecossistema - Análise dos meios de pagamento.csv"
        if os.path.exists(pagamentos_path):
            dados['pagamentos'] = pd.read_csv(pagamentos_path, sep=';')
    except:
        dados['pagamentos'] = None
    
    # Carregar dados de aging
    try:
        aging_path = "4Aging.csv"
        if os.path.exists(aging_path):
            dados['aging'] = pd.read_csv(aging_path, sep=';')
    except:
        dados['aging'] = None
    
    # Carregar dados de viagens
    try:
        viagens_path = "6Viagens.csv"
        if os.path.exists(viagens_path):
            dados['viagens'] = pd.read_csv(viagens_path, sep=';')
    except:
        dados['viagens'] = None
    
    return dados

def analisar_dados_financeiros_gemini(dados, pergunta):
    """Agente especialista usando Gemini AI que analisa dados e responde perguntas"""
    
    # Configurar Gemini
    model = configurar_gemini()
    if not model:
        return """
        ⚠️ **Gemini AI não configurado**
        
        Para usar a IA do Google Gemini, você precisa:
        1. Obter uma API key em: https://ai.google.dev/
        2. Adicionar a chave em secrets.toml ou variável de ambiente GEMINI_API_KEY
        
        **Exemplo de secrets.toml:**
        ```
        GEMINI_API_KEY = "sua_chave_aqui"
        ```
        """
    
    # Preparar contexto com dados financeiros
    contexto_dados = preparar_contexto_dados(dados)
    insights_visuais = gerar_insights_visuais(dados)
    kpis_financeiros = calcular_kpis_financeiros(dados)
    
    # Combinar contextos
    contexto_completo = contexto_dados
    
    if kpis_financeiros:
        contexto_completo += "\n\n=== KPIs E BENCHMARKS DE MERCADO ===\n"
        contexto_completo += "\n".join(kpis_financeiros)
    
    if insights_visuais:
        contexto_completo += "\n\n=== PADRÕES VISUAIS E TENDÊNCIAS IDENTIFICADAS ===\n"
        contexto_completo += "\n".join(insights_visuais)
    
    # Prompt especializado para análise financeira
    prompt = f"""
    Você é um CFO experiente e especialista em análise financeira com 20+ anos no mercado brasileiro.
    
    CONTEXTO DE MERCADO:
    - Data atual: {datetime.now().strftime('%d/%m/%Y')}
    - Ambiente econômico: Brasil, mercado financeiro corporativo
    - Moeda: Real brasileiro (R$)
    
    DADOS FINANCEIROS DETALHADOS:
    {contexto_completo}
    
    PERGUNTA DO USUÁRIO: "{pergunta}"
    
    INSTRUÇÕES PARA ANÁLISE:
    1. INTERPRETAÇÃO TEMPORAL: Identifique tendências, sazonalidades e padrões de crescimento/declínio
    2. ANÁLISE COMPARATIVA: Compare períodos, identifique variações significativas
    3. CONTEXTO DE MERCADO: Relacione os dados com práticas do mercado brasileiro
    4. INSIGHTS ESTRATÉGICOS: Forneça recomendações baseadas nos dados apresentados
    5. ALERTAS DE RISCO: Identifique riscos financeiros e pontos de atenção
    6. FORMATAÇÃO: Use formato brasileiro para valores monetários
    7. LINGUAGEM: Tom executivo, técnico mas acessível
    
    ÁREAS DE FOCO:
    - Liquidez e gestão de caixa
    - Eficiência operacional
    - Gestão de riscos
    - Otimização de custos
    - Performance vs benchmarks de mercado
    - Projeções e cenários
    
    FORMATO DE RESPOSTA:
    - Use emojis para destacar pontos importantes
    - Estruture em seções quando aplicável
    - Inclua números específicos dos dados
    - Sugira ações concretas
    - Indique se precisa de dados adicionais
    
    Analise profundamente e responda como um CFO apresentando para o board:
    """
    
    try:
        # Gerar resposta com Gemini
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"""
        ❌ **Erro ao processar com Gemini AI**
        
        Erro: {str(e)}
        
        Verifique:
        - Conexão com internet
        - Validade da API key
        - Limites de uso da API
        """

def preparar_contexto_dados(dados):
    """Prepara análise aprofundada dos dados para o contexto do Gemini"""
    contexto = []
    
    # Data atual para referência
    data_atual = datetime.now()
    
    # === ANÁLISE DE SALDOS COM EVOLUÇÃO TEMPORAL ===
    if dados.get('saldos') is not None:
        df_saldos = dados['saldos']
        if not df_saldos.empty:
            contexto.append("=== ANÁLISE DE SALDOS E LIQUIDEZ ===")
            
            # Converter colunas para análise
            df_saldos_work = df_saldos.copy()
            
            # Processar datas se disponível
            if 'Data' in df_saldos_work.columns:
                try:
                    df_saldos_work['Data'] = pd.to_datetime(df_saldos_work['Data'], format='%d/%m/%Y', errors='coerce')
                    df_saldos_work = df_saldos_work.dropna(subset=['Data'])
                    df_saldos_work = df_saldos_work.sort_values('Data')
                except:
                    pass
            
            # Converter valores monetários
            if 'Saldo_Final' in df_saldos_work.columns:
                df_saldos_work['Saldo_num'] = df_saldos_work['Saldo_Final'].apply(lambda x: 
                    pd.to_numeric(str(x).replace('.', '').replace(',', '.') if isinstance(x, str) else x, errors='coerce')
                )
                df_saldos_work = df_saldos_work.dropna(subset=['Saldo_num'])
                
                if not df_saldos_work.empty:
                    saldo_total = df_saldos_work['Saldo_num'].sum()
                    contexto.append(f"• Saldo Total Atual: R$ {saldo_total:,.2f}")
                    
                    # Análise por empresa se disponível
                    if 'Empresa' in df_saldos_work.columns:
                        saldo_por_empresa = df_saldos_work.groupby('Empresa')['Saldo_num'].sum().sort_values(ascending=False)
                        contexto.append("• Distribuição por Empresa:")
                        for empresa, saldo in saldo_por_empresa.head(5).items():
                            contexto.append(f"  - {empresa}: R$ {saldo:,.2f}")
                    
                    # Evolução temporal se há dados de data
                    if 'Data' in df_saldos_work.columns and len(df_saldos_work) > 1:
                        evolucao_temporal = df_saldos_work.groupby('Data')['Saldo_num'].sum().sort_index()
                        if len(evolucao_temporal) >= 2:
                            primeiro_periodo = evolucao_temporal.iloc[0]
                            ultimo_periodo = evolucao_temporal.iloc[-1]
                            variacao = ultimo_periodo - primeiro_periodo
                            variacao_pct = (variacao / primeiro_periodo * 100) if primeiro_periodo != 0 else 0
                            
                            contexto.append(f"• Evolução Temporal:")
                            contexto.append(f"  - Período: {evolucao_temporal.index[0].strftime('%d/%m/%Y')} a {evolucao_temporal.index[-1].strftime('%d/%m/%Y')}")
                            contexto.append(f"  - Variação: R$ {variacao:,.2f} ({variacao_pct:+.1f}%)")
                            
                            # Tendência
                            if variacao > 0:
                                contexto.append("  - Tendência: CRESCIMENTO na liquidez")
                            elif variacao < 0:
                                contexto.append("  - Tendência: REDUÇÃO na liquidez")
                            else:
                                contexto.append("  - Tendência: ESTABILIDADE na liquidez")
    
    # === ANÁLISE DE FLUXO DE CAIXA COM SAZONALIDADE ===
    if dados.get('fluxo') is not None:
        df_fluxo = dados['fluxo']
        if not df_fluxo.empty and 'Valor' in df_fluxo.columns:
            contexto.append("\n=== ANÁLISE DE FLUXO DE CAIXA ===")
            
            df_fluxo_work = df_fluxo.copy()
            
            # Processar datas
            if 'Data' in df_fluxo_work.columns:
                try:
                    df_fluxo_work['Data'] = pd.to_datetime(df_fluxo_work['Data'], format='%d/%m/%Y', errors='coerce')
                    df_fluxo_work = df_fluxo_work.dropna(subset=['Data'])
                    df_fluxo_work = df_fluxo_work.sort_values('Data')
                except:
                    pass
            
            # Converter valores
            df_fluxo_work['Valor_num'] = df_fluxo_work['Valor'].apply(lambda x: 
                pd.to_numeric(str(x).replace('.', '').replace(',', '.') if isinstance(x, str) else x, errors='coerce')
            )
            df_fluxo_work = df_fluxo_work.dropna(subset=['Valor_num'])
            
            if not df_fluxo_work.empty:
                entradas = df_fluxo_work[df_fluxo_work['Valor_num'] > 0]['Valor_num'].sum()
                saidas = abs(df_fluxo_work[df_fluxo_work['Valor_num'] < 0]['Valor_num'].sum())
                fluxo_liquido = entradas - saidas
                
                contexto.append(f"• Entradas: R$ {entradas:,.2f}")
                contexto.append(f"• Saídas: R$ {saidas:,.2f}")
                contexto.append(f"• Fluxo Líquido: R$ {fluxo_liquido:,.2f}")
                
                # Análise por tipo de movimentação
                if 'Movimentação' in df_fluxo_work.columns:
                    por_tipo = df_fluxo_work.groupby('Movimentação')['Valor_num'].sum()
                    contexto.append("• Análise por Tipo de Movimentação:")
                    for tipo, valor in por_tipo.items():
                        contexto.append(f"  - {tipo}: R$ {valor:,.2f}")
                
                # Evolução mensal se há dados temporais
                if 'Data' in df_fluxo_work.columns:
                    df_fluxo_work['Mes_Ano'] = df_fluxo_work['Data'].dt.to_period('M')
                    fluxo_mensal = df_fluxo_work.groupby('Mes_Ano')['Valor_num'].sum()
                    
                    if len(fluxo_mensal) >= 2:
                        contexto.append("• Evolução Mensal (últimos períodos):")
                        for periodo, valor in fluxo_mensal.tail(3).items():
                            contexto.append(f"  - {periodo}: R$ {valor:,.2f}")
                        
                        # Tendência mensal
                        ultimo_mes = fluxo_mensal.iloc[-1]
                        penultimo_mes = fluxo_mensal.iloc[-2] if len(fluxo_mensal) >= 2 else ultimo_mes
                        variacao_mes = ultimo_mes - penultimo_mes
                        
                        if variacao_mes > 0:
                            contexto.append("  - Tendência Mensal: MELHORIA no fluxo")
                        elif variacao_mes < 0:
                            contexto.append("  - Tendência Mensal: DETERIORAÇÃO no fluxo")
                        else:
                            contexto.append("  - Tendência Mensal: ESTABILIDADE no fluxo")
    
    # === ANÁLISE DETALHADA DE MEIOS DE PAGAMENTO ===
    if dados.get('pagamentos') is not None:
        df_pagamentos = dados['pagamentos']
        if not df_pagamentos.empty:
            contexto.append("\n=== ANÁLISE DE MEIOS DE PAGAMENTO ===")
            
            df_pag_work = df_pagamentos.copy()
            
            # Processar valores originais
            if 'Valor Original' in df_pag_work.columns:
                df_pag_work['Valor_num'] = df_pag_work['Valor Original'].apply(lambda x: 
                    pd.to_numeric(str(x).replace('.', '').replace(',', '.') if isinstance(x, str) else x, errors='coerce')
                )
                df_pag_work = df_pag_work.dropna(subset=['Valor_num'])
                
                if not df_pag_work.empty:
                    volume_total = df_pag_work['Valor_num'].sum()
                    contexto.append(f"• Volume Total: R$ {volume_total:,.2f}")
                    
                    # Análise por método de pagamento
                    if 'Método de Pagamento' in df_pag_work.columns:
                        por_metodo = df_pag_work.groupby('Método de Pagamento')['Valor_num'].sum().sort_values(ascending=False)
                        contexto.append("• Volume por Método:")
                        for metodo, valor in por_metodo.head(5).items():
                            percentual = (valor / volume_total * 100) if volume_total > 0 else 0
                            contexto.append(f"  - {metodo}: R$ {valor:,.2f} ({percentual:.1f}%)")
                    
                    # Análise de custos se disponível
                    if 'Valor da taxa' in df_pag_work.columns:
                        df_pag_work['Taxa_num'] = df_pag_work['Valor da taxa'].apply(lambda x: 
                            pd.to_numeric(str(x).replace('.', '').replace(',', '.') if isinstance(x, str) else x, errors='coerce')
                        )
                        custo_total = df_pag_work['Taxa_num'].sum()
                        custo_pct = (custo_total / volume_total * 100) if volume_total > 0 else 0
                        contexto.append(f"• Custo Total: R$ {custo_total:,.2f} ({custo_pct:.2f}% do volume)")
                        
                        # Custo por método
                        if 'Método de Pagamento' in df_pag_work.columns:
                            custo_metodo = df_pag_work.groupby('Método de Pagamento').agg({
                                'Valor_num': 'sum',
                                'Taxa_num': 'sum'
                            })
                            custo_metodo['Custo_Pct'] = (custo_metodo['Taxa_num'] / custo_metodo['Valor_num'] * 100)
                            
                            contexto.append("• Custo por Método:")
                            for metodo, dados_metodo in custo_metodo.head(3).iterrows():
                                contexto.append(f"  - {metodo}: {dados_metodo['Custo_Pct']:.2f}%")
    
    # === ANÁLISE DE AGING E RECEBÍVEIS ===
    if dados.get('aging') is not None:
        df_aging = dados['aging']
        if not df_aging.empty:
            contexto.append("\n=== ANÁLISE DE CONTAS A RECEBER (AGING) ===")
            
            df_aging_work = df_aging.copy()
            
            if 'Valor' in df_aging_work.columns:
                df_aging_work['Valor_num'] = df_aging_work['Valor'].apply(lambda x: 
                    pd.to_numeric(str(x).replace('.', '').replace(',', '.') if isinstance(x, str) else x, errors='coerce')
                )
                df_aging_work = df_aging_work.dropna(subset=['Valor_num'])
                
                if not df_aging_work.empty:
                    total_receber = df_aging_work['Valor_num'].sum()
                    contexto.append(f"• Total a Receber: R$ {total_receber:,.2f}")
                    
                    # Análise por intervalo de vencimento
                    if 'Intervalo' in df_aging_work.columns:
                        por_intervalo = df_aging_work.groupby('Intervalo')['Valor_num'].sum()
                        contexto.append("• Distribuição por Vencimento:")
                        for intervalo, valor in por_intervalo.items():
                            percentual = (valor / total_receber * 100) if total_receber > 0 else 0
                            contexto.append(f"  - {intervalo} dias: R$ {valor:,.2f} ({percentual:.1f}%)")
                        
                        # Análise de risco
                        em_atraso = por_intervalo.get('31-60', 0) + por_intervalo.get('61-180', 0) + por_intervalo.get('181-360', 0) + por_intervalo.get('360+', 0)
                        if em_atraso > 0:
                            risco_pct = (em_atraso / total_receber * 100)
                            contexto.append(f"• Risco de Inadimplência: R$ {em_atraso:,.2f} ({risco_pct:.1f}%)")
    
    # === ANÁLISE DE INVESTIMENTOS ===
    if dados.get('investimentos') is not None:
        df_invest = dados['investimentos']
        if not df_invest.empty:
            contexto.append("\n=== ANÁLISE DE INVESTIMENTOS ===")
            # Adicionar análise de investimentos se os dados estiverem disponíveis
            contexto.append("• Dados de investimentos identificados (requer análise específica)")
    
    return "\n".join(contexto) if contexto else "Dados financeiros não disponíveis ou em formato incompatível"

def gerar_insights_visuais(dados):
    """Gera descrições textuais de gráficos e padrões visuais para o Gemini"""
    insights_visuais = []
    
    # === GRÁFICOS DE TENDÊNCIA ===
    if dados.get('saldos') is not None:
        df_saldos = dados['saldos']
        if not df_saldos.empty and 'Data' in df_saldos.columns and 'Saldo_Final' in df_saldos.columns:
            try:
                df_work = df_saldos.copy()
                df_work['Data'] = pd.to_datetime(df_work['Data'], format='%d/%m/%Y', errors='coerce')
                df_work['Saldo_num'] = df_work['Saldo_Final'].apply(lambda x: 
                    pd.to_numeric(str(x).replace('.', '').replace(',', '.') if isinstance(x, str) else x, errors='coerce')
                )
                df_work = df_work.dropna(subset=['Data', 'Saldo_num']).sort_values('Data')
                
                if len(df_work) >= 3:
                    # Análise de tendência visual
                    saldos_serie = df_work.groupby('Data')['Saldo_num'].sum()
                    
                    # Detectar padrões visuais
                    valores = saldos_serie.values
                    if len(valores) >= 3:
                        # Tendência geral
                        tendencia = "crescente" if valores[-1] > valores[0] else "decrescente" if valores[-1] < valores[0] else "estável"
                        
                        # Volatilidade
                        std_dev = pd.Series(valores).std()
                        media = pd.Series(valores).mean()
                        volatilidade = (std_dev / media * 100) if media != 0 else 0
                        
                        insights_visuais.append(f"GRÁFICO DE SALDOS: Tendência {tendencia}, volatilidade {volatilidade:.1f}%")
                        
                        # Pontos de inflexão
                        for i in range(1, len(valores)-1):
                            if valores[i] > valores[i-1] and valores[i] > valores[i+1]:
                                data_pico = saldos_serie.index[i].strftime('%d/%m/%Y')
                                insights_visuais.append(f"PICO identificado em {data_pico}: R$ {valores[i]:,.2f}")
                            elif valores[i] < valores[i-1] and valores[i] < valores[i+1]:
                                data_vale = saldos_serie.index[i].strftime('%d/%m/%Y')
                                insights_visuais.append(f"VALE identificado em {data_vale}: R$ {valores[i]:,.2f}")
            except:
                pass
    
    # === ANÁLISE DE DISTRIBUIÇÃO ===
    if dados.get('pagamentos') is not None:
        df_pag = dados['pagamentos']
        if not df_pag.empty and 'Método de Pagamento' in df_pag.columns and 'Valor Original' in df_pag.columns:
            try:
                df_work = df_pag.copy()
                df_work['Valor_num'] = df_work['Valor Original'].apply(lambda x: 
                    pd.to_numeric(str(x).replace('.', '').replace(',', '.') if isinstance(x, str) else x, errors='coerce')
                )
                df_work = df_work.dropna(subset=['Valor_num'])
                
                if not df_work.empty:
                    distribuicao = df_work.groupby('Método de Pagamento')['Valor_num'].sum().sort_values(ascending=False)
                    total = distribuicao.sum()
                    
                    # Concentração (Pareto)
                    top3_valor = distribuicao.head(3).sum()
                    concentracao_pct = (top3_valor / total * 100) if total > 0 else 0
                    
                    insights_visuais.append(f"GRÁFICO DE PIZZA PAGAMENTOS: Top 3 métodos concentram {concentracao_pct:.1f}% do volume")
                    
                    # Método dominante
                    if len(distribuicao) > 0:
                        metodo_principal = distribuicao.index[0]
                        participacao = (distribuicao.iloc[0] / total * 100) if total > 0 else 0
                        insights_visuais.append(f"MÉTODO DOMINANTE: {metodo_principal} representa {participacao:.1f}% do total")
            except:
                pass
    
    # === ANÁLISE DE FLUXO TEMPORAL ===
    if dados.get('fluxo') is not None:
        df_fluxo = dados['fluxo']
        if not df_fluxo.empty and 'Data' in df_fluxo.columns and 'Valor' in df_fluxo.columns:
            try:
                df_work = df_fluxo.copy()
                df_work['Data'] = pd.to_datetime(df_work['Data'], format='%d/%m/%Y', errors='coerce')
                df_work['Valor_num'] = df_work['Valor'].apply(lambda x: 
                    pd.to_numeric(str(x).replace('.', '').replace(',', '.') if isinstance(x, str) else x, errors='coerce')
                )
                df_work = df_work.dropna(subset=['Data', 'Valor_num']).sort_values('Data')
                
                if len(df_work) >= 5:
                    # Fluxo mensal
                    df_work['Mes_Ano'] = df_work['Data'].dt.to_period('M')
                    fluxo_mensal = df_work.groupby('Mes_Ano')['Valor_num'].sum()
                    
                    if len(fluxo_mensal) >= 3:
                        # Padrão sazonal
                        valores_mensais = fluxo_mensal.values
                        if len(valores_mensais) >= 3:
                            ultimo_trimestre = valores_mensais[-3:]
                            media_trimestre = np.mean(ultimo_trimestre)
                            
                            # Crescimento/declínio no trimestre
                            if ultimo_trimestre[-1] > ultimo_trimestre[0]:
                                insights_visuais.append(f"GRÁFICO FLUXO: Tendência ascendente no último trimestre")
                            elif ultimo_trimestre[-1] < ultimo_trimestre[0]:
                                insights_visuais.append(f"GRÁFICO FLUXO: Tendência descendente no último trimestre")
                            
                            # Identificar mês atípico
                            desvios = [abs(v - media_trimestre) for v in ultimo_trimestre]
                            max_desvio_idx = desvios.index(max(desvios))
                            if max(desvios) > media_trimestre * 0.2:  # Desvio > 20%
                                mes_atipico = fluxo_mensal.index[-3:][max_desvio_idx]
                                valor_atipico = ultimo_trimestre[max_desvio_idx]
                                insights_visuais.append(f"MÊS ATÍPICO identificado: {mes_atipico} com R$ {valor_atipico:,.2f}")
            except:
                pass
    
    return insights_visuais

def calcular_kpis_financeiros(dados):
    """Calcula KPIs financeiros para contextualizar a análise"""
    kpis = []
    
    try:
        # === KPIs DE LIQUIDEZ ===
        if dados.get('saldos') is not None:
            df_saldos = dados['saldos']
            if not df_saldos.empty and 'Saldo_Final' in df_saldos.columns:
                df_work = df_saldos.copy()
                df_work['Saldo_num'] = df_work['Saldo_Final'].apply(lambda x: 
                    pd.to_numeric(str(x).replace('.', '').replace(',', '.') if isinstance(x, str) else x, errors='coerce')
                )
                saldo_total = df_work['Saldo_num'].sum()
                
                # Benchmarks típicos do mercado brasileiro
                if saldo_total > 0:
                    kpis.append(f"💰 LIQUIDEZ TOTAL: R$ {saldo_total:,.2f}")
                    
                    # Classificação de liquidez (baseada em práticas de mercado)
                    if saldo_total >= 10_000_000:
                        kpis.append("🟢 CLASSIFICAÇÃO: Liquidez muito alta (>R$ 10MM)")
                    elif saldo_total >= 5_000_000:
                        kpis.append("🟡 CLASSIFICAÇÃO: Liquidez alta (R$ 5-10MM)")
                    elif saldo_total >= 1_000_000:
                        kpis.append("🟠 CLASSIFICAÇÃO: Liquidez moderada (R$ 1-5MM)")
                    else:
                        kpis.append("🔴 CLASSIFICAÇÃO: Liquidez baixa (<R$ 1MM)")
        
        # === KPIs DE FLUXO DE CAIXA ===
        if dados.get('fluxo') is not None:
            df_fluxo = dados['fluxo']
            if not df_fluxo.empty and 'Valor' in df_fluxo.columns:
                df_work = df_fluxo.copy()
                df_work['Valor_num'] = df_fluxo['Valor'].apply(lambda x: 
                    pd.to_numeric(str(x).replace('.', '').replace(',', '.') if isinstance(x, str) else x, errors='coerce')
                )
                df_work = df_work.dropna(subset=['Valor_num'])
                
                if not df_work.empty:
                    entradas = df_work[df_work['Valor_num'] > 0]['Valor_num'].sum()
                    saidas = abs(df_work[df_work['Valor_num'] < 0]['Valor_num'].sum())
                    
                    if entradas > 0 and saidas > 0:
                        # Índice de cobertura de fluxo
                        indice_cobertura = entradas / saidas
                        kpis.append(f"📊 ÍNDICE COBERTURA: {indice_cobertura:.2f}x")
                        
                        if indice_cobertura >= 1.5:
                            kpis.append("🟢 STATUS FLUXO: Muito saudável (>1.5x)")
                        elif indice_cobertura >= 1.2:
                            kpis.append("🟡 STATUS FLUXO: Saudável (1.2-1.5x)")
                        elif indice_cobertura >= 1.0:
                            kpis.append("🟠 STATUS FLUXO: Equilibrado (1.0-1.2x)")
                        else:
                            kpis.append("🔴 STATUS FLUXO: Deficitário (<1.0x)")
        
        # === KPIs DE EFICIÊNCIA DE PAGAMENTOS ===
        if dados.get('pagamentos') is not None:
            df_pag = dados['pagamentos']
            if not df_pag.empty:
                df_work = df_pag.copy()
                
                if 'Valor Original' in df_work.columns and 'Valor da taxa' in df_work.columns:
                    df_work['Valor_num'] = df_work['Valor Original'].apply(lambda x: 
                        pd.to_numeric(str(x).replace('.', '').replace(',', '.') if isinstance(x, str) else x, errors='coerce')
                    )
                    df_work['Taxa_num'] = df_work['Valor da taxa'].apply(lambda x: 
                        pd.to_numeric(str(x).replace('.', '').replace(',', '.') if isinstance(x, str) else x, errors='coerce')
                    )
                    
                    volume_total = df_work['Valor_num'].sum()
                    custo_total = df_work['Taxa_num'].sum()
                    
                    if volume_total > 0:
                        custo_pct = (custo_total / volume_total) * 100
                        kpis.append(f"💳 CUSTO TRANSACIONAL: {custo_pct:.2f}%")
                        
                        # Benchmarks de mercado brasileiro
                        if custo_pct <= 2.0:
                            kpis.append("🟢 EFICIÊNCIA: Excelente (<2.0%)")
                        elif custo_pct <= 3.5:
                            kpis.append("🟡 EFICIÊNCIA: Boa (2.0-3.5%)")
                        elif custo_pct <= 5.0:
                            kpis.append("🟠 EFICIÊNCIA: Regular (3.5-5.0%)")
                        else:
                            kpis.append("🔴 EFICIÊNCIA: Baixa (>5.0%)")
        
    except Exception as e:
        kpis.append(f"⚠️ Erro no cálculo de KPIs: {str(e)}")
    
    return kpis

# Função legacy mantida como backup
def analisar_dados_financeiros(dados, pergunta):
    """Agente especialista que analisa dados e responde perguntas"""
    
    # Análises avançadas dos dados carregados
    insights = []
    metricas_calculadas = {}
    
    # Análise de Saldos
    if dados.get('saldos') is not None:
        df_saldos = dados['saldos']
        if not df_saldos.empty and 'Saldo_Final' in df_saldos.columns:
            saldo_total = df_saldos['Saldo_Final'].sum()
            insights.append(f"💰 **Saldo Total do Ecossistema**: R$ {saldo_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            metricas_calculadas['saldo_total'] = saldo_total
            
            if 'Empresa' in df_saldos.columns:
                saldo_por_empresa = df_saldos.groupby('Empresa')['Saldo_Final'].sum()
                maior_saldo = saldo_por_empresa.max()
                empresa_maior_saldo = saldo_por_empresa.idxmax()
                insights.append(f"🏢 **Maior Concentração**: {empresa_maior_saldo} com R$ {maior_saldo:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # Análise de Fluxo de Caixa
    if dados.get('fluxo') is not None:
        df_fluxo = dados['fluxo']
        if not df_fluxo.empty and 'Valor' in df_fluxo.columns:
            # Converter coluna Valor para numérico, tratando strings com formato brasileiro
            df_fluxo_copy = df_fluxo.copy()
            df_fluxo_copy['Valor_num'] = df_fluxo_copy['Valor'].apply(lambda x: 
                pd.to_numeric(str(x).replace('.', '').replace(',', '.') if isinstance(x, str) else x, errors='coerce')
            )
            df_fluxo_copy = df_fluxo_copy.dropna(subset=['Valor_num'])
            
            if not df_fluxo_copy.empty:
                entradas = df_fluxo_copy[df_fluxo_copy['Valor_num'] > 0]['Valor_num'].sum()
                saidas = abs(df_fluxo_copy[df_fluxo_copy['Valor_num'] < 0]['Valor_num'].sum())
                fluxo_liquido = entradas - saidas
                insights.append(f"📊 **Fluxo Líquido**: R$ {fluxo_liquido:,.2f} (Entradas: R$ {entradas:,.2f} | Saídas: R$ {saidas:,.2f})".replace(',', 'X').replace('.', ',').replace('X', '.'))
                metricas_calculadas['fluxo_liquido'] = fluxo_liquido
                metricas_calculadas['entradas'] = entradas
                metricas_calculadas['saidas'] = saidas
    
    # Análise de Meios de Pagamento
    if dados.get('pagamentos') is not None:
        df_pagamentos = dados['pagamentos']
        if not df_pagamentos.empty and 'Valor Original' in df_pagamentos.columns:
            # Converter valores para numérico
            df_pagamentos_copy = df_pagamentos.copy()
            df_pagamentos_copy['Valor_num'] = df_pagamentos_copy['Valor Original'].apply(lambda x: 
                pd.to_numeric(str(x).replace('.', '').replace(',', '.') if isinstance(x, str) else x, errors='coerce')
            )
            df_pagamentos_copy = df_pagamentos_copy.dropna(subset=['Valor_num'])
            
            if not df_pagamentos_copy.empty:
                volume_total = df_pagamentos_copy['Valor_num'].sum()
                insights.append(f"💳 **Volume de Pagamentos**: R$ {volume_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                
                if 'Método de Pagamento' in df_pagamentos_copy.columns:
                    metodo_volumes = df_pagamentos_copy.groupby('Método de Pagamento')['Valor_num'].sum()
                    if not metodo_volumes.empty:
                        top_metodo = metodo_volumes.idxmax()
                        insights.append(f"🥇 **Principal Meio**: {top_metodo}")
    
    # Respostas especializadas baseadas na pergunta
    pergunta_lower = pergunta.lower()
    
    if any(palavra in pergunta_lower for palavra in ['liquidez', 'saldo', 'disponível', 'caixa']):
        resposta = f"""
## 💧 **ANÁLISE DE LIQUIDEZ E POSIÇÃO DE CAIXA**

**📊 Situação Atual:**
{f"• Posição total de caixa: R$ {metricas_calculadas.get('saldo_total', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if 'saldo_total' in metricas_calculadas else "• Dados de saldo não disponíveis"}
• Status de liquidez: {'✅ SAUDÁVEL' if metricas_calculadas.get('saldo_total', 0) > 0 else '⚠️ ATENÇÃO NECESSÁRIA'}

**🎯 Impacto na Tesouraria:**
- **Liquidez Imediata**: Os saldos representam {metricas_calculadas.get('saldo_total', 0)/1000000:.1f}M em disponibilidades
- **Gestão de Float**: Otimização entre contas pode gerar ganhos adicionais de 0.5-1% ao mês
- **Reserva de Segurança**: Recomendado manter 15-30 dias de despesas operacionais

**📈 Recomendações Estratégicas:**
1. **Monitoramento Diário**: Implementar cash pooling para maximizar rendimentos
2. **Aplicações Automáticas**: Sweep accounts para saldos acima de R$ 100.000
3. **Limites Dinâmicos**: Ajustar reservas conforme sazonalidade do negócio
4. **Benchmark de Mercado**: Taxa atual DI está em ~11.75% a.a.

**⚡ Ações Imediatas:**
- Negociar remuneração de conta corrente acima de 90% do CDI
- Implementar aplicação automática em CDB/RDB de liquidez diária
- Revisar limites de conta corrente para reduzir custos de permanência
        """
    
    elif any(palavra in pergunta_lower for palavra in ['fluxo', 'entrada', 'saída', 'cash flow']):
        resposta = f"""
## 📊 **ANÁLISE DE FLUXO DE CAIXA**

**📈 Performance Atual:**
{f"• Fluxo líquido: R$ {metricas_calculadas.get('fluxo_liquido', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if 'fluxo_liquido' in metricas_calculadas else "• Dados de fluxo não disponíveis"}
{f"• Taxa de conversão: {(metricas_calculadas.get('entradas', 1) / (metricas_calculadas.get('entradas', 1) + metricas_calculadas.get('saidas', 0)) * 100):.1f}% entradas vs saídas" if 'entradas' in metricas_calculadas else ""}

**🎯 Impacto na Tesouraria:**
- **Previsibilidade**: Base para projeções de 13 semanas rolling forecast
- **Working Capital**: Otimização do ciclo operacional e financeiro
- **Funding Strategy**: Definição de necessidades de crédito vs investimento

**� Insights Estratégicos:**
1. **Aceleração de Recebimentos**: Implementar desconto para pagamento antecipado
2. **Otimização de Pagamentos**: Aproveitamento máximo de prazos de fornecedores
3. **Hedge Natural**: Matching de moedas em operações internacionais
4. **Cash Forecasting**: Modelo de previsão com acurácia >95% em 4 semanas

**🚀 Oportunidades Identificadas:**
- Negociação de D+0 com bancos adquirentes principais
- Implementação de PIX corporativo para reduzir float
- Antecipação de recebíveis com custo < 1.5% a.m.
- Concentração bancária para melhor poder de negociação
        """
    
    elif any(palavra in pergunta_lower for palavra in ['pagamento', 'método', 'cartão', 'pix']):
        resposta = """
## 💳 **ANÁLISE DE MEIOS DE PAGAMENTO**

**🎯 Impacto na Tesouraria:**
- **Custo Total**: Cartão de crédito (2.5-3.5%) vs PIX (R$ 0.60 por transação)
- **Timing de Recebimento**: PIX (D+0) vs Cartão (D+1 a D+30)
- **Negociação Bancária**: Volume consolidado aumenta poder de barganha em 15-25%

**� Análise Estratégica por Modalidade:**

**🏆 PIX Corporativo:**
- Custo: R$ 0.60 por transação (limitado a R$ 20.000)
- Liquidação: Instantânea (D+0)
- Recomendação: Incentivar para valores menores

**💳 Cartão de Débito:**
- Custo médio: 1.2-1.8%
- Liquidação: D+1
- Estratégia: Alternativa ao PIX para valores maiores

**💎 Cartão de Crédito:**
- Custo médio: 2.5-3.5%
- Liquidação: D+1 (crédito) / D+30 (parcelado)
- Gestão: Negociar antecipação com desconto

**💡 Otimizações Recomendadas:**
1. **Mix Inteligente**: 40% PIX, 30% débito, 30% crédito
2. **Incentivos**: Desconto 1% para PIX e débito
3. **Concentração**: Consolidar em 2-3 adquirentes principais
4. **Antecipação Seletiva**: Apenas para cartão parcelado >R$ 500
        """
    
    elif any(palavra in pergunta_lower for palavra in ['receber', 'aging', 'inadimplência', 'atraso']):
        resposta = """
## 📈 **ANÁLISE DE CONTAS A RECEBER**

**🎯 KPIs Críticos para Tesouraria:**
- **DSO (Days Sales Outstanding)**: Meta < 30 dias
- **Collection Rate**: Meta > 98% em 90 dias
- **Bad Debt**: Meta < 0.5% da receita bruta

**🔍 Gestão de Risco Estratégica:**

**📊 Aging Benchmark:**
- **0-30 dias**: 85-90% do total (Saudável)
- **31-60 dias**: 5-8% (Atenção)
- **61-90 dias**: 2-3% (Cobrança intensiva)
- **>90 dias**: <2% (Provisão 100%)

**💰 Impacto Financeiro:**
1. **Custo de Oportunidade**: Cada dia de atraso = 0.033% de CDI perdido
2. **Provisão IFRS**: Expectativa de perda vs fluxo de caixa
3. **Working Capital**: Impacto direto na necessidade de financiamento

**🚀 Ações Estratégicas:**
- **Cobrança Preventiva**: D-5 do vencimento
- **Scoring Dinâmico**: Análise preditiva de inadimplência
- **Seguro de Crédito**: Proteção para clientes >R$ 100K
- **Factoring Seletivo**: APR < 18% a.a. para clientes AAA
        """
    
    elif any(palavra in pergunta_lower for palavra in ['investimento', 'rendimento', 'cdi', 'aplicação']):
        resposta = f"""
## � **ANÁLISE DE INVESTIMENTOS**

**🎯 Benchmark Atual (CDI: 11.75% a.a.):**
- **Meta de Performance**: CDI + 0.5% a 1.5%
- **Liquidez**: Escalonamento D+0, D+1, D+30, D+90
- **Diversificação**: Máximo 30% por emissor/grupo econômico

**📊 Estrutura Recomendada para Tesouraria:**

**🔥 Alta Liquidez (40% da carteira):**
- CDB DI Liquidez Diária: CDI-0.5% a CDI+0.2%
- Tesouro Selic: CDI-0.1% (sem risco de crédito)
- Fundos DI Corporativos: CDI+0.3% a CDI+0.8%

**⚡ Média Liquidez (35% da carteira):**
- CDB 90 dias: CDI+0.8% a CDI+1.2%
- LCA/LCI: CDI+0.5% a CDI+1.0% (isenção IR)
- Debêntures Bancárias: CDI+1.5% a CDI+2.5%

**� Estratégica (25% da carteira):**
- CRI/CRA: CDI+2.0% a CDI+4.0%
- Fundos Multimercado: Objetivo CDI+3% a 5%
- Tesouro IPCA+: Proteção inflacionária

**🧮 Cálculo de Performance:**
{f"Com R$ {metricas_calculadas.get('saldo_total', 1000000):,.0f} investidos:".replace(',', 'X').replace('.', ',').replace('X', '.') if 'saldo_total' in metricas_calculadas else "Com R$ 1.000.000 investidos:"}
- **Poupança** (6.17% a.a.): R$ {(metricas_calculadas.get('saldo_total', 1000000) * 0.0617 / 12):,.0f}/mês
- **CDI 100%** (11.75% a.a.): R$ {(metricas_calculadas.get('saldo_total', 1000000) * 0.1175 / 12):,.0f}/mês
- **CDI+1%** (12.75% a.a.): R$ {(metricas_calculadas.get('saldo_total', 1000000) * 0.1275 / 12):,.0f}/mês

**⚡ Ações Imediatas:**
- Migrar da poupança para CDB DI (ganho de 5.58% a.a.)
- Implementar ladder de vencimentos para otimizar liquidez
- Negociar isenção de taxa de administração em fundos
        """.replace(',', 'X').replace('.', ',').replace('X', '.')
    
    elif any(palavra in pergunta_lower for palavra in ['cenário', 'risco', 'stress', 'contingência']):
        resposta = """
## ⚠️ **ANÁLISE DE CENÁRIOS E GESTÃO DE RISCOS**

**🎯 Stress Testing para Tesouraria:**

**📉 Cenário Pessimista (-20% receitas):**
- Redução de caixa operacional: 15-25%
- Necessidade de crédito adicional: R$ 500K-1M
- Ações: Corte de CAPEX, negociação de prazos

**📊 Cenário Base (atual):**
- Manutenção da operação
- Otimização contínua de processos
- Investimento em crescimento controlado

**📈 Cenário Otimista (+20% receitas):**
- Excesso de caixa: Oportunidade de investimento
- Expansão de operações
- Melhoria de rating de crédito

**�️ Plano de Contingência:**
1. **Linha de Crédito Stand-by**: R$ 2M pré-aprovados
2. **Reserva Estratégica**: 60 dias de despesas fixas
3. **Antecipação de Recebíveis**: Última instância com custo <2% a.m.
4. **Asset Light**: Redução de estoques e imobilizado

**📱 Monitoramento Contínuo:**
- Cash burn rate semanal
- Covenant compliance mensal
- Stress test trimestral
- Revisão de políticas semestral
        """
    
    else:
        resposta = f"""
## 🧠 **ANÁLISE FINANCEIRA INTEGRADA - VISÃO 360°**

**📊 Dashboard de Indicadores Chave:**
{f"• **Liquidez Total**: R$ {metricas_calculadas.get('saldo_total', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if 'saldo_total' in metricas_calculadas else "• Liquidez: Dados não disponíveis"}
{f"• **Fluxo Operacional**: R$ {metricas_calculadas.get('fluxo_liquido', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if 'fluxo_liquido' in metricas_calculadas else "• Fluxo: Dados não disponíveis"}
• **Status Geral**: {'🟢 OPERAÇÃO NORMAL' if metricas_calculadas.get('saldo_total', 0) > 0 and metricas_calculadas.get('fluxo_liquido', 0) > 0 else '🟡 ATENÇÃO REQUERIDA' if metricas_calculadas.get('saldo_total', 0) > 0 else '🔴 AÇÃO URGENTE'}

**🎯 Áreas para Perguntas Específicas:**

**💧 Gestão de Liquidez:**
- "Como otimizar nossa posição de caixa?"
- "Qual a estrutura ideal de investimentos?"
- "Como implementar cash pooling?"

**📊 Fluxo de Caixa:**
- "Como melhorar nosso cash conversion cycle?"
- "Qual estratégia para aceleração de recebimentos?"
- "Como otimizar prazos de pagamento?"

**💳 Meios de Pagamento:**
- "Qual o mix ideal de meios de pagamento?"
- "Como reduzir custos de transação?"
- "Estratégia de negociação com adquirentes?"

**📈 Contas a Receber:**
- "Como reduzir inadimplência?"
- "Estratégia de cobrança eficiente?"
- "Análise de aging e provisões?"

**🚀 Investimentos:**
- "Onde aplicar excedentes de caixa?"
- "Como diversificar sem perder liquidez?"
- "Análise de performance vs benchmark?"

**⚡ Análises Avançadas Disponíveis:**
- Stress testing de cenários
- Otimização de capital de giro  
- Hedging de riscos financeiros
- Planejamento tributário
        """
    
    # Adicionar insights específicos se houver dados
    if insights:
        resposta += "\n\n**📋 Métricas Atuais Identificadas:**\n" + "\n".join(f"- {insight}" for insight in insights)
    
    return resposta

# --- SIDEBAR COM LOGO ALUN ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 15px; margin-bottom: 2rem;">
        <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQwIiB2aWV3Qm94PSIwIDAgMTAwIDQwIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8dGV4dCB4PSI1MCIgeT0iMjUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyNCIgZm9udC13ZWlnaHQ9ImJvbGQiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5BTFVOPC90ZXh0Pgo8L3N2Zz4K" style="width: 120px; height: auto;">
        <div style="color: #ccc; font-size: 12px; margin-top: 10px;">Dashboard Financeiro</div>
    </div>
    """, unsafe_allow_html=True)

# --- HEADER APRIMORADO ---
st.markdown("""
<div style="text-align: center; margin-bottom: 3rem; padding: 3rem 2rem; background: linear-gradient(135deg, #262730 0%, #2a2d3a 100%); border-radius: 25px; box-shadow: 0 8px 32px rgba(14, 17, 23, 0.4);">
    <h1 style="color: #fafafa; font-weight: 700; margin-bottom: 1rem; font-size: 3rem; text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);">📊 Dashboard Financeiro ALUN</h1>
    <p style="color: #ff6b35; font-size: 1.3em; font-weight: 500; text-shadow: 0 0 15px rgba(255, 107, 53, 0.3);">Análise Integrada dos Indicadores Financeiros</p>
    <div style="margin-top: 2rem; padding: 1rem; background: rgba(255, 107, 53, 0.1); border-radius: 15px; border-left: 4px solid #ff6b35;">
        <p style="color: #ccc; margin: 0; font-size: 1rem; line-height: 1.6;">
            🎯 <strong>Bem-vindo!</strong> Navegue pelas páginas para explorar análises detalhadas de saldos, fluxo de caixa, 
            meios de pagamento, contas a receber e pagar, além do desempenho dos investimentos.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- AGENTE ESPECIALISTA EM FINANÇAS E TESOURARIA ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

st.markdown("""
<div class="agent-header">
    <h2 style="color: #ff6b35; margin-bottom: 0.5rem;">🤖 FinanceBot - Especialista em Tesouraria</h2>
    <p style="color: #ccc; margin: 0; font-size: 1.1rem;">
        Analista Financeiro Digital | Especialista em Cash Management & Treasury
    </p>
</div>
""", unsafe_allow_html=True)

# Carregar dados para o agente
dados_dashboard = carregar_dados_dashboard()

# Interface do chat
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'pergunta_selecionada' not in st.session_state:
    st.session_state.pergunta_selecionada = ""

# Campo de pergunta
col1, col2 = st.columns([4, 1])

with col1:
    # Se uma pergunta foi selecionada, usar ela como valor padrão
    valor_inicial = st.session_state.pergunta_selecionada if st.session_state.pergunta_selecionada else ""
    pergunta_usuario = st.text_input(
        "💬 Faça sua pergunta sobre finanças e tesouraria:",
        placeholder="Ex: Como está nossa liquidez? Qual o impacto dos meios de pagamento no fluxo de caixa?",
        value=valor_inicial,
        key="pergunta_input"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Espaçamento
    if st.button("🚀 Analisar", type="primary", use_container_width=True):
        if pergunta_usuario.strip():
            # Verificar se Gemini está configurado
            model = configurar_gemini()
            if not model:
                st.error("❌ Configure a API Key do Google Gemini nos secrets do Streamlit para usar o FinanceBot.")
                st.info("💡 Adicione 'GEMINI_API_KEY' nos secrets da aplicação.")
            else:
                # Adicionar pergunta ao histórico
                st.session_state.chat_history.append({
                    "tipo": "user",
                    "mensagem": pergunta_usuario,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                
                # Gerar resposta do agente usando Gemini AI
                resposta = analisar_dados_financeiros_gemini(dados_dashboard, pergunta_usuario)
                
                # Adicionar resposta ao histórico
                st.session_state.chat_history.append({
                    "tipo": "assistant",
                    "mensagem": resposta,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                
                # Limpar pergunta selecionada
                st.session_state.pergunta_selecionada = ""
                st.rerun()
        else:
            st.warning("⚠️ Digite sua pergunta para continuar.")

# Exibir histórico do chat
if st.session_state.chat_history:
    st.markdown("### 💬 Histórico da Conversa")
    
    for i, mensagem in enumerate(reversed(st.session_state.chat_history[-6:])):  # Últimas 6 mensagens
        if mensagem["tipo"] == "user":
            st.markdown(f"""
            <div class="chat-message-user">
                <strong>🧑‍💼 Você ({mensagem['timestamp']}):</strong><br>
                {mensagem['mensagem']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message-assistant">
                <strong>🤖 FinanceBot ({mensagem['timestamp']}):</strong>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(mensagem['mensagem'])

    # Botão para limpar histórico
    if st.button("🗑️ Limpar Conversa", type="secondary"):
        st.session_state.chat_history = []
        st.rerun()

else:
    # Mensagem de boas-vindas do agente
    st.markdown("""
    <div class="chat-message-assistant">
        <strong>🤖 FinanceBot (Powered by Google Gemini AI):</strong><br><br>
        Olá! Sou seu especialista em finanças e tesouraria. Posso analisar todos os dados da sua dashboard e fornecer insights estratégicos sobre:
        <br><br>
        <strong>🎯 Áreas de Especialidade:</strong><br>
        • 💰 <strong>Gestão de Liquidez</strong> - Análise de saldos e disponibilidades<br>
        • 📊 <strong>Fluxo de Caixa</strong> - Projeções e otimização de entradas/saídas<br>
        • 💳 <strong>Meios de Pagamento</strong> - Custos, prazos e negociação bancária<br>
        • 📈 <strong>Contas a Receber</strong> - Aging, cobrança e gestão de crédito<br>
        • 📉 <strong>Contas a Pagar</strong> - Otimização de prazos e relacionamentos<br>
        • 🚀 <strong>Investimentos</strong> - Performance e alocação de excedentes<br>
    </div>
    """, unsafe_allow_html=True)
    
    # Perguntas sugeridas
    st.markdown("#### 💡 Perguntas Sugeridas:")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        if st.button("💰 Como otimizar nossa liquidez?", use_container_width=True):
            st.session_state.pergunta_selecionada = "Como otimizar nossa liquidez?"
            st.rerun()
            
        if st.button("📊 Análise do fluxo de caixa", use_container_width=True):
            st.session_state.pergunta_selecionada = "Como está nosso fluxo de caixa?"
            st.rerun()
    
    with col_p2:
        if st.button("💳 Estratégia de meios de pagamento", use_container_width=True):
            st.session_state.pergunta_selecionada = "Qual a melhor estratégia para meios de pagamento?"
            st.rerun()
            
        if st.button("📈 Gestão de recebimentos", use_container_width=True):
            st.session_state.pergunta_selecionada = "Como melhorar nossa gestão de contas a receber?"
            st.rerun()
    
    with col_p3:
        if st.button("🚀 Performance dos investimentos", use_container_width=True):
            st.session_state.pergunta_selecionada = "Como estão nossos investimentos vs CDI?"
            st.rerun()
            
        if st.button("⚠️ Análise de cenários e riscos", use_container_width=True):
            st.session_state.pergunta_selecionada = "Faça uma análise de cenários de risco"
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
