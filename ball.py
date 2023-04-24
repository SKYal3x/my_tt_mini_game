#python 3.8
import pygame 
import os 

class AnimatedSprite(pygame.sprite.Sprite):
    ''' This is a basic class for our further classes
    '''
    def __init__(self,
                image_name,
                position:tuple([int,int]),
                size:tuple([int,int]),
                asset_folder = "Assets",
                image_folder = "img",
                ):
        super(AnimatedSprite, self).__init__()
        
        self.asset_folder = asset_folder
        self.image_folder = image_folder
        self.images = self.load_images(image_name)
        # transforming the images according to their size
        self.images = [pygame.transform.scale(image, size) 
                       for image in self.images]
        self.index = 0
        
        self.rect = pygame.Rect(position, size)
        self.velocity = pygame.math.Vector2(0,0)
        
        
    def load_images(self,
                     image_name,
                     asset_folder = None,
                     image_folder = None,
                     ):
        asset_folder = self.asset_folder
        image_folder = self.image_folder 
        images = list()
        for roots, dirs, files in os.walk(os.path.join(asset_folder, image_folder, image_name)):
            for img in files:
                images.append(pygame.image.load(os.path.join(asset_folder, image_folder, image_name, img)))
        return images 
        
    def update(self):
        ''' This is the API for the sprite group .updatate() method'''
        self.index += 0.1
        
        if self.index >= len(self.images):
            self.index = 0 
        self.image = self.images[int(self.index)]
        # updating inplace
        self.rect.move_ip(*self.velocity)
        
class BallSprite(AnimatedSprite):

    def __init__(self,
                image_name,
                position:tuple([int,int]),
                size:tuple([int,int])):
        super().__init__(image_name,
                         position,
                         size)
                         
        self.state = "ready_for_serve"
        self.check_state()
        
    def check_state(self):
        pass
        
    def handle_movement(self):
        pass
        
    def start_serve(self, player):
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.plain_serve()
        
    def plain_serve(self):
        self.velocity.y = -5

class Player1Sprite(AnimatedSprite):
    ''' No need for init, as we inhered the nneded stuff from the parent '''
    
    def handle_movement(self, keys_pressed, ball):
    
    # Rewrite the handler later, dont use hardcoded values!
        if keys_pressed[pygame.K_LEFT]:
            if self.rect.x < 0:
                self.velocity.x = 0
            else:
                self.rect.x += self.velocity.x
                self.velocity.x = -5
        if keys_pressed[pygame.K_RIGHT] and self.rect.x + self.velocity.x < 750:
            self.rect.x += self.velocity.x

        if keys_pressed[pygame.K_UP]:
            self.rect.y -= self.velocity.y

        if keys_pressed[pygame.K_DOWN]:
            self.rect.y += self.velocity.y
            
        if keys_pressed[pygame.K_SPACE]:
            ball.start_serve(self)
            
    
class Player2Sprite(AnimatedSprite):
    pass

class TableSprite(AnimatedSprite):
    pass

class game():
    def __init__(self, player1, player2, table, ball):
        self.player1 = player1
        self.player2 = player2
        self.table = table
        self.ball = ball 
        
    def check_conditions(self):
        responce_player1 = self.player1.rect.colliderect(self.ball.rect)
        responce_player2 = self.player2.rect.colliderect(self.ball.rect)
        if responce_player2:
            self.ball.velocity.y = -self.ball.velocity.y
        if responce_player1:
            self.ball.velocity.y = -self.ball.velocity.y 
        