"""
Arquivo: TheShip/main.py
Descrição:
    - Ponto de entrada do back-end (FastAPI).
    - Exemplo de configuração JWT (simplificada).
    - As rotas principais do sistema são incluídas aqui.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Import das rotas existentes (módulos Pyramid, Boy's Vault e Kerberos)
from TheShip.ThePyramid.keygen_service import router as keygen_router
from TheShip.TheBoy.vault_service import router as vault_router
from TheShip.Kerberos.audit_service import router as audit_router

# Cria a instância do aplicativo FastAPI
app = FastAPI(
    title="Prometheus Security Suite",
    description="Sistema profissional para geração de chaves quânticas, criptografia avançada e monitoramento de acessos.",
    version="1.0.0"
)

# Configura o OAuth2 com fluxo de password (para login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Chave secreta (use variáveis de ambiente em produção)
SECRET_KEY = "SUA_CHAVE_SECRETA"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Exemplo simples de usuários (Não usar em produção)
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "adminpass"  # Em produção, armazene hash seguro (bcrypt, argon2, etc.)
    }
}

def authenticate_user(username: str, password: str):
    """
    Função que valida se o usuário e senha estão corretos.
    Em produção, busque no banco e compare hashes de senha.
    """
    user = fake_users_db.get(username)
    if not user or user["password"] != password:
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Gera um token JWT com payload e tempo de expiração.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint de login que recebe usuário e senha.
    Retorna um token JWT se as credenciais forem válidas.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Verifica se o token JWT recebido é válido.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou sem 'sub'."
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado."
        )

@app.get("/secure")
def secure_endpoint(current_user: str = Depends(verify_token)):
    """
    Exemplo de rota protegida que requer um token JWT válido.
    """
    return {"status": "Ok", "user": current_user, "message": "Acesso autorizado!"}

# Inclui as rotas dos módulos principais
app.include_router(keygen_router, prefix="/pyramid", tags=["Key Generation"])
app.include_router(vault_router, prefix="/boy_vault", tags=["Data Vault"])
app.include_router(audit_router, prefix="/kerberos", tags=["Monitoring"])

@app.get("/")
def read_root():
    """
    Rota base para checagem de disponibilidade do servidor.
    """
    return {"message": "Bem-vindo ao Prometheus Security Suite"}

"""
MELHORIAS FUTURAS:
1. Usar hashing de senhas (bcrypt, argon2) e armazenar usuários em um banco de dados seguro.
2. Criar endpoints para cadastro, alteração de senha e revogação de tokens.
3. Implementar refresh tokens para sessões de longa duração.
4. Adicionar logs de acesso e falha de login em Kerberos (audit_service) para maior rastreabilidade.
"""
