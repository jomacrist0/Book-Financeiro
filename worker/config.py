# -*- coding: utf-8 -*-
"""
Configurações centralizadas para o sistema Malga
"""

import os
import pytz

# --- CREDENCIAIS API MALGA ---
MALGA_CLIENT_ID = "af94ea85-d55f-4458-a7e6-0ce2574472c7"
MALGA_CLIENT_SECRET = "7bd92a23-bb31-4b98-9b77-3fb3be94ecbb"
API_ENDPOINT = "https://api.malga.io/v1/charges"

# --- BANCO DE DADOS ---
# Caminho relativo à raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "malga_datamart.db")

# --- CONFIGURAÇÕES DE SINCRONIZAÇÃO ---
SYNC_INTERVAL_MINUTES = 1  # Worker roda a cada 1 minuto
MAX_TRANSACTIONS_PER_SYNC = 10000  # Limite de 10.000 transações por sincronização
API_TIMEOUT = 30  # Timeout de requisições em segundos
MAX_API_PAGES = 100  # 100 páginas × 100 = 10.000 transações máximo

# --- TIMEZONE ---
BRAZIL_TZ = pytz.timezone('America/Sao_Paulo')

# --- DEFINIÇÕES DE STATUS ---
APPROVED_STATUSES = ['authorized', 'pre_authorized', 'paid', 'captured']
CANCELLED_STATUSES = ['canceled', 'cancelled', 'void']
REFUNDED_STATUSES = ['refunded', 'refund', 'chargeback']
FAILED_STATUSES = ['failed', 'declined', 'error']

# --- CONFIGURAÇÕES DE AGREGAÇÃO ---
# Define quais períodos serão pré-calculados
AGGREGATION_PERIODS = ['minute', 'hour', 'day']

# --- CONFIGURAÇÕES DE LOGGING ---
LOG_LEVEL = 'INFO'
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "malga_worker.log")

# Cria diretório de logs se não existir
os.makedirs(LOG_DIR, exist_ok=True)
