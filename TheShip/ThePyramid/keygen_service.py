"""
Arquivo: TheShip/ThePyramid/keygen_service.py
Descrição: Fornece rotas e lógicas para gerar, armazenar e distribuir chaves quânticas.
"""

from fastapi import APIRouter
from .quantum_rng import generate_quantum_random_number

router = APIRouter()

@router.get("/generate_key")
def generate_key():
    """
    Gera uma chave quântica e retorna em formato hexadecimal.
    """
    # Gera um número aleatório de 256 bits
    random_int = generate_quantum_random_number(num_bits=256)

    # Converte para hexadecimal
    hex_key = hex(random_int)[2:]  # remove o prefixo '0x'

    return {"quantum_key": hex_key}

@router.get("/health")
def health_check():
    """
    Verifica a disponibilidade do módulo de geração de chaves.
    """
    return {"status": "Pyramid module is operational"}

"""
MELHORIAS FUTURAS:
1. Adicionar criptografia assimétrica pós-quântica (via 'pqcrypto') para distribuição segura das chaves.
2. Integrar a geração de chaves com repositório seguro para registro histórico das chaves geradas.
3. Implementar limitação de taxa (rate limiting) para evitar geração abusiva de chaves.
4. Habilitar logs que registrem o ID do cliente que solicita a chave, mantendo rastreabilidade.
"""
