# Arquivo: TheEnd/Dockerfile.backend
# Descrição: Dockerfile para a aplicação FastAPI (TheShip).

# Imagem base do Python
FROM python:3.10-slim as base

# Define a variável de ambiente para a root directory da aplicação
ENV APP_HOME /app
WORKDIR $APP_HOME

# Copia os arquivos de requirements (ou use poetry/hatch se preferir)
COPY TheShip/requirements.txt requirements.txt

# Instala as dependências
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY TheShip/ TheShip/

# Expõe a porta do container
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "TheShip.main:app", "--host", "0.0.0.0", "--port", "8000"]

#
# MELHORIAS FUTURAS:
# 1. Implementar multi-stage build (por exemplo, para rodar testes em um estágio separado).
# 2. Adicionar suporte a variáveis de ambiente seguras (para DB_URL, SECRET_KEY, etc.).
# 3. Usar imagens minimalistas como base (ex.: python:3.10-alpine) para reduzir tamanho do container.
# 4. Configurar logging e monitoramento dentro do container (ex.: Fluent Bit ou outro agente).
#
