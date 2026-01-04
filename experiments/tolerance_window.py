"""
Calibration tolerance window analysis.

This experiment computes the allowable RX angle deviation
range for which the average gate fidelity remains above
a target threshold, under increasing noise levels.
"""

import numpy as np
import matplotlib.pyplot as plt

from qiskit.quantum_info import average_gate_fidelity
from gates.single_qubit import rx_gate


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

THETA_IDEAL = np.pi / 2
ANGLE_DEVIATIONS = np.linspace(-0.15, 0.15, 601)
NOISE_LEVELS = [0.0, 0.005, 0.01, 0.02]
FIDELITY_THRESHOLD = 0.99


# ---------------------------------------------------------------------
# Experiment
# ---------------------------------------------------------------------

def compute_tolerance_window():
    ideal_gate = rx_gate(THETA_IDEAL)
    tolerance_ranges = []

    for p in NOISE_LEVELS:
        fidelities = []

        for delta in ANGLE_DEVIATIONS:
            test_gate = rx_gate(THETA_IDEAL + delta)

            fidelity = average_gate_fidelity(
                test_gate,
                ideal_gate
            )

            fidelity *= (1.0 - p)
            fidelities.append(fidelity)

        fidelities = np.array(fidelities)

        valid = ANGLE_DEVIATIONS[fidelities >= FIDELITY_THRESHOLD]

        if len(valid) > 0:
            tolerance = valid.max() - valid.min()
        else:
            tolerance = 0.0

        tolerance_ranges.append(tolerance)

    return tolerance_ranges


# ---------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------

def plot_results(tolerance_ranges):
    plt.figure(figsize=(7, 4))

    plt.plot(
        NOISE_LEVELS,
        tolerance_ranges,
        marker="o"
    )

    plt.xlabel("Depolarizing noise strength (p)")
    plt.ylabel("Allowed RX angle deviation range (radians)")
    plt.title("Calibration Tolerance Window vs Noise")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        "calibration_tolerance_window.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

if __name__ == "__main__":
    tolerance_ranges = compute_tolerance_window()
    plot_results(tolerance_ranges)
