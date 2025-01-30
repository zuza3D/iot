from config import *
import board
import neopixel

def setup_pixels():
    return neopixel.NeoPixel(board.D18, 8, brightness=1.0/32, auto_write=False)

def set_pixels(device, pixels):
    for i in range(8):
        device[i] = pixels[i]
    device.show()
