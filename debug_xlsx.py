import pandas as pd
import os

xlsx_path = os.path.join('data', '1Saldos - ecossistema.xlsx')
print(f'Arquivo existe: {os.path.exists(xlsx_path)}')
print(f'Caminho absoluto: {os.path.abspath(xlsx_path)}')

if os.path.exists(xlsx_path):
    try:
        df = pd.read_excel(xlsx_path)
        print(f'\n✅ Arquivo carregado com sucesso!')
        print(f'Total de linhas: {len(df)}')
        print(f'Colunas: {list(df.columns)}')
        
        # Procurar coluna de data
        data_col = None
        for col in df.columns:
            if 'data' in col.lower():
                data_col = col
                break
        
        if data_col:
            print(f'\n📅 Últimas 10 datas da coluna "{data_col}":')
            ultimas = df[data_col].tail(10).tolist()
            for i, data in enumerate(ultimas, 1):
                print(f'  {i}. {data}')
        else:
            print('\n❌ Nenhuma coluna com "data" encontrada')
            print(f'Primeiras linhas:\n{df.head()}')
            
    except Exception as e:
        print(f'❌ Erro ao carregar: {e}')
else:
    print(f'❌ Arquivo não encontrado em {os.path.abspath(xlsx_path)}')
