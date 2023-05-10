from machine import Pin, PWM, I2C
from time import sleep
from mfrc522 import MFRC522
from I2C_LCD import I2CLcd

reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)
lock = Pin(15, Pin.OUT)
buzzer = PWM(Pin(16))
buzzer.freq(500)
ledRouge = Pin(18,Pin.OUT)
ledVert = Pin(17,Pin.OUT)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000) # LCD
i2c_add = i2c.scan()[0] # LCD
lcd = I2CLcd(i2c, i2c_add, 2, 16) # LCD

def open_lock():
    lock.value(1)
    ledVert.value(1)
    buzzer.duty_u16(1500)
    sleep(4)
    lock.value(0)
    ledVert.value(0)
    buzzer.duty_u16(0)

def wrong_nfc():
    ledRouge.value(1)
    buzzer.duty_u16(1500)
    sleep(1)
    buzzer.duty_u16(0)
    sleep(2)
    ledRouge.value(0)

while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            open_lock()
            card = int.from_bytes(bytes(uid),"little",False) # type: ignore
            print("CARD ID: "+str(card))
            sleep(1)
            wrong_nfc()
