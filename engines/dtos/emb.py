from dataclasses import dataclass

@dataclass
class Emb:
    score: float
    index: int
    value: str