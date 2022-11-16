import numpy as np
from scipy.integrate import odeint 
from numpy import linalg as LA
import matplotlib.pyplot as plt
import control 
from plots import plot_cart
from animate import animate_simulation

# cart model from:
# book{brunton2022data,
#  title={Data-driven science and engineering: Machine learning, dynamical systems, and control},
#  author={Brunton, Steven L and Kutz, J Nathan},
#  year={2022},
#  publisher={Cambridge University Press}
# }


def cart(t, state, p, uf):
    x, v, th, om = state
    u = uf(state)

    m, M, L, g, d = p
    Sth = np.sin(th)
    Cth = np.cos(th)
    D = m*L*L*(M+m*(1-Cth**2))
    
    dx = v
    dv = (1/D)*(-(m**2)*(L**2)*g*Cth*Sth + m*(L**2)*(m*L*(om**2)  *Sth - d*v   )) + m*L*L*(1/D)*u
    dth = om
    dom = (1/D)*((m+M)*m*g*L*Sth - m*L*Cth*(m*L*(om**2)*Sth - d*v)) -     m*L*Cth*(1/D)*u

    return [dx, dv, dth, dom]


m = 1.0
M = 5.0
L = 2.0 
g = -10.0
d = 10.0 


p = m, M, L, g, d

x = -1.0
v = 0.0  
th = np.pi + 0.1
om = 0.0 

state = [x, v, th, om]  # Initial state of the system

u = 0.0 

t = np.arange(0.0, 10.0, 0.01)


b = 1 # pendulum up

A = np.array(  [[0, 1, 0, 0],
                [0, -d/M, b*m*g/M, 0],
                [0, 0, 0, 1],
                [0, -b*d/(M*L), -b*(m+M)*g/(M*L), 0]]
            )

B = np.array([0, 1/M,  0, b/(M*L)]).reshape(4,1)
Q = np.array([[1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1]]) 
R = 0.0001
K, S, E = control.lqr(A, B, Q, R)
#print(A, A.shape) 
#print(B, B.shape)
w, v = LA.eig(A)
print(w)
print(LA.matrix_rank(control.ctrb(A,B)))


#eigs = [-.3, -.4, -.5, -.6]
#K = control.place(A,B,eigs)
print('K', K)

# result_odeint = odeint(cart, state, t, args=(p, u ), tfirst=True)
# print(result_odeint[:10])
result = []
result.append(state)

wr = np.array([1, 0, np.pi, 0 ])
uf = lambda x : -K@(x-wr) 

result_odeint = odeint(cart, state, t, args=(p, uf ), tfirst=True)
#for i in range(len(t)-1):
#    result_odeint = odeint(cart, state, [0,0.1], args=(p, uf ), tfirst=True)
#    state = result_odeint[1]
#    result.append(list(state))
    #u = -K * (np.array(state )-np.array([1, 0, np.pi, 0 ]))
    # print(u)
result = result_odeint
# print(np.array(result[:10]))

plot_labels = ('x','v','theta','omega')
[plt.plot(t,result[:,j],linewidth=2,label=plot_labels[j]) for j in range(4)]
plt.xlabel('Time')
plt.ylabel('State')

plt.legend()

plot_cart(np.array(result), plt, t)
animate_simulation(np.array(result), t)


