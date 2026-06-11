from pathlib import Path

import yaml


class EntityExtractor:
    """Extract named entities from classical Chinese text.

    Uses gazetteer lists loaded from YAML reference files.
    """

    def __init__(self, reference_dir: Path) -> None:
        self.persons: dict[str, list[str]] = {}
        self.places: dict[str, list[str]] = {}
        self.terms: dict[str, list[str]] = {}

        persons_path = reference_dir / "personages.yaml"
        places_path = reference_dir / "place_names.yaml"
        terms_path = reference_dir / "ritual_terms.yaml"

        if persons_path.exists():
            with persons_path.open(encoding="utf-8") as f:
                self.persons = yaml.safe_load(f) or {}

        if places_path.exists():
            with places_path.open(encoding="utf-8") as f:
                self.places = yaml.safe_load(f) or {}

        if terms_path.exists():
            with terms_path.open(encoding="utf-8") as f:
                self.terms = yaml.safe_load(f) or {}
