import random
import tkinter
from tkinter import *
        

class CardDeck:

    def __init__(self,sideLen):
        self.sideLen = sideLen

    def read(self):

        file = open("/home/pi/Desktop/python-memory-game/memory.txt","r")
        line = file.readline()
        self.allWords = []
        while line !="":
            part = line.split("\n")
            self.allWords.append(part[0])
            line = file.readline()
        file.close()

    def random(self):
        random.shuffle(self.allWords)
        self.words = self.allWords[:int(pow(self.sideLen,2)/2)]

    def dubble(self):
        self.words = self.words*2
        random.shuffle(self.words)

    
    def createCards(self):
        self.cards = []
        for i in self.words:
            self.cards.append(Card(i,False))
        
class Card:

    def __init__(self,word,up):
        self.word = word
        self.up = up
    def __str__(self):
        if self.up == True:
            return self.word
        else:
            return ""
   

class Application:

    
    def __init__(self, root):
        self.root = root
        self.countClicks = 0
        self.indexToCompare = []
        self.trials = 0
        self.pairs = 0
        self.text = False

        self.root.title("EPRP Python Memory Game")
        tkinter.Frame(self.root, width=300, height=250).pack()

        self.setLevel()

    
    def setLevel(self):

        self.var = StringVar()
        self.txt = tkinter.Label(self.root, textvariable=self.var).place(x=0, y=0)
        self.var.set("Choose Level")
                                      
        self.varRadio = IntVar()
        self.radiobuttons = []
        for i in range(3):
            self.radiobuttons.append(Radiobutton (self.root, text="Level "+str(i+1), variable=self.varRadio, value=(i+1)*2, command=self.start))
            self.radiobuttons[i].pack(anchor = W)

    def start(self):
        self.sideLen = self.varRadio.get()

        self.c = CardDeck(self.sideLen)
        OK1 = True
        try:
            self.c.read()
        except IOError:
            text = self.var.get()
            self.var.set("File not found")
            OK1 = False

        if OK1 == True:
            if len(self.c.allWords) < pow(self.sideLen,2)/2:
                text = self.var.get()
                self.var.set("...")
            else:
                self.c.random()
                self.c.dubble()
                self.c.createCards()
                self.printBoard()

    
    def printBoard(self):
        xvar=10
        yvar=70
        self.buttons = []
        cardCount = 0
        for i in range(self.sideLen):
            for j in range(self.sideLen):

                cmd = lambda index=cardCount: self.click(index)               
                self.buttons.append(tkinter.Button(self.root, command=cmd, text=self.c.cards[cardCount], width="6"))
                self.buttons[cardCount].place(x=xvar, y=yvar)
                
                xvar=xvar+80
                cardCount += 1
            xvar=10
            yvar=yvar+60

        text = self.var.get()
        self.var.set("")
        
        for i in range(len(self.radiobuttons)):
            self.radiobuttons[i].pack_forget()

    def click(self,index):
        
        if self.c.cards[index].up == False:

            
            self.c.cards[index].up = True
            self.buttons[index].config(text=self.c.cards[index])
            self.countClicks += 1

            if self.text == True:
                text = self.var.get()
                self.var.set("")
                self.text = False

            if len(self.indexToCompare) == 2:
                self.buttons[self.indexToCompare[0]].config(text=self.c.cards[self.indexToCompare[0]])
                self.buttons[self.indexToCompare[1]].config(text=self.c.cards[self.indexToCompare[1]])
                self.indexToCompare = [] 

            if self.countClicks == 2:
                self.countClicks = 0
                self.indexToCompare.append(index)
                self.compare()
            else:
                self.indexToCompare.append(index)
                self.text = True
                
        else:
            text = self.var.get()
            self.var.set("You clicked on the same button")

    
    def compare(self):
        self.trials += 1
        if self.c.cards[self.indexToCompare[0]].word == self.c.cards[self.indexToCompare[1]].word:
            text = self.var.get()
            self.var.set("Congrats you got a match!")
            self.text = True
            
            self.indexToCompare = []
            self.countPairs()
        else:
            self.c.cards[self.indexToCompare[0]].up = False
            self.c.cards[self.indexToCompare[1]].up = False

    
    def countPairs(self):
        self.pairs += 1
        if self.pairs == pow(self.sideLen,2)/2:
            text = self.var.get()
            self.var.set("YOU WON!\nYou finished this game after "+str(self.trials)+" tries")
            self.newGameButton = tkinter.Button(self.root, command=self.newGame, text="Try again?", width="12")
            self.newGameButton.pack()

    
    def newGame(self):
        text = self.var.get()
        self.var.set("")
        self.text = False
        self.newGameButton.destroy()
        for i in range(len(self.buttons)):
            self.buttons[i].destroy()
        self.trials = 0
        self.pairs = 0
        self.text = False
        self.setLevel()


root = tkinter.Tk()
Application(root)
root.mainloop()
