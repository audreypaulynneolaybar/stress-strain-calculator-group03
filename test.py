# stress_calculator/test.py
from datetime import datetime
from typing import List, Dict, Any, Optional
from material import Material

class StressStrainTest:
    def __init__(
        self, 
        material: Material, 
        force_N: float, 
        area_m2: float, 
        length_m: float, 
        delta_length_m: float
    ):
        # Validation checks
        if area_m2 <= 0:
            raise ValueError("Cross-sectional area must be greater than zero.")
        if length_m <= 0:
            raise ValueError("Original length must be greater than zero.")
        if force_N < 0 or delta_length_m < 0:
            raise ValueError("Force and delta length cannot be negative.")

        # Encapsulated instance attributes
        self._material = material
        self._force_N = force_N
        self._area_m2 = area_m2
        self._length_m = length_m
        self._delta_length_m = delta_length_m
        self._timestamp = datetime.now()

    # --- Read-Only Properties ---
    @property
    def material(self) -> Material:
        return self._material

    @property
    def force_N(self) -> float:
        return self._force_N

    @property
    def area_m2(self) -> float:
        return self._area_m2

    @property
    def length_m(self) -> float:
        return self._length_m

    @property
    def delta_length_m(self) -> float:
        return self._delta_length_m

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    # --- Calculation Formulas as Properties ---
    @property
    def stress(self) -> float:
        """Calculates engineering stress in Pascals (σ = F / A)."""
        return self._force_N / self._area_m2

    @property
    def strain(self) -> float:
        """Calculates engineering strain (ε = ΔL / L₀)."""
        return self._delta_length_m / self._length_m

    @property
    def youngs_modulus(self) -> float:
        """Calculates Young's Modulus in Pascals (E = σ / ε)."""
        if self.strain == 0:
            raise ValueError("Strain cannot be zero when calculating Young's Modulus.")
        return self.stress / self.strain

    @property
    def factor_of_safety(self) -> float:
        """Calculates Factor of Safety (FoS = Yield Strength / Stress)."""
        return self._material.yield_strength_Pa / self.stress

    @property
    def is_safe(self) -> bool:
        """Evaluates structural safety threshold (FoS >= 1.0)."""
        return self.factor_of_safety >= 1.0

    # --- Serialization Helper ---
    def to_dict(self) -> Dict[str, Any]:
        """Converts test instance data into a dictionary for JSON/CSV exports."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "material_name": self.material.name,
            "category": self.material.material_category(),
            "force_N": self.force_N,
            "area_m2": self.area_m2,
            "original_length_m": self.length_m,
            "delta_length_m": self.delta_length_m,
            "stress_Pa": self.stress,
            "strain": self.strain,
            "youngs_modulus_Pa": self.youngs_modulus,
            "factor_of_safety": self.factor_of_safety,
            "status": "SAFE" if self.is_safe else "UNSAFE"
        }

    # --- Special Methods ---
    def __repr__(self) -> str:
        return (f"<StressStrainTest(Material='{self.material.name}', "
                f"Stress={self.stress:,.0f} Pa, Strain={self.strain:.6f})>")

    def __lt__(self, other: "StressStrainTest") -> bool:
        """Enables comparison and sorting based on Factor of Safety."""
        return self.factor_of_safety < other.factor_of_safety

    def __eq__(self, other: object) -> bool:
        """Equality based on calculated stress values."""
        if not isinstance(other, StressStrainTest):
            return False
        return self.stress == other.stress


class TestSession:
    """
    Manages historical records and summary statistics across multiple test runs.
    Encapsulates history list and unique_materials set management.
    """
    def __init__(self):
        self.history: List[StressStrainTest] = []
        self.unique_materials = set()

    def add_test(self, test: StressStrainTest) -> None:
        """Appends a new test object and updates the unique material set."""
        self.history.append(test)
        self.unique_materials.add(test.material.name)

    def get_summary_stats(self) -> Dict[str, Any]:
        """Computes aggregate statistical metrics over executed tests."""
        if not self.history:
            return {
                "total_tests": 0,
                "unique_materials_count": 0,
                "avg_stress_Pa": 0.0,
                "max_stress_Pa": 0.0,
                "min_stress_Pa": 0.0
            }

        stresses = [t.stress for t in self.history]
        return {
            "total_tests": len(self.history),
            "unique_materials_count": len(self.unique_materials),
            "unique_materials_list": list(self.unique_materials),
            "avg_stress_Pa": sum(stresses) / len(stresses),
            "max_stress_Pa": max(stresses),
            "min_stress_Pa": min(stresses)
        }

    def get_safest_test(self) -> Optional[StressStrainTest]:
        """Returns the test record with the highest Factor of Safety."""
        if not self.history:
            return None
        return max(self.history, key=lambda t: t.factor_of_safety)