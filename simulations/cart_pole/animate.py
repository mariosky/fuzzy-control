
# Contributed by Everton Colling to ApMonitor Site
# Code from: https://apmonitor.com/do/index.php/Main/InvertedPendulum

# The cart pole model considers the up position in theta = pi and down position in tetha = 0
import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def animate_simulation(result_odeint, t):
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

    plt.rcParams['animation.html'] = 'html5'

    x1 =result_odeint[:,0]
    y1 = np.zeros(len(t))

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

    ani_a = animation.FuncAnimation(fig, animate, \
         np.arange(1,len(t)), \
         interval=40,blit=False,init_func=init)
    plt.show()



