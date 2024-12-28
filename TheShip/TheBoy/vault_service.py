"""
Arquivo: TheShip/TheBoy/vault_service.py
Descrição:
    - Oferece rotas para inserir, recuperar e gerenciar dados no Boy’s Vault.
    - Criptografa e descriptografa valores usando Fernet (AES).
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cryptography.fernet import Fernet

from .models import Base, VaultItem

# Configuração do banco de dados (exemplo com SQLite local)
DATABASE_URL = "sqlite:///./boy_vault.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

router = APIRouter()

# Gera uma chave simétrica (uso didático). Em produção, armazene-a em local seguro (HSM/HashiCorp Vault).
FERNET_KEY = Fernet.generate_key()
cipher = Fernet(FERNET_KEY)

class VaultItemSchema(BaseModel):
    key_name: str
    value: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/store")
def store_item(item: VaultItemSchema, db=Depends(get_db)):
    """
    Armazena dados criptografados no Vault.
    """
    existing_item = db.query(VaultItem).filter(VaultItem.key_name == item.key_name).first()
    if existing_item:
        raise HTTPException(status_code=400, detail="Key name already exists.")

    encrypted_value = cipher.encrypt(item.value.encode('utf-8'))
    vault_item = VaultItem(key_name=item.key_name, encrypted_value=encrypted_value.decode('utf-8'))
    db.add(vault_item)
    db.commit()
    db.refresh(vault_item)
    return {"status": "success", "item_id": vault_item.id}

@router.get("/retrieve/{key_name}")
def retrieve_item(key_name: str, db=Depends(get_db)):
    """
    Recupera e descriptografa dados do Vault.
    """
    vault_item = db.query(VaultItem).filter(VaultItem.key_name == key_name).first()
    if not vault_item:
        raise HTTPException(status_code=404, detail="Item not found.")

    decrypted_value = cipher.decrypt(vault_item.encrypted_value.encode('utf-8'))
    return {
        "key_name": vault_item.key_name,
        "value": decrypted_value.decode('utf-8'),
        "created_at": vault_item.created_at
    }

"""
MELHORIAS FUTURAS:
1. Integrar controle de permissões (ex.: verificar se o usuário atual pode acessar o item).
2. Guardar a FERNET_KEY em um serviço seguro (AWS KMS, HashiCorp Vault, HSM).
3. Suportar algoritmos pós-quânticos ou híbridos (Kyber + AES) para reforçar a segurança.
4. Adicionar rotas para atualizar e deletar itens, com registro de auditoria em Kerberos.
"""
