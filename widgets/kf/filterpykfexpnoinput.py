# IMPORT LIB
import cv2 as cv
import filterpy
import numpy as np
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import KalmanFilter
from filterpy.kalman.kalman_filter import predict, update

### TRACKING POSITION AND VELOCITY FROM POSITIONS ###

# CONSTRUCT OBJECTS DIMENSIONALITY
f = KalmanFilter( dim_x = 2,
                  dim_z = 1 )

# ASSIGN INIT VALUES 
f.x = np.array([ [2.],      #position
                 [0.] ])    #velocity

# DEF STATE TRANSITION MATRIX
f.F = np.array([ [1., 1.], 
                 [0., 1.] ])

# DEF MEASUREMENT FUNCTION
f.H = np.array([ [1., 0.] ])

# DEF COVARIANCE MATRIX
f.P = np.array([ [1000., 0.], 
                 [0., 1000.] ])

# ASSIGN MEASUREMENT NOISE
f.R = np.array([ [5.] ])

# ASSIGN PROCESS NOISE  
f.Q = Q_discrete_white_noise(dim=2, dt=0.1, var=0.13)

# PREDICT UPDATE LOOP
while True:
    z, R = sensor_read()
    x, P = predict(x, P, F, Q)
    x, P = update(x, P, z, R, H)