from enum import Enum

from data_filter import DataFilter
from sensors import Accelerometer, Altimeter, IMU


class State(Enum):
    INACTIVE = 0
    ARMED = 1
    ACTIVE = 2
    MAX = 3
    FAILURE = 4


class StateManager:
    def __init__(self, accelerometer: Accelerometer, altimeter: Altimeter, imu: IMU, dfilter: DataFilter):
        self.accelerometer = accelerometer
        self.altimeter = altimeter
        self.imu = imu
        self.dfilter = dfilter

        self._state = State.INACTIVE

    @property
    def state(self) -> State:
        if self.dfilter.kalman_altitude < 50 and self.dfilter.kalman_acceleration < 50:
            self._state = State.INACTIVE
        elif self.dfilter.kalman_altitude > 50 and self.dfilter.kalman_acceleration > 50:
            self._state = State.ARMED
        elif self.dfilter.kalman_altitude < 1402 and self.dfilter.kalman_acceleration < -6:
            self._state = State.ACTIVE
        elif self.dfilter.kalman_altitude > 1402 and self.dfilter.kalman_velocity > 0:
            self._state = State.MAX
        elif self.dfilter.kalman_velocity < 0:
            self._state = State.FAILURE

        return self._state

