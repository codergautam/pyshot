import pygame

class Pickup:
  """
  An object that you can... well... pick up.
  """
  def __init__(self, type, pos, image, pickup):
    self.type = type
    self.pos = pos
    self.image = image
    self.type = type
    self.onpickup = pickup
    self.visible = True
    self.rect = image.get_rect(center=pos)
  
  def update(self, window, prect, *args):
    if(self.visible):
      if(self.rect.colliderect(prect)):
        self.visible = False
        self.onpickup(*args)
      window.blit(self.image, self.rect)
