import pygame, sys, time, random

#initial game variables

# Window size
frame_size_x = 720
frame_size_y = 480

#Parameters for Snake
snake_pos = [100, 50]
#snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
direction = 'RIGHT'
change_to = direction

#Parameters for food
food_pos = [250, 300]
food_spawn = False
food_size = [16,16]
food = pygame.Rect(food_pos[0], food_pos[1], food_size[0], food_size[1])

score = 0
speed = 10 

threshold = [(20 + food_size[0])/2, (20 + food_size[1])/2]

# Initialise game window
pygame.init()
pygame.display.set_caption('Snake Eater')
screen = pygame.display.set_mode((frame_size_x, frame_size_y))



# FPS (frames per second) controller to set the speed of the game
fps_controller = pygame.time.Clock()
bg_color = (0,0,0)
parts = []
part = pygame.Rect(200, 50 ,20, 20)
parts.append(part)
part2 = pygame.Rect(180, 50, 20, 20)
parts.append(part2)
part3 = pygame.Rect(160, 50, 20, 20)
parts.append(part3)
directions = [[1,0],[1,0],[1,0]]



def check_for_events():
    """
    This should contain the main for loop (listening for events). You should close the program when
    someone closes the window, update the direction attribute after input from users. You will have to make sure
    snake cannot reverse the direction i.e. if it turned left it cannot move right next.
    """
    global change_to
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP :
                if (directions[0][1] == 0):
                    change_to = 'UP'
            elif event.key == pygame.K_DOWN :
                if (directions[0][1] == 0):
                    change_to = 'DOWN'
            elif event.key == pygame.K_RIGHT :
                if (directions[0][0] == 0):
                    change_to = 'RIGHT'
            elif event.key == pygame.K_LEFT :
                if(directions[0][0] == 0):
                    change_to = 'LEFT'

def create_food():
    """ 
    This function should set coordinates of food if not there on the screen. You can use randrange() to generate
    the location of the food.
    """
    global frame_size_x, frame_size_y, food_size, food_spawn, food
    x = 0
    if food_spawn == False:
        food_pos = [random.randrange(0,frame_size_x-food_size[0]),random.randrange(25,frame_size_y-food_size[1])]
        food = pygame.Rect(food_pos[0], food_pos[1], food_size[0], food_size[1])
        food_spawn = True

def update_snake():
    """
     This should contain the code for snake to move, grow, detect walls etc.
     """
    # Code for making the snake move in the expected direction
    global frame_size_x, frame_size_y, parts, direction, directions, food_spawn, food, score
    if change_to != direction:
        if change_to == 'UP'  and directions[1] == directions[2] and abs(parts[0].centerx-parts[1].centerx)>=20:
            if (directions[0][1] == 0):
                directions[0] = [0,1]
                direction = 'UP'
        elif change_to == 'DOWN'  and directions[1] == directions[2] and abs(parts[0].centerx-parts[1].centerx)>=20:
            if (directions[0][1] == 0):
                directions[0] = [0,-1]
                direction = 'DOWN'
        elif change_to == 'RIGHT'  and directions[1] == directions[2] and abs(parts[0].centery-parts[1].centery)>=20:
            if (directions[0][0] == 0):
                directions[0] = [1,0]
                direction = 'RIGHT'
        elif change_to == 'LEFT'  and directions[1] == directions[2] and abs(parts[0].centery-parts[1].centery)>=20:
            if(directions[0][0] == 0):
                directions[0] = [-1,0]
                direction = 'LEFT'

    # Make the snake's body respond after the head moves. The responses will be different if it eats the food.
    # Note you cannot directly use the functions for detecting collisions 
    # since we have not made snake and food as a specific sprite or surface.

    if abs(parts[0].centerx - food.centerx) < threshold[0] and abs(parts[0].centery - food.centery) < threshold[1]:
        new_part = pygame.Rect(parts[len(parts) - 1].centerx - 10 - directions[len(parts)-1][0]*20, parts[len(parts) - 1].centery - 10 + directions[len(parts)-1][1]*20 , 20, 20)
        new_part_direction = directions[len(parts) - 1]
        parts.append(new_part)
        directions.append(new_part_direction)
        score = score + 1
        food_spawn = False
        create_food()
        pygame.draw.rect(screen, (255, 0, 0), food)
    
    for i in range(0,len(parts)):
        if i == 0 and i + 1<len(parts) and directions[i] != directions[i+1]:
            if directions[i][0] == 0:
                if parts[i].centerx != parts[i+1].centerx:
                    if directions[i][1] == 1:
                        parts[i].height = parts[i+1].midbottom[1] - parts[i].midtop[1] + speed
                    else:
                        parts[i].height = parts[i].midbottom[1] - parts[i+1].midtop[1] + speed
                else:
                    if directions[i][1] == -1:
                        parts[i].centery += 20
                    parts[i].height = 20
                    directions[i+1] = directions[i]
            elif directions[i][1] == 0:
                if parts[i].centery != parts[i+1].centery:
                    if directions[i][0] == 1:
                        parts[i].width = (parts[i].midright[0] - parts[i+1].midleft[0]) + speed
                    else:
                        parts[i].width = (-parts[i].midleft[0] + parts[i+1].midright[0]) + speed
                else:
                    if directions[i][0] == 1:
                        parts[i].centerx += 20
                    parts[i].width = 20
                    directions[i+1] = directions[i]                
        if i>=1 and i<(len(parts)-1) and directions[i] != directions[i+1]:
            if directions[i] == [0,1]:
                if parts[i].centerx != parts[i+1].centerx:
                    parts[i].height = parts[i+1].midbottom[1] - parts[i-1].midbottom[1] 
                else:
                    parts[i].height = 20
                    directions[i+1] = directions[i]
            elif directions[i] == [0,-1]:
                if parts[i].centerx != parts[i+1].centerx:
                    parts[i].height = parts[i-1].midtop[1] - parts[i+1].midtop[1] 
                else:
                    parts[i].height = 20
                    directions[i+1] = directions[i]                    
            elif directions[i] == [1,0]:
                if parts[i].centery != parts[i+1].centery: 
                    parts[i].width = abs(parts[i-1].midleft[0] - parts[i+1].midleft[0])
                else:
                    parts[i].width = 20
                    directions[i+1] = directions[i]
            elif directions[i] == [-1,0]:
                if parts[i].centery != parts[i+1].centery: 
                    parts[i].width = abs(parts[i+1].midright[0] - parts[i-1].midright[0])
                else:
                    parts[i].width = 20
                    directions[i+1] = directions[i]                   
        parts[i].centerx += speed*directions[i][0]
        parts[i].centery -= speed*directions[i][1]
        if i == 0 and i + 1<len(parts):
            if directions[i] == [1,0] and directions[i+1][0] == 0:
                dummy = (parts[i+1].midleft[0],parts[i].centery)
                parts[i].midleft = dummy
            elif directions[0] == [-1,0] and directions[i+1][0] == 0:
                dummy = (parts[i+1].midright[0],parts[i].centery)
                parts[i].midright = dummy
            elif directions[0] == [0,-1] and directions[i+1] != directions[i]:
                dummy = (parts[i].centerx,parts[i+1].midtop[1])
                parts[i].midtop = dummy
        if i>=1 and i<(len(parts) - 1):
            if directions[i] == [1,0] and (directions[i+1][0] == 0 or directions[i-1] == [1,0]):
                parts[i].midright = parts[i-1].midleft
            elif directions[i] == [-1,0] and (directions[i+1][0] == 0 or directions[i-1] == [-1,0]):
                parts[i].midleft = parts[i-1].midright
            elif directions[i] == [0,-1] and (directions[i+1][1] == 0 or directions[i-1] == [0,-1]):
                parts[i].midbottom = parts[i-1].midtop


    # End the game if the snake collides with the wall or with itself. 
    for i in range(2, len(parts)):
        if directions[i][1] == 0:
            if directions[0][0] == 0:
                if abs(parts[0].centery - parts[i].centery) < 20 and abs(parts[0].centerx - parts[i].centerx) < 20:
                    game_over()
            elif directions[0][0] == -directions[i][0]:
                if abs(parts[0].centerx - parts[i].centerx) < 20 and abs(parts[0].centery - parts[i].centery) < 20:
                    game_over()
        elif directions[i][0] == 0:
            if directions[0][1] == 0:
                if abs(parts[0].centerx - parts[i].centerx) < 20 and abs(parts[0].centery - parts[i].centery) < 20:
                    game_over()
            elif directions[0][1] == -directions[i][1]:
                if abs(parts[0].centery - parts[i].centery) < 20 and abs(parts[0].centerx - parts[i].centerx) < 20:
                    game_over()
    if not (parts[0].centerx >=10 and parts[0].centerx <= frame_size_x - 10 and parts[0].centery >=10 and parts[0].centery <= frame_size_y - 10):
        game_over()


def show_score(pos, color, font, size):
    """
    It takes in the above arguements and shows the score at the given pos according to the color, font and size.
    """
    global screen, score, frame_size_x
    Font = pygame.font.SysFont(font,  size)
    x = str(score)
    Score = Font.render("Score : " + x,True,color)
    Score_rect = Score.get_rect()
    Score_rect.center = (frame_size_x/2, 10)
    screen.blit(Score, Score_rect)

def update_screen():
    """
    Draw the snake, food, background, score on the screen
    """
    global screen, bg_color, parts, food
    screen.fill(bg_color)
    for i in range(0,len(parts)):
        pygame.draw.rect(screen, (0,255,0), parts[i])
    pygame.draw.rect(screen, (255, 0, 0), food)
    show_score((100,20), (255,255,255), None, 20)
    pygame.display.flip()

def game_over():
    """ 
    Write the function to call in the end. 
    It should write game over on the screen, show your score, wait for 3 seconds and then exit
    """
    global screen, frame_size_x, food_size, food, score
    gameover_img = pygame.font.SysFont(None, 48).render("GAME OVER", True, (240,240,240))
    gameover_rect = gameover_img.get_rect()
    gameover_rect.centerx = frame_size_x/2
    gameover_rect.top = 20
    parts.clear()
    food_size = [0, 0]
    food = pygame.Rect(food_pos[0], food_pos[1], food_size[0], food_size[1]) 
    update_screen()
    screen.fill((0,0,0))
    Font = pygame.font.SysFont(None, 24)
    x = str(score)
    Score = Font.render("Score : " + x,True,(240,240,240))
    Score_rect = Score.get_rect()
    Score_rect.center = (frame_size_x/2, frame_size_y/2)
    screen.blit(gameover_img, gameover_rect)
    screen.blit(Score, Score_rect)
    pygame.display.flip()
    time.sleep(3)
    sys.exit()

# Main loop
while True:
    # Make appropriate calls to the above functions so that the game could finally run
        check_for_events()
        update_snake()
        update_screen()
        
    # To set the speed of the screen
        fps_controller.tick(25)
