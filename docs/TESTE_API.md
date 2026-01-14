# 🔧 Guia de Teste da API Malga

## ✅ Melhorias Implementadas no Worker

### 1. Headers Completos
Adicionado header `"Accept": "application/json"` que estava faltando:
```python
headers = {
    "X-Client-Id": MALGA_CLIENT_ID,
    "X-Api-Key": MALGA_CLIENT_SECRET,
    "Content-Type": "application/json",
    "Accept": "application/json"  # ← Novo
}
```

### 2. Melhor Tratamento de Erros na Autenticação
Agora mostra detalhes específicos de cada tipo de erro:
- **401**: Credenciais inválidas
- **403**: Acesso negado
- **Outros**: Mostra resposta da API

### 3. Múltiplas Estratégias de Busca
O worker agora tenta dois conjuntos de parâmetros:

**Opção 1** (com filtro de data):
```python
{
    "limit": 100,
    "page": 1,
    "created.gt": "2024-09-20",
    "sort": "DESC"
}
```

**Opção 2** (sem filtro - busca tudo):
```python
{
    "limit": 100,
    "page": 1,
    "sort": "DESC"
}
```

### 4. Logs Detalhados
Cada tentativa agora mostra:
- Parâmetros usados
- Status HTTP
- Quantidade de transações
- Total acumulado

## 🧪 Como Testar

### 1. Verificar Credenciais
As credenciais devem estar em **DOIS** lugares idênticos:

**`config.py`:**
```python
MALGA_CLIENT_ID = "af94ea85-d55f-4458-a7e6-0ce2574472c7"
MALGA_CLIENT_SECRET = "7bd92a23-bb31-4b98-9b77-3fb3be94ecbb"
```

**`.streamlit/secrets.toml`:**
```toml
MALGA_CLIENT_ID = "af94ea85-d55f-4458-a7e6-0ce2574472c7"
MALGA_CLIENT_SECRET = "7bd92a23-bb31-4b98-9b77-3fb3be94ecbb"
```

### 2. Testar Worker
```powershell
python start_worker.py
```

**Saída esperada:**
```
🔐 Autenticando com Client-Id: af94ea85-d55f-4458...
✅ Autenticação bem-sucedida
🔍 Buscando transações desde 2024-09-20...
📡 Tentando buscar página 1 com params: {...}
📄 Página 1: 100 transações (total: 100)
📄 Página 2: 100 transações (total: 200)
...
✅ Total de 350 transações coletadas
💾 Inserindo transações no banco...
📊 Iniciando agregações...
✅ Sincronização concluída: 350 transações
```

### 3. Verificar Logs
```powershell
cat malga_worker.log
```

Procure por:
- ✅ "Autenticação bem-sucedida"
- 📄 "X transações coletadas"
- ❌ Qualquer erro

### 4. Testar Dashboard
```powershell
streamlit run Pagina_inicial.py
```

Acesse **"⚡ Aprovação Malga - Otimizada"** e verifique:
- Status do worker na sidebar
- Métricas globais preenchidas
- Gráficos com dados

## 🔍 Diagnóstico de Problemas

### Problema: "Credenciais inválidas (401)"
**Solução:**
1. Verifique se as credenciais em `config.py` e `.streamlit/secrets.toml` são idênticas
2. Confirme que são as credenciais corretas do painel Malga
3. Verifique se não há espaços extras

### Problema: "Nenhuma transação coletada"
**Possíveis causas:**
1. Filtro de data muito restritivo
2. Não há transações no período
3. API não suporta o parâmetro `created.gt`

**Solução:** O worker agora tenta automaticamente sem filtro de data

### Problema: "Timeout"
**Solução:**
Aumente o timeout em `config.py`:
```python
API_TIMEOUT = 30  # De 15 para 30 segundos
```

### Problema: Dashboard mostra "Worker não inicializado"
**Solução:**
1. Certifique-se de que `python start_worker.py` está rodando
2. Aguarde 1 minuto para a primeira sincronização
3. Clique em "🔄 Atualizar Dashboard"

## 📊 Verificar Banco de Dados

Para ver se há dados no banco:

```powershell
python -c "import sqlite3; conn = sqlite3.connect('malga_datamart.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM transactions'); print(f'Total transações: {cursor.fetchone()[0]}'); conn.close()"
```

## 🎯 Próximos Passos

Se ainda não funcionar:
1. Compartilhe o conteúdo completo do `malga_worker.log`
2. Mostre a saída do terminal ao executar `python start_worker.py`
3. Verifique se a API Malga está acessível: https://api.malga.io/v1/charges

## 📞 Endpoints da API Malga

- **Produção**: https://api.malga.io/v1/charges
- **Sandbox**: https://sandbox-api.malga.io/v1/charges

Certifique-se de usar o ambiente correto para suas credenciais!
