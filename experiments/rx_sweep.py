"""
RX gate calibration sensitivity experiment.

This experiment studies how small deviations in the RX rotation angle
and increasing depolarizing noise levels affect the average gate fidelity.

Compatible with:
- Python 3.11
- qiskit == 1.0.2
- qiskit-aer == 0.14.2
"""

import numpy as np
import matplotlib.pyplot as plt

from qiskit.quantum_info import average_gate_fidelity

from gates.single_qubit import rx_gate


# ---------------------------------------------------------------------
# Experiment configuration
# ---------------------------------------------------------------------

THETA_IDEAL = np.pi / 2
ANGLE_DEVIATIONS = np.linspace(-0.1, 0.1, 41)  # radians
DEPOLARIZING_LEVELS = [0.0, 0.005, 0.01, 0.02]


# ---------------------------------------------------------------------
# Experiment
# ---------------------------------------------------------------------

def run_rx_calibration_sweep():
    results = {}
    ideal_gate = rx_gate(THETA_IDEAL)

    for p in DEPOLARIZING_LEVELS:
        fidelities = []

        for delta in ANGLE_DEVIATIONS:
            test_gate = rx_gate(THETA_IDEAL + delta)

            # Ideal unitary mismatch fidelity
            fidelity = average_gate_fidelity(
                test_gate,
                ideal_gate
            )

            # Simple noise-induced degradation model
            fidelity *= (1.0 - p)

            fidelities.append(fidelity)

        results[p] = np.array(fidelities)

    return results


# ---------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------

def plot_results(results: dict):
    plt.figure(figsize=(8, 5))

    for p, fidelities in results.items():
        plt.plot(
            ANGLE_DEVIATIONS,
            fidelities,
            label=f"Depolarizing p = {p}"
        )

    plt.axvline(0.0, linestyle="--", color="gray", alpha=0.6)
    plt.xlabel("RX angle deviation Δθ (radians)")
    plt.ylabel("Average Gate Fidelity")
    plt.title("RX Gate Calibration Sensitivity")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

if __name__ == "__main__":
    results = run_rx_calibration_sweep()
    plot_results(results)
