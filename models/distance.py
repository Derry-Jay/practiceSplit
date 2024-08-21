import re
from decimal import Decimal
from typing import Any

from pydantic import BaseModel


class MetricDistance(BaseModel):

    def __init__(self, /, *args, **data: Any):
        super().__init__(**data)
        if len(args) == 1:
            if isinstance(args[0], str) and len(re.findall(".", args[0])) == 1:
                arr = args[0].split(".")
                self.km = int(arr[0])
                self.m = int(arr[1])
            elif isinstance(args[0], float) or isinstance(args[0], Decimal):
                vl = str(round(args[0], 3)).split(".")
                self.km = int(vl[0])
                self.m = int(vl[1])
            else:
                self.km = 0
                self.m = 0
        if len(args) == 2:
            self.km = int(args[0])
            self.m = int(args[1])
        else:
            self.km = 0
            self.m = 0

    def __eq__(self, other: 'MetricDistance'):
        return isinstance(other, MetricDistance) and self.km == other.km and self.m == other.m

    def __add__(self, other: 'MetricDistance'):
        sk = 0
        sm = self.m + other.m
        if sm > 999:
            sk += 1
            sm -= 1000
        sk += (self.km + other.km)
        return MetricDistance(round(float(sk + (sm/1000)), 3))

    def __sub__(self, other: 'MetricDistance'):
        dm = 0
        dk = 0
        if isinstance(other, MetricDistance):
            if self.km > other.km:
                dm = self.m - other.m
                if dm < 0:
                    dm += 1000
                    dk = self.km - (other.km + 1)
                else:
                    dk = self.km - other.m
            elif self.km == other.km:
                if self.m > other.m:
                    dm = self.m - other.m
        return MetricDistance(round(float(dk + (dm/1000)), 3))

    def __str__(self):
        return str(round(self.km + (self.m/1000), 3)) + " Kilometres"
