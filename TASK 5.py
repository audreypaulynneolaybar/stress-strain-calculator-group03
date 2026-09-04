from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class MaterialProperties:

    density: float  # kg/m³
    yield_strength: float  # MPa
    ultimate_strength: float  # MPa
    typical_youngs_modulus: float  # GPa

    def __post_init__(self):
        if self.density <= 0:
            raise ValueError("Density must be positive.")
        if self.yield_strength <= 0:
            raise ValueError("Yield strength must be positive.")
        if self.ultimate_strength <= 0:
            raise ValueError("Ultimate strength must be positive.")
        if self.typical_youngs_modulus <= 0:
            raise ValueError("Young's modulus must be positive.")


class Material(ABC):
    def __init__(self, name: str, properties: MaterialProperties):
        self.name = name
        self.properties = properties

    @abstractmethod
    def category(self) -> str:
        pass

    def can_withstand_stress(self, stress_mpa: float) -> bool:
        return abs(stress_mpa) < self.properties.yield_strength

    def __str__(self) -> str:
        return (
            f"{self.name} [{self.category()}] - Density: {self.properties.density} kg/m³, "
            f"Yield Strength: {self.properties.yield_strength} MPa"
        )


class Metal(Material):

    def __init__(
        self, name: str, properties: MaterialProperties, is_ferrous: bool = False
    ):
        super().__init__(name, properties)
        self.is_ferrous = is_ferrous

    def category(self) -> str:
        return "Ferrous Metal" if self.is_ferrous else "Non-Ferrous Metal"


class Plastic(Material):

    def __init__(
        self, name: str, properties: MaterialProperties, polymer_type: str
    ):
        super().__init__(name, properties)
        self.polymer_type = polymer_type

    def category(self) -> str:
        return f"Plastic ({self.polymer_type})"


class Composite(Material):

    def __init__(
        self, name: str, properties: MaterialProperties, matrix_type: str
    ):
        super().__init__(name, properties)
        self.matrix_type = matrix_type

    def category(self) -> str:
        return f"Composite ({self.matrix_type} matrix)"

class StressStrainTest:

    def __init__(
        self,
        material: Material,
        force: float,  # Newtons (N)
        area: float,  # Square millimeters (mm²)
        original_length: float,  # Millimeters (mm)
        change_in_length: float,  # Millimeters (mm)
    ):
        if force <= 0:
            raise ValueError("Force must be positive.")
        if area <= 0:
            raise ValueError("Cross-sectional area must be positive.")
        if original_length <= 0:
            raise ValueError("Original length must be positive.")

        self.material = material
        self._force = force
        self._area = area
        self._original_length = original_length
        self._change_in_length = change_in_length

    @property
    def stress(self) -> float:
        return self._force / self._area

    @property
    def strain(self) -> float:
        return self._change_in_length / self._original_length

    @property
    def youngs_modulus(self) -> float:
        if self.strain == 0:
            raise ValueError("Strain is zero; Young's Modulus is undefined.")
        # Converts MPa/strain to GPa (dividing by 1000)
        return (self.stress / self.strain) / 1000

    @property
    def factor_of_safety(self) -> float:
        if self.stress == 0:
            return float("inf")
        return self.material.properties.yield_strength / abs(self.stress)

    def will_fail(self) -> bool:
        return not self.material.can_withstand_stress(self.stress)

    def evaluate_status(self) -> str:
        current_stress = abs(self.stress)
        if current_stress >= self.material.properties.ultimate_strength:
            return "Ultimate Failure"
        elif current_stress >= self.material.properties.yield_strength:
            return "Plastic Deformation"
        return "Safe (Elastic)"

    def __str__(self) -> str:
        return (
            f"Test [{self.material.name}]: "
            f"Stress = {self.stress:.2f} MPa, "
            f"Strain = {self.strain:.6f}, "
            f"Modulus = {self.youngs_modulus:.2f} GPa"
        )


class MaterialTestAnalyzer:

    def __init__(self, tests: Optional[List[StressStrainTest]] = None):
        self.tests: List[StressStrainTest] = tests if tests is not None else []

    def add_test(self, test: StressStrainTest) -> None:
        """Appends a new test run to the analysis dataset."""
        self.tests.append(test)

    def generate_report(self) -> str:
        """Generates a text report summarizing test metrics."""
        if not self.tests:
            return "No test records available."

        header = (
            f"{'Material':<15} | {'Category':<20} | {'Stress (MPa)':<12} | "
                f"{'Strain':<10} | {'E Obs (GPa)':<11} | {'FOS':<6} | {'Status':<18}"
            )
        divider = "-" * len(header)
        lines = [header, divider]

        for t in self.tests:
            lines.append(
                f"{t.material.name:<15} | "
                f"{t.material.category():<20} | "
                f"{t.stress:<12.2f} | "
                f"{t.strain:<10.6f} | "
                f"{t.youngs_modulus:<11.2f} | "
                f"{t.factor_of_safety:<6.2f} | "
                f"{t.evaluate_status():<18}"
            )

        return "\n".join(lines)



if __name__ == "__main__":
    # Define Materials
    steel_props = MaterialProperties(
        density=7850, yield_strength=250, ultimate_strength=400, typical_youngs_modulus=200
    )
    aluminum_props = MaterialProperties(
        density=2700, yield_strength=95, ultimate_strength=110, typical_youngs_modulus=69
    )
    poly_props = MaterialProperties(
        density=950, yield_strength=20, ultimate_strength=30, typical_youngs_modulus=0.8
    )

    steel = Metal("Structural Steel", steel_props, is_ferrous=True)
    aluminum = Metal("Aluminum 6061", aluminum_props, is_ferrous=False)
    hdpe = Plastic("HDPE", poly_props, polymer_type="Thermoplastic")

    # Run Tests
    test1 = StressStrainTest(steel, force=50000, area=250, original_length=100, change_in_length=0.1)
    test2 = StressStrainTest(aluminum, force=30000, area=250, original_length=100, change_in_length=0.173)
    test3 = StressStrainTest(hdpe, force=1000, area=40, original_length=100, change_in_length=3.125)

    # Analyze & Report
    analyzer = MaterialTestAnalyzer([test1, test2, test3])
    print(analyzer.generate_report())