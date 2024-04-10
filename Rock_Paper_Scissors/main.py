import PIL.Image
import pygame as pg
import os 
import PIL
import json
import random

class Game:
    def __init__(self, width, height,*args, **kwargs) -> None:
        self.HEIGHT = height/2
        self.WIDTH = width
        pg.init()
        with open("color.json") as f:
                self.col_p = json.load(f)
        self.screen = pg.display.set_mode((self.WIDTH,self.HEIGHT+40))
        
        self.col = {'bg':self.col_p['blue']['50'],
                    'def_lines':self.col_p['green']['300'], 
                    'lines':self.col_p['green']['300'],
                    'x': self.col_p['red']['300'], 
                    'o':self.col_p['deeppurple']['300']}
        
        self.player_1 = ''
        self.npc =''
        
        self.score = {'npc': 0,
                      'player': 0}
        
        self.imgs= {'rock':pg.image.load('Rock_Paper_Scissors\\assets\\Rock.png').convert_alpha(),
               'paper' : pg.image.load('Rock_Paper_Scissors\\assets\\Paper.png').convert_alpha(),
               'scissors':pg.image.load('Rock_Paper_Scissors\\assets\\Scissors.png').convert_alpha()
                }
        for img in self.imgs:
            self.imgs[img] =pg.transform.scale(self.imgs[img],(50,50))
        
        self.hands = []
            
    def draw(self, obj : str, hands : list[str] = [], player :str = '')->None:
        if obj == 'start':
          
            imgs =list(self.imgs.keys())
            print(imgs)
            for i in range(2):
                for j in range(3):
                    rect = pg.Rect(self.WIDTH/9*5*i+50+60*j,self.HEIGHT*3/4,50,50)
                    if len(self.hands) < 6:
                        self.hands.append(rect)
                    
                    pg.draw.rect(self.screen, self.col['o'],rect)
                    self.screen.blit(self.imgs[imgs[j]],(self.WIDTH/9*5*i+50+60*j,self.HEIGHT*3/4))
        elif obj == 'big':
            for i in range(2):
                #npc
                if player =='npc':
                    img = pg.transform.scale(self.imgs[hands[0]],(100,100))
                    self.screen.blit(img,(50+300*i, self.HEIGHT/2))
    def logic(self):
        ls = [self.npc, self.player_1]
        print(ls)
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
        print(hand)
        hand_leg = {0:'rock',
                    1:'paper',
                    2:'scissors'}
       
        self.player_1 = hand_leg[hand]
        self.npc = hand_leg[random.randint(0,2)]
        self.logic()
        
    


    
    def run(self):
        self.screen.fill(self.col['bg'])
        self.draw('start')
        while True:
            pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    for hand in self.hands:
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
                    return pg.quit
            pg.display.update()
            
Game(600,600).run()