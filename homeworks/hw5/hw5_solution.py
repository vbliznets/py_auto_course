def add_ing(s: str) -> str:
    s += 'ing'
    return s


def change_symbol(s: str) -> str:
    return s.replace('#', '/')


def change_order(s: str) -> str:
    s1 = s.split()
    s1[0], s1[1] = s1[1], s1[0]
    s: str = ' '.join(s1)
    return s


def clean_string(s: str) -> str:
    return s.strip()


def to_capitalize(s: str) -> str:
    return s.capitalize()


def to_list(s: str) -> list:
    return s.split()


def formatting(array: list, s1: str, s2: str) -> str:
    name, lastname = array
    return f"Привет, {name} {lastname}! Добро пожаловать в {s1} {s2}"


def to_string(array: list) -> str:
    return ' '.join(array)


def insert_to_list(array: list, item: int | str, indx: int) -> list:
    array.insert(indx, item)
    return array

def delete_from_list(array: list, indx: int) -> list:
    del array[indx]
    return array
