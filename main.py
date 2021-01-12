BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas
import random

from tkinter import messagebox
import random
import json
timer = None
# passing current_card between funcions
current_card = {}
to_learn={}


#functions
def flip_card():
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_image, image=card_back_img)
    canvas.itemconfig(card_title, fill="white")
    canvas.itemconfig(card_word, fill="white")
    canvas.itemconfig(card_word, text=current_card.get("English"))


def next_card():
    global current_card, timer
    window.after_cancel(timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_word, text=current_card.get("Italian"), fill="black")
    canvas.itemconfig(card_title, text="Italian", fill="black")
    canvas.itemconfig(card_image, image=card_front_img)
    timer = window.after(3000, flip_card)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


#get data
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/italian_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

print(to_learn)



# user interface
window = Tk()
window.title("Italian - English Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526)
# Cannot create photoimage within a function
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
# The first arguments are the position THIS IS A POSITION
card_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", fill= "black", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

wrong_button_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_image, highlightthickness=0,command=next_card)
wrong_button.grid(row=2, column=0)

right_button_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_button_image, highlightthickness=0, command=is_known)
right_button.grid(row=2, column=1)

timer = window.after(3000, flip_card)
next_card()




window.mainloop()
