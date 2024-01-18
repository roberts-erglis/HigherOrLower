import pygame
from customtkinter import *
from PIL import Image
from random import *
import numpy as np
import data as D

def play_background_music(file_path, loop=True):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1 if loop else 0)
play_background_music("sound/music.mp3", loop=True)
if not D.settings[3]: pygame.mixer.music.set_volume(0.0)

#Update data by overwritting
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
root.title("Higher or Lower - Card Game")
root.attributes("-fullscreen", True)

#Sizes
_card_w = 230
_card_h = 318
#Color [Hex]
_base = D.database[2][D.settings[0]]
_white = "white"
_t = "transparent"
#Font Family
_arial = CTkFont(family="Arial", size=25, weight="bold")
_arial_2 = CTkFont(family="Arial", size=35, weight="bold")
_striked_arial_2 = CTkFont(family="Arial", size=35, weight="bold")

#Settings
theme = D.database[0][D.settings[0]]
bar = D.database[1][D.settings[1]]
#Images
_bg_green = CTkImage(dark_image=Image.open(F"images/{theme}"), size=(root.winfo_screenwidth() , root.winfo_screenheight()))
_bar = CTkImage(dark_image=Image.open(F"images/{bar}"), size=(root.winfo_screenwidth() , root.winfo_screenheight()*0.2))
_logo = CTkImage(dark_image=Image.open("images/title.png"), size=(root.winfo_screenwidth()*0.6 , root.winfo_screenheight()*0.5))
mess_img = CTkImage(dark_image=Image.open(F"images/{bar}"), size=(root.winfo_screenwidth()*0.5 , root.winfo_screenheight()*0.2))
mute_img = CTkImage(dark_image=Image.open(F"images/{bar}"), size=(root.winfo_screenwidth()*0.04 , root.winfo_screenheight()*0.07))
score_lbl_png = CTkImage(dark_image=Image.open(F"images/{bar}"), size=(root.winfo_screenwidth()*0.13 , root.winfo_screenheight()*0.07))

#Global data
player_hand = []; selected_card = ["None"]; game_deck=[]; discarded=[]
namedCards = ["jack", "queen", "king", "ace"]
suits = ["diamonds", "clubs", "hearts", "spades"]
onScreen_cards = [
    [0, "None"],
    [0, "None"]
]
score = 0

    
#Funcions
def toggle_music():
    if D.settings[3]: 
        pygame.mixer.music.set_volume(0.0)
        music_bt.configure(text_color="red")
    else: 
        pygame.mixer.music.set_volume(0.5)
        music_bt.configure(text_color=_white)
    D.settings[3] = not D.settings[3]

#[Card Game - Set card deck]
def deck_setup():
    suits = ["diamonds", "clubs", "hearts", "spades"]
    values = range(2, 15)
    namedCard = ["jack", "queen", "king", "ace"]
    
    global deck; deck=[]
    for s in suits:
        for v in values:
            if v < 11:
                deck.append(f"{v}_of_{s}")
            else:
                rank = namedCard[v-11]
                deck.append(f"{rank}_of_{s}")
deck_setup()

#Create a deck that are suffled for game
def suffle_deck():
    shuffled_deck = deck.copy()
    shuffle(shuffled_deck)
    return shuffled_deck
game_deck = suffle_deck()

#[Place two cards at start]
def take_out_two(i):
    values = game_deck[0].split("_of_")
    img = CTkImage(dark_image=Image.open(f"cards/{game_deck[0]}.png"), size=(_card_w-10, _card_h-10))
    if i < 1: left_deck_img.configure(image=img)
    else: right_deck_img.configure(image=img)
    if values[0] in namedCards:
        if values[0] == "ace" and suits.index(values[1]) in [1, 3]: values[0] = 1
        else: values[0] = 11 + namedCards.index(values[0])
    values[0] = int(values[0])
    
    game_deck.pop(0)
    onScreen_cards[i][0] = values[0]
    onScreen_cards[i][1] = values[1]
    
    if i < 1: take_out_two(i+1)
    update_hand()

#[Add card in hand] 
def add_hand():
    if onScreen_cards[0][0] == 0:
        take_out_two(0)
        if D.settings[2]: add_hand()
        return
        
    if len(player_hand) < 3 and game_deck:
        next_card = game_deck[0]
        game_deck.pop(0)
        player_hand.append(next_card)
        if D.settings[2]: add_hand() #If auto card is true, add card to player hand faster
        update_hand()

#[Card hover animation]
def card_anim(card, dir, index):
    if dir:
        card.configure(fg_color="grey")
    else:
        card.configure(fg_color="black")

#[Confirm if allowed to place]
def isAllowed(dir):
    global score
    placing = selected_card[0]
    values = placing.split("_of_")
    global upDown, isRule
    
    if values[0] in namedCards:
        if values[0] == "ace" and suits.index(values[1]) in [1, 3]: values[0] = 1
        else: values[0] = 11 + namedCards.index(values[0])
    
    if suits.index(values[1]) in [0, 2]:
        upDown = True
    else:
        upDown = False
    values[0] = int(values[0])
    
    if dir:
        if values[0] == onScreen_cards[0][0]:
            isRule = True
        else:
            side = onScreen_cards[1][0]
            if upDown: 
                if side < values[0]: isRule = True
                else: isRule = False
            else:
                if side > values[0]: isRule = True
                else: isRule = False
        
        if isRule:
            score = score + (abs(values[0] - onScreen_cards[1][0]))*5
            print(f"{score}, {values[0]}")
            onScreen_cards[0][0] = values[0]
            onScreen_cards[0][1] = values[1]
            return True
        return False
    else:
        if values[0] == onScreen_cards[1][0]:
            isRule = True
        else:
            side = onScreen_cards[0][0]
            if upDown: 
                if side < values[0]: isRule = True
                else: isRule = False
            else:
                if side > values[0]: isRule = True
                else: isRule = False
        
        if isRule:
            score = score + (abs(values[0] - onScreen_cards[0][0]))*5
            print(f"{score}, {values[0]}")
            onScreen_cards[1][0] = values[0]
            onScreen_cards[1][1] = values[1]
            return True
        return False

#[Discards unnecesary cards by palyer's wish or impposible to continue]
def discrd_card():
    global score
    if selected_card[0] != "None":
        placing = selected_card[0]
        values = placing.split("_of_")
        if values[0] in namedCards:
            if values[0] == "ace" and suits.index(values[1]) in [1, 3]: values[0] = 1
            else: values[0] = 11 + namedCards.index(values[0])
        
        values[0] = int(values[0])
        score -= values[0]
        player_hand.remove(selected_card[0])
        discarded.append(selected_card[0])
        selected_card[0] = "None"
        if D.settings[2]: add_hand()
        update_hand()
    if len(discarded) > 0:
        img = CTkImage(dark_image=Image.open(f"cards/back_card.png"), size=(_card_w-10, _card_h-10))
        discard_img.configure(image=img, text=(f"DISCARDED:\n{len(discarded)}"))

def place_card(dir):
    if selected_card[0] != "None":
        img = CTkImage(dark_image=Image.open(f"cards/{selected_card[0]}.png"), size=(_card_w-10, _card_h-10))
        
        if dir:
            if isAllowed(dir):
                player_hand.remove(selected_card[0])
                left_deck_img.configure(image=img)
                selected_card[0] = "None"
        else:
            if isAllowed(dir):
                player_hand.remove(selected_card[0])
                right_deck_img.configure(image=img)
                selected_card[0] = "None"
        
        if D.settings[2]: add_hand()
        update_hand()

def selection(index):
    #print(player_hand[index])
    if selected_card[0] == player_hand[index]:
        selected_card[0] = "None"
    else:
        selected_card[0] = player_hand[index]
    update_hand()

card_labels = []
def update_hand():
    global card_labels
    l = len(player_hand)
    interval = ((l-1)*0.03)/2
    
    deck_img.configure(text=(f"CARD LEFT:\n{len(game_deck)}"))
    score_lbl.configure(text=(f"Score: {score}"))
    #if len(discarded): discard_img.configure(text=(f"CARD LEFT:\n{len(game_deck)}"))
    
    for label in card_labels:
        label.destroy()
    card_labels = []
    
    if interval > 0:
        spaces = np.linspace(0.5-interval, 0.5+interval, l)
        for i, posx in enumerate(spaces):
            posy=0.8
            if player_hand[i] == selected_card[0]: posy=0.75
            
            img = CTkImage(dark_image=Image.open(f"cards/{player_hand[i]}.png"), size=(_card_w-10, _card_h-10))
            label = CTkLabel(root, image=img, fg_color="black", text=" ", width=_card_w, height=_card_h)
            label.place(anchor="center", relx=posx, rely=posy)
            
            label.bind("<Button-1>", lambda event, index=i: selection(index))
            label.bind("<Enter>", lambda event, index=i, lbl=label: card_anim(lbl, True, index))
            label.bind("<Leave>", lambda event, index=i, lbl=label: card_anim(lbl, False, index))
            card_labels.append(label)
    else:
        if player_hand:
            posy=0.8
            if player_hand[0] == selected_card[0]: posy=0.75
            
            img = CTkImage(dark_image=Image.open(f"cards/{player_hand[0]}.png"), size=(_card_w-10, _card_h-10))
            label = CTkLabel(root, image=img, fg_color="black", text=" ", width=_card_w, height=_card_h)
            label.place(anchor="center", relx=0.5, rely=posy)
            
            label.bind("<Button-1>", lambda event, index=0: selection(index))
            label.bind("<Enter>", lambda event, lbl=label: card_anim(lbl, True, 0))
            label.bind("<Leave>", lambda event, lbl=label: card_anim(lbl, False, 0))
            card_labels.append(label)
    if not game_deck and not player_hand:
        message_lbl.configure(text=(f"Final score: {score}"))
        end_frame.place(relx=0)
        D.leaderboard.append(score)
        update_data()
        

def get_size(object, dir):
    object.update_idletasks()
    if dir == "w":
        print(object.winfo_reqwidth())
        return object.winfo_width()
    elif dir == "h":
        print(object.winfo_reqheight())
        return object.winfo_height()

#Return to main.py
def back_menu():
    root.destroy()
    pygame.quit()
    os.system("python main.py")
    

#Main UI Design
#[Background]
table_fr = CTkLabel(root, corner_radius=0, image=_bg_green, text=" ")
table_fr.place(relwidth = 1, relheight=0.95)

bottom_table_fr = CTkLabel(root, corner_radius=0, image=_bar, text=" ")
bottom_table_fr.place(rely=0.8, relwidth = 1, relheight=0.2)

#[Game]
deck_img_png = CTkImage(dark_image=Image.open(f"cards/back_card.png"), size=(_card_w, _card_h))
deck_img = CTkLabel(root, image=deck_img_png, text="CARD LEFT:\n52", text_color=_white, font=_arial, width=_card_w, height=_card_h)
deck_img.place(anchor="center", relx=0.15, rely=0.5)
deck_img.bind("<Button-1>", lambda event: add_hand())

left_deck_img = CTkLabel(root, fg_color=_base, text=" ", width=_card_w, height=_card_h)
left_deck_img.place(anchor="e", relx=0.49, rely=0.4)

right_deck_img = CTkLabel(root, fg_color=_base, text=" ", width=_card_w, height=_card_h)
right_deck_img.place(anchor="w", relx=0.51, rely=0.4)

left_deck_img.bind("<Button-1>", lambda event: place_card(True))
right_deck_img.bind("<Button-1>", lambda event: place_card(False))

discard_img = CTkLabel(root, fg_color=_base, text=" ", text_color=_white, font=_arial, width=_card_w, height=_card_h)
discard_img.place(anchor="center", relx=0.85, rely=0.5)
discard_img.bind("<Button-1>", lambda event: discrd_card())

score_lbl = CTkLabel(bottom_table_fr, image=score_lbl_png, text="Score: 0", text_color=_white, font=_arial_2)
score_lbl.place(anchor="sw", relx= 0.1, rely=0.5)

high_score_lbl = CTkLabel(bottom_table_fr, image=score_lbl_png, text=(f"Score: {max(D.leaderboard)}"), text_color=_white, font=_arial_2)
high_score_lbl.place(anchor="nw", relx= 0.1, rely=0.5)

leave_bt = CTkLabel(bottom_table_fr, image=score_lbl_png, text="Leave", text_color=_white, font=_arial_2)
leave_bt.place(anchor="e", relx= 0.9, rely=0.5)
leave_bt.bind("<Button-1>", lambda event: back_menu())

def removeDummy():
    dummy_frame.destroy()

#[Start Menu]
dummy_frame = CTkFrame(root, corner_radius=0)
dummy_frame.place(relwidth=1, relheight=1)

dummy_table_fr = CTkLabel(dummy_frame, corner_radius=0, image=_bg_green, text=" ")
dummy_table_fr.place(relwidth = 1, relheight=0.95)

dummy_bottom_table_fr = CTkLabel(dummy_frame, corner_radius=0, image=_bar, text=" ")
dummy_bottom_table_fr.place(rely=0.8, relwidth = 1, relheight=0.2)

logo = CTkLabel(dummy_frame, fg_color=_t, bg_color=_t, corner_radius=0, image=_logo, text=" ")
logo.place(anchor="center", relx=0.5, rely=0.4)

start_game_bt = CTkLabel(dummy_bottom_table_fr, image=score_lbl_png, text="Start Game", text_color=_white, font=_arial_2)
start_game_bt.place(anchor="center", relx= 0.5, rely=0.5)
start_game_bt.bind("<Button-1>", lambda event: removeDummy())

#[End Menu]
end_frame = CTkFrame(root, corner_radius=0)
end_frame.place(relx=1, relwidth=1, relheight=1)

end_table_fr = CTkLabel(end_frame, corner_radius=0, image=_bg_green, text=" ")
end_table_fr.place(relwidth = 1, relheight=0.95)

end_bottom_table_fr = CTkLabel(end_frame, corner_radius=0, image=_bar, text=" ")
end_bottom_table_fr.place(rely=0.8, relwidth = 1, relheight=0.2)

message_lbl = CTkLabel(end_frame, image=mess_img, text="Score: 0", text_color=_white, font=_arial_2)
message_lbl.place(anchor="center", relx= 0.5, rely=0.4)

leave_game_bt = CTkLabel(end_bottom_table_fr, image=score_lbl_png, text="End Game", text_color=_white, font=_arial_2)
leave_game_bt.place(anchor="center", relx= 0.5, rely=0.5)
leave_game_bt.bind("<Button-1>", lambda event: back_menu())

music_bt = CTkLabel(bottom_table_fr, text="M", font=_striked_arial_2, image=mute_img)
music_bt.place(anchor="w", relx=0.03, rely=0.5)
if not D.settings[3]: music_bt.configure(text_color="red")
music_bt.bind("<Button-1>", lambda event: toggle_music())

pygame.event.wait() #For music to keep play
root.mainloop()