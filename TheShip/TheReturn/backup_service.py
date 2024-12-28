"""
Arquivo: TheShip/TheReturn/backup_service.py
Descrição: Módulo para backup e restauração dos dados sensíveis do sistema.
"""

import shutil
import os
from datetime import datetime

def backup_database(db_path: str, backup_dir: str):
    """
    Realiza backup de um arquivo de banco de dados (ex.: SQLite).
    """
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}.db")
    shutil.copy2(db_path, backup_path)
    return backup_path

"""
MELHORIAS FUTURAS:
1. Suportar múltiplos tipos de bancos de dados (PostgreSQL, MySQL, MongoDB) com dumps específicos.
2. Criptografar os arquivos de backup (uso de GPG ou AES).
3. Implementar restauração automática e testes periódicos de integridade de backups.
4. Integrar com serviços de armazenamento em nuvem (S3, Azure Blob, etc.) para maior disponibilidade.
"""
