from customtkinter import *
import data as D

def update_data():
    with open("data.py", "w", encoding="utf-8") as file:
        file.write("database = [\n")
        for item in D.database:
            file.write(f"   {item},\n")
        file.write("]\n")
        
        file.write("settings = [")
        for stt in D.settings:
            file.write(f"{stt}, ")
        file.write("]\n")
        
        file.write("leaderboard = [")
        for sc in D.leaderboard:
            file.write(f"{sc}, ")
        file.write("]\n")

root = CTk()
root.title("Higher or Lower - Settings")
root.geometry("400x700")
root.minsize(600, 400); root.maxsize(600, 400)

_arial = CTkFont(family="Arial", size=20, weight="bold")

def menu(select):
    new_sett = []
    theme_id = D.database[0].index(theme_box.get())
    bar_id = D.database[1].index(bar_box.get())
    a_c = auto_card.get()
    a_m = music.get()
    
    new_sett.append(theme_id)
    new_sett.append(bar_id)
    new_sett.append(a_c)
    new_sett.append(a_m)
    
    for i, new in enumerate(new_sett):
        D.settings[i] = new
    update_data()
    
    root.destroy()
    os.system(f"python {select}.py")

def button(t, bt):
    if t: bt.configure(fg_color="#404040")
    else: bt.configure(fg_color="#242424")

theme_box = CTkComboBox(root, values=[D.database[0][0], D.database[0][1], D.database[0][2]])
theme_box.place(anchor="center", relx=0.35, rely=0.3)
theme_box.set(D.database[0][D.settings[0]])

bar_box = CTkComboBox(root, values=[D.database[1][0], D.database[1][1], D.database[1][2]])
bar_box.place(anchor="center", relx=0.65, rely=0.3)
bar_box.set(D.database[1][D.settings[1]])

auto_card = CTkCheckBox(root, text="Auto Card", onvalue=True, offvalue=False)
auto_card.place(anchor="center", relx=0.35, rely=0.5)
if D.settings[2]: auto_card.select()

music = CTkCheckBox(root, text="Auto Music", onvalue=True, offvalue=False)
music.place(anchor="center", relx=0.65, rely=0.5)
if D.settings[3]: music.select()

start_bt = CTkLabel(root, fg_color="#242424", text="Save & Exit", font=_arial)
start_bt.place(anchor="n", relx=0.5, rely=0.6, relwidth=0.3, relheight=0.1)

start_bt.bind("<Button-1>", lambda event: menu("main"))
start_bt.bind("<Enter>", lambda event, bt=start_bt: button(True, bt))
start_bt.bind("<Leave>", lambda event, bt=start_bt: button(False, bt))

root.mainloop()