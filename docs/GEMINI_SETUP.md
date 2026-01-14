# 🤖 FinanceBot com Google Gemini AI

O FinanceBot agora usa inteligência artificial do Google Gemini para fornecer análises financeiras mais avançadas e personalizadas.

## 🔑 Como Configurar a API Key do Gemini

### 1. Obter API Key Gratuita
1. Acesse: https://ai.google.dev/
2. Faça login com sua conta Google
3. Clique em "Get API Key"
4. Crie um novo projeto (se necessário)
5. Copie sua API key

### 2. Configurar no Aplicativo

#### Opção 1: Via Interface (Recomendado)
1. Abra o aplicativo Streamlit
2. Na barra lateral, cole sua API key no campo "Gemini API Key"
3. A configuração será aplicada imediatamente

#### Opção 2: Via Arquivo secrets.toml
1. Edite o arquivo `.streamlit/secrets.toml`
2. Descomente e adicione sua chave:
```toml
GEMINI_API_KEY = "sua_chave_aqui"
```

#### Opção 3: Via Variável de Ambiente
```bash
set GEMINI_API_KEY=sua_chave_aqui
```

## 🚀 Funcionalidades da IA

- **Análise Inteligente**: Processamento avançado dos dados financeiros
- **Respostas Personalizadas**: Adaptadas ao contexto específico dos seus dados
- **Linguagem Natural**: Faça perguntas como se estivesse falando com um CFO
- **Insights Estratégicos**: Recomendações baseadas em melhores práticas do mercado

## 📊 Modelos Suportados

O sistema tenta usar automaticamente a melhor versão disponível:
1. `gemini-2.0-flash-exp` (Experimental - mais recente)
2. `gemini-1.5-pro` (Estável - mais avançado)
3. `gemini-1.5-flash` (Rápido)
4. `gemini-pro` (Básico)

## 🔒 Segurança

- Suas chaves API são armazenadas localmente
- Os dados financeiros são processados apenas durante a sessão
- Nenhum dado sensível é armazenado permanentemente

## 💡 Dicas de Uso

**Exemplos de perguntas otimizadas:**
- "Analise nossa posição de liquidez e sugira melhorias"
- "Qual estratégia você recomenda para otimizar nosso fluxo de caixa?"
- "Como podemos reduzir custos nos meios de pagamento?"
- "Avalie o risco da nossa carteira de investimentos"

---

🎯 **Resultado**: Análises financeiras profissionais com o poder da IA do Google!
