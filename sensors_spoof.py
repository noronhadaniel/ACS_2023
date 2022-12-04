import pandas
from flags import FAKE_DATA_FILE

accelerometer = None
altimeter = None
imu = None
curr_time = 0
acceleration_acce_x = 0
acceleration_acce_y = 0
acceleration_acce_z = 0
acceleration_imu_x = 0
acceleration_imu_y = 0
acceleration_imu_z = 0
linacceleration_imu_x = 0
linacceleration_imu_y = 0
linacceleration_imu_z = 0
eulerangle_imu_x = 0
eulerangle_imu_y = 0
eulerangle_imu_z = 0
gravity_imu_x = 0
gravity_imu_y = 0
gravity_imu_z = 0
altitude = 0


### Reading the data file

Fake_data = pandas.read_csv(FAKE_DATA_FILE)

Time_list = iter(Fake_data['Time'].tolist())
ADXL_Acceleration_X = iter(Fake_data['ADXL_Acceleration_X'].tolist())
ADXL_Acceleration_Y = iter(Fake_data['ADXL_Acceleration_Y'].tolist())
ADXL_Acceleration_Z = iter(Fake_data['ADXL_Acceleration_Z'].tolist())
Altitude = iter(Fake_data['Altitude'].tolist())
IMU_Acceleration_X = iter(Fake_data['IMU_Acceleration_X'].tolist())
IMU_Acceleration_Y = iter(Fake_data['IMU_Acceleration_Y'].tolist())
IMU_Acceleration_Z = iter(Fake_data['IMU_Acceleration_Z'].tolist())
Linear_Acceleration_X = iter(Fake_data['Linear_Acceleration_X'].tolist())
Linear_Acceleration_Y = iter(Fake_data['Linear_Acceleration_Y'].tolist())
Linear_Acceleration_Z = iter(Fake_data['Linear_Acceleration_Z'].tolist())
Euler_Angle_X = iter(Fake_data['Euler_Angle_X'].tolist())
Euler_Angle_Y = iter(Fake_data['Euler_Angle_Y'].tolist())
Euler_Angle_Z = iter(Fake_data['Euler_Angle_Z'].tolist())
Gravity_X = iter(Fake_data['Gravity_X'].tolist())
Gravity_Y = iter(Fake_data['Gravity_Y'].tolist())
Gravity_Z = iter(Fake_data['Gravity_Z'].tolist())

### end reading file

def read_time():
    global curr_time
    try:
        curr_time = next(Time_list)
    except:
        curr_time = 0

def read_accelerometer():
    global acceleration_acce_x
    global acceleration_acce_y
    global acceleration_acce_z
    try:
        acceleration_acce_x = next(ADXL_Acceleration_X)
        acceleration_acce_y = next(ADXL_Acceleration_Y)
        acceleration_acce_z = next(ADXL_Acceleration_Z)
    except:
        acceleration_acce_x = 0
        acceleration_acce_y = 0
        acceleration_acce_z = 0

def read_altimeter():
    global altitude
    try:
        altitude = next(Altitude)
    except:
        altitude = 0

def read_imu():
    global acceleration_imu_x, acceleration_imu_y, acceleration_imu_z 
    global linacceleration_imu_x, linacceleration_imu_y, linacceleration_imu_z
    global eulerangle_imu_x, eulerangle_imu_y, eulerangle_imu_z
    global gravity_imu_x, gravity_imu_y, gravity_imu_z
    try:
        acceleration_imu_x = next(IMU_Acceleration_X)
        acceleration_imu_y = next(IMU_Acceleration_Y)
        acceleration_imu_z = next(IMU_Acceleration_Z)
        linacceleration_imu_x = next(Linear_Acceleration_X)
        linacceleration_imu_y = next(Linear_Acceleration_Y)
        linacceleration_imu_z = next(Linear_Acceleration_Z)
        eulerangle_imu_x = next(Euler_Angle_X)
        eulerangle_imu_y = next(Euler_Angle_Y)
        eulerangle_imu_z = next(Euler_Angle_Z)
        gravity_imu_x = next(Gravity_X)
        gravity_imu_y = next(Gravity_Y)
        gravity_imu_z = next(Gravity_Z)
    except:
        acceleration_imu_x = 0
        acceleration_imu_y = 0
        acceleration_imu_z = 0
        linacceleration_imu_x = 0
        linacceleration_imu_y = 0
        linacceleration_imu_z = 0
        eulerangle_imu_x = 0
        eulerangle_imu_y = 0
        eulerangle_imu_z = 0
        gravity_imu_x = 0
        gravity_imu_y = 0
        gravity_imu_z = 0

def init_sensors():
    return True

def read_sensors():
    read_time()
    read_accelerometer()
    read_altimeter()
    read_imu()
