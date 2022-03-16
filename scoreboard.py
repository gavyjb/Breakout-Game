#-----------------------------This is Portfolio Project 6 of 100 Days of Code on Udemy ---------------------------#
#----------------------------- Created on 3/8/2022 by Gavra J Buckman --------------------------------------------#
#------------This module handles all code logic for keeping the player's score.  Single player game---------------#

#----------------------------------- IMPORT STATEMENTS ------------------------------------------------------------#
from turtle import Turtle

#------------------------------------ CONSTANTS -------------------------------------------------------------------#
COLOR = "#ffffff"
FONT = ("Terminal", 50, "normal")
Y_POSITION = 220
COLOR_SCORE_DICT = {
    "yellow": 1,
    "green": 3,
    "orange": 5,
    "red": 7
}
MAX_SCORE = 448

#------------------------------------ CLASSES -------------------------------------------------------------------#
class Score(Turtle):
    """ This Turtle subclass handles all logic for keeping and displaying the player's score. """

    def __init__(self, x_pos):
        super().__init__()
        self.score = 0
        self.hideturtle()
        self.pencolor(COLOR)
        self.goto(x_pos, Y_POSITION)
        self.write_score()

    def write_score(self):
        """ Clears the screen and write's the score stored in the current object to the screen"""
        self.clear()
        self.write(f"{self.score}", font=FONT)

    def increase_score(self, color):
        """ Increases the score stored in the current object based on the color string passed in and then calls
        write_score()"""
        self.score += COLOR_SCORE_DICT[color]
        self.write_score()

    def game_over(self):
        """ Handles game over logic.  Figures out if player broke out or not and ends the game"""
        self.penup()
        self.goto(0, 0)
        self.pendown()
        if self.score >= MAX_SCORE:
            self.write("You broke out! You hit the max high score!")
        self.write("GAME OVER.", align="center", font=FONT)
