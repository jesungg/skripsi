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

velx = vel(pos_x)
print(velx)
print(avgvel(velx))

#bla = list_min_avg(pos_x)
bla1 = vel_min_avg(velx)
pangkat_v=sqrt_alist(bla1)
std_si_v= stdvel(pangkat_v)
print (bla1,pangkat_v, std_si_v)




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