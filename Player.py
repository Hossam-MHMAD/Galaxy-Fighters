class Player:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.player_speed = 5
    self.health = 10
    self.fire_list = []

  def Move_Right(self):
    self.x += self.player_speed

  def Move_Left(self):
    self.x -= self.player_speed
  
  def Move_Up(self):
    self.y -= self.player_speed

  def Move_Down(self):
    self.y += self.player_speed
  
  def Take_Damage(self):
    self.health -= 1

  # Bullet_Direction Here Is To determine which player has shoot if left player 1 or -1 if right player, 
  # and Screen_Width is to check if the bullet get out of the screen
  # and i used the Bullet_Direction To To Determine Which Player i will remove its bullet if it gets out of the screen
  def Move_Bullets(self, Bullet_Direction, Screen_Width): 
    for bullet in self.fire_list:
      bullet.x += Bullet_Direction

      if Bullet_Direction > 0: # For Left Player Bullets
        if bullet.x > Screen_Width:
          self.fire_list.remove(bullet)
      
      else: # For Right Player Bullets
        if bullet.x < 0:
          self.fire_list.remove(bullet)
