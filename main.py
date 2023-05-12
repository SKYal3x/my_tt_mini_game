#python 3.8 
import pygame
import os

from ball import BallSprite, Player1Sprite, Player2Sprite, TableSprite, game
# from random import randint as rndm
# defining all of the constant values in all cap

# exctract this to a separate file afterwards
WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TT Masters")

BACKGROUND_COLOR = (125, 195, 170)
SCALE = 0.425
FPS = 59
VEL = 5
PLAYER_WIDTH, PLAYER_HEIGHT = 75, 60
TABLE_WIDTH, TABLE_HEIGHT = int(1391*SCALE), int(460*SCALE)
BALL_WIDTH, BALL_HEIGT = 12, 12
PLAYER_1_START_X, PLAYER_1_START_Y = 0, 0
PLAYER_2_START_X, PLAYER_2_START_Y = 0, 0
TABLE_POS_X, TABLE_POS_Y = 304, 300

'''
PLAYER_1 = pygame.image.load(
    os.path.join('Assets','img', 'players','player_1.png'))

# resize and rotate
PLAYER_1 = pygame.transform.rotate(
    pygame.transform.scale(
        PLAYER_1, (PLAYER_WIDTH, PLAYER_HEIGHT)), 360)

PLAYER_2 = pygame.image.load(
    os.path.join('Assets','img', 'players','player_2.png'))

# resize and rotate
PLAYER_2 = pygame.transform.rotate(
    pygame.transform.scale(
        PLAYER_2, (PLAYER_WIDTH, PLAYER_HEIGHT)), 180)

TABLE = pygame.image.load(
    os.path.join('Assets','img', 'table','table.png')) 

TABLE = pygame.transform.scale(
    TABLE, (TABLE_WIDTH, TABLE_HEIGHT))

#BALL = pygame.image.load(
#    os.path.join('Assets', 'img', 'ball', 'ball.png'))

    
#BALL = pygame.transform.scale(
#    BALL, (BALL_WIDTH, BALL_HEIGT))

'''

'''    
def draw_window(player1, player2, table, ball, draw_ball):
    WIN.fill(BACKGROUND_COLOR)
    # used to put text or images onto the screen
    
    # we now have the rectangles for our objects
    # and can access the coordinates directly
    
    WIN.blit(PLAYER_1, (player1.x, player1.y))
    WIN.blit(PLAYER_2, (player2.x, player2.y))
    WIN.blit(TABLE, (table.x, table.y))
    if draw_ball:
        WIN.blit(BALL.image, (ball.x, ball.y))
    pygame.display.update()
'''        
def main():
    
    # rectangles for the players
    PLAYER_1 = Player1Sprite('players',
                    position=(PLAYER_1_START_X, PLAYER_1_START_Y),
                    size = (PLAYER_WIDTH, PLAYER_HEIGHT))
                    
    PLAYER_2 = Player2Sprite('players',
                    position=(PLAYER_2_START_X, PLAYER_2_START_Y),
                    size = (PLAYER_WIDTH, PLAYER_HEIGHT))
                        
    TABLE = TableSprite('table',
                    position=(TABLE_POS_X, TABLE_POS_Y)
                    ,size = (TABLE_WIDTH, TABLE_HEIGHT))
    
    BALL = BallSprite('ball',
                  position=(400, 100),
                  size=(BALL_WIDTH, BALL_HEIGT))
    
    GAME = game(PLAYER_1, PLAYER_2, TABLE, BALL)
    
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group(TABLE, PLAYER_1, PLAYER_2, BALL)
    run = True
    draw_ball = False 
    
    while run:
        # speed control
        clock.tick(FPS)
        # looping through all of the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # parse pressed keys 
        keys_pressed = pygame.key.get_pressed()
        PLAYER_1.handle_movement(keys_pressed, BALL)
        GAME.check_conditions()
        
        WIN.fill(BACKGROUND_COLOR)
        all_sprites.update()
        all_sprites.draw(WIN)
        pygame.display.update()
            

        #BALL.update()
        
        #draw_window(player1, player2, table, ball, draw_ball)

    pygame.quit()
    
if __name__ == "__main__":
    main()