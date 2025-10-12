from dataclasses import dataclass, field
from typing import List

@dataclass
class Pruning:
    report_type: str
    value_type: str
    table_name: str
    column_predictions: List[str] = field(default_factory=List)
    column_schemas: List[str] = field(default_factory=List)