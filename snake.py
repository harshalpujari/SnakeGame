import pygame
import random
import os

pygame.mixer.init()
pygame.init()

#Colors
white = (56,189,255)
red = (255,0,0)
black = (0,0,0)
blue = (0,0,255)

#Game window
screen_width = 700
screen_height = 500
gameWindow = pygame.display.set_mode((screen_width,screen_height))

#Background Image
bgimg = pygame.image.load("snake.jpg")
bgimg = pygame.transform.scale(bgimg,(screen_width, screen_height)).convert_alpha()


#Game title
pygame.display.set_caption("SnakeGame")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None,28)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])
def plot_snake(gameWindow, color, snake_list, snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((56,189,255))
        gameWindow.blit(bgimg, (0, 0))
        text_screen("Welcome to SnakeGame",black,150,200)
        text_screen("Press Space Bar to Play Game",black,127,230)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('background.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)
#Game Loop
def gameloop():
    #Creating Variables
    snake_list = []
    snake_length = 1
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    init_velocity = 3
    snake_size = 15
    fps = 60
    food_x = random.randint(10,screen_width-20)
    food_y = random.randint(10,screen_height-20)
    score = 0
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            f.write("0")
    with open("highscore.txt","r") as f:
        highscore = f.read()

    while not exit_game:
        if game_over:
            with open("highscore.txt","w") as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Game Over! Press Enter To Continue",red,150,210)
            text_screen("Score: "+str(score),blue,300,240)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_x = 0
                        velocity_y = - init_velocity

                    if event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = init_velocity
                    
                    if event.key == pygame.K_TAB:
                        score += 50

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x)<10 and abs(snake_y - food_y)<10:
                score += 10
                food_x = random.randint(0,screen_width)
                food_y = random.randint(0,screen_height)
                snake_length += 5
                if score > int(highscore):
                    highscore = score
            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: "+str(score) + "  Highscore: "+str(highscore), red, 5, 5)
            pygame.draw.rect(gameWindow, blue, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list)>snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('smash.mp3')
                pygame.mixer.music.play()
            if snake_x < 0:
                snake_x = screen_width
            if snake_x > screen_width:
                snake_x = 0
            if snake_y > screen_height:
                snake_y = 0
            if snake_y < 0:
                snake_y = screen_height
            
            plot_snake(gameWindow, black, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()
# gameloop()