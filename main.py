from random import random
import pygame
import random
from collections import namedtuple
pygame.init()
G=2# value of gravity
SPEED=40# speed of game
# rang
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN=(0,128,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)

# bird  size...I mean radius
SIZE=20
#font vagera
font=pygame.font.SysFont('arial',25)

Point=namedtuple('Point','x, y, l, passed')#(x_cord,y_cord,length ) for bird it is set manually to zero
                                   # while in case of pipe it is randomlt selected and pass is just for time pass 😉

kuch_bhi=lambda : random.randint(150,200)#just to get random number number for diffrent size of pipe

class flappybird:
    
    def __init__(self,w=640,h=480) -> None:
        self.w=w
        self.h=h
        #init display
        self.display=pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption("flappy bird")
        self.Clock=pygame.time.Clock()
        self.reset()
        
    def reset(self):
        #init some game state...
        #like bird positon,initial pipe positon
        self.bird=Point(self.w/4,self.h/2,0,False)
        self.reward=0
        self.score=0
        self.jump=False
        self.should_append=True
        len_for_lower_Y=kuch_bhi()
        self.pipe=[Point(500,0,kuch_bhi(),False),Point(500,480-len_for_lower_Y,len_for_lower_Y,False)]#first time wala init

    def play(self,action):
        reward=0
        #User input
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        #move pipe and bird
        self.bird_move(action)#chidiya udi            
        #check if game over 
        if self.is_collision():
            game_over=True
            reward=-10
            return reward,game_over,self.score
        #update the UI and Clock
        self.update_ui()
        self.Clock.tick(SPEED)
        #return gameover and score
        game_over=False
        return reward,game_over,self.score

    def is_collision(self,edge_x=0,edge_y=0):
        #if bird touch the pipe
        col=False
        for i in range(len(self.pipe)):
            if i%2==0:
                if self.pipe[i].passed==True and self.bird.x+edge_x+SIZE>=self.pipe[i].x and self.bird.y-SIZE-edge_y<self.pipe[i].y+self.pipe[i].l:
                    col=True
                    break
                col=False
            if i%2==1:
                if self.pipe[i].passed==True and self.bird.x+edge_x+SIZE>=self.pipe[i].x and self.bird.y>self.pipe[i].y:
                    col=True
                    break
                col=False
        if self.bird.y>=480:
            col=True
        return col

    def bird_move(self,jump):
        global G
        x=self.bird.x
        y=self.bird.y
        if jump:
            G=2
            for i in range(0,10):
                y-=i
        G+=1
        y+=G
        self.jump=False
        self.bird=Point(x,y,0,False)

    def draw_pipe(self):
        for p in range(len(self.pipe)):
            x=self.pipe[p].x
            y=self.pipe[p].y
            x-=10
            self.pipe[p]=Point(x,y,self.pipe[p].l,False)
        if len(self.pipe)>8:
            return
        for P in self.pipe:
            pygame.draw.rect(self.display,GREEN,pygame.Rect(P.x,P.y,40,P.l))
        if self.pipe[0].x<-40:
            self.pipe.pop(0)
            self.pipe.pop(0)
            self.should_append=True
        if self.pipe[0].x<120:
            self.score+=1
            self.reward=10
            self.pipe[0]=Point(self.pipe[0].x,self.pipe[0].y,self.pipe[0].l,True)
            self.pipe[1]=Point(self.pipe[1].x,self.pipe[1].y,self.pipe[1].l,True)
        if self.pipe[0].x<random.randint(150,200) :
            if not self.should_append:
                return
            x=700#this will give a smooth appearing effect
            u_y=0
            len_for_lower_Y=kuch_bhi()
            #always the first pipe is upper and sec is lower one 
            self.pipe.append(Point(x,u_y,kuch_bhi(),False))
            self.pipe.append(Point(x,480-len_for_lower_Y,len_for_lower_Y,False))
            self.should_append=False
        

    def update_ui(self):
        self.display.fill(BLACK)
        #making the bird
        pygame.draw.circle(self.display,BLUE2,[self.bird.x,self.bird.y],SIZE,0)
        #pipe 
        self.draw_pipe()
        text=font.render("Score: "+str(self.score),True,WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()

