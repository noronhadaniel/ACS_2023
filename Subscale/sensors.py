import time
import board
import adafruit_adxl34x
import adafruit_mpl3115a2
import adafruit_bno055

i2c = board.I2C()

accelerometer = None
altimeter = None
imu = None
start_time = None
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

def init_time() -> bool:
    global start_time
    start_time = time.time()
    return True

def init_accelerometer() -> bool:
    global accelerometer
    accelerometer = adafruit_adxl34x.ADXL343(i2c)
    accelerometer.range = adafruit_adxl34x.Range.RANGE_16_G
    return True

def init_altimeter(zero=True,sealevelpressure=101000) -> bool:
    global altimeter
    altimeter = adafruit_mpl3115a2.MPL3115A2(i2c)
    if zero:
        N = 100
        sea_sum = 0
        for x in range(N):
            sea_sum += altimeter.pressure
            time.sleep(0.01)
        altimeter.sealevel_pressure = int(sea_sum*100 / N)
        return True
    else:
        altimeter.sealevel_pressure = int(sealevelpressure) # in Pascals
        return True

def init_imu() -> bool:
    global imu
    imu = adafruit_bno055.BNO055_I2C(i2c)
    return True

def read_time():
    global curr_time
    try:
        curr_time = time.time() - start_time
    except:
        curr_time = 0

def read_accelerometer():
    global acceleration_acce_x
    global acceleration_acce_y
    global acceleration_acce_z
    try:
        acceleration = accelerometer.acceleration
        acceleration_acce_x = acceleration[0] or acceleration_acce_x
        acceleration_acce_y = acceleration[1] or acceleration_acce_y
        acceleration_acce_z = acceleration[2] or acceleration_acce_z
    except:
        acceleration_acce_x = 0
        acceleration_acce_y = 0
        acceleration_acce_z = 0

def read_altimeter():
    global altitude
    try:
        altitude = altimeter.altitude or altitude
    except:
        altitude = 0

def read_imu():
    global acceleration_imu_x, acceleration_imu_y, acceleration_imu_z 
    global linacceleration_imu_x, linacceleration_imu_y, linacceleration_imu_z
    global eulerangle_imu_x, eulerangle_imu_y, eulerangle_imu_z
    global gravity_imu_x, gravity_imu_y, gravity_imu_z
    try:
        acceleration = imu.acceleration
        linear_acceleration = imu.linear_acceleration
        euler = imu.euler
        gravity = imu.gravity
        acceleration_imu_x = acceleration[0] or acceleration_imu_x
        acceleration_imu_y = acceleration[1] or acceleration_imu_y
        acceleration_imu_z = acceleration[2] or acceleration_imu_z
        linacceleration_imu_x = linear_acceleration[0] or linacceleration_imu_x
        linacceleration_imu_y = linear_acceleration[1] or linacceleration_imu_y
        linacceleration_imu_z = linear_acceleration[2] or linacceleration_imu_z
        eulerangle_imu_x = euler[0] or eulerangle_imu_x
        eulerangle_imu_y = euler[1] or eulerangle_imu_y
        eulerangle_imu_z = euler[2] or eulerangle_imu_z
        gravity_imu_x = gravity[0] or gravity_imu_x
        gravity_imu_y = gravity[1] or gravity_imu_y
        gravity_imu_z = gravity[2] or gravity_imu_z
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
    result = init_time()
    result = result and init_accelerometer()
    result = result and init_altimeter()
    result = result and init_imu()
    result = result and init_time()
    return result

def read_sensors():
    read_time()
    read_accelerometer()
    read_altimeter()
    read_imu()

