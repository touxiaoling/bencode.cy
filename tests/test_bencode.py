import pytest
import sys
from pathlib import Path

from bencode import bencode, bdecode


@pytest.fixture
def tor():
    f = Path("tests/debian-mac-13.1.0-amd64-netinst.iso.torrent")
    return f.read_bytes()


def test_bencode():
    assert bencode("WWWWWW") == b"6:WWWWWW"
    assert bencode(233) == b"i233e"


def test_bdecode():
    assert bdecode(b"6:WWWWWW") == b"WWWWWW"
    assert bdecode(b"i233e") == 233


def test_torrent(tor):
    torrent = bdecode(tor)
    assert torrent[b"announce"] == b"http://bttracker.debian.org:6969/announce"
    assert tor == bencode(torrent)


def test_bdecode_benchmark(benchmark, tor):
    benchmark(bdecode, tor)


def test_bencode_benchmark(benchmark, tor):
    e2 = bdecode(tor)
    benchmark(bencode, e2)


@pytest.mark.skipif(sys.version_info >= (3, 12), reason="anything")
def test_bdecoder_pyx_benchmark(benchmark, tor):
    from bencoder import bdecode, bencode

    benchmark(bdecode, tor)


@pytest.mark.skipif(sys.version_info >= (3, 12), reason="anything")
def test_bencode_pyx_benchmark(benchmark, tor):
    from bencoder import bdecode, bencode

    e2 = bdecode(tor)
    benchmark(bencode, e2)
