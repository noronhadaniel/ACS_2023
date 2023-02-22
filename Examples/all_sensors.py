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
acceleration_acce = None
acceleration_imu = None
linacceleration_imu = None
eulerangle_imu = None
gravity_imu = None
altitude = None



def init_time():
    global start_time
    start_time = time.time()
    return True

def init_accelerometer():
    global accelerometer
    accelerometer = adafruit_adxl34x.ADXL343(i2c)
    return True

def init_altimeter(zero=True,sealevelpressure=101000):
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

def init_imu():
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
    global acceleration_acce
    try:
        acceleration_acce = accelerometer.acceleration
    except:
        acceleration_acce = (0,0,0)

def read_altimeter():
    global altitude
    try:
        altitude = altimeter.altitude
    except:
        altitude = 0

def read_imu():
    global acceleration_imu, linacceleration_imu, eulerangle_imu, gravity_imu
    try:
        acceleration_imu = imu.acceleration
        linacceleration_imu = imu.linear_acceleration
        eulerangle_imu = imu.euler
        gravity_imu = imu.gravity
    except:
        acceleration_imu = (0,0,0)
        linacceleration_imu = (0,0,0)
        eulerangle_imu = (0,0,0)
        gravity_imu = (0,0,0)
       
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
    
## TESTING ##

init_sensors()
samples = 0
while curr_time <= 30:
    read_sensors()
    print(f"\nTime = {curr_time:.3f}s")
    print("-----Accelerometer-----")
    print(f"Acceleration = ({acceleration_acce[0]:.3f}, {acceleration_acce[1]:.3f}, {acceleration_acce[2]:.3f})")
    print()
    print("-----Altimeter-----")
    print(f"Altitude = {altitude:.2f}m")
    print()
    print("-----IMU-----")
    print(f"Acceleration = ({acceleration_imu[0]}, {acceleration_imu[1]}, {acceleration_imu[2]})")
    print(f"Linear Acceleration = ({linacceleration_imu[0]}, {linacceleration_imu[1]}, {linacceleration_imu[2]})")
    print(f"Euler Angle = ({eulerangle_imu[0]}, {eulerangle_imu[1]}, {eulerangle_imu[2]})")
    print(f"Gravity = ({gravity_imu[0]}, {gravity_imu[1]}, {gravity_imu[2]})")
    print()
    samples += 1
    print(f"Sample Rate = {samples/curr_time:.2f}Hz")

