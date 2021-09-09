import gf
import os
import binascii
import re
from ctypes import cdll, c_char_p, create_string_buffer


class OodleDecompressor:
    """
    Oodle decompression implementation.
    Requires Windows and the external Oodle library.
    """

    def __init__(self, library_path: str) -> None:
        """
        Initialize instance and try to load the library.
        """
        if not os.path.exists(os.getcwd() + library_path):
            print(f'Looking in {os.getcwd() + library_path}')
            raise Exception("Could not open Oodle DLL, make sure it is configured correctly.")

        try:
            self.handle = cdll.LoadLibrary(os.getcwd() + library_path)
        except OSError as e:
            raise Exception(
                "Could not load Oodle DLL, requires Windows and 64bit python to run."
            ) from e

    def decompress(self, payload: bytes, output_size) -> bytes:
        """
        Decompress the payload using the given size.
        """
        output = create_string_buffer(output_size)
        try:
            self.handle.OodleLZ_Decompress(
                c_char_p(payload), len(payload), output, output_size,
                0, 0, 0, None, None, None, None, None, None, 3)
        except OSError:
            return False
        return output.raw


class EntryA:
    def __init__(self):
        self.pk = ''
        self.path_length = 0
        self.entry_length = 0
        self.data_offset = 0
        self.data = b''
        self.out_data = b''
        self.path = ''
        self.length_to_next_pk = 0
        self.data_length_pre = 0
        self.data_length_post = 0


class EntryB:
    def __init__(self):
        self.pk = ''
        self.path_length = 0
        self.bitflags = 0
        # self.data_length_pre = 0
        # self.data_length_post = 0
        self.path = ''
        self.entrya_offset = 0



skipped = []
def unpack():
    global skipped
    paks = [x for x in os.listdir(direc) if '.pak' in x]
    for pak in paks:
        fbin = gf.get_hex_data(direc + pak)
        entriesB = []

        ret = [m.start() for m in re.finditer(b'\x50\x4B\x01\x02', fbin)]
        if not ret:
            raise Exception('no ret')
        for offset in ret:
            entry = EntryB()
            entry.pk = fbin[offset:offset+4]
            entry.bitflags = gf.get_int16(fbin, offset+4)
            entry.path_length = gf.get_int16(fbin, offset+0x1C)
            if entry.path_length == 0:
                continue  # Sometimes ends with a 0 length path for some reason
            entry.path = fbin[offset+0x2E:offset+(0x2E+entry.path_length)].decode('ansi')
            # entry.data_length_pre = gf.get_int32(fhex, offset + 0x14 * 2)
            # entry.data_length_post = gf.get_int32(fhex, offset + 0x18 * 2)
            entry.entrya_offset = gf.get_int32(fbin, offset + 0x2A)
            entriesB.append(entry)

        for entryb in entriesB:
            ot = entryb.entrya_offset
            entry = EntryA()
            entry.pk = fbin[ot:ot+4]
            entry.path_length = gf.get_int32(fbin, ot+0x1A)
            entry.path = fbin[ot+0x1E:ot+(0x1E+entry.path_length)].decode('ansi')
            if entryb.path != entry.path:
                print('ERROR PATHS DIFFER')
                continue
            else:
                print('Path match', entry.path)
            entry.data_offset = ot + (0x1E + entry.path_length)
            entry.data_length_pre = gf.get_int32(fbin, ot + 0x12)

            entry.data_length_post = gf.get_int32(fbin, ot + 0x16)
            entry.data = fbin[entry.data_offset:entry.data_offset+entry.data_length_pre]
            # Write
            path = f'{out_direc}/{"/".join(entry.path.split("/")[:-1])}'
            gf.mkdir(path)
            with open(f'{out_direc}/{entry.path}', 'wb') as f:
                decompressor = OodleDecompressor('/oo2core_8_win64.dll')
                if entryb.bitflags == 0x8:
                    entry.out_data = decompressor.decompress(entry.data, entry.data_length_post)
                elif entryb.bitflags == 0x14:   # 0xA is entryA
                    # No compression
                    entry.out_data = entry.data
                else:
                    entry.out_data = decompressor.decompress(entry.data, entry.data_length_post)
                if not entry.out_data:
                    raise Exception('DECOMP FAILED %%%%%%%%%%')
                f.write(entry.out_data)


if __name__ == '__main__':
    direc = 'New World Playtest/assets/'
    out_direc = 'unpacked_out/'
    gf.mkdir(out_direc)
    unpack()
    input('Unpack done! Press any key to quit...')
    # print(f'Total skipped: {[x[:36] for x in skipped]}')
