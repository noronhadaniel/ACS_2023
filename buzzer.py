import time

import pwmio


class Buzzer:
    def __init__(self, pin, **kwargs):
        self.buzzer = pwmio.PWMOut(pin, **kwargs)
        self._frequency = 500

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, f):
        self._frequency = f
        self.buzzer.frequency = f

    def beep(self, s, duty_cycle=2 ** 15):
        self.buzzer.duty_cycle = duty_cycle
        time.sleep(s)
        self.buzzer.duty_cycle = 0
