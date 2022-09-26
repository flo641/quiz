from tkinter import *
from tkinter import messagebox
import json

# Defnition aller Komponenten 
class Quiz:
    def __init__(self):

        self.question_num = 0

        self.show_title()
        self.show_question()

        self.opt_selected = IntVar()

        self.opts = self.radio_buttons()

        self.show_options()

        self.buttons()

        self.data_size = len(question)

        self.correct = 0

    # Zeigt das Ergebnis am ende des Quiz an
    def show_result(self):

        wrong_count = self.data_size - self.correct
        correct = f"Correct answers: {self.correct}"
        wrong = f"Wrong answers: {wrong_count}"

        score = int(self.correct / self.data_size * 100)
        result = f"Total score in percentage: {score}%"

        messagebox.showinfo("Result", f"{result}\n{correct}\n{wrong}")

    # Kontrolliert ob die Antwort richtig ist, wenn man auf nächste Frage klickt
    def check_answers(self, question_num):

        if self.opt_selected.get() == answer[question_num]:
            return True
    # Definition vom next button 
    def next_button(self):

        if self.check_answers(self.question_num):
            self.correct += 1

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

        next_button.place(x = 500, y = 500)

        quit_button = Button(gui, text = "Quit", command = gui.destroy,
                             width = 5, bg = "pink", fg = "black", font = ("ariel", 16, " bold"))

        quit_button.place(x = 1000, y = 100)

    # Die aktuelle Frage soll angezeigt werden
    def show_question(self):

        question_num = Label(gui, text = question[self.question_num], width = 60,
                     font = ('ariel', 16, 'bold'), anchor = 'w')

        question_num.place(x = 70, y = 100)

    # Dise Methode ist für die Eingabe zuständig
    def show_options(self):
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


gui = Tk()

gui.geometry("1200x600")

gui.title("Quiz game von Florian")

with open('questions_answers.json') as f:
    data = json.load(f)

question = (data['question'])
options = (data['options'])
answer = (data['answer'])

quiz = Quiz()

gui.mainloop()