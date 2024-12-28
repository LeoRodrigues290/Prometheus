"""
Arquivo: TheShip/Kerberos/audit_service.py
Descrição: Fornece rotas para registrar e consultar logs de auditoria.
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

@router.post("/log")
def log_action(action: str, details: str):
    """
    Registra um evento de auditoria no sistema.
    """
    db = SessionLocal()
    audit_entry = AuditLog(action=action, details=details)
    db.add(audit_entry)
    db.commit()
    db.refresh(audit_entry)
    return {"status": "logged", "log_id": audit_entry.id}

@router.get("/logs")
def get_logs():
    """
    Retorna todos os eventos de auditoria.
    """
    db = SessionLocal()
    logs = db.query(AuditLog).all()
    return logs

"""
MELHORIAS FUTURAS:
1. Adicionar buscas filtradas por data, tipo de ação, gravidade e usuário.
2. Exportar registros para formatos como JSON, CSV ou PDF.
3. Integrar o registro de auditoria a eventos do sistema (por exemplo, armazenar logs de geração de chaves no Kerberos).
4. Implementar paginação e ordenação de logs para evitar sobrecarga em grandes volumes de dados.
"""
