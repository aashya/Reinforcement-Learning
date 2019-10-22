#!/usr/bin/env python
# coding: utf-8

# In[9]:


import numpy as np
import matplotlib.pyplot as plt
import import_ipynb
from grid_world import standard_grid, negative_grid
from Iterative_Policy import print_values, print_policy

small_enough = 10e-4
gamma = 0.9
all_possible_actions = ('U', 'D', 'L', 'R')


def play_game(grid, policy):
	start_states = list (grid.actions.keys())
	#starting at a random state so that we can visit all states -- called the exploring starts method
	start_idx = np.random.choice(len(start_states)) 
	grid.set_state(start_states[start_idx])
	
	
	s = grid.current_state(start_idx)
	a = np.random.choice(all_possible_actions)
	
	states_and_rewards = [(s,a,0)]
	
	while True:
		old_s = grid.current_state(s)
		r = grid.move(a)
		s = grid.current_state(s)
		
		if old_s == s:
			states_and_rewards.append((s,None, -100))
			break
		elif grid.game_over():
			states_and_rewards.append((s,None, r))
			break
		else:
			a = policy[s]
			states_and_rewards.append((s,a, r))	
			
	G=0
	states_and_returns =[]
	first = True

	for s,a,r in reversed(states_and_rewards):
		if first:
			first = False
		else:
			states_and_returns.append((s,a, G))
		G = r + gamma*G
	states_and_returns.reverse()
	return states_and_returns
	
def max_dict(d):
	max_key = None
	max_value = float('-inf')
	for k, v in d.items():
		if v> max_value:
			max_value= v
			max_key = k
	return max_key, max_value
	
if __name__ == '__main__':
	
	grid = negative_grid(step_cost = -0.1)
	print ("rewards:")
	print_values(grid.rewards, grid)

	policy = {}
	for s in grid.actions.keys():
		policy[s]= np.random.choice(all_possible_actions)
		
	Q = {}
	returns = {}
	states = grid.all_states()
	for s in states:
		if s in grid.actions:
			Q[s] = {}
			for a in all_possible_actions:
				Q[s][a] = 0
				returns[(s,a)] = []
		else:
			pass
			
	deltas = []
	for t in range(2000):
		if t%1000 == 0:
			print (t)
			
		biggest_change = 0
		states_action_returns = play_game(grid, policy)
		seen_state_action_pairs = set()
		for s,a,G in states_action_returns:
			sa = (s,a)
			if sa not in seen_state_action_pairs:
				old_q = Q[s][a]
				returns[sa].append(G)
				Q[s][a] = np.mean(returns[sa])
				biggest_change = max(biggest_change, np.abs(old_q - Q[s][a]))
				seen_state_action_pairs.add(sa)
		deltas.append(biggest_change)
		
	
	for s in policy.keys():
		policy[s] = max_dict(Q[s])[0]
		
	plt.plot(deltas)
	plt.show()
	
	print ("final policy")
	print_policy(policy, grid)
	
	V = {}
	for s, Qs in Q.items():
		V[s]=max_dict(Q[s])[1]
		
		
	print ("final values")
	print_values(V, grid)


# In[ ]:




