from dataclasses import dataclass
from typing import Dict

@dataclass
class Airport:
    country_name: str
    iata_code: str
    name: str
    seo_name: str
    city: Dict[str, str]
