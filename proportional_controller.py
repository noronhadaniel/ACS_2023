"""
This program contains two functions: an apogee prediction algorithm
and a proportional control algorithm.
External data required:
    - Current Time
    - Current Velocity
    - Current Kalman Altitude
    - Target Apogee Constant [4600ft/1402m]
    - Servo Angle (to be implemented after testing)
Data output:
    - Projected Apogee
    - Apogee Error (Projected Apogee - Target Apogee[4600ft])
    - Target Servo Angle
"""

from utils import APOGEE_ALTITUDE as APOGEE_TARGET # 4600ft/1402m
from servo import Servo
from sensor_manager import SensorManager
import math

class Proportional_Controller:
    def __init__(self, sensor_manager: SensorManager, servo: Servo):
        self.apogee_projected = 0
        self.apogee_error = 0
        self.servo_target_angle = servo.SERVO_MIN
        self.sensor_manager = sensor_manager
        self.servo = servo
        self._t_prev = None
        self._dt = 0
        
    def _get_dt(self):
        if self._t_prev == None:
            self._dt = 0.1
        else:
            self._dt = self.sensor_manager.time - self._t_prev
        self._t_prev = self.sensor_manager.time

    def _fy(self, V, Cd_rocket, Cd_tabs, A_tabs, launch_angle, M_e):
        rho = 1.225 #[kg/m **3] density of air
        g = 9.80665 # [m/s **2] gravity
        A_rocket = (6.25*0.0254/2)**2*math.pi # [diamter in to m] [m**2]
        Ky = (-0.5*rho*Cd_rocket*V**2*A_rocket*math.cos(launch_angle) - 0.5*rho*Cd_tabs*V**2*A_tabs*math.cos(launch_angle) - M_e*g)/M_e
        return Ky
    
    def apogee_predict(self):
        # Get Inputs
        self._height = self.sensor_manager.kalman_altitude
        self._velocity = self.sensor_manager.kalman_velocity
        self._servo_angle = self.servo.angle

        # Initial constants
        # c = 343  #[m/s] speed of sound
        w_tabs = 1.75*0.0254  # [in to m] flap width
        L_tabs = 5.5*0.0254  # [in to m] flap length
        M_e = 773.95/35.274  # [oz to kg] EMPTY mass of rocket  # [m/s**2] gravity
        launch_angle = 6*math.pi/180 ## [degrees to radians] launch angle
        fixed_dt = 0.5  # [s] time step size

        # Mach = self._velocity/c

        # Mach correction
        # if Mach >= 1:
        #     Mach = 0.99

        # Unused code
        # extension = math.sin(0) * L_tabs
        extension = 0
        # Cd_o_tabs = 1.28*math.sin(0)
        Cd_o_tabs = 0
        # Cd_tabs = 1/math.sqrt(1-Mach**2)*Cd_o_tabs
        Cd_tabs = 0
        A_tabs = A_tabs = 4*w_tabs*(L_tabs)
        Cd_rocket = 0.42 

        # 4th Order Runge-Kutta Numerical approximation (simulate up to apogee)
        V_sim = self._velocity
        H_sim = self._height
        while V_sim > 0:
            k1vy = fixed_dt*self._fy(V_sim, Cd_rocket, Cd_tabs, A_tabs, launch_angle, M_e) 
            k1ry = fixed_dt*V_sim 
            
            k2vy = fixed_dt*self._fy(V_sim + 0.5*k1vy, Cd_rocket, Cd_tabs, A_tabs, launch_angle, M_e) 
            k2ry = fixed_dt*(V_sim + k1vy/2)
            
            k3vy = fixed_dt*self._fy(V_sim + 0.5*k2vy, Cd_rocket, Cd_tabs, A_tabs, launch_angle, M_e) 
            k3ry = fixed_dt*(V_sim + k2vy/2)
            
            k4vy = fixed_dt*self._fy(V_sim + k3vy, Cd_rocket, Cd_tabs, A_tabs, launch_angle, M_e) 
            k4ry = fixed_dt*(V_sim + k3vy)

            # Find values for Velocity and Altitude (at next time step)
            V_sim = V_sim + 1.0/6.0*(k1vy + 2.0*k2vy + 2.0*k3vy + k4vy) 
            H_sim = H_sim + 1.0/6.0*(k1ry + 2.0*k2ry + 2.0*k3ry + k4ry)

            # UNUSED: Calculate new drag coefficient for tabs/(rocket?)
            # Mach = V_sim/c
            # if Mach >= 1.0:
            #     Mach = 0.99
            # Cd_tabs = 1/math.sqrt(1-Mach**2)*Cd_o_tabs
            Cd_tabs = 0
        self.apogee_projected = H_sim
        self.apogee_error = H_sim - APOGEE_TARGET

    def proportional_target_angle_update(self):
        # Proportional Gain Constant (Max actuation is when Error>400ft ~= 123m)...(K_p*123+25=70deg)
        # K_p = 0.3
        K_p = 0.2
        self.servo_target_angle = K_p*self.apogee_error + self.servo.SERVO_MIN
        
        if (self.servo_target_angle - self._servo_angle) > 10:
            self.servo_target_angle = self._servo_angle + 10
        elif (self.servo_target_angle - self._servo_angle) < -10:
            self.servo_target_angle = self._servo_angle - 10
        # Limit checks...(Angle must be between 25 and 60 degrees)
        if self.servo_target_angle < self.servo.SERVO_MIN: # target < 25deg
            self.servo_target_angle = self.servo.SERVO_MIN + 1.0
        elif self.servo_target_angle > self.servo.SERVO_MAX:
            self.servo_target_angle = self.servo.SERVO_MAX - 1.0
        

