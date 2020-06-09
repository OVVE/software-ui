
try:
    import RPi.GPIO as GPIO
except:
    GPIO = None

import time


def pwrButtonPressed(pin):
    print("Power button pressed on pin " + str(pin))

if (not GPIO):
    print("Not running on Pi")
else:
    pwrPin = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwrPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pwrPin, GPIO.FALLING, callback=pwrButtonPressed, bouncetime = 200)

    try:
        while True:
            time.sleep(0.075)
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup() # cleanup all GPIO

