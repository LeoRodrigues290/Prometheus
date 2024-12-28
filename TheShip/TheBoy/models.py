"""
Arquivo: TheShip/TheBoy/models.py
Descrição:
    - Modelos de dados para itens armazenados no repositório seguro (Vault).
    - Usa SQLAlchemy para mapear a tabela 'vault_items'.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class VaultItem(Base):
    """
    Representa um registro seguro armazenado no Vault:
    - key_name (string única) para identificar o item.
    - encrypted_value (conteúdo criptografado).
    - created_at (timestamp de criação).
    """
    __tablename__ = "vault_items"

    id = Column(Integer, primary_key=True, index=True)
    key_name = Column(String, unique=True, index=True)
    encrypted_value = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

"""
MELHORIAS FUTURAS:
1. Adicionar relacionamento com User (owner_id), para controle de acesso avançado.
2. Guardar metadados adicionais (descrição, tags de classificação, etc.).
3. Possibilitar versionamento de itens (mantendo histórico de alterações).
4. Incluir timestamp de atualização (updated_at) e logs de acessos no Kerberos.
"""
