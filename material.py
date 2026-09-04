from dataclasses import dataclass
from abc import ABC, abstractmethod 

#Abstract base class
@dataclass
class Material (ABC):
    name: str
    density: float
    yield_strength: float
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