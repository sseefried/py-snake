from os import system
import curses
import shutil
from threading import Timer
import random

system("clear")

start_game = 1
maxstarheight = 20
maxstarwidth = 50
minstarwidth = 0
minstarheight = 0
game_run = 1
snake_x = [26, 25]
snake_y = [9, 9]
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
STILL = 4
current_direction = STILL
food_x = None
food_y = None
FRAME_RATE = 0.1 # DOES NOT LIKE THIS IDEA
min_snake_x = 2
start_timer = False
screen_flash = False



def grow_snake_food():
    l = len(snake_x)
    snake_x.append(snake_x[l-1])    
    snake_y.append(snake_y[l-1])
    snake_x.append(snake_x[l-1])    
    snake_y.append(snake_y[l-1])      
    return

 

def grow_snake_timer():
    global timer
    timer = Timer(1.0, grow_snake_timer)
    l = len(snake_x)
    snake_x.append(snake_x[l-1])    
    snake_y.append(snake_y[l-1])
    timer.start()      
    return
timer = Timer(1.0, grow_snake_timer)  
   

def food_overlaps():
    anyoverlap = False
    i = 0
    while i < len(snake_x):
        if food_x == snake_x[i] and food_y == snake_y[i]:
            anyoverlap = True
        i += 1            
    return anyoverlap
   
   
   
def game_over():
    system("sleep 2")
    i = 0
    while i < 3:          
        screen.clear()      
        screen.addstr(10, 34, "GAME OVER")
        screen.refresh()
        system("sleep 0.5")                      
        screen.clear()
        screen.addstr(10, 43, "")
        screen.refresh()
        system("sleep 0.5")
       
        if i == 2:
            screen.clear()      
            screen.addstr(10, 34, "GAME OVER")
            screen.refresh()
            system("sleep 1.5")
        i += 1

    screen.clear()
    screen.addstr(10, 33, "FINAL SCORE: %d" % (FINAL_SCORE))
    screen.refresh()    
    system("sleep 3")    

           
   

def printscreen():        
    screen.clear()
    screen.addstr(0, 0, "Use the WASD keys to move around! Press Q to exit game")
    y = minstarheight
 
    while y < maxstarheight:
       
        x = minstarwidth            
        while x < maxstarwidth:
           
            screen.addstr(y + 1, x, "-")
           
            if game_type == "f":
                if food_x == x and food_y == y:
                    screen.addstr(y + 1, x, "o")
               
            i = 0
            while i < len(snake_x):

                if (x == snake_x[i] and y == snake_y[i]):
                    screen.addstr(y + 1, x, "*")
                     
                i += 1
                                                                                                   
            x += 1
           
        y += 1        
    screen.refresh()
    return
   
   
   
screen = curses.initscr()
curses.noecho()
curses.cbreak()
     
screen.clear()
screen.addstr(9, 3, "WELCOME TO SNAKE! CHOOSE GAME MODE: PRESS 't' FOR TIME OR 'f' FOR FOOD")
screen.refresh()
try:        
    game_type = screen.getkey()
except:
    game_type = ""
   
while game_type != "f" and game_type != "t":
    screen.clear()
    screen.addstr(9, 20, "PLEASE ONLY PRESS 't' OR 'f' TO PROCEED")
    screen.refresh()
    try:        
        game_type = screen.getkey()
    except:
        game_type = ""
       
    if game_type == "f" or game_type == "t":
        break


screen.nodelay(True)
while game_run == 1:          
    printscreen()
    bool(screen_flash)
    if screen_flash == False:
        i = 0  
        while i < 3:
            system("sleep 0.3")
            screen.clear()      
            screen.addstr(20, 50, "")
            screen.refresh()
            system("sleep 0.3")                      
            screen.clear()
            printscreen()
            screen.refresh()
            system("sleep 0.3")
             
            i += 1
                 
        screen_flash = True
       
    system("sleep 0.1")  
   
    if food_x == None and food_y == None:
        while True:            
            food_x = random.randint(minstarwidth, maxstarwidth - 1)
            food_y = random.randint(minstarheight, maxstarheight - 1)
            if not food_overlaps():
                break
               
    try:        
        move = screen.getkey()
    except:
        move = ""
       
    if move == "w" and (current_direction == LEFT or current_direction == RIGHT or current_direction == STILL):
        current_direction = UP
       
    if move == "a" and (current_direction == UP or current_direction == DOWN or current_direction == STILL):
        current_direction = LEFT
       
    if move == "s" and (current_direction == LEFT or current_direction == RIGHT or current_direction == STILL):
        current_direction = DOWN
     
    if move == "d" and (current_direction == UP or current_direction == DOWN or current_direction == STILL):
        current_direction = RIGHT
       
    if move == "" and (current_direction == STILL):
        current_direction = STILL  
       
    if move == "q":
        game_run = 0
   
    if current_direction != STILL:          
        head_x = snake_x[0]
        head_y = snake_y[0]
       
        if current_direction == RIGHT:
            head_x += 1
           
        if current_direction == LEFT:
            head_x -= 1
           
        if current_direction == UP:
            head_y -= 1
           
        if current_direction == DOWN:
            head_y += 1
       
       
        snake_x.pop() #removes last element of list here
        snake_y.pop() # ^^
        snake_x.insert(0, head_x) #inserts new element at front
        snake_y.insert(0, head_y) #and shifts everything down
     

         
    i = 0    
    while i < len(snake_x):    
         
        if snake_x[i] < minstarwidth:
            snake_x[i] = maxstarwidth - 1
           
        if snake_x[i] >= maxstarwidth:
            snake_x[i] = minstarwidth
           
        i += 1
           
                   
    i = 0
    while i < len(snake_y):
       
        if snake_y[i] < minstarheight:
            snake_y[i] = maxstarheight - 1  
           
        if snake_y[i] >= maxstarheight:
            snake_y[i] = minstarheight
           
        i += 1
       
    head_x = snake_x[0]
    head_y = snake_y[0]
       
    if game_type == "f":    
        if head_x == food_x and head_y == food_y:
            grow_snake_food()  
            food_x = None
            food_y = None
           
    bool(start_timer)
    if game_type == "t" and start_timer == False and current_direction != STILL:
        timer.start()
        timer
        start_timer = True
       
               
    i = 1        
    while i < len(snake_x):        
        if head_x == snake_x[i] and head_y == snake_y[i] and current_direction != STILL:            
            game_run = 0
           
           
        i += 1  
   
       
FINAL_SCORE = len(snake_x)        
game_over()
if game_type == "t":
    timer.cancel()          
curses.endwin()