import random
import time
import sys
import os

# !/usr/bin/env python3

"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round.  The game is a best of 3 and if
there is no winner, the player will have the option of playing a 'golden goal'
style tiebreaker"""

moves = ['rock', 'paper', 'scissors']


# color definitions used in user interface
class color:
    red = '\033[1;31m'
    green = '\033[1;32m'
    yellow = '\033[1;33m'
    white = '\033[1;37m'
    grey = '\033[0;37m'
    magenta = '\033[1;35m'
    magenta_bg = '\033[0;36;45m'
    blue = '\033[1;36m'
    underline = '\033[4m'
    std = '\033[0;37;0m'
    game_start = '\033[2;35;46m'


# Parent class for all players in the game
class Player:
    def __init__(self):
        self.wincount = 0
        moves = ['rock', 'paper', 'scissors']
        self.my_move = random.choice(moves)
        self.their_move = random.choice(moves)

    def win(self):
        self.wincount += 1

    def move(self):
        return 'rock'

    def learn(self, my_move, their_move):
        self.my_move = my_move
        self.their_move = their_move


# The RandomPlayer(Player) class picks a random move each turn
class RandomPlayer(Player):
    def move(self):
        return random.choice(moves)


# First move is random, copies player's last move after that
class ReflectPlayer(Player):
    def move(self):
        return self.their_move


# Cycles from rock --> paper --> scissors with first move being random
class CyclePlayer(Player):
    def move(self):
        if self.my_move == "rock":
            return "paper"
        if self.my_move == "paper":
            return "scissors"
        if self.my_move == "scissors":
            return "rock"


# Human player class, player 1
class HumanPlayer(Player):
    def move(self):
        while True:
            move = input(f"{color.white}Make Your Move: ")
            if move.lower() == "rock" or move == "1":
                return "rock"
            elif move.lower() == "paper" or move == "2":
                return "paper"
            elif move.lower() == "scissors" or move == "3":
                return "scissors"
            else:
                print("\nPlease try again:\nType in: 1/2/3 or "
                      + "'rock'/'paper'/'scissors'\n")


# returns true if move one beats move two
def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


# Outputs a typed-style message as opposed to print function
def typing(message, delay):
    for typing in message:
        sys.stdout.write(typing)
        sys.stdout.flush()
        time.sleep(delay)


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    # Functinon allows typing function as above to be used within the class
    def typing(self, message, delay):
        for typing in message:
            sys.stdout.write(typing)
            sys.stdout.flush()
            time.sleep(delay)

    # outputs a colored decoration inputted by user
    def decoration(self, string, delay, fgcolor, bgcolor):
        sys.stdout.write(bgcolor)
        sys.stdout.write(fgcolor)
        for typing in string:
            sys.stdout.write(typing)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write(color.std)

    # Plays a single round of rock paper scissors
    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        self.typing(f"{color.green}Player 1: {move1}  {color.red}"
                    + f"Player 2: {move2}\n\033[1;37m", 0.01)
        time.sleep(0.5)
        if move1 == move2:
            print(f"{color.blue}Both players picked {move1}, it's a TIE!")
        elif beats(move1, move2):
            print(f"{color.green}Player 1 Wins!")
            self.p1.win()
        else:
            print(f"{color.red}Player 2 Wins!")
            self.p2.win()
        time.sleep(0.5)
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    # Plays a best of 3 game with a tie-breaker if necessary
    def play_game(self):
        self.typing(f"\n\n{color.yellow}For each round, type in 1 / rock, "
                    + "2 / paper or 3 / scissors\n", 0.01)
        time.sleep(1)
        self.decoration("_______________________", 0.03, color.magenta_bg,
                        color.blue)
        self.typing(f"{color.game_start}Game Start!!!{color.std}", 0.1)
        self.decoration("_______________________", 0.03, color.magenta_bg,
                        color.blue)
        time.sleep(1)
        print("\n")
        for round in range(3):
            time.sleep(0.3)
            print(f"\n\n{color.yellow}Round {round + 1}:")
            time.sleep(0.3)
            self.play_round()
            print(f"{color.grey}SCORE: {color.green}Player 1 = "
                  + f"{self.p1.wincount} {color.red}Player 2 = "
                  + f"{self.p2.wincount}")
            time.sleep(1)
        self.typing(f"\n\n{color.yellow}{color.underline}Game Over:"
                    + f"{color.std}\n", 0.3)
        print(f"{color.grey}FINAL SCORE: {color.green}Player 1 = "
              + f"{self.p1.wincount} {color.red}Player 2 = {self.p2.wincount}")
        if self.p1.wincount == self.p2.wincount:
            self.typing(f"{color.magenta}It's a Tie!\n\n", 0.1)
            while self.p1.wincount == self.p2.wincount:
                yesno = input(f"{color.white}Would you like to "
                              + f"play a Tie Breaker? (yes/no):")
                if yesno.lower() == "yes" or yesno.lower() == "y":
                    while self.p1.wincount == self.p2.wincount:
                        self.typing(f"\n{color.magenta}Next score wins "
                                    + f"the game!!!\n\n", 0.007)
                        self.play_round()
                        if self.p1.wincount > self.p2.wincount:
                            self.typing(f"\n{color.green}Congratulations "
                                        + "Player 1, you won the game!!!", 0.1)
                            break
                        if self.p2.wincount > self.p1.wincount:
                            self.typing(f"\n{color.red}Congratulations "
                                        + "Player 2, you won the game!!!", 0.1)
                            break
                elif yesno.lower() == "no" or yesno.lower() == "n":
                    self.typing(f"\n{color.blue}I hope you had fun.  "
                                + "Have a great day!!!", 0.007)
                    break
                else:
                    print(f"\n{color.grey}Please try again:")
        elif self.p1.wincount > self.p2.wincount:
            self.typing(f"{color.green}Player 1 WINS!!!", 0.3)
        elif self.p2.wincount > self.p1.wincount:
            self.typing(f"{color.red}Player 2 WINS!!!", 0.3)
        else:
            self.typing(f"{color.white}I hope you had fun.  Have a great "
                        + "day!!!", 0.007)
        print(f"{color.white}\n")
        time.sleep(10)


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    typing(f"\n{color.yellow}Get ready to play Rock, Paper, Scissors!\nYou can"
           + " choose from the opponents listed below:\n", 0.01)
    typing(f"{color.grey}1 - Rock Player\n2 - Random Player\n3 - Reflect "
           + "Player\n4 - Cycle Player\n5 - Random Opponent", 0.0005)
    while True:
        enemy = input(f"\n\n{color.white}Pick a number from 1-5: ")
        if enemy == "1":
            selection = Player()
            break
        elif enemy == "2":
            selection = RandomPlayer()
            break
        elif enemy == "3":
            selection = ReflectPlayer()
            break
        elif enemy == "4":
            selection = CyclePlayer()
            break
        elif enemy == "5":
            selection = random.choice([Player(), RandomPlayer(),
                                      ReflectPlayer(), CyclePlayer()])
            break
        else:
            print("Please Try Again...\n")
    game = Game(HumanPlayer(), selection)
    game.play_game()
