import time

import adafruit_adxl34x
import adafruit_bno055
import adafruit_mpl3115a2


class Accelerometer:
    def __init__(self, i2c):
        self.accelerometer = adafruit_adxl34x.ADXL343(i2c)
        self.accelerometer.range = adafruit_adxl34x.Range.RANGE_16_G

        self._acceleration_acce = (0, 0, 0)
        self._acceleration_acce_x = 0
        self._acceleration_acce_y = 0
        self._acceleration_acce_z = 0

    @property
    def acceleration_acce(self):
        self._acceleration_acce = self.accelerometer.acceleration or self._acceleration_acce
        self._acceleration_acce = (
            self._acceleration_acce[0] or self._acceleration_acce_x,
            self._acceleration_acce[1] or self.acceleration_acce_y,
            self._acceleration_acce[2] or self._acceleration_acce_z
        )
        return self._acceleration_acce

    @property
    def acceleration_acce_x(self):
        acceleration = self.acceleration_acce
        self._acceleration_acce_x = acceleration[0] or self._acceleration_acce_x
        self._acceleration_acce_y = acceleration[1] or self._acceleration_acce_y
        self._acceleration_acce_z = acceleration[2] or self._acceleration_acce_z
        return self._acceleration_acce_x

    @property
    def acceleration_acce_y(self):
        acceleration = self.acceleration_acce
        self._acceleration_acce_x = acceleration[0] or self._acceleration_acce_x
        self._acceleration_acce_y = acceleration[1] or self._acceleration_acce_y
        self._acceleration_acce_z = acceleration[2] or self._acceleration_acce_z
        return self._acceleration_acce_y

    @property
    def acceleration_acce_z(self):
        acceleration = self.acceleration_acce
        self._acceleration_acce_x = acceleration[0] or self._acceleration_acce_x
        self._acceleration_acce_y = acceleration[1] or self._acceleration_acce_y
        self._acceleration_acce_z = acceleration[2] or self._acceleration_acce_z
        return self._acceleration_acce_z


class Altimeter:
    def __init__(self, i2c, zero=True, sea_level_pressure=101000):
        self.altimeter = adafruit_mpl3115a2.MPL3115A2(i2c)

        self._altitude = 0

        if zero:
            self._zero()
        else:
            self.altimeter.sealevel_pressure = int(sea_level_pressure)

    def _zero(self):
        n = 100
        sea_sum = 0
        for _ in range(n):
            sea_sum += self.altimeter.pressure
            time.sleep(0.01)
        self.altimeter.sealevel_pressure = int(sea_sum * 100 / n)

    @property
    def altitude(self):
        self._altitude = self.altimeter.altitude or self._altitude
        return self._altitude


class IMU:
    def __init__(self, i2c):
        self.imu = adafruit_bno055.BNO055_I2C(i2c)

        self._acceleration_imu = (0, 0, 0)
        self._acceleration_imu_x = 0
        self._acceleration_imu_y = 0
        self._acceleration_imu_z = 0
        self._linacceleration_imu = (0, 0, 0)
        self._linacceleration_imu_x = 0
        self._linacceleration_imu_y = 0
        self._linacceleration_imu_z = 0
        self._eulerangle_imu = (0, 0, 0)
        self._eulerangle_imu_x = 0
        self._eulerangle_imu_y = 0
        self._eulerangle_imu_z = 0
        self._gravity_imu = (0, 0, 0)
        self._gravity_imu_x = 0
        self._gravity_imu_y = 0
        self._gravity_imu_z = 0

    @property
    def acceleration_imu(self):
        self._acceleration_imu = self.imu.acceleration or self._acceleration_imu
        self._acceleration_imu = (
            self._acceleration_imu[0] or self._acceleration_imu_x,
            self._acceleration_imu[1] or self.acceleration_imu_y,
            self._acceleration_imu[2] or self._acceleration_imu_z
        )
        return self._acceleration_imu

    @property
    def acceleration_imu_x(self):
        acceleration = self.acceleration_imu
        self._acceleration_imu_x = acceleration[0] or self._acceleration_imu_x
        self._acceleration_imu_y = acceleration[1] or self._acceleration_imu_y
        self._acceleration_imu_z = acceleration[2] or self._acceleration_imu_z
        return self._acceleration_imu_x

    @property
    def acceleration_imu_y(self):
        acceleration = self.acceleration_imu
        self._acceleration_imu_x = acceleration[0] or self._acceleration_imu_x
        self._acceleration_imu_y = acceleration[1] or self._acceleration_imu_y
        self._acceleration_imu_z = acceleration[2] or self._acceleration_imu_z
        return self._acceleration_imu_y

    @property
    def acceleration_imu_z(self):
        acceleration = self.acceleration_imu
        self._acceleration_imu_x = acceleration[0] or self._acceleration_imu_x
        self._acceleration_imu_y = acceleration[1] or self._acceleration_imu_y
        self._acceleration_imu_z = acceleration[2] or self._acceleration_imu_z
        return self._acceleration_imu_z

    @property
    def linacceleration_imu(self):
        self._linacceleration_imu = self.imu.linear_acceleration or self._linacceleration_imu
        self._linacceleration_imu = (
            self._linacceleration_imu[0] or self._linacceleration_imu_x,
            self._linacceleration_imu[1] or self.linacceleration_imu_y,
            self._linacceleration_imu[2] or self._linacceleration_imu_z
        )
        return self._linacceleration_imu

    @property
    def linacceleration_imu_x(self):
        linacceleration = self.linacceleration_imu
        self._linacceleration_imu_x = linacceleration[0] or self._linacceleration_imu_x
        self._linacceleration_imu_y = linacceleration[1] or self._linacceleration_imu_y
        self._linacceleration_imu_z = linacceleration[2] or self._linacceleration_imu_z
        return self._linacceleration_imu_x

    @property
    def linacceleration_imu_y(self):
        linacceleration = self.linacceleration_imu
        self._linacceleration_imu_x = linacceleration[0] or self._linacceleration_imu_x
        self._linacceleration_imu_y = linacceleration[1] or self._linacceleration_imu_y
        self._linacceleration_imu_z = linacceleration[2] or self._linacceleration_imu_z
        return self._linacceleration_imu_y

    @property
    def linacceleration_imu_z(self):
        linacceleration = self.linacceleration_imu
        self._linacceleration_imu_x = linacceleration[0] or self._linacceleration_imu_x
        self._linacceleration_imu_y = linacceleration[1] or self._linacceleration_imu_y
        self._linacceleration_imu_z = linacceleration[2] or self._linacceleration_imu_z
        return self._linacceleration_imu_z

    @property
    def eulerangle_imu(self):
        self._eulerangle_imu = self.imu.euler or self._eulerangle_imu
        self._eulerangle_imu = (
            self._eulerangle_imu[0] or self._eulerangle_imu_x,
            self._eulerangle_imu[1] or self._eulerangle_imu_y,
            self._eulerangle_imu[2] or self._eulerangle_imu_z
        )
        return self._eulerangle_imu

    @property
    def eulerangle_imu_x(self):
        eulerangle = self.eulerangle_imu
        self._eulerangle_imu_x = eulerangle[0] or self._eulerangle_imu_x
        self._eulerangle_imu_y = eulerangle[1] or self._eulerangle_imu_y
        self._eulerangle_imu_z = eulerangle[2] or self._eulerangle_imu_z
        return self._eulerangle_imu_x

    @property
    def eulerangle_imu_y(self):
        eulerangle = self.eulerangle_imu
        self._eulerangle_imu_x = eulerangle[0] or self._eulerangle_imu_x
        self._eulerangle_imu_y = eulerangle[1] or self._eulerangle_imu_y
        self._eulerangle_imu_z = eulerangle[2] or self._eulerangle_imu_z
        return self._eulerangle_imu_y

    @property
    def eulerangle_imu_z(self):
        eulerangle = self.eulerangle_imu
        self._eulerangle_imu_x = eulerangle[0] or self._eulerangle_imu_x
        self._eulerangle_imu_y = eulerangle[1] or self._eulerangle_imu_y
        self._eulerangle_imu_z = eulerangle[2] or self._eulerangle_imu_z
        return self._eulerangle_imu_z

    @property
    def gravity_imu(self):
        self._gravity_imu = self.imu.gravity or self._gravity_imu
        self._gravity_imu = (
            self._gravity_imu[0] or self._gravity_imu_x,
            self._gravity_imu[1] or self._gravity_imu_y,
            self._gravity_imu[2] or self._gravity_imu_z
        )
        return self._gravity_imu

    @property
    def gravity_imu_x(self):
        gravity = self.gravity_imu
        self._gravity_imu_x = gravity[0] or self._gravity_imu_x
        self._gravity_imu_y = gravity[1] or self._gravity_imu_y
        self._gravity_imu_z = gravity[2] or self._gravity_imu_z
        return self._gravity_imu_x

    @property
    def gravity_imu_y(self):
        gravity = self.gravity_imu
        self._gravity_imu_x = gravity[0] or self._gravity_imu_x
        self._gravity_imu_y = gravity[1] or self._gravity_imu_y
        self._gravity_imu_z = gravity[2] or self._gravity_imu_z
        return self._gravity_imu_y

    @property
    def gravity_imu_z(self):
        gravity = self.gravity_imu
        self._gravity_imu_x = gravity[0] or self._gravity_imu_x
        self._gravity_imu_y = gravity[1] or self._gravity_imu_y
        self._gravity_imu_z = gravity[2] or self._gravity_imu_z
        return self._gravity_imu_z

