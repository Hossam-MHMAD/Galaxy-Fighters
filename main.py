import pygame
from Player import *

class Game:
  def __init__(self):
    # Set Window
    self.WIDTH = 1000
    self.HEIGHT = 600
    self.LINE_WIDTH = 10     # Middle Line Width
    self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
    pygame.display.set_caption("Galaxy Fighters")
    self.Clock = pygame.time.Clock()
    

    # Init Players
    self.Player_Width, self.Player_Height = 50, 50
    self.P1 = Player(10, self.HEIGHT / 2 - self.Player_Height / 2)
    self.P2 = Player(self.WIDTH - self.Player_Width - 10, self.HEIGHT / 2 - self.Player_Height / 2) # Init The Yellow Player Before the edge 10 pixels

    # Load Assets
    self.BG = pygame.transform.scale(pygame.image.load("Assets/space.png"), (self.WIDTH, self.HEIGHT))
    self.P1_IMAGE = pygame.transform.scale(pygame.image.load("Assets/spaceship_red.png"), (self.Player_Width, self.Player_Height))
    self.P2_IMAGE = pygame.transform.scale(pygame.image.load("Assets/spaceship_yellow.png"), (self.Player_Width, self.Player_Height))

    # Rotate Two Images 
    self.P1_IMAGE = pygame.transform.rotate(self.P1_IMAGE, 90)
    self.P2_IMAGE = pygame.transform.rotate(self.P2_IMAGE, -90)

  def Check_Close_Window(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return False
    return True

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

  def Render(self):
    self.WIN.blit(self.BG, (0, 0))  # Put The Background Image
    pygame.draw.line(self.WIN, "Black", (self.WIDTH/2-(self.LINE_WIDTH/2), 0), (self.WIDTH/2-(self.LINE_WIDTH/2), self.HEIGHT), self.LINE_WIDTH) # Draw The Middle Line

    # Render Players According To Them x and y
    self.WIN.blit(self.P1_IMAGE, (self.P1.x, self.P1.y))
    self.WIN.blit(self.P2_IMAGE, (self.P2.x, self.P2.y))

    pygame.display.update()

  def Update(self): # This Funtion Will Check For Events
    self.Check_Players_Movement() # For Better View :>


  def Run(self):
    while True:

      # Set FPS
      self.Clock.tick(60)

      # Check If User Want To Quit
      run = self.Check_Close_Window()
      if not run:
        break

      self.Update() # For Events 
      self.Render() 


    pygame.quit()


Game().Run()