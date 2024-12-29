"""
Arquivo: TheShip/main.py
Descrição:
    - Ponto de entrada do back-end (FastAPI) do Prometheus Security Suite.
    - Gerencia a autenticação JWT, conexão com o banco de dados e integração dos módulos principais.
    - Inclui um middleware de auditoria para registrar todas as requisições.
    - Configura CORS para permitir requisições do frontend.
"""

import logging
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import bcrypt
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração básica de logging
logging.basicConfig(level=logging.DEBUG)  # Alterado para DEBUG para mais detalhes
logger = logging.getLogger(__name__)

# Importa o modelo de usuário e a base declarativa
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

# Configuração de CORS
origins = [
    "http://127.0.0.1:5173",  # Endereço do seu frontend Vue.js
    # Adicione outros domínios se necessário
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Permite apenas os domínios especificados
    allow_credentials=True,
    allow_methods=["*"],              # Permite todos os métodos HTTP
    allow_headers=["*"],              # Permite todos os headers
)

# Adiciona o middleware de auditoria para registrar requisições e respostas
app.middleware("http")(audit_middleware)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Carrega as variáveis de ambiente para configuração
SECRET_KEY = os.getenv("SECRET_KEY", "SuperSecretKey1234567890!@#$%^&*()_+-=")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define o caminho absoluto para o banco de dados
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'prometheus_users.db')}")

# Configura banco de dados para autenticação
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
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

def authenticate_user(db: Session, username: str, password: str):
    """
    Função que valida se o usuário existe e se a senha confere com o hash.
    Retorna o objeto User se autenticado, ou levanta uma exceção com erro específico.
    """
    logger.debug(f"Tentando autenticar usuário: {username}")
    try:
        user = db.query(User).filter(User.username == username).first()
        logger.debug(f"Usuário encontrado: {user.username if user else 'None'}")
    except Exception as e:
        logger.error(f"Erro ao consultar o usuário no banco de dados: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço indisponível. Tente novamente mais tarde."
        )

    if not user:
        logger.warning(f"Usuário {username} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado."
        )

    try:
        password_correct = bcrypt.checkpw(password.encode("utf-8"), user.hashed_password.encode("utf-8"))
        logger.debug(f"Senha correta: {password_correct}")
    except Exception as e:
        logger.error(f"Erro ao verificar a senha: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao verificar a senha."
        )

    if not password_correct:
        logger.warning(f"Senha inválida para usuário {username}.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta."
        )

    logger.info(f"Usuário {username} autenticado com sucesso.")
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
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        logger.error(f"Erro ao gerar o token JWT: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao gerar o token."
        )
    return encoded_jwt

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Rota para autenticação de usuários.
    Recebe username e password, autentica o usuário e retorna um token JWT.
    """
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
    except HTTPException as http_exc:
        # Relevância das mensagens específicas
        raise http_exc
    except Exception as e:
        logger.error(f"Erro inesperado durante a autenticação: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno durante a autenticação."
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    logger.info(f"Login bem-sucedido para usuário {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}

def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Verifica se o token JWT é válido e decodifica o 'username' (sub).
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.error("Token inválido ou sem 'sub'.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou sem 'sub'."
            )
        return username
    except JWTError as e:
        logger.error(f"Token inválido ou expirado: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado."
        )
    except Exception as e:
        logger.error(f"Erro ao decodificar o token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao verificar o token."
        )

@app.get("/secure")
def secure_endpoint(current_user: str = Depends(verify_token), db: Session = Depends(get_db)):
    """
    Exemplo de rota protegida que requer token JWT válido.
    Retorna dados do usuário, incluindo 'role'.
    """
    try:
        user_obj = db.query(User).filter(User.username == current_user).first()
    except Exception as e:
        logger.error(f"Erro ao consultar o usuário no banco de dados: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço indisponível. Tente novamente mais tarde."
        )

    if not user_obj:
        logger.error(f"Usuário {current_user} não encontrado.")
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    return {"status": "Ok", "user": user_obj.username, "role": user_obj.role}

@app.get("/admin_only")
def admin_route(current_user: str = Depends(verify_token), db: Session = Depends(get_db)):
    """
    Exemplo de rota que apenas usuários com role='admin' podem acessar.
    """
    try:
        user_obj = db.query(User).filter(User.username == current_user).first()
    except Exception as e:
        logger.error(f"Erro ao consultar o usuário no banco de dados: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço indisponível. Tente novamente mais tarde."
        )

    if not user_obj:
        logger.error(f"Usuário {current_user} não encontrado.")
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if user_obj.role != "admin":
        logger.warning(f"Acesso proibido para o usuário {current_user}.")
        raise HTTPException(status_code=403, detail="Acesso proibido para este perfil.")

    logger.info(f"Usuário {user_obj.username} acessou a rota de administração.")
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
    logger.info("Rota raiz acessada.")
    return {"message": "Bem-vindo ao Prometheus Security Suite"}

# Manipuladores globais para HTTPException e RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"Erro HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Erro de validação: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Erro de validação dos dados de entrada."},
    )
