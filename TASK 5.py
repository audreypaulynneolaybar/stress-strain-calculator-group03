#task_oop

from dataclasses import dataclass
from abc import ABC, abstractmethod 

#Abstract base class
@dataclass
class Material (ABC):
    name: str
    density: float
    yeild_strength: float
    ultimate_strength: float

    @abstractmethod
    def material_category(self):
        pass

#subclasses

class Metal(Material):
    def material_category(self) -> str:
        return "Metallic material"

class Plastic(Material):
    def material_category(self) -> str:
        return "Polymeric material"

class Composite(Material):
    def material_category(self) -> str:
        return "Composite material"

#Test the classes
class StressStrainTest:
    def __init__(self, material: Material, force_N: float, area_m2: float, delta_length_m: float, original_length_m: float):
        self.material = material
        self.force_N = force_N
        self.area_m2 = area_m2
        self.delta_length_m = delta_length_m

    @property
    def stress(self):
        if self.area_m2 <= 0:
            raise ValueError("Area cannot be zero for stress calculation.")
        return self.force_N / self.area_m2

    @property
    def strain(self):
        if self.original_length_m <= 0:
            raise ValueError("Original length cannot be zero for strain calculation.")
        return self.delta_length_m / self.original_length_m

    @property
    def youngs_modulus(self):
        if self.strain == 0:
            raise ValueError("Strain cannot be zero for Young's modulus calculation.")
        return self.stress / self.strain        

    @property
    def factor_of_safety(self) -> float:
        if self.stress == 0:
            raise ValueError("Stress cannot be zero for factor of safety calculation.")
        return self.material.yeild_strength / self.stress

    def __repr__(self) -> str:
        return (f"StressStrainTest(material={self.material.name}, force_N={self.force_N}, "
                f"area_m2={self.area_m2}, delta_length_m={self.delta_length_m}, "
                f"original_length_m={self.original_length_m})")

if __name__ == "__main__":
    # Create instances of materials
    steel = Metal(name="Steel", density=7850, yeild_strength=250e6, ultimate_strength=400e6)
    polyethylene = Plastic(name="Polyethylene", density=950, yeild_strength=20e6, ultimate_strength=30e6)
    carbon_fiber = Composite(name="Carbon Fiber", density=1600, yeild_strength=600e6, ultimate_strength=800e6)

    # Create a stress-strain test for steel
    test_steel = StressStrainTest(material=steel, force_N=10000, area_m2=0.01, delta_length_m=0.002, original_length_m=1.0)
    
    print(f"Material: {test_steel.material.name}")
    print(f"Stress: {test_steel.stress} Pa")
    print(f"Strain: {test_steel.strain}")
    print(f"Young's Modulus: {test_steel.youngs_modulus} Pa")
    print(f"Factor of Safety: {test_steel.factor_of_safety}")