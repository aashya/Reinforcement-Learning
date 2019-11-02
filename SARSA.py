#!/usr/bin/env python
# coding: utf-8

# In[19]:


import numpy as np
import matplotlib.pyplot as plt
import import_ipynb
from grid_world import standard_grid, negative_grid
from Iterative_policy import print_values, print_policy
from monte_carlo_exploring_starts import max_dict
from temp_diff import random_action

# small_enough = 10e-4
gamma = 0.9
alpha = 0.1
all_possible_actions = ('U', 'D', 'L', 'R')

if __name__ == '__main__':
	grid = negative_grid(step_cost=-0.1)
	print ("rewards")
	print_values(grid.rewards, grid)
	
	Q = {}
	states = grid.all_states()
	for s in states:
		Q[s] = {}
		for a in all_possible_actions:
			Q[s][a] = 0

	update_counts = {}
	update_counts_sa = {}
	for s in states:
		update_counts_sa[s] = {}
		for a in all_possible_actions:
			update_counts_sa[s][a] = 1.0
	
	t = 1.0
	deltas = []
	for it in range(10000):
		if it%100 == 0:
			t += 1e-2
		if it % 2000 == 0:
			print ("it:")
			print (it)
	
    
    
		s = (2,0)
		grid.set_state(s)
		a = max_dict(Q[s])[0]
		a = random_action(a, eps=0.5/t)
		biggest_change = 0
		while not grid.game_over():
			r=grid.move(a)
			s2 = grid.current_state(s)
		
			a2 = max_dict(Q[s2])[0]
			a2 = random_action(a2, eps = 0.5/t)
			
			alpha = alpha/update_counts_sa[s][a]
			update_counts_sa[s][a] +=0.005

			old_qsa = Q[s][a]
			Q[s][a] = Q[s][a] + alpha*(r + gamma*Q[s2][a2] - Q[s][a])
			biggest_change = max(biggest_change, np.abs(old_qsa - Q[s][a]))
			
			update_counts[s] = update_counts.get(s,0) + 1
			
			s = s2
			a = a2

		deltas.append(biggest_change)
	
	plt.plot(deltas)
	plt.show()
	 
	
	policy = {}
	V = {}
	for s in grid.actions.keys():
		a, max_q = max_dict(Q[s])
		policy[s] = a
		V[s] = max_q
		
	print ("update_counts")
	total = np.sum(list(update_counts.values()))
	for k, v in update_counts.items():
	
		update_counts[k] = float(v) / total
	print_values(update_counts, grid)
# 	for k, v in update_counts.items():
# 		update_counts[k] = float(v) / total
# 	print_values(update_counts, grid)
	
	print ("Values")
	print_values(V,grid)
	print ("Policy")
	print_policy(policy,grid)
	
    


# In[ ]:




