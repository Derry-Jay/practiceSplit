from datetime import datetime, timedelta, timezone
from decimal import Decimal
from math import atan2
from typing import Any


class LatLong:
    def to_tuple(self) -> tuple:
        return self.lat, self.lon

    def to_dict(self):
        d = {'latitude': str(self.lat), 'longitude': str(self.lon)}
        return d

    def __eq__(self, value):
        return isinstance(value, LatLong) and value.lat == self.lat and value.lon == self.lon

    def belongs_to(self, ll: list) -> bool:
        return all(isinstance(item, LatLong) for item in ll) and len(ll) > 0 and ll.__contains__(self)

    def reverse_geocode(self,
                        result_type: str | list | None = None,
                        location_type: list | None = None,
                        language: str | None = None) -> Any:
        from utils.values import gmc
        try:
            return gmc.get_reverse_geocode_result(lat_lng=self, result_type=result_type,
                                                  language=language, location_type=location_type)
        except Exception as e:
            return e

    def from_list_or_tuple(self, t: list | tuple) -> 'LatLong':
        if t != [] and t != () and len(t) == 2:
            self.lat = t[0] if t[0] is Decimal else Decimal(t[0])
            self.lon = t[1] if t[1] is Decimal else Decimal(t[1])
        else:
            self.lat = Decimal(0.0)
            self.lon = Decimal(0.0)
        return self

    def __init__(self, /, *args, **data: Any):
        super().__init__(**data)
        if len(args) == 2:
            self.lat = args[0] if isinstance(args[0], Decimal) else Decimal(
                args[0])
            self.lon = args[1] if isinstance(args[1], Decimal) else Decimal(
                args[1])
        else:
            self.lat = Decimal(0.0)
            self.lon = Decimal(0.0)

    def __str__(self) -> str:
        from extensions.custom_data_types import Pointed
        lats = "°"
        longs = "°"
        if self.lat > 0:
            lats += "N"
        elif self.lat < 0:
            lats += "S"
        pass
        if self.lon > 0:
            longs += "E"
        elif self.lon < 0:
            longs += "W"
        return "Latitude: " + str(Pointed(self.lat).unsigned()) + lats + " Longitude: " + str(Pointed(self.lon)) + longs

    def haversine(self, other: 'LatLong') -> float:
        from extensions.custom_data_types import Pointed
        s_lat = Pointed(Pointed(self.lat + other.lat).unsigned())
        d_lat = Pointed(Pointed(self.lat - other.lat).unsigned())
        d_lon = Pointed(Pointed(self.lon - other.lon).unsigned())
        f3 = d_lon.cosine() * (d_lat.cosine() + s_lat.cosine())
        f1 = Pointed(Pointed(1 + s_lat.cosine() - f3).unsigned()).square_root()
        f2 = Pointed(Pointed(1 - s_lat.cosine() + f3).unsigned()).square_root()
        return (self.earth_radius() + other.earth_radius()) * atan2(f1, f2)

    def earth_radius(self) -> float:
        from extensions.custom_data_types import Pointed
        eq_rad = 6378.137
        pole_rad = 6356.752
        eq_rad_sq = eq_rad ** 2
        pole_rad_4 = pole_rad ** 4
        pole_rad_sq = pole_rad ** 2
        lat_cos_sq = Pointed(self.lat).cosine()
        v2 = (eq_rad_sq - pole_rad_sq) * lat_cos_sq
        v1 = ((eq_rad_sq ** 2) - pole_rad_4) * lat_cos_sq
        return Pointed(Pointed((v1 + pole_rad_4) / (v2 + pole_rad_sq)).unsigned()).square_root()

    def from_dict(self, json: dict) -> 'LatLong':
        if 'latitude' in json.keys() and 'longitude' in json.keys():
            self.lat = json['latitude'] if json['latitude'] is Decimal else Decimal(
                json['latitude'])
            self.lon = json['longitude'] if json['longitude'] is Decimal else Decimal(
                json['longitude'])
        elif 'latitude' in json.keys():
            self.lat = json['latitude'] if json['latitude'] is Decimal else Decimal(
                json['latitude'])
        elif 'longitude' in json.keys():
            self.lon = json['longitude'] if json['longitude'] is Decimal else Decimal(
                json['longitude'])
        else:
            self.lat = Decimal(0.0)
            self.lon = Decimal(0.0)
        return self

    def get_date_time_excluding_time_zone(self) -> datetime:
        from extensions.custom_data_types import Pointed, Dotted, Int
        ln = Pointed(Dotted(self.lon).to_float())
        lnp = Pointed(ln.decimal_part() * 4)
        lnp2 = Pointed(lnp.decimal_part() * 60)
        lnp3 = Pointed(lnp2.decimal_part() * 1000)
        lnp4 = Pointed(lnp3.decimal_part() * 1000)
        hr = Dotted(self.lon // 15)
        mn = Dotted((4 * (self.lon % 15)) + lnp.lower())
        sec = Int(lnp2.lower())
        ms = Int(lnp3.lower())
        mus = Int(lnp4.lower())
        dt = datetime.now(timezone.utc)
        t = timedelta(hours=hr.to_float(), minutes=mn.to_float(), seconds=sec.to_float(),
                      milliseconds=ms.to_float(),
                      microseconds=mus.to_float())
        if self.lon > 0:
            dt += t
        elif self.lat < 0:
            dt -= t
        else:
            pass
        return dt
