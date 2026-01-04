"""
Fidelity vs noise strength at perfect calibration.

This experiment studies how depolarizing noise alone
limits the achievable gate fidelity when calibration
is ideal (Δθ = 0).

Compatible with:
- Python 3.11
- qiskit == 1.0.2
"""

import numpy as np
import matplotlib.pyplot as plt

from qiskit.quantum_info import average_gate_fidelity
from gates.single_qubit import rx_gate


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

THETA_IDEAL = np.pi / 2
NOISE_LEVELS = np.linspace(0.0, 0.03, 25)


# ---------------------------------------------------------------------
# Experiment
# ---------------------------------------------------------------------

def run_fidelity_vs_noise():
    ideal_gate = rx_gate(THETA_IDEAL)
    fidelities = []

    for p in NOISE_LEVELS:
        fidelity = average_gate_fidelity(
            ideal_gate,
            ideal_gate
        )

        # Noise-induced degradation model
        fidelity *= (1.0 - p)

        fidelities.append(fidelity)

    return np.array(fidelities)


# ---------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------

def plot_results(fidelities):
    plt.figure(figsize=(7, 4))

    plt.plot(
        NOISE_LEVELS,
        fidelities,
        marker="o"
    )

    plt.xlabel("Depolarizing noise strength (p)")
    plt.ylabel("Average gate fidelity")
    plt.title("Gate Fidelity vs Noise (Perfect Calibration)")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        "fidelity_vs_noise.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

if __name__ == "__main__":
    fidelities = run_fidelity_vs_noise()
    plot_results(fidelities)
