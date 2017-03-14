#!/usr/bin/env python

import RPi.GPIO as GPIO

gpio_pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(gpio_pin, GPIO.FALLING)
print "Button Pressed!"
