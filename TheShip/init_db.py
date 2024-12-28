"""
Arquivo: TheShip/init_db.py
Descrição:
    - Script para criar as tabelas no banco de dados e, opcionalmente, inserir usuários padrão.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from TheShip.TheKey.users_models import Base, User
import bcrypt

# Exemplo de URL de banco SQLite, mas em produção use PostgreSQL
DATABASE_URL = "sqlite:///./prometheus_users.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Exemplo de criação de usuário admin
    admin_username = "admin"
    admin_password = "adminpass"

    # Gera o hash da senha com bcrypt
    hashed = bcrypt.hashpw(admin_password.encode("utf-8"), bcrypt.gensalt())

    # Verifica se o usuário já existe
    existing_user = db.query(User).filter(User.username == admin_username).first()
    if not existing_user:
        user = User(username=admin_username, hashed_password=hashed.decode("utf-8"))
        db.add(user)
        db.commit()
        db.refresh(user)
        print("Usuário admin criado com sucesso!")
    else:
        print("Usuário admin já existe.")

    db.close()


if __name__ == "__main__":
    init()

"""
MELHORIAS FUTURAS:
1. Usar uma ferramenta de migração como Alembic para versionar o esquema do banco de dados.
2. Fazer a inserção de usuários iniciais via parâmetros (ex.: variáveis de ambiente).
3. Adicionar logs (Kerberos) para registrar a inicialização e criação de usuários.
4. Integrar o script de init com processos de CI/CD, para garantir que cada ambiente (dev/staging/prod) tenha a estrutura correta.
"""
