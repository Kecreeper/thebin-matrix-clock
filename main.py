from machine import Pin, SPI, I2C, RTC
from ssd1306 import SSD1306_I2C
from max7219 import Matrix8x8
from rotary_irq_rp2 import RotaryIRQ
from time import gmtime
import time
import math

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
    "a": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
}

TIMER_ON = False
FINAL_UNIX = 0
FINAL = False
STOP_UNIX = 0
STOP = True

HOURS = 0
MINUTES = 0
SELECTED = 1
SELECTING  = True

def timerFrame():
    unixTill = STOP_UNIX - time.time()
    hoursTill = math.floor(unixTill/3600)
    minutesTill = math.floor((unixTill-(hoursTill*3600))/60)
    secondsTill = unixTill-(hoursTill*3600)-(minutesTill*60)
    
    display.fill(0)
    display.text(str(hoursTill)  ,30 , 29, 1)
    display.text(str(minutesTill),60, 29, 1)
    display.text(str(secondsTill),90, 29, 1)
    display.show()

def tweenBrightness():
    for x in range(0, 16):
        timerFrame()
        matrix.brightness(x)
        matrix.show()
        time.sleep(.1)
        print("(brightness doesn't show in wokwi) Brightness: " + str(x))
    for x in reversed(range(0,16)):
        timerFrame()
        matrix.brightness(x)
        matrix.show()
        time.sleep(.1)
        print("(brightness doesn't show in wokwi) Brightness: " + str(x))

def cycle():
    global FINAL
    while FINAL == False:
        matrix.text_from_glyph("a", GLYPHS)
        matrix.show()
        tweenBrightness()
        for x in range(1, 5):
            print(time.time())
            print(FINAL_UNIX)
            matrix.text_from_glyph(str(x), GLYPHS)
            matrix.show()
            tweenBrightness()
        if FINAL_UNIX-15 <= time.time() >= FINAL_UNIX+16:
            FINAL = True
    finalCycle()

def finalCycle():
    matrix.text_from_glyph("a", GLYPHS)
    matrix.show()
    tweenBrightness()
    for x in range(5, 9):
        matrix.text_from_glyph(str(x), GLYPHS)
        matrix.show()
        tweenBrightness()
    while STOP == False:
        tweenBrightness()

def startTimer():
    global SELECTING
    global TIMER_ON
    global STOP
    STOP = False
    TIMER_ON = True
    SELECTING = False

    timerSeconds = HOURS*3600 + MINUTES*60

    global FINAL_UNIX
    global STOP_UNIX
    STOP_UNIX = time.time() + timerSeconds
    FINAL_UNIX = STOP_UNIX - 15
    cycle()



def updateFrame():
    display.fill(0)
    display.text("Hours:   " + str(HOURS),    4, 14, 1)
    display.text("Minutes: " + str(MINUTES), 4, 24, 1)
    display.text("Start Timer", 4, 34, 1)
    
    if SELECTED == 1:
        display.hline(32, 22, 64, 1)
    elif SELECTED == 2:
        display.hline(32, 32, 64, 1)
    elif SELECTED == 3:
        display.hline(32, 42, 64, 1)
    display.show()
updateFrame()

def rotary():
    global STOP
    global TIMER_ON
    global SELECTING
    global HOURS
    global MINUTES
    if TIMER_ON == False:
        if SELECTED == 1:
            HOURS = r.value()
        elif SELECTED == 2:
            MINUTES = r.value()
        elif SELECTED == 3:
            if HOURS == 0 and MINUTES == 0:
                print("a")
            else:
                startTimer()
    elif TIMER_ON == True:
        if STOP == False:
            STOP = True
            TIMER_ON = False
            SELECTING = True
            loop()


    updateFrame()

r.add_listener(rotary)
r.set(value=HOURS, min_val=0, max_val=23)
def loop():
    while SELECTING == True:
        first = button.value()
        time.sleep(0.01)
        second = button.value()
        if button.value() == 0 and (first and not second):
            global STOP
            global FINAL
            """
            if FINAL == True:
                STOP = True
                FINAL = False
            """
            global SELECTED
            if SELECTED == 3:
                SELECTED = 1
            else:
                SELECTED += 1
            
            if SELECTED == 1:
                r.set(value=HOURS, min_val=0, max_val=23)
            elif SELECTED == 2:
                r.set(value=MINUTES, min_val=0, max_val=59)
            
            updateFrame()

loop()