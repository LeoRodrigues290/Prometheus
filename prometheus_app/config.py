# prometheus_app/config.py

"""
Módulo de configuração global da plataforma Prometheus.
Armazena variáveis de ambiente, parâmetros do Qiskit, etc.
"""

import os

# Exemplo de variáveis de ambiente (podemos usar python-dotenv ou outro método)
PROMETHEUS_ENV = os.getenv("PROMETHEUS_ENV", "development")

# Configurações específicas de Qiskit (podemos expandir conforme necessidade)
QISKIT_BACKEND = os.getenv("QISKIT_BACKEND", "aer_simulator")
# 'aer_simulator' é o simulador local do Qiskit. Em produção, podemos configurar para usar um backend real.

# Configuração de log
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Futuras configurações como conexão de banco de dados, URIs, etc. ficarão aqui.
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING", "sqlite:///./prometheus.db")

"""
Dica de Melhoria Futura: Usar pacotes como python-dotenv ou dynaconf para gerenciamento de configurações mais robusto, além de separar ambiente de desenvolvimento e produção.
"""