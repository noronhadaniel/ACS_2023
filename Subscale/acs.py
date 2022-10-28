import sensors
import datalogger

datalogger.find_new_filename(datalogger.path, datalogger.name, datalogger.extension)
datalogger.new_CSV(datalogger.filename, datalogger.header)
sensors.init_sensors()

while sensors.curr_time < 10:
    datalogger.addRow(datalogger.f, datalogger.row)

datalogger.f.close()
