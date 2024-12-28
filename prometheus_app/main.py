# prometheus_app/main.py

"""
Arquivo principal que inicializa o FastAPI para o Prometheus Security Suite.
"""

from fastapi import FastAPI
from .config import PROMETHEUS_ENV, LOG_LEVEL

# Cria a instância do FastAPI
app = FastAPI(
    title="Prometheus Security Suite",
    description="Navegando com segurança em um oceano de incertezas.",
    version="0.1.0"
)

# Rota básica de teste
@app.get("/")
def read_root():
    """
    Rota de teste para verificar se o servidor está operacional.
    Retorna um simples dict com informações de status.
    """
    return {
        "app": "Prometheus Security Suite",
        "environment": PROMETHEUS_ENV,
        "log_level": LOG_LEVEL,
        "message": "Prometheus: Subindo velas rumo à segurança quântica!"
    }


# Dica de Melhoria Futura: Podemos adicionar middlewares de segurança, manipulação de exceções, autenticação via tokens JWT, e muito mais conforme avançarmos.