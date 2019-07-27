import gym
from gym import error, spaces, utils
from gym.utils import seeding
import sys, pygame,random
pygame.init()
pygame.display.set_caption('Snake')
class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        self.size = self.width, self.height = 640, 480
        self.speed = [2, 2]
        
        self.HeadX,self.HeadY = [50],[60]
        self.circlePosX , self.circlePosY = 40,40
        self.speedX, self.speedY =10,10
        self.originalPositionX, self.originalPositionY =list(map(lambda a : int(a/10)*10,self.HeadX)) , list(map(lambda a : int(a/10)*10,self.HeadY))
        self.score=0
        self.numRect = 1
        self.tempX , self.tempY = int(self.HeadX[0]/10)*10,int(self.HeadY[0]/10)*10
        self.Direction = 3
        self.addNode =False
    def action_sample (self):
        return int(random.randint(0,3))
    def step(self, action):
        self.reward= 0 
        if action==0 and self.Direction !=1 :
                    self.Direction = 0 
        elif action==1 and self.Direction!=0:
                    self.Direction = 1 
        elif action==2 and not self.Direction ==3:
                    self.Direction =2 
        elif action==3 and not self.Direction==2:
                    self.Direction =3 
        if self.Direction == 0 :
                self.HeadY[0]  -= self.speedY
        elif self.Direction == 1 :
                 self.HeadY[0] += self.speedY
        elif self.Direction == 2:
                 self.HeadX[0] -= self.speedX
        elif self.Direction == 3 :
                 self.HeadX[0] += self.speedX

        if self.circlePosX - 10 <=int(self.HeadX[0]/10)*10 <=self.circlePosX +8 and self.circlePosY -10 <=int(self.HeadY[0]/10)*10 <=self.circlePosY +8 :

            self.circlePosX , self.circlePosY = int(random.random() * (self.width-40) )+20, int(random.random()*(self.height-40))+20
            self.circlePosX = int(self.circlePosX/10)*10
            self.circlePosY = int(self.circlePosY/10)*10
            while (self.circlePosX in self.originalPositionX and self.circlePosY in self.originalPositionY):
                self.circlePosX , self.circlePosY = int(random.random() * (self.width-40) )+20, int(random.random()*(self.height-40))+20
                self.circlePosX = int(self.circlePosX/10)*10
                self.circlePosY = int(self.circlePosY/10)*10
            self.score+=1
            self.reward= 1
            self.addNode= True
        if self.addNode :
            self.HeadX.append(int(self.originalPositionX[-1])*10)
            self.HeadY.append(int(self.originalPositionY[-1])*10)
            self.addNode= False
        for i in range(1,len(self.HeadX)):
            self.HeadX[i] = int(self.originalPositionX[i-1]/10)*10
            self.HeadY[i] = int(self.originalPositionY[i-1]/10)*10
        self.tempX=int(self.HeadX[0]/10)*10;
        self.tempY=int(self.HeadY[0]/10)*10
        self.originalPositionX= list(map(lambda a : int(a/10)*10,self.HeadX)) ;
        self.originalPositionY =  list(map(lambda a : int(a/10)*10,self.HeadY)) ;
        self.info = {"Score  : "  : self.score}
        self.done = False
        if int(self.HeadX[0]) < 10 or int(self.HeadX[0]) > self.width-20 or int(self.HeadY[0]) < 10 or int(self.HeadY[0]) > self.height-20:
            self.done=True
        
        self.observation =  [self.HeadX[0],self.HeadY[0],self.circlePosX,self.circlePosY]
        left,right,front,back = 0,0,0,0
        for i in range(1,len(self.HeadX)):
            if(int(self.HeadX[0]/10)*10 ==int(self.HeadX[i]/10)*10 and int(self.HeadY[0]/10)*10==int(self.HeadY[i]/10)*10):
                self.done=True
            if(int(self.HeadX[0]/10)*10 ==((int(self.HeadX[i]/10)*10)-10)  and int(self.HeadY[0]/10)*10==int(self.HeadY[i]/10)*10):
                if self.Direction==0:
                    right=1
                elif self.Direction== 1 :
                    left=1
                elif self.Direction==2 :
                    back=1
                elif self.Direction== 3 :
                    front=1
            if(int(self.HeadX[0]/10)*10 ==((int(self.HeadX[i]/10)*10)+10 ) and int(self.HeadY[0]/10)*10==int(self.HeadY[i]/10)*10):
                if self.Direction==0:
                    left=1
                elif self.Direction== 1 :
                    right=1
                elif self.Direction==2 :
                    front=1
                elif self.Direction== 3 :
                    back=1
            if(int(self.HeadX[0]/10)*10 ==(int(self.HeadX[i]/10)*10)  and int(self.HeadY[0]/10)*10==(int(self.HeadY[i]/10)*10) -10):
                if self.Direction==0:
                    back=1
                elif self.Direction== 1 :
                    front=1
                elif self.Direction==2 :
                    right=1
                elif self.Direction== 3 :
                    left=1
            if(int(self.HeadX[0]/10)*10 ==(int(self.HeadX[i]/10)*10)  and int(self.HeadY[0]/10)*10==(int(self.HeadY[i]/10)*10)+10):
                if self.Direction==0:
                    front=1
                elif self.Direction== 1 :
                    back=1
                elif self.Direction==2 :
                    left=1
                elif self.Direction== 3 :
                    right=1

        self.observation.extend([front,left,right,self.Direction])
        return self.observation , self.reward, self.done , self.info
    def reset(self):
        self.speed = [2, 2]
        self.HeadX,self.HeadY = [50],[60]
        self.circlePosX , self.circlePosY = 40,40
        self.speedX, self.speedY =0.5,0.5
        self.originalPositionX, self.originalPositionY =list(map(lambda a : int(a/10)*10,self.HeadX)) , list(map(lambda a : int(a/10)*10,self.HeadY))
        self.score=0
        self.numRect = 1
        self.tempX , self.tempY = int(self.HeadX[0]/10)*10,int(self.HeadY[0]/10)*10
        self.Direction = 3
        self.addNode =False
    def render(self, mode='human'):
        black = 0, 0, 0
        screen = pygame.display.set_mode(self.size)
        screen.fill(black)
        # BORDER
        pygame.draw.rect(screen,pygame.Color(255,255,255),(0,0,9,self.height))
        pygame.draw.rect(screen,pygame.Color(255,255,255),(0,0,self.width,9))
        pygame.draw.rect(screen,pygame.Color(255,255,255),(self.width-9,self.height-10,9,-self.height))
        pygame.draw.rect(screen,pygame.Color(255,255,255),(self.width,self.height-9,-self.width,9))
        # BORDER END
        for i in range(len(self.HeadX)):
            pygame.draw.rect(screen,pygame.Color(0,255,0),(int(self.HeadX[i]/10)*10,int(self.HeadY[i]/10)*10,10,10))
        pygame.draw.circle(screen,pygame.Color(255,0,0),(self.circlePosX,self.circlePosY),6)
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.score), 1, (pygame.Color(50,100,255)))
        textpos = text.get_rect(centerx=screen.get_width()/2,centery=screen.get_height()/2)
        screen.blit(text, textpos)
        pygame.display.update()
    def close(self):
        pass


# 0 : w , 1:s , 2:a , 3:d