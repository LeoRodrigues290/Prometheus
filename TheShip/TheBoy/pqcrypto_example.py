"""
Arquivo: TheShip/TheBoy/pqcrypto_example.py
Descrição:
    - Demonstra como integrar um algoritmo pós-quântico (ex.: Kyber) para criptografia de dados.
"""

from pqcrypto.kem.kyber512 import generate_keypair, encrypt, decrypt
import os
from cryptography.fernet import Fernet

def hybrid_encrypt(data: bytes):
    """
    Exemplo de criptografia híbrida:
    1. Usa Kyber para gerar key pair (público/privado).
    2. Usa a chave pública para encapsular uma key simétrica (AES).
    3. Criptografa 'data' com AES (Fernet), e retorna tudo (ciphertxt, cipherkey, pk, sk).
    """
    # Gera par de chaves Kyber
    pk, sk = generate_keypair()

    # Gera key simétrica (Fernet)
    symm_key = Fernet.generate_key()
    f = Fernet(symm_key)

    # Encapsula a key simétrica usando pk (Kyber)
    cipherkey, shared_secret = encrypt(pk)

    # Aqui poderíamos usar 'shared_secret' como chave AES também, mas para exemplo
    # estamos armazenando a key simétrica e cipherkey.
    encrypted_data = f.encrypt(data)

    return {
        "encrypted_data": encrypted_data,
        "symm_key": symm_key,
        "cipherkey": cipherkey,
        "pk": pk,
        "sk": sk
    }

def hybrid_decrypt(encrypted_bundle: dict):
    """
    Inverte o processo de hybrid_encrypt usando sk (Kyber).
    """
    sk = encrypted_bundle["sk"]
    cipherkey = encrypted_bundle["cipherkey"]
    symm_key = encrypted_bundle["symm_key"]  # Em cenário real, esta key seria obtida após descapsular

    # Decapsula a key simétrica do cipherkey (caso fosse derivada do shared_secret)
    # shared_secret = decrypt(sk, cipherkey)

    # Decifra os dados com Fernet
    f = Fernet(symm_key)
    decrypted_data = f.decrypt(encrypted_bundle["encrypted_data"])

    return decrypted_data

"""
MELHORIAS FUTURAS:
1. Em um sistema real, separar a lógica de geração de par de chaves (pk, sk) e armazenar a private key com segurança.
2. Usar a 'shared_secret' derivada de Kyber para alimentar a chave simétrica (em vez de gerar outra).
3. Evitar trocar ou expor as chaves simétricas diretamente ao usuário final; preferir APIs seguras.
4. Implementar rotação de chaves (periodicamente regenerar e invalidar chaves antigas).
"""
