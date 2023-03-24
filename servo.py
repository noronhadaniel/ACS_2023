import time

from adafruit_servokit import ServoKit


class Servo:
    SERVO_CHANNEL = 1
    SERVO_INIT = 50
    SERVO_MIN = 25
    SERVO_MAX = 60
    SERVO_BURNOUT = 50 # replaced by proportional control algorithm

    def __init__(self, *, channels, initialize=True):
        self.kit = ServoKit(channels=channels)
        self.kit.servo[Servo.SERVO_CHANNEL].set_pulse_width_range(500, 2400)

        # Run initialization sequence.
        if initialize:
            self.angle = Servo.SERVO_MIN
            time.sleep(1)
            self.angle = Servo.SERVO_INIT
            time.sleep(1)
            self.angle = Servo.SERVO_MIN
            time.sleep(1)

    @property
    def angle(self):
        # return self.kit.servo[Servo.SERVO_CHANNEL].angle
        if self.kit.servo[Servo.SERVO_CHANNEL].angle is None:
            print("Servo angle returned None value!")
            return self.angle
        else:
            return self.kit.servo[Servo.SERVO_CHANNEL].angle

    @angle.setter
    def angle(self, angle):
        # Safety checks.
        # We do not want the servo to destroy the ACS device...
        if angle < Servo.SERVO_MIN:
            raise ValueError(f"servo angle must be at least {Servo.SERVO_MIN}")
        if angle > Servo.SERVO_MAX:
            raise ValueError(f"servo angle must be at most {Servo.SERVO_MAX}")

        self.kit.servo[Servo.SERVO_CHANNEL].angle = angle

