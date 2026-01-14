# 📊 Book Financeiro - Dashboard Streamlit

Sistema completo de dashboards financeiros com análise de dados da ALURA Group (marca ALUN).

## 🚀 Quick Start

### Instalação
```powershell
pip install -r requirements.txt
```

### Iniciar Dashboard
```powershell
streamlit run Pagina_inicial.py
```

### Iniciar Worker Malga (Opcional - para dashboard otimizado)

**Modo Teste (2000 transações):**
```powershell
python test_worker_once.py
```

**Modo Produção (contínuo):**
```powershell
python run_worker.py
```

> 💡 **Dica**: Comece com o modo teste para validar o funcionamento antes de rodar em produção.

## 📁 Estrutura do Projeto

```
📂 data/          # Arquivos CSV/Excel e banco de dados
📂 worker/        # Sistema Worker + SQLite para Malga API
📂 pages/         # Páginas do dashboard Streamlit
📂 docs/          # Documentação completa
📂 logs/          # Logs do sistema
📂 scripts/       # Scripts utilitários
```

## 📊 Dashboards Disponíveis

### 1. Saldos do Ecossistema
Análise de saldos consolidados por empresa (GOV, GE, PME, B2C)

### 2. Fluxo de Caixa
Entradas, saídas e saldo acumulado com visão operacional/financeira

### 3. Meios de Pagamento
Análise de volume, taxas e performance por método de pagamento

### 4. Contas a Receber (Aging)
Análise de aging de recebíveis com intervalos de vencimento

### 5. Contas a Pagar (PMP)
Prazo médio de pagamento e análise de fornecedores

### 6. Investimentos
Rentabilidade de investimentos com comparação ao CDI

### 7. Aprovação Malga 🆕
Análise de taxa de aprovação de pagamentos com API Malga
- **Em Construção**: Consulta direta à API
- **Otimizado** ⚡: Sistema Worker + SQLite (performance 10x+)

## ⚡ Sistema Worker Malga

### O que é?
Sistema de background que:
- Sincroniza automaticamente com API Malga (a cada 1 minuto)
- Armazena dados em banco SQLite local
- Pré-calcula métricas (taxa de aprovação, volumes, etc.)
- Permite dashboard ultra-rápido (milissegundos vs segundos)

### Como funciona?
```
API Malga → Worker (APScheduler) → SQLite → Dashboard Streamlit
```

### 🧪 Modo Teste (RECOMENDADO PARA INÍCIO)

Para testar com **2000 transações** antes de coletar volumes maiores:

```powershell
python test_worker_once.py
```

**Vantagens:**
- ✅ Executa UMA VEZ e para
- ✅ Rápido (~20 páginas de API)
- ✅ Ideal para validar funcionamento
- ✅ Logs detalhados em `logs/test_worker.log`

**O que verificar:**
- Total de transações coletadas (~2000)
- Taxa de aprovação consistente (não oscilando)
- Métricas calculadas corretamente
- Dashboard mostrando dados

📖 **Documentação completa:** [docs/TESTE_WORKER_2000.md](docs/TESTE_WORKER_2000.md)

### 🚀 Modo Produção (Contínuo)

Após validar com o teste, execute em produção:

```powershell
python run_worker.py
```

**Características:**
- 🔄 Sincroniza a cada 1 minuto automaticamente
- 📊 Coleta até 50.000 transações por sync
- 💾 Mantém dados sempre atualizados
- ⏱️ Roda continuamente (use Ctrl+C para parar)

### Configuração

1. **Atualizar chaves em `worker/config.py`:**
```python
MALGA_CLIENT_ID = "sua-chave-aqui"
MALGA_CLIENT_SECRET = "sua-chave-secreta"
```

2. **Ou em `.streamlit/secrets.toml`:**
```toml
MALGA_CLIENT_ID = "sua-chave-aqui"
MALGA_CLIENT_SECRET = "sua-chave-secreta"
```

3. **Iniciar worker:**
```powershell
python run_worker.py
```

4. **Acessar dashboard otimizado:**
- Abra o Streamlit
- Clique em "⚡ Aprovação Malga - Otimizada"

## 📚 Documentação Completa

- [📖 Estrutura do Projeto](docs/ESTRUTURA_PROJETO.md)
- [🔧 Setup do Worker Malga](docs/README_MALGA_WORKER.md)
- [🧪 Teste Worker (2000 transações)](docs/TESTE_WORKER_2000.md) ⭐ **Comece aqui!**
- [🐛 Troubleshooting API](docs/TESTE_API.md)
- [🤖 Gemini AI Setup](docs/GEMINI_SETUP.md)

## 🛠️ Tecnologias

- **Streamlit**: Framework web para dashboards
- **Pandas**: Manipulação de dados
- **Plotly**: Gráficos interativos
- **SQLite**: Banco de dados local
- **APScheduler**: Jobs agendados (worker)
- **Requests**: Chamadas HTTP para API Malga

## 🎨 Tema ALUN

Todos os dashboards usam o tema dark customizado da marca ALUN:
- Cor principal: Laranja `#ff6b35`
- Background: Dark `#0e1117`
- Containers: `#262730`
- Bordas: `#30343f`

## 📦 Dependências

```txt
streamlit
pandas
plotly
numpy
openpyxl
requests
apscheduler
pytz
google-generativeai
```

## 🔐 Segurança

⚠️ **IMPORTANTE:**
- Nunca faça commit de `secrets.toml`
- Nunca faça commit de chaves de API em `config.py`
- Use variáveis de ambiente em produção

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Projeto interno ALURA Group - Todos os direitos reservados.

## 🆘 Suporte

Para problemas ou dúvidas, consulte a [documentação completa](docs/) ou abra uma issue.

---

**Desenvolvido com ❤️ pela equipe ALUN**
