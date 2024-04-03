import pygame as pg
import itertools
import json


class Game:
    def __init__(self, width, height, *args, **kwargs):
        pg.init()
        self.HEIGHT = height
        self.WIDTH = width
        self.fields = 3
        with open("C:/Users/mirco/OneDrive/Desktop/Projekte/Programming/color.json") as f:
            self.col_p =json.load(f)
        self.winner_col = self.col_p['green']['300']
        self.col = {'bg':self.col_p['blue']['50'],'lines':self.winner_col, 'cross': self.col_p['red']['300'], 'circle':self.col_p['deeppurple']['300']}

        
        self.screen = pg.display.set_mode((self.HEIGHT,self.WIDTH))
        self.start = [[None for _ in range(self.fields)] for _ in range(self.fields)]
        self.place = 'X'
        self.x = []
        self.o = []
        
    
    def draw(self, obj:str, cords:tuple[int,int]=None, player:str = 'X')->None:
        if obj == 'board':
            for j in range(1,self.fields):
                    pg.draw.line(self.screen,self.col['lines'],(j*self.HEIGHT/self.fields,0),(j*self.HEIGHT/self.fields,self.WIDTH),10)
                    pg.draw.line(self.screen,self.col['lines'],(0,j*self.WIDTH/self.fields),(self.HEIGHT,j*self.WIDTH/self.fields),10)
        if obj == 'char':
            print(player)
            if player == 'X':
                self.x.append(cords)
                pg.draw.line(self.screen,self.col['cross'],(5*self.fields+cords[0]*self.HEIGHT/self.fields,5*self.fields+cords[1]*self.WIDTH/self.fields),((self.HEIGHT*(cords[0]+1)/self.fields)-5*self.fields,((1+cords[1])*self.WIDTH/self.fields)-5*self.fields),10)
                pg.draw.line(self.screen,self.col['cross'],(5*self.fields+cords[0]*self.HEIGHT/self.fields,((1+cords[1])*self.WIDTH/self.fields)-5*self.fields),((self.HEIGHT*(cords[0]+1)/self.fields)-5*self.fields,5*self.fields+cords[1]*self.WIDTH/self.fields),10)
            else:
                self.o.append(cords)
                pg.draw.circle(self.screen, self.col['circle'],(cords[0]*self.WIDTH/self.fields+self.WIDTH/(2*self.fields),cords[1]*self.HEIGHT/self.fields+self.HEIGHT/(2*self.fields)),self.WIDTH/(self.fields*2),5)
                #pg.draw.ellipse(self.screen,col['lines'],((cords[0]*WIDTH/self.fields+WIDTH/(2*self.fields)-self.HEIGHT/12, cords[1]*self.HEIGHT/self.fields+self.HEIGHT/(2*self.fields)-WIDTH/12),(self.HEIGHT/6,WIDTH/6)),10)
#(self.screen, col['lines'],(, (cords[0]*WIDTH/self.fields+30, cords[1]*self.HEIGHT/self.fields+30)
    def player(self)->str:
        if self.place == 'X':
            
            return 'O'
        else:
            return 'X'
    
    def check_game(self):
        win = ''
        ls = [self.o, self.x]
        for i, li in enumerate(ls):
            if ((0,0) and (0,1) and(0,2)) in li:
                self.win(i)        
            if ((0,0) and  (1,0) and (2,0)) in li:
                self.win(i)
            if ((0,0) and (1,1) and (2,2)) in li:
                self.win(i)
            if ((0,1) and (1,1) and (2,1)) in li:
                self.win(i)
            if ((0,2) and ( 1,2) and (2,2)) in li:
                self.win(i)
            if ((1,0) and (1,1) and (1,2)) in li:
                self.win(i)
            if ((2,0) and (2,1) and (2,2)) in li:
                self.win(i)
            if ((2,0) and (1,0) and (0,2)) in li:
                self.win(i)
 
                
    def win(self, winnter:str)->None:
        
        self.winner_col = self.col_p['red']['300']
        dic = {1:'X', 0 :'O'}
        print(dic[winnter])
        print(self.o)
        print(self.x)
        self.draw('board')
    def run(self)->None:
        self.screen.fill(self.col['bg'])

        self.draw('board')
        while True:
            pos = pg.mouse.get_pos()
            self.check_game()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    cords = (int((pos[1])/(self.WIDTH/self.fields)),int((pos[0])/(self.HEIGHT/self.fields)))
                    if self.start[cords[0]][cords[1]] == None:
                        self.place =self.player()
                        self.start[cords[0]][cords[1]] = self.place
                        self.draw('char', (cords[1],cords[0]),self.place)
                if event.type == pg.QUIT:
                    return pg.quit()
            pg.display.update()




