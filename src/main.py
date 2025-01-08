import gc
def vmem():
    print("Mem Used / Free: "+str(gc.mem_alloc())+' / '+str(gc.mem_free()))
vmem()    
from RP2040_LCD_1_28 import Touch_CST816T, LCD_1inch28
vmem()
from spritle import Spritle, RGB, HSV
vmem()
import framebuf
import time
from random import randint, random
vmem()

# Create our LCD and Touch screen instances.
LCD = LCD_1inch28()
LCD.set_bl_pwm(65535)
vmem()

Touch=Touch_CST816T(mode=0,LCD=LCD)
vmem()

#hbuf = bytearray(120*120*2)
hbuf = memoryview(LCD.buffer)
hscr = framebuf.FrameBuffer(hbuf,120,120,framebuf.RGB565)
vmem()

char = Spritle(16384,'sprites/fem1-idle1-erect.spr')
vmem()


transp = 8184

@micropython.viper
def halfblit():
    #ibuf = ptr16(hbuf)
    obuf = ptr16(LCD.buffer)
    for y in range(120):
        for x in range(120):
            c = obuf[(119-y)*120+(119-x)]
            obuf[(119-y)*480+(119-x)*2] = c
            obuf[(119-y)*480+(119-x)*2+1] = c
            obuf[(119-y)*480+(119-x)*2+240] = c
            obuf[(119-y)*480+(119-x)*2+241] = c

def GeneratePalette() :
    char.palette.pixel( 0, 0, RGB(  0,   0,   0)) # Black
    char.palette.pixel( 1, 0, RGB(255, 255, 255)) # White
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
    char.palette.pixel( 2, 0, RGB(sk[0][0],sk[0][1],sk[0][2]))
    char.palette.pixel( 3, 0, RGB(sk[1][0],sk[1][1],sk[1][2]))
    char.palette.pixel( 4, 0, RGB(sk[2][0],sk[2][1],sk[2][2]))
    char.palette.pixel( 5, 0, RGB(sk[3][0],sk[3][1],sk[3][2]))
    if (len(sk) == 7):
        char.palette.pixel( 9, 0, RGB(sk[4][0],sk[4][1],sk[4][2]))
        char.palette.pixel(10, 0, RGB(sk[5][0],sk[5][1],sk[5][2]))
        char.palette.pixel(11, 0, RGB(sk[6][0],sk[6][1],sk[6][2]))
    else:
        ds = dickskin[randint(0,len(dickskin) - 1)]
        char.palette.pixel( 9, 0, RGB(ds[0][0],ds[0][1],ds[0][2]))
        char.palette.pixel(10, 0, RGB(ds[1][0],ds[1][1],ds[1][2]))
        char.palette.pixel(11, 0, RGB(ds[2][0],ds[2][1],ds[2][2]))
    h = random()
    s = random()/2.0 + 0.5
    char.palette.pixel( 6, 0, HSV(h,s,1.0))
    char.palette.pixel( 7, 0, HSV(h,s,0.75))
    char.palette.pixel( 8, 0, HSV(h,s,0.5))
    char.palette.pixel(15, 0, transp)
    
def reroll():
    chars = [
        'fatso-idle1-erect',
        'fatso-idle1-flacid',
        'fem1-idle1-erect',
        'fem1-idle1-flacid',
        'masc1-idle1-erect',
        'masc1-idle1-flacid',
    ]
    char.load_sprite('sprites/'+chars[randint(0,len(chars)-1)]+'.spr')
    GeneratePalette()
    vmem()
    return

pent = Spritle(686,'sprites/pentaclemono.spr')
candles = Spritle(120,'sprites/candles.spr')
cflames = Spritle(128,'sprites/candleflame.spr')

backg = Spritle(7200,'sprites/background01.spr')
backg.palette.pixel(0,0,RGB(32,0,32))
backg.palette.pixel(1,0,RGB(32,32,0))

#char.palette.pixel(9,0,LCD.red)
bg=RGB(32,0,32)

vmem()

summon = False
while True:
    if (Touch.Gestures == 5):
        Touch.Gestures = None
        if not summon:
            reroll()
            summon = True
    elif (Touch.Gestures == 4):
        # swipe right keep
        Touch.Gestures = None
        print("Accept")
    elif (Touch.Gestures == 3):
        # swipe left reroll
        Touch.Gestures = None
        print("Re-roll")
        reroll()
    elif (Touch.Gestures == 0xC):
        Touch.Gestures = None
        summon = False
        
    LCD.fill(bg)
    
    hscr.fill(bg)
    backg.blit_frameidx(hscr,0,0)

    pent.blit_frameidx(hscr, 4, 59)

    candles.blit_frameidx(hscr, 100, 84, 0)
    cflames.blit_framerand(hscr,100, 82)
    candles.blit_frameidx(hscr, 26, 91, 1)
    cflames.blit_framerand(hscr, 26, 84)
    candles.blit_frameidx(hscr, 10, 61, 2)
    cflames.blit_framerand(hscr, 10, 54)
    candles.blit_frameidx(hscr, 51, 48, 3)
    cflames.blit_framerand(hscr, 51, 41)
    candles.blit_frameidx(hscr, 95, 56, 4)
    cflames.blit_framerand(hscr, 95, 49)


    if summon:
        char.blit_framenext(hscr, 28, 18)
    halfblit()
    
    if not summon:
        LCD.write_text("Tap to Summon",70,40,1,LCD.white)
        
    LCD.show()
    time.sleep(0.1)
    #print(str(Touch.Gestures))