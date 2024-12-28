# run.py

"""
Ponto de entrada para executar o Prometheus Security Suite.
Executa a aplicação FastAPI usando Uvicorn.
"""

import uvicorn
import os

if __name__ == "__main__":
    # Obtém a porta do ambiente ou usa 8000 como padrão
    port = int(os.getenv("PORT", 8000))

    # Executa o servidor
    uvicorn.run(
        "prometheus_app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=True  # 'reload=True' é útil em desenvolvimento (atualiza ao salvar)
    )

"""
Comentário: Em um ambiente de produção, podemos configurar gunicorn com uvicorn workers ou usar containers Docker, mas para desenvolvimento local, isso é suficiente.
Dica de Melhoria Futura: Criar arquivos de configuração para Docker (Dockerfile, docker-compose) para padronizar o ambiente em produção.
"""