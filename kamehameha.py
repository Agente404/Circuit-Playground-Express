import time
import board
import audioio
import neopixel
import digitalio

audio = audioio.AudioOut(board.A0)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)
pixels.fill((0, 0, 0))
pixels.show()

speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.switch_to_output(value=True)

buttonA = digitalio.DigitalInOut(board.BUTTON_A)
buttonA.direction = digitalio.Direction.INPUT
buttonA.pull = digitalio.Pull.DOWN
buttonB = digitalio.DigitalInOut(board.BUTTON_B)
buttonB.direction = digitalio.Direction.INPUT
buttonB.pull = digitalio.Pull.DOWN

index = 0

def increment_index():
    global index
    if index < 4:
        index = index + 1
    else:
        index = 0

def play_file(filename):
    bright = (0x7f, 0xf4, 0xff)
    dim = (0x00, 0xac, 0xbc)
    even = True
    wave_file = open(filename, "rb")
    
    with audioio.WaveFile(wave_file) as wave:
            audio.play(wave)
            while audio.playing:              
                if(index == 3):
                    pixels.fill(dim)
                    for i in range(len(pixels)):
                        if(i%2 == 0 and even == True):
                            pixels[i]=bright
                        if(i%2 != 0 and even == False):
                            pixels[i]=bright
                
                if(index == 4):
                    if(even == True):
                        pixels.fill(bright)
                    else:
                        pixels.fill(dim)
                    
                even = not even
                
                pixels.show()
                time.sleep(0.25)
                
                if buttonA.value:
                    audio.stop()
                    increment_index()
                    play_file("%s.wav" % index)
                pass            

while True:
    if buttonA.value:
        play_file("%s.wav" % index)
        increment_index()
    if buttonB.value:
        audio.stop()        
        index = 0
    if(index==4 or index in range(0,2)):
        pixels.fill((0,0,0))
        pixels.show()
