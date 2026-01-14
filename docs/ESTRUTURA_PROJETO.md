# 🗂️ Nova Estrutura do Projeto - Reorganizado

## 📁 Estrutura de Pastas

```
Book Financeiro - Streamlit/
│
├── 📂 data/                          # ✨ NOVO: Todos os arquivos de dados
│   ├── *.csv                         # Arquivos CSV de dados
│   ├── *.xlsx                        # Planilhas Excel
│   └── malga_datamart.db             # Banco SQLite do worker
│
├── 📂 worker/                        # ✨ NOVO: Sistema de Worker
│   ├── config.py                     # Configurações (CHAVES ATUALIZADAS)
│   ├── malga_database.py             # Gerenciamento SQLite
│   ├── malga_worker.py               # Worker de sincronização
│   └── start_worker.py               # Script de inicialização
│
├── 📂 pages/                         # Páginas do Streamlit
│   ├── 1Saldos_do_Ecossistema.py
│   ├── 2Fluxo_de_caixa.py
│   ├── 3Meios_de_pagamento.py
│   ├── 4Contas_a_Receber.py
│   ├── 5Contas_a_pagar.py
│   ├── 6Investimentos.py
│   ├── Aprovação_Malga_Em_construção.py
│   └── Aprovação_Malga_Otimizada.py  # ✨ Dashboard otimizado
│
├── 📂 docs/                          # ✨ NOVO: Documentação
│   ├── README.md                     # Documentação geral
│   ├── README_MALGA_WORKER.md        # Guia do worker
│   ├── TESTE_API.md                  # Guia de troubleshooting
│   ├── GEMINI_SETUP.md               # Setup do Gemini
│   └── ANALISE_APROFUNDADA.md        # Análises técnicas
│
├── 📂 logs/                          # ✨ NOVO: Arquivos de log
│   └── malga_worker.log              # Logs do worker
│
├── 📂 scripts/                       # ✨ NOVO: Scripts utilitários
│   ├── cleanup_modulos.py
│   ├── remove_dividers.py
│   └── Pagina_inicial_temp.py
│
├── 📂 .streamlit/                    # Configurações Streamlit
│   └── secrets.toml                  # Secrets (chaves API)
│
├── Pagina_inicial.py                 # Página inicial do app
├── requirements.txt                  # Dependências Python
├── utils.py                          # ✨ NOVO: Funções auxiliares
└── .gitignore                        # Arquivos ignorados pelo Git
```

## 🔑 Chaves API Atualizadas

### ✅ Locais Onde as Chaves Foram Atualizadas:

1. **`worker/config.py`** ✅
   ```python
   MALGA_CLIENT_ID = "af94ea85-d55f-4458-a7e6-0ce2574472c7"
   MALGA_CLIENT_SECRET = "7bd92a23-bb31-4b98-9b77-3fb3be94ecbb"
   ```

2. **`.streamlit/secrets.toml`** ✅
   ```toml
   MALGA_CLIENT_ID = "af94ea85-d55f-4458-a7e6-0ce2574472c7"
   MALGA_CLIENT_SECRET = "7bd92a23-bb31-4b98-9b77-3fb3be94ecbb"
   ```

## 🚀 Como Usar Após Reorganização

### 1. Iniciar o Worker

```powershell
cd worker
python start_worker.py
```

**Ou da raiz do projeto:**
```powershell
python worker/start_worker.py
```

### 2. Iniciar o Dashboard

```powershell
streamlit run Pagina_inicial.py
```

### 3. Verificar Logs

```powershell
cat logs/malga_worker.log
```

## 📝 Mudanças Importantes

### Caminhos Atualizados

**Antes (raiz do projeto):**
```python
"2Alura - Fluxo de caixa.csv"
```

**Depois (pasta data):**
```python
"data/2Alura - Fluxo de caixa.csv"
```

### Imports Atualizados

**Arquivo: `pages/Aprovação_Malga_Otimizada.py`**

**Antes:**
```python
from config import *
from malga_database import MalgaDatabase
```

**Depois:**
```python
from worker.config import *
from worker.malga_database import MalgaDatabase
```

### Helper para Caminhos

Use a função auxiliar `get_data_path()` para carregar dados:

```python
from utils import get_data_path

# Carrega arquivo automaticamente do local correto
file_path = get_data_path("2Alura - Fluxo de caixa.csv")
df = pd.read_csv(file_path)
```

## ✨ Benefícios da Nova Estrutura

1. **📁 Organização** - Arquivos agrupados por função
2. **🔍 Clareza** - Fácil encontrar o que procura
3. **🧹 Limpeza** - Raiz do projeto mais limpa
4. **📦 Modularidade** - Worker isolado em sua pasta
5. **📊 Dados centralizados** - Todos os CSVs/Excel em um lugar
6. **📝 Documentação** - Docs separados e organizados
7. **🔐 Segurança** - Configs sensíveis isoladas

## ⚠️ Avisos Importantes

### Git e Secrets
- ✅ `.gitignore` já ignora `secrets.toml`
- ✅ `.gitignore` já ignora `*.log`
- ✅ `.gitignore` já ignora `*.db`
- ⚠️ Nunca faça commit de chaves de API

### Backup
Recomendado fazer backup antes de:
- Mover arquivos manualmente
- Deletar arquivos antigos
- Atualizar dependências

## 🔄 Compatibilidade

A função `get_data_path()` em `utils.py` garante compatibilidade:
- ✅ Funciona com estrutura nova (data/)
- ✅ Funciona com estrutura antiga (raiz)
- ✅ Busca automaticamente em múltiplos locais

## 📚 Próximos Passos

1. ✅ Estrutura reorganizada
2. ✅ Chaves API atualizadas
3. ✅ Imports corrigidos
4. ⏳ Testar worker: `python worker/start_worker.py`
5. ⏳ Testar dashboard: `streamlit run Pagina_inicial.py`
6. ⏳ Verificar todas as páginas funcionam
7. ⏳ Commit das mudanças (exceto secrets!)

## 🆘 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'worker'"
**Solução:** Execute a partir da raiz do projeto

### Erro: "File not found: 2Alura - Fluxo de caixa.csv"
**Solução:** Use `get_data_path()` ou atualize caminho para `data/`

### Erro: "Credenciais inválidas"
**Solução:** Verifique se `worker/config.py` tem as chaves corretas

### Worker não inicia
**Solução:**
```powershell
cd worker
python -m pip install -r ../requirements.txt
python start_worker.py
```
