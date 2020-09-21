import json
import re
from pathlib import Path

rootProps = ['id', 'name', 'number', 'URL', 'socket', 'price']
reSubs = [(re.compile(pat), sub) for pat, sub in [
    (r"^" + '|'.join(rootProps) + "$", r''),
    (r"^None$", r''),
    (r"^Q1\s*'(\d\d)$", r'20\1-01-01'),
    (r"^Q2\s*'(\d\d)$", r'20\1-04-01'),
    (r"^Q3\s*'(\d\d)$", r'20\1-07-01'),
    (r"^Q4\s*'(\d\d)$", r'20\1-10-01'),
    (r"^Q1\s*'(\d\d\d\d)$", r'\1-01-01'),
    (r"^Q2\s*'(\d\d\d\d)$", r'\1-04-01'),
    (r"^Q3\s*'(\d\d\d\d)$", r'\1-07-01'),
    (r"^Q4\s*'(\d\d\d\d)$", r'\1-10-01'),
    (r"^(\d+)'(\d\d)$", r'20\2-\1-01'),
    (r"^\$(\d+(\.\d+)?).+", r'\1'),
    (r"\$", r''),
    (r"^(\d+(\.\d+)) GT/s$", r'\1'),
    (r"^(\d+(\.\d+)?)°C$", r'\1'),
]]

meta = json.load(open('items/cpuspecs/_legend.json'))
prices = json.load(open('items/cpuspecs/cpuprices.json'))

def tryUnitsToNum(value: str):
    value = str(value)
    for re, sub in reSubs:
        value = re.sub(sub, str(value))

    try:
        num = float(value)
        if int(num) == num:
            return str(int(num))
    except:
        pass

    if len(value.split(" ")) != 2:
        return value
    num, unit = value.split(" ")
    try:
        num = float(num)
    except:
        return value
    if int(num) == num:
        num = int(num)

    units = {
        "B": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3, "TB": 1024 ** 4,
        "Hz": 1, "kHz": 10 ** 3, "MHz": 10 ** 6, "GHz": 10 ** 9, "THz": 10 ** 12,
        "nm": 1, 'W': 1,
    }
    if unit not in units:
        return value
        print(unit)
    return num * units[unit]


with open('output.csv', 'w') as out:
    header = rootProps + [meta[section][col] for section in meta for col in meta[section]]
    out.write(';'.join(header) + '\n')

    for fn in Path('items').rglob('*.json'):
        if fn.name.lower() in ['_legend.json', 'cpuprices.json']:
            continue
        with open(fn) as f:
            data = json.load(f)
            cpuid = str(data["id"])
            data["price"] = prices[cpuid] if cpuid in prices else ""
            line = [tryUnitsToNum(data[col]) if col in data else col for col in rootProps]
            for m in meta:
                datam = data[m] if m in data else {}
                for m2 in meta[m]:
                    colName = m2
                    val = tryUnitsToNum(datam[colName]) if colName in datam else ''
                    line += [str(val)]
            out.write(';'.join(line) + '\n')
