#!/usr/bin/env python3

import zlib


def decrypt_entry(data: bytes):
    # TODO
    return data


def encrypt_entry(data: bytes):
    # TODO
    return data


def is_encrypted(data: bytes):
    # TODO
    return False


def is_compressed(data: bytes):
    return data[:0x2] == b'\x78\x9C'


def decompress(data: bytes):
    return zlib.decompress(data)


def compress(data: bytes):
    # TODO
    return zlib.compress(data, level=1)
