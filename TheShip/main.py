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

# Importa os routers dos módulos principais do sistema
from TheShip.ThePyramid.keygen_service import router as keygen_router
from TheShip.TheBoy.vault_service import router as vault_router
from TheShip.Kerberos.audit_service import router as audit_router

# Importa o middleware de auditoria (intercepta requisições e registra logs)
from TheShip.Kerberos.audit_middleware import audit_middleware

# Cria a aplicação FastAPI com título e descrição
app = FastAPI(
    title="Prometheus Security Suite",
    description="Sistema profissional para geração de chaves quânticas, criptografia avançada e monitoramento de acessos.",
    version="1.0.0"
)

# Adiciona o middleware de auditoria para registrar requisições e respostas
app.middleware("http")(audit_middleware)

# Configura detalhes de autenticação via OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Chave secreta e algoritmo JWT (use variáveis de ambiente em produção)
SECRET_KEY = "SUA_CHAVE_SECRETA"        # Substitua por algo seguro
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# URL de banco de dados para exemplo (SQLite local); em produção, prefira PostgreSQL ou outro SGDB
DATABASE_URL = "sqlite:///./prometheus_users.db"

# Cria o engine e a sessão do SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Garante que as tabelas (User, etc.) sejam criadas no banco de dados
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
    Função que valida se o usuário existe no banco e se a senha confere com o hash armazenado.
    Retorna o objeto 'User' se ok, ou None se falhar.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    # Verifica a senha usando bcrypt
    if not bcrypt.checkpw(password.encode("utf-8"), user.hashed_password.encode("utf-8")):
        return None

    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Gera um token JWT com payload 'data' e tempo de expiração.
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
    Endpoint de login que recebe usuário e senha (OAuth2PasswordRequestForm).
    Se credenciais forem válidas, retorna o token JWT.
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
    Verifica se o token JWT recebido (via bearer) é válido.
    Decodifica para extrair o 'username' (sub).
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
    Exemplo de rota protegida que requer um token JWT válido.
    Retorna uma mensagem de sucesso e o username do token.
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

    # Verifica se o usuário tem papel 'admin'
    if user_obj.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso proibido para este perfil.")

    return {"message": f"Bem-vindo, {user_obj.username}, à rota de administração!"}

# Inclui as rotas dos módulos principais do sistema
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
1. Criar rotas para cadastro de usuários e atualização de senha, com validações (e-mail, regras de complexidade).
2. Implementar refresh tokens para sessões de longa duração, permitindo renovação do JWT sem refazer login.
3. Registrar logs de login, logout e tentativas de acesso negadas no Kerberos (audit_service).
4. Integrar com uma ferramenta de migração de banco de dados (ex.: Alembic) para versionar o esquema.
5. Configurar variáveis de ambiente para SECRET_KEY e DATABASE_URL, evitando expor segredos no código.
6. Adicionar rate limiting e lockout temporário para mitigar ataques de força bruta de login.
7. Expandir o controle de roles (RBAC) ou migrar para ABAC, para granularidade mais avançada de permissões.
8. Integrar com sistemas de SIEM e observabilidade (Prometheus, Grafana, Splunk, etc.) para monitoramento.
"""
