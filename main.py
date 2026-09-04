# main.py
import csv
import json
import random
from datetime import datetime
from pathlib import Path

# Fixed imports: Added Metal to allow concrete object instantiation
from database import get_all_materials, get_material_by_key, add_custom_material
from properties import Metal, Material
from test import StressStrainTest, TestSession
import utils

# Output directory path setup
OUTPUT_DIR = Path("output_data")
OUTPUT_DIR.mkdir(exist_ok=True)


def get_yes_no_choice(prompt: str) -> bool:
    """Prompts the user repeatedly until a valid 'y' or 'n' is entered."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in ('y', 'yes'):
            return True
        elif choice in ('n', 'no'):
            return False
        print("Invalid input. Please enter 'y' for yes or 'n' for no.")


def select_material() -> Material:
    """Handles material selection from the database or custom creation."""
    print("\n--- Select Material ---")
    materials = get_all_materials()

    for key, mat in materials.items():
        print(f"{key}. {mat.name} - Yield Strength: {mat.yield_strength_Pa / 1e6:.1f} MPa")
    
    custom_option_key = str(len(materials) + 1)
    print(f"{custom_option_key}. Custom Material")

    while True:
        choice = input("Enter choice number: ").strip()

        if choice in materials:
            return materials[choice]
        elif choice == custom_option_key:
            break
        else:
            print(f"Invalid selection. Please enter a number between 1 and {custom_option_key}.")

    # Custom material input flow
    print("\n--- Create Custom Material ---")
    custom_name = input("Enter material name: ").strip() or "Custom Material"
    yield_str = utils.get_positive_float("Yield Strength (Pa): ")
    ult_str = utils.get_positive_float("Ultimate Strength (Pa): ")
    density = utils.get_positive_float("Density (kg/m³): ")

    # Instantiating the concrete Metal subclass instead of abstract Material
    custom_mat = Metal(
        name=custom_name,
        density=density,
        yield_strength_Pa=yield_str,
        ultimate_strength_Pa=ult_str
    )
    
    # Save to memory cache with unique key
    new_key = str(len(get_all_materials()) + 1)
    add_custom_material(new_key, custom_mat)
    return custom_mat


def run_simulated_tests(session: TestSession, count: int = 3) -> None:
    """Generates random test datasets using random module."""
    print(f"\n[SIMULATION] Generating {count} random test datasets...")
    materials_list = list(get_all_materials().values())

    if not materials_list:
        print("[WARNING] No materials available to generate simulations.")
        return

    for _ in range(count):
        mat = random.choice(materials_list)
        force = random.uniform(10_000, 100_000)
        area = random.uniform(0.001, 0.01)
        length = random.uniform(0.5, 3.0)
        delta_l = random.uniform(0.0001, 0.005)

        try:
            test = StressStrainTest(
                material=mat,
                force_N=force,
                area_m2=area,
                length_m=length,
                delta_length_m=delta_l
            )
            session.add_test(test)
        except ValueError as err:
            continue


def export_session_csv(session: TestSession, filepath: Path) -> None:
    """Exports session history into a CSV spreadsheet."""
    if not session.history:
        return

    records = [test.to_dict() for test in session.history]
    fieldnames = list(records[0].keys())

    try:
        with open(filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

        print(f"[CSV EXPORT] Saved data to: {filepath.resolve()}")
    except IOError as err:
        print(f"[ERROR] Failed to save CSV file: {err}")


def save_session_json(session: TestSession, filepath: Path) -> None:
    """Saves test session summary and records to JSON format."""
    payload = {
        "timestamp": datetime.now().isoformat(),
        "summary": session.get_summary_stats(),
        "records": [test.to_dict() for test in session.history]
    }

    try:
        with open(filepath, mode="w", encoding="utf-8") as file:
            json.dump(payload, file, indent=4)

        print(f"[JSON PERSISTENCE] Saved payload to: {filepath.resolve()}")
    except IOError as err:
        print(f"[ERROR] Failed to save JSON file: {err}")


def main():
    session = TestSession()
    print("=== Raw Material Stress & Strain Analysis System ===")

    # If the user says 'n' right away, exit directly with goodbye
    if not get_yes_no_choice("Generate simulated test data first? (y/n): "):
        print("\nThank you for using the Stress & Strain Analysis System. Goodbye!")
        return

    # If they said 'y', generate simulated tests
    run_simulated_tests(session, count=3)

    # Interactive test execution loop
    while True:
        material = select_material()

        print(f"\n--- Enter Test Parameters ({material.name}) ---")
        force_N = utils.get_positive_float("Force (N): ")
        area_m2 = utils.get_positive_float("Area (m²): ")
        length_m = utils.get_positive_float("Original Length (m): ")
        delta_length_m = utils.get_positive_float("Delta Length (m): ")

        try:
            test = StressStrainTest(
                material=material,
                force_N=force_N,
                area_m2=area_m2,
                length_m=length_m,
                delta_length_m=delta_length_m
            )
            session.add_test(test)

            print("\n================ TEST RESULT ================")
            print(f"Material:         {test.material.name}")
            print(f"Stress:           {test.stress:,.2f} Pa")
            print(f"Strain:           {test.strain:.6f}")
            print(f"Young's Modulus:  {test.youngs_modulus:,.2f} Pa")
            print(f"Factor of Safety: {test.factor_of_safety:.2f}")
            print(f"Status:           {'SAFE' if test.is_safe else 'UNSAFE'}")
            print("=============================================")

        except ValueError as err:
            print(f"\n[ERROR] Invalid parameters: {err}")

        # Input validation loop for running another test
        if not get_yes_no_choice("\nRun another test? (y/n): "):
            break

    # Final summary output
    stats = session.get_summary_stats()
    print("\n================ SESSION SUMMARY ================")
    print(f"Total Tests Executed: {stats['total_tests']}")
    if stats['total_tests'] > 0:
        print(f"Avg Stress:           {stats['avg_stress_Pa']:,.2f} Pa")
        print(f"Max Stress:           {stats['max_stress_Pa']:,.2f} Pa")
    print("=================================================")

    # File exports using datetime timestamps
    if session.history:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_session_csv(session, OUTPUT_DIR / f"session_{timestamp}.csv")
        save_session_json(session, OUTPUT_DIR / f"session_{timestamp}.json")

    # Goodbye message on normal exit
    print("\nThank you for using the Stress & Strain Analysis System. Goodbye!")


if __name__ == "__main__":
    main()