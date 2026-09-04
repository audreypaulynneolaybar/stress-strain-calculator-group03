def get_valid_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

#in is put ng va is lues
force = get_valid_float_input("Enter applied force in Newtons: ")
area = get_valid_float_input("Enter cross-sectional area in square meters: ")
original_length = get_valid_float_input("Enter original length in meters: ")
change_in_length = get_valid_float_input("Enter change in length in meters: ")

#calculate stress and strain
stress = force / area
strain = change_in_length / original_length

print(f"Stress: {stress:.2f} Pa")
print(f"Strain: {strain:.6f}")
