"""
Módulo de Parsers - Converte strings em valores estruturados
"""

import pandas as pd
import re
from datetime import datetime
from typing import Union, Optional, Tuple


def parse_brl(valor: str) -> float:
    """
    Converte string BRL (ex: "R$ 2.126.062,81") em float
    
    Args:
        valor: String no formato "R$ X.XXX.XXX,XX"
    
    Returns:
        float: Valor numérico
    
    Raises:
        ValueError: Se não conseguir fazer parse
    """
    if pd.isna(valor) or valor == "" or valor == "N/A":
        return 0.0
    
    if isinstance(valor, (int, float)):
        return float(valor)
    
    valor_str = str(valor).strip()
    
    # Remove "R$" e espaços
    valor_str = valor_str.replace("R$", "").strip()
    
    # Remove separador de milhares (ponto)
    valor_str = valor_str.replace(".", "")
    
    # Troca vírgula decimal por ponto
    valor_str = valor_str.replace(",", ".")
    
    try:
        return float(valor_str)
    except ValueError:
        raise ValueError(f"Não consegui fazer parse de: '{valor}'")


def parse_data(data_str: str) -> Optional[datetime]:
    """
    Converte string dd/mm/yyyy em datetime
    
    Args:
        data_str: String no formato "dd/mm/yyyy"
    
    Returns:
        datetime ou None se inválido/vazio
    """
    if pd.isna(data_str) or data_str == "" or data_str == "N/A":
        return None
    
    if isinstance(data_str, datetime):
        return data_str
    
    data_str = str(data_str).strip()
    
    try:
        return datetime.strptime(data_str, "%d/%m/%Y")
    except ValueError:
        return None


def parse_dias_cotizacao(dias_str: str) -> Tuple[Optional[int], Optional[datetime]]:
    """
    Interpreta "Dias para Cotização":
    - inteiro (ex: 91) -> número de dias corridos
    - "Fechado" -> indisponível
    - data "13/06/2029" -> usa como data_cotizacao diretamente
    
    Returns:
        Tuple[dias_int, data_fixa] onde apenas um será não-None
    """
    if pd.isna(dias_str) or dias_str == "" or dias_str == "N/A":
        return None, None
    
    dias_str = str(dias_str).strip()
    
    # Verificar se é "Fechado"
    if dias_str.lower() == "fechado":
        return None, None  # Indisponível
    
    # Tentar parse como inteiro
    try:
        dias_int = int(dias_str)
        return dias_int, None
    except ValueError:
        pass
    
    # Tentar parse como data
    data_parsed = parse_data(dias_str)
    if data_parsed:
        return None, data_parsed
    
    return None, None


def parse_dias_liquidacao(dias_str: str) -> Tuple[Optional[int], Optional[datetime]]:
    """
    Interpreta "Dias para Liquidação":
    - inteiro (ex: 1) -> número de dias úteis
    - data "13/06/2029" -> usa como data_disponibilidade diretamente
    - vazio -> N/A (será tratado por regra específica do Tipo)
    
    Returns:
        Tuple[dias_uteis_int, data_fixa]
    """
    if pd.isna(dias_str) or dias_str == "" or dias_str == "N/A":
        return None, None
    
    dias_str = str(dias_str).strip()
    
    # Tentar parse como inteiro
    try:
        dias_int = int(dias_str)
        return dias_int, None
    except ValueError:
        pass
    
    # Tentar parse como data
    data_parsed = parse_data(dias_str)
    if data_parsed:
        return None, data_parsed
    
    return None, None


def parse_posicao_file(source: Union[str, object]) -> pd.DataFrame:
    """
    Carrega arquivo de posição (XLSX ou CSV) local ou via URL
    
    Args:
        source: caminho local, URL RAW ou objeto file_uploader do Streamlit
    
    Returns:
        DataFrame com colunas padronizadas
    """
    # Detectar tipo de source
    if isinstance(source, str):
        if source.startswith("http"):
            # URL GitHub
            df = pd.read_excel(source) if source.endswith(".xlsx") else pd.read_csv(source)
        else:
            # Arquivo local
            df = pd.read_excel(source) if source.endswith(".xlsx") else pd.read_csv(source)
    else:
        # Streamlit UploadedFile
        if source.name.endswith(".xlsx"):
            df = pd.read_excel(source)
        else:
            df = pd.read_csv(source)
    
    # Limpar nomes de colunas
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("\n", "").str.replace("\r", "")
    
    # Validar colunas obrigatórias
    colunas_esperadas = [
        'Fundo_/_Ativo', 'Posição_Atual', 'Dias_para_Cotização', 'Dias_pra_Liquidação',
        'Tipo', 'Status', 'Empresa', 'Atualização'
    ]
    
    # Tentar encontrar colunas (case-insensitive)
    col_mapping = {}
    for col_esperada in colunas_esperadas:
        encontrada = False
        for col_atual in df.columns:
            if col_atual.lower() == col_esperada.lower():
                col_mapping[col_atual] = col_esperada
                encontrada = True
                break
        
        if not encontrada:
            raise ValueError(f"Coluna '{col_esperada}' não encontrada no arquivo!")
    
    # Renomear colunas
    df = df.rename(columns=col_mapping)
    
    return df
