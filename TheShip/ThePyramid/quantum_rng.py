"""
Arquivo: TheShip/ThePyramid/quantum_rng.py
Descrição: Implementa funções para gerar números aleatórios usando Qiskit.
"""

import qiskit
from qiskit import Aer, execute

def generate_quantum_random_number(num_bits=128):
    """
    Gera um número aleatório com base no estado quântico de um circuito.
    :param num_bits: Quantidade de bits aleatórios que desejamos.
    :return: Um inteiro aleatório de tamanho num_bits.
    """
    # Cria um circuito quântico simples
    circuit = qiskit.QuantumCircuit(num_bits, num_bits)

    # Aplica portas Hadamard para colocar os qubits em superposição
    for i in range(num_bits):
        circuit.h(i)

    # Faz a medição
    circuit.measure(range(num_bits), range(num_bits))

    # Executa o circuito no simulador local
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(circuit, simulator, shots=1)
    result = job.result()
    counts = result.get_counts(circuit)

    # Extraímos a única chave de contagem obtida (pois shots=1)
    measured_str = list(counts.keys())[0]

    # Converte a string binária em inteiro
    random_number = int(measured_str, 2)

    return random_number

"""
MELHORIAS FUTURAS:
1. Integrar a execução em um backend quântico real da IBM Quantum para geração de números ainda mais seguros.
2. Implementar protocolos de QKD (Quantum Key Distribution) no futuro, possibilitando troca segura de chaves.
3. Adicionar mecanismos de reintento ou redundância (repetir medições e combinar resultados) para reduzir ruídos em backends reais.
4. Criar testes unitários que validem a aleatoriedade gerada (usando testes estatísticos como NIST ou Dieharder).
"""
