import time
import board
import adafruit_bmp3xx

i2c = board.I2C()
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

bmp.pressure_oversampling = 4
# bmp.temperature_oversampling = 1
bmp.sea_level_pressure = 988

n = 100
sea_sum = 0
for _ in range(n):
    sea_sum += bmp.pressure
    time.sleep(0.01)
bmp.sea_level_pressure = int(sea_sum/n)

start_time = time.time()
samples = 0
while True:
    #print(
    #    "Pressure: {:6.4f}  Temperature: {:5.2f}".format(bmp.pressure, bmp.temperature)
    #)
    print('Pressure: {} Pascals'.format(bmp.pressure))
    print('Altitude: {} meters'.format(bmp.altitude))
    # time.sleep(1)
    print(f"Sample Rate: {samples/(time.time() - start_time)}Hz")
    samples += 1

