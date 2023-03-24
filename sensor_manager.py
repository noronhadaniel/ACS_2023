"""
sensor_manager.py contains the implementation of SensorManager,
which is responsible for the meat of filtration and state calculation.
"""

import time

from data_filter import DataFilter
from sensors import Accelerometer, Altimeter, Altimeter_BMP390, IMU
from state import State
from utils import LAUNCH_ACCELERATION, LAUNCH_ALTITUDE, BURNOUT_ACCELERATION, APOGEE_VELOCITY, APOGEE_ALTITUDE


class SensorManager:
    """
    The SensorManager class is responsible for updating sensor values,
    filtering the data through a Kalman Filter, and calculating the
    state of the launch vehicle. This is our source of truth.
    """

    def __init__(self, accelerometer: Accelerometer, altimeter: Altimeter, altimeter_bmp: Altimeter_BMP390,imu: IMU, spoof=None):
        self.spoof = spoof

        self.accelerometer = accelerometer
        self.altimeter = altimeter
        self.altimeter_bmp = altimeter_bmp
        self.imu = imu
        self.filter = DataFilter(spoof=self.spoof)

        self.readings = 0
        self.state = State.GROUND

        if self.spoof is not None:
            self.time_gen = iter((0, *spoof["Time"]))
        else:
            self.start = time.time()

        self.read_sensors()

    def _update_state(self):
        """
        The _update_state function determines and assigns the state of the launch vehicle
        given the sensor readings. The function is intended to be called internally
        by read_sensors because the state depends on the previous state (thus, it
        must be recalculated each time the sensors are read).
        """

        # Ground -> Launched.
        if self.state == State.GROUND and self.kalman_altitude > LAUNCH_ALTITUDE and self.kalman_acceleration > LAUNCH_ACCELERATION:
            self.state = State.LAUNCHED
        # Launched -> Burnout.
        elif self.state == State.LAUNCHED and self.kalman_altitude < APOGEE_ALTITUDE and self.kalman_acceleration < BURNOUT_ACCELERATION:
            self.state = State.BURNOUT
        # Burnout -> Overshoot.
        elif self.state == State.BURNOUT and self.kalman_altitude > APOGEE_ALTITUDE and self.kalman_acceleration < BURNOUT_ACCELERATION:
            self.state = State.OVERSHOOT
        # Burnout -> Apogee.
        elif self.state == State.BURNOUT and self.kalman_altitude < APOGEE_ALTITUDE and self.kalman_velocity < APOGEE_VELOCITY:
            self.state = State.APOGEE
        # Overshoot -> Apogee.
        elif self.state == State.OVERSHOOT and self.kalman_altitude > APOGEE_ALTITUDE and self.kalman_velocity < APOGEE_VELOCITY:
            self.state = State.APOGEE

    #def _calculate_predicted_apogee(self):
    #    delta_y = (-self.kalman_velocity ** 2) / (2 * self.kalman_acceleration)
    #    return self.kalman_altitude + delta_y

    def read_sensors(self):
        """
        The read_sensors function reads a new iteration of all sensor values.
        It also reads the current time, passes some values through the Kalman filter,
        and updates the launch vehicle state.
        """

        # Read time.
        # Time begins at approximately (but not exactly) 0.
        if self.spoof is not None:
            self.time = next(self.time_gen)
        else:
            self.time = time.time() - self.start

        # Read accelerometer values.
        self.acceleration_acce = self.accelerometer.acceleration_acce
        self.acceleration_acce_x = self.acceleration_acce[0]
        self.acceleration_acce_y = self.acceleration_acce[1]
        self.acceleration_acce_z = self.acceleration_acce[2]

        # Read altimeter values.
        self.altitude = self.altimeter.altitude
        self.altitude_bmp = self.altimeter_bmp.altitude

        # Read IMU values.
        self.acceleration_imu = self.imu.acceleration_imu
        self.acceleration_imu_x = self.acceleration_imu[0]
        self.acceleration_imu_y = self.acceleration_imu[1]
        self.acceleration_imu_z = self.acceleration_imu[2]
        self.linacceleration_imu = self.imu.linacceleration_imu
        self.linacceleration_imu_x = self.linacceleration_imu[0]
        self.linacceleration_imu_y = self.linacceleration_imu[1]
        self.linacceleration_imu_z = self.linacceleration_imu[2]
        self.eulerangle_imu = self.imu.eulerangle_imu
        self.eulerangle_imu_x = self.eulerangle_imu[0]
        self.eulerangle_imu_y = self.eulerangle_imu[1]
        self.eulerangle_imu_z = self.eulerangle_imu[2]
        self.gravity_imu = self.imu.gravity_imu
        self.gravity_imu_x = self.gravity_imu[0]
        self.gravity_imu_y = self.gravity_imu[1]
        self.gravity_imu_z = self.gravity_imu[2]

        # Calculate filter values.
        # Note that we can treat the Kalman filter as another sensor.
        self.filter.filter_data(self.altitude, self.acceleration_acce_y, self.eulerangle_imu_z)
        self.kalman_acceleration = self.filter.kalman_acceleration
        self.kalman_velocity = self.filter.kalman_velocity
        self.kalman_altitude = self.filter.kalman_altitude
        self.orientation_beta = self.filter.orientation_beta # Initial values for calibration: 359.9375, -0.125, -87.25

        # Predict apogee.
        # self.predicted_apogee = self._calculate_predicted_apogee()

        # Update state.
        # Note that we can also treat the state as another sensor,
        # once we have updated our sensor readings.
        self._update_state()

        # Update readings count.
        self.readings += 1

