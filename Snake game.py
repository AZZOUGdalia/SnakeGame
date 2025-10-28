import turtle
import time



delay = 0.1


# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("pink")
wn.setup(width=600, height=600)
wn.tracer(0)  # Turns off the screen updates


#quitter
running = True
def stop_game():
    global running
    print("Game Stopped")
    running = False
    
#Snake head 
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black") 
head.penup()
head.goto(0,0)
head.direction = "stop" 

# Functions to control the snake
def go_up():
    
        head.direction = "up"
def go_down():
        head.direction = "down"
def go_left():
        head.direction = "left"
def go_right():
        head.direction = "right"


def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)  

        
# Keyboard bindings
wn.listen()

wn.onkeypress(go_up, "z")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "q")
wn.onkeypress(go_right, "d")

wn.onkey(stop_game, "Escape")

try:
    while running:
        wn.update()
        move()
        time.sleep(delay)
except turtle.Terminator:
    # Fenêtre fermée pendant la boucle -> on sort sans crasher
    pass
finally:
    try:
        wn.bye()
    except turtle.Terminator:
        pass
