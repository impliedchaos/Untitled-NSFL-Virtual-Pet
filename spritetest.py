# Proto testing on waveshare RP2040-LCD-0.96 rev2  No idea why colors are fucked.
from ST7735 import TFT
from sysfont import sysfont
import time
import math
from machine import SPI,Pin,time_pulse_us
from framebuf import FrameBuffer, RGB565, GS4_HMSB
from random import randint

spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi,8,12,9)
tft.initr()
tft.rgb(False)
tft.invertcolor(True)
tft.fill(TFT.RED)

print("OK")
#time.sleep(1)

sbuf = bytearray(2*80*160)
screen = FrameBuffer(sbuf,160,80,RGB565)
charpalbuf=bytearray(32)
charpal = FrameBuffer(charpalbuf,16,1,RGB565)
charsprbuf = bytearray(16384)
charspr = [
    FrameBuffer(charsprbuf,      64, 64, GS4_HMSB),
    FrameBuffer(memoryview(charsprbuf)[2048:4095],   64, 64, GS4_HMSB),
    FrameBuffer(memoryview(charsprbuf)[4096:6143],   64, 64, GS4_HMSB),
    FrameBuffer(memoryview(charsprbuf)[6144:8191],   64, 64, GS4_HMSB),
    FrameBuffer(memoryview(charsprbuf)[8192:10239],  64, 64, GS4_HMSB),
    FrameBuffer(memoryview(charsprbuf)[10240:12287], 64, 64, GS4_HMSB),
    FrameBuffer(memoryview(charsprbuf)[12288:14335], 64, 64, GS4_HMSB),
    FrameBuffer(memoryview(charsprbuf)[14336:16383], 64, 64, GS4_HMSB)
]

print("OK")

def TFTColor( aR, aG, aB ) :
  return ((aB & 0xF8) << 8) | ((aG & 0xFC) << 3) | (aR >> 3)

TRANSP = TFTColor(255,0,255)

def GeneratePalette() :
    charpal.pixel( 0, 0, TFTColor(  0,   0,   0)) # Black
    charpal.pixel( 1, 0, TFTColor(255, 255, 255)) # White
    dickskin = [
        [ [239, 175, 159], [232, 142, 120], [209,  96,  35] ],
        [ [216, 182, 204], [200, 152, 175], [188, 113, 137] ],
    ]
    skin = [
        [ [243, 221, 206], [233, 192, 165], [210, 126,  70], [168,  94,  41] ],
        [ [243, 214, 150], [226, 179,  85], [179, 130,  30], [179,  89,  25] ],
        [ [240, 186, 127], [226, 156,  85], [179, 105,  30], [156,  78,  22] ],
        [ [196, 196, 196], [156, 156, 156], [105, 105, 105], [ 89,  89,  89], [210, 192, 188], [192, 166, 160], [147, 115,  98] ],
        [ [198, 130,  57], [174, 102,  30], [131,  77,  22], [ 89,  45,  13], [158,  83,  46], [131,  58,  22], [ 87,  39,  15] ],
    ]
    sk = skin[randint(0,len(skin) - 1)]
    charpal.pixel( 2, 0, TFTColor(sk[0][0],sk[0][1],sk[0][2]))
    charpal.pixel( 3, 0, TFTColor(sk[1][0],sk[1][1],sk[1][2]))
    charpal.pixel( 4, 0, TFTColor(sk[2][0],sk[2][1],sk[2][2]))
    charpal.pixel( 5, 0, TFTColor(sk[3][0],sk[3][1],sk[3][2]))
    if (len(sk) == 7):
        charpal.pixel( 9, 0, TFTColor(sk[4][0],sk[4][1],sk[4][2]))
        charpal.pixel(10, 0, TFTColor(sk[5][0],sk[5][1],sk[5][2]))
        charpal.pixel(11, 0, TFTColor(sk[6][0],sk[6][1],sk[6][2]))
    else:
        ds = dickskin[randint(0,len(dickskin) - 1)]
        print(ds)
        charpal.pixel( 9, 0, TFTColor(ds[0][0],ds[0][1],ds[0][2]))
        charpal.pixel(10, 0, TFTColor(ds[1][0],ds[1][1],ds[1][2]))
        charpal.pixel(11, 0, TFTColor(ds[2][0],ds[2][1],ds[2][2]))
    charpal.pixel( 6, 0, TFTColor(128,0,255))
    charpal.pixel( 7, 0, TFTColor(96,0,224))
    charpal.pixel( 8, 0, TFTColor(64,0,128))
    charpal.pixel(13, 0, TFT.RED)
    charpal.pixel(15, 0, TRANSP)

def Draw(frame=0) :
    screen.fill(TFTColor(32,32,32))
    screen.blit(charspr[frame], 58, 8, TRANSP, charpal)
    screen.blit(charpal, 0,0)
    screen.blit(charpal, 0,1)
    screen.blit(charpal, 0,2)
    screen.blit(charpal, 0,3)
    screen.blit(charpal, 0,4)
    screen.blit(charpal, 0,5)
    screen.blit(charpal, 0,6)
    screen.blit(charpal, 0,7)
    tft._writedata(sbuf)

def go() :
    GeneratePalette()
    Draw()
    
print("OK")

f=open('masc1-idle1-flacid.bmp', 'rb')
f.read(10)
offset = int.from_bytes(f.read(4), 'little')
f.seek(offset)
f.readinto(memoryview(charsprbuf),8192)
f.close()
#for x in range(4096):
#    charsprbuf[x] = x % 16
print(charsprbuf[0:2047])
print(charsprbuf[2048:4091])

print("OK")

fr = 0
GeneratePalette()
while True:
    if fr >= 8:
        GeneratePalette()
        fr = 0
    Draw(fr % 4)
    fr = fr + 1
    time.sleep(0.1)
