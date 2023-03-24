"""
sensors.py contains the class representations of the ACS device's sensors.
Note that all initial values are 0.

Also, each sensor allows for spoofing. To spoof the sensor, pass a pandas
dataframe corresponding to an output CSV (with appropriate titles). The
sensor class will then not bother reading from the physical sensor and
instead return the value from the dataframe.
"""

import time

import adafruit_adxl34x
import adafruit_bno055
import adafruit_mpl3115a2
import adafruit_bmp3xx


class Accelerometer:
    """
    The Accelerometer class represents the ADXL343 accelerometer.
    """

    def __init__(self, i2c, spoof=None):
        self.spoof = spoof
        if self.spoof is not None:
            self.acceleration_acce_x_gen = iter((0, *spoof["ADXL_Acceleration_X"]))
            self.acceleration_acce_y_gen = iter((0, *spoof["ADXL_Acceleration_Y"]))
            self.acceleration_acce_z_gen = iter((0, *spoof["ADXL_Acceleration_Z"]))
            return

        self.accelerometer = adafruit_adxl34x.ADXL343(i2c)
        self.accelerometer.range = adafruit_adxl34x.Range.RANGE_16_G

        self._acceleration_acce = (0, 0, 0)

    @property
    def acceleration_acce(self):
        if self.spoof is not None:
            return (
                next(self.acceleration_acce_x_gen),
                next(self.acceleration_acce_y_gen),
                next(self.acceleration_acce_z_gen)
            )

        self._acceleration_acce = self.accelerometer.acceleration
        return self._acceleration_acce


class Altimeter:
    """
    The Altimeter class represents the MPL3115A2 altimeter.
    """

    def __init__(self, i2c, zero=True, sea_level_pressure=101000, spoof=None):
        self.spoof = spoof
        if self.spoof is not None:
            self.altitude_gen = iter((0, *spoof["Altitude"]))
            return
        
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
        if self.spoof is not None:
            return next(self.altitude_gen)

        self._altitude = self.altimeter.altitude
        return self._altitude
    
class Altimeter_BMP390:
    """
    The Altimeter class represents the BMP390 altimeter.
    """

    def __init__(self, i2c, zero=True, sea_level_pressure=101000, spoof=None):
        self.spoof = spoof
        if self.spoof is not None:
            try:
                self.altitude_gen = iter((0, *spoof["Altitude"]))
            except:
                self.altitude_gen = iter((0, *spoof["BMP_Altitude"]))
            return
        
        self.altimeter = adafruit_bmp3xx.BMP3XX_I2C(i2c)
        self.altimeter.pressure_oversampling = 4

        self._altitude = 0

        if zero:
            self._zero()
        else:
            self.altimeter.sea_level_pressure = int(sea_level_pressure)

    def _zero(self):
        n = 100
        sea_sum = 0
        for _ in range(n):
            sea_sum += self.altimeter.pressure
            time.sleep(0.01)
        self.altimeter.sea_level_pressure = int(sea_sum/n)

    @property
    def altitude(self):
        if self.spoof is not None:
            return next(self.altitude_gen)

        self._altitude = self.altimeter.altitude
        return self._altitude


class IMU:
    """
    The IMU class represents the BNO055 inertial measurement unit.
    Note that after reviewing the source code of all the sensors, I
    determined that the IMU is the only one capable of software failure,
    which manifests in returning (None, None, None) for a reading. We
    account for this by only updating the reading if value[0] is not None. 
    """

    def __init__(self, i2c, spoof=None):
        self.spoof = spoof
        if self.spoof is not None:
            self.acceleration_imu_x_gen = iter((0, *spoof["IMU_Acceleration_X"]))
            self.acceleration_imu_y_gen = iter((0, *spoof["IMU_Acceleration_Y"]))
            self.acceleration_imu_z_gen = iter((0, *spoof["IMU_Acceleration_Z"]))
            self.linacceleration_imu_x_gen = iter((0, *spoof["Linear_Acceleration_X"]))
            self.linacceleration_imu_y_gen = iter((0, *spoof["Linear_Acceleration_Y"]))
            self.linacceleration_imu_z_gen = iter((0, *spoof["Linear_Acceleration_Z"]))
            self.eulerangle_imu_x_gen = iter((0, *spoof["Euler_Angle_X"]))
            self.eulerangle_imu_y_gen = iter((0, *spoof["Euler_Angle_Y"]))
            self.eulerangle_imu_z_gen = iter((0, *spoof["Euler_Angle_Z"]))
            self.gravity_imu_x_gen = iter((0, *spoof["Gravity_X"]))
            self.gravity_imu_y_gen = iter((0, *spoof["Gravity_Y"]))
            self.gravity_imu_z_gen = iter((0, *spoof["Gravity_Z"]))
            return

        self.imu = adafruit_bno055.BNO055_I2C(i2c)

        self._acceleration_imu = (0, 0, 0)
        self._linacceleration_imu = (0, 0, 0)
        self._eulerangle_imu = (0, 0, 0)
        self._gravity_imu = (0, 0, 0)

    @property
    def acceleration_imu(self):
        if self.spoof is not None:
            return (
                next(self.acceleration_imu_x_gen),
                next(self.acceleration_imu_y_gen),
                next(self.acceleration_imu_z_gen)
            )

        value = self.imu.acceleration
        if value[0] is not None:
            self._acceleration_imu = value
        return self._acceleration_imu

    @property
    def linacceleration_imu(self):
        if self.spoof is not None:
            return (
                next(self.linacceleration_imu_x_gen),
                next(self.linacceleration_imu_y_gen),
                next(self.linacceleration_imu_z_gen)
            )
        
        value = self.imu.linear_acceleration
        if value[0] is not None:
            self._linacceleration_imu = value
        return self._linacceleration_imu

    @property
    def eulerangle_imu(self):
        if self.spoof is not None:
            return (
                next(self.eulerangle_imu_x_gen),
                next(self.eulerangle_imu_y_gen),
                next(self.eulerangle_imu_z_gen)
            )
        
        value = self.imu.euler
        if value[0] is not None:
            self._eulerangle_imu = value
        return self._eulerangle_imu

    @property
    def gravity_imu(self):
        if self.spoof is not None:
            return (
                next(self.gravity_imu_x_gen),
                next(self.gravity_imu_y_gen),
                next(self.gravity_imu_z_gen)
            )
        
        value = self.imu.gravity
        if value[0] is not None:
            self._gravity_imu = value
        return self._gravity_imu
