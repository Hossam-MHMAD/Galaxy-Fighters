class Player:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.player_speed = 5

  def Move_Right(self):
    self.x += self.player_speed

  def Move_Left(self):
    self.x -= self.player_speed
  
  def Move_Up(self):
    self.y -= self.player_speed

  def Move_Down(self):
    self.y += self.player_speed
