#python 3.8
import pygame 
import os 
import random 

from physics import collision_norm
from rules_scores import stack_of_three, eval_score

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
        self.images = [pygame.transform.scale(image, size).convert_alpha()
                       for image in self.images]
        self.index = 0
        self.image = self.images[int(self.index)]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = position
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
        
        # Deal with the animation later
        # self.index += 0.1
        
        # if self.index >= len(self.images):
            # self.index = 0 
        # self.image = self.images[int(self.index)]
        # updating inplace
        # can't work with velocity now, as we need to avoid the collision
        # self.rect.move_ip(*self.velocity)
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        
class BallSprite(AnimatedSprite):
    
    # classvariable to determine contacts
    # and thus calculate the points
    CONTACTS = stack_of_three() 
    
    def __init__(self,
                image_name,
                position:tuple([int,int]),
                size:tuple([int,int])):
        super().__init__(image_name,
                         position,
                         size)
                         
        # not needed yet
        self._check_state = True
        
        # rect offset in px
        self.offset = size[1]
        
        # might be some contradictions later, maybe redefine it somewhere else
        self.gravity = 1
        self.velocity.y = 1
        
        # count the time of the ball between
        # in the air to simulate the spin behavior.
        self.fly_counter = 0
        
        self.TopSpin = False
        self.BackSpin = False
        self.NoSpin = True
    
    def player_contact(self):
        self.fly_counter = 0
        if  self.BackSpin:
            self.velocity.x = 15
            self.gravity = 0
            self.velocity.y = -5
            
        elif self.TopSpin:
            self.velocity.x = 30
            self.velocity.y = -15
            self.gravity = 0
        else:
            self.velocity.x = 21
            self.gravity = 1
            self.velocity.y = -11
    
    def oponent_contact(self):
            self.fly_counter = 0
            self.velocity.x = random.randint(-17,-15)
            self.velocity.y = random.randint(-14,-12)
            self.gravity = 1
            self.TopSpin = False
            self.BackSpin = False
            print(self.velocity.x, self.velocity.y)
            
    def table_contact(self, old_velocity):
        self.velocity.y = -old_velocity + self.gravity
    
    def check_state(self):
        """function for gravity changes
        in order to mimic the spin behavior
        """
        # how many frames is the ball flying
        self.fly_counter += 1
        
        if self.TopSpin:
            if self.fly_counter >= 10:
                self.gravity = 10
                
        if self.BackSpin:
            if self.fly_counter >= 10:
                self.gravity = 2
        
        self.velocity.y += self.gravity
 


class Player1Sprite(AnimatedSprite):

    def __init__(self,
                image_name,
                position:tuple([int,int]),
                size:tuple([int,int])):
        """ the only reason for overwriting 
            the parents init method is to add
            own attributes to the constructor
        """
        super().__init__(image_name,
                         position,
                         size)
        self.score = 0
        # add attributes later
    def handle_movement(self, keys_pressed):
    
    # Rewrite the handler later, dont use hardcoded values!


        if keys_pressed[pygame.K_UP]:
            self.image = pygame.transform.rotate(self.image, 90) 
            self.rect = self.image.get_rect()

        if keys_pressed[pygame.K_DOWN]:
            self.image = pygame.transform.rotate(self.image, -90)
            self.rect = self.image.get_rect()
    
    def ball_contact(self):
        BallSprite.CONTACTS.update(self)
            
class Player2Sprite(Player1Sprite):
    """ Same as player1, but we 
        erase the handle_movement method
        as the players2 movement would be handled by the pc
    """
    def handle_movement(self):
        pass
        
class TableSprite(AnimatedSprite):
    """ overriding the update method, because the table is not animated
    """
    def update(self):
        pass
    
    def ball_contact(self):
        BallSprite.CONTACTS.update(self)
        
class NetSprite(AnimatedSprite):
    pass
    
class FloorSprite(AnimatedSprite):
    
    def ball_contact(self):
        BallSprite.CONTACTS.update(self)
    
class game():
    def __init__(self, player1, player2, table, net, ball, floor, text1, text2):
    
        ### test ###
        self.crash_sound = pygame.mixer.Sound("Assets/sound/Stalin.wav")
        ############
        self.player1 = player1
        self.player2 = player2
        self.table = table
        self.net = net
        self.ball = ball 
        self.floor = floor
        self.text1 = text1
        self.text2 = text2
        
        self.ball_mask = pygame.mask.from_surface(self.ball.image)
        self.table_mask = pygame.mask.from_surface(self.table.image)
        self.net_mask = pygame.mask.from_surface(self.net.image)
        self.floor_mask = pygame.mask.from_surface(self.floor.image)
        self.player1_mask = pygame.mask.from_surface(self.player1.image)
        
        
        #some statics for tests REMOVE LATER
        self.TEST_PLAYER2_VELOCITY = -21
        
    def handle_keys(self, keys_pressed):
        """placing the ball on its spot"""
        if keys_pressed[pygame.K_SPACE]:
            self.player2.rect.y = 400
            self.ball.rect.topleft = (self.player2.rect.x, 50)
            self.ball.velocity.x = 0
            self.ball.velocity.y = 1
            self.ball.gravity = 1
        if keys_pressed[pygame.K_t]:
            self.ball.TopSpin = True
            self.ball.BackSpin = False
        elif keys_pressed[pygame.K_b]: 
            self.ball.TopSpin = False
            self.ball.BackSpin = True

             
    def check_conditions(self):
        
        """
        The opponents AI part :-D 
        """
        if self.ball.rect.x > 572:
            # the desired position
            self.des_pos = self.ball.rect.y -10
           
            if self.player2.rect.y > self.des_pos:
                self.player2.rect.y -= 5
            elif self.player2.rect.y < self.des_pos:
                self.player2.rect.y += 5
        
        """
        End of the AI part :-D
        """
        
        ball_table_collision = pygame.sprite.spritecollide(
                                    self.ball,
                                    [self.table],
                                    False,    # dokill argument defines if the sprite would be deleted afterwards
                                    pygame.sprite.collide_mask # using mask collision
                                    )
        # overlap method takes two args, 1st - the mask to detect the collision with
        #2nd- the offset, it should determine the distance between the top lefts of 
        # the two masks
        ball_table_overlap = self.ball_mask.overlap_area(
                                    self.table_mask,
                                    (self.table.rect.x-self.ball.rect.x, 
                                     self.table.rect.y-self.ball.rect.y-1)
                                    )
        
        ball_net_overlap = self.ball_mask.overlap_area(
                                    self.net_mask,
                                    (self.net.rect.x-self.ball.rect.x, 
                                     self.net.rect.y-self.ball.rect.y-1)
                                    )
        
        ball_floor_overlap = self.ball_mask.overlap_area(
                                    self.floor_mask,
                                    (self.floor.rect.x-self.ball.rect.x, 
                                     self.floor.rect.y-self.ball.rect.y-1)
                                    )
        #print(self.ball.rect.topleft)
        # save this one for later
        # ball_player1_collision = pygame.sprite.spritecollide(
                                    # self.ball,
                                    # [self.player1],
                                    # False,    # dokill argument defines if the sprite would be deleted afterwards
                                    # pygame.sprite.collide_mask # using mask collision
                                    # )
        ball_player1_collision = self.player1.rect.colliderect(self.ball.rect)
        ball_player2_collision = self.player2.rect.colliderect(self.ball.rect)    
        

        if ball_table_overlap:
        
            self.ball.table_contact(self.old_velocity)
            
            # self.player1.score = 0 if                     \
            # (BallSprite.CONTACTS.first == self.table) &   \
            # (BallSprite.CONTACTS.last == self.table)      \
            # else self.player1.score
            eval_score(self.ball, self.player1, self.player2)
            
            #extra function for this later
            self.text1.update_text_to_display(self.player1.score)
            self.text2.update_text_to_display(self.player2.score)
            
            self.table.ball_contact()

        if ball_net_overlap:
            """ calculating the colision normal for the ball and the net
            """
            dx, dy = collision_norm(self.ball_mask, 
                                    self.net_mask, 
                                    self.ball.rect.x,
                                    self.ball.rect.y-1,
                                    self.net.rect.x,
                                    self.net.rect.y)
            
            # dx = self.ball_mask.overlap_area(self.net_mask, (self.net.rect.x-self.ball.rect.x + 1, self.net.rect.y-self.ball.rect.y-1)) \
                # - self.ball_mask.overlap_area(self.net_mask, (self.net.rect.x-self.ball.rect.x - 1, self.net.rect.y-self.ball.rect.y-1))
            # dy = self.ball_mask.overlap_area(self.net_mask, (self.net.rect.x-self.ball.rect.x, self.net.rect.y-self.ball.rect.y-1 + 1)) \
                # - self.ball_mask.overlap_area(self.net_mask, (self.net.rect.x-self.ball.rect.x, self.net.rect.y-self.ball.rect.y-1 - 1))
            
            # print(dx, dy)
            """ End of calculation
            """

            self.ball.velocity.x = dx
            self.ball.velocity.y = dy
            
        if ball_floor_overlap:
            dx, dy = collision_norm(self.ball_mask, 
                                    self.floor_mask, 
                                    self.ball.rect.x,
                                    self.ball.rect.y-1,
                                    self.floor.rect.x,
                                    self.floor.rect.y)
            
            # dx = self.ball_mask.overlap_area(self.net_mask, (self.net.rect.x-self.ball.rect.x + 1, self.net.rect.y-self.ball.rect.y-1)) \
                # - self.ball_mask.overlap_area(self.net_mask, (self.net.rect.x-self.ball.rect.x - 1, self.net.rect.y-self.ball.rect.y-1))
            # dy = self.ball_mask.overlap_area(self.net_mask, (self.net.rect.x-self.ball.rect.x, self.net.rect.y-self.ball.rect.y-1 + 1)) \
                # - self.ball_mask.overlap_area(self.net_mask, (self.net.rect.x-self.ball.rect.x, self.net.rect.y-self.ball.rect.y-1 - 1))
            
            # print(dx, dy)
            """ End of calculation
            """

            self.ball.velocity.x = dx
            self.ball.velocity.y = dy   
            
            # separete into distinct funciton later
            self.player1.score = 0
            self.text1.update_text_to_display(self.player1.score)

            
        if self.ball.rect.y + self.ball.velocity.y > self.table.rect.y - self.ball.offset\
        and  self.ball.rect.x > self.table.rect.left       \
        and  self.ball.rect.x < self.table.rect.right:
            self.old_velocity = self.ball.velocity.y
            self.new_velocity = self.table.rect.y - self.ball.offset - self.ball.rect.y - self.ball.gravity
            #print("velocity correction: ", self.old_velocity, self.new_velocity)
            self.ball.velocity.y = self.new_velocity

            # # #if self.ball.rect.y > ball_table_overlap[1]:
            # # # if ball_table_overlap>105:
                # # # self.ball.rect.y = ball_table_overlap[1]
                # # # #self.ball.velocity.y = - self.ball.velocity.y + 1
                # # # self.ball._check_state = False
        if ball_player1_collision:
            
            self.ball.player_contact()
            

            # score setting into seperate function
            self.player1.score = self.player1.score + 1 if BallSprite.CONTACTS.last == self.table else 0
            self.text1.update_text_to_display(self.player1.score)
            pygame.mixer.Sound.play(self.crash_sound)
            
            self.player1.ball_contact()
        
        if ball_player2_collision:
            
            self.ball.oponent_contact()
            self.player2.ball_contact()
            
            # if not self.score_player1 % 5:
               # self.TEST_PLAYER2_VELOCITY -= 1  
        self.ball.check_state()
   
        