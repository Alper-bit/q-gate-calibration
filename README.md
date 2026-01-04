# Quantum Gate Calibration Sensitivity Analysis

This repository presents a numerical study of quantum gate calibration
sensitivity using Qiskit, with a focus on performance metrics relevant
to superconducting quantum processors.

The project investigates how small calibration errors and noise sources
affect the fidelity of quantum gates, reflecting real-world challenges
encountered in experimental quantum computing and QPU performance
optimization.

---

## Motivation

In practical quantum hardware, quantum gates are never implemented
perfectly. Small deviations in control parameters (such as rotation
angles) and unavoidable noise sources can significantly degrade gate
performance and, consequently, the reliability of quantum algorithms.

Understanding **how sensitive gate fidelity is to calibration errors**
is a key part of experimental characterization, calibration, and
performance optimization of quantum processing units (QPUs).

This project aims to provide a **numerical and simulation-based
framework** to study such effects in a controlled and reproducible
manner.

---

## Scope of the Project

The current scope of the project includes:

- Numerical analysis of **single-qubit RX gate calibration sensitivity**
- Systematic sweep of rotation angle deviations
- Evaluation of **average gate fidelity** as a performance metric
- Investigation of noise-induced fidelity degradation
- Scientific visualization of calibration tolerance and noise effects

The structure and methodology are designed to be extendable to
two-qubit gates (e.g., CNOT) and more advanced noise models.

---

## Methodology Overview

1. **Ideal Gate Definition**  
   An ideal RX gate with a target rotation angle is defined as a unitary
   operator.

2. **Calibration Error Modeling**  
   Small deviations around the ideal rotation angle are introduced to
   simulate imperfect calibration.

3. **Fidelity Evaluation**  
   The average gate fidelity between the ideal gate and the perturbed
   gate is computed using Qiskit’s quantum information tools.

4. **Noise Impact Modeling**  
   Noise strength is introduced as a degradation factor to emulate the
   effect of realistic hardware noise on gate performance.

5. **Visualization and Analysis**  
   Fidelity is plotted as a function of calibration error for different
   noise levels, revealing tolerance margins and performance trends.

---

## Getting Started

### Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.11**
- **pip**

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd new_Projects
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

The main experiment can be executed by running the RX calibration sweep script:

```bash
python experiments/rx_sweep.py
```

This will:
- Perform a systematic sweep of RX gate rotation angle deviations
- Calculate average gate fidelity for different depolarizing noise levels
- Generate and display a visualization plot showing calibration sensitivity

### Expected Output

When you run the experiment, you should see:
- A matplotlib window displaying a plot with:
  - X-axis: RX angle deviation Δθ (in radians, ranging from -0.1 to 0.1)
  - Y-axis: Average Gate Fidelity
  - Multiple curves representing different depolarizing noise levels (p = 0.0, 0.005, 0.01, 0.02)
  - A vertical dashed line at Δθ = 0 indicating the ideal calibration point

The plot demonstrates how gate fidelity degrades as calibration errors increase and as noise levels rise, providing insights into the tolerance margins for quantum gate calibration.

### Project Structure

```
new_Projects/
├── experiments/
│   ├── __init__.py
│   └── rx_sweep.py          # Main experiment script
├── gates/
│   ├── __init__.py
│   └── single_qubit.py      # Single-qubit gate implementations
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

### Troubleshooting

- **Import errors**: Ensure all dependencies are installed correctly using `pip install -r requirements.txt`
- **Matplotlib display issues**: If the plot doesn't appear, ensure you have a display backend configured. On some systems, you may need to set `matplotlib.use('TkAgg')` or use a different backend
- **Qiskit version compatibility**: This project is tested with Qiskit 1.0.2. If you encounter issues, ensure you're using the versions specified in `requirements.txt`