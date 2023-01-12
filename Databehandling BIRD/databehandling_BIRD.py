import numpy as np

#Importér datafiler
magdata = np.genfromtxt("mag_fil.csv",delimiter=",",names=True,dtype=None,encoding=None)
imutidsdata = open("IMUtid.txt","r").read().splitlines()
imudata = np.genfromtxt("state.csv",delimiter=",",names=True,dtype=None,encoding=None)
yawdata = np.genfromtxt("Yaw.csv",delimiter=";",names=True,dtype=None,encoding=None)
imuSensor = np.genfromtxt("RawSensors.csv",delimiter=",",names=True,dtype=None,encoding=None) #meget upræcis!!

#konvertér timestamp til sekunder
def convert_time(time_stamp):
    time = time_stamp.split(" ")[1].split(":")
    seconds = int(time[0])*60*60+int(time[1])*60+float(time[2])
    return(seconds)

starttid = convert_time(imutidsdata[0]) #startid for IMU data

#timestamps for hhv magnetometer, kamera, IMU
mag_time = [convert_time(magdata[i][0]) for i in range(len(magdata))]
billede_time = [convert_time(yawdata[i][0]) for i in range(len(yawdata))]
imu_tid = [starttid + i*0.10 for i in range(len(imudata))]

#sammenlign billedetid med sensortid
def sammenlign_tid(billede_tid,sensor_tid):
    sensor_index = []
    j = 0
    for i in billede_tid:
        while sensor_tid[j] < i:
            j += 1
        if sensor_tid[j] >= i:
            sensor_index.append(j)
            pass
    return sensor_index

#returnerer liste med index i sensorlisten for tilsvarende billede tid 
mag_index = sammenlign_tid(billede_time,mag_time)
imu_index = sammenlign_tid(billede_time,imu_tid)

#al data, der er synkroniseret i tid
magnetometer_vector = [[magdata[i][7],magdata[i][8],magdata[i][9]] for i in mag_index] #Fluxgate 3D magnetometer data
imuMag = [[imuSensor[i][9]/10,imuSensor[i][10]/10,imuSensor[i][11]/10] for i in imu_index] #IMU magnetometer data
roll =  [imudata[i][43]*np.pi/180 for i in imu_index] #roll fra IMU
pitch = [imudata[i][44]*np.pi/180 for i in imu_index] #pitch fra IMU
yaw = [-float(yawdata[i][3].replace(",","."))*np.pi/180 for i in range(len(yawdata))] #pitch fra billede

#----------------------------#
#Rotationsmatrix
def rotate(a,b,c,x):
    R = np.array([[np.cos(a)*np.cos(b),np.cos(a)*np.sin(b)*np.sin(c)-np.sin(a)*np.cos(c),np.cos(a)*np.sin(b)*np.cos(c)+np.sin(a)*np.sin(c)],
    [np.sin(a)*np.cos(b),np.sin(a)*np.sin(b)*np.sin(c)+np.cos(a)*np.cos(c),np.sin(a)*np.sin(b)*np.cos(c)-np.cos(a)*np.sin(c)],
    [-np.sin(b),np.cos(b)*np.sin(c),np.cos(b)*np.cos(c)]])

    M = R@x
    return(M)

#Beregning af vinkel mellem vektor og x-aksen (parraleol med landingsbane)
def vinkel(vektor):
    return np.arccos(np.abs(vektor[0])/np.linalg.norm(vektor))*180/np.pi

#Beregning af kurs for hver måling!
vinkler = []
for i in range(len(mag_index)):
    # print("pitch",pitch[i],"roll",roll[i],"yaw",yaw[i])
    rotated_vector = rotate(yaw[i],pitch[i],roll[i],np.array(magnetometer_vector[i]))
    print(i,": bird_vector",magnetometer_vector[i],"corrected_vector",rotated_vector) 

    kurs = 360-vinkel(rotated_vector)
    vinkler.append(kurs)

    print("kurs: ",kurs)

print("gennemsnit: ", np.mean(vinkler))
