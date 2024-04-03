import customtkinter as ct
import os,sys
from PIL import Image
import importlib.util
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
        imgs = {}
        for folder in os.listdir():
            try:
                imgs[folder] = ct.CTkImage(dark_image=Image.open(folder +'\\assets\\rep.png'),
                                           light_image=Image.open(folder +'\\assets\\rep.png'),
                                           size=(80,60))
               
            except:
                pass

        return imgs
        
    def gui(self):
        imgs = self.get_imgs()
        scr = ct.CTkScrollableFrame(self.root)
        scr.grid(row=0, column=0, pady=10, padx =10, sticky='nswe')

        for i,img in enumerate(imgs):
            frm = ct.CTkFrame(scr, fg_color=self.GREY)
            frm.grid(row=i, column=0, pady=10, padx =10, sticky='nswe')

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