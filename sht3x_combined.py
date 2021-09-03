#Temperature and Humidity Sensor, displayed to 2x6 LCD Display

#Raspberry Pi Pico Pins as follows:

#Pin 3 - Ground to GND on HD44780 Compatible LCD Display
#Pin 4 - GP2 - I2C(1) SDA to HD44780 Compatible LCD Display
#Pin 5 - GP3 - I2C(1) SCL to HD44780 Compatible LCD Display
#Pin 6 - GP4 - I2C(0) SDA to SHT3x Temp and Hum Monitor
#Pin 7 - GP5 - I2C(0) SCL to SHT3x Temp and Hum Monitor
#Pin 36 - 3V3(Out) - 3.3v to VIN for SHT3x Temp and Hum Monitor
#Pin 38 - Ground to GND for SHT3x Temp and Hum Monitor
#Pin 40 - VBUS - 5v to VCC on HD44780 Compatible LCD Display

import sys
import utime
from machine import Pin
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

def initial_display():
    lcd.backlight_on()
    lcd.clear()
    lcd.putstr("Version 1.0")
    lcd.move_to(0,1)
    lcd.putstr("Starting...")
    utime.sleep(1)
    lcd.clear()
    
def set_dispay():
    lcd.clear()
    lcd.putstr("Temperature")
    lcd.move_to(0,1)
    lcd.putstr("Humidity %")
 
def update_display():
    lcd.move_to(12,0)
    lcd.putstr(str(temp)[0:4])
    lcd.move_to(12,1)
    lcd.putstr(str(humd)[0:4])

def read_temp_humd():
    status = sht3x_i2c.writeto(sht3x_addr,b'\x24\x00')
    utime.sleep(1)
    # read 6 bytes
    databytes = sht3x_i2c.readfrom(sht3x_addr, 6)
    dataset = [databytes[0],databytes[1]]
    dataset = [databytes[3],databytes[4]]
    temperature_raw = databytes[0] << 8 | databytes[1]
    temperature = (175.0 * float(temperature_raw) / 65535.0) - 45
    humidity_raw = databytes[3] << 8  | databytes[4]
    humidity = (100.0 * float(humidity_raw) / 65535.0)
    sensor_data = [temperature, humidity]
    return sensor_data

#Define temperature and humidity sensor I2C settings
sht3x_i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000) 
sht3x_addrs = sht3x_i2c.scan()
sht3x_addr = sht3x_addrs.pop()
print("SHT3x Temperature and Humidity Sensor I2C Address:", sht3x_addr)

#Define LCD display I2C settings
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
lcd_i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
lcd_addrs = lcd_i2c.scan()
lcd_addr = lcd_addrs.pop()
print("LCD Display I2C Address:", lcd_addr)
lcd = I2cLcd(lcd_i2c, lcd_addr, I2C_NUM_ROWS, I2C_NUM_COLS) 

initial_display()
set_dispay()

while True:
    measure_data = read_temp_humd()
    temp = measure_data[0]
    humd = measure_data[1]
    print("Temp:", temp, "Humd:", humd)
    update_display()
    
