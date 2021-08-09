#!/usr/bin/env python3

import argparse
import os
import json

# Local imports
import constants
import mpk
import crypt
import meta


def extract(mpk_path: str, fldr: str, should_press: bool, should_crypt: bool):
    if not os.path.exists(mpk_path):
        print('MPK file \"{}\" does not exist!'.format(mpk_path))
        exit(-1)
        return

    mpk_file: mpk.Mpk = mpk.Mpk.from_file(mpk_path)

    if os.path.exists(fldr):
        print('Folder \"{}\" already exists!?\n'.format(fldr))
        pass
    else:
        os.mkdir(fldr)
        print('Created folder \"{}\"\n'.format(fldr))
        pass

    meta_fp = '{}{}{}'.format(fldr, constants.FP_SEP, meta.FILE_META)
    if not os.path.exists(meta_fp):
        print('Creating meta file...')
        meta_io = open(meta_fp, mode='xt', encoding='utf-8')
        mpk_meta = meta.MPKMeta(mpk_file.data_offset, mpk_file.amnt_of_entries, mpk_file.entries)
        json.dump(mpk_meta, fp=meta_io, ensure_ascii=False, indent=2, cls=meta.MPKMeta.JSONEncoder)
        meta_io.flush()
        meta_io.close()

        print('Done creating meta file \"{}\"!\n\n'.format(meta_fp))
        pass
    else:
        print('Meta file already exists.\nNot creating...\n\n\n')
        pass

    for mpk_entry in mpk_file.entries:
        entry_fp = '{}{}{}'.format(fldr, constants.FP_SEP, mpk_entry.file_name)
        if os.path.exists(entry_fp):
            print('Entry file \"{}\" already exists at path \"{}\"!\n'.format(mpk_entry.file_name, entry_fp))
            pass
        else:
            data: bytes = mpk_entry.data
            if crypt.is_compressed(data):
                print('Found compressed entry!')
                if should_press:
                    print('Decompressing...'.format(mpk_entry.file_name))
                    data = crypt.decompress(data)
                    print('Done decompressing!\n')
                    pass
                else:
                    print('... but decompression is disabled (--press)')
                    pass
                pass
            if crypt.is_encrypted(mpk_entry.data):
                if should_crypt:
                    print('Found encrypted entry!')
                    print('Decrypting entry...'.format(mpk_entry.file_name))
                    data = crypt.decrypt_entry(data)
                    print('Done decrypting!\n')
                    pass
                else:
                    print('... but decryption is disabled (--crypt)')
                    pass
                pass
            print('Writing entry \"{}\"...'.format(mpk_entry.file_name))
            entry_io = open(entry_fp, mode='x+b')
            entry_io.write(data)
            entry_io.flush()
            entry_io.close()
            print('Done writing entry \"{}\"!\n\n'.format(entry_fp))
            pass
        continue
    return


def create(fldr: str, mpk: str, should_press: bool, should_crypt: bool):
    if not os.path.exists(fldr):
        print('MPK folder \"{}\" does not exist!'.format(fldr))
        exit(-1)
        return

    path_meta = '{}{}{}'.format(fldr, constants.FP_SEP, meta.FILE_META)
    if not os.path.exists(path_meta):
        print('Meta file \"{}\" does not exist!'.format(path_meta))
        exit(-1)
        return

    if os.path.exists(mpk):
        print('MPK file \"{}\" already exists!'.format(mpk))
        exit(-1)
        return

    meta_io = open(path_meta, 'rt+', encoding='utf8')
    mpk_meta: meta.MPKMeta = meta.MPKMeta(**json.load(meta_io))
    meta_io.flush()
    meta_io.close()

    if mpk_meta.amount_of_entries != len(mpk_meta.entries):
        print('The entry \"{}\" in meta file is not equal to the amount of entries ({}) given!'.format(
                'amount_of_entries',
                len(mpk_meta.entries)
            )
        )
        pass
    else:
        print('Check passed: Amount of entries are equal')
        pass

    breakpoint()

    print('TODO')
    # TODO
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='input', required=True, nargs=1, type=str,
                        help='Input - e=MPK file, c=MPK folder'
                        )
    parser.add_argument('--output', dest='output', required=True, nargs=1, type=str,
                        help='Output - e=MPK folder, c=MPK file'
                        )
    parser.add_argument('--mode', dest='mode', required=True, choices=[constants.MODE_EXTRACT, constants.MODE_CREATE])
    parser.add_argument('--press', dest='should_press', required=False, action='store_true')
    parser.add_argument('--crypt', dest='should_crypt', required=False, action='store_true')
    args = parser.parse_args()

    i = args.input[0]
    o = args.output[0]
    mode = args.mode[0]

    if mode == constants.MODE_EXTRACT:
        extract(i, o, args.should_press, args.should_crypt)
        pass
    elif mode == constants.MODE_CREATE:
        create(i, o, args.should_press, args.should_crypt)
        pass

    print('Done!')
    return


if __name__ == '__main__':
    main()
    pass
