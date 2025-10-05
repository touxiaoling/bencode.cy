# Bencode.cy
[![PyPI License](https://img.shields.io/pypi/l/bencode.cy.svg)](https://pypi.org/project/bencode.cy/)
[![PyPI Version](https://img.shields.io/pypi/v/bencode.cy.svg)](https://pypi.org/project/bencode.cy/)

A fast bencode implementation based on Cython, supporting Python 3.9+. 

The bencode functions are 15% to 230% faster than other compiled libraries, and the decode methods are 40% to 320% faster than other compiled libraries. 

On average, they outperform pure Python versions by 250%.

Based on my tests, it is currently among the faster bencode libraries available. 

It is written using Cython's pure Python syntax, so it can run directly without Cython compilation. Of course, performance is significantly better after compilation. 



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

`bencode.cy.encode` and `bencode.cy.decode` are the Cython-compiled versions of this library. `bencode.cy.encodepy` and `bencode.cy.decodepy` are the Python versions. They are the same code—one compiled, one not—which is quite interesting.

`bencoder.pyx.encode` and `bencoder.pyx.decode` are the encoding/decoding functions from the [bencoder.pyx](https://github.com/whtsky/bencoder.pyx) library. However, it currently only supports up to Python 3.11 and is slightly slower, though I learned a lot from its code.

`fastbencode.encode` and `fastbencode.decode` are from another excellent library, [fastbencode](https://github.com/dust8/bencoding), which is written in Rust.

`better_bencode.encode` and `better_bencode.decode` are a C version of the bencoder library from [better_bencode](https://github.com/kosqx/better-bencode), but I don't know why it is so slow. Maybe Python 3.11 on macOS wasn't compiled to C.

`bencodepy.encode` and `bdecodepy.decode` are part of a pure Python version of the bencoder library from [BencodePy](https://github.com/eweast/BencodePy).

From the comparison, this library is currently among the fastest options. You can see more detailed results below.

### deocde benchmar result
| Name               | OPS (Kops/s)      | Mean          | StdDev        | Min           | Max             | Median        | IQR           | Outliers    | Rounds  | Iterations |
|--------------------|-------------------|---------------|---------------|---------------|-----------------|---------------|---------------|-------------|---------|------------|
| bencode.cy.decode     | 521.4145 (1.0)    | 1.9179 (1.0)  | 0.2650 (1.0)  | 1.7500 (1.0)  | 36.3330 (1.0)   | 1.8750 (1.0)  | 0.0410 (1.0)  | 2174;3385   | 40001   | 1          |
| bencode2.decode    | 490.4606 (0.94)   | 2.0389 (1.06) | 1.0887 (4.11) | 1.8750 (1.07) | 201.3750 (5.54) | 2.0000 (1.07) | 0.0420 (1.02) | 1082;12577  | 134085  | 1          |
| bencode_rs.decode  | 485.7196 (0.93)   | 2.0588 (1.07) | 0.5006 (1.89) | 1.8750 (1.07) | 64.9580 (1.79)  | 2.0410 (1.09) | 0.0420 (1.02) | 1664;16625  | 153847  | 1          |
| bencoder.pyx.decode| 191.7128 (0.37)   | 5.2161 (2.72) | 0.6630 (2.50) | 4.8750 (2.79) | 95.9590 (2.64)  | 5.1660 (2.76) | 0.0840 (2.05) | 1254;5630   | 68185   | 1          |
| bencode.cy.decodepy   | 164.2124 (0.31)   | 6.0897 (3.18) | 0.6805 (2.57) | 5.6670 (3.24) | 97.4160 (2.68)  | 6.0420 (3.22) | 0.1250 (3.05) | 829;2364    | 66116   | 1          |
| better_bencode.decode | 134.0034 (0.26) | 7.4625 (3.89) | 0.8133 (3.07) | 7.0000 (4.00) | 84.9580 (2.34)  | 7.4170 (3.96) | 0.0840 (2.05) | 499;3408    | 34238   | 1          |
| fastbencode.decode | 123.1785 (0.24)   | 8.1183 (4.23) | 1.1346 (4.28) | 5.0000 (2.86) | 107.4170 (2.96) | 8.0000 (4.27) | 0.2920 (7.12) | 1585;3315   | 63493   | 1          |
| bencodepy.decode   | 103.0055 (0.20)   | 9.7082 (5.06) | 0.7732 (2.92) | 9.1660 (5.24) | 84.0830 (2.31)  | 9.6670 (5.16) | 0.1670 (4.07) | 636;1559    | 39089   | 1          |
| bcoding.decode     | 53.2570 (0.10)    | 18.7769 (9.79)| 1.7134 (6.46) | 15.4580 (8.83)| 90.7500 (2.50)  | 18.9580 (10.11)| 0.5010 (12.21)| 1638;1730   | 11205   | 1          |

### encode benchmar result

| Name               | OPS (Kops/s)      | Mean           | StdDev          | Min            | Max               | Median         | IQR             | Outliers     | Rounds  | Iterations |
|--------------------|-------------------|----------------|-----------------|----------------|-------------------|----------------|-----------------|--------------|---------|------------|
| bencode.cy.encode     | 287.5983 (1.0)    | 3.4771 (1.0)   | 0.6224 (1.27)   | 3.2500 (1.0)   | 57.9590 (1.0)     | 3.4170 (1.0)   | 0.0430 (1.0)    | 565;8949     | 57143   | 1          |
| bencoder.pyx.encode| 256.2142 (0.89)   | 3.9030 (1.12)  | 0.4911 (1.0)    | 3.6660 (1.13)  | 93.9170 (1.62)    | 3.8750 (1.13)  | 0.0820 (1.91)   | 1054;3805    | 97163   | 1          |
| bencode.cy.encodepy   | 188.4005 (0.66)   | 5.3078 (1.53)  | 0.5279 (1.08)   | 5.0000 (1.54)  | 72.0420 (1.24)    | 5.2910 (1.55)  | 0.0830 (1.93)   | 1188;8115    | 83620   | 1          |
| bencode2.encode    | 183.6796 (0.64)   | 5.4443 (1.57)  | 2.0376 (4.15)   | 3.5840 (1.10)  | 68.7500 (1.19)    | 4.5000 (1.32)  | 2.7090 (62.98)  | 89;18        | 3999    | 1          |
| bencode_rs.encode  | 145.0679 (0.50)   | 6.8933 (1.98)  | 1.5164 (3.09)   | 4.3330 (1.33)  | 60.3750 (1.04)    | 7.4590 (2.18)  | 2.5420 (59.09)  | 3136;32      | 10601   | 1          |
| bcoding.encode     | 140.0668 (0.49)   | 7.1394 (2.05)  | 1.3146 (2.68)   | 6.6670 (2.05)  | 100.0000 (1.73)   | 7.0410 (2.06)  | 0.1660 (3.86)   | 410;1235     | 22494   | 1          |
| better_bencode.encode | 132.9986 (0.46) | 7.5189 (2.16)  | 0.6240 (1.27)   | 7.0830 (2.18)  | 69.4170 (1.20)    | 7.4590 (2.18)  | 0.1260 (2.93)   | 754;3475     | 53571   | 1          |
| fastbencode.encode | 93.0336 (0.32)    | 10.7488 (3.09) | 2.6568 (5.41)   | 8.2500 (2.54)  | 94.7080 (1.63)    | 9.2080 (2.69)  | 5.0420 (117.21) | 7655;25      | 23977   | 1          |
| bencodepy.encode   | 75.6976 (0.26)    | 13.2105 (3.80) | 29.4086 (59.88) | 8.3330 (2.56)  | 4,704.4170 (81.17)| 9.2500 (2.71)  | 0.3340 (7.76)   | 1831;3331    | 51065   | 1          |

Test Environment: Python 3.11.13, MacBook Air M2, macOS 26.01, October 2025