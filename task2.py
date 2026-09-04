# Predefined Material Yield Strengths (Pa)
MATERIALS = {
    "1": ("Structural Steel", 250e6),
    "2": ("Aluminum 6061-T6", 276e6),
    "3": ("Titanium Grade 5", 880e6)
}

def get_positive_float(prompt: str) -> float:
    """Repeatedly prompts the user until a positive numeric value is entered."""
    while True:
        try:
            val = float(input(prompt))
            if val <= 0:
                print("Error: Value must be greater than zero.")
                continue
            return val
        except ValueError:
            print("Error: Invalid numeric input. Please enter a valid number.")

while True:
    print("\n--- MATERIAL SELECTION ---")
    for key, (name, yield_str) in MATERIALS.items():
        print(f"[{key}] {name} (Yield Strength: {yield_str/1e6:.1f} MPa)")
    print("[4] Custom Material")
    print("[5] Exit Program")

    choice = input("Select an option (1-5): ").strip()
    if choice == "5":
        print("Exiting program...")
        break

    if choice in MATERIALS:
        mat_name, yield_strength = MATERIALS[choice]
    elif choice == "4":
        mat_name = input("Enter custom material name: ").strip()
        yield_strength = get_positive_float("Enter material yield strength (Pa): ")
    else:
        print("Invalid selection. Please choose between 1 and 5.")
        continue
        
     # Input gathering with strict validation
    force = get_positive_float("Enter applied force (N): ")
    area = get_positive_float("Enter cross-sectional area (m²): ")
    length = get_positive_float("Enter original length (m): ")
    delta_length = get_positive_float("Enter change in length (m): ")

    stress = force / area
    strain = delta_length / length
    factor_of_safety = yield_strength / stress

    print(f"\nResults for {mat_name}:")
    print(f"Calculated Stress: {stress:,.2f} Pa")
    print(f"Factor of Safety:  {factor_of_safety:.2f}")

    # Safety decision boundary
    if factor_of_safety < 1.0:
        print("WARNING: Material failure predicted! (FoS < 1.0)")
    elif factor_of_safety < 1.5:
        print("CAUTION: Low safety margin. Redesign recommended.")
    else:
        print("STATUS: Design is structurally safe under applied loads.")        