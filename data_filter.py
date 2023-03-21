import time

from filterpy.kalman import KalmanFilter
import numpy as np


class DataFilter:
    def __init__(self, spoof=None):
        self.spoof = spoof

        self._dt = 0
        self._t_prev = None
        self._initialize_filter()
        
        if self.spoof is not None:
            self.time_gen = iter((0, *spoof["Time"]))
            return

        self.kalman_altitude = 0
        self.kalman_velocity = 0
        self.kalman_acceleration = 0
        self.orientation_beta = 0

    def _initialize_filter(self):
        # Initializing what sensor data is being read
        sensor_matrix = [
            [1, 0, 0],
            [0, 0, 1]
            # [0, 0, 1]
        ]

        # Initializing Kalman Filter function
        self.filter = KalmanFilter(dim_x=3, dim_z=len(sensor_matrix))
        self.filter.H = np.array(sensor_matrix)

        # Covariance (error in estimate)
        self.filter.P *= 1

        # Measurement Noise
        self.filter.R *= 1

        self.filter.Q *= 1
        self.filter.x = np.array([0, 0, 0])

    def _calculate_dt(self, in_time):
        if self._t_prev is None:
            self._dt = 0.1
        else:
            self._dt = in_time - self._t_prev
        self._t_prev = in_time

    def _generate_phi(self):
        if self.spoof is not None:
            self._calculate_dt(next(self.time_gen))
        else:
            self._calculate_dt(time.time())

        dp = 1
        ds = 0  # filler
        di = (self._dt ** 2) / 2  # differences in time from current to previous state

        phi = np.array([
            [dp, self._dt, di],
            [ds, dp, self._dt],
            [ds, ds, dp]
        ])

        return phi

    def filter_data(self, altitude, acceleration_acce_x, acceleration_acce_y, acceleration_acce_z, eulerangle_imu_y, eulerangle_imu_z):
        R_x = np.array([
            [1, 0, 0],
            [0, np.cos(eulerangle_imu_z*np.pi/180), np.sin(eulerangle_imu_z*np.pi/180)],
            [0, -np.sin(eulerangle_imu_z*np.pi/180), np.cos(eulerangle_imu_z*np.pi/180)]
        ])
        R_y = np.array([
            [np.cos(eulerangle_imu_y*np.pi/180), 0, -np.sin(eulerangle_imu_y*np.pi/180)],
            [0, 1, 0],
            [np.sin(eulerangle_imu_y*np.pi/180), 0, np.cos(eulerangle_imu_y*np.pi/180)]
        ])
        acceleration = np.matmul(R_y,np.matmul(R_x,np.array([[acceleration_acce_x], [acceleration_acce_y], [acceleration_acce_z]])))
        # Read sensor data
        measurements = [
            float(altitude),
            float(float(acceleration[2]) - 9.770833429185348)
            # float(linacceleration_imu_z - 9.80665)
        ]

        # Update filter parameters
        params = np.array(measurements)
        self.filter.F = self._generate_phi()

        # Perform prediction/update steps
        self.filter.predict()
        self.filter.update(params)

        # Log the output
        self.kalman_altitude, self.kalman_velocity, self.kalman_acceleration = self.filter.x
        self.orientation_beta = eulerangle_imu_z  # Beta angle between rotated and fixed coordinate z-axis

