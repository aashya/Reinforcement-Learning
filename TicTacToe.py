#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

LENGTH = 3

class agent:
    def _init_(self, eps=0.1, alpha=0.5):
        self.eps = eps
        self.alpha = alpha
        self.verbose = False
        self.state_history = []
        
    def setV(self,V):
        self.V = V
    
    def set_symbol(self, sym):
        self.sym = sym
        
    def set_verbose(self,v):
        set.verbose = v
        
    def reset_history(self):
        self.state_history = []
        
        
    def take_action(self, env):
    # choose an action based on epsilon-greedy strategy
        r = np.random.rand()
        best_state = None
        if r < self.eps:
          # take a random action
            if self.verbose:
                print("Taking a random action")

                possible_moves = []
                for i in range(LENGTH):
                    for j in range(LENGTH):
                        if env.is_empty(i, j):
                            possible_moves.append((i, j))
                idx = np.random.choice(len(possible_moves))
                next_move = possible_moves[idx]
        else:
          # choose the best action based on current values of states
          # loop through all possible moves, get their values
          # keep track of the best value
            pos2value = {} # for debugging
            next_move = None
            best_value = -1
            for i in range(LENGTH):
                for j in range(LENGTH):
                    if env.is_empty(i, j):
                    # what is the state if we made this move?
                        env.board[i,j] = self.sym
                        state = env.get_state()
                        env.board[i,j] = 0 # don't forget to change it back!
                        pos2value[(i,j)] = self.V[state]
                        if self.V[state] > best_value:
                            best_value = self.V[state]
                            best_state = state
                            next_move = (i, j)

          # if verbose, draw the board w/ the values
            if self.verbose:
                print("Taking a greedy action")
                for i in range(LENGTH):
                    print("------------------")
                    for j in range(LENGTH):
                        if env.is_empty(i, j):
                          # print the value
                            print(" %.2f|" % pos2value[(i,j)], end="")
                        else:
                            print("  ", end="")
                            if env.board[i,j] == env.x:
                                print("x  |", end="")
                            elif env.board[i,j] == env.o:
                                print("o  |", end="")
                            else:
                                print("   |", end="")
                        print("")
                print("------------------")

            # make the move
            env.board[next_move[0], next_move[1]] = self.sym



    def update_state_history(self, s):

    # cannot put this in take_action, because take_action only happens

    # once every other iteration for each player

    # state history needs to be updated every iteration

    # s = env.get_state() # don't want to do this twice so pass it in

        self.state_history.append(s)
    


    def update(self, env):

    # we want to BACKTRACK over the states, so that:

    # V(prev_state) = V(prev_state) + alpha*(V(next_state) - V(prev_state))

    # where V(next_state) = reward if it's the most current state

    #

    # NOTE: we ONLY do this at the end of an episode

    # not so for all the algorithms we will study

        reward = env.reward(self.sym)

        target = reward

        for prev in reversed(self.state_history):

            value = self.V[prev] + self.alpha*(target - self.V[prev])

            self.V[prev] = value

            target = value

        self.reset_history()


    
 
                            

class environment:
    def __init__(self):
        self.board = np.zeros((LENGTH, LENGTH))
        self.x = -1 # represents an x on the board, player 1
        self.o = 1 # represents an o on the board, player 2
        self.winner = None
        self.ended = False
        self.num_states = 3**(LENGTH*LENGTH)
#         print("Environment")
        
        
    
    def is_empty(self,i,j):
#         print("isempty")
        return self.board[i,j] == 0

    def reward(self, sym):
#         print("reward")
    #no reward until game over
        if not self.game_over():
            return 0
#     game over
        return 1 if self.winner == sym else 0


    def get_state(self):
#         print("get_state")
#     length = 3^9
        h=0
        k=0
        for i in range(LENGTH):
            for j in range(LENGTH):
                if self.board[i,j] == 0:
                    v=0
                if self.board[i,j] == self.x:
                    v=1
                if self.board[i,j] == self.o:
                    v=2
                h += (3**k) *v
                k += 1
            return h
        
        
        
    def game_over(self, force_recalculate=False):
        if not force_recalculate and self.ended:
            return self.ended
    #     check rows
        for i in range(LENGTH):
            for player in (self.x, self.o):
                if self.board[i].sum() == player*LENGTH:
                    self.winner = player
                    self.ended = True
                    return True
    #     Check columns
        for j in range(LENGTH):
            for player in (self.x, self.o):
                if self.board[:,j].sum() == player*LENGTH:
                    self.winner = player
                    self.ended = True
                    return True
    #     Check diagnols
        for player in (self.x, self.o):
    #         Top LEft -->bottom right
            if self.board.trace() == player*LENGTH:
                self.winner = player
                self.ended = True
                return True

    #     Top right-->bottom left diagonal
            if np.fliplr(self.board).trace() == player*LENGTH:
                self.winner = player
                self.ended = True
                return True


    #         Check Draw

        if np.all((self.board == 0) == False):
    #         Winner stays none
            self.winner = None
            self.ended = True
            return True

    #     game is not over
        self.winner = None
        return False


    def draw_board(self):
        for i in range(LENGTH):
            print ("------------------")
            for j in range(LENGTH):
                print (" ", end = "")
                if self.board[i,j] == self.x:
                    print ("x", end="")
                if self.board[i,j] == self.o:
                    print ("o", end="")
                else:
                    print (" ", end="")
            print ("")
        print ("------------")


        
        
class human:
    
    def __init__(self):

        pass


    
    
    
    def set_symbol(self, sym):

        self.sym = sym



    def take_action(self, env):

        while True:

      # break if we make a legal move

            move = input("Enter coordinates i,j for your next move (i,j=0..2): ")

            i, j = move.split(',')

            i = int(i)

            j = int(j)

            if env.is_empty(i, j):

                env.board[i,j] = self.sym

                break



    def update(self, env):

        pass



    def update_state_history(self, s):

        pass




        

# recursive function that will return all

# possible states (as ints) and who the corresponding winner is for those states (if any)

# (i, j) refers to the next cell on the board to permute (we need to try -1, 0, 1)

# impossible games are ignored, i.e. 3x's and 3o's in a row simultaneously

# since that will never happen in a real game

def get_state_hash_and_winner(env, i=0, j=0):
    results = []

    for v in (0, env.x, env.o):
        env.board[i,j] = v # if empty board it should already be 0
        if j == 2:
      # j goes back to 0, increase i, unless i = 2, then we are done
            if i == 2:
        # the board is full, collect results and return
                state = env.get_state()
                ended = env.game_over(force_recalculate=True)
                winner = env.winner
                results.append((state, winner, ended))
            else:
                results += get_state_hash_and_winner(env, i + 1, 0)
        else:
      # increment j, i stays the same
            results += get_state_hash_and_winner(env, i, j + 1)

    return results


def initialv_x(env,state_winner_triples):
    V = np.zeros(env.num_states)
    for state, winner, ended, in state_winner_triples:
        if ended:
            if winner == env.x:
                v=1
            else:
                v=0
        else:
            v=0.5
        V[state] = v
    return V
            
    
def initialv_o(env,state_winner_triples):
    V = np.zeros(env.num_states)
    for state, winner, ended, in state_winner_triples:
        if ended:
            if winner == env.o:
                v=1
            else:
                v=0
        else:
            v=0.5
        V[state] = v
    return V


def play_game( p1, p2, env, draw=False ):
    
    current_player = None
    while not env.game_over():
    
#     Change Player
        if current_player == p1:
            current_player = p2
        else:                
            current_player = p1


    #     Draw Board
    if draw:
        if draw ==1 and current_player == p1:
            env.draw_board()
        if draw == 1 and current_player == p2:
            env.draw_board()

    #     Action
        current_player.take_action(env)

    #     Update Environment
        state = env.get_state()
        p1.update_state_history(state)
        p2.update_state_history(state)
    
    if draw:
        env.draw_board()
        
#         Update Value
    p1.update(env)
    p2.update(env)
    
def game_over():
    state 
    
    
if __name__ == '__main__':

  # train the agent

    p1 = agent()

    p2 = agent()



    
  # set initial V for p1 and p2

    env = environment()

    state_winner_triples = get_state_hash_and_winner(env)





    Vx = initialv_x(env, state_winner_triples)

    p1.setV(Vx)

    Vo = initialv_o(env, state_winner_triples)

    p2.setV(Vo)



  # give each player their symbol

    p1.set_symbol(env.x)

    p2.set_symbol(env.o)


    T = 10000

    for t in range(T):

#         if t % 200 == 0:
            
#             print("t")

#             print(t)

        print("play game")
        play_game(p1, p2, environment())



  # play human vs. agent

  # do you think the agent learned to play the game well?

    human = Human()

    human.set_symbol(env.o)

    while True:

        p1.set_verbose(True)

        play_game(p1, human, environment(), draw=2)

    # I made the agent player 1 because I wanted to see if it would

    # select the center as its starting move. If you want the agent

    # to go second you can switch the human and AI.

        answer = input("Play again? [Y/n]: ")

        if answer and answer.lower()[0] == 'n':

            break


# In[ ]:


# def get_state_hash_and_winner(env, i=0, j=0):
#     results = []

#     for v in (0, env.x, env.o):
#         env.board[i,j] = v # if empty board it should already be 0
#         if j == 2:
#       # j goes back to 0, increase i, unless i = 2, then we are done
#             if i == 2:
#         # the board is full, collect results and return
#                 state = env.get_state()
#                 ended = env.game_over(force_recalculate=True)
#                 winner = env.winner
#                 results.append((state, winner, ended))
#             else:
#                 results += get_state_hash_and_winner(env, i + 1, 0)
#         else:
#       # increment j, i stays the same
#             results += get_state_hash_and_winner(env, i, j + 1)

#     return results


# In[3]:


# def initialv_x(env,state_winner_triples):
#     V = np.zeros(env.num_states)
#     for state, winner, ended, in state_winner_triples:
#         if ended:
#             if winner == env.x:
#                 v=1
#             else:
#                 v=0
#         else:
#             v=0.5
#         V[state] = v
#     return V
            
    
# def initialv_o(env,state_winner_triples):
#     V = np.zeros(env.num_states)
#     for state, winner, ended, in state_winner_triples:
#         if ended:
#             if winner == env.o:
#                 v=1
#             else:
#                 v=0
#         else:
#             v=0.5
#         V[state] = v
#     return V


# In[4]:


# def play_game( p1, p2, env, draw=False ):
#     current_player = None
#     while not env.game_over():
    
# #     Change Player
#         if current_player == p1:
#             current_player = p2
#         else:                
#             current_player = p1


#     #     Draw Board
#     if draw:
#         if draw ==1 and current_player == p1:
#             env.draw_board()
#         if draw == 1 and current_player == p2:
#             env.draw_board()

#     #     Action
#         current_player.take_action(env)

#     #     Update Environment
#         state = env.get_state()
#         p1.update_state_history(state)
#         p2.update_state_history(state)
    
#     if draw:
#         env.draw_board()
        
# #         Update Value
#     p1.update(env)
#     p2.update(env)


# In[ ]:


# def game_over():
#     state 
    
    
# if __name__ == '__main__':

#   # train the agent

#     p1 = agent()

#     p2 = agent()



    
#   # set initial V for p1 and p2

#     env = environment()

#     state_winner_triples = get_state_hash_and_winner(env)





#     Vx = initialv_x(env, state_winner_triples)

#     p1.setV(Vx)

#     Vo = initialv_o(env, state_winner_triples)

#     p2.setV(Vo)



#   # give each player their symbol

#     p1.set_symbol(env.x)

#     p2.set_symbol(env.o)



#     T = 10000

#     for t in range(T):

#         if t % 200 == 0:

#             print(t)

#         play_game(p1, p2, environment())



#   # play human vs. agent

#   # do you think the agent learned to play the game well?

#     human = Human()

#     human.set_symbol(env.o)

#     while True:

#         p1.set_verbose(True)

#         play_game(p1, human, environment(), draw=2)

#     # I made the agent player 1 because I wanted to see if it would

#     # select the center as its starting move. If you want the agent

#     # to go second you can switch the human and AI.

#         answer = input("Play again? [Y/n]: ")

#         if answer and answer.lower()[0] == 'n':

#             break


# In[ ]:





# In[ ]:





# In[ ]:




