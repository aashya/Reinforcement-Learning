#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
import matplotlib.pyplot as plt
import import_ipynb
from grid_world import standard_grid, negative_grid
from Iterative_Policy import print_values, print_policy

small_enough = 10e-4
gamma = 0.9
all_possible_actions = ('U', 'D', 'L', 'R')

def play_game(grid, policy):
	start_states = list(grid.actions.keys())
	#starting at a random state so that we can visit all states -- called the exploring starts method
	start_idx = np.random.choice(len(start_states)) 
	grid.set_state(start_states[start_idx])
# 	print (start_idx)
	
	s = grid.current_state(start_idx)
	states_and_rewards = [(s,0)]
	while not grid.game_over():
		a = policy[s]
		r = grid.move(a)
        
		s = grid.current_state(s)
		states_and_rewards.append((s,r))
		
	G=0
	states_and_returns =[]
	first = True
	for s,r in reversed(states_and_rewards):
		if first:
			first = False
		else:
			states_and_returns.append((s,G))
		G = r + gamma*G
            
	states_and_returns.reverse()
	return states_and_returns
	
	
if __name__ == '__main__':
	
	grid = standard_grid()
	print ("rewards")
	print_values(grid.rewards, grid)

	
	policy = {
		(2, 0): 'U',

		(1, 0): 'U',

		(0, 0): 'R',

		(0, 1): 'R',

		(0, 2): 'R',

		(1, 2): 'R',

		(2, 1): 'R',

		(2, 2): 'R',

		(2, 3): 'U',

	}
	
	V= {}
	returns = {}
	states = grid.all_states()
	for s in states:
		if s in grid.actions:
			returns[s] = []
		else: 
			V[s] = 0
			
			
	for t in range(100):
		states_and_returns = play_game(grid, policy)
		seen_states = set()
		for s, G in states_and_returns:
# 			print ("G")
# 			print (G)

			if s not in seen_states:
				returns[s].append(G)
				V[s] = np.mean(returns[s])
				seen_states.add(s)
	
	print ("Values")
	print_values(V,grid)
	print ("Policy")
	print_policy(policy,grid)


# In[ ]:





# In[ ]:




