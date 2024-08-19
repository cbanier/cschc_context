from typing import Tuple


def int_to_2_bytes(number: int) -> Tuple[int, int]:
    return (number >> 8 & 0xff, number & 0xff) if number >= 256 else (0, number)


def byte_length(x: int) -> int:
    return x // 8 if x % 8 == 0 else 1 + x // 8