import customtkinter as ct
import os,sys
from PIL import Image
from adfadfad import a
import importlib.util

class game_manager:
    def __init__(self) -> None:
        self.da = os.sep
        self.root = ct.CTk()
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_rowconfigure(0,weight=1)
        WIDTH, HEIGHT = 600, 600
        self.root.geometry('{}x{}'.format(WIDTH, HEIGHT))
        self.GREY = ('#cccccc','#333333')

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
        package, name = f'{game}.py', 'main'
        a.Game().run()
        try:
            spec = importlib.util.spec_from_file_location(name,package)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
        except:
            print(game)
        



    def run(self):
        self.gui()

if __name__ == '__main__':
    game_manager().run()