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
DB_PATH = "malga_datamart.db"

# --- CONFIGURAÇÕES DE SINCRONIZAÇÃO ---
SYNC_INTERVAL_MINUTES = 1  # Worker roda a cada 1 minuto
MAX_TRANSACTIONS_PER_SYNC = 1000  # Máximo de transações por sincronização
API_TIMEOUT = 15  # Timeout de requisições em segundos
MAX_API_PAGES = 10  # Máximo de páginas da API por sincronização

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
LOG_FILE = 'malga_worker.log'
