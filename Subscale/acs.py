from flags import FAKE_DATA
import data_logger

if FAKE_DATA:
    import sensors_spoof as sensors
else:
    import sensors


data_logger.find_new_filename(data_logger.path, data_logger.name, data_logger.extension)
data_logger.new_CSV(data_logger.filename, data_logger.header)
sensors.init_sensors()
samples = 0

while True:
    sensors.read_sensors()
    data_logger.addRow(data_logger.f)
    samples += 1
    print("--------------------------------------------------")
    print(f"\nSample #{samples}; Time: {sensors.curr_time}s")
    print(f"Sample Rate = {samples/sensors.curr_time}Hz\n")
    print("--------------------------------------------------")

data_logger.f.close()
