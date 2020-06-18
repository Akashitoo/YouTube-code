#Colors Palette
# background 22,41,85
# snake 60,215,60
# food 210,45,60

import pygame
import json
# could also use the third party library PrettyTable 

from random import randint



def drawFood():
    food_color = pygame.Color(210,45,60)
    food_rect = pygame.Rect((food[0]*tile_w, food[1]*tile_h), (tile_w, tile_h))
    pygame.draw.rect(wind, food_color, food_rect)

def drawSnake():
    snk_color = pygame.Color(60,215,60)
    for cell in snake:
        cell_rect = pygame.Rect((cell[0]*tile_w, cell[1]*tile_h), (tile_w, tile_h))
        pygame.draw.rect(wind, snk_color, cell_rect)


def loadScoreboard():
    SCOREBOARD_LEN = 5
    scoreboard = []
    try:
        file = open('scoreboard.snk')
        scoreboard = json.load(file)
        file.close()
    except:
        print("An error occured while accessing the scoreboard")
    
    i=len(scoreboard)
    while i < SCOREBOARD_LEN:
        i += 1
        scoreboard.append({
            "rank": i,
            "name": "Anonymous",
            "score": 0
        })
    return scoreboard


def saveScore(snake, name):
    score = len(snake) - INITIAL_LENGTH
    scoreboard = loadScoreboard()

    for i in range(len(scoreboard)):
        if scoreboard[i]["score"] < score:
            scoreboard.insert(i, {"rank":i+1, "name":name, "score":score})
            scoreboard.pop()

            for j in range(i+1, len(scoreboard)):
                scoreboard[j]['rank'] += 1
            
            try:
                file = open('scoreboard.snk', 'w')
                json.dump(scoreboard, file)
                file.close()
            except IOError as e:
                print('Couldnt manage to save the score :', e)
            break

def printScoreboard():
    from math import ceil
    scoreboard = loadScoreboard()
    widths = [0]*len(scoreboard[0]) # width of each columns
    
    # insert header into the scoreboard
    scoreboard.insert(0, {key:key.capitalize() for key in scoreboard[0]})

    # Determine width of each columns
    for entry in scoreboard:
        i = 0
        for key in entry:
            leng = len( str(entry[key]) )
            widths[i] = widths[i] if leng <= widths[i] else leng
            i += 1

    # Print scoreboard
    print()
    for entry in scoreboard:
        i = 0 ; print('|', end='')
        for key in entry:
            offset = ( widths[i] - len(str(entry[key])) ) / 2
            print( ceil(offset)*' ', entry[key], int(offset)*' ', end = '|')
            i += 1
        print()
    print()


def updateSnake(direction):
    global food
    dirX, dirY = direction
    head = snake[0].copy()
    head[0] = (head[0]+dirX)%tiles_x
    head[1] = (head[1]+dirY)%tiles_y

    if head in snake[1:]:
        return False
    elif head == food:
        food = None
        while food is None:
            newfood = [
                randint(0, tiles_x-1),
                randint(0, tiles_y-1)
            ]
            food = newfood if newfood not in snake else None

    else:
        snake.pop()

    snake.insert(0, head)
    return True


## Init the window
sw = 640
sh = 480
wind = pygame.display.set_mode((sw, sh))

bg_color = pygame.Color(22,41,85)

## Define the playground
tiles_x = 32
tiles_y = 24

tile_w = sw // tiles_x
tile_h = sh // tiles_y

## Define the snake
snk_x, snk_y = tiles_x // 4, tiles_y //2

INITIAL_LENGTH = 3
snake = [[snk_x -i, snk_y] for i in range(INITIAL_LENGTH)] # nouvelle version du bloc ci dessous
""" snake = [
    [snk_x, snk_y],
    [snk_x-1, snk_y],
    [snk_x-2, snk_y]
] """

## Define the food
food = [tiles_x//2, tiles_y//2]


## Game loop
running = True
direction = [1,0]
while running:
    pygame.time.Clock().tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == 100 and not direction == [-1,0]: # 'd' to right
                direction = [1,0]
            if event.key == 97 and not direction == [1,0]: # 'q' to left
                direction = [-1,0]
            if event.key == 119 and not direction == [0,1]: # 'z' up
                direction = [0,-1]
            if event.key == 115 and not direction == [0,-1]: # 's' down
                direction = [0,1]


    # update
    if updateSnake(direction) == False:
        print("Game over")
        if input('Save the score ? (y/N)> ').lower() in ['o', 'oui', 'y', 'yes']:
	        name = input('What is your name ?> ')
	        saveScore(snake, name) # save the score
	        printScoreboard()
        running = False

    # draw
    wind.fill(bg_color)

    drawFood()
    drawSnake()

    pygame.display.update()


pygame.quit()





