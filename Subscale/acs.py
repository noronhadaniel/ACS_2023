FAKE_DATA = False

if FAKE_DATA:
    import sensors_spoof as sensors
else:
    import sensors
import datalogger

datalogger.find_new_filename(datalogger.path, datalogger.name, datalogger.extension)
datalogger.new_CSV(datalogger.filename, datalogger.header)
sensors.init_sensors()

while sensors.curr_time < 10:
    sensors.read_sensors()
    datalogger.addRow(datalogger.f)
    print("Logged")
    print(sensors.curr_time)

datalogger.f.close()
