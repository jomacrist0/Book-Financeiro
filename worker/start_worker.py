# -*- coding: utf-8 -*-
"""
Script de Inicialização do Worker Malga
Inicia o worker de background com tratamento de erros e shutdown gracioso
"""

import os
import sys
import logging
from datetime import datetime

# Adiciona diretório ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import BRAZIL_TZ, LOG_FILE
from malga_worker import start_worker

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def print_banner():
    """Imprime banner de inicialização"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              🚀 MALGA PAYMENT WORKER 🚀                   ║
    ║                                                           ║
    ║        Sistema de Sincronização Automática                ║
    ║        API Malga → SQLite → Dashboard Streamlit          ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)
    print(f"    📅 Data/Hora: {datetime.now(BRAZIL_TZ).strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"    📂 Log File: {LOG_FILE}")
    print("    " + "="*59)
    print()

def check_dependencies():
    """Verifica dependências necessárias"""
    logger.info("🔍 Verificando dependências...")
    
    required_modules = [
        'requests',
        'pandas',
        'apscheduler',
        'sqlite3'
    ]
    
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
            logger.info(f"  ✅ {module}")
        except ImportError:
            missing.append(module)
            logger.error(f"  ❌ {module}")
    
    if missing:
        logger.error(f"\n❌ Dependências ausentes: {', '.join(missing)}")
        logger.error("Execute: pip install -r requirements.txt")
        return False
    
    logger.info("✅ Todas as dependências estão instaladas!")
    return True

def main():
    """Função principal de inicialização"""
    try:
        print_banner()
        
        # Verifica dependências
        if not check_dependencies():
            sys.exit(1)
        
        logger.info("="*60)
        logger.info("🚀 INICIANDO WORKER...")
        logger.info("="*60)
        
        # Inicia worker
        start_worker()
        
    except KeyboardInterrupt:
        logger.info("\n" + "="*60)
        logger.info("⏹️ Worker finalizado pelo usuário (Ctrl+C)")
        logger.info("="*60)
        sys.exit(0)
        
    except Exception as e:
        logger.error("="*60)
        logger.error(f"❌ ERRO FATAL: {e}")
        logger.error("="*60)
        logger.exception("Detalhes do erro:")
        sys.exit(1)

if __name__ == "__main__":
    main()
