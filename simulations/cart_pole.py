import numpy as np
from scipy.integrate import odeint 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



# cart model from:
# book{brunton2022data,
#  title={Data-driven science and engineering: Machine learning, dynamical systems, and control},
#  author={Brunton, Steven L and Kutz, J Nathan},
#  year={2022},
#  publisher={Cambridge University Press}
# }


def cart(t, state, p, u):
    x, v, th, om = state
    m, M, L, g, d = p
    Sth = np.sin(th)
    Cth = np.cos(th)
    D = m*L**2*(M + m*(1-Cth**2))
    
    dx = v
    dv = (1/D)*(-m**2*L**2*g*Cth*Sth + m*L**2*(m*L*om**2*Sth - d*v) + m*L*L*u)
    dth = om
    dom = (1/D)*((m+M)*m*g*L*Sth - m*L*Cth*(m*L*om**2*Sth - d*v) + m*L*Cth*u)
    return [dx, dv, dth, dom]


m = 1.0
M = 5.0
L = 2.0 
g = -10.0
d = 10.0 


p = m, M, L, g, d

x = 0.0 
v = 0.0  
th = np.pi - 0.5
om = 0.0 

state = [x, v, th, om]  # Initial state of the system

u = 0.0 

t_span = (0.0, 100.0)
t = np.arange(0.0, 100.0, 0.01)
 
result_odeint = odeint(cart, state, t, args=(p, u ), tfirst=True)

import matplotlib.pyplot as plt
plt.figure(figsize=(12,10))


plt.subplot(222)
plt.plot(t,result_odeint[:,1],'g',lw=2)
plt.legend([r'$v$'],loc=1)
plt.ylabel('Velocity')
plt.xlabel('Time')
plt.xlim(t[0],t[-1])


plt.subplot(223)
plt.plot(t,result_odeint[:,0] ,'r',lw=2)
plt.legend([r'$x$'],loc=1)
plt.ylabel('Position')
plt.xlabel('Time')
plt.xlim(t[0],t[-1])

plt.subplot(224)
plt.plot(t,result_odeint[:,2],'y',lw=2)
#plt.plot(t,qa.value,'c',lw=2)
plt.legend([r'$\theta$'],loc=1)
#plt.legend([r'$\theta$',r'$q$'],loc=1)
plt.ylabel('Angle')
plt.xlabel('Time')
plt.xlim(t[0],t[-1])

# Contributed by Everton Colling
# Code from: https://apmonitor.com/do/index.php/Main/InvertedPendulum

# The model obove considers the up position in theta = pi and down position in tetha = 0

import matplotlib.animation as animation
plt.rcParams['animation.html'] = 'html5'

x1 =result_odeint[:,0]
y1 = np.zeros(len(t))

#suppose that l = 1
x2 = 1*np.sin(result_odeint[:,2])+x1
x2b = 1*np.sin(result_odeint[:,2])+x1
y2 = -1*np.cos(result_odeint[:,2])-y1
y2b = -1*np.cos(result_odeint[:,2])-y1

fig = plt.figure(figsize=(8,6.4))
ax = fig.add_subplot(111,autoscale_on=False,\
                     xlim=(-1.8,1.8),ylim=(-1.8,1.8))
ax.set_xlabel('position')
ax.get_yaxis().set_visible(False)

crane_rail, = ax.plot([-1.8,1.8],[-0.22,-0.22],'k-',lw=2)
#start, = ax.plot([-1,-1],[-1.5,1.5],'k:',lw=2)
#objective, = ax.plot([0,0],[-0.5,1.5],'k:',lw=2)
mass1, = ax.plot([],[],linestyle='None',marker='s',\
                 markersize=40,markeredgecolor='k',\
                 color='red',markeredgewidth=1)
mass2, = ax.plot([],[],linestyle='None',marker='o',\
                 markersize=12,markeredgecolor='k',\
                 color='black',markeredgewidth=2)
line, = ax.plot([],[],'o-',color='black',lw=3,\
                markersize=6,markeredgecolor='k',\
                markerfacecolor='k')
time_template = 'time = %.1fs'
time_text = ax.text(0.05,0.9,'',transform=ax.transAxes)
#start_text = ax.text(-1.06,-0.3,'start',ha='right')
#end_text = ax.text(0.06,-0.3,'objective',ha='left')

def init():
    mass1.set_data([],[])
    mass2.set_data([],[])
    line.set_data([],[])
    time_text.set_text('')
    return line, mass1, mass2, time_text

def animate(i):
    mass1.set_data([x1[i]],[y1[i]])
    mass2.set_data([x2b[i]],[y2b[i]])
    line.set_data([x1[i],x2[i]],[y1[i],y2[i]])
    time_text.set_text(time_template % t[i])
    return line, mass1, mass2, time_text

ani_a = animation.FuncAnimation(fig, animate, \
         np.arange(1,len(t)), \
         interval=40,blit=False,init_func=init)

#plt.plot(t, result_odeint[:,0])
plt.show()


