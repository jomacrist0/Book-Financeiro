# -*- coding: utf-8 -*-
"""
Funções auxiliares para o projeto
Gerencia caminhos de arquivos após reorganização
"""

import os

def get_data_path(filename):
    """
    Retorna o caminho completo para um arquivo de dados.
    Compatível com a nova estrutura de pastas.
    
    Args:
        filename (str): Nome do arquivo (ex: "1Saldos - ecossistema.xlsx")
    
    Returns:
        str: Caminho completo para o arquivo
    """
    # Diretório base do projeto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Tenta múltiplos caminhos para compatibilidade
    possible_paths = [
        os.path.join(base_dir, "data", filename),  # Nova estrutura
        os.path.join(base_dir, filename),           # Raiz (legado)
        os.path.join(os.getcwd(), "data", filename),
        os.path.join(os.getcwd(), filename)
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # Retorna o caminho preferencial mesmo se não existir
    return os.path.join(base_dir, "data", filename)

def get_worker_db_path():
    """Retorna caminho do banco de dados do worker"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "data", "malga_datamart.db")
