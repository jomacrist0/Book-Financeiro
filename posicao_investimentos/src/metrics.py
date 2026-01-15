"""
Módulo de Métricas - Cálculos de posição, classificação e KPIs
"""

import pandas as pd
from datetime import datetime
from typing import Dict, Optional

from parsers import parse_brl, parse_data, parse_dias_cotizacao, parse_dias_liquidacao
from dates import add_calendar_days, add_business_days, FERIADOS_2026_2027


def processar_posicao(row: pd.Series) -> Dict:
    """
    Processa uma linha do DataFrame e retorna dicionário com cálculos
    
    Args:
        row: Serie do DataFrame com colunas do arquivo
    
    Returns:
        dict: com chaves:
            - Posicao_Numerica (float)
            - Posicao_Formatada (str)
            - Data_Cotizacao (datetime ou None)
            - Data_Disponibilidade (datetime ou None)
            - Dias_Cotizacao_Display (str - exibição amigável)
            - Dias_Liquidacao_Display (str - exibição amigável)
            - Disponivel_Hoje (bool)
            - Dias_Restantes_Cotizacao (int ou None)
            - Dias_Uteis_Restantes_Liquidacao (int ou None)
            - Classificacao_Operacional (str)
    """
    
    # Parse de entrada
    posicao_num = parse_brl(row['Posição_Atual'])
    posicao_fmt = f"R$ {posicao_num:,.2f}"
    
    data_atualizacao = parse_data(row['Atualização'])
    if data_atualizacao is None:
        data_atualizacao = datetime.now()
    
    dias_cot_int, data_cot_fixa = parse_dias_cotizacao(row['Dias_para_Cotização'])
    dias_liq_int, data_liq_fixa = parse_dias_liquidacao(row['Dias_pra_Liquidação'])
    
    # Calcular data_cotizacao
    data_cotizacao = None
    if data_cot_fixa:
        data_cotizacao = data_cot_fixa
    elif dias_cot_int is not None:
        data_cotizacao = add_calendar_days(data_atualizacao, dias_cot_int)
    # else: Fechado ou inválido -> None
    
    # Calcular data_disponibilidade
    data_disponibilidade = None
    if data_liq_fixa:
        data_disponibilidade = data_liq_fixa
    elif data_cotizacao and dias_liq_int is not None:
        data_disponibilidade = add_business_days(data_cotizacao, dias_liq_int, FERIADOS_2026_2027)
    elif data_cotizacao and dias_liq_int is None:
        # Regra: se liquidação vazia mas tipo indicar liquidez imediata -> 0 dias úteis
        tipo = str(row.get('Tipo', '')).strip().lower()
        if 'imediato' in tipo or 'overnight' in tipo or 'renda fixa' in tipo:
            data_disponibilidade = data_cotizacao
        # else: deixar None
    
    # Display amigável
    dias_cot_display = str(row['Dias_para_Cotização'])
    dias_liq_display = str(row['Dias_pra_Liquidação']) if pd.notna(row['Dias_pra_Liquidação']) else "N/A"
    
    # Disponível hoje?
    disponivel_hoje = False
    if data_disponibilidade and data_disponibilidade.date() <= datetime.now().date() and data_cotizacao:
        disponivel_hoje = True
    
    # Dias restantes (cotização)
    dias_restantes_cot = None
    if data_cotizacao:
        dias_restantes_cot = max(0, (data_cotizacao - datetime.now()).days)
    
    # Dias úteis restantes (liquidação)
    dias_uteis_rest_liq = None
    if data_disponibilidade:
        dias_uteis_rest_liq = max(0, (data_disponibilidade - datetime.now()).days)
    
    # Classificação operacional
    classificacao = classificar_posicao(
        status=row['Status'],
        data_cotizacao=data_cotizacao,
        data_disponibilidade=data_disponibilidade
    )
    
    return {
        'Posicao_Numerica': posicao_num,
        'Posicao_Formatada': posicao_fmt,
        'Data_Cotizacao': data_cotizacao,
        'Data_Disponibilidade': data_disponibilidade,
        'Dias_Cotizacao_Display': dias_cot_display,
        'Dias_Liquidacao_Display': dias_liq_display,
        'Disponivel_Hoje': disponivel_hoje,
        'Dias_Restantes_Cotizacao': dias_restantes_cot,
        'Dias_Uteis_Restantes_Liquidacao': dias_uteis_rest_liq,
        'Classificacao_Operacional': classificacao,
    }


def classificar_posicao(
    status: str,
    data_cotizacao: Optional[datetime],
    data_disponibilidade: Optional[datetime]
) -> str:
    """
    Classifica a posição em categoria operacional
    
    Categorias:
    - Fechado-Indisponível: sem cotação
    - Aplicado: status != Resgatado, não fechado
    - Em Resgate: status == Resgatado, hoje < data_disponibilidade
    - Resgate Liquidado: status == Resgatado, hoje >= data_disponibilidade
    """
    
    if data_cotizacao is None:
        return "Fechado-Indisponível"
    
    status_clean = str(status).strip().lower()
    hoje = datetime.now().date()
    
    if "resgatado" in status_clean:
        if data_disponibilidade is None:
            return "Em Resgate"
        elif data_disponibilidade.date() <= hoje:
            return "Resgate Liquidado"
        else:
            return "Em Resgate"
    else:
        return "Aplicado"


def calcular_metricas(df: pd.DataFrame) -> Dict:
    """
    Calcula KPIs consolidados do DataFrame
    
    Args:
        df: DataFrame com posições processadas
    
    Returns:
        dict com KPIs:
            - total_carteira
            - total_aplicado
            - total_em_resgate
            - total_resgate_liquidado
            - total_fechado
            - total_disponivel_hoje
    """
    
    # Garantir que Posicao_Numerica existe
    if 'Posicao_Numerica' not in df.columns:
        df['Posicao_Numerica'] = df['Posição_Atual'].apply(lambda x: parse_brl(x))
    
    if 'Classificacao_Operacional' not in df.columns:
        df = df.apply(
            lambda row: pd.Series({
                **row,
                **processar_posicao(row)
            }),
            axis=1
        )
    
    total_carteira = df['Posicao_Numerica'].sum()
    
    # Aplicado
    total_aplicado = df[df['Classificacao_Operacional'] == 'Aplicado']['Posicao_Numerica'].sum()
    
    # Em Resgate
    total_em_resgate = df[df['Classificacao_Operacional'] == 'Em Resgate']['Posicao_Numerica'].sum()
    
    # Resgate Liquidado
    total_resgate_liquidado = df[df['Classificacao_Operacional'] == 'Resgate Liquidado']['Posicao_Numerica'].sum()
    
    # Fechado
    total_fechado = df[df['Classificacao_Operacional'] == 'Fechado-Indisponível']['Posicao_Numerica'].sum()
    
    # Disponível hoje
    if 'Disponivel_Hoje' in df.columns:
        total_disponivel_hoje = df[df['Disponivel_Hoje'] == True]['Posicao_Numerica'].sum()
    else:
        total_disponivel_hoje = 0.0
    
    return {
        'total_carteira': total_carteira,
        'total_aplicado': total_aplicado,
        'total_em_resgate': total_em_resgate,
        'total_resgate_liquidado': total_resgate_liquidado,
        'total_fechado': total_fechado,
        'total_disponivel_hoje': total_disponivel_hoje,
    }
