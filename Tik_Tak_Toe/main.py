import pygame as pg
import json


class Game:
    def __init__(self, width, height,*args, **kwargs):
        #TODO: Implement a non odd number possibilitys
        self.HEIGHT = height
        self.WIDTH = width
        self.fields = 3
        pg.init()
        with open("color.json") as f:
                self.col_p = json.load(f)
   
        self.screen = pg.display.set_mode((self.WIDTH,self.HEIGHT+40))
        
        
        self.col = {'bg':self.col_p['blue']['50'],
                    'def_lines':self.col_p['green']['300'], 
                    'lines':self.col_p['green']['300'],
                    'x': self.col_p['red']['300'], 
                    'o':self.col_p['deeppurple']['300']}

        
        
      

        pg.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.start = [None for _ in range(self.fields**2)]
        self.text = self.font.render('press [Space] to start new game', False, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(self.WIDTH/2, self.HEIGHT/2))
        self.place = 'x'
        self.in_prog = False
        self.winner = None

    def draw(self, obj:str, cords:tuple[int,int]=None, player:str = 'x')->None:
        def cmd(self):
            if player == 'o':
                
                pg.draw.line(self.screen,self.col['x'],(10,self.HEIGHT+35),(40, self.HEIGHT+5),5)
                pg.draw.line(self.screen,self.col['x'],(10,self.HEIGHT+5),(40, self.HEIGHT+35),5)
            else:
                pg.draw.circle(self.screen, self.col['o'],(25, self.HEIGHT+20),15,5)
            pg.draw.line(self.screen,self.col['x'],(70,self.HEIGHT+35),(90, self.HEIGHT+5),5)
            pg.draw.line(self.screen,self.col['x'],(90,self.HEIGHT+5),(110, self.HEIGHT+35),5)
            pg.draw.line(self.screen,self.col['x'],(140,self.HEIGHT+5),(160, self.HEIGHT+35),5)
            pg.draw.line(self.screen,self.col['x'],(160,self.HEIGHT+35),(180, self.HEIGHT+5),5)
            
        if obj == 'board':
            self.screen.fill(self.col['bg'])
            for j in range(1,self.fields):
                    #lucky it does not matter here wehre height  and wehere width
                    pg.draw.line(self.screen,self.col['lines'],(j*self.HEIGHT/self.fields,0),(j*self.HEIGHT/self.fields,self.WIDTH),10)
                    pg.draw.line(self.screen,self.col['lines'],(0,j*self.WIDTH/self.fields),(self.HEIGHT,j*self.WIDTH/self.fields),10)
            pg.draw.line(self.screen,self.col['lines'],(0,0),(self.WIDTH,0),10)
            pg.draw.line(self.screen,self.col['lines'],(0,0),(0,self.HEIGHT),10)
            pg.draw.line(self.screen,self.col['lines'],(self.WIDTH,0),(self.WIDTH,self.HEIGHT),10)
            pg.draw.line(self.screen,self.col['lines'],(self.WIDTH,self.HEIGHT-3),(0,self.HEIGHT-3),6)
            cmd(self)
              
        if obj == 'hide_cmd':
            pg.draw.rect(self.screen,self.col['bg'],((0,self.HEIGHT),(self.WIDTH,40)))
            cmd(self)
            
        if obj == 'char':
            if player == 'x':
                #TODO: x is not drawn corectly
                pg.draw.line(self.screen,self.col['x'],(5*self.fields+cords[0]*self.HEIGHT/self.fields,5*self.fields+cords[1]*self.WIDTH/self.fields),((self.HEIGHT*(cords[0]+1)/self.fields)-5*self.fields,((1+cords[1])*self.WIDTH/self.fields)-5*self.fields),10)
                pg.draw.line(self.screen,self.col['x'],(5*self.fields+cords[0]*self.HEIGHT/self.fields,((1+cords[1])*self.WIDTH/self.fields)-5*self.fields),((self.HEIGHT*(cords[0]+1)/self.fields)-5*self.fields,5*self.fields+cords[1]*self.WIDTH/self.fields),10)
            else:
                pg.draw.circle(self.screen, self.col['o'],(cords[0]*self.WIDTH/self.fields+self.WIDTH/(2*self.fields),cords[1]*self.HEIGHT/self.fields+self.HEIGHT/(2*self.fields)),self.WIDTH/(self.fields*2.3),10)
                
    def player(self)->str:
        if self.place == 'x':
            return 'o'
        else:
            return 'x'
    
    def check_game(self):
        winner_arr = {'exeption':[[None]*self.fields,[None]*self.fields],
                      'height':[[None]*self.fields for _ in range(self.fields)], 
                      'width':[[None]*self.fields for _ in range(self.fields)]}
       
        for i in range(self.fields):
            for j in range(self.fields):
                #top to bottom
                if self.start[self.decoder((i,j))]!= None:
                    winner_arr['width'][i][j] =self.start[self.decoder((i,j))]
                    
                #right to left
                if self.start[self.decoder((j,i))] != None:
                    
                    winner_arr['height'][i][j] = self.start[self.decoder((j,i))]
                    
                #top left to bottom right
                if i == j:
                    if  self.start[self.decoder((i,j))] != None:
                        winner_arr['exeption'][0][j] = self.start[self.decoder((i,j))]
                        
                #bottom left to top right
                
        for theme in winner_arr:
         
            for ls in winner_arr[theme]:
                if  ls.count(ls[0]) == len(ls):
                   
                    if None not in ls:
                        self.win(ls[0])

        if None not in self.start:
            self.win('def_lines')
              
    def win(self, winner:str, skip :bool= False)->None:
        
        self.col['lines'] = self.col[winner]
        self.winner = winner
        self.start = [None for _ in range(self.fields**2)]
      
        self.in_prog = False
        
    def decoder(self, cords:tuple[int])->int:
        return cords[1]+cords[0]*self.fields
    
    def label(self)->None:
        text = 'no one won :('
        if self.winner != 'def_lines':
            text = 'Player "{}" was the winner'.format(self.winner)
            
        winner = self.font.render(text, False, (0, 0, 0))
        winner_rect = winner.get_rect(center=(self.WIDTH/2, self.HEIGHT/3))
        if self.winner != None:
            self.screen.blit(winner,winner_rect)
        self.screen.blit(self.text, self.text_rect)
        
    def run(self)->None:
        self.screen.fill(self.col['bg'])
        self.draw('board', player=self.place)
        while True:
            pos = pg.mouse.get_pos()
            self.check_game()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                        cords = (int((pos[1])/(self.WIDTH/self.fields)),int((pos[0])/(self.HEIGHT/self.fields)))
                        if pos[1] >=self.HEIGHT:
                            if self.in_prog is False:
                                if pos[0] <=40:
                                    self.place = self.player()
                                elif 70 <= pos[0] <= 110:
                                        self.fields +=2
                                        self.start = [None for _ in range(self.fields**2)]
                                        self.draw('board')
                                elif 140 <= pos[0] <= 180:
                                    if self.fields != 1:
                                        self.fields -=2
                                        self.start = [None for _ in range(self.fields**2)]
                                        self.draw('board')
                                    
                                self.draw('hide_cmd', player=self.place)
                                
                        elif self.in_prog:
                            if type(self.start[self.decoder(cords)]) != type(str()) :
                        
                                self.place =self.player()
                                self.start[self.decoder(cords)] = self.place
                                self.draw('char', (cords[1],cords[0]),self.place)
                                self.draw('hide_cmd', player=self.place)
                                
                if self.in_prog is False:
                    self.label()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        if self.in_prog is False:
                            self.draw('board', player=self.place)
                            
                        self.in_prog = True
                    if event.key == pg.K_r:
                        self.win('def_lines', skip)
   
                if event.type == pg.QUIT:
                    return pg.quit()
            pg.display.update()



Game(600,600).run()
