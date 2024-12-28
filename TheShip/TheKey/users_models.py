"""
Arquivo: TheShip/TheKey/users_models.py
Descrição:
    - Define o modelo de usuário (User) que será armazenado em banco de dados.
    - Utiliza SQLAlchemy para mapeamento objeto-relacional.
    - Inclui suporte a roles (ex.: "admin", "user") e status (is_active).
"""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """
    Representa um usuário do Prometheus Security Suite.
    - 'username' é único e serve de identificação principal.
    - 'hashed_password' armazena a senha em formato de hash (bcrypt).
    - 'role' define o nível de acesso (ex.: "admin", "user").
    - 'is_active' indica se o usuário está habilitado para fazer login.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)

"""
MELHORIAS FUTURAS:
1. Adicionar colunas como 'email', 'phone_number' ou 'full_name' para compor dados do usuário.
2. Criar tabela separada de 'roles' com relacionamentos (1:N ou N:N), se for necessário um controle mais granular.
3. Armazenar logs de último acesso, datas de expiração de conta ou troca de senha para auditoria mais detalhada.
4. Adicionar colunas de timestamps (criado_em, atualizado_em) para rastrear histórico de cada registro.
"""
