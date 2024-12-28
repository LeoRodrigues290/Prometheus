"""
Arquivo: TheShip/Kerberos/audit_service.py
Descrição:
    - Oferece rotas de API para registrar e consultar logs de auditoria.
    - Pode ser chamado por outras partes do sistema para gravar eventos importantes.
"""

from fastapi import APIRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .audit_models import Base, AuditLog

router = APIRouter()

DATABASE_URL = "sqlite:///./kerberos_audit.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/log")
def log_action(action: str, details: str):
    """
    Registra um evento de auditoria no sistema.
    Pode ser chamado programaticamente por outros módulos.
    """
    db = SessionLocal()
    audit_entry = AuditLog(action=action, details=details)
    db.add(audit_entry)
    db.commit()
    db.refresh(audit_entry)
    db.close()
    return {"status": "logged", "log_id": audit_entry.id}

@router.get("/logs")
def get_logs():
    """
    Retorna todos os eventos de auditoria.
    """
    db = SessionLocal()
    logs = db.query(AuditLog).all()
    db.close()
    return logs

"""
MELHORIAS FUTURAS:
1. Adicionar paginação e filtros para consultas (por data, usuário, ação).
2. Criar logs estruturados (JSON) para facilitar integração com sistemas de análise.
3. Expandir para registrar não só texto, mas também metadados de requisição (IP, headers).
4. Configurar endpoint seguro, exigindo role='admin' para consulta de logs sensíveis.
"""
