from dataclasses import dataclass

@dataclass
class CPUMeasure:
    user: float
    system: float
    idle: float

