from flags import FAKE_DATA

if FAKE_DATA:
    import sensors_spoof as sensors
else:
    import sensors
import datalogger

datalogger.find_new_filename(datalogger.path, datalogger.name, datalogger.extension)
datalogger.new_CSV(datalogger.filename, datalogger.header)
sensors.init_sensors()
samples = 0

while True:
    sensors.read_sensors()
    datalogger.addRow(datalogger.f)
    samples += 1
    print("--------------------------------------------------")
    print(f"\nSample #{samples}; Time: {sensors.curr_time}s")
    print(f"Sample Rate = {samples/sensors.curr_time}Hz\n")
    print("--------------------------------------------------")

datalogger.f.close()
