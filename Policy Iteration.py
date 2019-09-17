#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import matplotlib.pyplot as plt
import import_ipynb
from grid_world import standard_grid, negative_grid
from Iterative_policy import print_values, print_policy

small_enough = 10e-4
gamma = 0.9
all_possible_actions = ('U', 'D', 'L', 'R')

if __name__ == '__main__':
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
		while True:
			biggest_change = 0
			for s in states:
				old_v = V[s]
				
				if s in policy:
					a = policy[s]
					grid.set_state(s)
					r = grid.move(a)
					V[s] = r + gamma * V[grid.current_state(s)]
					biggest_change = max( biggest_change, np.abs(old_v - V[s]))
				
			if biggest_change < small_enough:
				break
		is_policy_converged = True
		for s in states:
			if s in policy:
				old_a = policy[s]
				new_a = None
				best_value = float ('-inf')
				
				for a in all_possible_actions:
					grid.set_state(s)
					r = grid.move(a)
					v = r + gamma * V[grid.current_state(s)]
					if v > best_value:
						best_value = v 
						new_a = a
				policy[s] = new_a
				if new_a != old_a:
					is_policy_converged = False
					
		if is_policy_converged:
			break
	print ("Values")
	print_values(V,grid)
	print ("Policy")
	print_policy(policy,grid)
	


# In[ ]:




