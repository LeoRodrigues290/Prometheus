"""
Arquivo: TheShip/TheCalling/scheduler.py
Descrição: Configura rotinas (cron-like) para execução de tarefas periódicas.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from TheShip.TheReturn.backup_service import backup_database

def schedule_backups(db_path: str, backup_dir: str, interval_minutes: int):
    """
    Agenda backups periódicos do banco de dados.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(backup_database, 'interval', minutes=interval_minutes, args=[db_path, backup_dir])
    scheduler.start()
    return scheduler

"""
MELHORIAS FUTURAS:
1. Integrar logs das rotinas agendadas no Kerberos (audit_service).
2. Adicionar funcionalidades como notificação por email/Slack quando um job falha.
3. Escalonar com plataformas Cloud (AWS EventBridge, Azure Functions) para execuções em larga escala.
4. Adicionar tratamento de exceções detalhado e relatórios sobre o status dos jobs.
"""
