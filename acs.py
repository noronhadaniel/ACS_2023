"""
acs.py contains the main ACS control flow. This is where it all happens.
"""

SPOOF_FILE = None
SPOOF_FILE = "./_data/data_01.csv"

if SPOOF_FILE is not None:
    import pandas

import datetime
import traceback

import board

from buzzer import Buzzer
from logger import Logger
from sensor_manager import SensorManager
from sensors import Accelerometer, Altimeter, IMU
from servo import Servo
from state import State
from proportional_controller import Proportional_Controller
import utils

buzzer = Buzzer(board.D13)
buzzer.beep(1)

if SPOOF_FILE is None:
    brd = board.I2C()
    sensor_manager = SensorManager(Accelerometer(brd), Altimeter(brd), IMU(brd))
else:
    df = pandas.read_csv(SPOOF_FILE)
    sensor_manager = SensorManager(Accelerometer(None, spoof=df), Altimeter(None, spoof=df), IMU(None, spoof=df), spoof=df)

buzzer.frequency = 880
buzzer.beep(1)

# Initialize servor motor.
servo = Servo(channels=16)

# Initialize proportional controller
proportional_controller = Proportional_Controller(sensor_manager, servo)

logger = Logger(utils.DATA_PATH + "/data_" + utils.file_number() + ".csv", sensor_manager, servo, proportional_controller)

activated = False
deactivated = False
burnout_time = float("inf")

buzzer.frequency = 1760
buzzer.beep(1)

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

        if sensor_manager.state == State.BURNOUT: #and not activated and not deactivated:
            proportional_controller.apogee_predict()
            burnout_time = sensor_manager.time
            # activated = True
            # kit.servo[1].angle = MIN_SERVO_ANGLE #16
            # time.sleep(1)
        elif (sensor_manager.state == State.BURNOUT) and (sensor_manager.time - burnout_time >= 1): #and activated:
            proportional_controller.apogee_predict()
            proportional_controller.proportional_target_angle_update()
            servo.angle = proportional_controller.servo_target_angle
        elif sensor_manager.state == State.OVERSHOOT:
            servo.angle = servo.SERVO_MAX
        elif sensor_manager.state == State.APOGEE:
            servo.angle = servo.SERVO_MIN
        """
        elif sensor_manager.time - burnout_time >= 5 and activated: 
            deactivated = True
            activated = False
            servo.angle = Servo.SERVO_MIN
        elif sensor_manager.time - burnout_time >= 3 and activated:
            servo.angle = 65
        elif sensor_manager.time - burnout_time >= 1 and activated: 
            servo.angle = 50
        """
        # Finally, log the sensor values before repeating the cycle.
        logger.log()
        
    except Exception:
        # Report Issue
        print("Sorry, this program is experiencing a glitch :(")
        # Close data file
        logger.file.close()
        # Log Error
        with open('log_fullscale_error.txt','a') as err_log:
            err_log.write(str(datetime.datetime.now()))
            err_log.write("\n")
            err_log.write(traceback.format_exc()) 
            err_log.write("\n")
        # Retract Flaps
        servo.angle = Servo.SERVO_MIN
        
        # Give audio feedback and raise exception 
        buzzer.frequency = 256
        buzzer.beep(10)
        raise

