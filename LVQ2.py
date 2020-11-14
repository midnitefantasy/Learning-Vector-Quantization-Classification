import numpy as np
import math
import csv
import re
#Baca csv train
def ReadData():
    dataTraining=[]
    kelas=[]
    with open('C:\\Users\\fadil\\Downloads\\data_tugas\Train45.csv') as f:
        readCSV = csv.reader(f, delimiter=';')
        for row in readCSV:
            data=[]
            for i in range(len(row)):
                if i != (len(row)-1):
                    data.append(float(row[i]))
                
            kelas.append(float(row[-1]))
            dataTraining.append(data)
    return (dataTraining, kelas)


def ReadDataTest():
    dataTesting=[]
    kelas=[]
    with open('C:\\Users\\fadil\\Downloads\\data_tugas\\Test.csv') as f:
        readCSV = csv.reader(f, delimiter=';')
        for row in readCSV:
            data=[]
            for i in range(len(row)):
                if i != (len(row)-1):
                    data.append(float(row[i]))
                
            kelas.append(float(row[-1]))
            dataTesting.append(data)
    return (dataTesting,kelas)

  
#Jarak euclidean
def jarakEuc(w, x):
    result = np.zeros(len(w))
    for i in range(len(w)):
        rst = 0
        for j in range(len(x)):
            dst = x[j] - w[i,j]
            rst = rst + math.pow(dst,2)
        result[i] = math.sqrt(rst)
    return result

#Teknik sorting
def sorting(dist, w, kls_a): # dist, w, kls_a
    for j in range(len(dist)):
        for i in range(0, len(dist)-1):
            if dist[i]>dist[i+1]:
                temp_dist = dist[i]
                dist[i]= dist[i+1]
                dist[i+1]= temp_dist
                wtemp = []
                for z in w[i]:
                    wtemp.append(z)
                w[i]= w[i+1]
                w[i+1] = wtemp
                temp_kls_a =0 
                temp_kls_a=kls_a[i]
                kls_a[i] = kls_a[i+1]
                kls_a[i+1]= temp_kls_a
                
    return (dist , w, kls_a)    

#update bobot winner saja
def updateBobotPemenang(x, w, alfa, kelas_uji, kelas_w):
    deltaW = alfa*(x-w)
    if kelas_uji == kelas_w:
        w = w + deltaW
    elif kelas_uji != kelas_w: 
        w = w - deltaW
    return w

#Update bobot runner up dan bobot winner
def updateBobotRunnerV2(x, w, alfa, kelas_uji, kelas_w, kelas_winner):
    deltaw=[]
    for i in range(len(w)):
        deltaw.append(alfa * (x - w[i]))
    for i in range(len(w)):
        if i<2:
            for j in range(len(w[i])):
                if kelas_winner==kelas_uji:   
                    w[i] = w[i] - deltaw[i]
                else:
                    w[i] = w[i] + deltaw[i]
    return w

#Pengecekan if Kelas Uji == Kelas Runnner
def cek1(kelas_winner, kelas_runner):
    print('kelas winner: ', kelas_winner)
    print('kelas runner: ', kelas_runner)
    return True if kelas_winner != kelas_runner else False #cek 1

#Pengecekan kondisi if dc/dr > 1-epsilon AND dr/dc < 1+epsilon
def cek234(distance, epsilon = 0.35):
    dc = min(distance)
    dr = max(distance)
    dcdr = True if dc/dr > 1 - epsilon else False #cek 2
    drdc = True if dr/dc < 1 + epsilon else False #cek 3
    return True if dcdr == True and drdc == True else False #cek 4
#Pengecekan kondisi if Kelas Uji == Kelas
def cek5(kls_uji, kls_runner):
    return True if kls_uji == kls_runner else False

# Update Semua Bobot
def updateSemua(alfa, kelas_w, kelas_winner, kelas_runner, kelas_uji, w, x, distance):
    kondisi = cek1(kelas_winner,kelas_runner) and cek234(distance) and cek5(kelas_uji,kelas_runner) 
    print('Pengecekan Syarat[Cek 1 & Cek23]:\nCek 1 | Cek 234 | Cek 5 |',)
    top2Distance=[distance[0],distance[1]]
    print('Kelas uji: ',kelas_uji)
    print('%-6s|%-8s|%-7s|' % (cek1(kelas_uji,kelas_runner), cek234(top2Distance), cek5(kelas_uji,kelas_runner)))
    if kondisi==True :
        print('Update Bobot BMU dan Runner-Up:')
        if kelas_winner == kelas_w[0]:
            w = updateBobotRunnerV2(x, w, alfa, kelas_uji, kelas_w, kelas_winner)
    else:
        print('Update Bobot BMU saja:')
        w[0] = updateBobotPemenang(x, w[0], alfa, kelas_uji, kelas_w[0])
    return w

#Proses Main 
def Main():
    epoch = 0
    alfa=0.1
    treshold=0.001
    dt,kls = ReadData()
    w = np.array([[0.755,0.551,0.288,0.302,0.885,0.489], [0.937,0.255,0.054,0.162,0.951,0.239], [0.639,0.395,0.472,0.761,0.768,0.407]])
    print ('Bobot Awal [w1][w2]: ', w[0], w[1], w[2], '\nAlfa: ', alfa, '\nThreshold: ', treshold)
    kls_a = np.array([1,2,3])
    while(alfa > treshold):
        print('==================================')
        print('           EPOCH ke-',epoch+1)
        print('==================================')
        for i in range(len(dt)-1):
            x = dt[i]
            distance = jarakEuc(w, x)
            print('Data [%-d]\nInput x[%-d]: ' % (i+1, i+1))
            print(w)
            print('Distance: ', distance)
            distance, w, kls_winner = sorting(distance, w, kls_a)
            print('Kelas winner: ', kls_winner, distance)
            print('Input setelah Sorting: \n',w)
            print(kls[i])
            w = updateSemua(alfa, kls_a, kls_winner[0], kls_winner[1], kls[i], w, x, distance)
            print(w)
            print()
        epoch += 1
        alfa = 0.5 * alfa
        
    print('=======================================')
    print('             TESTING')
    print('=======================================')
    x_testing ,x_kelas= ReadDataTest() 
    print('Nilai Bobot: ', w)
    # x_testing = [0.3, 0.1, 0.4, 0.6, 0.2, 0.5]
    benar = 0
    for i in range(len(x_testing)):
        x2 = x_testing[i]
        jarak = jarakEuc(w, x2)
        print('Data [%-d]\nInput x[%-d]: ' % (i+1, i+1))
        print(w)
        print('Distance: ', jarak)
        jarak, w, kls_win = sorting(jarak, w, kls_a)   
        print('Kelas winner: ', kls_win, jarak)
        print('Hasil klasifikasi => ', kls_win[0])
        print('Kelas Asli => ',x_kelas[i])
        if kls_win[0] == x_kelas[i]:
            benar+=1
    akurasi =(float(benar)/len(x_testing))*100
    print('Akurasi = ',akurasi,'%')
if __name__ == '__main__':
    Main()



    