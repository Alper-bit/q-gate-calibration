"""
Two-qubit gate utilities.

Provides ideal CNOT gate operators for numerical analysis.
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator


def cnot_gate() -> Operator:
    """
    Construct an ideal CNOT gate operator.

    Returns
    -------
    Operator
        Ideal CNOT gate as a quantum operator.
    """
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    return Operator(qc)
