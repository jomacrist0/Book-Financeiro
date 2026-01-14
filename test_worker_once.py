# -*- coding: utf-8 -*-
"""
Script de Teste - Execução Única do Worker
Executa o worker UMA VEZ para testar com limite de 2000 transações
NÃO entra em loop - ideal para testes controlados
"""

import sys
import os
import logging
from datetime import datetime

# Adiciona pasta worker ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'worker'))

from worker.malga_worker import MalgaWorker

# --- CONFIGURAÇÃO DE LOGGING PARA TESTE ---
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'test_worker.log'), encoding='utf-8'),
        logging.StreamHandler()  # Também imprime no console
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Executa worker UMA VEZ e mostra resultados"""
    logger.info("=" * 80)
    logger.info("🧪 TESTE WORKER - EXECUÇÃO ÚNICA")
    logger.info("=" * 80)
    logger.info(f"⏰ Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info("")
    
    try:
        # Cria worker
        worker = MalgaWorker()
        
        # Executa sincronização
        logger.info("🚀 Iniciando sincronização com limite de 2000 transações...")
        worker.sync_and_aggregate()
        
        # Mostra estatísticas finais
        logger.info("")
        logger.info("=" * 80)
        logger.info("📊 ESTATÍSTICAS FINAIS")
        logger.info("=" * 80)
        
        # Busca informações do banco
        sync_info = worker.db.get_last_sync_info()
        if sync_info:
            logger.info(f"✅ Última sincronização: {sync_info[1]}")
            logger.info(f"✅ Total de transações no banco: {sync_info[2]}")
        
        logger.info("")
        logger.info(f"⏰ Fim: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        logger.info("✅ TESTE CONCLUÍDO COM SUCESSO")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error("=" * 80)
        logger.error(f"❌ ERRO NO TESTE: {e}")
        logger.error("=" * 80)
        raise
    
if __name__ == "__main__":
    main()
