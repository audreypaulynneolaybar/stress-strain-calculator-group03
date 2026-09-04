import math

# Material properties
materials = {
    "Steel": {
        "youngs_modulus": 200e9,
        "yield_strength": 250e6
    },
    "Aluminum": {
        "youngs_modulus": 69e9,
        "yield_strength": 276e6
    },
    "Copper": {
        "youngs_modulus": 117e9,
        "yield_strength": 70e6
    }
}

def get_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a value greater than 0.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def select_material():
    while True:
        print("\nAvailable materials:")
        for material in materials:
            print("-", material)
        print("- Custom")

        choice = input("Select a material: ").strip()

        if choice in materials:
            return choice, materials[choice]["youngs_modulus"], materials[choice]["yield_strength"]

        elif choice.lower() == "custom":
            name = input("Enter material name: ").strip()
            while not name:
                print("Material name cannot be empty.")
                name = input("Enter material name: ").strip()
            youngs_modulus = get_positive_number("Enter Young's modulus (Pa): ")
            yield_strength = get_positive_number("Enter yield strength (Pa): ")
            return name, youngs_modulus, yield_strength

        else:
            print("Invalid material selection. Please try again.")

def calculate_factor_of_safety(yield_strength, stress):
    """Calculates the factor of safety (from Task 2)."""
    if stress == 0:
        return float("inf") # handle zero stress to avoid division by zero
    return yield_strength / stress

def perform_calculation_and_record():
    print("\n--- Stress and Strain Calculation ---")

    force = get_positive_number("Enter applied force (N): ")
    area = get_positive_number("Enter cross-sectional area (m²): ")
    original_length = get_positive_number("Enter original length (m): ")
    change_in_length = get_positive_number("Enter change in length (m): ")

    material_name, youngs_modulus, yield_strength = select_material()

    stress = force / area
    strain = change_in_length / original_length

    factor_of_safety = calculate_factor_of_safety(
        yield_strength,
        stress
    )

    safety_result = "SAFE" if stress <= yield_strength else "UNSAFE"

    # Display results
    print("\n--- Results ---")
    print(f"Material: {material_name}")
    print(f"Stress: {stress:.2f} Pa")
    print(f"Strain: {strain:.6f}")
    print(f"Young's Modulus: {youngs_modulus:.2e} Pa")
    print(f"Yield Strength: {yield_strength:.2e} Pa")
    print(f"Factor of Safety: {factor_of_safety:.2f}")
    print(f"Safety Result: {safety_result}")

    # Return results as a dictionary
    return {
        "force": force,
        "area": area,
        "original_length": original_length,
        "change_in_length": change_in_length,
        "material_name": material_name,
        "youngs_modulus": youngs_modulus,
        "yield_strength": yield_strength,
        "stress": stress,
        "strain": strain,
        "factor_of_safety": factor_of_safety,
        "safety_result": safety_result
    }

def display_session_summary(history, unique_materials):
    print("\n--- Session Summary ---")
    if not history:
        print("No calculations performed in this session.")
        return

    total_tests = len(history)
    print(f"Total calculations performed: {total_tests}")

    print(f"Unique materials used: {', '.join(unique_materials)}")

    # statistical information
    total_stress = sum(record['stress'] for record in history)
    average_stress = total_stress / total_tests
    print(f"Average stress across all tests: {average_stress:.2f} Pa")

    # displaying history (first 3 records)
    print("\n--- Calculation History (First 3 Records) ---")
    for i, record in enumerate(history[:3]):
        print(f"Test {i+1}:")
        print(f"  Material: {record['material_name']}, Stress: {record['stress']:.2f} Pa, Strain: {record['strain']:.6f}, FoS: {record['factor_of_safety']:.2f}")

# Main program loop for Task 3
if __name__ == "__main__":
    calculation_history = []  # list to store dictionaries of test results
    unique_materials = set()  # set to track unique materials

    while True:
        test_result = perform_calculation_and_record()
        calculation_history.append(test_result)
        unique_materials.add(test_result['material_name'])

        another_calculation = input("\nPerform another calculation? (y/n): ").lower()
        if another_calculation != 'y':
            break

    display_session_summary(calculation_history, unique_materials)

