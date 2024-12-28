"""
Arquivo: TheShip/TheKey/users_models.py
Descrição:
    - Modelos de dados para gerenciamento de usuários no sistema.
    - Usa SQLAlchemy para criar tabela de usuários, armazenando username e senha com hash seguro.
"""

from sqlalchemy import Column, Integer, String
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

"""
MELHORIAS FUTURAS:
1. Incluir colunas como 'email', 'is_active', 'roles' para gerenciamento de permissões e perfis.
2. Armazenar data de criação, último login, e logs de tentativa de acesso para auditoria.
3. Implementar relacionamento com outras tabelas caso existam diferentes entidades de usuários.
4. Adicionar salt e utilizar algoritmos como Argon2 em vez de bcrypt, se performance e segurança exigirem.
"""
