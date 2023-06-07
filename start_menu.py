#python 3.8

import pygame
import button
#button class

        
def start_menu(WIN):  
    BACKGROUND_COLOR = (125, 195, 170)
    competetive_img = pygame.image.load('Assets/buttons/competetive.png').convert_alpha()
    arcade_img = pygame.image.load('Assets/buttons/arcade.png').convert_alpha()

    #create button instances
    competetive_button = button.Button(100, 200, competetive_img, 0.8)
    arcade_button = button.Button(600, 200, arcade_img, 0.8)
    
    pygame.mouse.set_visible(True)
    while True:
        
        WIN.fill(BACKGROUND_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_menu = False

        if arcade_button.draw(WIN):
            pygame.mouse.set_visible(False)
            return True
        if competetive_button.draw(WIN):
            return False
            
        pygame.display.update()
    