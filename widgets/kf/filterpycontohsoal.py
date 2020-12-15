# IMPORT LIB
import cv2 as cv
import filterpy
import numpy as np

from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import KalmanFilter
from filterpy.kalman.kalman_filter import predict, update

### TRACKING POSITION AND VELOCITY FROM POSITIONS ###

# CONSTRUCT OBJECTS DIMENSIONALITY (4x1 dengan 4x4)
f = KalmanFilter( dim_x = 4,
                  dim_z = 4 )

# ASSIGN INIT VALUES (proses mengkuti contoh soal)
f.x = np.array([ [257.],
                 [73.],      #position
                 [ np.negative(24.)],
                 [3.] ])    #velocity

# DEF STATE TRANSITION MATRIX
f.F = np.array([ [1., 0., 1., 0.],
                 [0., 1., 0., 1.],
                 [0., 0., 1., 0.], 
                 [0., 0., 0., 1.] ])
f.B = np.array([ [.5, 0.],
                 [0., .5],
                 [1., 0.], 
                 [0., 1.] ])
f.u = np.array([ [np.negative(14.)],
               [3.] ])

# DEF MEASUREMENT FUNCTION
f.H = np.array([ [1., 0., 0., 0.],
                 [0., 1., 0., 0.],
                 [0., 0., 1., 0.], 
                 [0., 0., 0., 1.] ])

# DEF COVARIANCE MATRIX
f.P = np.array([ [6400., 0., 1., 0.],
                 [0., 100., 0., 1.],
                 [0., 0., 25., 0.], 
                 [0., 0., 0., .09] ])

# ASSIGN MEASUREMENT NOISE
f.R = np.array([ [88.78**2, 0., 1., 0.],
                 [0., 18.34**2, 0., 1.],
                 [0., 0., 7.39**2, 0.], 
                 [0., 0., 0., 2.69**2] ])

# ASSIGN PROCESS NOISE  
f.Q = np.zeros((4,4))

#sensor input
def sensor_read():
    a =np.array([ [231.],
                 [77.],      #position
                 [ np.negative(26.)],
                 [4.] ])    #velocity
    return a


# PREDICT UPDATE LOOP
for i in range(1):
    print("start\n",f.x,"\n",f.P)
    z = np.array([ [231.],
                 [77.],      #position
                 [ np.negative(26.)],
                 [4.] ])    #velocity
    print(  "after z\n"
            "x before:", f.x_prior, "\n", 
            "x input:", f.x, "\n",
            "x after:", f.x_post, "\n",

            "P before:", f.P_prior, "\n", 
            "P input:", f.P, "\n",
            "P after:", f.P_post, "\n"
        )
    f.predict()
    print(  "after predict\n"
            "B:", f.B, "\n",
            "u:", f.u, "\n",  
            "x before:", f.x_prior, "\n", 
            "x input:", f.x, "\n",
            "x after:", f.x_post, "\n",

            "P before:", f.P_prior, "\n", 
            "P input:", f.P, "\n",
            "P after:", f.P_post, "\n"
        )
    f.update(z)
    print(  "after update\n"
            "z:", f.z, "\n",
            "x before:", f.x_prior, "\n", 
            "x input:", f.x, "\n",
            "x after:", f.x_post, "\n",

            "K:", f.K, "\n",
            "P before:", f.P_prior, "\n", 
            "P input:", f.P, "\n",
            "P after:", f.P_post, "\n"
        )