"""
Arquivo: TheShip/Kerberos/audit_models.py
Descrição:
    - Modelos de dados para registro de eventos de auditoria.
    - Cada log registra uma ação (action), detalhes e timestamp.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class AuditLog(Base):
    """
    Representa um registro de evento de auditoria:
    - 'action': Nome da ação (ex.: "LOGIN", "REQUEST", etc.)
    - 'details': Descrição da ação.
    - 'timestamp': Data/hora do evento.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, index=True)
    details = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

"""
MELHORIAS FUTURAS:
1. Adicionar colunas como user_id, ip_address, severity para enriquecer a auditoria.
2. Criar índices adicionais para consultas de alto desempenho em grandes volumes de logs.
3. Integrar com sistemas SIEM (Splunk, Elasticsearch, Security Onion).
4. Implementar rotação e arquivamento de logs para reduzir tamanho do banco.
"""
