from random import *
from tkinter import *
import tkinter as tk
import tkinter.font
from re import *
import os
import json
import nltk
from nltk.corpus import words
import random
from time import sleep

pt = 1
theme = "white"
window = tk.Tk()
window.title("Hangman")
window.geometry("350x350")
window.resizable(False, False)

def night_mode():
    global theme
    theme = "black"
    window.config(bg="Black")
    label_correct_word.config(bg="Black", fg="White")
    label_word.config(bg="Black", fg="White")
    label_chances.config(bg="Black", fg="White")
    label_result.config(bg="Black", fg="White")
    label_turn.config(bg="Black", fg="White")
    label_name.config(bg="Black", fg="White")
    label_score.config(bg="Black", fg="White")
    game_menu.config(bg= "Black", fg="White")
    option_menu.config(bg= "Black", fg="White")
    option_menu.delete("Night Mode")
    option_menu.add_command(label="Light Mode", command= light_mode)

def light_mode():
    global theme
    theme = "white"
    window.config(bg="White")
    label_correct_word.config(bg="White", fg="Black")
    label_word.config(bg="White", fg="Black")
    label_chances.config(bg="White", fg="Black")
    label_result.config(bg="White", fg="Black")
    label_turn.config(bg="White", fg="Black")
    label_name.config(bg="White", fg="Black")
    label_score.config(bg="White", fg="Black")
    game_menu.config(bg="White", fg="Black")
    option_menu.config(bg="White", fg="Black")
    option_menu.delete("Light Mode")
    option_menu.add_command(label="Night Mode", command= night_mode)

def level_screen():
    global window
    level = Toplevel(window)
    level.title("Levels")
    level.geometry("240x150")
    level.resizable(False, False)
    level.focus()
    string_level = StringVar()
    string_level.set("Easy")
    label_level = Label(level, text="Easy or Hard?", font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
    oe = Radiobutton(level, text="Easy", variable=string_level, value="Easy", font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
    oh = Radiobutton(level, text="Hard", variable=string_level, value="Hard", font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
    button_level = Button(level, text="Submit", command=lambda: [level_set(string_level.get()), level.destroy()], font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()

    level.wait_window(level)

def level_set(level):
    global words, blank, chances, w, lw, lblank
    if level == "Easy":
        with open("E:/Yasan/Hangman/words.txt") as file:
            words = file.read().split()
        rc = random.randint(0, 3)
    elif level == "Hard":
        nltk.download("words")
        a = words.words()
        random.shuffle(a)
        t = 10
        words = a[:t]
        rc = random.randint(0, 5)

    n = randint(0, len(words)-1)
    w = words[n].upper()
    lw = list(w)
    blank = len(w) * "_ "
    lblank = blank.split()
    print(w)
    chances = len(w) + rc

def delete_screen():
    global delete
    delete = Toplevel(window)
    delete.title("Delete")
    delete.geometry("300x150")
    delete.resizable(False, False)
    if theme == "white":
        label_delete = Label(delete, text="Enter the name of your save:", font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
        delete_name = StringVar()
        entry_delete = Entry(delete, textvariable=delete_name).pack()
        button_delete = Button(delete, text="Confirm", command= lambda: delete_confirm(f"{delete_name.get()}.txt"), font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
    elif theme == "black":
        delete.config(bg= "Black")
        label_delete = Label(delete, text="Enter the name of your save:", bg="Black", fg="White", font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
        delete_name = StringVar()
        entry_delete = Entry(delete, textvariable=delete_name, bg="Black", fg="White").pack()
        button_delete = Button(delete, text="Confirm", bg="Black", fg="White", command= lambda: delete_confirm(f"{delete_name.get()}.txt"), font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()

def delete_confirm(name):
    global text
    if os.path.exists(f"E:/Yasan/Hangman/saves/{name}"):
        game_menu.delete(os.path.splitext(name)[0])
        os.remove(f"E:/Yasan/Hangman/saves/{name}")
        if f'{text["fname"]}.txt' == name:
            with os.scandir("E:/Yasan/Hangman/saves") as saves:
                for s in saves:
                    last_game = s.name

            with open(f"E:/Yasan/Hangman/saves/{s.name}") as file:
                text = json.load(file)

            text["status"] = "active"
            label_name.config(text=text["fname"])

            if text["nplayers"] == 1:
                p1s = text["player1"]
                label_score.config(text=f"Player 1: {p1s}")
                file_text = f'{{"fname": "{text["fname"]}",\n"status": "active",\n"nplayers": 1,\n"player1": {text["player1"]}}}'
            else:
                p1s = text["player1"]
                p2s = text["player2"]
                label_score.config(text=f"Player 1: {p1s}\nPlayer 2: {p2s}")
                file_text = f'{{"fname": "{text["fname"]}",\n"status": "active",\n"nplayers": 2,\n"player1": {text["player1"]},\n"player2": {text["player2"]}}}'

            with open(f"E:/Yasan/Hangman/saves/{s.name}", "w") as file:
                file.write(file_text)

        delete.destroy()
    else:
        print(theme)
        if theme == "white":
            label_error = Label(delete, text="This save does not exist!", font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
        elif theme == "black":
            label_error = Label(delete, text="This save does not exist!", bg="Black", fg="White", font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()

def check(gl, gb):
    global chances, pt, p1s, p2s
    if text["nplayers"] == 2:
        if pt % 2 == 0:
            label_turn.config(text="It's Player 1's Turn.")
            if gl in w:
                p2s += 1
                text["player2"] = p2s
        else:
            label_turn.config(text="It's Player 2's Turn.")
            if gl in w:
                p1s += 1
                text["player1"] = p1s
        pt += 1
        new_text = f'{{"fname": "{text["fname"]}",\n"status": "active",\n"nplayers": 2,\n"player1": {p1s},\n"player2": {p2s}}}'
        label_score.config(text=f"Player 1: {p1s}\nPlayer 2: {p2s}")

    else:
        if gl in w:
            p1s += 1
            text["player1"] = p1s

        new_text = f'{{"fname": "{text["fname"]}",\n"status": "active",\n"nplayers": 1,\n"player1": {p1s}}}'
        label_score.config(text=f"Player 1: {p1s}")

    with open(f"E:/Yasan/Hangman/saves/{text['fname']}.txt", "w") as file:
        file.write(new_text)

    guess = False
    for i in range(len(lw)):
        if gl == lw[i-1]:
            lblank[i-1] = gl
            guess = True
            gb.config(bg="Green", relief="sunken", state= DISABLED)

    blank = ""
    for i in lblank:
        blank += i + " "
    
    label_word.config(text=blank)

    if lblank  == lw:
        label_result.config(text="You won!", fg="Green")
    elif guess == False:
        chances -= 1
        gb.config(bg="Red", relief="sunken", state= DISABLED)
        label_chances.config(text=f"You have {chances} chances.")
        if chances == 0:
            label_result.config(text="You lose!", fg="Red")
            label_correct_word.config(text=f"The word was {w}!", fg="Red")

def new_game():
    global cgame
    cgame = Toplevel(window)
    cgame.title("New Game")
    cgame.geometry("260x170")
    cgame.resizable(False, False)
    cgame.focus()
    players = IntVar()
    players.set(1)
    file_name = StringVar()
    file_name.set("New Game")
    if theme == "white":
        label_players = Label(cgame, text="How Many Players Does Your Game Have?", font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
        o1 = Radiobutton(cgame, text="1 Player", variable=players, value=1, font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
        o2 = Radiobutton(cgame, text="2 Players", variable=players, value=2, font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
        label_name = Label(cgame, text="Enter The Name Of Your Game:", font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
        entry_name = Entry(cgame, textvariable=file_name).pack()
        button_confirm = Button(cgame, text="Confirm", command= lambda: create_file(players.get(), file_name.get()), font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
    elif theme == "black":
        cgame.config(bg= "Black")
        label_players = Label(cgame, text="How Many Players Does Your Game Have?", bg="Black", fg="White", font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
        o1 = Radiobutton(cgame, text="1 Player", variable=players, value=1, bg="Black", fg="White", font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
        o2 = Radiobutton(cgame, text="2 Players", variable=players, value=2, bg="Black", fg="White", font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
        label_name = Label(cgame, text="Enter The Name Of Your Game:", bg="Black", fg="White", font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()
        entry_name = Entry(cgame, textvariable=file_name, bg="Black", fg="White").pack()
        button_confirm = Button(cgame, text="Confirm", bg="Black", fg="White", command= lambda: create_file(players.get(), file_name.get()), font=tkinter.font.Font(family="Comic Sans MS", size=10)).pack()

def create_file(players, file_name):
    global text
    if players == 1:
        file_text = f'{{"fname": "{file_name}",\n"status": "active",\n"nplayers": 1,\n"player1": 0}}'
        p1s = 0
        label_score.config(text=f"Player 1: 0")
    elif players == 2:
        file_text = f'{{"fname": "{file_name}",\n"status": "active",\n"nplayers": 2,\n"player1": 0,\n"player2": 0}}'
        p1s = 0
        p2s = 0
        label_score.config(text=f"Player 1: 0\nPlayer 2: 0")

    if text["nplayers"] == 1:
        alter_text = f'{{"fname": "{text["fname"]}",\n"status": "inactive",\n"nplayers": 1,\n"player1": {text["player1"]}}}'
    if text["nplayers"] == 2:
        alter_text = f'{{"fname": "{text["fname"]}",\n"status": "inactive",\n"nplayers": 2,\n"player1": {text["player1"]},\n"player2": {text["player2"]}}}'

    with open(f"E:/Yasan/Hangman/saves/{text['fname']}.txt", "w") as file:
        file.write(alter_text)

    with open(f"E:/Yasan/Hangman/saves/{file_name}.txt", "w") as file:
        file.write(file_text)
    
    with open(f"E:/Yasan/Hangman/saves/{file_name}.txt") as file:
        text = json.load(file)

    game_menu.add_command(label=file_name, command= lambda: set_game(file_name))
    label_name.config(text=text["fname"])
    cgame.destroy()

def set_game(file_name):
    global text
    print(file_name)
    with open(f"E:/Yasan/Hangman/saves/{file_name}.txt") as file:
        text2 = json.load(file)

    print(f"text 2= {text2}")

    if text["nplayers"] == 1:
        alter_text = f'{{"fname": "{text["fname"]}",\n"status": "inactive",\n"nplayers": 1,\n"player1": {text["player1"]}}}'
        file_text = f'{{"fname": "{file_name}",\n"status": "active",\n"nplayers": 1,\n"player1": {text2["player1"]}}}'
        p1s = text2["player1"]
        label_score.config(text=f"Player 1: {p1s}")
    elif text["nplayers"]:
        alter_text = f'{{"fname": "{text["fname"]}",\n"status": "inactive",\n"nplayers": 2,\n"player1": {text["player1"]},\n"player2": {text["player2"]}}}'
        file_text = f'{{"fname": "{file_name}",\n"status": "active",\n"nplayers": 2,\n"player1": {text2["player1"]},\n"player2": {text2["player2"]}}}'
        p1s = text2["player1"]
        p2s = text2["player2"]
        label_score.config(text=f"Player 1: {p1s}\nPlayer 2: {p2s}")

    with open(f"E:/Yasan/Hangman/saves/{text['fname']}.txt", "w") as file:
        file.write(alter_text)

    text = text2
    label_name.config(text=text["fname"])

    with open(f"E:/Yasan/Hangman/saves/{text['fname']}.txt", "w") as file:
        file.write(file_text)

level_screen()
label_correct_word = Label(window, text="", font=tkinter.font.Font(family="Comic Sans MS", size=15))
label_word = Label(window, text=blank, font=tkinter.font.Font(family="Comic Sans MS", size=20))
label_chances = Label(window, text=f"You have {chances} chances.", font=tkinter.font.Font(family="Comic Sans MS", size=10))
label_result = Label(window, text="", font=tkinter.font.Font(family="Comic Sans MS", size=20))
ba = Button(window, text="A", height=1, width=2, command= lambda: check("A", ba), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bb = Button(window, text="B", height=1, width=2, command= lambda: check("B", bb), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bc = Button(window, text="C", height=1, width=2, command= lambda: check("C", bc), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bd = Button(window, text="D", height=1, width=2, command= lambda: check("D", bd), font=tkinter.font.Font(family="Comic Sans MS", size=8))
be = Button(window, text="E", height=1, width=2, command= lambda: check("E", be), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bf = Button(window, text="F", height=1, width=2, command= lambda: check("F", bf), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bg = Button(window, text="G", height=1, width=2, command= lambda: check("G", bg), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bh = Button(window, text="H", height=1, width=2, command= lambda: check("H", bh), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bi = Button(window, text="I", height=1, width=2, command= lambda: check("I", bi), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bj = Button(window, text="J", height=1, width=2, command= lambda: check("J", bj), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bk = Button(window, text="K", height=1, width=2, command= lambda: check("K", bk), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bl = Button(window, text="L", height=1, width=2, command= lambda: check("L", bl), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bm = Button(window, text="M", height=1, width=2, command= lambda: check("M", bm), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bn = Button(window, text="N", height=1, width=2, command= lambda: check("N", bn), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bo = Button(window, text="O", height=1, width=2, command= lambda: check("O", bo), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bp = Button(window, text="P", height=1, width=2, command= lambda: check("P", bp), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bq = Button(window, text="Q", height=1, width=2, command= lambda: check("Q", bq), font=tkinter.font.Font(family="Comic Sans MS", size=8))
br = Button(window, text="R", height=1, width=2, command= lambda: check("R", br), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bs = Button(window, text="S", height=1, width=2, command= lambda: check("S", bs), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bt = Button(window, text="T", height=1, width=2, command= lambda: check("T", bt), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bu = Button(window, text="U", height=1, width=2, command= lambda: check("U", bu), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bv = Button(window, text="V", height=1, width=2, command= lambda: check("V", bv), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bw = Button(window, text="W", height=1, width=2, command= lambda: check("W", bw), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bx = Button(window, text="X", height=1, width=2, command= lambda: check("X", bx), font=tkinter.font.Font(family="Comic Sans MS", size=8))
by = Button(window, text="Y", height=1, width=2, command= lambda: check("Y", by), font=tkinter.font.Font(family="Comic Sans MS", size=8))
bz = Button(window, text="Z", height=1, width=2, command= lambda: check("Z", bz), font=tkinter.font.Font(family="Comic Sans MS", size=8))
label_turn = Label(window, text="It's Player 1's Turn.", font=tkinter.font.Font(family="Comic Sans MS", size=10))
menubar = Menu(window)
window.config(menu=menubar)
option_menu = Menu(menubar, tearoff=False, font=tkinter.font.Font(family="Comic Sans MS", size=9))
game_menu = Menu(menubar, tearoff=False, font=tkinter.font.Font(family="Comic Sans MS", size=9))
game_menu.add_command(label="New Game...", command=new_game)
option_menu.add_command(label="Delete", command= delete_screen)
option_menu.add_command(label="Exit", command= lambda: window.destroy())
option_menu.add_command(label="Night Mode", command= night_mode)

with os.scandir("E:/Yasan/Hangman/saves") as saves:
    for s in saves:
        with open(f"E:/Yasan/Hangman/saves/{s.name}") as file:
            file_content = json.load(file)
            if file_content["status"] == "active":
                text = file_content
                if text["nplayers"] == 1:
                    p1s = text["player1"]
                    label_score = Label(window, text=f"Player 1: {str(p1s)}", justify="left", font=tkinter.font.Font(family="Comic Sans MS", size=10))
                else:
                    p1s = text["player1"]
                    p2s = text["player2"]
                    label_score = Label(window, text=f"Player 1: {str(p1s)}\nPlayer 2: {str(p2s)}", justify="left", font=tkinter.font.Font(family="Comic Sans MS", size=10))

        gn = os.path.splitext(s.name)
        game_menu.add_command(label=gn[0], command= lambda: set_game(gn[0]))

menubar.add_cascade(label="Options", menu=option_menu)
menubar.add_cascade(label="Game", menu=game_menu)
label_name = Label(window, text=text["fname"], font=tkinter.font.Font(family="Comic Sans MS", size=11))

label_name.pack()
label_score.pack()
label_word.pack()
label_chances.pack()
bq.place(x=45, y=120)
bw.place(x=70, y=120)
be.place(x=95, y=120)
br.place(x=120, y=120)
bt.place(x=145, y=120)
by.place(x=170, y=120)
bu.place(x=195, y=120)
bi.place(x=220, y=120)
bo.place(x=245, y=120)
bp.place(x=270, y=120)
ba.place(x=55, y=147)
bs.place(x=80, y=147)
bd.place(x=105, y=147)
bf.place(x=130, y=147)
bg.place(x=155, y=147)
bh.place(x=180, y=147)
bj.place(x=205, y=147)
bk.place(x=230, y=147)
bl.place(x=255, y=147)
bz.place(x=65, y=174)
bx.place(x=90, y=174)
bc.place(x=115, y=174)
bv.place(x=140, y=174)
bb.place(x=165, y=174)
bn.place(x=190, y=174)
bm.place(x=215, y=174)
label_turn.place(x=115, y=210)
label_result.place(x=110, y=230)
label_correct_word.place(x=80, y=270)

window.mainloop()