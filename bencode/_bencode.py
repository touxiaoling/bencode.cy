# cython: language_level=3str, boundscheck=False, wraparound=False
# , linetrace=True
try:
    import cython
    from cython import int as cint
except ImportError:
    print("Warning! import use fake cython!")
    from ._fake_cython import Cython

    cython = Cython()

    cint = cython.int

from typing import Union, Tuple, List, Dict


NUM_ENCODING: str = cython.declare(str, "ascii")
VAL_ENCODING: str = cython.declare(str, "utf-8")

TypeEncodable = Union[str, int, List, set, Tuple, Dict, bytes, bytearray, bool]

if not cython.compiled:
    print("Warning! bencode not compiled!")


@cython.cfunc
@cython.inline
def _bencode_set(value: set, r: "cython.list"):
    r.append(b"l")
    for k in value:
        _bencode(k, r)
    r.append(b"e")


@cython.cfunc
@cython.inline
def _bencode(value: TypeEncodable, r: "cython.list") -> bytes:
    if isinstance(value, (bytes, bytearray)):
        r.append(str(len(value)).encode(NUM_ENCODING))
        r.append(b":")
        r.append(value)

    elif isinstance(value, int):
        r.append(b"i")
        r.append(str(value).encode(NUM_ENCODING))
        r.append(b"e")

    elif isinstance(value, dict):
        r.append(b"d")
        keys: cython.list = sorted(value)
        for i in range(len(keys)):
            key: str | bytes = keys[i]
            _bencode(key, r)
            _bencode(value[key], r)
        r.append(b"e")

    elif isinstance(value, (list, tuple)):
        r.append(b"l")
        for i in range(len(value)):
            _bencode(value[i], r)
        r.append(b"e")

    elif isinstance(value, str):
        _bencode(value.encode(VAL_ENCODING), r)

    elif isinstance(value, set):
        _bencode_set(value, r)
    else:
        raise ValueError(f"Unable to encode `{type(value)}` {value}")


@cython.ccall
def bencode(value: TypeEncodable) -> bytes:
    r: cython.list[bytes] = []
    _bencode(value, r)
    return b"".join(r)


@cython.cfunc
@cython.inline
def _compress_stack(stack: "cython.list"):
    subitems: cython.list = []
    while True:
        item = stack.pop()
        if item is dict:
            stack.append(dict(zip(*[iter(reversed(subitems))] * 2)))
            break
        elif item is list:
            stack.append(list(reversed(subitems)))
            break

        subitems.append(item)


@cython.cfunc
@cython.inline
def _parse_forward(till_char: cint, sequence: bytes, pos: cint) -> Tuple[cint, cint]:
    idx: cint
    ichar: cint
    number: cint = 0

    for idx in range(pos, len(sequence)):
        ichar = sequence[idx]
        if ichar == till_char:
            break
        number = number * 10 + (ichar - 48)

    return number, idx + 1


@cython.ccall
def bdecode(encoded: bytes):
    """Decodes bencoded data introduced as bytes.

    Returns decoded structure(s).

    :param encoded:

    """

    stack: cython.list = []

    pos: cint = 0
    bytes_len: cint = len(encoded)
    char_byte: cint = 0
    number: cint = 0
    str_len: cint = 0

    while pos < bytes_len:
        char_byte = encoded[pos]

        if 47 < char_byte < 58:  # 0-9 bytes
            # 0:48 1:49 2:50 3:51 4:52 5:53 6:54 7:55 8:56 9:57 ::58
            str_len, pos = _parse_forward(58, encoded, pos)  #:
            stack.append(encoded[pos : pos + str_len])
            pos += str_len

        elif char_byte == 105:  # i Integer
            number, pos = _parse_forward(101, encoded, pos + 1)  # e
            stack.append(number)

        elif char_byte == 100:  # d Dictionary
            stack.append(dict)
            pos += 1

        elif char_byte == 108:  # l List
            stack.append(list)
            pos += 1

        elif char_byte == 101:  # End of a dictionary | list
            _compress_stack(stack)
            pos += 1

        else:
            raise ValueError(f"Unable to interpret `{chr(char_byte)}:{char_byte}` char.")

    return stack[0]
