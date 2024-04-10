import pygame as pg
import json
from random import *
import time
class Game():
    def __init__(self, width:int, height: int,*args, **kwargs) -> None:
        self.HEIGHT = height
        self.WIDTH = width
        self.fields = 3
        pg.init()
        with open("color.json") as f:
                self.col_p = json.load(f)
        self.screen = pg.display.set_mode((self.WIDTH,self.HEIGHT+40))
        
        
        #unique
        self.ROW, self.COLUMN = 8,8

        self.start = [[randint(0,255) for k in range(3)] for i in range(int((self.ROW*self.COLUMN)/2))]
        for pos in self.start:
            pos.append(randint(0,4))
        self.start *=2
        shuffle(self.start)
        
        self.c_len = 60
        
        self.cards = []
        self.rem_cards = []
        
        self.plaing = 0
        self.player = 1
        self.open = []
        self.player_score :dict = {'player_1':0,'player_2': 0}
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        
        self.col = {'bg':self.col_p['blue']['50'],
                    'cards_back':self.col_p['green']['300'], 
                    'cards_bg': self.col_p['red']['300'], 
                    'o':self.col_p['deeppurple']['300']}
        
        
        
    def draw(self, obj: str, card:tuple[int] = (0,0,0,0), cards :list[tuple] = [], col :str ='bg')-> None:
        match obj:
            case 'board':
                self.screen.fill(self.col['bg'])
                for j in range(self.COLUMN):
                    for i in range(self.ROW):
                        card = pg.Rect(25+70*j,15+70*i,self.c_len, self.c_len)
                        self.cards.append(card)     
                        pg.draw.rect(self.screen,self.col['o'],(card[0]-3,card[1]-3,card[2]+6,card[3]+6)
                                     ,width=10 ,border_radius=15)               
                        pg.draw.rect(self.screen,self.col['cards_back'],card, border_radius=15)
                        
            case 'card':
                self.open.append(card)
                self.objs(card)
                
            case 'ret_card':
                time.sleep(1)
                for Card in cards:
                    pg.draw.rect(self.screen,self.col[col],Card, border_radius=15)
            case 'score':
                self.text = self.font.render('Player 1: '+str(self.player_score['player_1']), False, (0, 0, 0))
                self.text_rect = self.text.get_rect(left_center=(20, self.HEIGHT))
                self.screen.blit(self.text,self.text_rect)
    
    def objs(self, rect:tuple[int] =(0,0,0,0)) ->None:
        col = self.start[self.cards.index(rect)]
        obj = col[-1]
        match obj:
            case 0:
                #circle with width
                pg.draw.circle(self.screen, col,(rect[0]+self.c_len/2,rect[1]+ self.c_len/2),25,5)
            case 1:
                #full circle
                pg.draw.circle(self.screen, col,(rect[0]+self.c_len/2,rect[1]+ self.c_len/2),25)
            case 2:
                #full rect
                pg.draw.rect(self.screen, col,(rect[0]+7.5,rect[1]+7.5,rect[2]-15,rect[3]-15),border_radius=4)
            case 3:
                #some polygon
                #star
                pass
            case _:
                pg.draw.rect(self.screen, col,(rect[0]+7.5,rect[1]+7.5,rect[2]-15,rect[3]-15),6,border_radius=15)
    
    def play_score(self,player)->None:
        if player == 0:
            self.player_score['player_1'] +=100
            
        else:
            self.player_score['player_2'] +=100
        
    def run(self):
        self.draw('board')
        while True:
            pos = pg.mouse.get_pos()
            if self.plaing == 2:
                
                col = 'cards_back'
                if self.start[self.cards.index(self.open[0])] == self.start[self.cards.index(self.open[1])]:
                    self.rem_cards.append(self.open[0])
                    self.rem_cards.append(self.open[1])
                    col = 'bg' 
                    self.player_score(self.player)   
                else:
                    if self.player == 0:
                        self.player = 1
                    else:
                        self.player = 0
                    
                    
                self.plaing = 0
                self.draw('ret_card', cards=self.open, col = col)
                self.open = []
                self.draw('score')
                
            for event in pg.event.get():
                if event.type  == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        for i, card in enumerate(self.cards):  
                            if card not in self.rem_cards:
                                if card not in self.open:
                                    if card.collidepoint(pos):
                                        self.plaing += 1
                                        self.draw('card',card)
                                    
                                                        
                if event.type == pg.QUIT:
                    return pg.quit()
            pg.display.update()
Game(600,600).run()