"""
Arquivo: TheShip/Kerberos/audit_models.py
Descrição: Modelos de dados para registro de auditorias.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class AuditLog(Base):
    """
    Representa um registro de evento de auditoria no sistema.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, index=True)
    details = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

"""
MELHORIAS FUTURAS:
1. Adicionar colunas como 'user_id', 'ip_address' e 'severity' para enriquecer o log de auditoria.
2. Implementar criptografia ou hashing em certos campos sensíveis, se necessário.
3. Criar índices adicionais para otimizar queries de busca (por data, usuário, etc.).
4. Possibilitar integração com sistemas SIEM (Security Information and Event Management).
"""
