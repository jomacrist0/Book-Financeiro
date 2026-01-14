import pandas as pd
import os

# Tentar múltiplos caminhos
possible_paths = [
    os.path.join(os.path.dirname(__file__), "data", "1Saldos - ecossistema.xlsx"),
    os.path.join(os.getcwd(), "data", "1Saldos - ecossistema.xlsx"),
    os.path.join("data", "1Saldos - ecossistema.xlsx"),
    os.path.join(os.path.dirname(__file__), "1Saldos - ecossistema.xlsx"),
    os.path.join(os.getcwd(), "1Saldos - ecossistema.xlsx"),
    "1Saldos - ecossistema.xlsx"
]

print("🔍 Procurando arquivo...")
print(f"Diretório atual: {os.getcwd()}")
print(f"Diretório do script: {os.path.dirname(__file__)}\n")

xlsx_path = None
for path in possible_paths:
    exists = os.path.exists(path)
    print(f"{'✅' if exists else '❌'} {path}")
    if exists and xlsx_path is None:
        xlsx_path = path

if xlsx_path:
    print(f"\n✅ Arquivo encontrado: {xlsx_path}")
    print(f"Tamanho: {os.path.getsize(xlsx_path)} bytes")
    print(f"Modificado: {pd.Timestamp.utcfromtimestamp(os.path.getmtime(xlsx_path))}")
    
    # Ler e exibir informações
    df = pd.read_excel(xlsx_path)
    print(f"\n📊 Colunas encontradas:")
    for i, col in enumerate(df.columns):
        print(f"  {i+1}. '{col}'")
    
    print(f"\n📈 Primeiras linhas:")
    print(df.head())
    
    print(f"\n📋 Total de registros: {len(df)}")
else:
    print("\n❌ Arquivo não encontrado em nenhum caminho!")
