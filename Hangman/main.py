import customtkinter as ct
import json
import random
from PIL import Image, ImageTk
root = ct.CTk()
font_1 =("Comic Sans MS", 40, "bold") 
font_2 =("Comic Sans MS", 30, "bold") 
chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
fguess = ''
rguess= ''
st_var =ct.StringVar(value='start')
counter = 0
var_list, let_list ,charsl= [], [], []
white ='#ffffff'
green = '#77DD77'
red = '#FF6961'

#pictures

pngs = [ ct.CTkImage(dark_image=Image.open(f"C:/Users/mirco/OneDrive/Desktop/Projekte/Programming/Python/2WP/Games/Hangman/assets/White/Hangman_{i}.png"),
                      light_image=Image.open(f"C:/Users/mirco/OneDrive/Desktop/Projekte/Programming/Python/2WP/Games/Hangman/assets/Black/Hangman_{i}.png"),
                      size=(417.8571428571429,450)) for i in range(-1,10)]
# Todo: öüä übersetzer

def read_json(path:str)->any:
        with open (path) as f:
            return json.load(f)
        
def underscore(word:str)->None:
    for i,letter in enumerate(word):
        var_list.append(ct.StringVar(value='_'))
        let_list.append(letter.capitalize())
        frm_1.grid_columnconfigure(i,weight=1)
        l = ct.CTkLabel(frm_1,text='2', textvariable=var_list[i],font=font_1)
        l.grid(row=0, column=i,sticky='we', padx=5)
        
def start()->None:
    global frm_1, var_list, let_list, charsl, fguess, rguess, counter
 
    
    if st_var.get() == 'start':
        var_list, let_list = [], []
        for letter in charsl:
            letter.configure(text_color=white)
        fguess=''
        rguess = ''
        counter = -1
        image_handler(counter)
        st_var.set('give Up')
        
        frm_1.destroy()
        frm_1 = ct.CTkFrame(root,width=300,height=300)
        frm_1.grid(row=0,column=0, pady=5, padx=5,sticky='nswe')
        frm_1.grid_rowconfigure(0,weight=1)
        
        word = read_json('C:/Users/mirco/OneDrive/Desktop/Projekte/Programming/Python/2WP/Games/Hangman/words.json')
        
        underscore(word[random.randint(0,len(word)-1)])
        
    else:
        image_handler(8)
        end(False)

def answer()->None:
    st_var.set('start')
    for i, let in enumerate(let_list):
        var_list[i].set(let_list[i]) 
    
def end(bool:bool)->None:   
    if bool:
        image_handler(-2)
        st_var.set('start')
        
        
    else:
        
        answer()
    for letter in chars:
        if letter in let_list:
            charsl[chars.index(letter)].configure(text_color=green)
        else:
            charsl[chars.index(letter)].configure(text_color=red)
    
def hint()->None:
    pass

def show(event:tuple)->None:
    letter = event.char.capitalize()
    bl = False
    for i,let in enumerate(let_list):
        if let.capitalize() == letter:
            bl = True
            var_list[i].set(let_list[i])
            try:
                charsl[chars.index(letter)].configure(text_color=green )
            except:
                print('mistacke')
            
    if bl:
        right(letter)
    else:
        mist(letter)

def right(letter:chr)->None:
    global rguess
    rguess += letter
    bl = True
    print(rguess,let_list)
    for let in let_list:
        if let not in rguess:
            bl = False
    if bl:
        end(True)
            
def mist(letter:chr)->None:
    global counter ,chars, fguess   
    try:
        if letter not in fguess:
            charsl[chars.index(letter)].configure(text_color=red)
            fguess+=letter
            counter +=1 
    except:
        print('mistacke')
    if counter < 8:
        image_handler(counter)
    else:
        image_handler(-3)
        end(False)

def letters()->None:
    for i,char in enumerate(chars):
        frame = ct.CTkFrame(frm_2, fg_color='transparent')
        
        if i >= 13:
            x = 1
            y = (13-i)*-1
        else:
            x = 0
            y = i
            
        frame.grid(row=x, column=y, pady=5, padx=5, sticky='nswe')
        frame.grid_columnconfigure(0,weight=1)
        frame.grid_rowconfigure(0, weight=1)
        lable = ct.CTkLabel(frame, text=char, font=font_2)    
        lable.grid(row=0, column=0, sticky='nswe')
        charsl.append(lable)
   
def image_handler(counter:int)->None:
    img_but.configure(image=pngs[counter+1])
    
root.grid_columnconfigure(0,weight=2)
root.grid_columnconfigure(1,weight=1)
root.grid_rowconfigure([0,1],weight=1)
root.bind("<Key>",show)

frm_1 = ct.CTkFrame(root,width=300,height=300)
frm_1.grid(row=0,column=0, pady=5, padx=5,sticky='nswe')
frm_1.grid_rowconfigure(0,weight=1)

frm_2 = ct.CTkFrame(root)
frm_2.grid(row=1,column=0, padx=5,pady=(0,5),sticky='nswe')
frm_2.grid_columnconfigure([0,1,2,3,4,5,6,7,8,9,10,11,12,13],weight=1)
frm_2.grid_rowconfigure([0,1],weight=1)

frm_3 = ct.CTkFrame(root)
frm_3.grid(row=0,column=1,pady=5, padx=(0,5),sticky='nswe')
def test():
    print('leave the pole alone you Mole!')

frm_3.grid_columnconfigure(0,weight=1)
frm_3.grid_rowconfigure(0,weight=1)
img_but = ct.CTkButton(frm_3,text='', hover=False, image=pngs[0],command=test, fg_color='transparent')
img_but.grid(row=0,column=0, sticky='nswe')

frm_4 = ct.CTkFrame(root)
frm_4.grid(row=1,column=1,pady=(0,5), padx=(0,5),sticky='nswe')

frm_4.grid_rowconfigure([0,1],weight=1)
frm_4.grid_columnconfigure(0, weight=1)

st_but = ct.CTkButton(frm_4, text='start',textvariable=st_var, command=start)
st_but.grid(row=0,column=0,sticky='nswe',pady=5,padx=5)

tipp_but = ct.CTkButton(frm_4,text='hint' ,command=hint)
tipp_but.grid(row=1,column=0,sticky='nswe',pady=(0,5),padx=5)

letters()

root.mainloop()