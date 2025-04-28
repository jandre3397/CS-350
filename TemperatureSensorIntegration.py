#
# TemperatureSensorIntegration.py - Final version
# Works with Adafruit SHT41 sensor, button toggle, LCD, and live terminal output
#

#------------------------------------------------------------------
# Change History
#------------------------------------------------------------------
# Version   |   Description
#------------------------------------------------------------------
#    1          Updated for SHT41 sensor and added terminal live output
#------------------------------------------------------------------

##
## Imports required
##
from gpiozero import Button, LED
from statemachine import StateMachine, State
from time import sleep
from datetime import datetime
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import adafruit_sht4x
from threading import Thread

##
## Debug flag
##
DEBUG = True

##
## ManagedDisplay Class
##
class ManagedDisplay():
    def __init__(self):
        self.lcd_rs = digitalio.DigitalInOut(board.D17)
        self.lcd_en = digitalio.DigitalInOut(board.D27)
        self.lcd_d4 = digitalio.DigitalInOut(board.D5)
        self.lcd_d5 = digitalio.DigitalInOut(board.D6)
        self.lcd_d6 = digitalio.DigitalInOut(board.D13)
        self.lcd_d7 = digitalio.DigitalInOut(board.D26)

        self.lcd_columns = 16
        self.lcd_rows = 2

        self.lcd = characterlcd.Character_LCD_Mono(
            self.lcd_rs, self.lcd_en,
            self.lcd_d4, self.lcd_d5,
            self.lcd_d6, self.lcd_d7,
            self.lcd_columns, self.lcd_rows
        )
        self.lcd.clear()

    def cleanupDisplay(self):
        self.lcd.clear()
        self.lcd_rs.deinit()
        self.lcd_en.deinit()
        self.lcd_d4.deinit()
        self.lcd_d5.deinit()
        self.lcd_d6.deinit()
        self.lcd_d7.deinit()

    def clear(self):
        self.lcd.clear()

    def updateScreen(self, message):
        self.lcd.clear()
        self.lcd.message = message

##
## TempMachine Class
##
class TempMachine(StateMachine):
    "State machine for managing temperature display"

    redLight = LED(18)
    blueLight = LED(23)

    scale1 = 'F'
    scale2 = 'C'

    Celsius = State(initial=True)
    Fahrenheit = State()

    screen = ManagedDisplay()

    i2c = board.I2C()
    thSensor = adafruit_sht4x.SHT4x(i2c)

    def on_enter_Celsius(self):
        self.activeScale = self.scale2
        if DEBUG:
            print("* Changing state to Celsius")

    def on_enter_Fahrenheit(self):
        self.activeScale = self.scale1
        if DEBUG:
            print("* Changing state to Fahrenheit")

    def processButton(self):
        print('*** processButton')
        self.send("cycle")

    cycle = (
        Celsius.to(Fahrenheit) | Fahrenheit.to(Celsius)
    )

    def run(self):
        myThread = Thread(target=self.displayTemp)
        myThread.start()

    def getCelsius(self):
        temperature, _ = self.thSensor.measurements
        return temperature

    def getFahrenheit(self):
        temperature, _ = self.thSensor.measurements
        return (((9/5) * temperature) + 32)

    def getRH(self):
        _, humidity = self.thSensor.measurements
        return humidity

    endDisplay = False

    def displayTemp(self):
        while not self.endDisplay:
            line1 = datetime.now().strftime('%b %d  %H:%M:%S\n')

            if self.activeScale == 'C':
                temp = self.getCelsius()
                humidity = self.getRH()
                line2 = f"T:{temp:0.1f}C H:{humidity:0.1f}%"
            else:
                temp = self.getFahrenheit()
                humidity = self.getRH()
                line2 = f"T:{temp:0.1f}F H:{humidity:0.1f}%"

            # Print live to terminal
            print(line1.strip())
            print(line2.strip())
            print("--------------------")

            self.screen.updateScreen(line1 + line2)
            sleep(1)

        self.screen.cleanupDisplay()

##
## Main program entry point
##
if __name__ == "__main__":
    machine = TempMachine()
    machine.run()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Exiting program...")
        machine.endDisplay = True
