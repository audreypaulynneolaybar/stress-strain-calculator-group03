UNITS = ("N", "m^2", "m", "Pa")
MATERIALS = {"Steel": 250e6, "Aluminum": 70e6, "Copper": 70e6}

def calculate_stress(force,area):
    return force / area

def calculate_strain(change_in_length, original_length):
    return change_in_length / original_length

def calculate_youngs_modulus(stress,strain):
    return stress / strain

def calculate_factor_of_safety(yield_strength, stress):
    return yield_strength / stress