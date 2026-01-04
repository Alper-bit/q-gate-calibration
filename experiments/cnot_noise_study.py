"""
Full (more realistic) CNOT noise study:
- Coherent error: small systematic ZZ phase error (calibration-like)
- Incoherent noise: T1/T2 thermal relaxation + two-qubit depolarizing
- Gate time depends on noise strength p (longer effective exposure)

Model:
  Φ(p) = Depol(p) ∘ Thermal(T1,T2, tau(p)) ∘ U_err ∘ U_ideal

Outputs:
  - plot + PNG file
"""

import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, SuperOp, average_gate_fidelity

from qiskit_aer.noise.errors import depolarizing_error, thermal_relaxation_error


# ---------------------------------------------------------------------
# Hardware-inspired parameters (tuneable, but realistic ranges)
# ---------------------------------------------------------------------

T1 = 30e-6          # 30 microseconds
T2 = 20e-6          # 20 microseconds
CNOT_TIME_0 = 300e-9  # base CNOT duration: 300 ns

# Gate-time growth with noise (simple but hardware-motivated proxy)
# tau(p) = CNOT_TIME_0 * (1 + ALPHA * p)
ALPHA = 15.0

# Coherent (systematic) ZZ phase error magnitude (radians)
# This models residual ZZ coupling / conditional phase miscalibration.
ZZ_PHASE_ERROR = 0.03  # ~1.7 degrees

# Noise sweep
NOISE_LEVELS = np.linspace(0.0, 0.03, 21)

SAVE_PATH = "cnot_fidelity_full_model.png"


# ---------------------------------------------------------------------
# Gate / channel builders
# ---------------------------------------------------------------------

def ideal_cnot_operator() -> Operator:
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    return Operator(qc)


def coherent_error_operator(zz_phi: float) -> Operator:
    """
    Build a small coherent two-qubit error as a ZZ phase rotation:
      U_err = exp(-i * zz_phi/2 * Z⊗Z)  == RZZ(zz_phi)

    In circuit form: RZZ(zz_phi) (Qiskit uses a standard definition).
    """
    qc = QuantumCircuit(2)
    qc.rzz(zz_phi, 0, 1)
    return Operator(qc)


def tau_of_p(p: float) -> float:
    """Effective gate duration depending on p (proxy for slower control / exposure)."""
    return CNOT_TIME_0 * (1.0 + ALPHA * p)


def full_noisy_cnot_channel(p: float) -> SuperOp:
    """
    Construct the full noisy channel:
      Φ(p) = Depol(p) ∘ Thermal(T1,T2,tau(p)) ∘ U_err ∘ U_ideal
    """
    # Ideal CNOT
    U_ideal = SuperOp(ideal_cnot_operator())

    # Coherent systematic error (calibration-like)
    U_err = SuperOp(coherent_error_operator(ZZ_PHASE_ERROR))

    # Thermal relaxation on both qubits, depends on tau(p)
    tau = tau_of_p(p)
    therm_q0 = thermal_relaxation_error(T1, T2, tau)
    therm_q1 = thermal_relaxation_error(T1, T2, tau)
    thermal_2q = therm_q0.tensor(therm_q1)
    N_thermal = SuperOp(thermal_2q)

    # Two-qubit depolarizing (incoherent) noise
    depol_2q = depolarizing_error(p, 2).to_quantumchannel()
    N_depol = SuperOp(depol_2q)

    # Compose (right-to-left action): start with U_ideal, then U_err, then thermal, then depol
    return N_depol.compose(N_thermal.compose(U_err.compose(U_ideal)))


# ---------------------------------------------------------------------
# Experiment
# ---------------------------------------------------------------------

def run_study():
    ideal = ideal_cnot_operator()
    fidelities = []

    for p in NOISE_LEVELS:
        noisy = full_noisy_cnot_channel(p)
        F = average_gate_fidelity(noisy, ideal)
        fidelities.append(F)

    return np.array(fidelities)


# ---------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------

def plot_results(fidelities: np.ndarray):
    plt.figure(figsize=(7.8, 4.6))
    plt.plot(NOISE_LEVELS, fidelities, marker="o")
    plt.xlabel("Two-qubit depolarizing strength (p)")
    plt.ylabel("Average gate fidelity (noisy channel vs ideal CNOT)")
    plt.title("CNOT Fidelity: Coherent + T₁/T₂ + Depolarizing (Full Model)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(SAVE_PATH, dpi=300, bbox_inches="tight")
    plt.show()
    print(f"Saved figure: {SAVE_PATH}")


if __name__ == "__main__":
    fidelities = run_study()
    plot_results(fidelities)
