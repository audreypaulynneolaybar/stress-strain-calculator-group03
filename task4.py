UNITS = ("N", "m^2", "m", "Pa")
MATERIALS = {"Steel": 250e6, "Aluminum": 70e6, "Copper": 70e6}

def calculate_stress(force, area):
    return force / area

def calculate_strain(change_in_length, original_length):
    return change_in_length / original_length

def calculate_youngs_modulus(stress, strain):
    return stress / strain

def calculate_factor_of_safety(yield_strength, stress):
    return yield_strength / stress

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("Must be > 0.")
        except ValueError:
            print("Invalid number.")

def select_material():
    print("1. Steel | 2. Aluminum | 3. Copper | 4. Custom")
    choice = input("Select (1-4): ")
    if choice in ("1", "2", "3"):
        material_name = ["Steel", "Aluminum", "Copper"][int(choice) - 1]
        return material_name, MATERIALS[material_name]
    return input("Custom name: "), get_positive_float("Yield strength (Pa): ")

def create_record(material_name, stress, strain, modulus, factor_of_safety):
    return {
        "material": material_name,
        "stress": stress,
        "strain": strain,
        "modulus": modulus,
        "factor_of_safety": factor_of_safety,
        "safe": factor_of_safety >= 1.0
    }

def display_result(record):
    print(f"\n--- Result ---\nMaterial: {record['material']}\nStress: {record['stress']:.2f} {UNITS[3]}")
    print(f"Strain: {record['strain']:.6f}\nYoung's Modulus: {record['modulus']:.2f} {UNITS[3]}")
    print(f"Factor of Safety: {record['factor_of_safety']:.2f}\nStatus: {'SAFE' if record['safe'] else 'UNSAFE'}")

def display_summary(history, unique_materials):
    if history:
        stresses = [record["stress"] for record in history]
        print(f"\n--- Summary ---\nTotal: {len(history)}\nMaterials: {', '.join(unique_materials)}")
        print(f"Avg Stress: {sum(stresses)/len(stresses):.2f} {UNITS[3]}")

def main():
    history, unique_materials = [], set()
    while True:
        material_name, yield_strength = select_material()
        force = get_positive_float(f"Force ({UNITS[0]}): ")
        area = get_positive_float(f"Area ({UNITS[1]}): ")
        original_length = get_positive_float(f"Length ({UNITS[2]}): ")
        change_in_length = get_positive_float(f"Delta L ({UNITS[2]}): ")

        stress = calculate_stress(force, area)
        strain = calculate_strain(change_in_length, original_length)
        modulus = calculate_youngs_modulus(stress, strain)
        factor_of_safety = calculate_factor_of_safety(yield_strength, stress)

        record = create_record(material_name, stress, strain, modulus, factor_of_safety)
        history.append(record)
        unique_materials.add(material_name)

        display_result(record)
        if input("\nAgain? (y/n): ").lower() != 'y':
            break

    display_summary(history, unique_materials)

if __name__ == "__main__":
    main()