from typing import Any
from decimal import Decimal


class Point:
    def __init__(self, /, *args, **data: Any):
        super().__init__(**data)
        if len(args) == 2:
            self.x = args[0] if isinstance(args[0], Decimal) else Decimal(
                args[0])
            self.y = args[1] if isinstance(args[1], Decimal) else Decimal(
                args[1])
        else:
            self.x = Decimal(0.0)
            self.y = Decimal(0.0)

    def distance_between(self, other: 'Point') -> float:
        from extensions.custom_data_types import Dotted
        c1 = Dotted(other.x - self.x).square()
        c2 = Dotted(other.y - self.y).square()
        return Dotted(c1 + c2).square_root()
