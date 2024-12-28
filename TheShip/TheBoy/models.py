"""
Arquivo: TheShip/TheBoy/models.py
Descrição: Modelos de dados para o repositório seguro de dados.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class VaultItem(Base):
    """
    Representa um item seguro armazenado no repositório (Boy’s Vault).
    """
    __tablename__ = "vault_items"

    id = Column(Integer, primary_key=True, index=True)
    key_name = Column(String, unique=True, index=True)
    encrypted_value = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

"""
MELHORIAS FUTURAS:
1. Incluir campos adicionais, como 'owner_id' ou 'tenant_id', para multiusuários e controle de acesso.
2. Adicionar versionamento do valor (ex.: histórico de alterações).
3. Implementar índice de texto completo ou criptografia de busca (Searchable Encryption) em valores sensíveis.
4. Criar tabela de relacionamentos para gerenciar permissões de acesso a cada 'VaultItem'.
"""
