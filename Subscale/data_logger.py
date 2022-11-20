from flags import FAKE_DATA
import glob
import csv
import data_filter

if FAKE_DATA:
    import sensors_spoof as sensors
else:
    import sensors

if FAKE_DATA:
    name = 'fake_data'
    path = '../test_data/'
else:
    name = 'data'
    path = '../_data/'

extension = '.csv'
filename = None
f = None
header = [
    "Time",
    "ADXL_Acceleration_X",
    "ADXL_Acceleration_Y",
    "ADXL_Acceleration_Z",
    "Altitude",
    "IMU_Acceleration_X",
    "IMU_Acceleration_Y",
    "IMU_Acceleration_Z",
    "Linear_Acceleration_X",
    "Linear_Acceleration_Y",
    "Linear_Acceleration_Z",
    "Euler_Angle_X",
    "Euler_Angle_Y",
    "Euler_Angle_Z",
    "Gravity_X",
    "Gravity_Y",
    "Gravity_Z",
    "Kalman_Acceleration",
    "Kalman_Velocity",
    "Kalman_Altitude",
    "Orientation(Beta)"
]

def find_new_filename(path: str, name: str, extension: str) -> bool:
    global filename
    # Find existing files in directory
    old_files = glob.glob(path+name+"_*"+extension) # returns list of files

    # Find largest file
    max_num = 0
    for file in old_files:
        file_num = int(file.replace(path+name+"_","").replace(extension,""))
        if file_num > max_num:
            max_num = file_num
    if len(old_files) == 0:
        new_num = 0
    else:
        new_num = max_num + 1

    # Create new filename and return it
    if new_num < 10:
        new_filename = path+name+'_0'+str(new_num)+extension
    else:
        new_filename = path+name+'_'+str(new_num)+extension

    filename = new_filename
    return True

def new_CSV(filename: str, header: list) -> bool:
    global f
    file = open(filename, 'w')
    csv.writer(file).writerow(header)
    f = file

def addRow(f) -> bool:
    row = [
            sensors.curr_time,
            sensors.acceleration_acce_x,
            sensors.acceleration_acce_y,
            sensors.acceleration_acce_z,
            sensors.altitude,
            sensors.acceleration_imu_x,
            sensors.acceleration_imu_y,
            sensors.acceleration_imu_z,
            sensors.linacceleration_imu_x,
            sensors.linacceleration_imu_y,
            sensors.linacceleration_imu_z,
            sensors.eulerangle_imu_x,
            sensors.eulerangle_imu_y,
            sensors.eulerangle_imu_z,
            sensors.gravity_imu_x,
            sensors.gravity_imu_y,
            sensors.gravity_imu_z,
            data_filter.kalman_acceleration,
            data_filter.kalman_velocity,
            data_filter.kalman_altitude,
            data_filter.orientation_beta
        ]
    csv.writer(f).writerow(row)
    return True

