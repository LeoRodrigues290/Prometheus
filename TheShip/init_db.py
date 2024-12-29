"""
Arquivo: TheShip/init_db.py
Descrição:
    - Script para inicializar/criar as tabelas no banco de dados.
    - Exemplo de criação de um usuário 'admin' com senha em hash (bcrypt).
    - Em produção, recomenda-se o uso de migrações (ex.: Alembic) em vez de scripts manuais.
    - Utiliza variáveis de ambiente para configurações sensíveis.
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import bcrypt
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Adiciona o diretório raiz do projeto ao PYTHONPATH para permitir imports absolutos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Importa a Base e o modelo User definidos em TheKey
from TheShip.TheKey.users_models import Base, User

# Obtém a URL do banco de dados a partir das variáveis de ambiente
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./prometheus_users.db")

# Cria o engine do SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init():
    """
    Inicializa o banco de dados:
    - Cria as tabelas definidas na Base se ainda não existirem.
    - Cria um usuário admin com senha em hash se não existir.
    """
    try:
        # Cria as tabelas, caso ainda não existam
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()

        # Exemplo de criação de um usuário admin
        admin_username = "admin"
        admin_password = "adminpass"

        # Gera o hash da senha usando bcrypt
        hashed = bcrypt.hashpw(admin_password.encode("utf-8"), bcrypt.gensalt())

        # Verifica se já existe um usuário com esse username
        existing_user = db.query(User).filter(User.username == admin_username).first()
        if not existing_user:
            user = User(
                username=admin_username,
                hashed_password=hashed.decode("utf-8"),
                role="admin",
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print("Usuário admin criado com sucesso!")
        else:
            print("Usuário admin já existe.")

    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init()

"""
MELHORIAS FUTURAS:
1. Integrar o script de init com uma ferramenta de migração (Alembic) para versionar mudanças no schema do banco.
2. Tornar a criação do usuário admin opcional, via linha de comando ou variáveis de ambiente.
3. Registrar logs no Kerberos sobre criação/alteração de usuários durante a inicialização.
4. Implementar testes automatizados para garantir que a estrutura do banco está correta antes de iniciar a aplicação.
"""
