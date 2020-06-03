def floatConv(value: str):
    fl, unit = value.split(" ")
    return {"value": float(fl), "unit": unit}


def unitsToNum(value: str, units: map):
    num, unit = value.split(" ")

    if unit not in units:
        raise ValueError(f"unit {unit} not in units")

    try:
        num = int(num)
    except ValueError:
        try:
            num = float(num)
        except ValueError:
            raise

    if not (isinstance(num, int) or isinstance(num, float)):
        raise ValueError(f"number is not int or float")

    return num * units[unit]


def sizeToBytes(value: str) -> int:
    value = value.replace("/s", "")

    return int(unitsToNum(value, {
        "B": 1,
        "KB": 2 ** 10,
        "MB": 2 ** 20,
        "GB": 2 ** 30,
        "TB": 2 ** 40,
    }))


def speedToHz(value: str) -> int:
    return int(unitsToNum(value, {
        "Hz": 1,
        "kHz": 10 ** 3,
        "MHz": 10 ** 6,
        "GHz": 10 ** 9,
        "THz": 10 ** 12,
    }))


def toList(value: str) -> list:
    return value.split(", ")


def toPackage(value: str) -> list:
    return value.split(" x ")


def toTDP(value: str) -> float:
    watts, unit = value.split(" ")

    if unit != 'W':
        raise ValueError("unit was not W")

    return float(watts)
