"""
acs.py contains the main ACS control flow. This is where it all happens.
"""
MIN_SERVO_ANGLE = 25
MAX_SERVO_ANGLE = 70
SERVO_INIT_ANGLE = 40
SERVO_BURNOUT_ANGLE = 50
SERVO_CHANNEL = 1

SPOOF_FILE = None
#SPOOF_FILE = "./test_data/test_Truncated_ACS_Fullscale_Launch_Data_20221120.csv"

if SPOOF_FILE is not None:
    import pandas

import time
import datetime
import traceback

from adafruit_servokit import ServoKit
import board
import pwmio

from sensor_logger import SensorLogger
from sensor_manager import SensorManager
from sensors import Accelerometer, Altimeter, IMU
from state import State
import utils

buzzer = pwmio.PWMOut(board.D13, variable_frequency=False)

buzzer.frequency = 440
buzzer.duty_cycle = 2**15
time.sleep(1)
buzzer.duty_cycle = 0


if SPOOF_FILE is None:
    brd = board.I2C()
    sensor_manager = SensorManager(Accelerometer(brd), Altimeter(brd), IMU(brd))
else:
    df = pandas.read_csv(SPOOF_FILE)
    sensor_manager = SensorManager(Accelerometer(None, spoof=df), Altimeter(None, spoof=df), IMU(None, spoof=df), spoof=df)

sensor_logger = SensorLogger(utils.DATA_PATH + "/data_" + utils.file_number() + ".csv", sensor_manager)

buzzer.frequency = 880
buzzer.duty_cycle = 2**15
time.sleep(1)
buzzer.duty_cycle = 0

# Initialize servor motor.
kit = ServoKit(channels=16)
kit.servo[SERVO_CHANNEL].set_pulse_width_range(500, 2400)
kit.servo[SERVO_CHANNEL].angle = MIN_SERVO_ANGLE #25
time.sleep(1)
kit.servo[SERVO_CHANNEL].angle = SERVO_INIT_ANGLE #36
time.sleep(1)
kit.servo[SERVO_CHANNEL].angle = MIN_SERVO_ANGLE #16
time.sleep(1)

activated = False
deactivated = False
burnout_time = float("inf")

buzzer.frequency = 1760
buzzer.duty_cycle = 2**15
time.sleep(1)
buzzer.duty_cycle = 0

while True:
    try:
        # Control flow begins with reading sensors, filtering data, and calculating the state.
        # All this is handled by one function call.
        sensor_manager.read_sensors()

        # Next, we must use our sensor readings and state calculation to
        # determine the ACS's path of action.
        print("––––––––––")
        print("Reading " + str(sensor_manager.readings))
        print("Time: " + str(sensor_manager.time) + "s")
        print("Frequency: " + str(sensor_manager.readings / sensor_manager.time))
        print("State: " + sensor_manager.state.name)

        if sensor_manager.state == State.BURNOUT and not activated and not deactivated:
            burnout_time = sensor_manager.time
            activated = True
            # kit.servo[1].angle = MIN_SERVO_ANGLE #16
            # time.sleep(1)
        elif sensor_manager.time - burnout_time >= 5 and activated: 
            deactivated = True
            activated = False
            kit.servo[SERVO_CHANNEL].angle = MIN_SERVO_ANGLE #16
        elif sensor_manager.time - burnout_time >= 3 and activated: 
            kit.servo[SERVO_CHANNEL].angle = 65
        elif sensor_manager.time - burnout_time >= 1 and activated: 
            kit.servo[SERVO_CHANNEL].angle = 50
        
        # Finally, log the sensor values before repeating the cycle.
        sensor_logger.log()
        # Wait for servo actuation if using fake data:
        if SPOOF_FILE is not None:
            time.sleep(0.04) # Simulates 25Hz
        
    except Exception:
        # Report Issue
        print("Sorry, this program is experiencing a glitch :(")
        # Close data file
        sensor_logger.file.close()        
        # Log Error
        with open('log_fullscale_error.txt','a') as err_log:
            err_log.write(datetime.date.today().ctime())
            err_log.write("\n")
            err_log.write(traceback.format_exc()) 
            err_log.write("\n")
        # Retract Flaps
        kit.servo[SERVO_CHANNEL].angle = MIN_SERVO_ANGLE
        
        # Give audio feedback and raise exception 
        buzzer.frequency = 256
        buzzer.duty_cycle = 2**15
        time.sleep(10)
        buzzer.duty_cycle = 0
        raise

