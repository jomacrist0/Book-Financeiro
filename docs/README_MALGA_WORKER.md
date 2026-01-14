# 🚀 Malga Payment Analytics - Arquitetura Otimizada

## 📋 Visão Geral

Sistema de análise de aprovação de pagamentos Malga com arquitetura Worker + Data Mart para performance otimizada:

```
API Malga → Worker (APScheduler) → SQLite → Dashboard Streamlit
```

## 🏗️ Arquitetura

### Componentes

1. **config.py**: Configurações centralizadas (API, banco, constantes)
2. **malga_database.py**: Gerenciamento do banco SQLite com agregações
3. **malga_worker.py**: Worker de background que sincroniza a cada 1 minuto
4. **start_worker.py**: Script de inicialização do worker
5. **pages/Aprovação_Malga_Otimizada.py**: Dashboard Streamlit otimizado

### Fluxo de Dados

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  API Malga  │─────▶│   Worker    │─────▶│   SQLite    │─────▶│  Dashboard  │
│  (Charges)  │      │ (1 minuto)  │      │  (Data Mart)│      │ (Streamlit) │
└─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘
                            │                     │
                            │                     │
                            ▼                     ▼
                     ┌─────────────┐      ┌─────────────┐
                     │   Logging   │      │  Métricas   │
                     │ (worker.log)│      │ Agregadas   │
                     └─────────────┘      └─────────────┘
```

## 🗄️ Estrutura do Banco de Dados

### Tabelas

1. **transactions**: Cache bruto das transações da API
2. **metrics_by_minute**: Métricas agregadas por minuto
3. **metrics_by_hour**: Métricas agregadas por hora
4. **metrics_by_day**: Métricas agregadas por dia
5. **sync_control**: Controle de sincronização

### Métricas Calculadas

- Taxa de aprovação
- Volume total e por status
- Contadores por método de pagamento
- Contadores por bandeira de cartão
- Distribuição por status

## 🚀 Como Usar

### 1. Instalação de Dependências

```bash
pip install -r requirements.txt
```

**Pacotes necessários:**
- streamlit
- pandas
- plotly
- requests
- apscheduler
- pytz
- openpyxl (para outros dashboards)

### 2. Configuração

Edite `config.py` com suas credenciais Malga:

```python
MALGA_CLIENT_ID = "seu-client-id"
MALGA_CLIENT_SECRET = "sua-api-key"
```

### 3. Iniciar o Worker

**Windows (PowerShell):**
```powershell
python start_worker.py
```

**Linux/Mac:**
```bash
python start_worker.py
```

O worker irá:
- ✅ Criar banco de dados SQLite automaticamente
- ✅ Buscar transações da API Malga
- ✅ Processar e agregar dados a cada 1 minuto
- ✅ Gerar logs em `worker.log`

### 4. Iniciar o Dashboard

Em outro terminal:

```powershell
streamlit run Pagina_inicial.py
```

Acesse a página **"⚡ Aprovação Malga - Otimizada"** no menu lateral.

## 📊 Funcionalidades do Dashboard

### Métricas Globais
- Total de transações
- Transações aprovadas/reprovadas
- Taxa de aprovação média
- Volume financeiro total

### Análises Disponíveis

1. **📈 Evolução Temporal**
   - Gráfico de linha com taxa de aprovação
   - Volume de transações ao longo do tempo
   - Granularidade: minuto, hora ou dia

2. **💳 Por Método de Pagamento**
   - Distribuição por método (Pix, Credit Card, etc.)
   - Taxa de aprovação por método
   - Volume financeiro detalhado

3. **🏦 Por Bandeira**
   - Análise de bandeiras de cartão (Visa, Mastercard, etc.)
   - Comparação de performance entre bandeiras

4. **📊 Análise de Status**
   - Distribuição de transações por status
   - Identificação de principais motivos de falha

### Filtros
- 📅 Data inicial/final
- 📊 Granularidade (minuto/hora/dia)
- 🔍 Exibição de transações detalhadas

## ⚙️ Parâmetros de Configuração

### Sincronização (config.py)

```python
SYNC_INTERVAL_MINUTES = 1  # Intervalo de sincronização
MAX_TRANSACTIONS_PER_SYNC = 1000  # Limite por sincronização
MAX_API_PAGES = 50  # Máximo de páginas da API
API_TIMEOUT = 30  # Timeout das requisições
```

### Períodos de Agregação

- **Por minuto**: Análise em tempo quase real
- **Por hora**: Visão agregada de curto prazo
- **Por dia**: Análise de tendências

## 📈 Vantagens da Arquitetura

### Performance
- ⚡ **Dashboard carrega em milissegundos** (vs. segundos com API direta)
- 🔄 Dados sempre atualizados (sincronização a cada 1 minuto)
- 📊 Métricas pré-calculadas (zero processamento no dashboard)

### Escalabilidade
- 💾 Banco local SQLite (sem limite de consultas)
- 📈 Suporta milhões de transações
- 🔁 Agregações incrementais eficientes

### Confiabilidade
- 🛡️ Desacoplamento entre API e dashboard
- 📝 Logs detalhados para troubleshooting
- ♻️ Retry automático em caso de falha

### Custos
- 💰 Redução de chamadas à API (1 chamada/minuto vs. milhares)
- 🔌 Funciona offline após sincronização inicial
- 📉 Menor custo operacional

## 🔧 Troubleshooting

### Worker não inicia
```bash
# Verifique dependências
python -c "import apscheduler, requests, pandas; print('OK')"

# Verifique permissões do banco
ls -l malga_datamart.db
```

### Dashboard não mostra dados
1. Verifique se o worker está rodando
2. Confira o arquivo `worker.log`
3. Veja status na sidebar do dashboard

### Erro de autenticação API
- Verifique credenciais em `config.py`
- Teste manualmente:
```python
import requests
headers = {
    "X-Client-Id": "seu-id",
    "X-Api-Key": "sua-key"
}
r = requests.get("https://api.malga.io/v1/charges?limit=1", headers=headers)
print(r.status_code)  # Deve ser 200
```

## 📝 Logs

O worker gera logs em `worker.log`:

```
2025-01-30 14:35:00 - INFO - 🚀 Iniciando sincronização...
2025-01-30 14:35:01 - INFO - ✅ Autenticação bem-sucedida
2025-01-30 14:35:02 - INFO - 📄 Página 1: 100 transações
2025-01-30 14:35:03 - INFO - ✅ Total de 250 transações coletadas
2025-01-30 14:35:04 - INFO - ✅ 250 transações processadas
2025-01-30 14:35:05 - INFO - 💾 Inserindo transações no banco...
2025-01-30 14:35:06 - INFO - 📊 Iniciando agregações...
2025-01-30 14:35:07 - INFO - ✅ Sincronização concluída: 250 transações
```

## 🔒 Segurança

- ⚠️ **Nunca comite `config.py` com credenciais reais**
- 🔐 Use variáveis de ambiente para produção
- 🛡️ Mantenha `malga_datamart.db` fora do controle de versão

## 📚 Estrutura de Arquivos

```
Book Financeiro - Streamlit/
├── config.py                          # Configurações centralizadas
├── malga_database.py                  # Gerenciamento do banco SQLite
├── malga_worker.py                    # Worker de background
├── start_worker.py                    # Script de inicialização
├── requirements.txt                   # Dependências Python
├── malga_datamart.db                  # Banco SQLite (gerado automaticamente)
├── worker.log                         # Logs do worker (gerado automaticamente)
├── Pagina_inicial.py                  # Página inicial Streamlit
└── pages/
    ├── Aprovação_Malga_Otimizada.py   # Dashboard otimizado ⚡
    └── ...outros dashboards...
```

## 🎯 Próximos Passos

### Melhorias Sugeridas

1. **Alertas automáticos**
   - Notificações quando taxa de aprovação cai
   - Alertas de falhas críticas

2. **Machine Learning**
   - Predição de aprovação
   - Detecção de anomalias

3. **Exportação de dados**
   - Relatórios automáticos em PDF
   - Integração com BI tools

4. **Dashboard adicional**
   - Análise de motivos de recusa
   - Comparação entre períodos

## 🤝 Contribuindo

Para adicionar novas funcionalidades:

1. Modifique `malga_database.py` para novas agregações
2. Atualize `malga_worker.py` se precisar de novos campos
3. Edite `pages/Aprovação_Malga_Otimizada.py` para novos gráficos

## 📄 Licença

Este projeto faz parte do livro "Streamlit e BI" - ALURA Group.

---

**Desenvolvido com ❤️ usando Streamlit + SQLite + APScheduler**
