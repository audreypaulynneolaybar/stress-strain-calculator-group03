# task3_data_structures.py

# Tuples for immutable system configurations
UNITS = ("N", "m²", "m", "Pa")

# Set to track distinct materials tested across the session
unique_materials_tested = set()

# List to serve as our sequential test ledger
test_history = []

def run_test_session():
    # Example raw data simulation
    sample_tests = [
        {"mat": "Structural Steel", "F": 50000, "A": 0.01, "L0": 10.0, "dL": 0.005, "yield": 250e6},
        {"mat": "Aluminum 6061-T6", "F": 10000, "A": 0.002, "L0": 1.0, "dL": 0.0015, "yield": 276e6}
    ]

    for data in sample_tests:
        stress = data["F"] / data["A"]
        strain = data["dL"] / data["L0"]
        youngs = stress / strain if strain != 0 else float('inf') # Added handling for zero strain
        fos = data["yield"] / stress

        # Track unique materials
        unique_materials_tested.add(data["mat"])

        # Dictionary representation of a single record
        record = {
            "material": data["mat"],
            "force_N": data["F"],
            "area_m2": data["A"],
            "original_length_m": data["L0"],
            "delta_length_m": data["dL"],
            "stress_Pa": stress,
            "strain": strain,
            "youngs_modulus_Pa": youngs,
            "factor_of_safety": fos,
            "is_safe": fos >= 1.0
        }
        test_history.append(record)

def display_session_summary():
    if not test_history:
        print("No test data available.")
        return

    print("\n================ SESSION SUMMARY ================")
    print(f"Total Tests Executed:    {len(test_history)}")
    print(f"Unique Materials Tested: {', '.join(unique_materials_tested)}")

    stresses = [t["stress_Pa"] for t in test_history]
    avg_stress = sum(stresses) / len(stresses)
    max_stress = max(stresses)

    print(f"Average System Stress:   {avg_stress:,.2f} Pa")
    print(f"Maximum Observed Stress: {max_stress:,.2f} Pa")
    print("=================================================")

run_test_session()
display_session_summary()
