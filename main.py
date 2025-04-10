import pygame
pygame.font.init()
pygame.mixer.init()
from Player import *

class Game:
  def __init__(self):
    # Set Window
    self.WIDTH = 1000
    self.HEIGHT = 600
    self.LINE_WIDTH = 10     # Middle Line Width
    self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
    pygame.display.set_caption("Galaxy Fighters")
    self.Clock = pygame.time.Clock() # For FPS




    # Bullet Speed
    self.BULLET_SPEED = 10

    # Set Fonts
    self.HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
    self.WINNER_FONT = pygame.font.SysFont('comicsans', 100)
    
    # Init Players
    self.Player_Width, self.Player_Height = 50, 50
    self.P1 = Player(10, self.HEIGHT / 2 - self.Player_Height / 2)
    self.P2 = Player(self.WIDTH - self.Player_Width - 10, self.HEIGHT / 2 - self.Player_Height / 2) # Init The Yellow Player Before the edge 10 pixels

    # Load Assets
    self.BG = pygame.transform.scale(pygame.image.load("Assets/space.png"), (self.WIDTH, self.HEIGHT))
    self.P1_IMAGE = pygame.transform.scale(pygame.image.load("Assets/spaceship_red.png"), (self.Player_Width, self.Player_Height))
    self.P2_IMAGE = pygame.transform.scale(pygame.image.load("Assets/spaceship_yellow.png"), (self.Player_Width, self.Player_Height))
    self.GUN_SOUND = pygame.mixer.Sound("Assets/Gun+Silencer.mp3")
    self.GRENADE = pygame.mixer.Sound("Assets/Grenade+1.mp3")

    # Rotate Two Images 
    self.P1_IMAGE = pygame.transform.rotate(self.P1_IMAGE, 90)
    self.P2_IMAGE = pygame.transform.rotate(self.P2_IMAGE, -90)

    self.Game_Over = False


  # ----------------------------------------------- Draw
  def Render(self):
    self.WIN.blit(self.BG, (0, 0))  # Put The Background Image
    pygame.draw.line(self.WIN, "Black", (self.WIDTH/2-(self.LINE_WIDTH/2), 0), (self.WIDTH/2-(self.LINE_WIDTH/2), self.HEIGHT), self.LINE_WIDTH) # Draw The Middle Line

    # Render Players Health
    P1_Health_Text = self.HEALTH_FONT.render(f"Health: {self.P1.health}", True, "white")
    P2_Health_Text = self.HEALTH_FONT.render(f"Health: {self.P2.health}", True, "white")
    self.WIN.blit(P1_Health_Text, (10, 5))
    self.WIN.blit(P2_Health_Text, (self.WIDTH - P2_Health_Text.get_width() - 10, 5))

    # Render Players According To Them x and y
    self.WIN.blit(self.P1_IMAGE, (self.P1.x, self.P1.y))
    self.WIN.blit(self.P2_IMAGE, (self.P2.x, self.P2.y))

    # Render P1 Bullets
    for bullet in self.P1.fire_list:
      pygame.draw.rect(self.WIN, "red", bullet)
    
    # Render P2 Bullets
    for bullet in self.P2.fire_list:
      pygame.draw.rect(self.WIN, "yellow", bullet)

    pygame.display.update()

  # ------------------------------------------------ Events And Updates
  def Check_Players_Movement(self):
    keys = pygame.key.get_pressed()

    # Check Player1 Movement
    if keys[pygame.K_w] and self.P1.y > self.P1.player_speed:
      self.P1.Move_Up()
    if keys[pygame.K_s] and self.P1.y < self.HEIGHT - self.P1.player_speed - self.Player_Height:
      self.P1.Move_Down()
    if keys[pygame.K_a] and self.P1.x > 0:
      self.P1.Move_Left()
    if keys[pygame.K_d] and self.P1.x < self.WIDTH / 2 - 10 - self.Player_Width: # 10 Is Extra Space
      self.P1.Move_Right()

    # Check Player2 Movement
    if keys[pygame.K_UP] and self.P2.y > self.P2.player_speed:
      self.P2.Move_Up()
    if keys[pygame.K_DOWN] and self.P2.y < self.HEIGHT - self.P2.player_speed - self.Player_Height:
      self.P2.Move_Down()
    if keys[pygame.K_LEFT] and self.P2.x > self.WIDTH / 2 + 5:
      self.P2.Move_Left()
    if keys[pygame.K_RIGHT] and self.P2.x < self.WIDTH - self.Player_Width:
      self.P2.Move_Right()

  def Check_Close_Window_And_Fire(self): # This Check IF Anybody shoot other player And If User Want to QUIT
    for event in pygame.event.get():

      if event.type == pygame.QUIT:
        return False

      if event.type == pygame.KEYDOWN:
        # IF players 1 clicked on L CTRL
        if event.key == pygame.K_LCTRL:
          P1_Bullet = pygame.Rect(self.P1.x + self.Player_Width, self.P1.y + self.Player_Height / 2, 10, 5)
          self.P1.fire_list.append(P1_Bullet)
          self.GUN_SOUND.play()

        # IF Player 2 Clicked on R Ctrl
        if event.key == pygame.K_RCTRL :
          P2_Bullet = pygame.Rect(self.P2.x, self.P2.y + self.Player_Height / 2, 10, 5)
          self.P2.fire_list.append(P2_Bullet)
          self.GUN_SOUND.play()


    return True

  def Check_Hit(self):
    # Check If P1 is Hitted
    for P2_Bullet in self.P2.fire_list:
      if P2_Bullet.x > self.P1.x and P2_Bullet.colliderect(pygame.Rect(self.P1.x, self.P1.y, self.Player_Width, self.Player_Height)):
        self.P2.fire_list.remove(P2_Bullet)
        self.P1.health -= 1
        self.GRENADE.play()

    for P1_Bullet in self.P1.fire_list:
      if P1_Bullet.x > self.P2.x and P1_Bullet.colliderect(pygame.Rect(self.P2.x, self.P2.y, self.Player_Width, self.Player_Height)):
        self.P1.fire_list.remove(P1_Bullet)
        self.P2.health -= 1
        self.GRENADE.play()

  def Check_Winner(self):
    if self.P1.health == 0:
      Yellow_Win_Text = self.WINNER_FONT.render("Yellow Win", True, "white")
      self.WIN.blit(Yellow_Win_Text, (self.WIDTH / 2 - Yellow_Win_Text.get_width() / 2, self.HEIGHT / 2 - Yellow_Win_Text.get_height() / 2))
      pygame.display.update()
      pygame.time.delay(3000)
      return True
    
    elif self.P2.health == 0:
      Red_Win_Text = self.WINNER_FONT.render("Red Win", True, "white")
      self.WIN.blit(Red_Win_Text, (self.WIDTH / 2 - Red_Win_Text.get_width() / 2, self.HEIGHT / 2 - Red_Win_Text.get_height() / 2))
      pygame.display.update()
      pygame.time.delay(3000)
      return True
    
    else:
      return False
    
  def Update(self): # This Funtion Will Check For Events
    self.Check_Players_Movement() # For Better View :>

    # Move Each Player Bullet
    self.P1.Move_Bullets(self.BULLET_SPEED, self.WIDTH) # 1 to move bullet right 
    self.P2.Move_Bullets(-self.BULLET_SPEED, self.WIDTH) # -1 to move bullet left

    # Check If Any Player Has Hitted
    self.Check_Hit()

    if self.Check_Winner():
      self.Game_Over = True

  # ------------------------------------------------ Run The Game

  def Run(self):
    while True:

      # Set FPS
      self.Clock.tick(60)

      # Check If User Want To Quit ANd it Will Check If Any Player Hass SHoot if yes it will add a regtangle object (bullet) to its fire_List
      run = self.Check_Close_Window_And_Fire()
      if not run:
        break

      self.Update() # For Events 
      self.Render() 

      if self.Game_Over:
        break

    pygame.quit()


Game().Run()
