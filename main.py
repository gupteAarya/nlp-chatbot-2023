import tkinter
from tkinter import messagebox

from PIL import Image
from textblob import TextBlob
import random
import json
import customtkinter
from customtkinter import *
from difflib import get_close_matches

keys = []

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("theme.json")
def load_training_data(file_path : str) -> dict:
    with open(file_path,'r') as file:
        data: dict = json.load(file)
    return data

def save_training_data(file_path : str, data: dict):
    with open(file_path,'w') as file:
        json.dump(data, file,indent=2)

def find_accurate(user_question : str, questions : list[str]) -> str|None:
    matches: list = get_close_matches(user_question,questions,n=1,cutoff=0.6)
    return matches[0] if matches else None

def get_answer(request: str, training:dict) -> str|None:
    for q in training["requests"]:
        if q["request"] == request:
            return q["reply"]


root = tkinter.Tk()
root.title("Gizmo Geeks Help Bot")
root.geometry("455x771")
root.resizable(False, False)
root.configure(background="white")

send = Image.open("assets/send.png")
botIcon = Image.open("./assets/robot.png")
userIcon = Image.open("./assets/user.png")

framePrompt = customtkinter.CTkFrame(root)
framePrompt.pack(side=BOTTOM)
frameTitle = customtkinter.CTkFrame(root, width=345, height=50)
frameTitle.pack(side=TOP, pady=10)
frameChat = customtkinter.CTkScrollableFrame(root, width=430, height=650, scrollbar_fg_color="white",
                                             scrollbar_button_hover_color="white", scrollbar_button_color="white")
frameChat.pack()

prompt_input = customtkinter.CTkEntry(
    framePrompt,
    height=55,
    width=375,
    border_width=0,
    placeholder_text="Type your prompt here",
    placeholder_text_color="#2c2c2c",
    fg_color="#d2ecfa",
    text_color="#2c2c2c",
    font=("Poppins", 18),
)
prompt_input.grid(column=0, row=0, padx=6, pady=8)
prompt_input.focus()
class FadeInLabel(customtkinter.CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields = ('text_color', 'fg_color')
        self.colors = {key: self.cget(key) for key in self.fields}
        self.colors['base'] = self.master.cget('fg_color')
        self.configure(**{key: self.colors['base'] for key in self.fields})

        for key, color in self.colors.items():
            if isinstance(color, str):
                rgb_color = self.winfo_rgb(color)
                self.colors[key] = (rgb_color, rgb_color)
            else:
                self.colors[key] = self.winfo_rgb(color[0]), self.winfo_rgb(color[1])

        self.transition = 0
        root.after(1, self.change_color())

    def get_curr(self, start, end):
        rgb_to_hex = lambda rgb: '#{:02x}{:02x}{:02x}'.format(*[int(val * 255 / 65535) for val in rgb])
        return rgb_to_hex([start[i] + (end[i] - start[i]) * self.transition for i in range(3)])

    def change_color(self):
        self.configure(
            **{key: (self.get_curr(self.colors['base'][0], self.colors[key][0]),
                     self.get_curr(self.colors['base'][1], self.colors[key][1])) for key in self.fields}
        )
        self.transition += 0.05
        if self.transition < 1:
            self.after(10, self.change_color)
def clear():
    for widgets in frameChat.winfo_children():
        widgets.destroy()
def _update_UI_(usrPrompt, respo):
    if prompt_input == "b./c":
        clear()
        prompt_input.delete(0, END)
    else:
        btnProfile = customtkinter.CTkButton(frameChat,text="You",image=CTkImage(light_image=userIcon,dark_image=userIcon),fg_color="white",hover_color="white",compound="right",width=30,font=("Quicksand", 18, "bold"))
        btnProfile.pack(anchor="e", padx=10)
        label = customtkinter.CTkLabel(
            frameChat,
            text=usrPrompt,
            font=("Poppins", 20, "bold"),
            anchor="w",
            width=20,
            fg_color="#2c2c2c",
            height=35,
            wraplength=200,
            justify="left",
            padx=20,
            pady=20,
            text_color="white",
            corner_radius=20
        )
        frameChat.configure(width=430, height=700)
        label.pack(anchor="e", padx=10)
        customtkinter.CTkFrame(frameChat, fg_color=("white"), width=410, height=10).pack()
        btnAI = customtkinter.CTkButton(frameChat, image=CTkImage(light_image=botIcon, dark_image=botIcon),
                                        compound="left",
                                        text="AI ChatBot", height=30, width=30, font=("Quicksand", 18, "bold"),
                                        fg_color=("white", "#2C2C2C"), hover_color=("white", "#2C2C2C"))
        btnAI.pack(anchor="w", padx=10)
        prompt_input.delete(0, END)
        promptReply = FadeInLabel(frameChat,
                                  text=respo,
                                  fg_color=("#3b96d2", "#FFFFFF"), text_color=("#FFFFFF", "#2c2c2c"), padx=20, pady=20,
                                  wraplength=350,
                                  justify="left",
                                  anchor="w",
                                  width=20,
                                  height=35,
                                  font=("Quicksand", 18,"bold"),
                                  corner_radius=10, )

        promptReply.pack(anchor="w", padx=10)

        root.after(50, frameChat._parent_canvas.yview_moveto, 1)

        customtkinter.CTkFrame(frameChat, fg_color=("white"), width=410, height=15).pack()


def chatBot():
    training: dict = load_training_data("train.json")
    user_input: str = prompt_input.get().lower()
    if user_input == "b./c":
        clear()
        prompt_input.delete(0, END)
    else:
        best_match: str | None = find_accurate(user_input, [q["request"] for q in training["requests"]])
        if best_match:
            reply: str = get_answer(best_match, training)
            _update_UI_(usrPrompt=user_input, respo=reply)
        else:
            if prompt_input.get() == "" or prompt_input.get() == " ":
                messagebox.askokcancel("askokcancel", "Please Enter Your Request Before Sending It")
            else:
                req = str(TextBlob(prompt_input.get().lower()).correct())
                best_match: str | None = find_accurate(req, [q["request"] for q in training["requests"]])
                if best_match:
                    reply: str = get_answer(best_match, training)
                    _update_UI_(usrPrompt=user_input, respo=reply)
                else:
                    lst_err_res = ["Sorry, but I couldn't understand that statement",
                                   "Could you please rephrase your sentence?"]
                    i = (random.randint(0, 1))
                    _update_UI_(usrPrompt=user_input, respo=lst_err_res[i])

btnSend = customtkinter.CTkButton(
    framePrompt,
    text="",
    image=CTkImage(light_image=send,dark_image=send),
    width=55,
    height=55,
    corner_radius=10,
    command=chatBot,
    fg_color="#78c5ef",
    hover_color="#69beed"
)
btnSend.grid(column=1,row=0)
txt1 = customtkinter.CTkLabel(frameTitle,text="Gizmo",font=("Quicksand",45,"bold"),text_color="#65dcb8").pack(side=LEFT)
txt2 = customtkinter.CTkLabel(frameTitle,text="Bot",font=("Poppins",45,"bold"),text_color="#3b96d2").pack(side=LEFT)

prompt_input.bind("<Return>",lambda event : chatBot())

root.mainloop()
