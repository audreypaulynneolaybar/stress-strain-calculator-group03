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

            youngs_modulus = get_positive_number(
                "Enter Young's modulus (Pa): "
            )

            yield_strength = get_positive_number(
                "Enter yield strength (Pa): "
            )

            return name, youngs_modulus, yield_strength

        else:
            print("Invalid material selection. Please try again.")

def calculate_factor_of_safety(yield_strength, stress):
    if stress == 0:
        return float("inf")

    return yield_strength / stress

def perform_calculation():

    print("\n--- Stress and Strain Calculation ---")

    force = get_positive_number(
        "Enter applied force (N): "
    )

    area = get_positive_number(
        "Enter cross-sectional area (m²): "
    )

    original_length = get_positive_number(
        "Enter original length (m): "
    )

    change_in_length = get_positive_number(
        "Enter change in length (m): "
    )

    material, youngs_modulus, yield_strength = select_material()

    stress = force / area
    strain = change_in_length / original_length

    factor_of_safety = calculate_factor_of_safety(
        yield_strength,
        stress
    )

    if stress <= yield_strength:
        safety_result = "SAFE"
    else:
        safety_result = "UNSAFE"

    # display results
    print("\n--- Results ---")
    print(f"Material: {material}")
    print(f"Stress: {stress:.2f} Pa")
    print(f"Strain: {strain:.6f}")
    print(f"Young's Modulus: {youngs_modulus:.2e} Pa")
    print(f"Yield Strength: {yield_strength:.2e} Pa")
    print(f"Factor of Safety: {factor_of_safety:.2f}")
    print(f"Safety Result: {safety_result}")


# MAIN PROGRAM
def main():

    print("===================================")
    print("   STRESS AND STRAIN ANALYZER")
    print("===================================")

    while True:

        perform_calculation()

        while True:
            again = input(
                "\nWould you like to perform another calculation? (yes/no): "
            ).strip().lower()

            if again in ["yes", "y"]:
                break

            elif again in ["no", "n"]:
                print("\nProgram terminated.")
                return

            else:
                print("Invalid choice. Please enter yes or no.")


main()