"""
Módulo de Datas - Cálculos de datas com feriados e dias úteis
Timezone: America/Bahia (compatível com mercado financeiro Brasil)
"""

from datetime import datetime, timedelta
from typing import List, Optional

# FERIADOS 2026 e 2027 (formato: datetime object)
FERIADOS_2026_2027 = [
    # 2026
    datetime(2026, 1, 1),   # Ano Novo
    datetime(2026, 2, 16),  # Segunda de Carnaval
    datetime(2026, 2, 17),  # Terça de Carnaval
    datetime(2026, 4, 3),   # Sexta-feira Santa
    datetime(2026, 4, 21),  # Tiradentes
    datetime(2026, 5, 1),   # Dia do Trabalho
    datetime(2026, 6, 4),   # Corpus Christi
    datetime(2026, 9, 7),   # Independência
    datetime(2026, 10, 12), # Nossa Senhora Aparecida
    datetime(2026, 11, 2),  # Finados
    datetime(2026, 11, 15), # Proclamação da República
    datetime(2026, 11, 20), # Consciência Negra
    datetime(2026, 12, 25), # Natal
    
    # 2027
    datetime(2027, 1, 1),   # Ano Novo
    datetime(2027, 2, 8),   # Segunda de Carnaval
    datetime(2027, 2, 9),   # Terça de Carnaval
    datetime(2027, 3, 26),  # Sexta-feira Santa
    datetime(2027, 4, 21),  # Tiradentes
    datetime(2027, 5, 1),   # Dia do Trabalho
    datetime(2027, 5, 27),  # Corpus Christi
    datetime(2027, 9, 7),   # Independência
    datetime(2027, 10, 12), # Nossa Senhora Aparecida
    datetime(2027, 11, 2),  # Finados
    datetime(2027, 11, 15), # Proclamação da República
    datetime(2027, 11, 20), # Consciência Negra
    datetime(2027, 12, 25), # Natal
]


def is_business_day(date: datetime, holidays: List[datetime] = None) -> bool:
    """
    Verifica se uma data é dia útil (não é sábado, domingo ou feriado)
    
    Args:
        date: datetime a verificar
        holidays: lista de feriados (padrão: FERIADOS_2026_2027)
    
    Returns:
        bool: True se é dia útil
    """
    if holidays is None:
        holidays = FERIADOS_2026_2027
    
    # Sábado = 5, Domingo = 6
    if date.weekday() >= 5:
        return False
    
    # Verificar se é feriado
    if date.date() in [h.date() for h in holidays]:
        return False
    
    return True


def add_business_days(start_date: datetime, business_days: int, holidays: List[datetime] = None) -> datetime:
    """
    Adiciona N dias úteis a uma data, pulando fins de semana e feriados
    
    Args:
        start_date: data inicial
        business_days: número de dias úteis a adicionar
        holidays: lista de feriados (padrão: FERIADOS_2026_2027)
    
    Returns:
        datetime: data final após adicionar dias úteis
    
    Exemplo:
        start = datetime(2026, 1, 2)  # Sexta-feira
        result = add_business_days(start, 1)
        # result = datetime(2026, 1, 5)  # Próxima segunda-feira (pulou fim de semana)
    """
    if holidays is None:
        holidays = FERIADOS_2026_2027
    
    current_date = start_date
    days_added = 0
    
    while days_added < business_days:
        current_date += timedelta(days=1)
        if is_business_day(current_date, holidays):
            days_added += 1
    
    return current_date


def business_days_between(start_date: datetime, end_date: datetime, holidays: List[datetime] = None) -> int:
    """
    Calcula número de dias úteis entre duas datas
    
    Args:
        start_date: data inicial
        end_date: data final
        holidays: lista de feriados (padrão: FERIADOS_2026_2027)
    
    Returns:
        int: número de dias úteis (excluindo start_date, incluindo end_date)
    """
    if holidays is None:
        holidays = FERIADOS_2026_2027
    
    if start_date >= end_date:
        return 0
    
    business_days = 0
    current_date = start_date + timedelta(days=1)
    
    while current_date <= end_date:
        if is_business_day(current_date, holidays):
            business_days += 1
        current_date += timedelta(days=1)
    
    return business_days


def add_calendar_days(start_date: datetime, calendar_days: int) -> datetime:
    """
    Adiciona N dias corridos (simples)
    
    Args:
        start_date: data inicial
        calendar_days: número de dias corridos a adicionar
    
    Returns:
        datetime: data final
    """
    return start_date + timedelta(days=calendar_days)


def dias_restantes_cotizacao(data_atualizacao: datetime, dias_cotizacao: Optional[int]) -> Optional[int]:
    """
    Calcula dias corridos restantes até cotização
    
    Args:
        data_atualizacao: quando foi atualizado
        dias_cotizacao: dias corridos até cotização (ou None se fechado/data)
    
    Returns:
        int: dias restantes (mín. 0), ou None se N/A
    """
    if dias_cotizacao is None:
        return None
    
    data_cotizacao = add_calendar_days(data_atualizacao, dias_cotizacao)
    dias_restantes = (data_cotizacao - datetime.now()).days
    
    return max(0, dias_restantes)


def dias_uteis_restantes_liquidacao(
    data_cotizacao: Optional[datetime],
    dias_liquidacao: Optional[int],
    holidays: List[datetime] = None
) -> Optional[int]:
    """
    Calcula dias úteis restantes até liquidação
    
    Args:
        data_cotizacao: data de cotização (ponto de partida)
        dias_liquidacao: dias úteis até liquidação (ou None se N/A)
        holidays: lista de feriados
    
    Returns:
        int: dias úteis restantes (mín. 0), ou None se N/A
    """
    if data_cotizacao is None or dias_liquidacao is None:
        return None
    
    if holidays is None:
        holidays = FERIADOS_2026_2027
    
    data_disponibilidade = add_business_days(data_cotizacao, dias_liquidacao, holidays)
    dias_restantes = (data_disponibilidade - datetime.now()).days
    
    # Para dias úteis, contar quantos dia úteis restam
    if dias_restantes <= 0:
        return 0
    
    # Simplificado: usar business_days_between
    return business_days_between(datetime.now(), data_disponibilidade, holidays)
