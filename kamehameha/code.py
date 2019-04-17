import time
import board
import audioio
import touchio
import neopixel
import digitalio

#Activamos la salida de audio
audio = audioio.AudioOut(board.A0)

speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.switch_to_output(value=True)

#Configuramos los Neopixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)
pixels.fill((0, 0, 0))
pixels.show()

#Configuramos el pin tactil A3. Para usar el botón A, comentar esta línea y descomentar las siguientes
start_pin = touchio.TouchIn(board.A3)
#start_pin = digitalio.DigitalInOut(board.BUTTON_A)
#start_pin.direction = digitalio.Direction.INPUT
#start_pin.pull = digitalio.Pull.DOWN

#Configuramos el botón para resetear el indice
reset_pin = digitalio.DigitalInOut(board.BUTTON_B)
reset_pin.direction = digitalio.Direction.INPUT
reset_pin.pull = digitalio.Pull.DOWN

#Variable índice, almacenará el número de sonido a reproducir
index = 0

#Funcion para incrementar el índice
def increment_index():
    global index
    if index < 4:
        index = index + 1
    else:
        index = 0

#Función para reproducir el sonido y la animación de luz
def play_file(filename):
    bright = (0x7f, 0xf4, 0xff)
    dim = (0x00, 0xac, 0xbc)
    even = True
    
    #Abrimos el archivo de sonido
    wave_file = open(filename, "rb")
    
    #Y lo reproducimos
    with audioio.WaveFile(wave_file) as wave:
            audio.play(wave)
            
            #Lanzamos la animación correspondiente para cada sonido
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
                
                #Si presionamos el botón pasamos al siguiente sonido
                if start_pin.value:
                    audio.stop()
                    increment_index()
                    play_file("%s.wav" % index)
                
                pass            

while True:
    #Iniciamos la reproducción
    if start_pin.value:
        play_file("%s.wav" % index)
        increment_index()
        
    #Reseteamos la reproducción
    if reset_pin.value:
        audio.stop()
        index = 0
        
    #Apagamos los neopixels una vez terminado
    if(index==4 or index in range(0,2)):
        pixels.fill((0,0,0))
        pixels.show()
