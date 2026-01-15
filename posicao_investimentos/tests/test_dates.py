"""
Testes unitários para módulo de datas
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from datetime import datetime
from dates import (
    is_business_day,
    add_business_days,
    business_days_between,
    add_calendar_days,
    FERIADOS_2026_2027
)


class TestIsBusinessDay:
    """Testa identificação de dias úteis"""
    
    def test_segunda_eh_util(self):
        """Segunda-feira é dia útil"""
        segunda = datetime(2026, 1, 5)  # 05/01/2026 é segunda
        assert is_business_day(segunda)
    
    def test_sabado_nao_eh_util(self):
        """Sábado não é dia útil"""
        sabado = datetime(2026, 1, 3)  # 03/01/2026 é sábado
        assert not is_business_day(sabado)
    
    def test_domingo_nao_eh_util(self):
        """Domingo não é dia útil"""
        domingo = datetime(2026, 1, 4)  # 04/01/2026 é domingo
        assert not is_business_day(domingo)
    
    def test_feriado_nao_eh_util(self):
        """Feriado (01/01) não é dia útil"""
        feriado = datetime(2026, 1, 1)
        assert not is_business_day(feriado)


class TestAddBusinessDays:
    """Testa adição de dias úteis"""
    
    def test_adicionar_um_dia_util_sexta(self):
        """De sexta-feira (02/01) + 1 dia útil = segunda-feira (05/01)"""
        sexta = datetime(2026, 1, 2)
        resultado = add_business_days(sexta, 1)
        esperado = datetime(2026, 1, 5)
        assert resultado == esperado
    
    def test_adicionar_um_dia_util_segunda(self):
        """De segunda-feira (05/01) + 1 dia útil = terça-feira (06/01)"""
        segunda = datetime(2026, 1, 5)
        resultado = add_business_days(segunda, 1)
        esperado = datetime(2026, 1, 6)
        assert resultado == esperado
    
    def test_pulando_feriado_ano_novo(self):
        """31/12/2025 + 1 dia útil = 02/01/2026 (pula Ano Novo)"""
        vespera = datetime(2025, 12, 31)
        resultado = add_business_days(vespera, 1)
        esperado = datetime(2026, 1, 2)  # Sexta
        assert resultado == esperado
    
    def test_adicionar_multiplos_dias_uteis(self):
        """02/01/2026 (sexta) + 3 dias úteis = 07/01/2026 (quarta)"""
        data_inicio = datetime(2026, 1, 2)
        resultado = add_business_days(data_inicio, 3)
        # Sexta (02) -> Seg (05) -> Ter (06) -> Qua (07)
        esperado = datetime(2026, 1, 7)
        assert resultado == esperado
    
    def test_zero_dias_uteis(self):
        """Adicionar 0 dias úteis retorna a próxima data útil"""
        sexta = datetime(2026, 1, 2)
        resultado = add_business_days(sexta, 0)
        # 0 dias úteis = mantém a data
        assert resultado == sexta


class TestBusinessDaysBetween:
    """Testa contagem de dias úteis"""
    
    def test_um_dia_util_entre_sexta_segunda(self):
        """De sexta (02/01) até segunda (05/01) = 1 dia útil"""
        sexta = datetime(2026, 1, 2)
        segunda = datetime(2026, 1, 5)
        resultado = business_days_between(sexta, segunda)
        assert resultado == 1
    
    def test_cinco_dias_uteis_semana_completa(self):
        """De segunda (05/01) até sexta (09/01) = 4 dias úteis"""
        segunda = datetime(2026, 1, 5)
        sexta = datetime(2026, 1, 9)
        resultado = business_days_between(segunda, sexta)
        assert resultado == 4  # Ter, Qua, Qui, Sex (seg já está contado)
    
    def test_datas_iguais(self):
        """Datas iguais = 0 dias úteis"""
        data = datetime(2026, 1, 5)
        resultado = business_days_between(data, data)
        assert resultado == 0


class TestAddCalendarDays:
    """Testa adição de dias corridos"""
    
    def test_adicionar_um_dia_corrido(self):
        """02/01 + 1 dia = 03/01"""
        data = datetime(2026, 1, 2)
        resultado = add_calendar_days(data, 1)
        esperado = datetime(2026, 1, 3)
        assert resultado == esperado
    
    def test_adicionar_cinco_dias_corridos(self):
        """02/01 + 5 dias = 07/01"""
        data = datetime(2026, 1, 2)
        resultado = add_calendar_days(data, 5)
        esperado = datetime(2026, 1, 7)
        assert resultado == esperado


# Testes de integração
class TestCenarioCompleto:
    """Testes de cenários reais"""
    
    def test_cotizacao_5_dias_mais_liquidacao_2_dias_uteis(self):
        """
        Atualizado em 15/01 (quinta)
        Cotização em 5 dias = 20/01 (terça)
        Liquidação em 2 dias úteis = 22/01 (quinta)
        """
        atualizacao = datetime(2026, 1, 15)  # Quinta
        cotizacao = add_calendar_days(atualizacao, 5)  # 20/01 (terça)
        assert cotizacao == datetime(2026, 1, 20)
        
        disponibilidade = add_business_days(cotizacao, 2)  # +2 dias úteis
        # Ter 20 -> Qua 21 -> Qui 22
        assert disponibilidade == datetime(2026, 1, 22)
    
    def test_pulando_fim_de_semana_e_feriado(self):
        """
        31/12/2025 (quarta) + 5 dias corridos = 05/01/2026 (segunda)
        Depois +2 dias úteis = 07/01/2026 (quarta)
        """
        atualizacao = datetime(2025, 12, 31)
        cotizacao = add_calendar_days(atualizacao, 5)
        assert cotizacao == datetime(2026, 1, 5)  # Segunda
        
        # Segunda (05) + 2 dias úteis = Quarta (07)
        disponibilidade = add_business_days(cotizacao, 2)
        assert disponibilidade == datetime(2026, 1, 7)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
