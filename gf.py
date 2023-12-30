import os
import numpy as np


def fill_hex_with_zeros(s, desired_length):
    return ("0"*desired_length + s)[-desired_length:]


def get_hex_data(direc):
    t = open(direc, 'rb')
    r = t.read()
    t.close()
    return r


def get_flipped_hex(h, length):
    if length % 2 != 0:
        print("Flipped hex length is not even.")
        return None
    return b"".join(reversed([h[:length][i:i + 2] for i in range(0, length, 2)]))


def get_file_from_hash(hsh):
    hsh = get_flipped_hex(hsh, 8)
    first_int = int(hsh.upper(), 16)
    one = first_int - 2155872256
    first_hex = hex(int(np.floor(one/8192)))
    second_hex = hex(first_int % 8192)
    return f'{fill_hex_with_zeros(first_hex[2:], 4)}-{fill_hex_with_zeros(second_hex[2:], 4)}'.upper()


def get_hash_from_file(file):
    pkg = file.replace(".bin", "").upper()

    firsthex_int = int(pkg[:4], 16)
    secondhex_int = int(pkg[5:], 16)

    one = firsthex_int*8192
    two = hex(one + secondhex_int + 2155872256)
    return two[2:]


def mkdir(path):
    k = path.split('/')
    for i in range(len(k)):
        try:
            # print('/'.join(k[:i+1]))
            os.mkdir('/'.join(k[:i+1]))
        except:
            pass


def get_int32(hx, offset):
    return int.from_bytes(hx[offset:offset+4], byteorder='little')


def get_int16(hx, offset):
    return int.from_bytes(hx[offset:offset+2], byteorder='little')