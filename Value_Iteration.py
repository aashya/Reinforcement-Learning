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

if __name__ == '__main__':
	
	# maximizing reward only, the goal is not to reach the final destination set by us
	grid = negative_grid()
	print ("rewards")
	print_values(grid.rewards, grid)

	policy = {}
	for s in grid.actions.keys():
		policy[s] = np.random.choice(all_possible_actions)
	
	print ("Initial Policy")
	print_policy(policy, grid)
	
	V= {}
	states = grid.all_states()
	for s in states:
		if s in grid.actions:
			V[s] = np.random.random()
		else:
			V[s] = 0


	while True:
		biggest_change = 0
		for s in states:
			old_v = V[s]
				
			if s in policy:
				#checking which side the agent is going, i.e. which policy it adhears to
				#setting the policy value as per defined
				new_v = float('-inf')
				for a in all_possible_actions:
					grid.set_state(s)
					r = grid.move(a)
					v = r + gamma * V[grid.current_state(s)]
					if v > new_v:
						new_v = v
				V[s] = new_v
				biggest_change = max( biggest_change, np.abs(old_v - V[s]))
				  
		if biggest_change < small_enough:
			break
		
		for s in policy.keys():
			best_a = None
			best_value = float('-inf') 
				
			for a in all_possible_actions:
				grid.set_state(s)
				r = grid.move(a)
				v = r + gamma * V[grid.current_state(s)]
				if v > best_value:
					best_value = v 
					new_a = a
			policy[s] = best_a

	print ("Values")
	print_values(V,grid)
	print ("Policy")
	print_policy(policy,grid)


# In[ ]:




