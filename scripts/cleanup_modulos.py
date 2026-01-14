#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script para remover a seção "Módulos Disponíveis" do arquivo Pagina_inicial.py

def limpar_arquivo():
    with open('Pagina_inicial.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Encontrar onde termina o FinanceBot e começa os módulos
    new_lines = []
    found_financebot_end = False
    
    for i, line in enumerate(lines):
        # Procurar pela linha que fecha a div do chat
        if "st.markdown('</div>', unsafe_allow_html=True)" in line and i > 1000:
            new_lines.append(line)
            found_financebot_end = True
            break
        else:
            new_lines.append(line)
    
    if found_financebot_end:
        with open('Pagina_inicial.py', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("✅ Seção 'Módulos Disponíveis' removida com sucesso!")
        print(f"📄 Arquivo reduzido de {len(lines)} para {len(new_lines)} linhas")
    else:
        print("❌ Não foi possível encontrar o final do FinanceBot")

if __name__ == "__main__":
    limpar_arquivo()
