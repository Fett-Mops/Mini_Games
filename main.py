import customtkinter as ct
import os,sys
from PIL import Image
import importlib.util
from icecream import ic
#words_hints.json from https://github.com/le717/PHP-Hangman/tree/master
#color.json form #color pallete from here https://gist.github.com/kawanet/a880c83f06d6baf742e45ac9ac52af96


class game_manager:
    def __init__(self) -> None:
        self.da = os.sep
        self.root = ct.CTk()
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_rowconfigure(0,weight=1)
        self.WIDTH, self.HEIGHT = 600, 600
        self.root.geometry('{}x{}'.format(self.WIDTH, self.HEIGHT))
        self.GREY = ('#cccccc','#333333')
        self.games_dict = {}
        

    def get_imgs(self)  -> dict:
        global img_counter
        imgs = {}
        for folder in os.listdir():
            if '.' not in folder :
              
                img_counter = 0 
                try:
                    img = [self.path_imgs(folder) for _ in range(2)]
                
                    if '' in img:
                        if img.index('') == 0:
                          
                            img[0] = img[1]
                        else:
                            img[1] = img[0]
                    for i in range(2):
                        img[i] = Image.open(img[i])
            
                    imgs[folder] = ct.CTkImage(dark_image=img[0],
                                               light_image=img[1],
                                               size=(self.format_imgs(img[0])))
               
                except:
                    raise ImportError()
        return imgs
    
    def path_imgs(self,folder:str)->str:
        global img_counter
        path = ''
        mini_dic = {0 : 'white\\', 1 : 'black\\'}
        img_types : list[str] =['png','jpg']
 
        for type in  img_types:
            try:
                path_str = folder +'\\assets\\{}rep.'.format(mini_dic[img_counter],type)
                path : os.path = os.path.join(path_str)
                if os.path.exists(path):
                    break
                
                path_str = folder +'\\assets\\rep.{}'.format(type)
                path : os.path = os.path.join(path_str)
        
                if os.path.exists(path):
                    break
                else:
                    path = ''
            except:
                    raise FileNotFoundError()
     
        img_counter += 1
        return path
        
    def format_imgs(self, img:Image) ->tuple[int]:
        h, w = img.size
        propotion = w/h
        if propotion != 1:
            if propotion < 1:
             
                return(256,256*propotion)
            else:
                return(256*(propotion**-1),256)
        else:
            return (256,256)
    
    def gui(self):
        imgs = self.get_imgs()
        scr = ct.CTkScrollableFrame(self.root)
        scr.grid(row=0, column=0, pady=10, padx =10, sticky='nswe')

        for i,img in enumerate(imgs):
            frm = ct.CTkFrame(scr, fg_color=self.GREY)
            frm.grid(row=i, column=0, pady=10, padx =10, sticky='nswe')
            frm.grid_columnconfigure(0,weight=1)

            button = ct.CTkButton(frm, fg_color='transparent', text='', image=imgs[img], hover=False,
                                  command=lambda img = img: self.start_game(img))
            button.grid(row=0, column=0, pady=10, padx =10, sticky='nswe')

            lable = ct.CTkLabel(frm, text=img)
            lable.grid(row=1, column=0, pady=10, padx =10, sticky='nswe')

        self.root.mainloop()
    
    def start_game(self, game):
    
        
       
        imp_game = importlib.import_module(game + ".main")
        game_init = imp_game.Game(self.WIDTH,self.HEIGHT).run()
   
    def run(self):
        self.gui()

if __name__ == '__main__':
    game_manager().run()