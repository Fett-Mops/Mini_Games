import pygame as pg
from typing import Tuple, Iterable
import itertools
import copy

#column = 0
#row = 1
col ={'white':(255,255,255),
      'black':(0,0,0),
      'w': (254, 255, 236),
      'b':(35,43,43),
      'P':(100,100,100),
      'T':(204, 202, 92),
      'H':(149, 207, 57),
      'B':(149, 20, 7),
      'K':(255, 207, 57),
      'D':(149, 207, 255),
      'red': (255,0,0)}

class Schach:
    def __init__(self) -> None:
        pg.init()
        self.figs = []
        self.screen = pg.display.set_mode((600,600))
        self.start = [['Tb','Hb','Bb','Db','Kb','Bb','Hb','Tb'],
                      ['Pw','Pb','Pb','Pb','Db','Pb','Pb','Pb'],
                      ['XX','XX','XX','XX','Dw','Dw','XX','XX'],
                      ['XX','XX','XX','XX','XX','XX','XX','XX'],
                      ['XX','XX','XX','XX','XX','XX','XX','XX'],
                      ['XX','XX','XX','XX','XX','XX','XX','XX'],
                      ['XX','XX','XX','XX','XX','XX','XX','XX'],
                      #['Pw','Pw','Pw','Pw','Pw','Pw','Pw','Pw'],
                      ['Tw','Hw','Bw','Dw','Kw','Bw','Hw','Tw']]
        self.option_translater = {0:'H', 1:'B',2:'T', 3:'D'}

        self.Pesants = {'w': [False for _ in range(8)],'b': [False for _ in range(8)]}
        self.moving = False
        self.scords = None
        self.already_protecting = False
        self.marks = []
        self.objmarks = []
        self.cords = ()
        
    def draw(self, obj:str, **kargs)->pg.Rect | None :
       
        match obj:
            case 'board':
                color = 'white'
                for i in range(0,8):
                    if color == 'black':
                            color = 'white'
                    else:
                            color ='black'
                            
                    for j in range(0,8):
                        
                        if color == 'black':
                            color = 'white'
                        else:
                            color ='black'
                        
                       
                        pg.draw.rect(self.screen, col[color], (j*75,i*75 , 75, 75)) 
                        if self.start[i][j] != 'XX':
                            if self.start[i][j][1] == 'w':
                                pg.draw.rect(self.screen, col[self.start[i][j][0]], ((j*75)+10+2.5,(i*75) +10+2.5 , 50, 50)) 
                            else:
                                pg.draw.circle(self.screen,col[self.start[i][j][0]],((j*75)+37.5,(i*75) +37.5 ), 30)
                      
                      
            case 'circle':
                
                cord = kargs['mov']
                
                pg.draw.circle(self.screen, col['red'], ((cord[1]*75)+37.5,(cord[0]*75)+37.5),13) 
            case 'cross':
                cord = kargs['mov']
              
                
                pg.draw.circle(self.screen, col['red'], ((cord[1]*75)+37.5,(cord[0]*75)+37.5),30,5)
            case 'selection':
              
                cord = kargs['sel']
                drawing =pg.draw.circle(self.screen, col['red'], ((cord[1]*75)+37.5,(cord[0]*75)+37.5),30,5)
                return pg.Rect(drawing)
            case 'case':
  
                cord = kargs['sel']
          
                pg.draw.rect(self.screen, col['T'], ((cord[1]*75),(cord[0]*75),300,75),0,13)            
                        
    def show_move(self, cords: tuple[int,int],*args)->None:
        self.moving = True
        if self.idk_why == None:
            self.draw('board')
        
        self.marks= []
        self.objmarks = []
        self.movement(cords,self.start)
        for i,mark in enumerate(self.marks):
            self.draw(self.objmarks[i],mov=mark)
            
        
    def movement(self, cords: tuple[int,int], start:dict[list[list[str]]]):

            match start[cords[0]][cords[1]][0]:
                case 'H':
                    moves =[(1,2),(-1,2),(1,-2),(-1,-2),(2,1),(-2,1),(2,-1),(-2,-1)]
                    for i,j in moves:
                        cord = ((cords[0]+i),(cords[1]+j))
                        self.Hitbox_check((cords[0],cords[1]),self.cord_check(cord),start)    
                        
                case 'B'|'D'|'T' :
                    if start[cords[0]][cords[1]][0] != 'T':
                        for i in [1,-1]:
                            for j in [1,-1]:
                                for k in range(1,8):
                                    cord =((cords[0]+k*i),(cords[1]+k*j))

                                    if self.Hitbox_check((cords[0],cords[1]),self.cord_check(cord),start) != None:
                                        break

                                    
                    if start[cords[0]][cords[1]][0] != 'B':    

                    
                        for k in [1,-1]:  
                             for i in range(1,9):
                                cord = ((cords[0]),(cords[1]+k*i))

                                if self.Hitbox_check((cords[0],cords[1]),self.cord_check(cord),start) != None:
                                    break
                                
                        for k in [1,-1]:    
                            for i in range(1,9):          
                                cord = (cords[0]+k*i,(cords[1]))

                                if self.Hitbox_check((cords[0],cords[1]),self.cord_check(cord),start) != None:
                                    break
                case 'K':
                    for k in itertools.product(range(-1, 2), repeat=2):
                        if k != (0, 0):
                            cord = ((cords[0]+k[0])),((cords[1]+k[1]))
                            self.Hitbox_check((cords[0],cords[1]),self.cord_check(cord),start)

                #Enpansante
                case 'P':
                    for i in range(-1,2):

                        check, y = None, 1
                        if start[cords[0]][cords[1]][1] == 'w':
                            y = -1
                        cord = ((cords[0]+y),(cords[1]+i))
                        check = self.Hitbox_check((cords[0],cords[1]),self.cord_check(cord),start)
                        if check != 1:
                            if i==0:                           
                                if start[cords[0]][cords[1]][1] == 'w':
                                    if cords[0] == 6:
                                    
                                        self.Hitbox_check((cords[0],cords[1]),self.cord_check(((cords[0]-2),(cords[1]))),start)

                                else:
                                    if cords[0] == 1:
                                        self.Hitbox_check((cords[0],cords[1]),self.cord_check(((cords[0]+2),(cords[1]))),start)    

                    var = (-1,'b') if start[cords[0]][cords[1]][1] == 'w' else (1,'w')

                    for i in [1,-1]:
                        if 0 <= i+cord[1] <= 7 and 0 <= cord[1]+i <= 7:
                            if start[cords[0]][cords[1] +i] == 'P'+var[1]:
                                if self.Pesants[var[1]][cords[1]+i]:
                                    self.Hitbox_check((cords[0],cords[1]),self.cord_check(((cords[0]+var[0]),(cords[1]+i))),start,skip=True)
           
    def king_under_attack(self, start:dict[list[list[str]]]) -> bool:
      
        ls = {'w': [None,[]], 'b': [None,[]]}
        for k,y in enumerate(start):
            for j,i in enumerate(start[k]):
                if start[k][j] != 'XX':
                    if start[k][j][0] == 'K':
                        ls[start[k][j][1]][0]  = (k,j)
                        
                    
                    self.marks = []
                    self.movement((k,j),start)
                    self.marks.append([k,j])
                    
                    ls[start[k][j][1]][1].append(self.marks)
        
        for marks in ls['b'][1]:
            if ls['w'][0] in marks :
                if not self.already_protecting:
                   self.protect_king(ls['w'][0], marks, ls)
                else:
                    print(marks, ls['w'][0])
                
                    return False
            
        if not self.already_protecting:
                 
                    return True
                
   
    def protect_king(self, king_pos: Tuple[int, int], attacker:Tuple[int,int], ls:dict['w':[tuple[int,int],[tuple[int]]],'b': [tuple[int,int],[[tuple[int]]]]]) -> list[Tuple[int, int]]:
        valid_moves = []
        self.already_protecting = True
        for marks in ls['w'][1]:
            piece = marks[-1]
            marks.pop(-1)
            for move in marks:
                if self.king_check_after((piece), move):
                    print(move)
                    valid_moves.append(move)
        self.already_protecting = False
        for i,mark in enumerate(valid_moves):
            self.draw(self.objmarks[i],mov=mark)
        print(valid_moves)
             
    def king_check_after(self,cord:tuple[int,int],target:tuple[int,int]):
        start_cp = copy.deepcopy(self.start)   
        #print(start_cp[target[0]][target[1]],start_cp[cord[0]][cord[1]] )
        start_cp[target[0]][target[1]] =start_cp[cord[0]][cord[1]] 
        
        start_cp[cord[0]][cord[1]] = 'XX'
        if self.king_under_attack(start_cp):
            return True
                                               
    def cord_check(self, cord:tuple[int,int])->tuple[int,int] | None:
        if 0 <= cord[0] <= 7 and 0 <= cord[1] <= 7:
            return cord
        return None
   
    def Hitbox_check(self, cords:tuple[int,int] ,target:tuple[int,int], start:dict[list[list[int]]],skip:str = False)->int | None:
        piece = start[cords[0]][cords[1]]
        if target == None:
            return None
        if start[target[0]][target[1]][1] == piece[1]:
            return 8       
        elif  piece[0] == 'P':
           
                if start[target[0]][target[1]][1] != piece[1] and start[target[0]][target[1]] != 'XX' and target[1] != cords[1] :
                    self.marks.append(target) 
                    self.objmarks.append('cross')
                elif skip:
                    self.scords = target
                    self.marks.append(target) 
                    self.objmarks.append('cross') 
                elif target[1] == cords[1] :
              
                    if start[target[0]][target[1]] == 'XX' :
                        self.marks.append(target) 
                        self.objmarks.append('circle')

                     
                       
                    else:
                        return 1
                else: 
                    return 7
                
        elif start[target[0]][target[1]][1] != piece[1] and start[target[0]][target[1]] != 'XX':
            self.marks.append(target) 
            self.objmarks.append('cross')
            return 9

            
        else:      
            self.marks.append(target) 
            self.objmarks.append('circle')
        
    def move(self, cords:tuple[int,int], target: tuple[int,int],skip:tuple[int,int])->None:
        self.start[target[0]][target[1]] = self.start[cords[0]][cords[1]] 
        self.start[cords[0]][cords[1]] = 'XX'
        if skip != None:
            self.scords = None
        
            if self.start[target[0]][target[1]][1] == 'w':
        
                self.start[target[0]+1][target[1]] = 'XX'
            else:
                self.start[target[0]-1][target[1]] = 'XX'
        self.draw('board')
        self.cords = ()
        self.marks = []
        self.moving = False
        self.Pesants = self.Pesants = {'w': [False for _ in range(8)],'b': [False for _ in range(8)]}
        if self.start[target[0]][target[1]][0] == 'P' :    
            if abs(target[0] - cords[0]) == 2:
                self.Pesants[self.start[target[0]][target[1]][1]][cords[1]] = True
            if target[0] == 7 or target[0] == 0:
                self.transformation(target)
                        
    def transformation(self, cords:tuple[int,int])->str:
        
        self.idk_why =True
        options = []
        k = -1.5
        if cords[1] == 0:
                k= 0
        elif cords[1] == 1:
            k = -1
        elif cords[1] == 6:
                k = -2
        elif cords[1]==7:
                k=-3
        if cords[0] ==0:
            self.draw('case', sel=((cords[0]+1),(cords[1]+k))) 
        else:
            self.draw('case', sel=((cords[0]-1),(cords[1]+k)))
       
        for i in range(4):
      
            if cords[0] == 0:                
                options.append(self.draw('selection',sel=((cords[0]+1),(cords[1]+i+k)) ))             
            else:
                options.append(self.draw('selection',sel=((cords[0]-1),(cords[1]+i+k))))
        self.option = True
        self.cords = cords
        self.figs=options
    
    def opt_choser(self)->str:
        var = None
        for i in self.figs:
            if i.collidepoint(self.pos):
                var = self.figs.index(i)
                self.start[self.cords[0]][self.cords[1]] = self.option_translater[var]+self.start[self.cords[0]][self.cords[1]][1]
                self.cords = None
                self.draw('board')
                self.option = False
           
    def run(self)-> None:
        self.draw('board')
        self.option = False
      
        while True:
            
            self.pos = pg.mouse.get_pos()
          
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        
                        self.draw('board')
                        self.marks, self.objmarks = [],[]
                        self.moving = False
                    
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.idk_why = None
                    if not self.option:
                        if self.moving  :
                        #print(self.marks,( int(self.pos[0]/75),int(self.pos[1]/75),))
                            if (int(self.pos[1]/75), int(self.pos[0]/75)) in self.marks:
                                self.move(self.cords,(int(self.pos[1]/75), int(self.pos[0]/75)), self.scords)
                            else:
                            
                                self.moving = False
                            
                        if not self.moving:
                            self.marks = []
                            self.cords = (int(self.pos[1]/75), int(self.pos[0]/75))
                            self.king_under_attack(self.start)
                            
                            
                            self.show_move(self.cords)
                            
                            
                      
                    else:
                        self.opt_choser()
                        
                        
                if event.type == pg.QUIT:
                    exit()
        
            pg.display.flip()
      
if __name__ == '__main__':
    run = Schach()
    run.run()