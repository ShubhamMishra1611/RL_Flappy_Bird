#This to get as state
#bird y position
#pipe location(probably next one)

#rememeber fucntion
#train_long_memeory
#train_short_memory
#get action form the model
#training

import torch
import random
from collections import deque
import numpy as np
from main import flappybird,Point
from model import Linear_QNet,QTrainer
from helper import plot

MAX_MEMORY=100000
BATCH=1000#batch size
LR=0.001#learning rate

class Agent:

    def __init__(self) -> None:
        self.n_games=0
        self.eplison=0#degree of randomness .... entropy nhi he bhai
        self.gamma=0.9
        self.memory=deque(maxlen=MAX_MEMORY)
        self.model=Linear_QNet(4,256,1)
        self.trainer=QTrainer(self.model,lr=LR,gamma=self.gamma)


    def get_state(self,game):
        bird=game.bird
        current_y_cord=bird.y
        pipe=game.pipe
        #print(len(pipe))
        for i in range(len(pipe)):
            if pipe[i].x-bird.x>=0:
                nearest_pipe_x_upper=pipe[i].x
                nearest_pipe_y_upper=pipe[i].y
                nearest_pipe_y_lower=pipe[i+1].y
                break
        

        state=[
            current_y_cord,
            nearest_pipe_x_upper,
            nearest_pipe_y_lower,
            nearest_pipe_y_upper,
        ]

        return np.array(state,dtype=int)


    def train_long_memory(self):
        if len(self.memory)>BATCH:
            mini_sample=random.sample(self.memory,BATCH)
        else:
            mini_sample=self.memory
        
        states,rewards,actions,next_states,dones=zip(*mini_sample)
        self.trainer.train_step(states,rewards,actions,next_states,dones)

    def train_short_memory(self,state,reward,action,next_state,done):
        self.trainer.train_step(state,reward,action,next_state,done)
        
    def remember(self,state,reward,action,next_state,done):
        self.memory.append((state,reward,action,next_state,done))

    def get_action(self,state):
        self.eplison=100-self.n_games
        if random.randint(0,200)<self.eplison:
            move=random.randint(0,1) == 0
            final_move=move
        else:
            state0=torch.tensor(state,dtype=torch.float)
            prediction=self.model(state0)
            move=torch.argmax(prediction).item()
            final_move=move
        return final_move
        


def train():
    plot_score=[]
    plot_mean_score=[]
    total_score=0
    record=0
    agent=Agent()
    game=flappybird()
    while True:
        state_old=agent.get_state(game)
        final_move=agent.get_action(state_old)
        reward,done,score=game.play(final_move)
        state_new=agent.get_state(game)
        agent.train_short_memory(state_old,reward,final_move,state_new,done)
        agent.remember(state_old,reward,final_move,state_new,done)

        if done:
            game.reset()
            agent.n_games+=1
            agent.train_long_memory()

            if score>record:
                record=score
                agent.model.save()
            print("Game ",agent.n_games,'score ',score,'record: ',record)
            plot_score.append(score)
            total_score+=score
            mean_score=total_score/agent.n_games
            plot_mean_score.append(mean_score)
            plot(plot_score,plot_mean_score)

if __name__=="__main__":
    train()