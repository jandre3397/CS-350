# TemperatureSensorTest.py - This is the Python code used to demonstrate
# the data that is received from the SHT41 temperature and humidity sensor board.
#
# This code works with the test circuit built for module 6 (with SHT41 substitution).
#
#------------------------------------------------------------------
# Change History
#------------------------------------------------------------------
# Version   |   Description
#------------------------------------------------------------------
#    1          Modified to work with SHT41
#------------------------------------------------------------------

##
## Import necessary to provide timing in the main loop
##
from time import sleep

##
## Imports necessary to provide connectivity to the 
## sensor and the I2C bus
##
import board
import adafruit_sht4x

##
## Create an I2C instance so that we can communicate with
## devices on the I2C bus.
##
i2c = board.I2C()

##
## Initialize our Temperature and Humidity sensor
##
thSensor = adafruit_sht4x.SHT4x(i2c)

##
## Setup the flag that will control our main loop
##
repeat = True

##
## Loop until the user issues a KeyboardInterrupt (CTRL-C)
##
while repeat:
    try:
        ##
        ## Print basic temperature and humidity information.
        ## The temperature is in Degrees Celsius, the 
        ## Relative Humidity is in %. The accuracy of measurement
        ## should be +/- .2 degrees for temperature and 
        ## +/- 1.5% for humidity (SHT41 specs).
        ##
        temperature, humidity = thSensor.measurements
        print("\nTemperature: %0.1f C" % temperature)
        print("RH: %0.1f %%" % humidity)
        sleep(5)
    except KeyboardInterrupt:
        ## Catch the keyboard interrupt and exit gracefully
        print("Exiting...")
        repeat = False
