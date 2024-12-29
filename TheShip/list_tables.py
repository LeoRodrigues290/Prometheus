# Arquivo: TheShip/list_tables.py

import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./prometheus_users.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
inspector = inspect(engine)

def list_tables():
    tables = inspector.get_table_names()
    print("Tabelas no banco de dados:")
    for table in tables:
        print(f"- {table}")

if __name__ == "__main__":
    list_tables()
