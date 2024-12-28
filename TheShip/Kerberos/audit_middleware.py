"""
Arquivo: TheShip/Kerberos/audit_middleware.py
Descrição:
    - Middleware de FastAPI que intercepta requisições e registra logs de cada chamada.
    - Exemplo simples que chama log_action() após a resposta ser gerada.
"""

from starlette.requests import Request
from starlette.responses import Response
from .audit_service import log_action

async def audit_middleware(request: Request, call_next):
    """
    Intercepta a requisição antes de ser processada.
    Registra informações de método, path e status da resposta.
    """
    method = request.method
    url = request.url.path

    response: Response = await call_next(request)
    status_code = response.status_code

    details = f"Method={method}, Path={url}, Status={status_code}"
    try:
        # Chama a função do Kerberos para logar a ação no banco
        log_action("REQUEST", details)
    except Exception:
        # Evita que falhas de auditoria quebrem a aplicação principal
        pass

    return response

"""
MELHORIAS FUTURAS:
1. Adicionar IP de origem (request.client.host) e User-Agent (request.headers['user-agent']) caso seja permitido.
2. Diferenciar logs de erros (status_code >= 400) dos demais.
3. Integrar com tracing (OpenTelemetry) para rastreamento distribuído de requisições.
4. Criar mecanismo de filtragem (por rota, por método) para evitar grande volume de logs irrelevantes.
"""
