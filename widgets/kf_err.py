# IMPORT LIB
import cv2 as cv
import filterpy
import numpy as np
import math

from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import KalmanFilter
from filterpy.kalman.kalman_filter import predict, update

### PARAMETERS OPERATION ###

#list posisi objek
pos_x = [291., 281., 257., 231., 202., 178., 145., 117.,  81.,  51.]
pos_y = [ 70.,  70.,  73.,  77.,  84.,  89.,  96., 102., 111., 118.]
kf_res_x = []
kf_res_y = []
kf_res_vx = []
kf_res_vy = []

#list velocity; input=pos
def vel(alist):
    vel_list = [0.]
    for i in range(len(alist)):
        j = i+1
        print(i)
        print(alist[i])
        try:
            vel_list.append(alist[j] - alist[i])
        except:
            pass
    return vel_list

#list acceleration; input=vel_list
def accel(alist):
    accel_list = [0., 0.]
    try:
        if not alist[2]:
            pass
        else:
            for i in range(len(alist)):
                j = i+1
                k = j+1
                accel_list.append(alist[k]-alist[j]) 
    except:
        pass
    return accel_list

#list error
def sqrt_alist(alist): #input alist= _min_avg yang mau di kuadrat
    sqrt_list=[]
    for i in range(len(alist)):
        sqrt_list.append(round((alist[i]**2), 2))
    return sqrt_list

def avgpos(alist):
    average = sum(alist) / len(alist)
    average = round(average, 2)
    return average

def avgvel(alist):
    average = sum(alist) / (len(alist)-1)
    average = round(average, 2)
    return average

def pos_min_avg(alist):
    min_avg = []
    try:
        for i in range(len(alist)):
            min_aver = alist[i] - avgpos(alist)
            min_avg.append(round(min_aver, 2))
    except:
        pass
    return min_avg

def vel_min_avg(alist):
    min_avg = [0.]
    for i in range(len(alist)):
        j = i+1
        try:
            min_avg.append(round((alist[j] - avgvel(alist)), 2))
        except:
            pass
    return min_avg

#standar deviasi
def stdpos(alist): #input=list yang udh di kuadrat
    n = len(alist) 
    std = math.sqrt( (1/(n-1)) * sum(alist) )
    return std

def stdvel(alist): #input=list yang udh di kuadrat; -2 soalnya isi mulai dr index 1
    n = len(alist)
    std = math.sqrt( (1/(n-2)) * sum(alist) )
    return std

vel_x = vel(pos_x)
vel_y = vel(pos_y)
accelx = accel(pos_x)
accely = accel(pos_y)

var_x = stdpos( sqrt_alist( pos_min_avg(pos_x) ) )
var_y = stdpos( sqrt_alist( pos_min_avg(pos_y) ) )
var_vx = stdvel( sqrt_alist( vel_min_avg(vel_x) ) )
var_vy = stdvel( sqrt_alist( vel_min_avg(vel_y) ) )


### TRACKING POSITION AND VELOCITY FROM POSITIONS ###

# CONSTRUCT OBJECTS DIMENSIONALITY (4x1 dengan 4x4)
f = KalmanFilter( dim_x = 4,
                  dim_z = 4 )

# ASSIGN INIT VALUES (proses mengkuti contoh soal)
f.x = np.array([ pos_x[2],
                 pos_y[2],      #position
                 vel_x[2],
                 vel_y[2] ])    #velocity

# DEF STATE TRANSITION MATRIX
f.F = np.array([ [1., 0., 1., 0.],
                 [0., 1., 0., 1.],
                 [0., 0., 1., 0.], 
                 [0., 0., 0., 1.] ])
f.B = np.array([ [.5, 0.],
                 [0., .5],
                 [1., 0.], 
                 [0., 1.] ])
f.u = np.array([ accelx[2],
                 accely[2] ])

# DEF MEASUREMENT FUNCTION
f.H = np.array([ [1., 0., 0., 0.],
                 [0., 1., 0., 0.],
                 [0., 0., 1., 0.], 
                 [0., 0., 0., 1.] ])

# DEF COVARIANCE MATRIX
f.P = np.array([ [.9*((var_x)**2), 0., 1., 0.],
                 [0., .9*((var_y)**2), 0., 1.],
                 [0., 0., .9*((var_vx)**2), 0.], 
                 [0., 0., 0., .9*((var_vy)**2)] ])

# ASSIGN MEASUREMENT NOISE
f.R = np.array([ [(var_x)**2, 0., 1., 0.],
                 [0., (var_y)**2, 0., 1.],
                 [0., 0., (var_vx)**2, 0.], 
                 [0., 0., 0., (var_vy)**2] ])

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
for i in range(len(accelx)-3): #masi kebanyakan len nya mknya out of range
    z = np.array([ pos_x[i+3],
                   pos_y[i+3],      #position
                   vel_x[i+3],
                   vel_y[i+3] ])    #velocity    
    f.predict()
    try:
        f.u = np.array([ accelx(i+3),
                         accely(i+3)  ])
    except:
        pass
    f.update(z)
    kf_res_x.append(np.round(f.x[0]))
    kf_res_y.append(np.round(f.x[1]))
    kf_res_vx.append(np.round(f.x[2]))
    kf_res_vy.append(np.round(f.x[3]))

    print('input z:')
    print(z)
    print('predict')
    print(f.x)

print(kf_res_x,kf_res_y,kf_res_vx,kf_res_vy)
b=.9*((var_vy)**2)
print(b)
print(var_x,var_y,var_vx,var_vy)
print(f.R)