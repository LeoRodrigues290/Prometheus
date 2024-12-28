"""
Arquivo: TheShip/TheKey/users_models.py
Descrição:
    - Extensão do modelo de usuário para suportar roles (perfis de acesso).
"""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """
    Representa um usuário do Prometheus Security Suite.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")  # Ex.: "admin", "user"
    is_active = Column(Boolean, default=True)

"""
MELHORIAS FUTURAS:
1. Migrar de RBAC para ABAC, permitindo regras mais dinâmicas (por ex., acesso baseado em atributos).
2. Incluir data de criação, último login, e logs detalhados para auditoria de atividades.
3. Manter tabela separada de 'roles' e relacionar com usuários, para maior escalabilidade de perfis.
4. Criar uma estrutura de permissões por módulo, definindo granularidade (ex.: CRUD do Vault).
"""
