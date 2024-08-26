from typing import Tuple


def split_uint16_into_2_uint8(number: int) -> Tuple[int, int]:
    # Splits an uint16 defined as int into 2 uint8 
    return (number >> 8 & 0xff, number & 0xff) if number >= 256 else (0, number)


def byte_length(bit_len: int) -> int:
    # Return the byte length associated to a bit length
    return bit_len // 8 if bit_len % 8 == 0 else 1 + bit_len // 8