# database.py
from typing import Dict, Optional, List
from properties import Metal, Material

# Predefined material database populated with Metal dataclass instances
PREDEFINED_MATERIALS: Dict[str, Material] = {
    "1": Metal(
        name="Structural Steel",
        density=7850.0,
        yield_strength_Pa=250e6,
        ultimate_strength_Pa=400e6
    ),
    "2": Metal(
        name="Aluminum 6061-T6",
        density=2700.0,
        yield_strength_Pa=276e6,
        ultimate_strength_Pa=310e6
    ),
    "3": Metal(
        name="Titanium Grade 5",
        density=4430.0,
        yield_strength_Pa=880e6,
        ultimate_strength_Pa=950e6
    )
}


def get_all_materials() -> Dict[str, Material]:
    """Returns the dictionary of all predefined materials."""
    return PREDEFINED_MATERIALS


def get_material_by_key(key: str) -> Optional[Material]:
    """
    Retrieves a material by its selection key.
    Returns None if key is invalid.
    """
    return PREDEFINED_MATERIALS.get(key)


def add_custom_material(key: str, material: Material) -> None:
    """Adds or updates a custom material in the database."""
    PREDEFINED_MATERIALS[key] = material


def list_material_names() -> List[str]:
    """Returns a list of all material names in the database."""
    return [mat.name for mat in PREDEFINED_MATERIALS.values()]