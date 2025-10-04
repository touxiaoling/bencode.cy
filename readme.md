# Bencode.cy

A fast bencode implementation based on Cython that supports Python 3, written using Cython's pure Python syntax.

[![PyPI License](https://img.shields.io/pypi/l/bencode.cy.svg)](https://pypi.org/project/bencode.cy/)


## Installation

```bash
pip install bencode.cy
```

## Usage Examples

```python
from bencoder import bencode, bdecode

assert bencode("WWWWWW") == b'6:WWWWWW'
assert bencode(233) == b'i233e'

with open("debian-8.3.0-amd64-netinst.iso.torrent", "rb") as f:
    torrent = bdecode(f.read())
    print(torrent[b'announce'])
```


## Speed Benchmark

| Name (time in us)<br>(Kops/s)         | Rounds  | Iterations | Min                 | Max                  | Mean                | StdDev               | Median              | IQR                  | Outliers     |
|---------------------------------------|---------|------------|---------------------|----------------------|---------------------|----------------------|---------------------|---------------------|--------------|
| test_bencode_benchmark<br><span style="color: green;">295.5083 (1.0)</span>       | 64000   | 1          | <span style="color: green;">3.1660 (1.0)</span> | 96.9160 (2.11)       | <span style="color: green;">3.3840 (1.0)</span> | 0.4740 (1.48)        | <span style="color: green;">3.3750 (1.0)</span> | <span style="color: green;">0.0420 (1.0)</span> | 718;9493     |
| test_bdecode_benchmark<br><span style="color: red;">270.3499 (0.91)</span>        | 51393   | 1          | 3.4160 (1.08)       | <span style="color: green;">45.8750 (1.0)</span> | 3.6989 (1.09)       | <span style="color: green;">0.3211 (1.0)</span> | 3.6670 (1.09)       | <span style="color: green;">0.0840 (2.00)</span> | 675;1780     |
| test_bencode_pyx_benchmark<br><span style="color: red;">217.9582 (0.74)</span>    | 64692   | 1          | 3.6660 (1.16)       | <span style="color: red;">1,718.6250 (37.46)</span> | 4.5880 (1.36)       | <span style="color: red;">16.2727 (50.67)</span> | 3.8750 (1.15)       | 0.0830 (1.98)       | 191;7556     |
| test_bdecoder_pyx_benchmark<br><span style="color: red;">194.6135 (0.66)</span>   | 66481   | 1          | <span style="color: red;">4.7910 (1.51)</span> | 64.1660 (1.40)       | <span style="color: red;">5.1384 (1.52)</span> | 0.4587 (1.43)        | <span style="color: red;">5.1250 (1.52)</span> | <span style="color: red;">0.1240 (2.95)</span> | 970;1778     |

Test Environment: Python 3.11.13, MacBook Air M2, macOS 26.01, October 2025



## Changelog

### Version 1.0.0
- Initialization of the project