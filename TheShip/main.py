"""
Arquivo: TheShip/main.py
Descrição: Ponto de entrada para a aplicação FastAPI.
Este arquivo configura as rotas, inicializa o app e faz a conexão com os módulos de segurança.
"""

from fastapi import FastAPI
from TheShip.ThePyramid.keygen_service import router as keygen_router
from TheShip.TheBoy.vault_service import router as vault_router
from TheShip.Kerberos.audit_service import router as audit_router

# Cria a instância da aplicação FastAPI
app = FastAPI(
    title="Prometheus Security Suite",
    description="Sistema profissional para geração de chaves quânticas, criptografia avançada e monitoramento de acessos.",
    version="1.0.0"
)

# Inclui rotas dos módulos
app.include_router(keygen_router, prefix="/pyramid", tags=["Key Generation"])
app.include_router(vault_router, prefix="/boy_vault", tags=["Data Vault"])
app.include_router(audit_router, prefix="/kerberos", tags=["Monitoring"])

# Rota base
@app.get("/")
def read_root():
    """
    Retorna uma mensagem de boas-vindas e checa se o servidor está funcionando.
    """
    return {"message": "Bem-vindo ao Prometheus Security Suite"}

"""
MELHORIAS FUTURAS:
1. Adicionar suporte a autenticação e autorização (OAuth2, JWT, etc.) para proteger as rotas.
2. Habilitar versionamento de rotas (ex.: /v1, /v2) para suportar evolução do sistema sem quebrar compatibilidade.
3. Integrar logs detalhados de request/response para auditoria e observabilidade.
4. Configurar CORS adequadamente para permitir ou restringir acessos de domínios específicos.
"""
