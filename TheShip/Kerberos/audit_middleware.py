"""
Arquivo: TheShip/Kerberos/audit_middleware.py
Descrição:
    - Implementa um middleware de FastAPI para registrar cada requisição no sistema de auditoria.
"""
from starlette.requests import Request
from starlette.responses import Response
from .audit_service import log_action

async def audit_middleware(request: Request, call_next):
    """
    Middleware que intercepta a requisição, processa e registra no Kerberos.
    """
    # Antes da chamada
    method = request.method
    url = request.url.path

    response: Response = await call_next(request)

    # Após a chamada
    status_code = response.status_code

    # Registra no Kerberos (pode-se injetar DB session se precisar)
    try:
        details = f"Method: {method}, Path: {url}, Status: {status_code}"
        log_action("REQUEST", details)  # Exemplo de log
    except Exception:
        # Evitar travar a requisição se falhar a auditoria
        pass

    return response

"""
MELHORIAS FUTURAS:
1. Adicionar informações de cabeçalhos, IP de origem e User-Agent, se permitido pela política de privacidade.
2. Integrar com outros sistemas de SIEM via streaming (ex.: Kafka, Splunk).
3. Otimizar para não gerar logs excessivos (filtrar rotas específicas).
4. Adicionar correlação de ID de requisição, facilitando o tracing distribuído.
"""
