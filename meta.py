#!/usr/bin/env python3
from array import array

import crypt
import json
from typing import Any, Callable

import mpk

FILE_META = 'mpk.meta.json'


class MPKMetaEntry:

    def __init__(self,
                 folder_index: int,
                 file_index: int,
                 data_offset: int,
                 entry_len,
                 entry_len_uncompressed: int,
                 file_name: str,
                 is_compressed: bool
                 ):
        self.folder_index = folder_index
        self.file_index = file_index
        self.data_offset = data_offset
        self.len = entry_len
        self.len_uncompressed = entry_len_uncompressed
        self.file_name = file_name
        self.is_compressed = is_compressed
        return

    class JSONDecoder(json.JSONDecoder):

        def decode(self, s: str, _w: Callable[..., Any] = ...) -> Any:
            breakpoint()
            super().decode(s)
            breakpoint()
            return


class MPKMeta:

    def __init__(self, data_offset: int, amount_of_entries: int, entries):
        self.data_offset = data_offset
        self.amount_of_entries = amount_of_entries
        self.entries = []
        for entry in entries:
            if isinstance(entry, mpk.Mpk.Entry):
                self.entries.append(
                    MPKMetaEntry(
                        entry.folder_index,
                        entry.file_index,
                        entry.data_offset,
                        entry.len,
                        entry.idk3,
                        entry.file_name,
                        crypt.is_compressed(entry.data)
                    )
                )
                pass
            elif isinstance(entry, dict):
                # TODO
                breakpoint()
                pass
            else:
                breakpoint()
                pass
            continue
        return

    class JSONEncoder(json.JSONEncoder):

        def default(self, o: Any) -> Any:
            if isinstance(o, MPKMeta):
                return o.__dict__
            elif isinstance(o, MPKMetaEntry):
                return o.__dict__
            print('Something bad happened!')
            print('Could not serialize unknown object! \"{}\"'.format(o))
            return

    class JSONDecoder(json.JSONDecoder):

        def decode(self, s: str, _w: Callable[..., Any] = ...) -> Any:
            breakpoint()
            super().decode(s)
            breakpoint()
            return
