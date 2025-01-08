#!/usr/bin/env python3
"""bmp2spr.py"""

__author__ = "Dave Maez"
__version__ = "0.1"

# Date: 2025-01-07

import os.path
import sys
import re

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def convert(filename, frames=1):
    if not os.path.exists(filename):
        eprint("Error: file not found: " + filename)
        return
    with open(filename, 'rb') as f:
        if f.read(2) != b'BM':
            eprint("Error: not a BMP file.")
            return
        f.seek(10)
        offset = int.from_bytes(f.read(4), 'little')
        hdrsize = int.from_bytes(f.read(4), 'little')
        width = int.from_bytes(f.read(4), 'little')
        height = int.from_bytes(f.read(4), 'little')
        if int.from_bytes(f.read(2),'little') != 1:
            eprint("Error.")
            return
        depth = int.from_bytes(f.read(2), 'little')
        if int.from_bytes(f.read(4),'little') != 0:
            eprint("Error: this only works on uncompressed BMPs.")
            return
        size = int.from_bytes(f.read(4), 'little')
        convert_to_2bit = False
        if (depth == 4):
            convert_to_2bit = True
            f.seek(offset)
            for i in range(size):
                cc = int.from_bytes(f.read(1),'little')
                if (cc >= 64 or cc & 15 >= 4):
                    convert_to_2bit = False
                    break
        pal = []
        if (depth <= 8):
            f.seek(0x36)
            for i in range(2 ** depth):
                cc = int.from_bytes(f.read(4),'little')
                pal.append(cc)
        ofn = re.sub(r'\.bmp$','',filename,re.I) + '.spr'
        out = open(ofn, 'wb')
        out.write(b'SPR')
        if convert_to_2bit:
            out.write(b'\x02')
        else:
            out.write(depth.to_bytes(1,'little'))
        out.write(width.to_bytes(2,'little'))
        out.write(int(height/frames).to_bytes(2,'little'))
        out.write(height.to_bytes(2,'little'))
        out.write(frames.to_bytes(1,'little'))
        for i in range(len(pal)):
            if (convert_to_2bit and i > 3):
                break
            out.write(pal[i].to_bytes(3,'little'))
        block = int(width / (8 / depth))
        if depth == 1:
            blockpad = block + (4 - (block % 4))
        else:
            blockpad = block
        size = blockpad * height
        print(str(blockpad))
        for i in range(height):
            ob = offset + size - ((i + 1) * blockpad)
            print("Seek: "+str(ob))
            f.seek(ob)
            if convert_to_2bit:
                for j in range(int(block/2)):
                    c = int.from_bytes(f.read(2),'big')
                    cc = ((c & 0x3) << 6) | (c & 0x30) | ((c & 0x300) >> 6) | ((c & 0x3000) >> 12)
                    out.write(cc.to_bytes(1,'little'))
            else:
                out.write(f.read(block))
        out.close()


convert(sys.argv[1],int(sys.argv[2]))
