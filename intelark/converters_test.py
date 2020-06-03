from converters import sizeToBytes, speedToHz

if __name__ == '__main__':
    wanted = 3460000000
    got = speedToHz("3.46 GHz")
    if got != wanted:
        raise ValueError(f"wanted {wanted} got {got}")

    wanted = 3460000
    got = speedToHz("3.46 MHz")
    if got != wanted:
        raise ValueError(f"wanted {wanted} got {got}")

    wanted = 824633720832
    got = sizeToBytes("768 GB")
    if got != wanted:
        raise ValueError(f"wanted {wanted} got {got}")
