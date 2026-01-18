# 📊 Guia de Atualização dos Dados do Planejamento Estratégico

## 📁 Arquivos de Dados (CSV)

### 1. `planejamento_estrategico_2026.csv`
Contém os dados atuais de cada indicador por período.

### 2. `kpis_historico_2026.csv`
Contém o histórico mensal para gerar os gráficos de evolução.

---

## 🔧 Estrutura do `planejamento_estrategico_2026.csv`

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| `objetivo_id` | ID do objetivo (1-7) | 1 |
| `objetivo` | Nome completo do objetivo | Aumentar eficiência técnica... |
| `resultado_chave` | Nome do indicador | Percentual do time que completou... |
| `meta` | Valor da meta | 100 |
| `valor_atual` | Valor atual medido | 25 |
| `periodo` | Data do período (YYYY-MM-DD) | 2024-12-31 |
| `ano` | Ano do dado | 2024 |
| `mes` | Mês do dado (1-12) | 12 |
| `tipo_indicador` | Tipo do valor | percentual, dias, horas, reais, quantidade, booleano |
| `tipo_calculo` | Lógica de avaliação | maior_melhor, menor_melhor, menor_igual_melhor, sim_nao |
| `qtd_pessoas_time` | Qtd. pessoas (para Obj 1) | 4 |
| `status` | Status atual | em_andamento, meta_atingida, nao_atingido |
| `observacoes` | Comentários | Texto livre |

---

## 📐 Tipos de Cálculo (MUITO IMPORTANTE!)

### `maior_melhor`
- **Quando usar:** Indicadores onde valor MAIOR é melhor
- **Exemplos:** % Trilha da Lívia, % Automações, % CDI
- **Lógica:** ✅ se valor >= meta

### `menor_melhor`
- **Quando usar:** Indicadores onde valor MENOR é melhor (meta é o MÍNIMO aceitável)
- **Exemplos:** PMP (dias) - queremos aumentar para 20, valor menor é RUIM
- **Lógica:** ✅ se valor < meta
- **ATENÇÃO:** Se a meta é 20 e o valor é 15, NÃO atingiu (queremos 20 ou mais)

### `menor_igual_melhor`
- **Quando usar:** Indicadores onde valor deve ser MENOR OU IGUAL à meta (meta é o MÁXIMO)
- **Exemplos:** SLA ≤24h, Desvio ≤0.1%, Tickets ≤10
- **Lógica:** ✅ se valor <= meta

### `maior_igual_melhor`
- **Quando usar:** Indicadores onde valor deve ser MAIOR OU IGUAL à meta
- **Exemplos:** % CDI ≥100%
- **Lógica:** ✅ se valor >= meta

### `percentual_meta`
- **Quando usar:** Indicadores calculados como % da meta
- **Exemplos:** Cashback (valor atual / meta * 100)
- **Meta:** valor que precisa atingir (ex: R$10.657 que é base + 20%)
- **Lógica:** ✅ se valor >= meta

### `sim_nao`
- **Quando usar:** Indicadores booleanos (Sim ou Não)
- **Exemplos:** Fechamento sem atraso, Vans implementadas, Bolecode
- **Valores válidos no valor_atual:** sim, nao (ou s, n, 1, 0, true, false)
- **Meta:** sempre "sim"
- **Lógica:** ✅ se valor = "sim"

---

## 📋 Tipos de Indicador (Formatação)

| Tipo | Formatação na Dashboard | Exemplo |
|------|------------------------|---------|
| `percentual` | XX.XX% | 25.00% |
| `dias` | XX.XX dias | 15.44 dias |
| `horas` | XX.Xh | 24.1h |
| `reais` | R$ X.XXX,XX | R$ 6.664,00 |
| `quantidade` | XX | 12 |
| `booleano` | Sim/Não | Sim |

---

## 🎯 Mapeamento Completo por Objetivo

### Objetivo 1: Eficiência Técnica da Tesouraria
| Indicador | tipo_indicador | tipo_calculo | Meta |
|-----------|---------------|--------------|------|
| % Trilha da Lívia | percentual | maior_melhor | 100% |
| % Automações construídas | percentual | maior_melhor | 100% |

### Objetivo 2: Ciclo de Pagamentos
| Indicador | tipo_indicador | tipo_calculo | Meta |
|-----------|---------------|--------------|------|
| PMP (dias) | dias | **menor_melhor** | 20 (Q1), 25 (Q2), 30 (Q3) |
| Cashback mensal | reais | percentual_meta | Base + 20% |
| SLA 1ª Resposta (interno) | horas | **menor_igual_melhor** | ≤24h |

**⚠️ ATENÇÃO PMP:** A meta é AUMENTAR o PMP para 20 dias. Se o valor é 15.44, está ABAIXO da meta!

**⚠️ ATENÇÃO Cashback:** 
- Coloque na **meta** o valor que precisa atingir (base + 20%)
- Exemplo: se base é R$8.882, meta = R$10.658,40
- O sistema calcula se valor >= meta

**⚠️ ATENÇÃO SLA:** Meta é 24h ou MENOS. Se valor > 24h, NÃO atingiu!

### Objetivo 3: Acuracidade
| Indicador | tipo_indicador | tipo_calculo | Meta |
|-----------|---------------|--------------|------|
| Desvio Fin. vs Cont. | percentual | **menor_igual_melhor** | ≤0.1% |
| Saldo Irregularidades | reais | **menor_melhor** | 0 (zerar) |

**⚠️ ATENÇÃO Desvio:** Meta é 0.1% ou MENOS. Se valor > 0.1%, NÃO atingiu!

### Objetivo 4: Eficiência Operacional
| Indicador | tipo_indicador | tipo_calculo | Meta |
|-----------|---------------|--------------|------|
| Fechamento sem atraso | booleano | sim_nao | sim |
| Vans Bancárias implementadas | booleano | sim_nao | sim |

### Objetivo 5: Rentabilidade
| Indicador | tipo_indicador | tipo_calculo | Meta |
|-----------|---------------|--------------|------|
| % CDI | percentual | maior_igual_melhor | ≥100% |

### Objetivo 6: Eficiência de Caixa
| Indicador | tipo_indicador | tipo_calculo | Meta |
|-----------|---------------|--------------|------|
| Bolecode implementado | booleano | sim_nao | sim |
| % Conversão em Caixa | percentual | maior_melhor | 100% |

### Objetivo 7: Prazos Operacionais
| Indicador | tipo_indicador | tipo_calculo | Meta |
|-----------|---------------|--------------|------|
| Tickets na Caixa | quantidade | **menor_igual_melhor** | ≤10 |
| SLA 1ª Resposta (tickets) | horas | **menor_igual_melhor** | ≤24h |

---

## 📈 Estrutura do `kpis_historico_2026.csv`

| Coluna | Descrição |
|--------|-----------|
| `ano` | Ano do registro (2024, 2025, 2026) |
| `mes` | Mês (1-12) |
| `kpi_tipo` | Tipo do KPI |
| `kpi_nome` | Nome do KPI |
| `valor` | Valor medido |
| `meta` | Meta do período |
| `unidade` | Unidade (%, dias, horas, reais, quantidade, booleano) |
| `tipo_calculo` | Lógica de avaliação |

### Mapeamento kpi_tipo → Objetivo:
- `eficiencia_tecnica` → Objetivo 1
- `ciclo_pagamentos` → Objetivo 2
- `acuracidade` → Objetivo 3
- `operacional` → Objetivo 4
- `rentabilidade` → Objetivo 5
- `eficiencia_caixa` → Objetivo 6
- `prazos` → Objetivo 7

### Nomes de KPIs válidos:
- `trilha_livia_percent`, `automacoes_percent`
- `pmp_dias`, `cashback_mensal`, `sla_horas`
- `desvio_percentual`, `saldo_irregularidades`
- `fechamento_sem_atraso`, `vans_bancarias`
- `cdi_percentual`
- `bolecode_implementado`, `conversao_caixa`
- `tickets_caixa`, `sla_tickets_horas`

---

## 🔄 Como Atualizar

### Passo 1: Editar os arquivos CSV
- Abra no Excel ou editor de texto
- Adicione novas linhas com os dados do novo período
- **IMPORTANTE:** Preencha ano e mes corretamente!

### Passo 2: Validar os dados
- Verifique se `tipo_indicador` e `tipo_calculo` estão corretos
- Use valores numéricos com **ponto decimal** (15.44, não 15,44)
- Para booleanos use: sim ou nao

### Passo 3: Commit e Push
```bash
git add data/planejamento_estrategico_2026.csv
git add data/kpis_historico_2026.csv
git commit -m "Atualização dados mês XX/XXXX"
git push
```

### Passo 4: Aguardar deploy
O Streamlit Cloud atualizará automaticamente em ~2 minutos.

---

## ⚠️ Erros Comuns e Soluções

### 1. **Indicador aparece vermelho quando deveria ser verde**
- Verifique se `tipo_calculo` está correto
- PMP usa `menor_melhor` (queremos AUMENTAR o prazo)
- SLA usa `menor_igual_melhor` (queremos ≤24h)

### 2. **Gráfico de evolução não aparece**
- Verifique se há dados no `kpis_historico_2026.csv`
- Confira se `kpi_tipo` está correto

### 3. **Valores formatados errado**
- Use **ponto** como separador decimal (15.44)
- Não use R$ nos valores de reais, só o número

### 4. **Filtro de ano mostra dados errados**
- Verifique as colunas `ano` e `mes` nos CSVs
- Dezembro/2024 deve ter ano=2024, mes=12

### 5. **Indicador booleano não funciona**
- Use exatamente: `sim` ou `nao` (minúsculo)
- Meta deve ser: `sim`

---

## 📌 Resumo Rápido

| Indicador | Se valor é... | Então está... |
|-----------|--------------|---------------|
| PMP 15.44 (meta 20) | menor que meta | ❌ ABAIXO da meta |
| SLA 24.1h (meta 24) | maior que meta | ❌ NÃO atingiu |
| Desvio 0.203% (meta 0.1) | maior que meta | ❌ ACIMA do limite |
| CDI 102.54% (meta 100) | maior que meta | ✅ SUPEROU |
| Fechamento = nao | diferente de sim | ❌ NÃO atingiu |
