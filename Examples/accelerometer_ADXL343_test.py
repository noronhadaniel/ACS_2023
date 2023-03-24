import time
import board
import adafruit_adxl34x
import sys

i2c = board.I2C()

accelerometer = adafruit_adxl34x.ADXL343(i2c)
accelerometer.range = adafruit_adxl34x.Range.RANGE_16_G

start_time = time.time()
samples = 0
previous_acceleration = (0,0,0)
acceleration_list = []

while (time.time()-start_time < 200):
    current_acceleration = accelerometer.acceleration
    if previous_acceleration != current_acceleration:
        print(f"x = {accelerometer.acceleration[0]:.3f} y = {(accelerometer.acceleration[1]-9.770833429185348):.3f} z = {accelerometer.acceleration[2]:.3f}")
        samples += 1
        acceleration_list.append(current_acceleration[1])
        previous_acceleration = current_acceleration
        print(f"Sample Rate = {samples/(time.time()-start_time):.4f}Hz")

    time.sleep(0.2)
print(f"Average z-axis acceleration: {sum(acceleration_list)/samples}m/s^2")


