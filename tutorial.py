from customtkinter import *
from PIL import Image

root = CTk()
root.title("Higher or Lower - Tutorial")
root.geometry("400x700")
img_w = 1200
img_h = 800
root.minsize(img_w, img_h); root.maxsize(img_w, img_h)
_arial = CTkFont(family="Arial", size=25, weight="bold")
pa=1 

def menu(select):
    root.destroy()
    os.system(f"python {select}.py")

def button(t, bt):
    if t: bt.configure(fg_color="#404040")
    else: bt.configure(fg_color="#242424")

def switch_page(dir):
    global pa
    if dir:
        if pa < 5:
            pa += 1
            _img.configure(dark_image=Image.open(f"images/tutorial/{pa}.png"))
            tutorial_lbl.configure(image=_img)
    else:
        if pa > 1:
            pa -= 1
            _img.configure(dark_image=Image.open(f"images/tutorial/{pa}.png"))
            tutorial_lbl.configure(image=_img)

_img = CTkImage(dark_image=Image.open(f"images/tutorial/1.png"), size=(img_w , img_h))
tutorial_lbl = CTkLabel(root, image=_img, text=" ")
tutorial_lbl.place(anchor="center", relx=0.5, rely=0.5)

next_bt = CTkLabel(root, fg_color="#242424", font=_arial, width=(img_w/5)*2, height=50, text=">>>")
next_bt.place(anchor="se", relx=1, rely=1)

previous_bt = CTkLabel(root, corner_radius=0, fg_color="#242424", font=_arial, width=(img_w/5)*2, height=50, text="<<<")
previous_bt.place(anchor="sw", relx=0, rely=1)

back_bt = CTkLabel(root, corner_radius=0, fg_color="#242424", font=_arial, width=img_w/5, height=50, text="Back")
back_bt.place(anchor="s", relx=0.5, rely=1)

next_bt.bind("<Button-1>", lambda event: switch_page(True))
next_bt.bind("<Enter>", lambda event, bt=next_bt: button(True, bt))
next_bt.bind("<Leave>", lambda event, bt=next_bt: button(False, bt))

previous_bt.bind("<Button-1>", lambda event: switch_page(False))
previous_bt.bind("<Enter>", lambda event, bt=previous_bt: button(True, bt))
previous_bt.bind("<Leave>", lambda event, bt=previous_bt: button(False, bt))

back_bt.bind("<Button-1>", lambda event: menu("main"))
back_bt.bind("<Enter>", lambda event, bt=back_bt: button(True, bt))
back_bt.bind("<Leave>", lambda event, bt=back_bt: button(False, bt))

root.mainloop()