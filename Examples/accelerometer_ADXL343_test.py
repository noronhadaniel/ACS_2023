import time
import board
import adafruit_adxl34x
import sys

i2c = board.I2C()

accelerometer = adafruit_adxl34x.ADXL343(i2c)

start_time = time.time()
samples = 0
previous_acceleration = (0,0,0)

while (time.time() - start_time) < float(sys.argv[1]):
    current_acceleration = accelerometer.acceleration
    if previous_acceleration != current_acceleration:
        print(f"x = {accelerometer.acceleration[0]:.3f} y = {accelerometer.acceleration[1]:.3f} z = {accelerometer.acceleration[2]:.3f}")
        samples += 1
        previous_acceleration = current_acceleration
        print(f"Sample Rate = {samples/(time.time()-start_time):.4f}Hz")

    #time.sleep(float(sys.argv[2]))



