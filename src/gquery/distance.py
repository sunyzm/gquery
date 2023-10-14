from enum import Enum

class LengthUnit(Enum):
    KM = 1
    MI = 2


class Distance:
    def __init__(self, value: float, unit: LengthUnit | str):
        self.value = value
        if  isinstance(unit, LengthUnit):
            self.unit = unit
        else:
            match unit.lower():
                case "mi" | "mile":
                    self.unit = LengthUnit.MI
                case "km" | "kilometer":
                    self.unit = LengthUnit.KM
                case _:
                    raise ValueError("Unsupported unit")
    
    def __iadd__(self, other):
        if self.unit != other.unit:
            raise ValueError("Units do not match")
        
        self.value += other.value
        return self
    
    def __str__(self):
        if self.unit == LengthUnit.KM:            
            return f"{self.value:.1f} km"
        else:
            return f"{self.value:.1f} mi"
