# Prometheus Security Suite

**Versão Inicial**  
Este repositório contém a aplicação “Prometheus Security Suite” que visa geração, armazenamento e distribuição segura de dados, valendo-se de componentes de computação quântica (Qiskit).  

## Estrutura
- **prometheus_app/**: Código-fonte principal (FastAPI + Módulos).
- **run.py**: Ponto de entrada para executar o servidor.
- **requirements.txt**: Dependências do projeto.
- **docs/**: Documentação e guias de uso.

## Setup
1. Crie um ambiente virtual: `python -m venv venv`
2. Ative o ambiente (Windows: `venv\Scripts\activate`, Linux/Mac: `source venv/bin/activate`)
3. Instale as dependências: `pip install -r requirements.txt`
4. Rode a aplicação: `python run.py`
5. Acesse `http://localhost:8000` para ver o sistema em execução.

## Próximos Passos
- Implementar módulo “Pyramid” para geração de chaves quânticas.
- Criar estrutura de bancos de dados e logs (Módulo “Kerberos”).
- Armazenamento seguro no “Boy’s Vault”.
- Autenticação e controle de acesso a APIs.
