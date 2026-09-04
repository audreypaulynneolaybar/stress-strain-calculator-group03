def get_valid_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def main():
    print("=== Stress and Strain Calculator ===")
    print()

    #user input
    force = get_valid_float_input("Enter applied force in Newtons: ")
    area = get_valid_float_input("Enter cross-sectional area in square meters: ")
    original_length = get_valid_float_input("Enter original length in meters: ")
    change_in_length = get_valid_float_input("Enter change in length in meters: ")

    #stress and strain calculations
    stress = force / area
    strain = change_in_length / original_length

    print()
    print("=== RESULTS ===")
    print(f"Force: {force:.2f} N")
    print(f"Area: {area:.2f} m²")
    print(f"Original Length: {original_length:.2f} m")
    print(f"Change in Length: {change_in_length:.2f} m")

    #output
    print()
    print(f"Stress: {stress:.2f} Pa")
    print(f"Strain: {strain:.6f}")

    # Bonus
    stress_mpa = stress / 1_000_000
    loading = "Tension" if change_in_length >= 0 else "Compression"

    print(f"Stress (MPa): {stress_mpa:.4f} MPa")
    print(f"Loading Type: {loading}")

    print()
    print("=== Analysis Complete ===")


if __name__ == "__main__":
    main()
