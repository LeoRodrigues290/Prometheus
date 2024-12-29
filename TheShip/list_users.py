# Arquivo: TheShip/list_users.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from TheShip.TheKey.users_models import User, Base

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./prometheus_users.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def list_users():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        if not users:
            print("Nenhum usuário encontrado.")
            return
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Role: {user.role}, Active: {user.is_active}")
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    list_users()
