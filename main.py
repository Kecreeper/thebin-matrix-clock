from machine import Pin, SPI, I2C, RTC
from ssd1306 import SSD1306_I2C
from max7219 import Matrix8x8
from rotary_irq_rp2 import RotaryIRQ
from ds1307 import DS1307
from time import gmtime, time

i2c_rtc = I2C(1, scl=Pin(27), sda=Pin(26), freq=800000)
ds1307 = DS1307(addr=0x68, i2c=i2c_rtc)

button = Pin(15, Pin.IN, Pin.PULL_UP)

resX = 128
resY = 64
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)
display = SSD1306_I2C(resX, resY, i2c)

r = RotaryIRQ(pin_num_clk=12, 
              pin_num_dt=13, 
              min_val=0, 
              max_val=5, 
              reverse=False, 
              range_mode=RotaryIRQ.RANGE_WRAP)
     
val_old = r.value()

spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)
matrix = Matrix8x8(spi, ss, 1)

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
    "5": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    "6": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    "7": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    "8": [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ],
}

def tweenBrightness():
  for x in range(0, 16):
    matrix.brightness(x)
    matrix.show()
    time.sleep(.3)
    print("(brightness doesn't show in wokwi) Brightness: " + str(x))
  for x in reversed(range(0,16)):
    matrix.brightness(x)
    matrix.show()
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


"""
TOPLine    = "Hours:   " + str(HOURS)
MIDDLELine = "Minutes: " + str(MINUTES)
"""
HOURS = 0
MINUTES = 0
BOTTOMLine = "Start Timer"
SELECTED = 1
SELECTING  = True

def startTimer():
    SELECTING = False
    cycle()

def updateFrame():
  display.fill(0)
  display.text("Hours:   " + str(HOURS),    4, 14, 1)
  display.text("Minutes: " + str(MINUTES), 4, 24, 1)
  display.text(BOTTOMLine, 4, 34, 1)
  
  if SELECTED == 1:
    display.hline(32, 22, 64, 1)
  elif SELECTED == 2:
    display.hline(32, 32, 64, 1)
  elif SELECTED == 3:
    display.hline(32, 42, 64, 1)
    
  display.show()
updateFrame()

def rotary():
    global HOURS
    global MINUTES
    if SELECTED == 1:
        HOURS = r.value()
    elif SELECTED == 2:
        MINUTES = r.value()
    elif SELECTED == 3:
        startTimer()
    updateFrame()

r.add_listener(rotary)
r.set(value=HOURS, min_val=0, max_val=23)
def loop():
    while SELECTING == True:
        first = button.value()
        time.sleep(0.01)
        second = button.value()
        if button.value() == 0 and (first and not second):
            global SELECTED
            if SELECTED == 3:
                SELECTED = 1
            else:
                SELECTED += 1
            
            if SELECTED == 1:
                r.set(value=HOURS, min_val=0, max_val=23)
            elif SELECTED == 2:
                r.set(value=MINUTES, min_val=0, max_val=59)
            elif SELECTED == 3:
                print("a")

            print(SELECTED)
            updateFrame()
