#python 3.8 
import pygame
import os

from ball import BallSprite, Player1Sprite, Player2Sprite, TableSprite, NetSprite, FloorSprite, game
from text import TextTable
from start_menu import start_menu

# from random import randint as rndm
# defining all of the constant values in all cap

# exctract this to a separate file afterwards
pygame.init()
WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TT Masters")

BACKGROUND_COLOR = (125, 195, 170)
SCALE = 0.425
FPS = 60
VEL = 5
PLAYER_1_WIDTH, PLAYER_1_HEIGHT = 20, 50
PLAYER_2_WIDTH, PLAYER_2_HEIGHT = 20, 60
TABLE_WIDTH, TABLE_HEIGHT = int(1391*SCALE), int(460*SCALE)
BALL_WIDTH, BALL_HEIGT = 13, 13
PLAYER_1_START_X, PLAYER_1_START_Y = 200, 200
PLAYER_2_START_X, PLAYER_2_START_Y = 900, 400
TABLE_POS_X, TABLE_POS_Y = 304, 334
NET_POS_X, NET_POS_Y = 581, 292
NET_WIDTH, NET_HEIGH = 40, 56
FLOOR_WIDTH, FLOOR_HEIGH = 15000, 300
FLOOR_POX_X, FLOOW_POS_Y = -FLOOR_WIDTH/2, 300
#hide mouse cursor
pygame.mouse.set_visible(False)
     
def main():
    
    # rectangles for the players
    PLAYER_1 = Player1Sprite('players',
                    position=(PLAYER_1_START_X, PLAYER_1_START_Y),
                    size = (PLAYER_1_WIDTH, PLAYER_1_HEIGHT))
                    
    PLAYER_2 = Player2Sprite('players',
                    position=(PLAYER_2_START_X, PLAYER_2_START_Y),
                    size = (PLAYER_2_WIDTH, PLAYER_2_HEIGHT))
                        
    TABLE = TableSprite('table',
                    position=(TABLE_POS_X, TABLE_POS_Y)
                    ,size = (TABLE_WIDTH, TABLE_HEIGHT))
                    
    NET = NetSprite('net',
                    position=(NET_POS_X, NET_POS_Y)
                    ,size = (NET_WIDTH, NET_HEIGH))
    
    BALL = BallSprite('ball',
                  position=(900, 50),
                  size=(BALL_WIDTH, BALL_HEIGT))
    
    FLOOR = FloorSprite('floor',
                    position=(FLOOR_POX_X, TABLE.rect.bottom),
                    size=(FLOOR_WIDTH, FLOOR_HEIGH)
                    )
    
    TEXT1 = TextTable( (250, 530) )
    
    TEXT2 = TextTable( (800, 530) )
    
    GAME = game(PLAYER_1, PLAYER_2, TABLE, NET, BALL, FLOOR, TEXT1, TEXT2)
    
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group(TABLE, NET, PLAYER_1, PLAYER_2, BALL, FLOOR)
    


    run = start_menu(WIN)
    
    while run:
        # speed control
        clock.tick(FPS)
        # looping through all of the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # player 1 position
        pos = pygame.mouse.get_pos()
        WHOS_POS = PLAYER_1
        WHOS_POS.rect.x = pos[0]
        WHOS_POS.rect.y = pos[1]
        
        # player1 rectangles position
        bullet = pygame.Surface((10, 10))
        bullet2 = pygame.Surface((10,10))
        bullet.fill((255, 0, 0))
        bullet2.fill((255, 0, 0))
        bullet_mask = pygame.mask.from_surface(bullet)
        bullet_mask = pygame.mask.from_surface(bullet2)

        
        
        # parse pressed keys 
        keys_pressed = pygame.key.get_pressed()
        GAME.handle_keys(keys_pressed)
        GAME.check_conditions()
        
        WIN.fill(BACKGROUND_COLOR)
        all_sprites.update()
        all_sprites.draw(WIN)
        # rect coordinates and rect borders.
        WIN.blit(bullet, pos)
        
        WIN.blit(bullet2, (TABLE.rect.x, TABLE.rect.y))
        
        # The scores
        WIN.blit(TEXT1.text, TEXT1.rect)
        WIN.blit(TEXT2.text, TEXT2.rect)
        
        # player 
        pygame.draw.rect(WIN, (255, 0, 0), PLAYER_1.rect, 1)
        
        # replace with update, as update updates only the changed components
        pygame.display.flip()
            

        #BALL.update()
        
        #draw_window(player1, player2, table, ball, draw_ball)

    pygame.quit()
    
if __name__ == "__main__":
    main()