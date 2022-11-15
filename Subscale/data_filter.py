from flags import FAKE_DATA
import numpy as np
from filterpy.kalman import KalmanFilter
if FAKE_DATA: 
    import sensors_spoof as sensors
else:
    import sensors as sensors

# Dumby variable for filter object
my_filter = None

# Previous Time
t_prev = None

# Initializing the Kalman Filter
def initialize_filter():
    global my_filter

    # Initializing what sensor data is being read
    sensorMatrix = [[1,0,0], 
                    [0,0,1],
                    [0,0,1]]

    # Initializing Kalman Filter function
    my_filter = KalmanFilter(dim_x=3, dim_z=len(sensorMatrix))
    my_filter.H = np.array(sensorMatrix)

    # Covariance (error in estimate)
    my_filter.P *= 1
    
    # Measurement Noise
    my_filter.R *= 1

    # 
    my_filter.Q *= 1

    my_filter.x = np.array([0,0,0])

# Gets change in time between iterations
def get_dt(in_time):
    global t_prev

    if t_prev == NONE:
        dt = 0.1
    else:
        dt = in_time - t_prev
    t_prev = in_time
    return dt

# Generates state transition matrix
def gen_phi(dt):
    dp = 1
    ds = 0 # filler
    di = (dt**2)/2 # differences in time from current to previous state

    phi = np.array([dp, dt, di],
                   [ds, dp, dt],
                   [ds, ds, dp])

    return phi

# Calibrate sensors output (reads in tuple of sensor data)
def transform_accelerometer(in_accel):
    if FAKE_DATA:
        out_accel = (float(in_accel[0])) - 9.81
    else:
        out_accel = (float(in_accel[0])) - 9.81

    return out_accel

def transform_IMU(in_accel):
    if FAKE_DATA:
        out_accel = (float(in_accel[0])) - 9.81
    else:
        out_accel = (float(in_accel[0])) - 9.81

    return out_accel

# Actual filter woo hoo!
def filter_data():
    global my_filter
    global t_prev

    if my_filter == None:
        raise Exception("None")

    # Read sensor data
    measurements = []
    measurements.append(float(sensors.altitude))
    measurements.append(float(sensors.acceleration_acce_x), 
                        float(sensors.acceleration_acce_y), 
                        float(sensors.acceleration_acce_z))
    measurements.append(float(sensors.linacceleration_imu_x),
                        float(sensors.linacceleration_imu_y),
                        float(sensors.linacceleration_imu_z))