#!/bin/sh

python3 bmp2spr.py ../sprites_bmp/background01.bmp 1
mv ../sprites_bmp/background01.spr ../sprites/

python3 bmp2spr.py ../sprites_bmp/pentaclemono.bmp 1
mv ../sprites_bmp/pentaclemono.spr ../sprites/

python3 bmp2spr.py ../sprites_bmp/fatso-idle1-erect.bmp 4
mv ../sprites_bmp/fatso-idle1-erect.spr ../sprites/
python3 bmp2spr.py ../sprites_bmp/fatso-idle1-flacid.bmp 4
mv ../sprites_bmp/fatso-idle1-flacid.spr ../sprites/

python3 bmp2spr.py ../sprites_bmp/fem1-idle1-erect.bmp 4
mv ../sprites_bmp/fem1-idle1-erect.spr ../sprites/
python3 bmp2spr.py ../sprites_bmp/fem1-idle1-flacid.bmp 4
mv ../sprites_bmp/fem1-idle1-flacid.spr ../sprites/

python3 bmp2spr.py ../sprites_bmp/masc1-idle1-erect.bmp 4
mv ../sprites_bmp/masc1-idle1-erect.spr ../sprites/
python3 bmp2spr.py ../sprites_bmp/masc1-idle1-flacid.bmp 4
mv ../sprites_bmp/masc1-idle1-flacid.spr ../sprites/

python3 bmp2spr.py ../sprites_bmp/candles.bmp 5
mv ../sprites_bmp/candles.spr ../sprites/

python3 bmp2spr.py ../sprites_bmp/candleflame.bmp 8
mv ../sprites_bmp/candleflame.spr ../sprites/

python3 bmp2spr.py ../sprites_bmp/battery.bmp 10
mv ../sprites_bmp/battery.spr ../sprites/

python3 bmp2spr.py ../sprites_bmp/prideflag.bmp 1
mv ../sprites_bmp/prideflag.spr ../sprites/
