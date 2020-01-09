import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BOARD)

#LED
GPIO.setup(12, GPIO.OUT)

#Contact testers
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#turn on LED
GPIO.output(12, GPIO.HIGH)


time.sleep(10)
GPIO.output(13, GPIO.HIGH)

#Check for contact
while(GPIO.input(15) == GPIO.LOW):
    i=1

#turn off LED, and clean up
GPIO.output(12, GPIO.LOW)
GPIO.cleanup()
