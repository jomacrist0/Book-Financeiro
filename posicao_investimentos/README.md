# 💼 Posição de Investimentos - Dashboard

## ⚠️ STATUS: PRE-RELEASE (NÃO COMMITADO NO GITHUB)

Dashboard Streamlit para análise consolidada de posição de investimentos com cálculos avançados de cotização e liquidação.

---

## 📋 ASSUNÇÕES & DOCUMENTAÇÃO

### 1. Formato do Arquivo de Entrada
Esperamos um arquivo XLSX ou CSV com colunas:
- **Fundo / Ativo**: Nome do fundo ou ativo
- **Posição Atual**: String formato BRL (ex: "R$ 2.126.062,81")
- **Dias para Cotização**: Inteiro (dias corridos) | "Fechado" | Data "dd/mm/yyyy"
- **Dias pra Liquidação**: Inteiro (dias úteis) | Data "dd/mm/yyyy" | Vazio
- **Tipo**: "Fundo" | "Renda Fixa" | "Imediato" | etc
- **Status**: "Disponível" | "Resgatado"
- **Empresa**: Nome da empresa
- **Atualização**: Data "dd/mm/yyyy" da última atualização

### 2. Regras de Cálculo

#### Data de Cotização
- Se **inteiro N**: `data_cotizacao = Atualização + N dias corridos`
- Se **data**: `data_cotizacao = essa data`
- Se **"Fechado"** ou vazio: `data_cotizacao = NULL` → Fechado-Indisponível

#### Data de Disponibilidade (Liquidação)
- Se **inteiro M**: `data_disponibilidade = data_cotizacao + M dias úteis` (pulando fins de semana e feriados)
- Se **data**: `data_disponibilidade = essa data`
- Se **vazio + Tipo indicar liquidez imediata** ("Imediato", "Overnight", "Renda Fixa"): `M = 0` (data_disponibilidade = data_cotizacao)
- Se **vazio + Tipo normal**: `data_disponibilidade = NULL` (marcado como "Sem regra de liquidação")

#### Classificação Operacional
```
├─ Fechado-Indisponível: data_cotizacao = NULL
├─ Aplicado: Status != "Resgatado" E não fechado
├─ Em Resgate: Status = "Resgatado" E hoje < data_disponibilidade
└─ Resgate Liquidado: Status = "Resgatado" E hoje >= data_disponibilidade
```

#### Disponível Hoje?
- `TRUE` se: `data_disponibilidade <= hoje` E não fechado
- `FALSE` caso contrário

### 3. Cálculos Temporais
- **Dias Restantes (Cotização)**: dias corridos entre hoje e data_cotizacao (mín. 0)
- **Dias Úteis Restantes (Liquidação)**: dias úteis entre hoje e data_disponibilidade (mín. 0)
- **Dias Úteis**: segunda a sexta, excluindo feriados (lista fixa 2026-2027)

### 4. Feriados Considerados
Feriados brasileiros 2026-2027 (definidos em `src/dates.py`):
```
2026: 01/01, 16/02, 17/02, 03/04, 21/04, 01/05, 04/06, 07/09, 12/10, 02/11, 15/11, 20/11, 25/12
2027: 01/01, 08/02, 09/02, 26/03, 21/04, 01/05, 27/05, 07/09, 12/10, 02/11, 15/11, 20/11, 25/12
```

---

## 🚀 Como Usar

### Instalação Local

1. **Clone o repositório** (quando pronto para produção)
```bash
git clone <repo>
cd posicao_investimentos
```

2. **Instale dependências**
```bash
pip install -r requirements.txt
```

3. **Prepare seu arquivo** (`data/posicao.xlsx` ou `.csv`)
```
Fundo / Ativo | Posição Atual | Dias para Cotização | Dias pra Liquidação | Tipo | Status | Empresa | Atualização
Fundo X | R$ 1.000.000,00 | 5 | 2 | Fundo | Disponível | Empresa A | 15/01/2026
```

4. **Inicie o Streamlit**
```bash
streamlit run posicao_investimentos/app.py
```

5. **Acesse**
```
http://localhost:8501
```

---

### Usando com GitHub

1. **Faça upload do seu arquivo no GitHub** (em uma branch de staging)
   ```
   Exemplo: https://github.com/seu-usuario/seu-repo/raw/staging/data/posicao.xlsx
   ```

2. **No app Streamlit**, selecione **"🌐 GitHub"** e cole a URL RAW

3. **Clique em "Acessar"** e o dashboard carregará os dados

---

## 📊 Funcionalidades

### KPIs (Cards Superiores)
- 💰 **Total Carteira**: Soma de todas as posições
- 📌 **Total Aplicado**: Posições não resgatadas e não fechadas
- ⏳ **Em Resgate**: Resgatadas mas não liquidadas
- ✅ **Resgate Liquidado**: Resgatadas e já disponíveis
- 🔒 **Fechado/Indisponível**: Sem cotação

### Gráficos
- **Pizza - Composição por Empresa**: Distribuição de valores
- **Pizza - Composição por Tipo**: Fundo vs Renda Fixa vs outros

### Tabela Detalhada (Filtrável)
Colunas incluem:
- Fundo/Ativo
- Empresa
- Tipo
- Status original
- Atualização
- Posição (formatada e numérica)
- Dias para cotização (display)
- Dias para liquidação (display)
- **Data Cotização** (calculada)
- **Data Disponibilidade** (calculada)
- Disponível Hoje? (sim/não)
- Dias restantes para cotização
- Dias úteis restantes para liquidação
- Classificação Operacional

### Filtros
- **Empresa**: Multiselect
- **Tipo**: Multiselect
- **Status**: Multiselect

### Export
- Download em CSV dos dados filtrados

---

## 🧪 Testes

Run tests with pytest:
```bash
pytest tests/
```

Testes cobrem:
- ✅ Parsing de BRL
- ✅ Parsing de datas
- ✅ Parsing misto (dias vs data vs "Fechado")
- ✅ Dias úteis (pulando fins de semana)
- ✅ Feriados (01/01, etc)
- ✅ Cálculos de liquidação
- ✅ Casos edge (vazio, zero dias, etc)

---

## 📁 Estrutura

```
posicao_investimentos/
├── app.py                    # App principal Streamlit
├── requirements.txt          # Dependências Python
├── README.md                 # Este arquivo
├── data/
│   └── posicao.xlsx          # Arquivo de entrada (exemplo)
├── src/
│   ├── __init__.py
│   ├── parsers.py            # Parse BRL, datas, dias
│   ├── dates.py              # Cálculos de data, dias úteis, feriados
│   └── metrics.py            # Cálculos de KPIs e classificações
└── tests/
    └── test_dates.py         # Testes unitários
```

---

## 🔐 Segurança

- ✅ Nenhum CDN externo
- ✅ Tudo em Python puro
- ✅ Dados locais ou via GitHub RAW (sem autenticação necessária)
- ✅ Cache Streamlit automático

---

## 🚧 Próximas Versões

- [ ] Histórico de posições (trend analysis)
- [ ] Alertas de vencimentos próximos
- [ ] Integração com APIs de preços de ativos
- [ ] Relatórios em PDF
- [ ] Dashboard mobile-friendly

---

## 📝 Changelog

### v1.0.0 (PRE-RELEASE)
- Implementação inicial
- Parsing BRL, datas, dias
- Cálculos de cotização e liquidação
- KPIs e classificações
- Tabela filtrável
- Export CSV
- Suporte GitHub RAW

---

## 📞 Suporte

Para dúvidas sobre:
- **Parsing**: Ver `src/parsers.py`
- **Datas e dias úteis**: Ver `src/dates.py`
- **Cálculos**: Ver `src/metrics.py`

---

**⚠️ Status**: PRE-RELEASE - Não publicado no GitHub até aprovação final.
