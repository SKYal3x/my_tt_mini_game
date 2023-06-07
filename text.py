#python 3.8
import pygame 

class TextTable():
    def __init__(self, 
                 position:tuple([int,int])):
        
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)

        self.font = pygame.font.Font('freesansbold.ttf', 32)
        
        self.text_to_display = "0"
        self.text = self.font.render(f'Points: {self.text_to_display} ',
                    True, self.green, self.blue) # font color, box color

        self.rect = self.text.get_rect()
        self.rect.topleft = position
   
   
    def update_text_to_display(self, text):
        self.text = self.font.render(f'Points: {text} ',
                    True, self.green, self.blue) # font color, box color    
        
    def update(self):
        ''' This is the API for the sprite group .updatate() method'''
        
        # Deal with the animation later
        # self.index += 0.1
        
        # if self.index >= len(self.images):
            # self.index = 0 
        # self.image = self.images[int(self.index)]
        # updating inplace
        # can't work with velocity now, as we need to avoid the collision
        # self.rect.move_ip(*self.velocity)
        text = font.render(f'Points: {self.text_to_display}', true, green, blue)