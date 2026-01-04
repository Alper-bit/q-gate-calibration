"""
Single-qubit gate utilities.

Provides RX and RZ gate operators for numerical analysis.

Compatible with:
- qiskit == 1.0.2
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator


def rx_gate(theta: float) -> Operator:
    """
    Construct an RX gate operator.

    Parameters
    ----------
    theta : float
        Rotation angle in radians.

    Returns
    -------
    Operator
        RX gate as a quantum operator.
    """
    qc = QuantumCircuit(1)
    qc.rx(theta, 0)
    return Operator(qc)


def rz_gate(phi: float) -> Operator:
    """
    Construct an RZ gate operator.

    Parameters
    ----------
    phi : float
        Rotation angle in radians.

    Returns
    -------
    Operator
        RZ gate as a quantum operator.
    """
    qc = QuantumCircuit(1)
    qc.rz(phi, 0)
    return Operator(qc)
