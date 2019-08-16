#!/usr/bin/env python
# coding: utf-8

# In[22]:


import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Epsilon Greedy 
class Bandit_eps:
#     print("Bandit")
    def __init__(self,m):
        self.m = m
        self.mean = 0
        self.N = 0
        
    def pull(self):
        return np.random.randn() + self.m
    
    def update(self,x):
        self.N += 1
        self.mean = (1-(1.0/self.N))*self.mean + (1.0/self.N)*x


        
# Comparing three different bandits    
def run_eps(m1,m2,m3,eps,N):
    print("epsilon greedy")
    bandits_eps = [Bandit_eps(m1), Bandit_eps(m2), Bandit_eps(m3)]
        
    data = np.empty(N)
        
#       choosing exploit or explore based on epsilon value
    for i in range(N):
        p=np.random.random()
        if p < eps:
#              explore
            j=np.random.choice(3) 
        else:
#               exploit
            j=np.argmax([b.mean for b in bandits_eps])
        x=bandits_eps[j].pull()
        bandits_eps[j].update(x)
    
       # for the plot

        data[i] = x
    cumulative_average = np.cumsum(data) / (np.arange(N) + 1)



  # plot moving average ctr

#     matplotlib.rcParams['figure.figsize'] = [80, 80]
    
    plt.plot(cumulative_average)
    plt.plot(np.ones(N)*m1)
    plt.plot(np.ones(N)*m2)
    plt.plot(np.ones(N)*m3)

    plt.xscale('log')
    plt.show()
    
    
    for b in bandits_eps:
        print(b.mean)

    return cumulative_average

    
    
    
# Optimistic Initial Value
class Bandit_oiv:
#     print("Bandit")
    def __init__(self,m, upper_limit):
        self.m = m
        self.mean = upper_limit
        self.N = 1
        
    def pull(self):
#         print("pull")
        return np.random.randn() + self.m
    
    def update(self,x):
        self.N += 1
        self.mean = (1-(1.0/self.N))*self.mean + (1.0/self.N)*x
        
                
# Comparing three different bandits    
def run_oiv(m1,m2,m3,N, upper_limit=10):
    print("optimistic value")
    bandits_oiv = [Bandit_oiv(m1, upper_limit), Bandit_oiv(m2, upper_limit), Bandit_oiv(m3, upper_limit)]
        
    data = np.empty(N)
        
#       choosing exploit or explore based on epsilon value
    for i in range(N):
        j=np.argmax([b.mean for b in bandits_oiv])
        x=bandits_oiv[j].pull()
#         print(x)
        bandits_oiv[j].update(x)
    
       # for the plot

        data[i] = x
        cumulative_average = np.cumsum(data) / (np.arange(N) + 1)



  # plot moving average ctr

#     matplotlib.rcParams['figure.figsize'] = [80, 80]
    plt.plot(cumulative_average)
    plt.plot(np.ones(N)*m1)
    plt.plot(np.ones(N)*m2)
    plt.plot(np.ones(N)*m3)

    plt.xscale('log')
    plt.show()
    
    for b in bandits_oiv:
        print(b.mean)

    return cumulative_average
    
    
# UCB1
class Bandit_ucb:
#     print("Bandit")
    def __init__(self,m):
        self.m = m
        self.mean = 0
        self.N = 0
        
    def pull(self):
#         print("pull")
        return np.random.randn() + self.m
    
    def update(self,x):
        self.N += 1
        self.mean = (1-(1.0/self.N))*self.mean + (1.0/self.N)*x
        
                

def ucb(mean, n, nj):

    if nj == 0:
        return float('inf')
    return mean + np.sqrt(2*np.log(n) / nj)


            
# Comparing three different bandits    
def run_ucb(m1,m2,m3,N):
    print("UCB1")
    bandits_ucb = [Bandit_ucb(m1), Bandit_ucb(m2), Bandit_ucb(m3)]
        
    data = np.empty(N)
        
#       choosing exploit or explore based on epsilon value
    for i in range(N):
        j=np.argmax([ucb(b.mean, i+1, b.N) for b in bandits_ucb])
        x=bandits_ucb[j].pull()
#         print(x)
        bandits_ucb[j].update(x)
    
       # for the plot

        data[i] = x
        cumulative_average = np.cumsum(data) / (np.arange(N) + 1)



  # plot moving average ctr

#     matplotlib.rcParams['figure.figsize'] = [80, 80]
    plt.plot(cumulative_average)
    plt.plot(np.ones(N)*m1)
    plt.plot(np.ones(N)*m2)
    plt.plot(np.ones(N)*m3)

    plt.xscale('log')
    plt.show()
    
    for b in bandits_ucb:
        print(b.mean)

    return cumulative_average
    


if __name__ == '__main__':
    c_1=run_eps(1.0,2.0,3.0,0.1,100000)
    c_2=run_eps(1.0,2.0,3.0,0.05,100000)
    c_3=run_eps(1.0,2.0,3.0,0.01,100000)
    
    
    oiv1=run_oiv(1.0,2.0,3.0,100000)
    
    ucb = run_ucb(1.0, 2.0, 3.0, 100000)
    # log scale plot

#     matplotlib.rcParams['figure.figsize'] = [50, 50]
    print("log scale plots")
    plt.plot(c_1, label='eps = 0.1')

    plt.plot(c_2, label='eps = 0.05')

    plt.plot(c_3, label='eps = 0.01')

    plt.plot(oiv1, label='optimistic')

    plt.plot(ucb, label='ucb')
    
    plt.legend()

    plt.xscale('log')

    plt.show()





      # linear plot

#     matplotlib.rcParams['figure.figsize'] = [40, 50]
    print ("linear plots")
    plt.plot(c_1, label ='eps = 0.1')

    plt.plot(c_2, label ='eps = 0.05')

    plt.plot(c_3, label ='eps = 0.01')
    
    plt.plot(oiv1, label ='optimistic')
    
    plt.plot(ucb, label='ucb')

    plt.legend()

    plt.show()


    
#       # log scale plot

#     plt.plot(eps, label='decaying-epsilon-greedy')

#     plt.plot(oiv, label='optimistic')

#     plt.plot(ucb, label='ucb1')

#     plt.plot(bayes, label='bayesian')

#     plt.legend()

#     plt.xscale('log')

#     plt.show()





#   # linear plot

#   plt.plot(eps, label='decaying-epsilon-greedy')

#   plt.plot(oiv, label='optimistic')

#   plt.plot(ucb, label='ucb1')

#   plt.plot(bayes, label='bayesian')

#   plt.legend()

#   plt.show()


# In[ ]:




