# stress-strain-calculator-group03

> Project Title: Stress and Strain Analysis System

> Members:

Patrick Raphael Lista - Task 1 - Basic Calculations
Patricia Ann Mae Pascual - Task 2 – Control Structures
Maureen Joi Cruz - Task 3 – Data Structures
Gianela Zapata - Task 4 - Functions and Parameters
Audrey Paulynne Olaybar - Task 5 – Object-Oriented Programming

Note: Task 6 – Modular Integration was completed collaboratively by all members.

> Project Description

The Stress and Strain Analysis System is a comprehensive, object-oriented Python application designed for engineering calculations. It allows users to input physical measurements (force, cross-sectional area, length) to compute material stress, strain, and Young's modulus. The system models various material types, performs safety analyses, and maintains a session history of all conducted tests.

> Program Features

1. Core Calculations: Computes Stress (σ = F / A), Strain (ε = ΔL / L₀), and Young's modulus.
2. Robust Input Validation & Error Handling: Prevents crashes from division-by-zero, invalid numeric types, negative dimensions, or unselected materials.
3. Material Hierarchy & Dataclasses: Supports built-in and custom materials across distinct categories (Metal, Plastic, Composite) with predefined yield strengths and elastic moduli.
4. Session Tracking & Statistical Summaries: Maintains a comprehensive history of executed tests using Python data structures (lists, dicts, sets, tuples) to compute session metrics.
5. Data Persistence & File Operations:

Save and load full test sessions via JSON (json module).

Export structured test reports to CSV format (csv module).

Automatic directory and file path management (pathlib / os modules).

6. Simulated Test Data Generation: Utility to generate random stress-strain test scenarios for rapid verification (random module).

> Installation/Requirements

- Python: 3.8 or higher
- Packages: None (Uses Python Standard Library only)

- Standard Library Packages Used

1. dataclasses (Object-oriented domain modeling)
2. pathlib (Cross-platform file path handling)
3. csv & json (Data export and persistence)
4. datetime (Timestamping test sessions)
5. random (Simulation dataset generation)
6. abc & typing (Abstract base classes and type hinting)

> HOW TO RUN THE PROGRAM

1. Clone or download the repository to your local machine: 
    git clone https://github.com/your-username/stress-strain-calculator-groupXX.git

2. Navigate to the application folder:
    cd stress-strain-calculator-groupXX/stress_calculator

3. Run the application entry point:
    python main.py

> Repository Structure

stress_calculator/
│
├── material.py     # Material class hierarchy      (Material, Metal, Plastic, Composite)
├── properties.py   # Dataclasses for physical properties and constant units
├── tests.py        # Classes modeling individual StressStrainTest instances & session history
├── utils.py        # Core math formulas, validation functions, and file I/O helpers
├── database.py     # Predefined material database and custom material storage
└── main.py         # Entry point coordinating UI loop, menu workflows, and module integration




