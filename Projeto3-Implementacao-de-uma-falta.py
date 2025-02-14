
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 09:16:04 2016

@author: Carlosjunior
"""

#imports
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from numpy import linspace 
from numpy import linalg 
from numpy import multiply 
from numpy import cross
import math
import matplotlib.font_manager as font_manager

title_font = {'fontname':'Helvetica', 'size':'16', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'} # Bottom vertical alignment for more space
axis_font = {'fontname':'Helvetica', 'size':'14'}


ax = plt.subplot() # Defines ax variable by creating an empty plot



# Set the tick labels font
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')
    label.set_fontsize(13)

#constantes
#p = 0.25
#p = 0.25
#r = 35 * 10 ** -2 #m
#Area = 4 * math.pi * r ** 2 #m2
#g = 10 # m/s**2
#m = 430 * 10 ** -3 #kg
#s = 200 #rpm
def gra_rad(teta):
    ang = teta * math.pi/180
    return ang

def forca_drag(V,r,Area): # V = [vx,vy,vz]
    v = linalg.norm(V)
    
    v_versor =  V/v
    
    f_c =  p * Area * v**2 / 2
    
    f = multiply(f_c, - v_versor)
    
    return f
    
def forca_magnus(V): #V = [vx,vy,vz]
    v = linalg.norm(V)
    
    v_versor = V/v
    w = [0,0,1]
    
    versor = cross(w,v_versor)
    f_d = (4/3)* (4 *math.pi * r ** 3 * p * v * s)
    
    f = multiply(f_d, versor)
    
    return f
    

def func(A,t): #A=[x,y,z,vx,vy,vz]
    dxdt = A[3]
    dydt = A[4]
    dzdt = A[5]
    V = [A[3],A[4],A[5]]
    
    Fmagnus = forca_magnus(V)
    Fdrag = forca_drag(V,r,Area)
    
    dvxdt = (Fdrag[0]/m) + (Fmagnus[0]/m) 
    dvydt =   (Fmagnus[1]/m) + (Fdrag[1]/m)
    dvzdt = -g + (Fdrag[2]/m)
    return [dxdt,dydt,dzdt,dvxdt,dvydt,dvzdt]


#Dados para a validacao

td = [
0.03,
0.1,
0.17,
0.23,
0.3, 
0.33,
0.4,
0.47,  
0.53, 
0.57,
0.63, 
0.67,
0.73, 
0.8, 
0.83, 
0.9, 
0.93, 
1.0,  
1.07,
1.13, 
1.2,  
1.27, 
1.3,  
1.37,
1.43]

yr = [
0.0,
1.5883896,
3.0648432,
4.375156,
5.5216794,
6.3948293,
7.4329443,
8.308446,
9.070835,
9.883902,
10.537882,
11.462885,
12.330155,
13.960992,
14.825911,
15.799239,
16.665335,
17.419493,
18.604935,
19.631292,
20.710678,
21.570894,
22.37573,
23.072157,
23.931196,
]



xr = [
0.0,
0.15137841,
0.2297927,
0.2813985,
0.3781544,
0.39347926,
0.44609067,
0.50716895,
0.52209157,
0.52894956,
0.55274135,
0.59427136,
0.6079873,
0.61323637,
0.61021966,
0.5781822,
0.52780324,
0.48709777,
0.4473979,
0.4070947,
0.3575201,
0.28980508,
0.24103497,
0.16424969,
0.10560489,
]

#for a in td:
#    yr.append(float("{0:.2f}".format(a)))
#print(len(td),len(xr))
#Constantes
p = 0.25
r = 0.11 #m
Area = 4 * math.pi * r ** 2 #m2
g = 9.8 # m/s**2
m = 430 * 10 ** -3 #kg 430
s = 11 #Hz

#Valores iniciais
teta = gra_rad(15)
#teta = 0.295765
v0 = 30#30.48
vx = 2.5
vy = v0 * math.cos(teta)#2.6565
vz = v0 * math.sin(teta)#30.640
x = 0
y = 0
z = 0
V = [vx,vy,vz]


#Implementação
Y0 = [x,y,z,vx,vy,vz]
T = linspace(0,1.4,16)
y0 = odeint(func,Y0,T)


#Listas dos Espaços e Velocidade
velocidade = []
Sz = y0[:,2]
Sy = []
Sx = y0[:,0]
velz = y0[:,5]
vely = y0[:,4]
velx = y0[:,3]

for i in range(len(Sx)):
    velocidade.append(math.sqrt(y0[:,3][i]**2 + y0[:,4][i]**2 +y0[:,5][i]**2))

  
#======================Gráfico da posicao de y por z==============================================    

plt.plot(y0[:,0], y0[:,2],'o',color = 'black')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1),fontsize = 14)
plt.title('Visão do Roberto Carlos',**title_font)
plt.xlabel('Espaço x[m]',**axis_font)
plt.ylabel('Espaço z[m]',**axis_font)
plt.axis([0,0.7,0,2])


plt.grid()
plt.show()



#======================Gráfico da posicao de y por x==============================================    
#for i in range(len(Sx)):
#    print("({0},{1})".format(Sx[i],Sy[i]))
# Set the font dictionaries (for plot title and axis titles)



plt.plot(y0[:,1],y0[:,0],'o',color = 'black')
plt.plot(yr,xr,'o',color = 'y',label = 'Bola real')
plt.legend(loc='upper right', bbox_to_anchor=(1.39, 1.1),fontsize = 14)
plt.title('Visão de cima do campo',**title_font)
plt.xlabel('Espaço y[m]',**axis_font)
plt.ylabel('Espaço x[m]',**axis_font)

plt.grid()
plt.show()

#======================Gráfico da posicao z por x==============================================
plt.plot(y0[:,1], y0[:,2],'o',color = 'black',label = 'Bola implementação')
#plt.plot(xr,zr,'o',color = 'blue',label = 'Bola real')
plt.legend(loc='upper right', bbox_to_anchor=(1.45, 1.1),fontsize = 14)
plt.title('Visão do banco de reservas',**title_font)
plt.xlabel('Espaço y[m]',**axis_font)
plt.ylabel('Espaço z[m]',**axis_font)
#plt.axis([-0.15,25,-0.15,2.5])

plt.grid()
plt.show()

#======================Gráfico da posicao x, y e z==============================================

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(y0[:,0], y0[:,1], y0[:,2], label='Movimento da bola',marker = 'o',color = 'black')
ax.set_xlabel('Posição em x',**axis_font)
ax.set_ylabel('Posição em y',**axis_font)
ax.set_zlabel('Posicção em z',**axis_font)
ax.legend()

plt.show()

#======================Gráfico da posicao de y pelo tempo==============================================
plt.plot(T,y0[:,1],'-',label = 'Posição em y',c='y')
plt.plot(td,yr,'o',color = 'blue',label = 'Posição y da bola real')
plt.legend(loc='upper right', bbox_to_anchor=(1.55, 1.1),fontsize = 14)
plt.title('Gráficos das posições em y',**title_font)
plt.xlabel('Tempo[s]',**axis_font)
plt.ylabel('Espaço[m]',**axis_font)

plt.grid()
plt.show()


#======================Gráfico da posicao de x  pelo tempo==============================================
plt.plot(T,y0[:,0],'-',label = 'Posição em x',c='red')
plt.plot(td,xr,'o',color = 'blue',label = 'Posição x da bola real')
plt.legend(loc='upper right', bbox_to_anchor=(1.55, 1.1),fontsize = 14)
plt.title('Gráficos das posições em x',**title_font)
plt.xlabel('Tempo[s]',**axis_font)
plt.ylabel('Espaço[m]',**axis_font)

plt.grid()
plt.show()

#======================Gráfico da posicao de z  pelo tempo==============================================
plt.plot(T,y0[:,2],'-',label = 'Posição em z',c='green')
#plt.plot(td,zr,'o',color = 'blue',label = 'Posição z da bola real')
plt.legend(loc='upper right', bbox_to_anchor=(1.45, 1.1),fontsize = 14)
plt.title('Gráficos das posições em z',**title_font)
plt.axis([0,1.4,0,2])
plt.xlabel('Tempo[s]',**axis_font)
plt.ylabel('Espaço[m]',**axis_font)

plt.grid()
plt.show()


#======================Gráfico da posicao de v pelo tempo==============================================
plt.plot(T,velocidade,'-',label = 'Velocidade',c='black')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1),fontsize = 14)
plt.title('Gráficos das velocidades',**title_font)
plt.xlabel('Tempo[s]',**axis_font)
plt.ylabel('Velocidade[m/s]',**axis_font)


plt.grid()
plt.show()

#======================Gráfico da posicao de vx pelo tempo==============================================
plt.plot(T,y0[:,3],'-',label = 'Velocidade em x',c='r')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1),fontsize = 14)
plt.title('Gráficos das velocidades em x',**title_font)
plt.xlabel('Tempo[s]',**axis_font)
plt.ylabel('Velocidade[m/s]',**axis_font)


plt.grid()
plt.show()

#======================Gráfico da posicao de vz pelo tempo==============================================
plt.plot(T,y0[:,5],'-',label = 'Velocidade em z',c='green')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1),fontsize = 14)
plt.title('Gráficos das velocidades em z',**title_font)
plt.xlabel('Tempo[s]',**axis_font)
plt.ylabel('Velocidade[m/s]',**axis_font)


plt.grid()
plt.show()


#======================Gráfico da posicao de v e vy pelo tempo==============================================
#plt.plot(T,velocidade,'-',label = 'Velocidade')
plt.plot(T,y0[:,4],'-',label = 'Velocidade em y',c='y')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1),fontsize = 14)
plt.title('Gráficos das velocidades em y',**title_font)
plt.xlabel('Tempo[s]',**axis_font)
plt.ylabel('Velocidade[m/s]',**axis_font)

plt.grid()
plt.show()

#__________________________________________________________________________________________________________




#======================Figura de mérito==============================================
def rad_gra(teta):
    ang=180*teta/math.pi
    return ang
merito = []
merito.append(max(Sz))
merito2 = []
merito2.append(max(Sx))
tetas = []
#teta = gra_rad(16.5)
ang = rad_gra(teta)
tetas.append(ang)
#tetas.append(teta)
for i in range(1,10):
    teta -= math.pi * 0.5/180
    
    v0 = 31.48
    vx = 2.7
    vy = v0 * math.cos(teta)#2.6565
    vz = v0 * math.sin(teta)#30.640
    x = 0
    y = 0
    z = 0
    V = [vx,vy,vz]
    ang = rad_gra(teta)
    tetas.append(ang)
    
    #Implementação
    Y0 = [x,y,z,vx,vy,vz]
    T = linspace(0,1.3,16)
    y = odeint(func,Y0,T)
    
    
    #Listas dos Espaços e Velocidade
    velocidade = []
    Sz = y[:,2]
    Sy = y[:,1]
    Sx = y[:,0]
    velz = y[:,5]
    vely = y[:,4]
    velx = y[:,3]
    
    for i in range(len(Sx)):
        velocidade.append(math.sqrt(y[:,3][i]**2 + y[:,4][i]**2 +y[:,5][i]**2))
    merito.append(max(Sz))
    merito2.append(max(Sy))

for i in range(len(merito)):
    if tetas[i]<=13.5:
        print(merito[i])
    if merito[i] >= 1.8:
        print(tetas[i])
        
        

plt.plot(tetas,merito,'o',label = '',c = 'r')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1),fontsize = 14)
plt.title('Gráficos da altura máxima da bola',**title_font)
plt.xlabel('ângulo [graus]',**axis_font)
plt.ylabel('Altura máxima[m]',**axis_font)
plt.axis([10,14.5,0,2])

plt.grid()
plt.show()
    
plt.plot(tetas,merito2,'o',label = '',c = 'g')
plt.legend(loc='upper right', bbox_to_anchor=(1.13, 1.1),fontsize = 14)
plt.title('Gráficos da distância máxima da bola',**title_font)
plt.xlabel('ângulo [º]',**axis_font)
plt.ylabel('Espaço[m]',**axis_font)
plt.axis([0,25,22.6,23.2])

plt.grid()
plt.show()
    
