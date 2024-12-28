"""
Arquivo: TheShip/TheBoy/vault_service.py
Descrição: Oferece rotas para inserir, recuperar e gerenciar dados no Boy’s Vault.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, VaultItem
from cryptography.fernet import Fernet

router = APIRouter()

# Configuração simplificada de banco de dados (use variáveis de ambiente em produção)
DATABASE_URL = "sqlite:///./boy_vault.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Inicializa o banco de dados
Base.metadata.create_all(bind=engine)

# Chave simétrica para criptografar dados no Vault
# Em produção, essa chave deve ser armazenada com segurança (cofre de senhas, HSM, etc.)
FERNET_KEY = Fernet.generate_key()
cipher = Fernet(FERNET_KEY)

class VaultItemSchema(BaseModel):
    key_name: str
    value: str

@router.post("/store")
def store_item(item: VaultItemSchema):
    """
    Armazena dados criptografados no Vault.
    """
    db = SessionLocal()

    # Verifica se já existe um item com o mesmo nome de chave
    existing_item = db.query(VaultItem).filter(VaultItem.key_name == item.key_name).first()
    if existing_item:
        raise HTTPException(status_code=400, detail="Key name already exists.")

    # Criptografa o valor
    encrypted_value = cipher.encrypt(item.value.encode('utf-8'))

    # Cria e armazena o objeto
    vault_item = VaultItem(key_name=item.key_name, encrypted_value=encrypted_value.decode('utf-8'))
    db.add(vault_item)
    db.commit()
    db.refresh(vault_item)

    return {"status": "success", "item_id": vault_item.id}

@router.get("/retrieve/{key_name}")
def retrieve_item(key_name: str):
    """
    Recupera e descriptografa dados do Vault.
    """
    db = SessionLocal()

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
1. Implementar controle de permissões e autenticação (RBAC ou ABAC) para acesso a cada 'VaultItem'.
2. Integrar com módulos HSM para guardar a FERNET_KEY de maneira mais segura.
3. Implementar logs detalhados de acesso, armazenando quem acessou e quando (integrar com Kerberos/Audit).
4. Criar endpoints para atualizar e excluir itens, mantendo a funcionalidade de versionamento.
"""
