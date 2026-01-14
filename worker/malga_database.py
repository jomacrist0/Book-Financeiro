# -*- coding: utf-8 -*-
"""
Módulo de gerenciamento do banco de dados SQLite
Responsável por criar tabelas, inserir dados e fazer agregações
"""

import sqlite3
import pandas as pd
from datetime import datetime
from worker.config import *

class MalgaDatabase:
    """Gerenciador do banco de dados Malga"""
    
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None
        
        # Cria diretório se não existir
        import os
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        # Garante que as tabelas existam ao criar a instância
        self._ensure_tables_exist()
    
    def connect(self):
        """Conecta ao banco de dados"""
        self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def close(self):
        """Fecha conexão"""
        if self.conn:
            self.conn.close()
    
    def _ensure_tables_exist(self):
        """Garante que as tabelas existam (silencioso)"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Tabela de transações brutas (cache das transações da API)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id TEXT PRIMARY KEY,
                created_at TIMESTAMP,
                amount REAL,
                status TEXT,
                payment_method TEXT,
                card_brand TEXT,
                description TEXT,
                declined_code TEXT,
                network_denied_reason TEXT,
                network_denied_message TEXT,
                retryable INTEGER,
                raw_json TEXT,
                inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de métricas por minuto
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics_by_minute (
                timestamp TIMESTAMP PRIMARY KEY,
                total_transactions INTEGER,
                approved_count INTEGER,
                cancelled_count INTEGER,
                refunded_count INTEGER,
                failed_count INTEGER,
                approval_rate REAL,
                total_amount REAL,
                avg_ticket REAL,
                updated_at TIMESTAMP
            )
        ''')
        
        # Tabela de métricas por hora
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics_by_hour (
                timestamp TIMESTAMP PRIMARY KEY,
                total_transactions INTEGER,
                approved_count INTEGER,
                cancelled_count INTEGER,
                refunded_count INTEGER,
                failed_count INTEGER,
                approval_rate REAL,
                total_amount REAL,
                avg_ticket REAL,
                updated_at TIMESTAMP
            )
        ''')
        
        # Tabela de métricas por dia
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics_by_day (
                date TEXT PRIMARY KEY,
                total_transactions INTEGER,
                approved_count INTEGER,
                cancelled_count INTEGER,
                refunded_count INTEGER,
                failed_count INTEGER,
                approval_rate REAL,
                total_amount REAL,
                avg_ticket REAL,
                updated_at TIMESTAMP
            )
        ''')
        
        # Tabela de métricas por método de pagamento
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics_by_payment_method (
                payment_method TEXT PRIMARY KEY,
                total_transactions INTEGER,
                approved_count INTEGER,
                declined_count INTEGER,
                approval_rate REAL
            )
        ''')
        
        # Tabela de controle de sincronização
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_control (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                last_sync_time TIMESTAMP,
                last_transaction_date TIMESTAMP,
                total_synced INTEGER DEFAULT 0,
                last_error TEXT
            )
        ''')
        
        conn.commit()
        # NÃO fecha a conexão aqui! A conexão deve permanecer aberta
    
    def init_database(self):
        """Cria estrutura do banco de dados se não existir"""
        conn = self.connect()
        cursor = conn.cursor()
        
        print("🔧 Inicializando estrutura do banco de dados...")
        
        # Tabela de transações brutas (cache das transações da API)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id TEXT PRIMARY KEY,
                created_at TIMESTAMP,
                amount REAL,
                status TEXT,
                payment_method TEXT,
                card_brand TEXT,
                description TEXT,
                declined_code TEXT,
                network_denied_reason TEXT,
                network_denied_message TEXT,
                retryable INTEGER,
                raw_json TEXT,
                inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Índices para performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON transactions(created_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON transactions(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_payment_method ON transactions(payment_method)')
        
        # Tabela agregada por minuto (pré-calculada)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics_by_minute (
                timestamp TIMESTAMP PRIMARY KEY,
                total_transactions INTEGER,
                approved_count INTEGER,
                cancelled_count INTEGER,
                refunded_count INTEGER,
                failed_count INTEGER,
                approval_rate REAL,
                total_amount REAL,
                avg_ticket REAL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela agregada por hora
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics_by_hour (
                timestamp TIMESTAMP PRIMARY KEY,
                total_transactions INTEGER,
                approved_count INTEGER,
                cancelled_count INTEGER,
                refunded_count INTEGER,
                failed_count INTEGER,
                approval_rate REAL,
                total_amount REAL,
                avg_ticket REAL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela agregada por dia
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics_by_day (
                date DATE PRIMARY KEY,
                total_transactions INTEGER,
                approved_count INTEGER,
                cancelled_count INTEGER,
                refunded_count INTEGER,
                failed_count INTEGER,
                approval_rate REAL,
                total_amount REAL,
                avg_ticket REAL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela agregada por método de pagamento
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics_by_payment_method (
                payment_method TEXT,
                period_start TIMESTAMP,
                period_end TIMESTAMP,
                total_transactions INTEGER,
                approved_count INTEGER,
                approval_rate REAL,
                total_amount REAL,
                PRIMARY KEY (payment_method, period_start)
            )
        ''')
        
        # Tabela de controle de sincronização
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_control (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                last_sync_time TIMESTAMP,
                last_transaction_date TIMESTAMP,
                total_synced INTEGER DEFAULT 0,
                last_error TEXT
            )
        ''')
        
        # Inicializa controle se não existir
        cursor.execute('''
            INSERT OR IGNORE INTO sync_control (id, last_sync_time, total_synced) 
            VALUES (1, ?, 0)
        ''', (datetime.now(BRAZIL_TZ),))
        
        conn.commit()
        self.close()
        print(f"✅ Banco de dados inicializado: {self.db_path}")
    
    def insert_transactions(self, transactions_df):
        """Insere ou atualiza transações no banco"""
        if transactions_df.empty:
            return 0
        
        conn = self.connect()
        cursor = conn.cursor()
        
        # Prepara dados para inserção
        now_str = datetime.now(BRAZIL_TZ).strftime('%Y-%m-%d %H:%M:%S')
        
        inserted_count = 0
        
        # Insere linha por linha usando INSERT OR IGNORE para evitar duplicatas
        for _, row in transactions_df.iterrows():
            try:
                # Converte timestamps para string
                created_at_str = pd.to_datetime(row['created_at']).strftime('%Y-%m-%d %H:%M:%S')
                
                cursor.execute('''
                    INSERT OR IGNORE INTO transactions 
                    (id, created_at, amount, status, payment_method, card_brand, 
                     description, declined_code, network_denied_reason, network_denied_message,
                     retryable, raw_json, inserted_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['id'], created_at_str, row['amount'], row['status'],
                    row['payment_method'], row['card_brand'], row['description'],
                    row['declined_code'], row['network_denied_reason'],
                    row.get('network_denied_message', None), row.get('retryable', 0),
                    row['raw_json'], now_str
                ))
                
                if cursor.rowcount > 0:
                    inserted_count += 1
                    
            except Exception as e:
                print(f"⚠️ Erro ao inserir transação {row['id']}: {e}")
                continue
        
        conn.commit()
        self.close()
        
        return inserted_count
    
    def aggregate_by_minute(self, start_date=None, end_date=None):
        """Agrega métricas por minuto - FÓRMULA: (authorized + canceled) / (authorized + canceled + failed)"""
        conn = self.connect()
        
        where_clause = ""
        if start_date and end_date:
            where_clause = f"WHERE created_at BETWEEN '{start_date}' AND '{end_date}'"
        
        query = f"""
            INSERT OR REPLACE INTO metrics_by_minute
            SELECT 
                strftime('%Y-%m-%d %H:%M:00', created_at) as timestamp,
                COUNT(*) as total_transactions,
                SUM(CASE WHEN status IN ({','.join(['?' for _ in APPROVED_STATUSES])}) THEN 1 ELSE 0 END) as approved_count,
                SUM(CASE WHEN status IN ({','.join(['?' for _ in CANCELLED_STATUSES])}) THEN 1 ELSE 0 END) as cancelled_count,
                SUM(CASE WHEN status IN ({','.join(['?' for _ in REFUNDED_STATUSES])}) THEN 1 ELSE 0 END) as refunded_count,
                SUM(CASE WHEN status IN ({','.join(['?' for _ in FAILED_STATUSES])}) THEN 1 ELSE 0 END) as failed_count,
                CASE 
                    WHEN (SUM(CASE WHEN status IN ({','.join(['?' for _ in APPROVED_STATUSES])}) THEN 1 ELSE 0 END) + 
                          SUM(CASE WHEN status IN ({','.join(['?' for _ in CANCELLED_STATUSES])}) THEN 1 ELSE 0 END) +
                          SUM(CASE WHEN status IN ({','.join(['?' for _ in FAILED_STATUSES])}) THEN 1 ELSE 0 END)) > 0 
                    THEN CAST(SUM(CASE WHEN status IN ({','.join(['?' for _ in APPROVED_STATUSES])}) THEN 1 ELSE 0 END) + 
                              SUM(CASE WHEN status IN ({','.join(['?' for _ in CANCELLED_STATUSES])}) THEN 1 ELSE 0 END) AS FLOAT) / 
                         (SUM(CASE WHEN status IN ({','.join(['?' for _ in APPROVED_STATUSES])}) THEN 1 ELSE 0 END) + 
                          SUM(CASE WHEN status IN ({','.join(['?' for _ in CANCELLED_STATUSES])}) THEN 1 ELSE 0 END) +
                          SUM(CASE WHEN status IN ({','.join(['?' for _ in FAILED_STATUSES])}) THEN 1 ELSE 0 END)) * 100
                    ELSE 0 
                END as approval_rate,
                SUM(amount) as total_amount,
                AVG(amount) as avg_ticket,
                CURRENT_TIMESTAMP as updated_at
            FROM transactions
            {where_clause}
            GROUP BY strftime('%Y-%m-%d %H:%M:00', created_at)
        """
        
        params = APPROVED_STATUSES + CANCELLED_STATUSES + REFUNDED_STATUSES + FAILED_STATUSES + APPROVED_STATUSES + CANCELLED_STATUSES + FAILED_STATUSES + APPROVED_STATUSES + CANCELLED_STATUSES + APPROVED_STATUSES + CANCELLED_STATUSES + FAILED_STATUSES
        
        conn.execute(query, params)
        conn.commit()
        self.close()
        print("✅ Agregação por minuto concluída (nova fórmula)")
    
    def aggregate_by_hour(self):
        """Agrega métricas por hora - FÓRMULA: (authorized + canceled) / (authorized + canceled + failed)"""
        conn = self.connect()
        
        query = f"""
            INSERT OR REPLACE INTO metrics_by_hour
            SELECT 
                strftime('%Y-%m-%d %H:00:00', created_at) as timestamp,
                COUNT(*) as total_transactions,
                SUM(CASE WHEN status IN ({','.join(['?' for _ in APPROVED_STATUSES])}) THEN 1 ELSE 0 END) as approved_count,
                SUM(CASE WHEN status IN ({','.join(['?' for _ in CANCELLED_STATUSES])}) THEN 1 ELSE 0 END) as cancelled_count,
                SUM(CASE WHEN status IN ({','.join(['?' for _ in REFUNDED_STATUSES])}) THEN 1 ELSE 0 END) as refunded_count,
                SUM(CASE WHEN status IN ({','.join(['?' for _ in FAILED_STATUSES])}) THEN 1 ELSE 0 END) as failed_count,
                CASE 
                    WHEN (SUM(CASE WHEN status IN ({','.join(['?' for _ in APPROVED_STATUSES])}) THEN 1 ELSE 0 END) + 
                          SUM(CASE WHEN status IN ({','.join(['?' for _ in CANCELLED_STATUSES])}) THEN 1 ELSE 0 END) +
                          SUM(CASE WHEN status IN ({','.join(['?' for _ in FAILED_STATUSES])}) THEN 1 ELSE 0 END)) > 0 
                    THEN CAST(SUM(CASE WHEN status IN ({','.join(['?' for _ in APPROVED_STATUSES])}) THEN 1 ELSE 0 END) + 
                              SUM(CASE WHEN status IN ({','.join(['?' for _ in CANCELLED_STATUSES])}) THEN 1 ELSE 0 END) AS FLOAT) / 
                         (SUM(CASE WHEN status IN ({','.join(['?' for _ in APPROVED_STATUSES])}) THEN 1 ELSE 0 END) + 
                          SUM(CASE WHEN status IN ({','.join(['?' for _ in CANCELLED_STATUSES])}) THEN 1 ELSE 0 END) +
                          SUM(CASE WHEN status IN ({','.join(['?' for _ in FAILED_STATUSES])}) THEN 1 ELSE 0 END)) * 100
                    ELSE 0 
                END as approval_rate,
                SUM(amount) as total_amount,
                AVG(amount) as avg_ticket,
                CURRENT_TIMESTAMP as updated_at
            FROM transactions
            GROUP BY strftime('%Y-%m-%d %H:00:00', created_at)
        """
        
        params = APPROVED_STATUSES + CANCELLED_STATUSES + REFUNDED_STATUSES + FAILED_STATUSES + APPROVED_STATUSES + CANCELLED_STATUSES + FAILED_STATUSES + APPROVED_STATUSES + CANCELLED_STATUSES + APPROVED_STATUSES + CANCELLED_STATUSES + FAILED_STATUSES
        
        conn.execute(query, params)
        conn.commit()
        self.close()
        print("✅ Agregação por hora concluída (nova fórmula)")
    
    def aggregate_by_day(self):
        """Agrega métricas por dia - FÓRMULA: (authorized + canceled) / (authorized + canceled + failed)"""
        conn = self.connect()
        
        query = f"""
            INSERT OR REPLACE INTO metrics_by_day
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as total_transactions,
                SUM(CASE WHEN status IN ({','.join(['?' for _ in APPROVED_STATUSES])}) THEN 1 ELSE 0 END) as approved_count,
                SUM(CASE WHEN status IN ({','.join(['?' for _ in CANCELLED_STATUSES])}) THEN 1 ELSE 0 END) as cancelled_count,
                SUM(CASE WHEN status IN ({','.join(['?' for _ in REFUNDED_STATUSES])}) THEN 1 ELSE 0 END) as refunded_count,
                SUM(CASE WHEN status IN ({','.join(['?' for _ in FAILED_STATUSES])}) THEN 1 ELSE 0 END) as failed_count,
                CASE 
                    WHEN (SUM(CASE WHEN status IN ({','.join(['?' for _ in APPROVED_STATUSES])}) THEN 1 ELSE 0 END) + 
                          SUM(CASE WHEN status IN ({','.join(['?' for _ in CANCELLED_STATUSES])}) THEN 1 ELSE 0 END) +
                          SUM(CASE WHEN status IN ({','.join(['?' for _ in FAILED_STATUSES])}) THEN 1 ELSE 0 END)) > 0 
                    THEN CAST(SUM(CASE WHEN status IN ({','.join(['?' for _ in APPROVED_STATUSES])}) THEN 1 ELSE 0 END) + 
                              SUM(CASE WHEN status IN ({','.join(['?' for _ in CANCELLED_STATUSES])}) THEN 1 ELSE 0 END) AS FLOAT) / 
                         (SUM(CASE WHEN status IN ({','.join(['?' for _ in APPROVED_STATUSES])}) THEN 1 ELSE 0 END) + 
                          SUM(CASE WHEN status IN ({','.join(['?' for _ in CANCELLED_STATUSES])}) THEN 1 ELSE 0 END) +
                          SUM(CASE WHEN status IN ({','.join(['?' for _ in FAILED_STATUSES])}) THEN 1 ELSE 0 END)) * 100
                    ELSE 0 
                END as approval_rate,
                SUM(amount) as total_amount,
                AVG(amount) as avg_ticket,
                CURRENT_TIMESTAMP as updated_at
            FROM transactions
            GROUP BY DATE(created_at)
        """
        
        params = APPROVED_STATUSES + CANCELLED_STATUSES + REFUNDED_STATUSES + FAILED_STATUSES + APPROVED_STATUSES + CANCELLED_STATUSES + FAILED_STATUSES + APPROVED_STATUSES + CANCELLED_STATUSES + APPROVED_STATUSES + CANCELLED_STATUSES + FAILED_STATUSES
        
        conn.execute(query, params)
        conn.commit()
        self.close()
        print("✅ Agregação por dia concluída (nova fórmula)")
    
    def get_metrics_by_period(self, period='day', start_date=None, end_date=None):
        """Retorna métricas agregadas por período"""
        conn = self.connect()
        
        table_map = {
            'minute': 'metrics_by_minute',
            'hour': 'metrics_by_hour',
            'day': 'metrics_by_day'
        }
        
        table = table_map.get(period, 'metrics_by_day')
        
        where_clause = ""
        if start_date and end_date:
            # metrics_by_day usa 'date', outras usam 'timestamp'
            date_field = 'date' if period == 'day' else 'timestamp'
            where_clause = f"WHERE {date_field} BETWEEN '{start_date}' AND '{end_date}'"
        
        query = f"SELECT * FROM {table} {where_clause} ORDER BY 1 DESC"
        
        df = pd.read_sql_query(query, conn)
        self.close()
        return df
    
    def get_last_sync_info(self):
        """Retorna informações da última sincronização"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM sync_control WHERE id = 1')
        result = cursor.fetchone()
        
        self.close()
        return result
    
    def update_sync_control(self, last_transaction_date=None, total_synced=0, error=None):
        """Atualiza controle de sincronização"""
        conn = self.connect()
        cursor = conn.cursor()
        
        if last_transaction_date:
            cursor.execute('''
                UPDATE sync_control 
                SET last_sync_time = ?, 
                    last_transaction_date = ?,
                    total_synced = total_synced + ?,
                    last_error = ?
                WHERE id = 1
            ''', (datetime.now(BRAZIL_TZ), last_transaction_date, total_synced, error))
        else:
            cursor.execute('''
                UPDATE sync_control 
                SET last_sync_time = ?,
                    last_error = ?
                WHERE id = 1
            ''', (datetime.now(BRAZIL_TZ), error))
        
        conn.commit()
        self.close()
    
    def get_database_stats(self):
        """Retorna estatísticas do banco de dados"""
        conn = self.connect()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total de transações
        cursor.execute('SELECT COUNT(*) FROM transactions')
        stats['total_transactions'] = cursor.fetchone()[0]
        
        # Data mais antiga
        cursor.execute('SELECT MIN(created_at) FROM transactions')
        stats['oldest_transaction'] = cursor.fetchone()[0]
        
        # Data mais recente
        cursor.execute('SELECT MAX(created_at) FROM transactions')
        stats['newest_transaction'] = cursor.fetchone()[0]
        
        # Registros agregados
        cursor.execute('SELECT COUNT(*) FROM metrics_by_minute')
        stats['metrics_by_minute'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM metrics_by_hour')
        stats['metrics_by_hour'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM metrics_by_day')
        stats['metrics_by_day'] = cursor.fetchone()[0]
        
        self.close()
        return stats
