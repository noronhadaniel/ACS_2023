import glob
import csv
import sensors

path = '../_data/'
name = 'data'
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
    "Gravity_Z"
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
            "%.4f" % sensors.curr_time,
            "%.4f" % sensors.acceleration_acce_x,
            "%.4f" % sensors.acceleration_acce_y,
            "%.4f" % sensors.acceleration_acce_z,
            "%.4f" % sensors.altitude,
            "%.4f" % sensors.acceleration_imu_x,
            "%.4f" % sensors.acceleration_imu_y,
            "%.4f" % sensors.acceleration_imu_z,
            "%.4f" % sensors.linacceleration_imu_x,
            "%.4f" % sensors.linacceleration_imu_y,
            "%.4f" % sensors.linacceleration_imu_z,
            "%.4f" % sensors.eulerangle_imu_x,
            "%.4f" % sensors.eulerangle_imu_y,
            "%.4f" % sensors.eulerangle_imu_z,
            "%.4f" % sensors.gravity_imu_x,
            "%.4f" % sensors.gravity_imu_y,
            "%.4f" % sensors.gravity_imu_z
        ]
    csv.writer(f).writerow(row)
    return True

