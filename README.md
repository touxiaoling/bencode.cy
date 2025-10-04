# Bencode.cy

A fast bencode implementation based on Cython, supporting Python 3.9+. 

The bencode functions are 15% to 145% faster than other compiled libraries, and the decode methods are 40% to 136% faster than other compiled libraries. 

On average, they outperform pure Python versions by 150%.

Based on my tests, it is currently among the faster bencode libraries available. 

It is written using Cython's pure Python syntax, so it can run directly without Cython compilation. Of course, performance is significantly better after compilation. 


[![PyPI License](https://img.shields.io/pypi/l/bencode.cy.svg)](https://pypi.org/project/bencode.cy/)


## Installation

```bash
pip install bencode.cy
```

or, if you use uv (it might be better):

```bash
uv add bencode.cy
```


## Usage Examples

```python
from bencode import bencode, bdecode, compiled

assert True == compiled # Check if the code has been compiled with Cython

assert bencode("WWWWWW") == b'6:WWWWWW'
assert bencode(233) == b'i233e'

with open("debian-8.3.0-amd64-netinst.iso.torrent", "rb") as f:
    torrent = bdecode(f.read())
    print(torrent[b'announce'])
```

## Speed Benchmark

`bencode.encode` and `bencode.decode` are the Cython-compiled versions of this library. `bencode.encodepy` and `bencode.decodepy` are the Python versions. They are the same code—one compiled, one not—which is quite interesting.

`bencoder.pyx.encode` and `bencoder.pyx.decode` are the encoding/decoding functions from the [bencoder.pyx](https://github.com/whtsky/bencoder.pyx) library. However, it currently only supports up to Python 3.11 and is slightly slower, though I learned a lot from its code.

`fastbencode.encode` and `fastbencode.decode` are from another excellent library, [fastbencode](https://github.com/dust8/bencoding), which is written in Rust.

`better_bencode.encode` and `better_bencode.decode` are a C version of the bencoder library from [better_bencode](https://github.com/kosqx/better-bencode), but I don't know why it is so slow. Maybe Python 3.11 on macOS wasn't compiled to C.

`bencodepy.encode` and `bdecodepy.decode` are part of a pure Python version of the bencoder library from [BencodePy](https://github.com/eweast/BencodePy).

From the comparison, this library is currently among the fastest options. You can see more detailed results below.


| Name (time in us)               | Mean             | StdDev             | Min               | Max                | Median            | IQR               | Outliers   | OPS (Kops/s)       | Rounds  | Iterations |
|---------------------------------|------------------|--------------------|-------------------|--------------------|-------------------|-------------------|------------|--------------------|---------|------------|
| bencode.bencode          | 3.4163 (1.0)     | 0.4844 (2.26)      | 3.2080 (1.0)      | 102.6660 (4.70)    | 3.3750 (1.0)      | 0.0830 (1.98)     | 802;2552   | 292.7143 (1.0)     | 73850   | 1          |
| bencode.bdecode          | 3.7500 (1.10)    | 0.2139 (1.0)       | 3.5000 (1.09)     | 21.8330 (1.0)      | 3.7090 (1.10)     | 0.0420 (1.0)      | 1407;5217  | 266.6637 (0.91)    | 45627   | 1          |
| bencoder.pyx.bencode     | 3.9179 (1.15)    | 0.6638 (3.10)      | 3.5830 (1.12)     | 64.7080 (2.96)     | 3.8750 (1.15)     | 0.0840 (2.00)     | 966;4215   | 255.2408 (0.87)    | 67986   | 1          |
| bdecoder.pyx.bdecode     | 5.2444 (1.54)    | 0.7875 (3.68)      | 4.8330 (1.51)     | 58.6670 (2.69)     | 5.2080 (1.54)     | 0.0840 (2.00)     | 821;4277   | 190.6796 (0.65)    | 62830   | 1          |
| bencode.bencodepy       | 5.3323 (1.56)    | 0.8498 (3.97)      | 4.9590 (1.55)     | 100.7910 (4.62)    | 5.2910 (1.57)     | 0.1250 (2.98)     | 735;1305   | 187.5346 (0.64)    | 44860   | 1          |
| better_bencode.bencode   | 7.3494 (2.15)    | 0.6396 (2.99)      | 6.9160 (2.16)     | 46.6670 (2.14)     | 7.3330 (2.17)     | 0.1660 (3.95)     | 580;1007   | 136.0660 (0.46)    | 35399   | 1          |
| better_bdecode.bdecode   | 7.6453 (2.24)    | 0.7714 (3.61)      | 7.2080 (2.25)     | 98.6250 (4.52)     | 7.5830 (2.25)     | 0.1260 (3.00)     | 669;3513   | 130.7988 (0.45)    | 42031   | 1          |
| fastbencode.bencode | 8.3677 (2.45)    | 1.2711 (5.94)      | 4.2910 (1.34)     | 86.0000 (3.94)     | 8.3750 (2.48)     | 0.2090 (4.98)     | 3405;5445  | 119.5076 (0.41)    | 78181   | 1          |
| fastbencode.bdecode  | 9.3035 (2.72)    | 2.1248 (9.93)      | 7.5830 (2.36)     | 134.5000 (6.16)    | 9.0000 (2.67)     | 1.1670 (27.79)    | 3154;3291  | 107.4862 (0.37)    | 39473   | 1          |
| bencodepy.encode        | 9.8214 (2.87)    | 1.4897 (6.97)      | 8.9170 (2.78)     | 106.6250 (4.88)    | 9.6250 (2.85)     | 0.2910 (6.93)     | 1501;2528  | 101.8184 (0.35)    | 38772   | 1          |
| bdecode.decodepy       | 10.2167 (2.99)   | 0.8118 (3.80)      | 9.5000 (2.96)     | 82.0420 (3.76)     | 10.1670 (3.01)    | 0.2500 (5.95)     | 545;915    | 97.8788 (0.33)     | 28986   | 1          |
| bdecodepy.decode        | 13.2964 (3.89)   | 32.1082 (150.12)   | 8.4170 (2.62)     | 4,944.1660 (226.45)| 9.2920 (2.75)     | 0.3750 (8.93)     | 1562;2741  | 75.2085 (0.26)     | 43400   | 1          |

Test Environment: Python 3.11.13, MacBook Air M2, macOS 26.01, October 2025