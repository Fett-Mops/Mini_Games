import PIL.Image
import pygame as pg
import os 
import json
import random
from icecream import ic

class Game:
    def __init__(self, width, height,*args, **kwargs) -> None:
        self.HEIGHT = height/2
        self.WIDTH = width
        pg.init()
        
        with open("color.json") as f:
                self.col_p = json.load(f)
                
        self.screen = pg.display.set_mode((self.WIDTH,self.HEIGHT+40))
        pg.display.set_caption('Rock Paper Scissers')
        self.col = {'bg':self.col_p['blue']['50'],
                    'winn':self.col_p['green']['300'], 
                    'lines':self.col_p['green']['300'],
                    'x': self.col_p['red']['300'], 
                    'o':self.col_p['deeppurple']['300']}
        
        self.player_1 = ''
        self.npc =''
        
        self.score = {'player': 0,
                      'npc': 0}
        
        self.imgs= {'rock':pg.image.load('Rock_Paper_Scissors\\assets\\Rock.png').convert_alpha(),
               'paper' : pg.image.load('Rock_Paper_Scissors\\assets\\Paper.png').convert_alpha(),
               'scissors':pg.image.load('Rock_Paper_Scissors\\assets\\Scissors.png').convert_alpha()
                }
        for img in self.imgs:
            self.imgs[img] =pg.transform.scale(self.imgs[img],(50,50))
        
        self.hands = []
        self.font = pg.font.SysFont('Comic Sans MS', 30)
            
    def draw(self, obj : str, hands : list[str] = [], player :str = '')->None:
        if obj == 'start':
            self.screen.fill(self.col['bg'])
          
            imgs =list(self.imgs.keys())

            
            for j in range(3):
                    rect = pg.Rect(50+60*j,self.HEIGHT*3/4,50,50)
                    if len(self.hands) < 6:
                        self.hands.append(rect)
                    
                    pg.draw.rect(self.screen, self.col['o'],rect)
                    self.screen.blit(self.imgs[imgs[j]],(50+60*j,self.HEIGHT*3/4))
                    
            for i,p in enumerate(self.score):
                render = self.font.render('{}: {}'.format(p,self.score[p]),False,self.col['o'])
                self.screen.blit(render, (100+300*i,self.HEIGHT/10))
                
                
                    
        elif obj == 'big':
            self.draw('start')
            for i in range(2):
                
                if player == 'player' and i ==0:
                
                    pg.draw.circle(self.screen,self.col['winn'],(150, self.HEIGHT/3+50),70)
                    
                    
                elif player == 'npc':
                    pg.draw.circle(self.screen,self.col['winn'],(450, self.HEIGHT/3+50),70,)
                   
                img = pg.transform.scale(self.imgs[hands[i]],(100,100))
                self.screen.blit(img,(100+300*i, self.HEIGHT/3))
                
    def logic(self):
 
        ls = [self.player_1,self.npc]
     
        if ls[1] == ls[0]:
            self.draw('big', ls)
        
        elif 'rock' in ls:
            if 'paper' in ls:
                self.score[list(self.score.keys())[ls.index('paper')]] +=1
                self.draw('big', ls, list(self.score.keys())[ls.index('paper')])
     

                
            elif 'scissors' in ls:
                self.score[list(self.score.keys())[ls.index('rock')]] +=1
                self.draw('big', ls, list(self.score.keys())[ls.index('rock')])

       
        else:
            self.score[list(self.score.keys())[ls.index('scissors')]] +=1
            self.draw('big', ls, list(self.score.keys())[ls.index('scissors')])

             
    def chosen_hand(self, hand):

        hand_leg = {0:'rock',
                    1:'paper',
                    2:'scissors'}
       
        self.player_1 = hand_leg[hand]
        self.npc = hand_leg[random.randint(0,2)]
        self.logic()
        
    def run(self):
        self.draw('start')
        while True:
            pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    for hand in self.hands[:3]:
                        if hand.collidepoint(pos):
                            self.chosen_hand(self.hands.index(hand))
                            
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.chosen_hand(0)
                    elif event.key == pg.K_p:
                        self.chosen_hand(1)
                    elif event.key == pg.K_s:
                        self.chosen_hand(2)
                if event.type == pg.QUIT:
                    return pg.quit()
            pg.display.update()
            
