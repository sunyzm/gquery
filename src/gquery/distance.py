from enum import Enum


class LengthUnit(Enum):
    KM = 1
    MI = 2


class Distance:
    mi_to_km: float = 1.60934

    def __init__(self, value: float, unit: LengthUnit | str):
        self.value = value
        if isinstance(unit, LengthUnit):
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

    def to_km(self):
        if self.unit == LengthUnit.KM:
            return self
        return Distance(self.value * Distance.mi_to_km, LengthUnit.KM)

    @classmethod
    def from_str(cls, raw_string: str):
        if (split := raw_string.find("km")) >= 0:
            val = float(raw_string[0:split])
            return cls(val, LengthUnit.KM)

        if (split := raw_string.find("mi")) >= 0:
            val = float(raw_string[0:split])

            return cls(val, LengthUnit.MI)

        val = float(raw_string)
        return cls(val, LengthUnit.KM)
