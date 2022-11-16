

def plot_cart(result_odeint, plt, t):
    plt.figure(figsize=(12,10))

    plt.subplot(221)
    plt.plot(t,result_odeint[:,3],'b',lw=2)
    plt.legend([r'$v$'],loc=1)
    plt.ylabel('Force')
    plt.xlabel('$u$')
    plt.xlim(t[0],t[-1])

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

