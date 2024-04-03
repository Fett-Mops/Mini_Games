import pygame as pg 
import time



class Game:
    def __init__(self, width, height, *args, **kwargs) -> None:
        #TODO: Implement resising ROW/COLUMNS
        #TODO: Implement Back to gui
        self.cords = {}
        self.COLUMN = 76
        self.ROW = 43
        self.col ={True:(255, 250, 129),False:(218, 184, 148),'bg' : (72, 181, 163), 'black':(0,0,0)}
   
        pg.init()
        pg.display.set_caption("Game of Live")
        self.screen = pg.display.set_mode((width,height), pg.RESIZABLE)
        
       
        self.bits =  [[[]for _ in range(self.ROW)] for _ in range(self.COLUMN)]    
        self.update = []
        
        
    def draw(self, spec:str=False, cord:tuple[int,int]=(-1,-1), bl:bool=False)->None:
        if spec == 'setup':
           
            for j in range(self.ROW):
                for i in range(self.COLUMN):
                    if len(self.bits[i][j]) == 3:
                        if self.bits[i][j][1]:
                            pg.draw.rect(self.screen,self.col[True],(10+int(i)*25, 10+int(j)*25, 20, 20))
                        else:
                            pg.draw.rect(self.screen,self.col[False],(10+int(i)*25, 10+int(j)*25, 20, 20))
                    else:
                        pg.draw.rect(self.screen,self.col[False],(10+int(i)*25, 10+int(j)*25, 20, 20))
                        self.bits[i][j].append((i,j))
                        self.bits[i][j].append(False)
                        self.bits[i][j].append(0)
                        
                            
        else:
       
        
            pg.draw.rect(self.screen,self.col[bl],(10+cord[0]*25, 10+cord[1]*25, 20, 20))
            self.bits[cord[0]][cord[1]][1] =bl    
            
    def step(self, ls:list[tuple[int,int]]):
        for j in range(self.COLUMN):
            for i in range(self.ROW):
                   
                    self.draw(cord=(i,j),bl= self.bits[i][j][0] in ls )
                    
    def checker(self):
        neigbors = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        self.update = []
        for j in range(self.COLUMN):
            for i in range(self.ROW):
                self.bits[i][j][2] =0
                for k in neigbors:
                    if self.in_range(i,j,k):
                        if self.bits[i+k[0]][j+k[1]][1]:
                            self.bits[i][j][2] +=1
                            
                self.rules(i,j)
   
    def rules(self, i:int, j:int)->None:
     
        #? Any live cell with fewer than two live neighbors dies, as if by underpopulation.
        #? Any live cell with two or three live neighbors lives on to the next generation.
        #? Any live cell with more than three live neighbors dies, as if by overpopulation.
        #? Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
      
        if self.bits[i][j][1]: # Check if cell is alive
            if self.bits[i][j][2] == 2 or self.bits[i][j][2] == 3: # Survival
                self.update.append((i, j))
            elif self.bits[i][j][2] > 3: # Overpopulation
                pass
        else: # Cell is dead
            if self.bits[i][j][2] == 3: # Reproduction
                self.update.append((i, j))   
                            
    def in_range(self, i:int,j:int,k:tuple[int,int])->bool:
        x = int(k[0]) + i
        y = int(k[1]) + j
        if -1 < x < self.ROW and  -1 < y < self.COLUMN:
            return True
        return False
  
    def run(self)->None:
        
        s = False
        while True:
            
            
            if s:
                time.sleep(0.2)
                self.screen.fill(self.col['bg'])
                self.checker()
                self.step(self.update) 
            else:
                
                self.screen.fill(self.col['black'])
                self.draw('setup')
                
            
            pos  = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_a:
                        if s:
                            s = False
                        else:
                            s = True
                        
                               
                if event.type == pg.MOUSEBUTTONDOWN:
                    tp = (int((-10+pos[0])/25),int((-10+pos[1])/25))
                    try:
                        self.draw(cord=tp, bl=bool(not self.bits[tp[0]][tp[1]][1]))
                    except:
                        pass

                if event.type == pg.QUIT:
                    return pg.quit()
                
                elif event.type == pg.VIDEORESIZE:
                    # Update screen dimensions if window is resized
                    self.screen_width = event.w
                    self.screen_height = event.h
                    self.screen = pg.display.set_mode((self.screen_width, self.screen_height), pg.RESIZABLE)
        

            
            pg.display.flip()
    
    

