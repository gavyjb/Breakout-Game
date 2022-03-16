#-----------------------------This is Portfolio Project 6 of 100 Days of Code on Udemy ---------------------------#
#----------------------------- Created on 3/8/2022 by Gavra J Buckman --------------------------------------------#
#------------This module handles all code logic for game components such as the paddle, ball, and bricks----------#

#----------------------------------- IMPORT STATEMENTS ------------------------------------------------------------#
import math
from turtle import Turtle
import random

#------------------------------------ CONSTANTS -------------------------------------------------------------------#
BALL_SHAPE = "circle"
OTHER_SHAPE = "square"
WHITE = "#ffffff"
BLUE = "#0099ff"
DEFAULT_TURTLE_SIZE = 20
WALL_X_COORD = 380
WALL_Y_COORD = 280
BALL_STARTING_Y = -WALL_Y_COORD + DEFAULT_TURTLE_SIZE
BRICK_STARTING_Y = 200
PADDLE_Y = -WALL_Y_COORD + 15
MOVE_DISTANCE = 40
MOVE_DISTANCE_BALL = 10
ROW_HEIGHT = 25
MOVE_SPEED_DIVISOR = 1.5
BRICK_COLORS = ['red', 'orange', 'green', 'yellow']

#------------------------------------ CLASSES -------------------------------------------------------------------#
class Ball(Turtle):
    """ This Turtle subclass handles all logic to make the ball move and bounce when it hits another object"""

    def __init__(self):
        super().__init__()
        self.x_move = None
        self.y_move = None
        self.shape(BALL_SHAPE)
        self.color(WHITE)
        self.penup()
        self.shapesize(stretch_wid=0.8)
        self.move_speed = 0.1
        self.reset_position()

    def move(self):
        """ Makes the ball move on the screen by changing its x and y coordinates"""
        curr_x = self.xcor()
        curr_y = self.ycor()
        new_x = curr_x + self.x_move
        new_y = curr_y + self.y_move

        self.goto(new_x, new_y)
        #self.forward(MOVE_DISTANCE_BALL)

    def bounce(self, collision_type, ball_x=0, object_x=0):
        """ For future upgrade - change angle of ball based on where it hits brick or paddle"""
        self.radians()
        current_angle = self.heading()

        match collision_type:
            # Handle situation when ball bounces off paddle
            case 'p' | 'b':
                # If ball hits paddle directly in middle, just reverse direction.
                if ball_x == object_x:
                    self.left(math.pi)
                # Ball has hit paddle somewhere other than the middle, must calculate new angle
                elif ball_x > object_x:
                    self.setheading(math.pi/4)
                else:
                    self.setheading(math.pi - math.pi/4)
            case 'w':
                # Handle situation when ball bounces off ceiling or wall
                if (current_angle > math.pi and ball_x < 0) or (current_angle < math.pi and ball_x > 0):
                    self.left(math.pi / 2)
                    print(f"Turning left 90 degrees")
                else:
                    self.right(math.pi / 2)
                    print(f"Turning right 90 degrees")

        self.degrees()
        self.forward(MOVE_DISTANCE_BALL)
        print(f"Heading is {self.heading()}")

    def bounce_y(self):
        """ Changes the direction that the ball is moving on the y-axis, i.e. bouncing it"""
        self.y_move *= -1

    def bounce_x(self):
        """ Changes the direction that the ball is moving on the x-axis, i.e. bouncing it"""
        self.x_move *= -1

    def reset_position(self):
        """ Sets the ball back to the starting position"""
        self.x_move = MOVE_DISTANCE_BALL
        self.y_move = MOVE_DISTANCE_BALL
        angle = random.randint(45, 135)
        self.setheading(angle)
        self.goto(0, -WALL_Y_COORD)

    def speedup(self):
        """ Increases the speed that the ball is moving """
        self.move_speed /= MOVE_SPEED_DIVISOR


class Paddle(Turtle):
    def __init__(self):
        """
        This Turtle subclass handles all the logic to configure and move the paddle around the screen
        """
        super().__init__()
        self.shape(OTHER_SHAPE)
        self.color(BLUE)
        self.len = 9
        self.collision_distance = self.len * 10
        self.shapesize(stretch_wid=0.5, stretch_len=self.len)
        self.penup()
        self.goto(0, -WALL_Y_COORD)

    def shrink(self):
        """ Makes the paddle half its length """
        self.len = self.len / 2
        self.shapesize(stretch_len=self.len)
        self.collision_distance = self.len * 10

    def move(self, direction):
        """
        Moves the paddle left or right based on the passed in string by changing the x coordinate by a constant
        distance
        """
        if direction == 'left':
            new_x = self.xcor() - MOVE_DISTANCE
        else:
            new_x = self.xcor() + MOVE_DISTANCE

        if abs(new_x) < WALL_X_COORD:
            self.goto(new_x, self.ycor())

    def move_left(self):
        """ This function is triggered by a Left key press event in the main game"""
        self.move("left")

    def move_right(self):
        """ This function is triggered by a Right key press event in the main game"""
        self.move("right")


class Brick(Turtle):
    """
    This Turtle subclass handles all the logic to build and dispose of the bricks
    """
    def __init__(self, width, num_columns):
        super().__init__()
        self.shape(OTHER_SHAPE)
        self.penup()
        self.hideturtle()
        self.goto(-WALL_X_COORD, BRICK_STARTING_Y)
        self.brick_len = 2.5
        # The default size of a turtle is 20px, so stretch_wid=1 is 10 px and len of 2.5 is 50 px
        self.shapesize(stretch_wid=1, stretch_len=self.brick_len, outline=1)
        self.stamps = {}
        # Set up the initial board with all bricks intact
        self.draw_initial(width, num_columns)

    def draw_initial(self, width, num_columns):
        """ Draws the initial brick layout based on two passed in integer parameters: width is the width of the game
        screen and num_columns is the number of columns of bricks to make
        """
        # Loop through each brick color
        for color in BRICK_COLORS:
            self.color(color)
            # Each color gets two rows like in the original game
            for i in range(num_columns * 2):
                # Create a stamp of the current turtle color and store the id
                stamp = self.stamp()
                # Add the current coordinates tuple as key to the stamps dictionary.
                # Dictionary value is a list of color string and the id of the stamp
                self.stamps[self.position()] = [color, stamp]
                # Move forward to the next set of coordinates to stamp a brick with the same color
                self.forward(int(width / num_columns))
                # When we hit the wall go back to the left x coordinate and drop to the next row
                if self.xcor() >= WALL_X_COORD:
                    self.goto(-WALL_X_COORD, self.ycor() - ROW_HEIGHT)