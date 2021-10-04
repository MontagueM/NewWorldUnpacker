The unpacker.exe requires the following file structure:

- New World Alpha/assets (which has all the .pak files in)
- oo2core_8_win64.dll

The unpack takes about 70GB of space, so ensure to have that much free.

# Dependencies

* Python3
 * numpy

# Setup

Install Python 3 from [here](https://www.python.org/downloads/).

Run `python3 -m pip install numpy`

# Usage

Extract this repository into your game directory, usually `C:\Program Files (x86)\Steam\steamapps\common\New World {Playtest/Alpha/Closed Beta}`.

Edit `unpacker.py` at line #130 from:

```py
if __name__ == '__main__':
    direc = 'New World Alpha/assets/'
    out_direc = 'unpacked_out/'
    gf.mkdir(out_direc)
    unpack()
    input('Unpack done! Press any key to quit...')
```

To:

```py
if __name__ == '__main__':
    direc = '../assets/'
    out_direc = 'unpacked_out/'
    gf.mkdir(out_direc)
    unpack()
    input('Unpack done! Press any key to quit...')
```

Then simply run `python3 unpacker.py`
