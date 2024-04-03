import pygame as pg
import itertools
import json
HEIGHT = 750
WIDTH = 750
fields = 3

with open("C:/Users/mirco/OneDrive/Desktop/Projekte/Programming/color.json") as f:
    col_p =json.load(f)
winner_col = col_p['green']['300']
col = {'bg':col_p['blue']['50'],'lines':winner_col, 'cross': col_p['red']['300'], 'circle':col_p['deeppurple']['300']}

class Tick_Tack_Toe:
    def __init__(self):
        pg.init()
        
        self.screen = pg.display.set_mode((HEIGHT,WIDTH))
        self.start = [[None for _ in range(fields)] for _ in range(fields)]
        self.place = 'X'
        self.x = []
        self.o = []
        
    
    def draw(self, obj:str, cords:tuple[int,int]=None, player:str = 'X')->None:
        if obj == 'board':
            for j in range(1,fields):
                    pg.draw.line(self.screen,col['lines'],(j*HEIGHT/fields,0),(j*HEIGHT/fields,WIDTH),10)
                    pg.draw.line(self.screen,col['lines'],(0,j*WIDTH/fields),(HEIGHT,j*WIDTH/fields),10)
        if obj == 'char':
            print(player)
            if player == 'X':
                self.x.append(cords)
                pg.draw.line(self.screen,col['cross'],(5*fields+cords[0]*HEIGHT/fields,5*fields+cords[1]*WIDTH/fields),((HEIGHT*(cords[0]+1)/fields)-5*fields,((1+cords[1])*WIDTH/fields)-5*fields),10)
                pg.draw.line(self.screen,col['cross'],(5*fields+cords[0]*HEIGHT/fields,((1+cords[1])*WIDTH/fields)-5*fields),((HEIGHT*(cords[0]+1)/fields)-5*fields,5*fields+cords[1]*WIDTH/fields),10)
            else:
                self.o.append(cords)
                pg.draw.circle(self.screen, col['circle'],(cords[0]*WIDTH/fields+WIDTH/(2*fields),cords[1]*HEIGHT/fields+HEIGHT/(2*fields)),WIDTH/(fields*2),5)
                #pg.draw.ellipse(self.screen,col['lines'],((cords[0]*WIDTH/fields+WIDTH/(2*fields)-HEIGHT/12, cords[1]*HEIGHT/fields+HEIGHT/(2*fields)-WIDTH/12),(HEIGHT/6,WIDTH/6)),10)
#(self.screen, col['lines'],(, (cords[0]*WIDTH/fields+30, cords[1]*HEIGHT/fields+30)
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
        global winner_col
        winner_col = col_p['red']['300']
        dic = {1:'X', 0 :'O'}
        print(dic[winnter])
        print(self.o)
        print(self.x)
        self.draw('board')
    def run(self)->None:
        self.screen.fill(col['bg'])

        self.draw('board')
        while True:
            pos = pg.mouse.get_pos()
            self.check_game()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    cords = (int((pos[1])/(WIDTH/fields)),int((pos[0])/(HEIGHT/fields)))
                    if self.start[cords[0]][cords[1]] == None:
                        self.place =self.player()
                        self.start[cords[0]][cords[1]] = self.place
                        self.draw('char', (cords[1],cords[0]),self.place)
                if event.type == pg.QUIT:
                    exit()
            pg.display.update()




if __name__ =='__main__':
    run = Tick_Tack_Toe()
    run.run()