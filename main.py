from machine import Pin, SPI, I2C
from ssd1306 import SSD1306_I2C
from max7219 import Matrix8x8
import time
import asyncio

"""
rtc = machine.RTC()
rtc.datetime((2020, 1, 21, 2, 10, 32, 36, 0))
print(rtc.datetime())
"""

spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)
matrix = Matrix8x8(spi, ss, 1)

resX = 128
resY = 64
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)
display = SSD1306_I2C(resX, resY, i2c)

GLYPHS = {
    "1": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    "2": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    "3": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    "4": [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ],
}

def tweenBrightness():
  for x in range(0, 16):
    matrix.brightness(x)
    time.sleep(.3)
    print("(brightness doesn't show in wokwi) Brightness: " + str(x))
  for x in reversed(range(0,16)):
    matrix.brightness(x)
    time.sleep(.3)
    print("(brightness doesn't show in wokwi) Brightness: " + str(x))

def cycle():
  matrix.text(" ")
  matrix.show()
  tweenBrightness()
  for x in range(1, 5):
    matrix.text_from_glyph(str(x), GLYPHS)
    matrix.show()
    tweenBrightness()

TOPLine    = "TOPLine"
MIDDLELine = "MIDDLELine"
BOTTOMLine = "BOTTOMLine"
SELECTED   = 1

def updateFrame():
  display.fill(0)
  display.text(TOPLine,    4, 14, 1)
  display.text(MIDDLELine, 4, 24, 1)
  display.text(BOTTOMLine, 4, 34, 1)
  """
  if SELECTED == 1:
    
  """
  display.show()

updateFrame()