"""
acs.py contains the main ACS control flow. This is where it all happens.
"""

SPOOF_FILE = None
# SPOOF_FILE = "./test_data/data_01_20230218.csv"

if SPOOF_FILE is not None:
    import pandas

import time
import datetime
import traceback

import board

from buzzer import Buzzer
from logger import Logger
from sensor_manager import SensorManager
from sensors import Accelerometer, Altimeter, Altimeter_BMP390, IMU
from servo import Servo
from state import State
from proportional_controller import Proportional_Controller
import utils

buzzer = Buzzer(board.D13)
buzzer.beep(1)

if SPOOF_FILE is None:
    brd = board.I2C()
    sensor_manager = SensorManager(Accelerometer(brd), Altimeter(brd), Altimeter_BMP390(brd), IMU(brd))
else:
    df = pandas.read_csv(SPOOF_FILE)
    sensor_manager = SensorManager(Accelerometer(None, spoof=df), Altimeter(None, spoof=df), Altimeter_BMP390(None, spoof=df), IMU(None, spoof=df), spoof=df)

buzzer.frequency = 880
buzzer.beep(1)

# Initialize servor motor.
servo = Servo(channels=16)

# Initialize proportional controller
proportional_controller = Proportional_Controller(sensor_manager, servo)

logger = Logger(utils.DATA_PATH + "/data_" + utils.file_number() + ".csv", sensor_manager, servo, proportional_controller)

# activated = False
# deactivated = False
done = False
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
        print("Reading " + str(sensor_manager.readings-1))
        print("Time: " + str(sensor_manager.time) + "s")
        print("Frequency: " + str(sensor_manager.readings / sensor_manager.time))
        print("State: " + sensor_manager.state.name)
        
        if (sensor_manager.state == State.BURNOUT) and (burnout_time == float("inf")):
            burnout_time = sensor_manager.time
        elif (sensor_manager.state == State.BURNOUT) and (sensor_manager.time - burnout_time >= 1): #and activated:
            proportional_controller.apogee_predict()
            proportional_controller.proportional_target_angle_update()
            servo.angle = proportional_controller.servo_target_angle
        elif sensor_manager.state == State.BURNOUT: # and not activated and not deactivated:
            proportional_controller.apogee_predict()
            # activated = True
            # kit.servo[1].angle = MIN_SERVO_ANGLE #16
            # time.sleep(1)
        elif sensor_manager.state == State.OVERSHOOT:
            servo.angle = servo.SERVO_MAX
            proportional_controller.servo_target_angle = servo.SERVO_MAX
        elif (sensor_manager.state == State.APOGEE) and (sensor_manager.time - burnout_time <= 6):
            sensor_manager.state = State.BURNOUT
            proportional_controller.apogee_predict()
            proportional_controller.proportional_target_angle_update()
            servo.angle = proportional_controller.servo_target_angle
        elif sensor_manager.state == State.APOGEE:
            if not done:
                servo.angle = servo.SERVO_MIN
                proportional_controller.apogee_projected = sensor_manager.kalman_altitude
                proportional_controller.servo_target_angle = servo.SERVO_MIN
                with open("SUCCESS.txt", 'w') as f_success:
                    f_success.write(f"ACS detected apogee at {sensor_manager.kalman_altitude}m = {sensor_manager.kalman_altitude*3.28084}ft (Kalman Altitude @ t={sensor_manager.time}s from power-on).\nMPL3115A2 altitude reading was {sensor_manager.altitude}m = {sensor_manager.altitude*3.28084}ft.\nIt will be on the ground shortly and is ready for inspection!\n") 
                done = not done
            else:
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
        if SPOOF_FILE is not None:
            time.sleep(1/28.5) # Simulates 28.5Hz (Servo Delay...)
        
    except Exception:
        # Report Issue
        print("Sorry, this program is experiencing a glitch :(")
        # Log Error
        with open('log_fullscale_error.txt','a') as err_log:
            err_log.write("ERROR!\n")
            err_log.write(str(datetime.datetime.now()))
            err_log.write("\n")
            err_log.write("Sample #")
            err_log.write(str(sensor_manager.readings-1))
            err_log.write(" @ ")
            err_log.write(str(sensor_manager.time))
            err_log.write("s\n")
            err_log.write(traceback.format_exc()) 
            err_log.write("\n")
        # Retract Flaps
        servo.angle = Servo.SERVO_MIN
        
        # Give audio feedback and raise exception 
        buzzer.frequency = 255
        buzzer.beep(0.1)
        continue

