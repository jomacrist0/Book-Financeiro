# -*- coding: utf-8 -*-
"""
Script de Inicialização do Worker Malga - Versão Raiz
Executa o worker da pasta worker/
"""

import sys
import os

# Adiciona pasta worker ao path
worker_dir = os.path.join(os.path.dirname(__file__), 'worker')
sys.path.insert(0, worker_dir)

# Muda para o diretório worker
os.chdir(worker_dir)

# Importa e executa o start_worker original
from start_worker import main

if __name__ == "__main__":
    print("🚀 Iniciando Worker Malga...")
    print(f"📁 Diretório: {worker_dir}")
    print("="*60)
    main()
