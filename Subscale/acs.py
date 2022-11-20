from flags import FAKE_DATA
import data_logger
import data_filter

if FAKE_DATA:
    import sensors_spoof as sensors
else:
    import sensors


data_logger.find_new_filename(data_logger.path, data_logger.name, data_logger.extension)
data_logger.new_CSV(data_logger.filename, data_logger.header)
sensors.init_sensors()
data_filter.initialize_filter()
samples = 0

while True:
    sensors.read_sensors()
    data_filter.filter_data()
    data_logger.addRow(data_logger.f)
    samples += 1
    # acce_acceleration = []
    # imu_linacceleration = []
    print("--------------------------------------------------")
    if samples > 1:
        print(f"\nSample #{samples}; Time: {sensors.curr_time}s")
        print(f"Sample Rate = {samples/sensors.curr_time}Hz\n")
        #print(f"IMU Lin Acceleration(x): {sensors.linacceleration_imu_x}") # x reads -9.81
        #print(f"Accelerometer Acceleration(x): {sensors.acceleration_acce_x}") # x reads 10.2
        #print(f"Euler(y): {sensors.eulerangle_imu_y}") #euler y reads -90deg (beta)
        #print("Getting average accelerations (IMU+Accelerometer)")
        #acce_acceleration.append(sensors.acceleration_acce_x)
        #imu_linacceleration.append(sensors.linacceleration_imu_x) 
        #print(f"AVG_ACCE = {sum(acce_acceleration)/len(acce_acceleration)}")
        #print(f"AVG_IMU_ACCE = {sum(imu_linacceleration)/len(imu_linacceleration)}")
        # time.sleep(0.5)
    print("--------------------------------------------------")

data_logger.f.close()
