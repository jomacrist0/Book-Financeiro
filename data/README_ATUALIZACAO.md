# 📊 Como Atualizar os Dados do Planejamento Estratégico

## 🎯 Arquivos de Dados

Existem **2 arquivos principais** para você atualizar:

### 1. `planejamento_estrategico_2026.xlsx` 
**O QUE É:** Dados dos objetivos, metas e resultados atuais

**COLUNAS:**
- `objetivo_id`: Número do objetivo (1, 2, 3...)
- `objetivo`: Descrição completa do objetivo estratégico
- `resultado_chave`: O que você quer medir (KR - Key Result)
- `meta`: Valor que você quer atingir (ex: 100 para 100%)
- `valor_atual`: Valor atual do indicador (ex: 25 para 25%)
- `periodo`: Data de referência (formato: YYYY-MM-DD, ex: 2024-12-31)
- `status`: Estado atual (em_andamento, meta_atingida, abaixo_meta, atencao, nao_iniciado, descontinuado, sem_dados)
- `observacoes`: Comentários adicionais

**EXEMPLO DE LINHA:**
```
1 | Aumentar eficiência técnica... | 100% do time completar Trilha | 100 | 25 | 2024-12-31 | em_andamento | 25% da área completou
```

---

### 2. `kpis_historico_2026.xlsx`
**O QUE É:** Evolução mensal dos indicadores para gráficos de linha/tendência

**COLUNAS:**
- `mes`: Mês (1-12)
- `ano`: Ano (2024, 2025, 2026...)
- `kpi_tipo`: Categoria (eficiencia_tecnica, ciclo_pagamentos, acuracidade, operacional, rentabilidade)
- `kpi_nome`: Nome do indicador específico
- `valor`: Valor medido naquele mês
- `meta`: Meta esperada para aquele mês
- `unidade`: Unidade de medida (%, dias, reais, horas)

**EXEMPLO DE LINHA:**
```
12 | 2024 | ciclo_pagamentos | pmp_dias | 15.44 | 20 | dias
```

---

## ✏️ Como Atualizar (Passo a Passo)

### **OPÇÃO 1: Editar no Excel (Mais Fácil)**

1. Abra o arquivo Excel (`planejamento_estrategico_2026.xlsx` ou `kpis_historico_2026.xlsx`)
2. Edite diretamente as células
3. **IMPORTANTE:** Mantenha o formato das datas (YYYY-MM-DD) e números (use ponto para decimal: 15.44)
4. Salve o arquivo
5. Faça commit no GitHub (explico abaixo)

### **OPÇÃO 2: Editar no CSV (Mais Técnico)**

1. Abra o arquivo CSV com um editor de texto (VSCode, Notepad++)
2. Cada linha é separada por vírgulas
3. Edite os valores
4. Salve o arquivo
5. Faça commit no GitHub

---

## 🚀 Como Atualizar no GitHub

Depois de editar os arquivos, você precisa enviar para o GitHub:

```powershell
# 1. Entre na pasta do projeto
cd "C:\Users\colaboradorfiap\OneDrive - Fiap-Faculdade de Informática e Administração Paulista\Documentos\Projetos\Book-Financeiro"

# 2. Adicione os arquivos alterados
git add data/planejamento_estrategico_2026.xlsx data/kpis_historico_2026.xlsx

# 3. Faça o commit
git commit -m "Atualiza dados do planejamento estratégico - [MÊS/ANO]"

# 4. Envie para o GitHub
git push
```

**O Streamlit Cloud vai atualizar automaticamente em ~2 minutos!**

---

## 📝 Dicas de Preenchimento

### **Status Recomendados:**
- `meta_atingida` ✅ - Quando valor_atual >= meta
- `em_andamento` 🟡 - Progresso bom mas ainda não atingiu
- `abaixo_meta` 🟠 - Valor atual está abaixo do esperado
- `atencao` ⚠️ - Situação crítica, precisa atenção
- `nao_iniciado` ⭕ - Ainda não começou
- `superou_meta` 🎯 - Superou a meta!
- `descontinuado` ❌ - KPI descontinuado
- `sem_dados` ⚪ - Sem dados disponíveis ainda

### **Valores Numéricos:**
- Percentuais: use números diretos (25 para 25%, não 0.25)
- Dinheiro: valor bruto (6664 para R$ 6.664)
- Dias/Horas: use decimais com ponto (24.1 para 24h e 6min)
- Datas: formato YYYY-MM-DD (2024-12-31)

### **KPI Tipos (para histórico):**
- `eficiencia_tecnica` - Trilha, automações
- `ciclo_pagamentos` - PMP, cashback, SLA
- `acuracidade` - Desvios, irregularidades
- `operacional` - Fechamentos, vans bancárias
- `rentabilidade` - CDI
- `eficiencia_caixa` - Bolecode, conversão

---

## 🔄 Frequência de Atualização Recomendada

- **Mensal:** Adicione novas linhas no `kpis_historico_2026.xlsx` todo mês
- **Trimestral:** Revise metas e status no `planejamento_estrategico_2026.xlsx`
- **Sempre que houver mudanças:** Atualize `valor_atual` e `observacoes`

---

## 🆘 Troubleshooting

**"Dashboard não atualizou após commit"**
- Aguarde 2-3 minutos
- Acesse o Streamlit Cloud e force um "Reboot app"

**"Erro ao ler a planilha"**
- Verifique se manteve os nomes das colunas exatamente iguais
- Confira se o formato das datas está correto (YYYY-MM-DD)
- Use ponto (.) para decimais, não vírgula

**"Gráfico não aparece"**
- Certifique-se de ter pelo menos 2 meses de dados no histórico
- Verifique se o `kpi_nome` está consistente (mesma escrita)

---

## 📞 Contato

Se tiver dúvidas, consulte este README ou verifique os exemplos nos arquivos CSV/Excel.

**Arquivos de Template:**
- `data/planejamento_estrategico_2026.xlsx` - Dados principais
- `data/kpis_historico_2026.xlsx` - Histórico mensal
- `data/planejamento_estrategico_2026.csv` - Backup CSV
- `data/kpis_historico_2026.csv` - Backup CSV
