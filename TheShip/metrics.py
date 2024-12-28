"""
Arquivo: TheShip/metrics.py
Descrição:
    - Integração básica com Prometheus para expor métricas.
"""

from prometheus_client import Counter, Histogram
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest

router = APIRouter()

REQUEST_COUNT = Counter("request_count", "Número de requisições recebidas", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Latência das requisições em segundos", ["endpoint"])

@router.get("/metrics", response_class=PlainTextResponse)
def metrics():
    """
    Endpoint para o Prometheus coletar as métricas.
    """
    return generate_latest()

"""
MELHORIAS FUTURAS:
1. Adicionar métricas personalizadas (ex.: 'keys_generated_count' para medir chaves quânticas criadas).
2. Criar um middleware para automatizar a coleta de latência por rota (similar ao de auditoria).
3. Integrar com tracing distribuído (ex.: OpenTelemetry) para mapear fluxos complexos.
4. Prover dashboards prontos no Grafana para visualizar métricas e alertas.
"""
