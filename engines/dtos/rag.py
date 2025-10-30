from dataclasses import dataclass, field
from typing import List

@dataclass
class RagFilterSchema:
    field: str
    operator: str
    value: str | int | List[str] | None = None


@dataclass
class RagSchema:
    greeting_statements: str
    closing_statements: str
    filters: List[RagFilterSchema] = field(default_factory=list)
