import pygame as pg
import itertools
import json


class Game:
    def __init__(self, width, height,*args, **kwargs):
        self.HEIGHT = height
        self.WIDTH = width
        self.fields = 3
        
            
        pg.init()
        with open("color.json") as f:
                self.col_p =json.load(f)
   
        self.screen = pg.display.set_mode((self.HEIGHT,self.WIDTH))
        
        
        self.col = {'bg':self.col_p['blue']['50'],'def_lines':self.col_p['green']['300'], 'lines':self.col_p['green']['300'],'x': self.col_p['red']['300'], 'o':self.col_p['deeppurple']['300']}

        
        
        self.start = [None for _ in range(self.fields**2)]
        self.place = 'x'

        
    
    def draw(self, obj:str, cords:tuple[int,int]=None, player:str = 'x')->None:
        if obj == 'board':
            for j in range(1,self.fields):
                    pg.draw.line(self.screen,self.col['lines'],(j*self.HEIGHT/self.fields,0),(j*self.HEIGHT/self.fields,self.WIDTH),10)
                    pg.draw.line(self.screen,self.col['lines'],(0,j*self.WIDTH/self.fields),(self.HEIGHT,j*self.WIDTH/self.fields),10)
        if obj == 'char':
            print(player)
            if player == 'x':
                
                pg.draw.line(self.screen,self.col['x'],(5*self.fields+cords[0]*self.HEIGHT/self.fields,5*self.fields+cords[1]*self.WIDTH/self.fields),((self.HEIGHT*(cords[0]+1)/self.fields)-5*self.fields,((1+cords[1])*self.WIDTH/self.fields)-5*self.fields),10)
                pg.draw.line(self.screen,self.col['x'],(5*self.fields+cords[0]*self.HEIGHT/self.fields,((1+cords[1])*self.WIDTH/self.fields)-5*self.fields),((self.HEIGHT*(cords[0]+1)/self.fields)-5*self.fields,5*self.fields+cords[1]*self.WIDTH/self.fields),10)
            else:
                
                pg.draw.circle(self.screen, self.col['o'],(cords[0]*self.WIDTH/self.fields+self.WIDTH/(2*self.fields),cords[1]*self.HEIGHT/self.fields+self.HEIGHT/(2*self.fields)),self.WIDTH/(self.fields*2),5)
                
    def player(self)->str:
        if self.place == 'x':
            return 'o'
        else:
            return 'x'
    
    def check_game(self):
        if self.start[0] == self.start[1] == self.start[2] != None:
            self.win(self.start[0])
        if self.start[0] == self.start[4] == self.start[8] != None:
            self.win(self.start[0])
        if self.start[0] == self.start[3] == self.start[6] != None:
            self.win(self.start[0])
        if self.start[3] == self.start[4] == self.start[5] != None:
            self.win(self.start[3])
        if self.start[6] == self.start[7] == self.start[8] != None:
            self.win(self.start[6])
        if self.start[1] == self.start[4] == self.start[7] != None:
            self.win(self.start[1])
        if self.start[2] == self.start[5] == self.start[8] != None:
            self.win(self.start[2])
        if self.start[2] == self.start[4] == self.start[6] != None:
            self.win(self.start[2])
        if None not in self.start:
            self.win('def_lines')
 
                
    def win(self, winner:str)->None:
        
        self.col['lines'] = self.col[winner]
           
        
        self.start = [None for _ in range(self.fields**2)]
        self.place = 'x'
        self.screen.fill(self.col['bg'])
        self.draw('board')
    
    def decoder(self, cords:tuple[int])->int:
        return cords[1]+cords[0]*self.fields
       
    def run(self)->None:
        self.screen.fill(self.col['bg'])

        self.draw('board')
        while True:
            pos = pg.mouse.get_pos()
            
            self.check_game()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    cords = (int((pos[1])/(self.WIDTH/self.fields)),int((pos[0])/(self.HEIGHT/self.fields)))
                    if type(self.start[self.decoder(cords)]) != type(str()) :
                        
                        self.place =self.player()
                        self.start[self.decoder(cords)] = self.place
                        self.draw('char', (cords[1],cords[0]),self.place)
                        
                if event.type == pg.QUIT:
                    return pg.quit()
            pg.display.update()



Game(300,300).run()
