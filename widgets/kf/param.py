#list posisi objek
pos_x = [291., 281., 257., 231., 202., 178., 145., 117.,  81.,  51.]
pos_y = [ 70.,  70.,  73.,  77.,  84.,  89.,  96., 102., 111., 118.]

#list velocity
vel_x = [0.]
for i in range(len(pos_x)):
    j = i+1
    print(i)
    print(pos_x[i])
    try:
        vel_x.append(pos_x[j] - pos_x[i])
        print(pos_x[j])
    except:
        pass

#list acceleration
accel_x = [0., 0.]
try:
    if not vel_x[2]:
        pass
    else:
        for i in range(len(vel_x)):
            j = i+1
            k = j+1
            accel_x.append(vel_x[k]-vel_x[j]) 
except:
    pass

print(pos_x, vel_x, accel_x)