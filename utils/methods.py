from re import Match, search

from extensions.custom_data_types import String


def zeroStr() -> str:
    return 'ZERO'


def zero(end: str | None):
    print(zeroStr(), end=end if end is not None else "\n")


def set_not_null_data(c, d):
    print("++++++++++++++++++++++++++++++++++++++++")
    print(c)
    print("-----------------------------------------")
    return c if c is not None else d


def get_lat_long_from_zip_code_and_country_code(z: str, c: str) -> dict:
    if z is not None and c is not None and z != "" and c != "":
        return String(c).nominatim().query_postal_code(z).dropna().to_dict()
    else:
        return {}


def generate_count_statement(table_name: str, data: dict, primary_key: str) -> str:
    cqs = '''select count(''' + primary_key + ''') from ''' + \
          table_name + ''' where '''
    k = 0
    for i in data.keys():
        if search('_id', i) is None:
            cqs += (i + '''=%s''')
            if k < len(data.keys()) - 1:
                cqs += ''' and '''
            k += 1
    return cqs


def generate_insert_statement(table_name: str, data: dict) -> str:
    inst = '''insert into ''' + table_name + '''('''
    k = 0
    for i in data.keys():
        inst += i
        if k < len(data.keys()) - 1:
            inst += ''', '''
        else:
            inst += ''') '''
        k += 1
    inst += '''values('''
    for i in range(len(data.keys())):
        inst += '''%s'''
        if i < len(data.keys()) - 1:
            inst += ''', '''
        else:
            inst += ''')'''
    return inst


def generate_update_statement(table_name: str, data: dict) -> str:
    ust = '''update ''' + table_name + ''' set'''
    k = 0
    pk = ''
    for i in data.keys():
        tm1 = set_not_null_data(search('_id', i), Match())
        tm2 = set_not_null_data(
            search('_token', i), Match())
        if tm1 is None and tm2 is None:
            ust += (i + '''=%s''')
            if k < len(data.keys()) - 2:
                ust += ''', '''
            else:
                ust += ''' '''
            k += 1
        elif tm2 is not None:
            pk = tm2.string
        else:
            pk = tm1.string
    ust += ('''where ''' + pk + '''=%s''')
    return ust


def extension(func):
    # Define the wrapper function to extend int
    def wrapper(self, *args, **kwargs):
        # Perform any additional functionality here
        # print(f"Extended functionality for int: {func.__name__}")
        return func(self, *args, **kwargs)

    # Return the wrapper function
    return wrapper
