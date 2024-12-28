"""
Arquivo: tests/test_quantum_rng.py
"""

from TheShip.ThePyramid.quantum_rng import generate_quantum_random_number

def test_generate_quantum_random_number():
    result = generate_quantum_random_number(128)
    assert isinstance(result, int), "O resultado deve ser um inteiro"
    assert result > 0, "O número aleatório deve ser maior que zero"

"""
MELHORIAS FUTURAS:
1. Adicionar testes estatísticos (Dieharder, NIST SP 800-22) para aferir qualidade da aleatoriedade.
2. Incluir mocks para simular diferentes cenários de backends quânticos.
3. Configurar cobertura de código (coverage.py) e analisar relatórios.
4. Incorporar testes de integração e end-to-end (ex.: usando pytest + HTTP client).
"""
