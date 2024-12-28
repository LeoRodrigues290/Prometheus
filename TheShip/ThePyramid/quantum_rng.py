"""
Arquivo: TheShip/ThePyramid/quantum_rng.py
Descrição:
    - Implementa funções para geração de números aleatórios usando Qiskit.
    - Exemplo simples de circuito quântico com portas Hadamard e medição.
"""

import qiskit
from qiskit import Aer, execute

def generate_quantum_random_number(num_bits=128):
    """
    Gera um número aleatório com base no estado quântico de um circuito Qiskit.
    :param num_bits: Quantidade de bits a serem gerados.
    :return: Um inteiro aleatório equivalente ao resultado medido dos qubits.
    """
    circuit = qiskit.QuantumCircuit(num_bits, num_bits)

    # Coloca cada qubit em superposição usando portas Hadamard
    for i in range(num_bits):
        circuit.h(i)

    # Mede todos os qubits
    circuit.measure(range(num_bits), range(num_bits))

    # Usa o simulador local para executar 1 shot
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(circuit, simulator, shots=1)
    result = job.result()
    counts = result.get_counts(circuit)

    # Extrai a única medição (chave do dicionário 'counts')
    measured_str = list(counts.keys())[0]

    # Converte a string binária em inteiro
    random_number = int(measured_str, 2)
    return random_number

"""
MELHORIAS FUTURAS:
1. Integrar com um backend real da IBM Quantum para gerar verdadeira aleatoriedade quântica.
2. Adicionar testes estatísticos (NIST, Dieharder) para validar a qualidade dos bits gerados.
3. Expandir para protocolos completos de QKD (Quantum Key Distribution) em comunicações seguras.
4. Implementar redundância (executar circuito várias vezes e combinar resultados) para reduzir ruídos em hardware real.
"""
