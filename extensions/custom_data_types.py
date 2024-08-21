from ast import literal_eval
from base64 import b64encode
from datetime import datetime
from decimal import Decimal
from json import *
from math import ceil, sqrt, floor, sin, cos, tan, asin, acos, atan
from re import *
from typing import Any, Type, Mapping

from bson.codec_options import TypeRegistry
from fastapi.responses import JSONResponse
from googlemaps import Client
from googlemaps.geocoding import *
from googlemaps.geolocation import *
from pandas import DataFrame, Series
from pgeocode import COUNTRIES_VALID, Nominatim
from pyfcm import FCMNotification
from pymongo import MongoClient
from starlette.background import BackgroundTask

from models.lat_long import LatLong
from utils.methods import *


class Int(int):
    @extension
    def to_char(self) -> str:
        return chr(self)

    @extension
    def unsigned(self) -> int:
        return abs(self)

    @extension
    def to_string(self) -> str:
        return str(self)

    @extension
    def to_float(self) -> float:
        return float(self)

    @extension
    def square_root(self) -> float:
        return sqrt(self)

    @extension
    def geo_locate(self) -> Any:
        from utils.values import gmc
        try:
            return geolocate(client=gmc, home_mobile_country_code='+' + self.to_string())
        except Exception as e:
            return e

    @extension
    def square(self) -> int:
        return self.to_the_power_of(2)

    @extension
    def to_decimal(self) -> Decimal:
        return Decimal(self.to_float())

    @extension
    def to_the_power_of(self, p: int) -> int:
        return pow(self, p)

    @extension
    def is_eligible_age_to_vote(self) -> bool:
        return self >= 18

    @extension
    def either_zero_or_one(self) -> bool:
        return [0, 1].__contains__(self) or self == 0 or self == 1

    @extension
    def is_adam(self) -> bool:
        return self.square() == Int(Int(self.rev()).square()).rev()

    @extension
    def is_perfect_square(self) -> bool:
        sr = Pointed(self.square_root())
        return sr.upper() == sr.lower()

    @extension
    def is_perfect(self) -> bool:
        return self == sum([j for j in range(1, self) if self % j == 0])

    @extension
    def is_fibonacci_term(self) -> bool:
        a = 5 * self.square()
        b = 4
        return Int(a + b).is_perfect_square() or Int(a - b).is_perfect_square()

    @extension
    def nth_fibonacci_term(self) -> int:
        return self.__int__() if self.either_zero_or_one() else (
                Int(self - 1).nth_fibonacci_term() + Int(self - 2).nth_fibonacci_term())

    @extension
    def factorial(self) -> int:
        return (Int(-1).to_the_power_of(self.unsigned()) * (Int(self.unsigned()).factorial())) if self < 0 else (
            1 if self.either_zero_or_one() else self * Int(self - 1).factorial())

    @extension
    def is_strong(self) -> bool:
        s = 0
        a = self
        while a != 0:
            d = a % 10
            s += Int(d).factorial()
            a //= 10
        return s == self

    @extension
    def radians(self):
        pi = Decimal(11)
        st = Decimal(630)
        return (self * pi) / st

    @extension
    def is_armstrong(self) -> bool:
        s = 0
        a = self
        while a != 0:
            d = a % 10
            s += Int(d).to_the_power_of(3)
            a //= 10
        return s == self

    @extension
    def rev(self) -> int:
        t = 0
        c = self
        while c != 0:
            t = ((t * 10) + (c % 10))
            c //= 10
        return t

    @extension
    def nod(self) -> int:
        g = self
        i = 0
        while g != 0:
            i += 1
            g //= 10
        return i

    @extension
    def is_prime(self) -> bool:
        i = 2
        f = True
        k = self
        while i <= Pointed(k / 2).upper():
            if k % i == 0:
                f = False
                break
            i += 1
        return f

    @extension
    def number_to_words(self):
        k = self.rev()
        while k != 0:
            m = k % 10
            Int(m).number_to_word_single_digit(" ")
            k //= 10
        if self.nod() != Int(self.rev()).nod():
            for k in range(Int(self.rev()).nod(), self.nod()):
                zero(None if k == self.nod() else " ")

    @extension
    def number_to_word_single_digit(self, end: str | None):
        print(self.number_to_word_individual(), end=end if end is not None else "\n")

    @extension
    def number_in_words(self) -> str:
        k: int = self.rev()
        digits = []
        while k != 0:
            m = k % 10
            digits.append(Int(m).number_to_word_individual())
            k //= 10
        if self.nod() != Int(self.rev()).nod():
            for j in range(Int(self.rev()).nod(), self.nod()):
                digits.append(zeroStr())
        return ' '.join(digits)

    @extension
    def number_to_word_individual(self) -> str:
        if self == 0:
            return zeroStr()
        elif self == 1:
            return 'ONE'
        elif self == 2:
            return 'TWO'
        elif self == 3:
            return 'THREE'
        elif self == 4:
            return 'FOUR'
        elif self == 5:
            return 'FIVE'
        elif self == 6:
            return 'SIX'
        elif self == 7:
            return 'SEVEN'
        elif self == 8:
            return 'EIGHT'
        elif self == 9:
            return 'NINE'
        else:
            return 'INVALID'


class List(list):
    @extension
    def first(self):
        return self[0]

    @extension
    def last(self):
        return self[self.length() - 1]

    @extension
    def length(self) -> int:
        return len(self)

    @extension
    def to_dict(self) -> dict:
        return dict(self)

    @extension
    def join(self, s: str) -> str:
        return s.join(self)

    @extension
    def to_lat_long(self) -> LatLong:
        return LatLong().from_list_or_tuple(self)

    @extension
    def distinct_elements_count(self) -> int:
        return Tuple(self.distinct_elements()).length()

    @extension
    def distinct_elements(self) -> tuple:
        d = dict()
        n = 0
        for c in self:
            if c not in d:
                d[c] = 1
                n += 1
            else:
                d[c] += 1
        return tuple(d.keys())


class Json(dict):
    @extension
    def to_series(self) -> Series:
        return Series(self)

    @extension
    def to_data_frame(self) -> DataFrame:
        return DataFrame.from_dict(self)

    @extension
    def to_lat_long(self) -> LatLong:
        return LatLong().from_dict(self)

    @extension
    def get_data_frame(self) -> DataFrame:
        return DataFrame(self.items(), columns=tuple(self.keys()))

    @extension
    def symmetric_data_frame(self) -> DataFrame:
        return self.get_data_frame().compare(self.to_data_frame()).dropna()

    @extension
    def get_list_from_dict(self) -> list:
        g = []
        pk = ''
        for i in self.keys():
            smt = String(i).find_pattern('_id')
            if smt is None:
                g.append(self[i])
            else:
                tm = set_not_null_data(smt, Match())
                pk = tm.string
        if pk != '':
            g.append(self[pk])
        return g

    @extension
    def json_to_bytes(self, ecd: str | None, e: str | None) -> bytes:
        return b64encode(
            str(self).encode(ecd if ecd is not None else "utf-8", e if e is not None else "strict"))


class String(str):
    @extension
    def length(self) -> int:
        return len(self)

    @extension
    def unicode(self) -> int:
        return ord(self)

    @extension
    def is_empty(self) -> bool:
        return String(self.strip()).length() <= 0

    @extension
    def to_float(self) -> float:
        return float(self)

    @extension
    def is_not_empty(self) -> bool:
        return String(self.strip()).length() > 0

    @extension
    def to_decimal(self) -> Decimal:
        return Decimal(self)

    @extension
    def nominatim(self) -> Nominatim:
        return Nominatim(self)

    @extension
    def evaluate_literal(self) -> Any:
        return literal_eval(self)

    @extension
    def get_geocode_result(self) -> Any:
        from utils.values import gmc
        try:
            return gmc.get_geocode_result(address=self)
        except Exception as e:
            return e

    @extension
    def distinct_characters(self) -> str:
        d = dict()
        for c in self:
            if c not in d:
                d[c] = 1
            else:
                d[c] += 1
        return ', '.join(tuple(d.keys()))

    @extension
    def distinct_elements(self) -> tuple:
        d = dict()
        for c in self:
            if c not in d:
                d[c] = 1
            else:
                d[c] += 1
        return tuple(d.keys())

    @extension
    def to_int(self, r: int | None) -> int:
        return int(self) if r is None else int(self, r)

    @extension
    def distinct_elements_count(self) -> int:
        return len(self.distinct_elements())

    @extension
    def get_lat_long_from_zip_code(self) -> [LatLong]:
        g = [LatLong]
        for i in COUNTRIES_VALID:
            if self.is_not_empty():
                ldf = String(i).nominatim().query_postal_code(self).dropna()
                x = ldf.to_dict()
                if 'latitude' in x.keys() and 'longitude' in x.keys():
                    ao1 = LatLong(x['latitude'], x['longitude'])
                    if not (g.__contains__(ao1)):
                        g.append(ao1)
                    else:
                        continue
                else:
                    continue
            else:
                continue
        return g

    @extension
    def get_google_maps_client(self) -> 'GoogleMapsClient':
        return GoogleMapsClient(self)

    @extension
    def to_pattern(self, flags: int | RegexFlag = None) -> Pattern:
        return compile(self, flags if flags is not None else 0)

    @extension
    def to_fcm_instance(self, service_account_file: str) -> FCMNotification:
        return FCMNotification(service_account_file=service_account_file if service_account_file is not None else "",
                               project_id=self)

    @extension
    def generate_select_statement(self, attributes: list[str] | None, data: dict | None) -> str:
        sst = '''select '''
        j = 0
        if attributes is None:
            sst += ''' *'''
        else:
            for i in attributes:
                sst += i
                if j < len(attributes) - 1:
                    sst += ''', '''
                j += 1
        sst += ''' from ''' + self
        j = 0
        if data is not None and len(data.keys()) != 0:
            sst += ''' where '''
            for k in data.keys():
                sst += (k + '''=%s ''')
                if j < len(data.keys()) - 1:
                    sst += '''and '''
        return sst

    @extension
    def find_pattern(self, pattern: str | Pattern[str], flags: int | RegexFlag = None) -> Match[str] | None:
        return search(pattern, self, flags if flags is not None else 0)

    @extension
    def lades(self,
              cls: Type[JSONDecoder] | None = None) -> Any:
        return loads(self, cls=cls)

    @extension
    def get_mongo_db_instance(self,
                              connect: bool | None = None,
                              tz_aware: bool | None = None,
                              type_registry: TypeRegistry | None = None) -> MongoClient:
        sa = self.split(':')
        return MongoClient(self, port=String(List(sa).last()).to_int(), tz_aware=tz_aware, connect=connect,
                           type_registry=type_registry)


class Bytes(bytes):
    @extension
    def unicode(self) -> int:
        return ord(self)

    @extension
    def decoded(self, ecd: str | None, e: str | None) -> str:
        return self.decode(ecd if ecd is not None else "utf-8", e if e is not None else "strict")

    @extension
    def lades(self,
              cls: Type[JSONDecoder] | None = None) -> Any:
        return loads(self, cls=cls)


class Dynamic(Any):
    @extension
    def ditch(self,
              allow_nan: bool | None,
              cls: Type[JSONEncoder] | None,
              separators: tuple[str, str] | None,
              skip_keys: bool | None,
              indent: None | int | str,
              ensure_ascii: bool | None,
              check_circular: bool | None,
              sort_keys: bool | None) -> str:
        return dumps(obj=self, cls=cls, indent=indent, separators=separators,
                     skipkeys=skip_keys if skip_keys is not None else False,
                     allow_nan=allow_nan if allow_nan is not None else True,
                     sort_keys=sort_keys if sort_keys is not None else False,
                     ensure_ascii=ensure_ascii if ensure_ascii is not None else True,
                     check_circular=check_circular if check_circular is not None else True)

    @extension
    def to_json_response(self,
                         code: int | None = None,
                         media_type: str | None = None,
                         headers: Mapping[str, str] | None = None,
                         background: BackgroundTask | None = None) -> JSONResponse:
        return JSONResponse(content=self, headers=headers, media_type=media_type, background=background,
                            status_code=code if code is not None else 200)


class Tuple(tuple):
    @extension
    def length(self) -> int:
        return len(self)

    @extension
    def to_dict(self) -> dict:
        return dict(self)

    @extension
    def join(self, s: str) -> str:
        return s.join(self)

    @extension
    def to_lat_long(self) -> LatLong:
        return LatLong().from_list_or_tuple(self)

    @extension
    def distinct_elements(self) -> tuple:
        d = dict()
        n = 0
        for c in self:
            if c not in d:
                d[c] = 1
                n += 1
            else:
                d[c] += 1
        return tuple(d.keys())


class Pointed(float):
    @extension
    def to_decimal(self) -> Decimal:
        return Decimal(self)

    @extension
    def lower(self) -> int:
        return floor(self)

    @extension
    def upper(self) -> int:
        return ceil(self)

    @extension
    def square(self) -> float:
        return self ** 2

    @extension
    def is_eligible_age_to_vote(self) -> bool:
        return self >= 18

    @extension
    def decimal_part(self) -> float:
        return self.__float__() - self.lower()

    @extension
    def radians(self):
        pi = 11
        st = 630
        return (self * pi) / st

    @extension
    def is_perfect_square(self) -> bool:
        sr = self.square_root()
        return sr * sr == self

    @extension
    def unsigned(self) -> float:
        return abs(self)

    @extension
    def square_root(self) -> float:
        return sqrt(self)

    @extension
    def sine(self) -> float:
        return sin(self.radians())

    @extension
    def cosine(self) -> float:
        return cos(self.radians())

    @extension
    def tangent(self) -> float:
        return tan(self.radians())

    @extension
    def sine_inverse(self) -> float:
        return asin(self)

    @extension
    def cos_inverse(self) -> float:
        return acos(self)

    @extension
    def tan_inverse(self) -> float:
        return atan(self)


class Dotted(Decimal):
    @extension
    def lower(self) -> int:
        return floor(self)

    @extension
    def upper(self) -> int:
        return ceil(self)

    @extension
    def to_float(self) -> float:
        return float(self)

    @extension
    def square(self) -> Decimal:
        return self ** 2

    @extension
    def is_eligible_age_to_vote(self) -> bool:
        return self >= 18

    @extension
    def decimal_part(self) -> float:
        return self.__float__() - self.lower()

    @extension
    def radians(self):
        pi = 11
        st = 630
        return (self * pi) / st

    @extension
    def is_perfect_square(self) -> bool:
        sr = sqrt(self)
        return sr * sr == self

    @extension
    def unsigned(self) -> Decimal:
        return abs(self)

    @extension
    def square_root(self) -> float:
        return sqrt(self)

    @extension
    def sine(self) -> float:
        return sin(self.radians())

    @extension
    def cosine(self) -> float:
        return cos(self.radians())

    @extension
    def tangent(self) -> float:
        return tan(self.radians())

    @extension
    def sine_inverse(self) -> float:
        return asin(self)

    @extension
    def cos_inverse(self) -> float:
        return acos(self)

    @extension
    def tan_inverse(self) -> float:
        return atan(self)


class Error(Exception):
    @extension
    def to_string(self) -> str:
        return self.args[0].split('\n')[0]


class DateTime(datetime):
    @extension
    def to_string(self, date_format: str) -> str:
        return self.strftime(date_format)


class ByteArray(bytearray):
    @extension
    def unicode(self) -> int:
        return ord(self)

    @extension
    def lades(self,
              cls: Type[JSONDecoder] | None = None) -> Any:
        return loads(self, cls=cls)


class GoogleMapsClient(Client):
    @extension
    def get_geocode_result(self,
                           bounds: Any = None,
                           region: str = None,
                           address: str = None,
                           language: str = None,
                           place_id: str = None,
                           components: dict = None) -> Any:
        return geocode(client=self, address=address, place_id=place_id, components=components, bounds=bounds,
                       language=language, region=region)

    @extension
    def get_reverse_geocode_result(self,
                                   lat_lng: LatLong,
                                   language: str = None,
                                   location_type: list = None,
                                   result_type: str | list = None) -> Any:
        return reverse_geocode(client=self, latlng=lat_lng.to_tuple(), result_type=result_type,
                               location_type=location_type,
                               language=language)
