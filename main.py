"""
    TITLE: QUIZO
    VERSION: 0.1
    CODER: TAUSEEF HILAL TANTARY

    This is a basic text based quiz game.
"""

# Import necessary modules
import sys
import time
import datetime
from os import system
from random import choice
import pygame

# Initialize music
pygame.init()
pygame.mixer.init()

key_sound = pygame.mixer.Sound('key.wav')
pygame.mixer.music.load('bg_music.mp3')
pygame.mixer.music.play(-1)


# Formats
MENU = """
==================================================================
                       QUIZO v0.1
==================================================================
                    [1] Start Game
                    [2] View Highscore
                    [3] Credits
                    [4] Quit
=================================================================="""

DESIGN = """
==================================================================
Streak: {:3}                                          Score: {:6}
==================================================================
{}
==================================================================
        (a) {:25}(b) {}
        (c) {:25}(d) {}
=================================================================="""

with open("dictionary.txt", 'r') as dict_file:
    q_data = dict_file.readlines()

SCORES = """
==================================================================
                            RECENT SCORES
==================================================================
                  (DATE)    (TIME)   (SCORE)  (HIGHSCORES)
"""

with open("scores.txt", 'r') as scr_file:
    score_data = scr_file.readlines()

CREDITS = """
==================================================================
                  TITLE: QUIZO
                  VERSION: 0.1
                  CODER: TAUSEEF HILAL TANTARY

          Thank you for trying out my game. Hope you liked it.
=================================================================="""


# Important variables
VALID = ['1', '2', '3', '4']
SPACES = '=' * 66
option = ''
score = 0


# Functions
def start_game(q_list, design, s):
    """
        Start the real game
    """

    temp = []
    streak = 0
    current_score = 0
    valids = {'a': 0, 'b': 1, 'c': 2, 'd': 3}

    while True:

        if len(temp) == len(q_list) - 1:
            return streak, current_score

        master = choice(q_list)
        if master in temp:
            continue

        quest, ans, choices = master.split('-')
        temp.append(master)
        choices = choices.split('~')

        if len(quest) > 66:
            quest = quest[:66] + '-\n' + quest[66:]

        while True:
            clear_screen()

            if master == q_list[-1]:
                print(design.format(
                    int(streak), current_score, quest,
                    choices[0], choices[1], choices[2], choices[3])
                )
            else:
                print(design.format(
                    int(streak), current_score, quest,
                    choices[0], choices[1], choices[2], choices[3][:-1])
                )
            guess = input("Choose an option >>> ").lower()
            key_sound.play()

            if not guess in valids.keys():
                print(f"Invalid Option!\nGuess again!\n{s}")
                time.sleep(2)
                continue

            if guess in valids.keys():
                if valids[guess] == 3:
                    if choices[valids[guess]][:-1] == ans:
                        streak, current_score = correct(streak, current_score)
                        break
                if choices[valids[guess]] == ans:
                    streak, current_score = correct(streak, current_score)
                    break
                wrong()
                return streak, current_score


def correct(c_streak, c_score):
    """
        Increase score by 5 points
    """

    c_score += 5
    c_streak = c_score / 5

    return c_streak, c_score

def wrong():
    """
        Display that the guess is wrong
    """

    print("Sorry! You lost")
    time.sleep(2)

def show_scores(scores, score_file, spaced):
    """
        Show recent scores with dates
        (Under construction)
    """

    temp = []
    scrs = []
    for _ in enumerate(score_file):
        temp.append((_[0], int(_[1][23:27])))
        scrs.append(temp[-1][1])

    index = temp[scrs.index(max(scrs))][0]

    print(scores)
    for i, j in enumerate(score_file[:]):
        if i == index:
            print("           [{:02}] {}\t  ***".format((i + 1), j[:-1]))
            continue
        print("           [{:02}] {}".format((i + 1), j[:-1]))
    input(f"\n{spaced}")
    key_sound.play()

def generate_score(scr, data):
    """
        Update the scores file
    """

    _ = datetime.datetime.now()

    with open("scores.txt", 'w') as update:
        update.write(_.strftime("%Y-%m-%d %H:%M:%S") + f"    {str(scr):0>4}\n")
        update.writelines(data[:9])

    with open("scores.txt", 'r') as update:
        new_scr = update.readlines()

    return new_scr

def show_credits(cd):
    """
        Display game credits
    """

    input(f"{cd}\nPress a key to continue...")
    key_sound.play()

def show_exit():
    """
        Exit the game
    """

    print(f"Exiting...\n{SPACES}")
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit(time.sleep(2))

def clear_screen():
    """
        Clear the screen
    """

    if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
        return system("clear")
    return system("cls")


# Game loop
while True:

    clear_screen()
    print(MENU)
    option = input("Choose an option >>> ")
    key_sound.play()

    if not option in VALID:
        print(f"Invalid Option!{SPACES}")
        continue

    if option == '4':
        clear_screen()
        show_exit()
    elif option == '3':
        clear_screen()
        show_credits(CREDITS)
        continue
    elif option == '2':
        clear_screen()
        show_scores(SCORES, score_data, SPACES)
        continue
    elif option == '1':
        score = start_game(q_data, DESIGN, SPACES)
        score_data = generate_score(score, score_data)
        continue
