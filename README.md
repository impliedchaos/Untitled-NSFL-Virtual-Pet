Untitled Not-Safe-For-Life Virtual Pet
======================================

[comment]: # (Author: Dave Maez)
[comment]: # (Creation Date: 2025-01-04)


VERY VERY WIP..

Intention is to run Gen1 on RP2040 with small touch display.

Initial testing platform is [Waveshare RP2040-Touch-LCD-1.28](https://www.waveshare.com/wiki/RP2040-Touch-LCD-1.28#Overview).  Initially chosen since it already had a case, unfortunately that case is too narrow to fit a battery, so I'm still going to have to CAD a bottom for it, which sucks, because 3D printing sucks and is a barrier to entry for many.  

There's something very wrong with me.

Attempting in Micropython first, which sucks, but I'm literally too lazy to install the RP2040 C toolchain.

Currently there are only three characters: Fitboy, Fatboy and Femboy.  More to be added.  Also this is currently not a game.  So far all that's implemented is the initial "hatching" stage where we summon our characters and randomize their palettes.  Swipe left to re-roll.

### Instalation on RP2040-Touch-LCD-1.28

- If micropython isn't installed yet, hold the boot button while plugging into your PC, and 
release once plugged in.  Now you can drag the micropython firmware onto the device.
- Open Thonny, and connect to your device.
- In Thonny, right click the `sprites` directory and select `Upload to /`.
- Next navigate to or expand the `src` directory, select all three `.py` files and again click `Upload to /`.  
- Double click the `main.py` that's now on the device, and select run.
- You're done.

### Mini FAQ:

- Q: Like, what the fuck, Dave?
- A: I wanted a perverted tamagotchi, what's wrong with that?

- Q: This is really gay.
- A: First, that's not a question.  Second, I mean, that's like just your opinion, man.

- Q: No, I mean this is homoerotic.
- A: Yeah, that's still not a question, but OK, yeah it's pretty gay.  Also, maybe you should stop using the word `gay` to describe things you don't like, cuz that's racist.

- Q: I didn't use it that way, you interpretted it that way, asshole!
- A: Are you ever gonna ask a question?

- Q: Fine.  Are you going to add vaginas?
- A: Eh, probably not.  I dunno.  I wanted this to be obscene, and jiggling pixel dicks are hilariously obscene.  But it's rather hard to make extra lewd vulvas in 64x64 pixels.  But who really knows what the future holds.

- Q: Are you actually gonna finish this?
- A: Ha!  History tells us that no, I probably won't.  But I would really like to.