import pygame, os, sys, math, random

WIN_W = 1280
WIN_H = 720

WHITE = (255, 255, 255)
LIGHT_GREY = (150, 150, 150)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

fps = 60


class Ship_Type(pygame.sprite.Sprite):
   def __init__(self, speed, width, height, firerate, bullet_type):
       pygame.sprite.Sprite.__init__(self)
       self.speed = speed
       self.width = width
       self.height = height
       self.firerate = firerate
       self.bullet_type = bullet_type

class Bullet_Type(pygame.sprite.Sprite):
   def __init__(self, speed, width, height):
       pygame.sprite.Sprite.__init__(self)
       self.speed = speed
       self.width = width
       self.height = height

class Enemy_Type(pygame.sprite.Sprite):
   def __init__(self, speed, width, height, enemy_attack, behavior):
       pygame.sprite.Sprite.__init__(self)
       self.speed = speed
       self.width = width
       self.height = height
       self.attack = enemy_attack
       self.behavior = behavior
       #"strafe_._": move to target y amd shoot at player while moving to random target coords within radius
       #"snipe_;_": strafe within radius of target y
       #"dive_": move at a steep angle down the screen, attack, and fly off
       #"bomb_": move to bottom of screen to shoot, then move back up

class Enemy_Attack(pygame.sprite.Sprite):
   def __init__(self, bullet_type, volley, firerate, cooldown, spread, random_spread, aim_shot, type, shots):
       pygame.sprite.Sprite.__init__(self)
       self.bullet = bullet_type
       self.volley = volley
       self.firerate = firerate
       self.cooldown = cooldown
       self.spread = spread
       self.random_spread = random_spread
       self.aim_shot = aim_shot #True = aims every shot number = turns n degrees speed in between shooting
       self.type = type
       self.shots = shots
       #"regular" = regular
       #"shotgun_" = shotgun _ shells, must add extra _ at end, spread = total angle of spread shot
       #"spiral" = shoots in circle around self, turns spread degrees, spread = angular dist between shots
       #"laser" = draws line to deal dmg, spread = width of beam
       #"sides_" = shoots pairs of shots from either side, angle intervals of spread away from front


class Enemy_Bullet_Type(pygame.sprite.Sprite):
   def __init__(self, speed, width, height, accel, homing, delay, spread):
       pygame.sprite.Sprite.__init__(self)
       self.speed = speed
       self.width = width
       self.height = height
       self.accel = accel
       self.homing_speed = homing
       self.delay = delay
       self.spread = spread

bullet_type = Bullet_Type(15, 5, 5)
ship_type = Ship_Type(5, WIN_W/25, WIN_H/24, 5, bullet_type)
enemy_bullet_regular = Enemy_Bullet_Type(10, 5, 5, False, 0, 0, 0)
enemy_attack_regular = Enemy_Attack(enemy_bullet_regular, 3, 5, 15, 0, 0, True, "regular", 1)
enemy_type_regular = Enemy_Type(0.1, WIN_W/25, WIN_H/24, enemy_attack_regular, "snipe" + str(WIN_H//4) + ";100_")

enemy_bullet_slow = Enemy_Bullet_Type(5, 5, 5, False, 0, 0, 0)
enemy_attack_shotgun = Enemy_Attack(enemy_bullet_slow, 8, 10, 15, 30, 30, True, "shotgun2_", 1)
enemy_type_shotgun = Enemy_Type(0.25, WIN_W/25, WIN_H/24, enemy_attack_shotgun, "diveplayer200_")

enemy_attack_spiral = Enemy_Attack(enemy_bullet_regular, 30, 60, 20, 24, 0, False, "spiral", 1)
enemy_type_spiral = Enemy_Type(0.3, WIN_W/25, WIN_H/24, enemy_attack_spiral, "bomb" + str(WIN_H//4) + ";100_")

enemy_bullet_rocket = Enemy_Bullet_Type(0.3, 5, 5, "8;5_", 1, "150;60_", 5)
enemy_attack_rocket = Enemy_Attack(enemy_bullet_rocket, 15, 60, 30, 90, 30, True, "sides2_", 2)
enemy_type_rocket = Enemy_Type(0.1, WIN_W/25, WIN_H/24, enemy_attack_rocket, "snipe" + str(WIN_H//4) + ";100_")

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Force static position of screen

class Button(pygame.sprite.Sprite):
   def __init__(self, centerx, centery, width, height):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface((width, height))
       self.rect = self.image.get_rect()
       self.rect.centerx = centerx
       self.rect.centery = centery
       self.image.fill(GREEN)
       self.clicked = False
       self.activate = False

   def update(self):
       if self.rect.collidepoint(pygame.mouse.get_pos()):
           self.image.fill(BLUE)
           if self.clicked == False and pygame.mouse.get_pressed()[0] == True:
               self.clicked = True
           if self.clicked and pygame.mouse.get_pressed()[0] == False:
               self.clicked = False
               self.activate = True
       else:
           self.image.fill(GREEN)

class Ship(pygame.sprite.Sprite):
   def __init__(self, ship_type, startx, starty):
       pygame.sprite.Sprite.__init__(self)
       self.speed = ship_type.speed
       self.width = ship_type.width
       self.height = ship_type.height
       self.image = pygame.Surface((self.width, self.height))
       self.rect = self.image.get_rect()
       self.rect.centerx = startx
       self.rect.centery = starty
       self.image.fill(GREEN)
       self.firerate = ship_type.firerate
       self.fireclock = 0
       self.bullet_type = ship_type.bullet_type
       self.alive = True

   def update(self, bullet_group, enemy_bullet_group, game):
       key = pygame.key.get_pressed()

       if key[pygame.K_w] or key[pygame.K_UP]:
           self.rect.y -= self.speed
           if self.rect.top < 0:
               self.rect.top = 0
       if key[pygame.K_s] or key[pygame.K_DOWN]:
           self.rect.y += self.speed
           if self.rect.bottom > WIN_H:
               self.rect.bottom = WIN_H
       if key[pygame.K_a] or key[pygame.K_LEFT]:
           self.rect.x -= self.speed
           if self.rect.left < 0:
               self.rect.left = 0
       if key[pygame.K_d] or key[pygame.K_RIGHT]:
           self.rect.x += self.speed
           if self.rect.right > WIN_W:
               self.rect.right = WIN_W

       if key[pygame.K_SPACE] and self.fireclock == 0:
           b = Bullet(self, self.bullet_type, math.pi/2)
           bullet_group.add(b)
           self.fireclock = self.firerate // fps

       e_bullets_list = pygame.sprite.spritecollide(self, enemy_bullet_group, True)
       for e in e_bullets_list:
           self.alive = False


class Bullet(pygame.sprite.Sprite):
   def __init__(self, ship, bullet_type, direction):
       pygame.sprite.Sprite.__init__(self)
       self.width = bullet_type.width
       self.height = bullet_type.height
       self.speed = bullet_type.speed
       self.image = pygame.image.load('images/enemy_bullet.png')
       self.image.fill(BLUE)
       self.rect = self.image.get_rect()
       self.rect.center = ship.rect.center
       self.direction = direction
       self.xvel = math.cos(direction) * self.speed
       self.yvel = math.sin(direction) * self.speed

   def update(self):
       self.rect.x += self.xvel
       self.rect.y -= self.yvel
       if self.rect.x < 0 or self.rect.x > WIN_W or self.rect.y < 0 or self.rect.y > WIN_H:
           self.kill()

class Enemy(pygame.sprite.Sprite):
   def __init__(self, enemy_type, startpos, target, hp, dog):
       pygame.sprite.Sprite.__init__(self)
       self.type = enemy_type
       font = pygame.font.Font("fonts/fourside.ttf", 70)
       if not dog:
           self.image = font.render("!", 1, WHITE)
       else:
           self.image = font.render("!", 1, RED)
       self.rect = self.image.get_rect()
       self.rect.x = startpos[0]
       self.rect.y = startpos[1]
       self.fireclock = 0
       self.volley = 0
       self.direction = 0
       self.target = target
       self.alive = True
       self.hp = hp
       if "strafe" in self.type.behavior:
           self.targety = float(self.type.behavior[6:self.type.behavior.find(";")])
           self.strafe_radius = float(self.type.behavior[self.type.behavior.find(";") + 1: -1])
           self.targetx = self.rect.x
       elif "snipe" in self.type.behavior:
           self.targety = float(self.type.behavior[5:self.type.behavior.find(";")])
           self.basey = self.targety
           self.strafe_radius = float(self.type.behavior[self.type.behavior.find(";") + 1: -1])
           self.targetx = self.rect.x

       elif "dive" in self.type.behavior:
           self.targety = WIN_H + self.type.speed*100
           if "player" in self.type.behavior:
               if random.randrange(2) == 1:
                   self.targetx = target.rect.x + random.randrange(int(self.type.behavior[10:-1])//2, int(self.type.behavior[10:-1]) + 1)
               else:
                   self.targetx = target.rect.x - random.randrange(int(self.type.behavior[10:-1])//2, int(self.type.behavior[10:-1]) + 1)

           else:
               self.targetx = self.rect.x + random.randrange(-int(self.type.behavior[4:-1]), int(self.type.behavior[4:-1]) + 1)
       elif "bomb" in self.type.behavior:
           self.targety = float(self.type.behavior[4:self.type.behavior.find(";")])
           self.basey = self.targety
           self.targetx = self.rect.x
           self.strafe_radius = float(self.type.behavior[self.type.behavior.find(";") + 1: -1])

       self.x = self.rect.x
       self.y = self.rect.y
       self.xvel = 0
       self.yvel = 0
       self.cooldown = 30


   def update(self, enemy_bullet_group, target, screen, bullet_group):
       if self.cooldown == 0:
           self.image = pygame.image.load('images/enemy.png')
           for b in bullet_group:
               if math.sqrt((b.rect.x - self.rect.x) ** 2 + (b.rect.y - self.rect.y) ** 2) <= 40:
                   if type(b) == type(Bullet):
                       b.kill()
                   else:
                       b.hit = True
                   self.alive = False
           if self.fireclock == 0:
               if self.volley == 0:
                   self.volley = self.type.attack.volley
                   self.fireclock = self.type.attack.cooldown
               else:
                   if self.type.attack.aim_shot == True and type(self.type.attack.aim_shot) != int or self.volley == self.type.attack.volley:
                       self.direction = math.atan2(self.rect.centery - target.rect.centery, target.rect.centerx - self.rect.centerx)
                   if self.volley == self.type.attack.volley:
                       self.fireclock = 60 // self.type.attack.firerate
                   if self.type.attack.aim_shot >= 1:
                       player_direction = math.atan2(self.rect.centery - target.rect.centery, target.rect.centerx - self.rect.centerx)
                       if self.direction + math.radians(self.type.attack.aim_shot)/60 > player_direction and self.direction - math.radians(self.type.attack.aim_shot)/60 < player_direction:
                           self.direction = player_direction
                       else:
                           if self.direction >= 0:
                               if player_direction > self.direction or player_direction < self.direction - math.pi:
                                   self.direction += math.radians(self.type.attack.aim_shot)/60
                               else:
                                   self.direction -= math.radians(self.type.attack.aim_shot)/60
                           else:
                               if player_direction > self.direction and player_direction < self.direction + math.pi:
                                   self.direction += math.radians(self.type.attack.aim_shot)/60
                               else:
                                   self.direction -= math.radians(self.type.attack.aim_shot)/60
                   self.volley -= 1
                   if self.type.attack.type != "laser":
                       for a in range(self.type.attack.shots):
                           self.fireclock = 60 // self.type.attack.firerate
                           if "shotgun" in self.type.attack.type:
                               for a in range(int(self.type.attack.type[7:-1])):
                                   e = Enemy_Bullet(self, self.type.attack.bullet, self.direction + math.radians(-self.type.attack.spread/2 + self.type.attack.spread * a/(int(self.type.attack.type[7:-1])-1)) + math.radians(random.randrange(-self.type.attack.random_spread, self.type.attack.random_spread + 1)))
                                   enemy_bullet_group.add(e)
                           elif "sides" in self.type.attack.type:
                               if int(self.type.attack.type[5:-1]) % 2 == 0:
                                   for a in range(int(self.type.attack.type[5:-1])//2):
                                       e = Enemy_Bullet(self, self.type.attack.bullet, self.direction - math.radians(self.type.attack.spread*(a + 1)) + math.radians(random.randrange(-self.type.attack.random_spread, self.type.attack.random_spread + 1)))
                                       enemy_bullet_group.add(e)
                                       e = Enemy_Bullet(self, self.type.attack.bullet, self.direction + math.radians(self.type.attack.spread*(a + 1)) + math.radians(random.randrange(-self.type.attack.random_spread, self.type.attack.random_spread + 1)))
                                       enemy_bullet_group.add(e)
                               else:
                                   e = Enemy_Bullet(self, self.type.attack.bullet, self.direction + math.radians(random.randrange(-self.type.attack.random_spread, self.type.attack.random_spread + 1)))
                                   enemy_bullet_group.add(e)
                                   for a in range(int(self.type.attack.type[5:-1])//2 - 1):
                                       e = Enemy_Bullet(self, self.type.attack.bullet, self.direction - math.radians(self.type.attack.spread*(a + 1)) + math.radians(random.randrange(-self.type.attack.random_spread, self.type.attack.random_spread + 1)))
                                       enemy_bullet_group.add(e)
                                       e = Enemy_Bullet(self, self.type.attack.bullet, self.direction + math.radians(self.type.attack.spread*(a + 1)) + math.radians(random.randrange(-self.type.attack.random_spread, self.type.attack.random_spread + 1)))
                                       enemy_bullet_group.add(e)

                           else:
                               e = Enemy_Bullet(self, self.type.attack.bullet, self.direction + math.radians(random.randrange(-self.type.attack.random_spread, self.type.attack.random_spread + 1)))
                               enemy_bullet_group.add(e)
                           if self.type.attack.type == "spiral":
                               self.direction += math.radians(self.type.attack.spread)
                   elif self.fireclock == 0:
                       pygame.draw.line(screen, RED, (self.rect.center), (self.rect.centerx + math.cos(self.direction)*1000, self.rect.centery - math.sin(self.direction)*1000), self.type.attack.spread)
                       if self.direction - math.pi > player_direction:
                           angle_diff = math.fabs(self.direction - (player_direction + 2*math.pi))
                       elif player_direction - math.pi > self.direction:
                           angle_diff = math.fabs(player_direction - (self.direction + 2*math.pi))
                       else:
                           angle_diff = math.fabs(self.direction - player_direction)
                       x = target.rect.width
                       y = target.rect.height
                       if math.sin(math.fabs(angle_diff)) * math.hypot(self.rect.centerx - target.rect.centerx, self.rect.centery - target.rect.centery) < self.type.attack.spread/2 + (x + y)/(4*(math.cos(angle_diff) + math.tan(angle_diff)*math.sin(angle_diff))):
                           target.image.fill(BLUE)
                       else:
                           target.image.fill(GREEN)

           else:
               if self.fireclock <= 1:
                   self.fireclock = 0
               else:
                   self.fireclock -= 1

           if math.hypot(self.targetx - self.rect.x, self.targety - self.rect.y) > self.type.speed * 20:

               if (self.rect.right < 0 or self.rect.left > WIN_W) and (self.rect.top > WIN_H or self.rect.bottom < 0):
                   self.kill()

               if math.fabs(self.rect.x - self.targetx) > self.type.speed*100:
                   self.xvel += self.type.speed * (self.targetx - self.rect.x)/math.hypot(self.targetx - self.rect.x, self.targety - self.rect.y)

               elif math.fabs(self.xvel) > math.fabs(self.type.speed*10):
                   if self.xvel < 0:
                       self.xvel += self.type.speed
                   else:
                       self.xvel -= self.type.speed

               else:
                   self.xvel += self.type.speed * ((self.targetx - self.rect.x)/math.hypot(self.targetx - self.rect.x, self.targety - self.rect.y)) / 3

               if math.fabs(self.rect.y - self.targety) > self.type.speed*100:
                   self.yvel -= self.type.speed * (self.targety - self.rect.y)/math.hypot(self.targetx - self.rect.x, self.targety - self.rect.y)

               elif math.fabs(self.yvel) > math.fabs(self.type.speed*10):
                   if self.yvel < 0:
                       self.yvel += self.type.speed
                   else:
                       self.yvel -= self.type.speed

               else:
                   self.yvel -= self.type.speed * ((self.targety - self.rect.y)/math.hypot(self.targetx - self.rect.x, self.targety - self.rect.y)) / 3
           else:
               if "strafe" in self.type.behavior:
                   while math.hypot(self.targetx - self.rect.x, self.targety - self.rect.y) > self.strafe_radius or math.hypot(self.targetx - self.rect.x, self.targety - self.rect.y) < self.strafe_radius/2 or self.targetx < self.type.speed*100 or self.targetx > WIN_W - self.type.speed*100 or self.targety < self.type.speed*100 or self.targety > WIN_H - self.type.speed*100:
                       self.targetx = random.randrange(self.rect.x - self.strafe_radius,self.rect.x + self.strafe_radius + 1)
                       self.targety = random.randrange(self.rect.y - self.strafe_radius,self.rect.y + self.strafe_radius + 1)
               elif "snipe" in self.type.behavior:
                   while math.hypot(self.targetx - self.rect.x, self.targety - self.rect.y) > self.strafe_radius or math.hypot(self.targetx - self.rect.x, self.targety - self.rect.y) < self.strafe_radius/2 or self.targetx < self.type.speed*100 or self.targetx > WIN_W - self.type.speed*100 or self.targety < self.type.speed*100 or self.targety > WIN_H - self.type.speed*100 or self.targety < self.basey - self.strafe_radius or self.targety > self.basey + self.strafe_radius:
                       self.targetx = random.randrange(self.rect.x - self.strafe_radius,self.rect.x + self.strafe_radius + 1)
                       self.targety = random.randrange(self.rect.y - self.strafe_radius,self.rect.y + self.strafe_radius + 1)
               elif "bomb" in self.type.behavior:
                   if self.fireclock < 120:
                       while math.hypot(self.targetx - target.rect.x, self.targety - (target.rect.y - self.strafe_radius/2)) > self.strafe_radius * 2 or math.hypot(self.targetx - target.rect.x, self.targety - (target.rect.y - self.strafe_radius/2)) < self.strafe_radius or self.targetx < self.type.speed * 100 or self.targetx > WIN_W - self.type.speed * 100 or self.targety < self.type.speed * 100 or self.targety > WIN_H - self.type.speed * 100:
                           self.targetx = random.randrange(target.rect.x - self.strafe_radius, target.rect.x + self.strafe_radius + 1)
                           self.targety = random.randrange((target.rect.y - self.strafe_radius/2) - self.strafe_radius, (target.rect.y - self.strafe_radius/2) + self.strafe_radius + 1)
                   elif self.rect.y > self.basey - self.strafe_radius*2:
                       while math.hypot(self.targetx - self.rect.x, self.targety - self.basey) > self.strafe_radius or math.hypot(self.targetx - self.rect.x, self.targety - self.basey) < self.strafe_radius / 2 or self.targetx < self.type.speed * 100 or self.targetx > WIN_W - self.type.speed * 100 or self.targety < self.type.speed * 100 or self.targety > WIN_H - self.type.speed * 100:
                           self.targetx = random.randrange(self.rect.x - self.strafe_radius, self.rect.x + self.strafe_radius + 1)
                           self.targety = random.randrange(self.basey - self.strafe_radius, self.basey + self.strafe_radius + 1)
                   else:
                       while math.hypot(self.targetx - self.rect.x, self.targety - self.rect.y) > self.strafe_radius or math.hypot(self.targetx - self.rect.x, self.targety - self.rect.y) < self.strafe_radius / 2 or self.targetx < self.type.speed * 100 or self.targetx > WIN_W - self.type.speed * 100 or self.targety < self.type.speed * 100 or self.targety > WIN_H - self.type.speed * 100:
                           self.targetx = random.randrange(self.rect.x - self.strafe_radius, self.rect.x + self.strafe_radius + 1)
                           self.targety = random.randrange(self.rect.y - self.strafe_radius, self.rect.y + self.strafe_radius + 1)

           if math.fabs(math.hypot(self.xvel, self.yvel)) > self.type.speed * 20:
               self.xvel *= self.type.speed*20/math.fabs(math.hypot(self.xvel, self.yvel))
               self.yvel *= self.type.speed*20/math.fabs(math.hypot(self.xvel, self.yvel))
           self.x += self.xvel
           self.y -= self.yvel
           self.rect.x = self.x
           self.rect.y = self.y
           if math.fabs(self.xvel) < 0.01:
               self.xvel = 0
           else:
               self.xvel *= 0.98
           if math.fabs(self.yvel) < 0.01:
               self.yvel = 0
           else:
               self.yvel *= 0.98
           return 0
       else:
           self.cooldown -= 1


class Enemy_Bullet(pygame.sprite.Sprite):
   def __init__(self, spawner, enemy_bullet_type, direction):
       pygame.sprite.Sprite.__init__(self)
       self.type = enemy_bullet_type
       self.image = pygame.image.load('images/enemy_bullet.png')
       self.rect = self.image.get_rect()
       self.rect.centerx = spawner.rect.centerx
       self.rect.centery = spawner.rect.centery
       self.direction = direction
       self.player_direction = math.atan2(self.rect.centery - spawner.target.rect.centery, spawner.target.rect.centerx - self.rect.centerx)
       self.spawner = spawner
       if self.type.accel == False:
           self.xvel = math.cos(direction) * self.type.speed
           self.yvel = math.sin(direction) * self.type.speed
       else:
           if type(self.type.accel) == int:
               self.xvel = math.cos(direction) * self.type.accel
               self.yvel = math.sin(direction) * self.type.accel
           else:
               speed = int(self.type.accel[0:self.type.accel.find(";")]) + random.randrange(-int(self.type.accel[self.type.accel.find(";") + 1:-1]), int(self.type.accel[self.type.accel.find(";") + 1:-1]) + 1)
               self.xvel = math.cos(direction) * speed
               self.yvel = math.sin(direction) * speed
       self.x = self.rect.x
       self.y = self.rect.y
       if type(self.type.delay) == int:
           self.fuse = self.type.delay
       else:
           self.fuse = int(self.type.delay[0:self.type.delay.find(";")]) + random.randrange(-int(self.type.delay[self.type.delay.find(";") + 1:-1]), int(self.type.delay[self.type.delay.find(";") + 1:-1]) + 1)


   def update(self, target):
       if self.fuse == 0:
           if self.direction < -math.pi:
               self.direction += 2*math.pi
           if self.direction > math.pi:
               self.direction -= 2*math.pi
           if self.type.homing_speed > 0:
               player_direction = math.atan2(self.rect.centery - target.rect.centery, target.rect.centerx - self.rect.centerx)
               if self.direction >= 0:
                   if player_direction > self.direction or player_direction < self.direction - math.pi:
                       self.direction += math.radians(self.type.homing_speed) / 60
                   else:
                       self.direction -= math.radians(self.type.homing_speed) / 60
               else:
                   if player_direction > self.direction and player_direction < self.direction + math.pi:
                       self.direction += math.radians(self.type.homing_speed) / 60
                   else:
                       self.direction -= math.radians(self.type.homing_speed) / 60

           if self.type.accel != 0:
               self.xvel += math.cos(self.direction) * self.type.speed
               self.yvel += math.sin(self.direction) * self.type.speed

       else:
           player_direction = math.atan2(self.rect.centery - target.rect.centery,target.rect.centerx - self.rect.centerx)
           if self.type.accel != 0:
               if self.direction >= 0:
                   if player_direction > self.direction or player_direction < self.direction - math.pi:
                       self.direction += math.radians(self.type.homing_speed) / 60
                   else:
                       self.direction -= math.radians(self.type.homing_speed) / 60
               else:
                   if player_direction > self.direction and player_direction < self.direction + math.pi:
                       self.direction += math.radians(self.type.homing_speed) / 60
                   else:
                       self.direction -= math.radians(self.type.homing_speed) / 60
           self.fuse -= 1
           if self.fuse == 0:
               if self.type.homing_speed == 0:
                   self.direction = self.player_direction + math.radians(random.randrange(-self.type.spread, self.type.spread + 1))
               else:
                   self.direction = math.atan2(self.spawner.rect.centery - target.rect.centery, target.rect.centerx - self.spawner.rect.centerx) + math.radians(random.randrange(-self.type.spread, self.type.spread + 1))


           if math.fabs(self.xvel) < 0.01:
               self.xvel = 0
           else:
               self.xvel *= 0.95
           if math.fabs(self.yvel) < 0.01:
               self.yvel = 0
           else:
               self.yvel *= 0.95

       self.x += self.xvel
       self.y -= self.yvel
       self.rect.x = self.x
       self.rect.y = self.y

       if self.rect.x < 0 or self.rect.x > WIN_W or self.rect.y < 0 or self.rect.y > WIN_H:
           self.kill()


"""def main():
   pygame.init()
   # Create Game Variables
   clock = pygame.time.Clock()
   menu = True
   game = False
   pygame.display.set_caption('Raiden')
   screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)
   button_group = pygame.sprite.Group()
   ship_group = pygame.sprite.Group()
   bullet_group = pygame.sprite.Group()
   enemy_group = pygame.sprite.Group()
   enemy_bullet_group = pygame.sprite.Group()
   play_button = Button(WIN_W/2, WIN_H/2, WIN_W/3, WIN_H/10)
   button_group.add(play_button)
   while True:
       play_button.activate = False
       while menu:
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   sys.exit()
           play_button.update()
           if play_button.activate:
               menu = False
               game = True
           screen.fill(BLACK)
           screen.blit(play_button.image, play_button.rect)
           pygame.display.flip()
           clock.tick(fps)
       player = Ship(ship_type, WIN_W/2, WIN_H/2)
       ship_group.add(player)
       #t = Enemy(enemy_type_spiral, (random.randrange(WIN_W // 5, WIN_W * 4 // 5), 0), player)
       #enemy_group.add(t)
       #t = Enemy(enemy_type_regular, (random.randrange(WIN_W // 5, WIN_W * 4 // 5), 0), player)
       #enemy_group.add(t)
       t = Enemy(enemy_type_rocket, (random.randrange(WIN_W // 5, WIN_W * 4 // 5), 0), player)
       enemy_group.add(t)
       while game:
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   sys.exit()
           screen.fill(WHITE)
           for s in ship_group:
               s.update(bullet_group, enemy_bullet_group, game)
               if s.alive == False:
                   game = False
                   menu = True
                   s.kill()
                   for b in bullet_group:
                       b.kill()
                   for e in enemy_group:
                       e.kill()
                   for e in enemy_bullet_group:
                       e.kill()
           for b in bullet_group:
               b.update()
           for e in enemy_group:
               e.update(enemy_bullet_group, player, screen)
           for e in enemy_bullet_group:
               e.update(player)
           for s in ship_group:
               screen.blit(s.image, s.rect)
           for b in bullet_group:
               screen.blit(b.image, b.rect)
           for e in enemy_group:
               screen.blit(e.image, e.rect)
           for e in enemy_bullet_group:
               screen.blit(e.image, e.rect)
           pygame.display.flip()
           clock.tick(fps)
if __name__ == "__main__":
   main()"""
