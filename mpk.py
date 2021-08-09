# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Mpk(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(4)
        if not self.magic == b"\x4D\x50\x4B\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x4D\x50\x4B\x00", self.magic, self._io, u"/seq/0")
        self.data_offset = self._io.read_u4le()
        self.amnt_of_entries = self._io.read_u4le()
        self.unused = self._io.read_bytes(52)
        self._raw_entries = [None] * (self.amnt_of_entries)
        self.entries = [None] * (self.amnt_of_entries)
        for i in range(self.amnt_of_entries):
            self._raw_entries[i] = self._io.read_bytes(256)
            _io__raw_entries = KaitaiStream(BytesIO(self._raw_entries[i]))
            self.entries[i] = Mpk.Entry(_io__raw_entries, self, self._root)


    class Entry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.folder_index = self._io.read_u4le()
            self.file_index = self._io.read_u4le()
            self.data_offset = self._io.read_u4le()
            self.unused1 = self._io.read_u4le()
            self.len = self._io.read_u4le()
            self.unused2 = self._io.read_u4le()
            self.idk3 = self._io.read_u4le()
            self.unused3 = self._io.read_u4le()
            self.file_name = (self._io.read_bytes_term(0, False, True, True)).decode(u"utf8")

        @property
        def data(self):
            if hasattr(self, '_m_data'):
                return self._m_data if hasattr(self, '_m_data') else None

            io = self._root._io
            _pos = io.pos()
            io.seek(self.data_offset)
            self._m_data = io.read_bytes(self.len)
            io.seek(_pos)
            return self._m_data if hasattr(self, '_m_data') else None



