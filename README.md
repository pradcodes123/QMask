# Quantum QML Obfuscation Framework

Architecture-aware benchmarking and analysis framework for evaluating the structural and semantic impact of obfuscation on Quantum Machine Learning (QML) circuits using QASM-level transformations.

---

## Overview

This project provides a unified platform for:

* Parsing and executing OpenQASM circuits
* Applying multiple circuit-level obfuscation techniques
* Evaluating semantic preservation after transformation
* Measuring structural distortion across different QML architectures
* Visualizing circuit transformations and benchmarking metrics

The framework supports both:

* Predefined QML circuit templates
* Custom user-provided QASM circuits

---

# Features

## Obfuscation Techniques

Implemented transformation pipelines include:

* Composite Gate Insertion
* Cloaked Gate Substitutions
* Basis Transformations
* Delayed Gate Structures
* Inverse-Gate Obfuscation
* Identity Padding & Structural Expansion

Each technique supports:

* Light obfuscation
* Moderate obfuscation
* Heavy obfuscation

---

## Supported QML Circuit Families

The framework currently supports architecture-aware analysis for:

| Circuit Family   | Description                               |
| ---------------- | ----------------------------------------- |
| VQC / HEA        | Variational Quantum Circuits              |
| TTN              | Tree Tensor Networks                      |
| IQP              | Instantaneous Quantum Polynomial circuits |
| QAOA             | Optimization-oriented ansätze             |
| Data Reuploading | Repeated classical encoding architectures |
| MPU              | Multi-Parameterized Unitary structures    |
| SEL              | Supervised Entanglement Learning circuits |

---

# Architecture-Aware Metrics

Unlike generic black-box benchmarking, the framework evaluates circuit-specific structural properties.

## General Metrics

* Semantic Accuracy
* Total Variation Distance (TVD)
* Runtime Overhead
* Distribution Fidelity
* Obfuscation Score

## Circuit-Specific Metrics

### VQC / HEA

* Depth Growth
* Entangling Gate Shift

### TTN

* Connectivity Expansion
* Hierarchy Preservation

### IQP

* Phase Structure Preservation
* Phase Gate Ratio

### QAOA

* Mixer Layer Shift
* Cost Layer Shift
* Optimization Structure Preservation

### Data Reuploading

* Encoding Density Ratio
* Reupload Depth Growth

### MPU

* Parameter Density Ratio
* Unitary Structure Preservation

### SEL

* Entanglement Shift
* Learning Structure Preservation

---

# Tech Stack

## Backend

* FastAPI
* Qiskit
* Qiskit Aer
* Python

## Frontend

* HTML
* CSS
* Vanilla JavaScript

## Visualization

* Matplotlib
* Dynamic metric rendering
* Circuit comparison visualization

---

# Project Structure

project/
│
├── frontend/
│   ├── data/
│   │   └── predefined/
│   │       ├── HEA/
│   │       ├── IQP/
│   │       ├── QAOA/
│   │       └── ...
│
├── services/
│   ├── analyzer.py
│   ├── metrics_router.py
│   ├── score.py
│   ├── circuit_classifier.py
│   │
│   └── metrics_specific/
│       ├── vqc_metrics.py
│       ├── ttn_metrics.py
│       ├── iqp_metrics.py
│       ├── qaoa_metrics.py
│       └── ...
│
├── techniques/
│   ├── composite_gates.py
│   ├── inverse_gates.py
│   ├── cloaked_gates.py
│   └── ...
│
├── main.py
└── README.md


---

# Installation

## Clone Repository


git clone <repo-url>
cd <repo-name>


---

## Install Dependencies


pip install -r requirements.txt


---

# Run Backend


uvicorn main:app --reload


Backend runs at:


http://127.0.0.1:8000


Swagger API docs:

http://127.0.0.1:8000/docs


---

# API Usage

## POST `/analyze`

### Request Body

{
  "qasm": "OPENQASM 2.0; ...",
  "technique": "composite",
  "level": "moderate",
  "circuit_name": "VQC_2"
}


---

## Response

{
  "score": 0.84,
  "general_metrics": {},
  "specific_metrics": {},
  "counts_original": {},
  "counts_obfuscated": {},
  "images": {}
}

---

# Visualization Features

* Original vs Obfuscated Circuit Comparison
* Dynamic Metric Dashboard
* Circuit-Specific Metric Rendering
* Runtime & Structural Analysis
* QASM Benchmark Visualization

---

# Research Motivation

Quantum Machine Learning circuits are increasingly vulnerable to:

* Reverse engineering
* Structural extraction
* Intellectual property leakage

This project explores whether obfuscation techniques can:

* Conceal circuit structure
* Preserve semantic behavior
* Maintain trainability and utility
* Resist optimization simplification

while remaining executable under realistic QML workflows.

---

# Future Work

* Compiler-aware obfuscation analysis
* Hardware-aware benchmarking
* Gradient landscape analysis
* Noise-model evaluation
* Exportable benchmarking reports
* Interactive visualization dashboards

---

# Author

**Pradyun P**
Amrita Vishwa Vidyapeetham
Quantum ML Obfuscation Research Framework
