#python3.8
import pygame

class stack_of_three:
    """ This class holds represents
        a stack for two elements
    """
    def __init__(self):
        self.first = None
        self.middle = None
        self.last = None
        
    def update(self, element):
        self.first = self.middle
        self.middle = self.last
        self.last = element

def eval_score(ball, player1, player2):
    first = ball.CONTACTS.first
    middle = ball.CONTACTS.middle
    last = ball.CONTACTS.last
    
    if middle == last:
        player1.score = 0
    
    
    