# 🧪 Teste do Worker com 2000 Transações

## 📋 Objetivo

Este documento explica como executar o Worker em **modo de teste** com limite de **2000 transações**, ideal para validar o funcionamento antes de coletar volumes maiores de dados.

## 🎯 Por Que 2000 Transações?

Durante os testes iniciais, o worker estava buscando transações infinitamente (passando de 150+ páginas), o que:
- ⏱️ Demorava muito tempo
- 💾 Consumia muitos recursos
- 🐛 Dificultava identificar problemas

Com o limite de **2000 transações**:
- ✅ Teste rápido (20 páginas × 100 transações)
- ✅ Volume suficiente para validar cálculos
- ✅ Fácil verificar se está funcionando corretamente
- ✅ Permite iteração rápida em caso de bugs

## 🔧 Configuração de Teste

### Arquivo: `worker/config.py`

```python
# === CONFIGURAÇÃO DE SINCRONIZAÇÃO ===
MAX_TRANSACTIONS_PER_SYNC = 2000  # 🧪 LIMITE DE TESTE (20 páginas × 100)
API_TIMEOUT = 30
MAX_API_PAGES = 20  # Máximo de páginas a buscar (20 × 100 = 2000)
```

### Arquivo: `worker/malga_worker.py`

O worker foi modificado para:
1. **Contar transações coletadas** (`total_collected`)
2. **Parar quando atingir o limite** (2000 transações)
3. **Cortar a última página** se ultrapassar o limite
4. **Adicionar rate limiting** (0.5s entre páginas)
5. **Mostrar progresso detalhado** no log

## 🚀 Como Executar o Teste

### Opção 1: Script de Teste (RECOMENDADO)

Execute o script que roda **UMA VEZ** e para:

```bash
python test_worker_once.py
```

**Vantagens:**
- ✅ Executa apenas uma vez
- ✅ Mostra estatísticas finais
- ✅ Logs no console + arquivo `logs/test_worker.log`
- ✅ Ideal para validar funcionamento

### Opção 2: Worker em Background

Execute o worker que **roda continuamente**:

```bash
cd worker
python start_worker.py
```

**Vantagens:**
- ✅ Sincroniza a cada 1 minuto
- ✅ Mantém dados sempre atualizados
- ✅ Ideal para produção

**Desvantagens:**
- ⚠️ Roda infinitamente (precisa Ctrl+C para parar)
- ⚠️ Mais difícil de testar mudanças rápidas

## 📊 O Que Esperar nos Logs

### Início da Sincronização

```
============================================================
🚀 Iniciando sincronização...
============================================================
🔍 PRIMEIRA SINCRONIZAÇÃO - Buscando TODAS as transações...
🎯 LIMITE CONFIGURADO: 2000 transações
```

### Durante a Coleta

```
📡 Página 1...
📄 Página 1: 100 transações | Total acumulado: 100/2000
📡 Página 2...
📄 Página 2: 100 transações | Total acumulado: 200/2000
...
📡 Página 20...
📄 Página 20: 100 transações | Total acumulado: 2000/2000
🛑 LIMITE ATINGIDO: 2000 transações coletadas
```

### Processamento

```
✅ Total de 2000 transações coletadas
📊 Páginas processadas: 20
✅ 2000 transações processadas
💾 2000 transações salvas no banco
```

### Agregações

```
📊 Agregando por minuto...
📊 Agregando por hora...
📊 Agregando por dia...
✅ Sincronização concluída em XX segundos
```

## 🔍 Verificação dos Resultados

### 1. Verificar Logs

```bash
# Logs do teste único
cat logs/test_worker.log

# Logs do worker contínuo
cat logs/malga_worker.log
```

### 2. Verificar Banco de Dados

```bash
sqlite3 data/malga_datamart.db
```

```sql
-- Total de transações
SELECT COUNT(*) FROM transactions;

-- Últimas transações
SELECT id, created_at, status, amount FROM transactions ORDER BY created_at DESC LIMIT 10;

-- Métricas por dia
SELECT * FROM metrics_by_day ORDER BY period DESC LIMIT 7;

-- Informação de sincronização
SELECT * FROM sync_control;
```

### 3. Verificar Dashboard

```bash
streamlit run pages/Aprovação_Malga_Otimizada.py
```

Verifique se:
- ✅ Gráficos mostram dados
- ✅ Taxa de aprovação está correta (não oscilando 0-100%)
- ✅ Volume de transações está correto
- ✅ Filtros funcionam

## 🔄 Aumentando para Produção

Quando o teste estiver funcionando perfeitamente, aumente os limites:

### Arquivo: `worker/config.py`

```python
# === CONFIGURAÇÃO DE SINCRONIZAÇÃO ===
MAX_TRANSACTIONS_PER_SYNC = 50000  # 🚀 PRODUÇÃO (500 páginas × 100)
API_TIMEOUT = 30
MAX_API_PAGES = 500  # Máximo de páginas a buscar
```

### Executar Worker em Produção

```bash
cd worker
python start_worker.py
```

O worker agora vai:
- 🔄 Sincronizar a cada 1 minuto
- 📈 Buscar até 50.000 transações por sync
- 💾 Manter dados sempre atualizados

## ⚠️ Troubleshooting

### Problema: "Nenhuma transação coletada"

**Possíveis causas:**
- ❌ API keys incorretas no `worker/config.py`
- ❌ Sem conexão com internet
- ❌ API da Malga fora do ar

**Solução:**
1. Verifique as credenciais:
   ```python
   CLIENT_ID = "af94ea85-d55f-4458-a7e6-0ce2574472c7"
   API_KEY = "7bd92a23-bb31-4b98-9b77-3fb3be94ecbb"
   ```
2. Teste manualmente:
   ```bash
   curl -X GET "https://api.malga.io/v1/charges?limit=1" \
     -H "X-Client-Id: af94ea85-d55f-4458-a7e6-0ce2574472c7" \
     -H "X-Api-Key: 7bd92a23-bb31-4b98-9b77-3fb3be94ecbb"
   ```

### Problema: "Worker não para em 2000"

**Solução:**
- Verifique se `worker/config.py` tem `MAX_TRANSACTIONS_PER_SYNC = 2000`
- Verifique se `worker/malga_worker.py` foi atualizado com a lógica de stop

### Problema: "Taxa de aprovação oscilando 0-100%"

**Solução:**
- ✅ Já foi corrigido! A fórmula agora é: `approved/(approved+failed)*100`
- Verifique se `worker/malga_database.py` tem a fórmula correta nas 3 funções de agregação

## 📝 Resumo dos Arquivos

| Arquivo | Propósito |
|---------|-----------|
| `worker/config.py` | Configurações (limite de 2000) |
| `worker/malga_worker.py` | Worker com lógica de stop |
| `worker/malga_database.py` | Banco de dados SQLite |
| `test_worker_once.py` | Script de teste (execução única) |
| `worker/start_worker.py` | Worker em background (loop contínuo) |
| `logs/test_worker.log` | Logs do teste |
| `logs/malga_worker.log` | Logs do worker contínuo |
| `data/malga_datamart.db` | Banco de dados SQLite |

## ✅ Checklist de Teste

- [ ] Configuração com 2000 transações em `worker/config.py`
- [ ] Executar `python test_worker_once.py`
- [ ] Verificar logs em `logs/test_worker.log`
- [ ] Confirmar que parou em ~2000 transações
- [ ] Verificar banco: `SELECT COUNT(*) FROM transactions;`
- [ ] Abrir dashboard e verificar gráficos
- [ ] Taxa de aprovação está consistente (não oscila)
- [ ] Se tudo OK, aumentar para 50.000 e rodar em produção

---

**Dúvidas?** Consulte também:
- `docs/ESTRUTURA_PROJETO.md` - Arquitetura completa
- `docs/CORRECOES_TAXA_APROVACAO.md` - Correção da fórmula
- `README.md` - Visão geral do projeto
