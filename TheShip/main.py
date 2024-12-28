"""
Arquivo: TheShip/main.py
Descrição:
    - Ponto de entrada do back-end (FastAPI) do Prometheus Security Suite.
    - Gerencia a autenticação JWT, conexão com o banco de dados e integração dos módulos (Pyramid, Boy’s Vault, Kerberos).
    - Inclui um middleware de auditoria para registrar todas as requisições.
    - Demonstração de controle de perfis de acesso (RBAC) em rotas específicas.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import bcrypt

# Importa o modelo de usuário, com suporte a roles (admin/user), e a base declarativa
from TheShip.TheKey.users_models import Base, User

# Importa os routers dos módulos principais
from TheShip.ThePyramid.keygen_service import router as keygen_router
from TheShip.TheBoy.vault_service import router as vault_router
from TheShip.Kerberos.audit_service import router as audit_router

# Importa o middleware de auditoria
from TheShip.Kerberos.audit_middleware import audit_middleware

app = FastAPI(
    title="Prometheus Security Suite",
    description="Sistema profissional para geração de chaves quânticas, criptografia avançada e monitoramento de acessos.",
    version="1.0.0"
)

# Adiciona o middleware de auditoria para registrar requisições e respostas
app.middleware("http")(audit_middleware)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = "SUA_CHAVE_SECRETA"  # Em produção, usar variáveis de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configura banco de dados para autenticação
DATABASE_URL = "sqlite:///./prometheus_users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Garante criação de tabelas (User, etc.)
Base.metadata.create_all(bind=engine)

def get_db():
    """
    Gera uma sessão de banco de dados para ser injetada nas rotas.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(db, username: str, password: str):
    """
    Função que valida se o usuário existe e se a senha confere com o hash.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not bcrypt.checkpw(password.encode("utf-8"), user.hashed_password.encode("utf-8")):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Gera um token JWT com payload 'data' e tempo de expiração (exp).
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
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    """
    Endpoint de login que recebe usuário/senha (OAuth2PasswordRequestForm).
    Retorna token JWT se credenciais forem válidas.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Verifica se o token JWT é válido e decodifica o 'username' (sub).
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
def secure_endpoint(current_user: str = Depends(verify_token), db=Depends(get_db)):
    """
    Exemplo de rota protegida que requer token JWT válido.
    Retorna dados do usuário, incluindo 'role'.
    """
    user_obj = db.query(User).filter(User.username == current_user).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return {"status": "Ok", "user": user_obj.username, "role": user_obj.role}

@app.get("/admin_only")
def admin_route(current_user: str = Depends(verify_token), db=Depends(get_db)):
    """
    Exemplo de rota que apenas usuários com role='admin' podem acessar.
    """
    user_obj = db.query(User).filter(User.username == current_user).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if user_obj.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso proibido para este perfil.")
    return {"message": f"Bem-vindo, {user_obj.username}, à rota de administração!"}

# Inclui as rotas dos módulos Pyramid, Boy’s Vault e Kerberos
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
1. Criar rotas para cadastro/alteração de senha de usuários, com validações de e-mail e regras de complexidade.
2. Implementar refresh tokens para sessões de longa duração, permitindo renovação do JWT.
3. Logar tentativas de login e logout no Kerberos (audit_service).
4. Configurar SECRET_KEY e DATABASE_URL como variáveis de ambiente, evitando exposições no código.
5. Adicionar rate limiting e lockout após várias tentativas de login falhas para mitigar força bruta.
6. Migrar para um SGBD robusto (PostgreSQL, MySQL) para ambientes de produção.
7. Expandir o controle de roles (RBAC) ou migrar para ABAC para mais granularidade de permissões.
8. Integrar com Prometheus, Grafana ou outra ferramenta de observabilidade para métricas e alertas.
"""
