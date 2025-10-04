from pathlib import Path
import pstats
import cProfile
from bencode import bencode, bdecode


def test_bdecode(e1):
    for i in range(10000):
        assert bencode(bdecode(e1)) == e1


f = Path("tests/debian-mac-13.1.0-amd64-netinst.iso.torrent")
e1 = f.read_bytes()

cProfile.runctx("test_bdecode(e1)", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()
