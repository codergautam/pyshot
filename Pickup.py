class Pickup:
    """
  An object that you can... well... pick up.
  """

    def __init__(self, type_, pos, image, pickup):
        self.type = type_
        self.pos = pos
        self.image = image
        self.type = type_
        self.pickup = pickup
        self.visible = True
        self.rect = image.get_rect(center=pos)

    def update(self, window, player_rect, *args):
        if self.visible:
            if self.rect.colliderect(player_rect):
                self.visible = False
                self.pickup(*args)
            window.blit(self.image, self.rect)
