UNITS = ("N", "m^2", "m", "Pa")
MATERIALS = {"Steel": 250e6, "Aluminum": 70e6, "Copper": 70e6}

def calculate_stress(force, area):
    return force / area

def calculate_strain(original_length, change_in_length):
    return change_in_length / original_length

def calculate_youngs_modulus(stress, strain):
    return stress / strain

def calculate_factor_of_safety(yield_strength, stress):
    return yield_strength / stress

def validate_positive_number(value, parameter_name):
    if value <= 0:
        raise ValueError(f"{parameter_name} must be > 0.")
    return value

def validate_input(force, area, original_length, change_in_length):
    validate_positive_number(force, "Force")
    validate_positive_number(area, "Area")
    validate_positive_number(original_length, "Length")
    validate_positive_number(change_in_length, "Delta L")
    return True

def get_positive_float(prompt):
    while True:
        try:
            return validate_positive_number(float(input(prompt)), "Input")
        except ValueError as e:
            print(f"Invalid: {e}")

def get_materials_database():
    return MATERIALS.copy()

def create_calculation_record(material, inputs, results):
    return {
        "material": material,
        **inputs,
        **results,
        "safe": results["factor_of_safety"] >= 1.0
    }

def add_to_history(history_list, record):
    history_list.append(record)

def display_material_menu(database):
    print("\nMaterials: 1. Steel | 2. Aluminum | 3. Copper | 4. Custom")
    choice = input("Select (1-4): ").strip()
    keys = list(database.keys())
    if choice in ("1", "2", "3"):
        name = keys[int(choice) - 1]
        return name, database[name]
    
name = input("Custom material name: ").strip() or "Custom"
    return name, get_positive_float(f"Yield strength ({UNITS[3]}): ")

def display_calculation_results(record):
    print(f"\n--- Results: {record['material']} ---")
    print(f"Stress: {record['stress']:.2f} {UNITS[3]} | Strain: {record['strain']:.6f}")
    print(f"Modulus: {record['modulus']:.2e} {UNITS[3]} | Safety Factor: {record['factor_of_safety']:.2f}")
    print(f"Status: {'SAFE' if record['safe'] else 'UNSAFE'}")

def display_session_summary(history, unique_materials):
    if history:
        avg_stress = sum(r["stress"] for r in history) / len(history)
        print(f"\n--- Summary ---\nTotal Runs: {len(history)}")
        print(f"Materials: {', '.join(sorted(unique_materials))}")
        print(f"Avg Stress: {avg_stress:.2f} {UNITS[3]}")

def main_calculator(material, force, area, original_length, change_in_length):
    validate_input(force, area, original_length, change_in_length)
    stress = calculate_stress(force, area)
    strain = calculate_strain(original_length, change_in_length)
    modulus = calculate_youngs_modulus(stress, strain)
    return {"stress": stress, "strain": strain, "modulus": modulus}

def main():
    db, history, unique_materials = get_materials_database(), [], set()

while True:
        mat_name, yield_str = display_material_menu(db)
        inputs = {
            "force": get_positive_float(f"Force ({UNITS[0]}): "),
            "area": get_positive_float(f"Area ({UNITS[1]}): "),
            "original_length": get_positive_float(f"Length ({UNITS[2]}): "),
            "change_in_length": get_positive_float(f"Delta L ({UNITS[2]}): ")
        }

        results = main_calculator(mat_name, **inputs)
        results["factor_of_safety"] = calculate_factor_of_safety(yield_str, results["stress"])

        record = create_calculation_record(mat_name, inputs, results)
        add_to_history(history, record)
        unique_materials.add(mat_name)

        display_calculation_results(record)

        if input("\nCalculate again? (y/n): ").lower() != 'y':
            break

    display_session_summary(history, unique_materials)

if __name__ == "__main__":
    main()