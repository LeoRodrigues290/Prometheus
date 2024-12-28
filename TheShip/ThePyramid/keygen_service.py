"""
Arquivo: TheShip/ThePyramid/keygen_service.py
Descrição:
    - Fornece rotas e lógicas de API para geração de chaves quânticas.
    - Usa o módulo quantum_rng.py para gerar bits aleatórios.
"""

from fastapi import APIRouter
from .quantum_rng import generate_quantum_random_number

router = APIRouter()

@router.get("/generate_key")
def generate_key():
    """
    Gera uma chave quântica de 256 bits e retorna em formato hexadecimal.
    """
    random_int = generate_quantum_random_number(num_bits=256)
    hex_key = hex(random_int)[2:]  # Remove o prefixo '0x'
    return {"quantum_key": hex_key}

@router.get("/health")
def health_check():
    """
    Endpoint para verificar a disponibilidade do módulo de geração de chaves.
    """
    return {"status": "Pyramid module is operational"}

"""
MELHORIAS FUTURAS:
1. Adicionar endpoints para geração de chaves com comprimentos diferentes (512, 1024 bits, etc.).
2. Integrar criptografia pós-quântica (pqcrypto) para distribuir chaves de forma segura.
3. Registar cada geração de chave no Kerberos (audit log) para fins de auditoria.
4. Possibilitar armazenar automaticamente as chaves geradas no Vault, caso necessário.
"""
