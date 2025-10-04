# Bencode.cy

A fast bencode implementation based on Cython, supporting Python 3.9+. 

It is written using Cython's pure Python syntax, so it can run directly without Cython compilation. 

Of course, performance is significantly better after compilation. 

Based on my tests, this library is currently among the faster ones available.

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
from bencode import bencode, bdecode

assert bencode("WWWWWW") == b'6:WWWWWW'
assert bencode(233) == b'i233e'

with open("debian-8.3.0-amd64-netinst.iso.torrent", "rb") as f:
    torrent = bdecode(f.read())
    print(torrent[b'announce'])
```


## Speed Benchmark

`bencode.encode` and `bencode.decode` are the Cython-compiled versions of this library. `bencode.encodepy` and `bencode.decodepy` are the Python versions. They are the same code—one compiled, one not—which is quite interesting.

`bencoder.pyx.encode` and `bencoder.pyx.decode` are the encoding/decoding functions from the [bencoder.pyx](https://github.com/whtsky/bencoder.pyx) library. However, it currently only supports up to Python 3.11 and is slightly slower, though I learned from its code.

`fastbencode.encode` and `fastbencode.decode` are from another excellent library, [fastbencode](https://github.com/dust8/bencoding), which is written in Rust.

From the comparison, this library is currently among the faster options.


| Name (time in us)               | Mean              | StdDev              | Min        | Max               | Median          | IQR             | Outliers       | OPS (Kops/s)    | Rounds  | Iterations |
|---------------------------------|-------------------|---------------------|------------|-------------------|-----------------|-----------------|----------------|-----------------|---------|------------|
| bencode.encode          | 3.6375 (1.0)      | 1.2714 (2.58)       | 3.2500 (1.0) | 124.3750 (2.25)   | 3.5000 (1.0)    | 0.2920 (3.52)   | 783;2232       | 274.9122 (1.0)  | 46967   | 1          |
| bencode.decode          | 3.7377 (1.03)     | 0.4936 (1.0)        | 3.5000 (1.08) | 57.8750 (1.05)    | 3.7080 (1.06)   | 0.1250 (1.51)   | 870;1387       | 267.5478 (0.97) | 41524   | 1          |
| bencoder.pyx.encode     | 3.8702 (1.06)     | 0.5671 (1.15)       | 3.6660 (1.13) | 101.7500 (1.84)   | 3.8330 (1.10)   | 0.0830 (1.0)    | 863;2908       | 258.3843 (0.94) | 63160   | 1          |
| bencode.encodepy       | 5.4584 (1.50)     | 1.4604 (2.96)       | 4.9580 (1.53) | 152.1250 (2.75)   | 5.2500 (1.50)   | 0.1670 (2.01)   | 1778;4048      | 183.2048 (0.67) | 39802   | 1          |
| bencoder.pyx.decode     | 7.3514 (2.02)     | 3.2231 (6.53)       | 4.9580 (1.53) | 93.4590 (1.69)    | 6.1670 (1.76)   | 2.4580 (29.61)  | 1628;1596      | 136.0280 (0.49) | 15085   | 1          |
| fastbencode.encode | 8.3929 (2.31)     | 0.6864 (1.39)       | 5.0000 (1.54) | 55.2910 (1.0)     | 8.2920 (2.37)   | 0.2930 (3.53)   | 2436;3550      | 119.1477 (0.43) | 36530   | 1          |
| fastdecode.decode  | 10.0628 (2.77)    | 1.9921 (4.04)       | 7.5000 (2.31) | 83.6670 (1.51)    | 9.4170 (2.69)   | 0.4160 (5.01)   | 2463;2791      | 99.3756 (0.36)  | 19450   | 1          |
| bencode.decodepy       | 13.9937 (3.85)    | 275.3247 (557.75)   | 9.6250 (2.96) | 45,984.8750 (831.69) | 10.2910 (2.94) | 0.6670 (8.04)   | 15;2005        | 71.4610 (0.26)  | 35346   | 1          |


Test Environment: Python 3.11.13, MacBook Air M2, macOS 26.01, October 2025