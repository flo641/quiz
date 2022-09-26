from time import time
from tkinter import *
from tkinter import messagebox
import json
from random import random
import threading
import time
from pprint import pprint

import requests

# Defnition aller Komponenten 
class Quiz:
    
    def __init__(self):

        self.overallTime = 0
        gui.configure(bg='white')
        self.question_num = 0

        self.show_title()
        self.show_question()

        self.opt_selected = IntVar()

        self.opts = self.radio_buttons()

        self.show_options()

        self.buttons()

        self.data_size = len(question)

        self.correct = 0
        
        self.answer_checked = False

    # Zeigt das Ergebnis am ende des Quiz an
    def show_result(self):

        wrong_count = self.data_size - self.correct
        correct = f"Correct answers: {self.correct}"
        wrong = f"Wrong answers: {wrong_count}"

        score = int(self.correct / self.data_size * 100)
        result = f"Total score in percentage: {score}%"
        
        time = f"Overall Time: {self.overallTime} seconds"

        messagebox.showinfo("Result", f"{result}\n{correct}\n{wrong}\n{time}")

    # Kontrolliert ob die Antwort richtig ist, wenn man auf nächste Frage klickt
    def check_answers(self, question_num):

        if self.opt_selected.get() == answer[question_num]:
            return True
        
    def check_button(self):

        if self.answer_checked: return
        
        
        if self.check_answers(self.question_num):
            self.correct += 1
            
            gui.configure(bg='green')
        else:
            gui.configure(bg='red')
            
        self.answer_checked = True
            
    
    def timer(self):
        
        start_time = time.time()
        time_left = IntVar()
        time_left.set(10)
        question_num = Label(gui, textvariable = time_left, width = 60,
                     font = ('ariel', 16, 'bold'), anchor = 'w')
        
        question_num.place(x = 1000, y = 70)
        
        
        while time_left.get()>0:
            time.sleep(0.05)
            if self.answer_checked: 
                self.overallTime = self.overallTime + 10 - time_left.get()
                return
            time_left.set(10-int(time.time()-start_time))
        
        
        self.overallTime = self.overallTime + 10
        self.check_button()
        
        
    
    # Definition vom next button 
    def next_button(self):
        
        if not self.answer_checked: return 
        
        self.answer_checked = False

        gui.configure(bg='white')
        
        self.question_num += 1
        
        if self.question_num == self.data_size:

            self.show_result()

            gui.destroy()
        else:
            self.show_question()
            self.show_options()

       
    # Aussehen und Position der Buttons 
    def buttons(self):

        next_button = Button(gui, text = "Next question", command = self.next_button,
                             width = 10, bg = "blue", fg = "black", font = ("ariel", 20, "bold"))
        
        check_button = Button(gui, text = "check question", command = self.check_button,
                             width = 12, bg = "blue", fg = "black", font = ("ariel", 20, "bold"))
        

        next_button.place(x = 700, y = 500)
        check_button.place(x = 300, y = 500)

        quit_button = Button(gui, text = "Quit", command = gui.destroy,
                             width = 5, bg = "pink", fg = "black", font = ("ariel", 16, " bold"))

        quit_button.place(x = 1000, y = 100)

    # Die aktuelle Frage soll angezeigt werden
    def show_question(self):
        
        questions = question[self.question_num]
        questions = questions[:70] + '\n' + questions[70:]
        
        question_num = Label(gui, text = questions, width = 60,
                     font = ('ariel', 16, 'bold'), anchor = 'w')

        question_num.place(x = 70, y = 100)

    # Dise Methode ist für die Eingabe zuständig
    def show_options(self):
        
        self.t1 = threading.Thread(target=self.timer)
        self.t1.start()

        value = 0

        self.opt_selected.set(0)

        for option in options[self.question_num]:
            self.opts[value]['text'] = option
            value += 1

    # TDiese Methode zeigt zeigt die überschrift
    def show_title(self):

        title = Label(gui, text = "Quiz Game",
                      width = 70, bg = "grey", fg = "white", font = ("ariel", 30, "bold"))

        title.place(x = 1, y = 2)

    # Die Methode ist für die Auswahl der Antworten zuständig
    def radio_buttons(self):

        question_list = []

        y_pos = 150

        while len(question_list) < 4:
            radio_btn = Radiobutton(gui, text =" ", variable = self.opt_selected,
                                    value = len(question_list) + 1, font = ("ariel", 20))

            question_list.append(radio_btn)

            radio_btn.place(x = 100, y = y_pos)

            y_pos += 60

        return question_list


answer = list([])

def getAnswers(e):
    answers = e['incorrectAnswers']
    
    correct_answer = int(random()*4)
    answer.append(correct_answer+1)
    
    answers.insert(correct_answer,e['correctAnswer'])
    
    return answers

data = requests.get(f"https://the-trivia-api.com/api/questions").json()


question = list(map(lambda x:x['question'],data))
options = list(map(getAnswers,data)) 


gui = Tk()
gui.geometry("1200x600")

gui.title("Quiz game von Florian")

quiz = Quiz()

gui.mainloop()
