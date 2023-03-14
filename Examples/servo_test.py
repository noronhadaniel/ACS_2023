# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for a standard servo on channel 0 and a continuous rotation servo on channel 1."""
import time
import sys
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
kit.servo[1].set_pulse_width_range(500,2400)

if len(sys.argv) == 1:
    #time.sleep(1)
    #kit.servo[1].angle = 0
    # kit.continuous_servo[1].throttle = 1
    #time.sleep(1)
    #kit.continuous_servo[1].throttle = -1
    #time.sleep(1)
    #kit.servo[1].angle = 180
    # kit.continuous_servo[1].throttle = 0
    #time.sleep(1)
    #kit.servo[1].angle = 0
    pass
else:
    time.sleep(1)
    if int(sys.argv[1]) > 70 or int(sys.argv[1]) < 25:
        exit("angle too high or low, use [25,70]!!!")
    #print(f"Angle: {kit.servo[1].angle}")
    kit.servo[1].angle = int(sys.argv[1])
    # Positive angle = counterclockwise turn

