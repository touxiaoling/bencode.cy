try:
    from ._bencodec import bencode, bdecode, TypeEncodable
except ImportError:
    from ._bencode import bencode, _bencode, TypeEncodable
