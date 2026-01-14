# -*- coding: utf-8 -*-
"""
Script de Debug - Testa Worker e mostra diagnóstico completo
"""

import sys
import os
from datetime import datetime
import pytz
import pandas as pd

# Adiciona worker ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'worker'))

from worker.config import *
from worker.malga_worker import MalgaWorker
from worker.malga_database import MalgaDatabase

BRASILIA_TZ = pytz.timezone('America/Sao_Paulo')

def diagnose_system():
    """Diagnóstico completo do sistema"""
    print("="*60)
    print("🔍 DIAGNÓSTICO COMPLETO DO SISTEMA")
    print("="*60)
    
    # 1. Verificar configurações
    print("\n📋 1. CONFIGURAÇÕES")
    print(f"   Client ID: {MALGA_CLIENT_ID[:20]}...")
    print(f"   API Secret: {MALGA_CLIENT_SECRET[:20]}...")
    print(f"   API Endpoint: {API_ENDPOINT}")
    print(f"   Banco de dados: {DB_PATH}")
    print(f"   Intervalo sync: {SYNC_INTERVAL_MINUTES} minuto(s)")
    print(f"   Limite transações: {MAX_TRANSACTIONS_PER_SYNC}")
    
    # 2. Verificar se banco existe
    print("\n📋 2. BANCO DE DADOS")
    if os.path.exists(DB_PATH):
        size_mb = os.path.getsize(DB_PATH) / (1024*1024)
        mtime = datetime.fromtimestamp(os.path.getmtime(DB_PATH))
        print(f"   ✅ Banco existe")
        print(f"   📦 Tamanho: {size_mb:.2f} MB")
        print(f"   🕐 Última modificação: {mtime.strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Ver estatísticas
        db = MalgaDatabase()
        stats = db.get_database_stats()
        sync_info = db.get_last_sync_info()
        
        print(f"   📊 Transações no banco: {stats['total_transactions']:,}")
        print(f"   📊 Métricas/minuto: {stats.get('metrics_by_minute', 0)}")
        print(f"   📊 Métricas/hora: {stats.get('metrics_by_hour', 0)}")
        print(f"   📊 Métricas/dia: {stats.get('metrics_by_day', 0)}")
        
        if sync_info:
            last_sync_str = sync_info[1]
            last_sync = pd.to_datetime(last_sync_str, format='ISO8601')
            if last_sync.tzinfo is None:
                last_sync = pytz.UTC.localize(last_sync)
            last_sync_brasilia = last_sync.astimezone(BRASILIA_TZ)
            now_brasilia = datetime.now(BRASILIA_TZ)
            diff = now_brasilia - last_sync_brasilia
            minutes_ago = int(diff.total_seconds() / 60)
            
            print(f"   🕐 Última sincronização: {last_sync_brasilia.strftime('%d/%m/%Y %H:%M:%S')} (Brasília)")
            print(f"   ⏱️  Há {minutes_ago} minuto(s) atrás")
            
            if minutes_ago > 5:
                print(f"   ⚠️  ALERTA: Worker pode não estar rodando!")
        else:
            print(f"   ⚠️ Nenhuma sincronização registrada")
    else:
        print(f"   ❌ Banco NÃO existe em: {DB_PATH}")
        print(f"   📁 Diretório data/ existe? {os.path.exists(os.path.dirname(DB_PATH))}")
    
    # 3. Testar autenticação na API
    print("\n📋 3. TESTE DE AUTENTICAÇÃO API")
    try:
        import requests
        headers = {
            "X-Client-Id": MALGA_CLIENT_ID,
            "X-Api-Key": MALGA_CLIENT_SECRET,
            "Accept": "application/json"
        }
        
        print(f"   🔐 Testando autenticação...")
        response = requests.get(
            f"{API_ENDPOINT}?limit=1",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"   ✅ API respondendo (HTTP 200)")
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                print(f"   ✅ Dados disponíveis na API")
                print(f"   📊 Primeira transação ID: {data['items'][0].get('id', 'N/A')}")
                print(f"   📅 Data: {data['items'][0].get('createdAt', 'N/A')}")
            else:
                print(f"   ⚠️ API respondeu mas sem dados")
                print(f"   Resposta: {data}")
        elif response.status_code == 401:
            print(f"   ❌ ERRO DE AUTENTICAÇÃO (HTTP 401)")
            print(f"   🔑 Verifique as credenciais em worker/config.py")
            print(f"   Resposta: {response.text[:200]}")
        else:
            print(f"   ❌ Erro na API: HTTP {response.status_code}")
            print(f"   Resposta: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Erro ao testar API: {str(e)}")
    
    # 4. Verificar logs
    print("\n📋 4. VERIFICAÇÃO DE LOGS")
    if os.path.exists(LOG_FILE):
        size_kb = os.path.getsize(LOG_FILE) / 1024
        mtime = datetime.fromtimestamp(os.path.getmtime(LOG_FILE))
        print(f"   ✅ Log existe: {LOG_FILE}")
        print(f"   📦 Tamanho: {size_kb:.2f} KB")
        print(f"   🕐 Última modificação: {mtime.strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Ler últimas 10 linhas
        print(f"\n   📄 Últimas 10 linhas do log:")
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[-10:]:
                    print(f"      {line.rstrip()}")
        except Exception as e:
            print(f"   ⚠️ Erro ao ler log: {e}")
    else:
        print(f"   ⚠️ Log não existe: {LOG_FILE}")
        print(f"   📁 Diretório logs/ existe? {os.path.exists(LOG_DIR)}")
    
    # 5. Executar sincronização de teste
    print("\n📋 5. EXECUTANDO SINCRONIZAÇÃO DE TESTE")
    print("   (Isso pode levar alguns minutos...)")
    
    try:
        worker = MalgaWorker()
        print(f"   ✅ Worker inicializado")
        
        # Executar sync
        worker.sync_and_aggregate()
        
        print(f"\n   ✅ Sincronização concluída!")
        
        # Verificar banco novamente
        db = MalgaDatabase()
        stats_after = db.get_database_stats()
        sync_info_after = db.get_last_sync_info()
        
        print(f"\n📋 6. RESULTADOS PÓS-SINCRONIZAÇÃO")
        print(f"   📊 Total no banco agora: {stats_after['total_transactions']:,}")
        
        if sync_info_after:
            last_sync_str = sync_info_after[1]
            last_sync = pd.to_datetime(last_sync_str, format='ISO8601')
            if last_sync.tzinfo is None:
                last_sync = pytz.UTC.localize(last_sync)
            last_sync_brasilia = last_sync.astimezone(BRASILIA_TZ)
            print(f"   🕐 Última sync: {last_sync_brasilia.strftime('%d/%m/%Y %H:%M:%S')} (Brasília)")
        
        # Verificar se tem dados
        if stats_after['total_transactions'] > 0:
            print(f"\n   ✅ SUCESSO! Banco tem {stats_after['total_transactions']:,} transações")
            print(f"   ✅ Dashboard deve funcionar corretamente agora")
        else:
            print(f"\n   ⚠️ ATENÇÃO: Banco ainda vazio após sincronização")
            print(f"   Possível causa: API não retornou dados")
        
    except Exception as e:
        print(f"\n   ❌ Erro na sincronização: {str(e)}")
        import traceback
        print("\n   📋 Stack trace completo:")
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("✅ DIAGNÓSTICO CONCLUÍDO")
    print("="*60)
    
    # Recomendações
    print("\n📋 RECOMENDAÇÕES:")
    
    if not os.path.exists(DB_PATH):
        print("   ❌ Banco não existe - Execute: python test_worker_once.py")
    elif stats_after['total_transactions'] == 0:
        print("   ⚠️ Banco vazio - Verifique credenciais da API")
    else:
        print("   ✅ Sistema funcionando!")
        print("   ▶️ Próximo passo:")
        print("      1. Terminal 1: python run_worker.py")
        print("      2. Terminal 2: streamlit run Pagina_inicial.py")

if __name__ == "__main__":
    try:
        diagnose_system()
    except KeyboardInterrupt:
        print("\n⚠️ Diagnóstico interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {str(e)}")
        import traceback
        traceback.print_exc()
