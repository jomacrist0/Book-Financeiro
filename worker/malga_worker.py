# -*- coding: utf-8 -*-
"""
Worker em Background para sincronização com API Malga
Roda periodicamente (a cada 1 minuto) e mantém dados agregados no SQLite
"""

import requests
import pandas as pd
import json
import time
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from worker.config import *
from worker.malga_database import MalgaDatabase

# --- CONFIGURAÇÃO DE LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# --- CLASSE PRINCIPAL DO WORKER ---

class MalgaWorker:
    """Worker para sincronização periódica com API Malga"""
    
    def __init__(self):
        self.db = MalgaDatabase()
        self.headers = None
    
    def authenticate(self):
        """Autentica na API Malga"""
        self.headers = {
            "X-Client-Id": MALGA_CLIENT_ID,
            "X-Api-Key": MALGA_CLIENT_SECRET,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            logger.info(f"🔐 Autenticando com Client-Id: {MALGA_CLIENT_ID[:20]}...")
            response = requests.get(f"{API_ENDPOINT}?limit=1", 
                                    headers=self.headers, 
                                    timeout=API_TIMEOUT)
            
            if response.status_code == 200:
                logger.info("✅ Autenticação bem-sucedida")
                return True
            elif response.status_code == 401:
                logger.error(f"❌ Credenciais inválidas (401)")
                logger.error(f"   Client-Id: {MALGA_CLIENT_ID}")
                return False
            elif response.status_code == 403:
                logger.error(f"❌ Acesso negado (403)")
                return False
            else:
                logger.error(f"❌ Erro de autenticação: HTTP {response.status_code}")
                logger.error(f"   Resposta: {response.text[:200]}")
                return False
        except Exception as e:
            logger.error(f"❌ Erro ao autenticar: {e}")
            return False
    
    def fetch_new_transactions(self, last_sync_date):
        """Busca transações novas desde última sincronização"""
        if not self.authenticate():
            return []
        
        all_transactions = []
        page = 1
        total_collected = 0
        
        # Define estratégia de busca
        if last_sync_date:
            # Sincronização incremental - busca apenas novas
            start_date = last_sync_date
            # Usa formato completo com hora para precisão
            start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%S')
            logger.info(f"🔄 Sincronização incremental desde {start_date_str}...")
            use_date_filter = True
        else:
            # Primeira sincronização - busca TUDO
            logger.info(f"🔍 PRIMEIRA SINCRONIZAÇÃO - Buscando TODAS as transações...")
            use_date_filter = False
            start_date_str = None
        
        logger.info(f"🎯 LIMITE CONFIGURADO: {MAX_TRANSACTIONS_PER_SYNC} transações")
        
        while page <= MAX_API_PAGES:
            # Define parâmetros baseado na estratégia
            if use_date_filter and start_date_str:
                params = {
                    "limit": 100,
                    "page": page,
                    "created.gt": start_date_str,  # API só aceita .gt (maior que), não .gte
                    "sort": "DESC"
                }
            else:
                params = {
                    "limit": 100,
                    "page": page,
                    "sort": "DESC"
                }
            
            try:
                logger.info(f"📡 Página {page}...")
                response = requests.get(API_ENDPOINT, 
                                        headers=self.headers, 
                                        params=params, 
                                        timeout=API_TIMEOUT)
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('items', [])
                    
                    if not items:
                        logger.info(f"📭 Página {page} sem itens - fim da busca")
                        break
                    
                    # Calcula quanto espaço ainda temos disponível
                    remaining_space = MAX_TRANSACTIONS_PER_SYNC - total_collected
                    
                    # Se o limite já foi atingido, para
                    if remaining_space <= 0:
                        logger.warning(f"� LIMITE ATINGIDO: {total_collected} transações coletadas")
                        break
                    
                    # Se esta página ultrapassaria o limite, pega só o necessário
                    if len(items) > remaining_space:
                        items = items[:remaining_space]
                        logger.info(f"✂️ Página {page}: Cortando para {remaining_space} transações (limite atingido)")
                    
                    all_transactions.extend(items)
                    total_collected = len(all_transactions)
                    
                    logger.info(f"📄 Página {page}: {len(items)} transações | Total acumulado: {total_collected}/{MAX_TRANSACTIONS_PER_SYNC}")
                    
                    # Se atingiu o limite exato, para
                    if total_collected >= MAX_TRANSACTIONS_PER_SYNC:
                        logger.warning(f"🛑 LIMITE ATINGIDO: {total_collected} transações coletadas")
                        break
                    
                    # Se retornou menos que 100, não há mais páginas
                    if len(items) < 100:
                        logger.info(f"✅ Última página alcançada (menos de 100 items)")
                        break
                    
                    page += 1
                    
                    # Rate limiting - evita sobrecarregar API
                    time.sleep(0.5)
                    
                else:
                    logger.error(f"❌ HTTP {response.status_code} - {response.text[:200]}")
                    break
                    
            except Exception as e:
                logger.error(f"❌ Erro na página {page}: {e}")
                break
        
        logger.info(f"✅ Total de {len(all_transactions)} transações coletadas")
        logger.info(f"📊 Páginas processadas: {page - 1}")
        return all_transactions
    
    def process_transactions(self, transactions):
        """Processa e transforma dados brutos da API"""
        if not transactions:
            return pd.DataFrame()
        
        processed_data = []
        
        for tx in transactions:
            try:
                # Extrai dados relevantes
                processed = {
                    'id': tx.get('id'),
                    'created_at': tx.get('createdAt'),
                    'amount': tx.get('amount', 0) / 100,  # Converte centavos para reais
                    'status': tx.get('status'),
                    'payment_method': tx.get('paymentMethod', {}).get('paymentType'),
                    'card_brand': tx.get('paymentMethod', {}).get('card', {}).get('brand'),
                    'description': tx.get('description'),
                    'declined_code': tx.get('declinedCode'),
                    'network_denied_reason': tx.get('networkDeniedReason'),
                    'network_denied_message': tx.get('networkDeniedMessage'),
                    'retryable': 1 if tx.get('retryable') else 0,
                    'raw_json': json.dumps(tx)
                }
                
                processed_data.append(processed)
                
            except Exception as e:
                logger.error(f"❌ Erro ao processar transação {tx.get('id')}: {e}")
                continue
        
        df = pd.DataFrame(processed_data)
        
        # Converte datas
        if not df.empty and 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        
        logger.info(f"✅ {len(df)} transações processadas")
        return df
    
    def sync_and_aggregate(self):
        """Executa sincronização completa e agregações"""
        logger.info("=" * 60)
        logger.info("🚀 Iniciando sincronização...")
        logger.info("=" * 60)
        
        try:
            # Verifica última sincronização
            sync_info = self.db.get_last_sync_info()
            
            if sync_info:
                last_sync = sync_info[1]
                last_transaction_date_str = sync_info[2]
                logger.info(f"📅 Última sincronização: {last_sync}")
                
                # Converte string para datetime se necessário
                if last_transaction_date_str:
                    if isinstance(last_transaction_date_str, str):
                        last_transaction_date = pd.to_datetime(last_transaction_date_str, format='mixed')
                    else:
                        last_transaction_date = last_transaction_date_str
                else:
                    last_transaction_date = None
            else:
                last_transaction_date = None
                logger.info("📅 Primeira sincronização")
            
            # Busca novas transações
            transactions = self.fetch_new_transactions(last_transaction_date)
            
            if transactions:
                # Processa transações
                df = self.process_transactions(transactions)
                
                if not df.empty:
                    # Insere no banco
                    logger.info("💾 Inserindo transações no banco...")
                    inserted_count = self.db.insert_transactions(df)
                    
                    if inserted_count > 0:
                        logger.info(f"✅ {inserted_count} transações NOVAS inseridas (de {len(df)} coletadas)")
                    else:
                        logger.info(f"ℹ️ Nenhuma transação nova (todas já existiam no banco)")
                    
                    # Pega data mais recente e converte para string
                    newest_date_str = pd.to_datetime(df['created_at'].max()).strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Agrega dados
                    logger.info("📊 Iniciando agregações...")
                    self.db.aggregate_by_minute()
                    self.db.aggregate_by_hour()
                    self.db.aggregate_by_day()
                    
                    # Atualiza controle
                    self.db.update_sync_control(
                        last_transaction_date=newest_date_str,
                        total_synced=len(df)
                    )
                    
                    logger.info(f"✅ Sincronização concluída: {len(df)} transações")
                else:
                    logger.info("ℹ️ Nenhuma transação nova encontrada")
                    self.db.update_sync_control()
            else:
                logger.info("ℹ️ Nenhuma transação nova para processar")
                self.db.update_sync_control()
            
            # Mostra estatísticas
            stats = self.db.get_database_stats()
            logger.info("📈 Estatísticas do banco:")
            logger.info(f"   - Total de transações: {stats['total_transactions']}")
            logger.info(f"   - Métricas por minuto: {stats['metrics_by_minute']}")
            logger.info(f"   - Métricas por hora: {stats['metrics_by_hour']}")
            logger.info(f"   - Métricas por dia: {stats['metrics_by_day']}")
            
        except Exception as e:
            logger.error(f"❌ Erro durante sincronização: {e}")
            self.db.update_sync_control(error=str(e))
        
        logger.info("=" * 60)
        logger.info(f"⏰ Próxima sincronização em {SYNC_INTERVAL_MINUTES} minuto(s)")
        logger.info("=" * 60)

# --- FUNÇÕES PRINCIPAIS ---

def initialize_system():
    """Inicializa sistema na primeira execução"""
    logger.info("🔧 Inicializando sistema...")
    db = MalgaDatabase()
    db.init_database()
    logger.info("✅ Sistema inicializado com sucesso!")

def start_worker():
    """Inicia worker em modo contínuo"""
    logger.info("=" * 60)
    logger.info("🚀 MALGA WORKER - INICIANDO")
    logger.info("=" * 60)
    logger.info(f"⏰ Intervalo de sincronização: {SYNC_INTERVAL_MINUTES} minuto(s)")
    logger.info(f"💾 Banco de dados: {DB_PATH}")
    logger.info("=" * 60)
    
    # Inicializa banco se necessário
    initialize_system()
    
    # Cria instância do worker
    worker = MalgaWorker()
    
    # Executa primeira sincronização imediatamente
    logger.info("🔄 Executando primeira sincronização...")
    worker.sync_and_aggregate()
    
    # Configura scheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(
        worker.sync_and_aggregate,
        'interval',
        minutes=SYNC_INTERVAL_MINUTES,
        id='malga_sync',
        name='Sincronização Malga',
        replace_existing=True
    )
    
    logger.info("✅ Worker configurado e rodando!")
    logger.info("⚠️ Pressione Ctrl+C para parar")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("⏹️ Worker finalizado pelo usuário")

if __name__ == "__main__":
    start_worker()
