#python 3.8
import pygame 

def collision_norm(mask:pygame.mask,
                   other:pygame.mask,
                   mask_rect_x:pygame.Rect.x,
                   mask_rect_y:pygame.Rect.y,
                   other_sprite_x:pygame.Rect.x,
                   other_sprite_y:pygame.Rect.y,
                   ) -> (int, int):
    """ https://www.pygame.org/docs/ref/mask.html#pygame.mask.Mask.overlap_area
    """
    dx = mask.overlap_area(other, (other_sprite_x - mask_rect_x + 1, other_sprite_y - mask_rect_y))\
       - mask.overlap_area(other, (other_sprite_x - mask_rect_x - 1, other_sprite_y - mask_rect_y))
    dy = mask.overlap_area(other, (other_sprite_x - mask_rect_x, other_sprite_y - mask_rect_y + 1))\
       - mask.overlap_area(other, (other_sprite_x - mask_rect_x, other_sprite_y - mask_rect_y - 1))
    result = (dx, dy)
    return result