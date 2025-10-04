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
@cython.boundscheck(False)  # 关闭边界检查
@cython.wraparound(False)  # 关闭负索引检查
@cython.exceptval(check=False)
def _compress_stack(stack: "cython.list", stack_pos: cint) -> cint:
    i: cint
    j: cint
    item: list | dict | cython.p_char | cint
    for i in range(stack_pos):
        i = stack_pos - i - 1
        item = stack[i]
        if item is dict:
            idict: dict = {}
            for j in range(i + 1, stack_pos, 2):
                idict[stack[j]] = stack[j + 1]
            stack[i] = idict
            break
        elif item is list:
            stack[i] = stack[i + 1 : stack_pos]
            break

    return i


@cython.cfunc
@cython.inline
@cython.boundscheck(False)  # 关闭边界检查
@cython.wraparound(False)  # 关闭负索引检查
@cython.exceptval(check=False)
def _parse_forward(till_char: cint, encoded: cython.p_char, pos: cint, bytes_len: cint) -> Tuple[cint, cint]:
    idx: cint = pos + 1
    number: cint = 0
    ichar: cython.char = encoded[pos]
    if ichar == 45:  # '-' 负值
        while idx < bytes_len:
            ichar = encoded[idx]
            idx += 1
            if ichar == till_char:
                break
            number = number * 10 - (ichar - 48)
    else:
        number = ichar - 48
        while idx < bytes_len:
            ichar = encoded[idx]
            idx += 1
            if ichar == till_char:
                break
            number = number * 10 + (ichar - 48)

    return number, idx


@cython.cfunc
@cython.boundscheck(False)  # 关闭边界检查
@cython.wraparound(False)  # 关闭负索引检查
@cython.exceptval(check=False)
def _bdecode(encoded: cython.p_char, bytes_len: cint):
    stack: "cython.list" = [None] * 20
    stack_len: cint = 20
    stack_pos: cint = 0
    pos: cint = 0

    ichar: cython.char = 0
    number: cint = 0
    str_len: cint = 0

    while pos < bytes_len:
        ichar = encoded[pos]

        if 47 < ichar < 58:  # 0-9 bytes
            # 0:48 1:49 2:50 3:51 4:52 5:53 6:54 7:55 8:56 9:57 ::58
            str_len, pos = _parse_forward(58, encoded, pos, bytes_len)  #:
            stack[stack_pos] = encoded[pos : pos + str_len]
            pos += str_len

        elif ichar == 105:  # i Integer
            number, pos = _parse_forward(101, encoded, pos + 1, bytes_len)  # e
            stack[stack_pos] = number

        elif ichar == 100:  # d Dictionary
            stack[stack_pos] = dict
            pos += 1

        elif ichar == 108:  # l List
            stack[stack_pos] = list
            pos += 1

        elif ichar == 101:  # End of a dictionary | list
            stack_pos = _compress_stack(stack, stack_pos)
            pos += 1

        else:
            raise ValueError(f"Unable to interpret `{chr(ichar)}`:{ichar} char.")

        stack_pos += 1
        if stack_pos >= stack_len:
            stack.extend([None] * 20)
            stack_len += 20

    return stack[0]


@cython.ccall
def bdecode(encoded: bytes):
    """Decodes bencoded data introduced as bytes.

    Returns decoded structure(s).

    :param encoded:

    """
    bytes_len: cint = len(encoded)
    return _bdecode(encoded, bytes_len)
