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
        self.ROW, self.COLUMN = 5,6
        #self.start = [i for i in range(int((self.ROW*self.COLUMN)/2)) for j in range(2)]
        self.start = [[randint(0,255) for k in range(3)] for i in range(int((self.ROW*self.COLUMN)/2))]*2
        print(self.start)
        shuffle(self.start)
        self.c_len = 60
        
        self.cards = []
        self.rem_cards = []
        
        self.plaing = 0
        self.open = []
        
        self.player_1 = 0
        self.player_2 = 0   
        
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
                        card = pg.Rect(10+70*j,10+70*i,self.c_len, self.c_len)
                        self.cards.append(card)                    
                        pg.draw.rect(self.screen,self.col['cards_back'],card, border_radius=15)
            case 'card':
                self.open.append(card)
                self.objs(card)
            case 'ret_card':
                time.sleep(1)
                for Card in cards:
                    pg.draw.rect(self.screen,self.col[col],Card, border_radius=15)
    
    def objs(self, rect:tuple[int] =(0,0,0,0)) ->None:
        col = self.start[self.cards.index(rect)]
        obj = self.start.index(col)
        match obj:
            case 0:
                #circle with width
                pg.draw.circle(self.screen, col,(rect[0]+self.c_len/2,rect[1]+ self.c_len/2),25,5)
            case 1:
                #full circle
                pg.draw.circle(self.screen, col,(rect[0]+self.c_len/2,rect[1]+ self.c_len/2),25)
            case 2:
                #full rect
                pg.draw.rect(self.screen, col,rect)
            case 3:
                #some polygon
                #star
                pass
            case _:
                pg.draw.rect(self.screen, col,rect,7)
            
                             
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
                self.plaing = 0
                self.draw('ret_card', cards=self.open, col = col)
                self.open = []
               
            for event in pg.event.get():
                if event.type  == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        for i, card in enumerate(self.cards):  
                            if card not in self.rem_cards:
                                if card.collidepoint(pos):
                                    self.plaing += 1
                                    self.draw('card',card)
                                    
                                                        
                if event.type == pg.QUIT:
                    return pg.quit()
            pg.display.update()
Game(600,600).run()