#-----------------------------This is Portfolio Project 6 of 100 Days of Code on Udemy ---------------------------#
#----------------------------- Created on 3/8/2022 by Gavra J Buckman --------------------------------------------#
#--------All code is mine.  I certify that I did not copy or plagiarize anyone else's work------------------------#
# Requirement is to create a clone of the 80's hit arcade game Breakout using turtle

#----------------------------------- IMPORT STATEMENTS ------------------------------------------------------------#
from turtle import Screen, Turtle
from components import *
import time
from scoreboard import Score

#------------------------------------ CONSTANTS -------------------------------------------------------------------#
WIDTH = 800
HEIGHT = 600
NUM_COLUMNS = 14
COLLISION_DISTANCE_BRICK = 25
BGCOLOR = '#000000'
FONT = ("Terminal", 50, "normal")

#------------------------------------ UI SETUP -------------------------------------------------------------------#
screen = Screen()
screen.setup(width=WIDTH, height=HEIGHT)
screen.bgcolor(BGCOLOR)
screen.title("Gav's Breakout Game")
screen.tracer(0)

# Create the Brick object that will handle drawing and erasing the bricks. From components module
brick_handler = Brick(WIDTH, NUM_COLUMNS)

# Create the Paddle, Ball, and Score objects
paddle = Paddle()
ball = Ball()
score = Score(-WALL_X_COORD + 100)
screen.update()

# Wait for the user to press Right and Left keys to control the paddle and trigger a function each time
screen.listen()
screen.onkey(fun=paddle.move_left, key="Left")
screen.onkey(fun=paddle.move_right, key="Right")

# Variables to control number of tries, number of times the ball has hit a brick, and other various milestones
num_tries = 3
num_hits = 0
first_hit_orange = False
first_hit_red = False
second_level_red = False
# Loop to allow gameplay to continue as long as the user has tries left
while num_tries > 0:
    # Sync the time sleep to the ball's move speed so we can always see the ball's motion as fluid. Every time the ball
    # moves, update the screen
    time.sleep(ball.move_speed)
    ball.move()
    screen.update()

    # Get positions of paddle and ball and calculate collision distance based on current paddle size
    paddle_x = paddle.xcor()
    ball_x = round(ball.xcor())
    ball_y = round(ball.ycor())
    range_start = round(paddle_x - paddle.collision_distance)
    range_end = round(paddle_x + paddle.collision_distance)
    heading = ball.heading()

    # Detect collision with upper, right and left walls and bounce on appropriate axis
    if abs(ball_x) >= WALL_X_COORD:
        print("Bounced off the wall")
        ball.bounce_x()
    elif ball_y >= WALL_Y_COORD:
        print("Bounced off the ceiling")
        ball.bounce_y()

    # Detect collision with paddle and bounce on the y-axis
    if ball_x in range(range_start, range_end) and -WALL_Y_COORD < ball_y < PADDLE_Y and ball.y_move < 0:
        print("Made contact with paddle")
        ball.bounce_y()

    # Detect collision with any brick
    # Loop through all the stamps in the brick handler's stamps dictionary to see if the ball is touching any of them
    for brick_pos in brick_handler.stamps.keys():
        if ball.distance(brick_pos) < COLLISION_DISTANCE_BRICK:
            print("Hit a brick")
            num_hits += 1
            value = brick_handler.stamps.get(brick_pos)
            color = value[0]
            stamp_id = value[1]

            # Bounce the ball on y-axis and remove the brick by clearing the stamp
            #ball.bounce(collision_type='b', ball_x=ball_x)
            ball.bounce_y()
            brick_handler.clearstamp(stamp_id)

            # Remove the item from the dictionary and increment the score according to the color of the stamp
            brick_handler.stamps.pop(brick_pos)
            score.increase_score(color)

            # Check if we need to increment the ball speed
            # The first time we hit an orange brick, increase speed and set the flag
            if not first_hit_orange and color == 'orange':
                first_hit_orange = True
                ball.speedup()
                print("Speeding up because we hit orange")

            # The first time we hit a red brick, increase speed and set the flat
            if not first_hit_red and color == 'red':
                first_hit_red = True
                ball.speedup()
                print("Speeding up because we hit red")

            # Increase speed when we've hit the 4th and 12th brick
            if num_hits in [4, 12]:
                ball.speedup()
                print("Speeding up because of number of hits")

            # Shrink the paddle once we've broken through the last row of bricks and set the flag
            if not second_level_red and ball.ycor() > BRICK_STARTING_Y:
                second_level_red = True
                paddle.shrink()
            # Leave the loop
            break

    # Detect when paddle misses ball, decrease number of tries and send ball back to starting position
    if ball_x not in range(range_start, range_end) and ball_y < -WALL_Y_COORD:
        print("Paddle missed the ball")
        print(f"Ball coordinates are {ball.position()}")
        print(f"Paddle coordinates are {paddle.position()}")
        num_tries -= 1
        # Send ball back to starting position after a short pause
        time.sleep(0.5)
        ball.reset_position()

# Call game over function and exit
score.game_over()
screen.update()
screen.exitonclick()
