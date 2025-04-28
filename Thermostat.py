 #
# Thermostat.py
#

from time import sleep
from datetime import datetime
from statemachine import StateMachine, State
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import adafruit_sht4x
import serial
from gpiozero import Button, PWMLED
from threading import Thread
from math import floor

DEBUG = True

# Initialize I2C
i2c = board.I2C()

# Initialize Temperature and Humidity sensor (SHT41)
thSensor = adafruit_sht4x.SHT4x(i2c)

# Initialize Serial connection
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# LEDs
redLight = PWMLED(18)
blueLight = PWMLED(23)

# Managed Display Class
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

# Initialize display
screen = ManagedDisplay()

# TemperatureMachine (Thermostat)
class TemperatureMachine(StateMachine):
    off = State(initial=True)
    heat = State()
    cool = State()

    setPoint = 72

    cycle = (
        off.to(heat) |
        heat.to(cool) |
        cool.to(off)
    )

    def on_enter_heat(self):
        if DEBUG:
            print("* Changing state to heat")
        self.updateLights()

    def on_exit_heat(self):
        pass

    def on_enter_cool(self):
        if DEBUG:
            print("* Changing state to cool")
        self.updateLights()

    def on_exit_cool(self):
        pass

    def on_enter_off(self):
        if DEBUG:
            print("* Changing state to off")
        self.updateLights()

    def processTempStateButton(self):
        if DEBUG:
            print("Cycling Temperature State")
        self.send("cycle")

    def processTempIncButton(self):
        if DEBUG:
            print("Button pressed: Increasing setpoint!")
        self.setPoint += 1
        self.updateLights()

    def processTempDecButton(self):
        if DEBUG:
            print("Button pressed: Decreasing setpoint!")
        self.setPoint -= 1
        self.updateLights()

    def updateLights(self):
        temp = floor(self.getFahrenheit())
        redLight.off()
        blueLight.off()

        if DEBUG:
            print(f"State: {self.current_state.id}")
            print(f"SetPoint: {self.setPoint}")
            print(f"Temp: {temp}")

        if self.current_state.id == 'heat':
            if temp < self.setPoint:
                redLight.pulse()
            else:
                redLight.value = 1
        elif self.current_state.id == 'cool':
            if temp > self.setPoint:
                blueLight.pulse()
            else:
                blueLight.value = 1

    def run(self):
        myThread = Thread(target=self.manageMyDisplay)
        myThread.start()

    def getFahrenheit(self):
        temperature, _ = thSensor.measurements
        return (((9/5) * temperature) + 32)

    def setupSerialOutput(self):
        output = f"{self.current_state.id},{self.getFahrenheit():0.1f},{self.setPoint}"
        return output

    endDisplay = False

    def manageMyDisplay(self):
        counter = 1
        altCounter = 1
        while not self.endDisplay:
            current_time = datetime.now()
            lcd_line_1 = current_time.strftime('%b %d  %H:%M:%S\n')

            if altCounter < 6:
                lcd_line_2 = f"T:{self.getFahrenheit():0.1f}F"
                altCounter += 1
            else:
                lcd_line_2 = f"{self.current_state.id}:{self.setPoint}F"
                altCounter += 1
                if altCounter >= 11:
                    self.updateLights()
                    altCounter = 1

            screen.updateScreen(lcd_line_1 + lcd_line_2)

            if DEBUG:
                print(f"Counter: {counter}")

            if (counter % 30) == 0:
                ser.write((self.setupSerialOutput() + "\n").encode('utf-8'))
                counter = 1
            else:
                counter += 1

            sleep(1)

        screen.cleanupDisplay()

# Setup State Machine
tsm = TemperatureMachine()

# Setup Buttons
greenButton = Button(24)
greenButton.when_pressed = tsm.processTempStateButton

redButton = Button(25)
redButton.when_pressed = tsm.processTempIncButton

blueButton = Button(12)
blueButton.when_pressed = tsm.processTempDecButton

# Start Display Thread
tsm.run()

# Main Loop
repeat = True

while repeat:
    try:
        sleep(30)
    except KeyboardInterrupt:
        print("Cleaning up. Exiting...")
        
        # Show Goodbye FIRST
        screen.updateScreen(" Goodbye!\n See you later")
        sleep(2)
        
        repeat = False
        tsm.endDisplay = True
        sleep(1)
