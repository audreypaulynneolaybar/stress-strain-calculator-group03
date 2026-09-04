# properties.py
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# Immutable system constants
UNITS = ("N", "m²", "m", "Pa")

# --- DATACLASSES FOR MATERIAL PROPERTIES ---

@dataclass
class Material(ABC):
    name: str
    density: float
    yield_strength: float
    ultimate_strength: float

    @abstractmethod
    def material_category(self) -> str:
        pass


@dataclass
class Metal(Material):
    def material_category(self) -> str:
        return "Metallic material"


@dataclass
class Plastic(Material):
    def material_category(self) -> str:
        return "Polymeric material"


@dataclass
class Composite(Material):
    def material_category(self) -> str:
        return "Composite material"


# --- DATACLASS FOR TEST RECORD DATA STRUCTURE ---

@dataclass
class TestRecord:
    material: str
    force_N: float
    area_m2: float
    original_length_m: float
    delta_length_m: float
    stress_Pa: float
    strain: float
    youngs_modulus_Pa: float
    factor_of_safety: float
    is_safe: bool = field(init=False)

    def __post_init__(self):
        self.is_safe = self.factor_of_safety >= 1.0