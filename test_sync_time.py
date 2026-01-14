"""
Script de teste para verificar cálculo de tempo de sincronização
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
import pytz
import pandas as pd
from worker.malga_database import MalgaDatabase

BRASILIA_TZ = pytz.timezone('America/Sao_Paulo')

# Conecta ao banco
db = MalgaDatabase()
sync_info = db.get_last_sync_info()

if sync_info:
    print("="*60)
    print("🔍 TESTE DE CÁLCULO DE TEMPO DE SINCRONIZAÇÃO")
    print("="*60)
    
    last_sync_str = sync_info[1]
    print(f"\n📄 Raw do banco: {last_sync_str}")
    print(f"   Tipo: {type(last_sync_str)}")
    
    # Parse
    if isinstance(last_sync_str, str):
        last_sync_time = pd.to_datetime(last_sync_str, format='mixed', utc=True)
    else:
        last_sync_time = last_sync_str
    
    print(f"\n📅 Parsed: {last_sync_time}")
    print(f"   Timezone: {last_sync_time.tzinfo}")
    
    # Garante timezone
    if last_sync_time.tzinfo is None:
        last_sync_time = pytz.UTC.localize(last_sync_time)
    
    # Converte para UTC
    last_sync_utc = last_sync_time.astimezone(pytz.UTC)
    now_utc = datetime.now(pytz.UTC)
    
    print(f"\n🌍 UTC:")
    print(f"   Última sync: {last_sync_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"   Agora:       {now_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Calcula diferença
    time_diff = now_utc - last_sync_utc
    minutes_ago = max(0, int(time_diff.total_seconds() / 60))
    seconds_ago = int(time_diff.total_seconds())
    
    print(f"\n⏱️  Diferença:")
    print(f"   {seconds_ago} segundos = {minutes_ago} minutos")
    
    # Converte para Brasília
    last_sync_brasilia = last_sync_utc.astimezone(BRASILIA_TZ)
    now_brasilia = now_utc.astimezone(BRASILIA_TZ)
    
    print(f"\n🇧🇷 Brasília (GMT-3):")
    print(f"   Última sync: {last_sync_brasilia.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"   Agora:       {now_brasilia.strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Status
    print(f"\n📊 Status:")
    if minutes_ago <= 1:
        print(f"   ✅ ONLINE - Sincronizado há {minutes_ago} minuto(s)")
    elif minutes_ago <= 3:
        print(f"   ⚠️  ATENÇÃO - Última sync há {minutes_ago} minuto(s)")
    else:
        print(f"   ❌ ALERTA - Worker parado há {minutes_ago} minuto(s)!")
    
    print("\n" + "="*60)
else:
    print("❌ Nenhuma sincronização encontrada no banco!")
