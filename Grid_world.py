#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt

class Grid:
	def __init__(self, rows, columns, start):
		self.rows = rows 
		self.columns = columns
        #current location will be seen through instance variales i and j
		self.i = start[0]
		self.j = start[1]
		
	#Setter -- sets rewards and actions simultaneously
	def set(self, rewards, actions):
		#rewards and actions is a dictionary where the key is i,j coordinate representing state --> value = numerical reward / list of possible actions
		self.rewards = rewards
		self.actions = actions
		# actions show all actions -- even the impossible ones, the grid class will ignore those since it will not be in the actions dictionary
		
	#Useful when you need to set the state such as in iterative policy evaluation	
	def set_state(self,s):
		self.i = s[0]
		self.j = s[1]
		
	#defines current position	
	def current_state(self,s):
		return(self.i, self.j)
		
	#returns true if it is a terminal state, false if not
	def is_terminal(self,s):
		return s not in self.actions
		
		
	# Takes the action as an argument
	def move(self, action):
		#check if action is in actions dictionary
		if action in self.actions[(self.i, self.j)]:
			#following array convention where i=0 to n moves from top to bottom and j =0 to n from left to right
			if action == "U":
				self.i -= 1
			if action == "D":
				self.i += 1
			if action == "R":
				self.j += 1
			if action == "L":
				self.j -= 1
		return self.rewards.get((self.i, self.j), 0)
		
	#Environment undos the action done by you	
	def undo_move(self, action):
		if action == "U":
			self.i += 1
		if action == "D":
			self.i -= 1
		if action == "R":
			self.j -= 1
		if action == "L":
			self.j += 1
		
		#Checking if current state is in the set of all allowed states
		#Since we should never reach this point, we put an assert function to stop the code in case of failure
		assert(self.current_state() in self.all_states())
	
	#Checks if we are in the terminal state and then provides true in case it is 
	def game_over(self):
		return (self.i, self.j) not in self.actions
		
	#Calculates all states from which we can take an action, not including terminal states and states returning a reward	
	def all_states(self):
		return set(self.actions.keys() | self.rewards.keys())

    # 	def all_states(self):
# 		return set(self.actions.keys()) | set(self.rewards.keys())
# # 		Action_keys = list(self.actions.keys())
# # 		Reward_keys = list(self.rewards.keys())
# 		return set (Action_keys | Reward_keys)

#Defines the grid and the movement in the grid including rewards and actions
def standard_grid():
# x means you cant go there -- such as a wall
# s means start position 
# number defines the reward at that state
# . . . 1 -- grid first line
# . x . -1 -- grid second line
# s . . . -- grid third line
# g shows the grid of 3*4 = 3 rows, 4 columns, with starting position at (2,0) which means third row, first column 
# rewards defines the rewards at the specific positions
	g = Grid(3,4,(2,0)) 
	rewards = { (0,3): 1, (1,3): -1}
	actions = {
		(0, 0): ('D', 'R'),
		
		(0, 1): ('L', 'R'),
		
		(0, 2): ('L', 'D', 'R'),

		(1, 0): ('U', 'D'),

		(1, 2): ('U', 'D', 'R'),

		(2, 0): ('U', 'R'),

		(2, 1): ('L', 'R'),

		(2, 2): ('L', 'R', 'U'),

		(2, 3): ('L', 'U'),
	}
	g.set (rewards, actions)
	return g
	
#Shows the penalisation for each move so that we can achieve the target efficiently	
def negative_grid():
	g = standard_grid()
	g.rewards.update({
		(0, 0): step_cost,

		(0, 1): step_cost,

		(0, 2): step_cost,

		(1, 0): step_cost,

		(1, 2): step_cost,

		(2, 0): step_cost,

		(2, 1): step_cost,

		(2, 2): step_cost,
		
		(2, 3): step_cost,
    })
	return g 
	
def play_game(agent, env):
	pass


# In[ ]:




