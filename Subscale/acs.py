from flags import FAKE_DATA
import time
import data_logger
import data_filter
import datetime
import traceback

if FAKE_DATA:
    import sensors_spoof as sensors
else:
    import sensors


data_logger.find_new_filename(data_logger.path, data_logger.name, data_logger.extension)
data_logger.new_CSV(data_logger.filename, data_logger.header)
sensors.init_sensors()
data_filter.initialize_filter()
samples = 0
errors = 0

while True:
    try:
        sensors.read_sensors()
        data_filter.filter_data()
        data_logger.addRow(data_logger.f)
        samples += 1
        # acce_acceleration = []
        # imu_linacceleration = []
        print("--------------------------------------------------")
        if samples > 1:
            print("Logging Data")
            #print(f"\nSample #{samples}; Time: {sensors.curr_time}s")
            #print(f"Sample Rate = {samples/sensors.curr_time}Hz\n")
            #print(f"IMU Lin Acceleration(x): {sensors.linacceleration_imu_x}") # x reads -9.81
            #print(f"Kalman Acceleration(x): {data_filter.kalman_acceleration}") # x reads 10.2
            #print(f"Kalman Altitude: {data_filter.kalman_altitude}") 
            #print(f"Kalman Orientation: {data_filter.orientation_beta}") #euler y reads -90deg (beta)

            # Kalman Orientation accurate within ~2 degrees (+- 0.5)

            #print("Getting average accelerations (IMU+Accelerometer)")
            #acce_acceleration.append(sensors.acceleration_acce_x)
            #imu_linacceleration.append(sensors.linacceleration_imu_x) 
            #print(f"AVG_ACCE = {sum(acce_acceleration)/len(acce_acceleration)}")
            #print(f"AVG_IMU_ACCE = {sum(imu_linacceleration)/len(imu_linacceleration)}")
            # time.sleep(0.5)
        print("--------------------------------------------------")
    except:
        errors += 1
        print("Error! Will try looping again after logging it :(")
        print(f"\nError #{errors}")
        print(datetime.datetime.now())
        print(traceback.format_exc())
        print()
        with open("error_log.txt", 'a') as err_log:
            err_log.write(f"Error #{errors}\n")
            err_log.write(str(datetime.datetime.now()))
            err_log.write('\n')
            err_log.write(traceback.format_exc())
            err_log.write('\n')
        if errors >= 10:
            break
        else:
            time.sleep(0.5)
            continue    

data_logger.f.close()
