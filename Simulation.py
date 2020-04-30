import matplotlib
matplotlib.use('Tkagg')
import numpy as np 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

W = np.zeros((16))
T1 = np.zeros((16))
T2 = np.zeros((16))
for i in range(8):
    W[i]= 128
    T1[i]= 0.075*0.5
    T2[i]= 0.04*0.5
for i in range(8,16):
    W[i]= 128
    T1[i]= 0.15*0.5
    T2[i]= 0.075*0.5
rand = np.random.randint(low=1 ,high=20 ,size= 16)

map = plt.figure()
map_ax = Axes3D(map)
map_ax.autoscale(enable=True, axis='both', tight=True)
map_ax.set_xlim3d([-0.5,9])
map_ax.set_ylim3d([-0.5,9])
map_ax.set_zlim3d([-0.5,2.5])
 
color = [['b' ,'g','r'] , [ 'Oil','Water' ,'BulkVector'] ]
patch =[]
for i in range(3):
    patch.append(mpatches.Patch(color=color[0][i], label=color[1][i]))
    
plt.legend(handles=patch)



def get_parameters():    
    
    uniformity = int(input("if you want to add nonuniformity effect enter 1 else 2:"  ))
    
    return uniformity

def update_line(hl,h2, loc,new_data,de=False):
    
    if de == False :         
        xdata, ydata, zdata = hl._verts3d
        hl.set_xdata(list(np.append(xdata, new_data[0])))
        hl.set_ydata(list(np.append(ydata, new_data[1])))
        hl.set_3d_properties(list(np.append(zdata, new_data[2])))
        
    #  	xdata1, ydata1, zdata1 = h2._verts3d
        h2.set_xdata(list([loc[0], new_data[0]]))
        h2.set_ydata(list([loc[1],new_data[1]]))
        h2.set_3d_properties(list([0, new_data[2]]))
        plt.draw()       
    



 

def excitation(h2,location_x,location_y):
    t = 0    
    x =location_x
    y =location_y
    while (y[0]< 2 ):
		#My
        y = np.add([1*np.sin(2*np.pi*t)]*16,location_y)               
		#Mz 
        z= [1*np.cos(2*np.pi*t)]*16
        for i in range(16):
            loc =[location_x[i],location_y[i]]
            update_line(h1[i], h2[i] ,loc, (x[i],y[i], z[i]))
        t= t + 0.05
        plt.show(block=False)
        plt.pause(0.00000001)
	    
    return h2

def relaxation(special_encoding,h2,h1,location_x,location_y):
    
    x=[0]*16
    y=[0]*16
    z=[0]*16
    t=0
    print(5)
    while (np.max(z )< 0.75): 
        print(4)
		#Mx = 2*np.exp(t/T2) np.sin(W*t)
        x = np.add(1*(np.exp(-1*(t/T2)))*np.sin(2*np.pi*np.add(W,special_encoding)*t) , location_x)

		#My = 2*np.exp(t/T2) np.cos(W*t)
        y =np.add(1*(np.exp(-1*(t/T2)))*np.cos(2*np.pi* np.add(W,special_encoding)*t),location_y)
        
		#Mz = 10*(1 -np.exp(t/T1))
        z= 1*(1- np.exp(-1*(t/T1)))

		#ax.plot([0,1],[0,1] ,[0,1], zdir='z')
        for i in range(16):
            loc =[location_x[i],location_y[i]]
            update_line(h1[i] , h2[i] ,loc, (x[i],y[i], z[i]))
        t= t + 0.0002
        plt.show(block=False)
        plt.pause(0.00000001)
 
h1=[]
h2=[]
location_x =[1,1,1,1,3,3,3,3,5,5,5,5,7,7,7,7]
location_y =[1,3,5,7,1,3,5,7,1,3,5,7,1,3,5,7]
#get parameter

add_random = get_parameters() %2

#### Simultion 
#Calculate Freq encoding Gradient        
Freq_Encoding = np.zeros((16))
freq_step =2*np.pi/3
freq= 0
for p in range(4):
    for l in range(4):
        Freq_Encoding[p + 4*l] = Freq_Encoding[p + 4*l] + freq
    freq += freq_step

for i in range(4):
    #Prepare to draw oil spins
    for k in range(8):
       if i !=0:
           h1[k].set_visible(False)
           h2[k].set_visible(False)
       h2_temp ,  = map_ax.plot3D([location_x[k]], [location_y[k]], [0],'r') 
       h1_temp ,  = map_ax.plot3D([location_x[k]], [location_y[k]], [1],'b')
       if i==0:
           h1.append(h1_temp)
           h2.append(h2_temp)
       else:
           h1[k]=h1_temp
           h2[k]=h2_temp
   #Prepare to draw water spins
    for k in range(8,16):
        
        if i !=0:
           h1[k].set_visible(False)
           h2[k].set_visible(False)
        h2_temp ,  = map_ax.plot3D([location_x[k]], [location_y[k]], [0],'r') 
        h1_temp ,  = map_ax.plot3D([location_x[k]], [location_y[k]], [1],'g')
        if i==0:
           h1.append(h1_temp)
           h2.append(h2_temp)
        else:
           h1[k]=h1_temp
           h2[k]=h2_temp
    #Calc phase encoding gradient       
    Phase_Encoding = np.zeros((16))
    max_phase = (i+1)*np.pi/(4)
    step_phase = 2*max_phase/3
    phase = -1*max_phase
        
    for j in range(4):
        phase += step_phase  
        for o in range(4):
            Phase_Encoding[o +4*j] = Phase_Encoding[o +4*j] + phase
    #Start    
    special_encoding = (Freq_Encoding  + Phase_Encoding )*10 +rand*add_random 
    plt.title(f"K-space ROW NO {i+1}")
    h3 =excitation(h2,location_x,location_y)
    relaxation( special_encoding , h3,h1,location_x,location_y)



 
plt.show(block=True)




