import pygame, sys, random, math, idkanymore

width = 1280
height = 720

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (127, 127, 127)

bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()

chance_normal = 100
chance_spiral = 0
chance_shotgun = 0
chance_rocket = 0

hp = 1

score = 0

civil_group = pygame.sprite.Group()

dog = False
cat = False


civil_saved = 0
civil_needed = 3

shotgun = False
boomerang = False
presicion = False

SIZE = 32
SAVE_DATA = None
with open(".store.txt", 'r') as f:
	SAVE_DATA = eval(f.read())
	highscore = SAVE_DATA["highscore"]

class Boomerang(pygame.sprite.Sprite):
	def __init__(self, x, y, x_speed, y_speed, player):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("images/boomerang.png"), (SIZE, SIZE))
		self.rect = pygame.Rect((x,y), self.image.get_size())
		self.size = 20
		self.x_speed = x_speed
		self.y_speed = y_speed
		self.hit = False
		self.player = player
		self.target = player
		self.type = "bm"
		self.amogus = 0
	def update(self):
		self.image = pygame.transform.rotate(pygame.image.load("images/boomerang.png"), self.amogus)
		self.amogus += 10
		if self.rect.centerx < 0 or self.rect.centerx > width:
			self.kill()
		if self.rect.centery < 0 or self.rect.centery > height:
			self.kill()
		if self.hit:
			for e in enemy_group:
				if math.sqrt((self.rect.centerx - e.rect.centerx) ** 2 + (self.rect.centery - e.rect.centery) ** 2) <= 100:
					self.target = e
					break
				else:
					self.target = self.player
			if self.rect.centerx <= self.target.rect.centerx and self.rect.centery < self.target.rect.centery:
				dir = 1
				dir_y = 1
			elif self.rect.centerx <= self.target.rect.centerx and self.rect.centery >= self.target.rect.centery:
				dir_y = -1
				dir = 1
			elif self.rect.centerx > self.target.rect.centerx and self.rect.centery >= self.target.rect.centery:
				dir_y = -1
				dir = -1
			elif self.rect.centerx > self.target.rect.centerx and self.rect.centery < self.target.rect.centery:
				dir = -1
				dir_y = 1
			if not self.rect.centerx - self.target.rect.centerx == 0 and not self.rect.centery - self.target.rect.centery == 0:
				#self.rect.centerx += dir * math.cos(math.atan(abs(self.rect.centery - self.target.rect.centery) / abs(self.rect.centery - self.target.rect.centery))) * 20
				#self.rect.centery += dir_y * math.sin(math.atan(abs(self.rect.centery - self.target.rect.centery) / abs(self.rect.centery - self.target.rect.centery))) * 20
				self.rect.centerx -= (self.rect.centerx - self.target.rect.centerx) * 0.125
				self.rect.centery -= (self.rect.centery - self.target.rect.centery) * 0.125
			else:
				self.target = self.player
			if math.sqrt((self.rect.centerx - self.target.rect.centerx) ** 2 + (self.rect.centery - self.target.rect.centery) ** 2) <= 40:
				if not self.target == self.player:
					for e in enemy_group:
						if math.sqrt((self.rect.centerx - e.rect.centerx) ** 2 + (
								self.rect.centery - e.rect.centery) ** 2) <= 100:
							self.target = e
							break
						else:
							self.target = self.player
				else:
					self.kill()
		else:
			self.rect.centerx += self.x_speed
			self.rect.centery += self.y_speed



class Civilians(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		font = pygame.font.Font("fonts/fourside.ttf", SIZE * 2)
		if (not dog):
			self.image = font.render("!", 1, WHITE)
		else:
			self.image = font.render("!", 1, GREEN)
		self.rect = pygame.Rect(x, y, SIZE, SIZE)
		self.size = 40
		self.tick = 1
		self.rotation = 1
		self.dir = 1
		self.cooldown = 30
		self.speed = 2

	def update(self):
		global score
		global civil_saved
		if self.cooldown == 0:
			self.image = pygame.transform.scale(pygame.image.load('images/civilian.png'), (SIZE, SIZE))
			if self.tick <= 0:
				self.rect.y += (1 * self.speed)
				self.rect.x += (random.randint(-1, 1) if random.randint(5, 5) == 5 else 0)
				self.tick = 3
			self.tick -= 1
			if self.rect.y > height:
				civil_group.remove(self)
				civil_saved += 1
			hit = pygame.sprite.spritecollide(self, bullet_group, True)
			for e in hit:
				if(type(e) == type(Bullet)):
					score -= 5
					e.kill()
					self.kill()
				else:
					score -= 5
					self.kill()
				break


		else:
			self.cooldown -= 1


class Bullet(pygame.sprite.Sprite):
	def __init__(self, coordinates, x_speed, y_speed, image):
		super().__init__()
		self.type = "Bullet"
		self.image = image
		self.rect = pygame.Rect(coordinates[0], coordinates[1], 10, 10)
		self.size = 5
		self.x_speed = x_speed
		self.y_speed = y_speed
		self.type = "bu"

	def update(self):
		self.rect.x += self.x_speed
		self.rect.y += self.y_speed
		if self.rect.centerx < 0 or self.rect.centerx > width:
			self.kill()
		if self.rect.centery < 0 or self.rect.centery > height:
			self.kill()


def shootboom(player):
	new_boom = Boomerang(player.rect.centerx, player.rect.centery, player.dir * math.cos(player.rotation) * 20, player.dir_y * math.sin(player.rotation) * 20, player)
	bullet_group.add(new_boom)


def shoot(shooter_coordinates, dir, dir_y, rotation, player, speed):
	if player:
		new_bullet = Bullet(shooter_coordinates, math.cos(rotation) * dir * speed, math.sin(rotation) * dir_y * speed,
							pygame.image.load("images/player_bullet.png"))
		bullet_group.add(new_bullet)
	else:
		new_bullet = Bullet(shooter_coordinates, math.cos(rotation) * dir * speed, math.sin(rotation) * dir_y * speed,
							pygame.image.load("images/enemy_bullet.png"))
		enemy_bullet_group.add(new_bullet)


def spawn(player):
	if len(enemy_group) < 15:
		random_num = random.randint(1, 100)
		if random_num <= chance_rocket:
			t = idkanymore.Enemy(idkanymore.enemy_type_rocket, (random.randrange(height // 5, width * 4 // 5), 0),
								 player, hp, dog)
		if chance_rocket <= random_num and random_num <= chance_spiral + chance_rocket:
			t = idkanymore.Enemy(idkanymore.enemy_type_spiral, (random.randrange(height // 5, width * 4 // 5), 0),
								 player, hp, dog)
		if chance_spiral + chance_rocket <= random_num and random_num <= chance_shotgun + chance_spiral + chance_rocket:
			t = idkanymore.Enemy(idkanymore.enemy_type_spiral, (random.randrange(height // 5, width * 4 // 5), 0),
								 player, hp, dog)
		if chance_shotgun + chance_spiral + chance_rocket <= random_num and random_num <= 100:
			t = idkanymore.Enemy(idkanymore.enemy_type_regular, (random.randrange(height // 5, width * 4 // 5), 0),
								 player, hp, dog)
		enemy_group.add(t)

def noboom(group):
	for b in group:
		if type(b) != type(Bullet):
			return False
	return True

class Player:
	def __init__(self, gamemode):
		self.image = pygame.transform.scale(pygame.image.load("images/character.png"), (SIZE, SIZE))
		self.rect = pygame.Rect(width / 2, height / 2, SIZE, SIZE)
		self.size = 10
		self.speed = 1
		self.rotation = 0
		self.dir = 1
		self.dir_y = 1
		self.cooldown_counter = 0
		self.scooldown_counter = 0
		self.cooldown = 20
		self.health = 5
		self.healthcounter = 0
		self.dead = False
		self.bullet_speed = 10
		self.weapon = 0
		self.primed = False
		self.primed_cooldown = 0
		self.gamemode = gamemode
		self.dashcool = -1000
		self.dashlen = 10
		self.dashspeed = 5
		self.dashcooltime = 250
		self.invinc = False
		self.bullets = 50
		self.souls = 0
		self.soulspersoulcrystal = 3
		self.soulcrystals = 0
		self.soulrange = 256
		self.soulexpanimcount = 0

	def update(self, left_clicked, right_clicked, true_screen):
		global score
		self.soulcrystals += 1
		if self.soulexpanimcount > 0:
			self.soulexpanimcount -= 32
			image = pygame.transform.scale(pygame.image.load("images/soulexp.png"), (self.soulrange * 2 * (self.soulexpanimcount / 512), self.soulrange * 2 * (self.soulexpanimcount / 512)))
			imagerect = image.get_rect()
			imagerect.centerx = self.rect.centerx
			imagerect.centery = self.rect.centery
			screen.blit(image, imagerect)
		self.dashcool -= 1
		if self.dashcool == 0:
			self.speed /= self.dashspeed
			self.invinc = False
			pass
		mouse_pos = pygame.mouse.get_pos()
		mouse_pos = (mouse_pos[0] / (true_screen.get_rect().size[0] / width),
					 mouse_pos[1] / (true_screen.get_rect().size[1] / height))
		key = pygame.key.get_pressed()
		if key[pygame.K_l]:
			self.dead = True
		if self.rect.centerx - mouse_pos[0] != 0:
			self.rotation = math.atan(abs(self.rect.centery - mouse_pos[1]) / abs(self.rect.centerx - mouse_pos[0]))
		else:
			self.slope = 0

		if self.rect.centerx <= mouse_pos[0] and self.rect.centery < mouse_pos[1]:
			self.dir = 1
			self.dir_y = 1
		elif self.rect.centerx <= mouse_pos[0] and self.rect.centery >= mouse_pos[1]:
			self.dir_y = -1
			self.dir = 1
		elif self.rect.centerx > mouse_pos[0] and self.rect.centery >= mouse_pos[1]:
			self.dir_y = -1
			self.dir = -1
		elif self.rect.centerx > mouse_pos[0] and self.rect.centery < mouse_pos[1]:
			self.dir = -1
			self.dir_y = 1
		if self.gamemode == 1:
			if right_clicked and abs(self.rect.x - mouse_pos[0]) > 10 and abs(self.rect.y - mouse_pos[1]) > 10:
				self.rect.x += math.cos(self.rotation) * self.speed * self.dir
				self.rect.y += math.sin(self.rotation) * self.speed * self.dir
		elif self.gamemode == 0:
			if key[pygame.K_w] and self.rect.top > 0:
				self.rect.y -= self.speed
			elif key[pygame.K_s] and self.rect.bottom < height:
				self.rect.y += self.speed
			if key[pygame.K_a] and self.rect.left > 0:
				self.rect.x -= self.speed
			elif key[pygame.K_d] and self.rect.right < width:
				self.rect.x += self.speed
			if (key[pygame.K_LSHIFT] or key[pygame.K_SPACE]) and self.dashcool <= -self.dashcooltime:
				self.speed *= self.dashspeed
				self.dashcool = self.dashlen
				self.invinc = True
			if key[pygame.K_q] and self.soulcrystals >= 3:
				print("works")
				self.soulcrystals = 0
				for e in enemy_group:
					if ((self.rect.centerx - e.rect.centerx)**2 + (self.rect.centery - e.rect.centery)**2)**0.5 <= self.soulrange:
						enemy_group.remove(e)
						score += 1
				self.soulexpanimcount = 512
		if self.weapon == 0:
			if left_clicked and self.cooldown_counter == 0:
				shoot((self.rect.centerx, self.rect.centery), self.dir, self.dir_y, self.rotation, True,
					  self.bullet_speed)
				self.cooldown_counter = self.cooldown
			if right_clicked and self.scooldown_counter == 0:
				if boomerang:
					if (noboom(bullet_group)):
						shootboom(self)
				elif shotgun:
				# if math.floor(self.bullets) == 3:
						#shoot((self.rect.centerx, self.rect.centery), self.dir, self.dir_y, self.rotation, True,
							  #self.bullet_speed)
						#shoot((self.rect.centerx, self.rect.centery), self.dir, self.dir_y, self.rotation - 0.25, True,
							  #self.bullet_speed)
						#shoot((self.rect.centerx, self.rect.centery), self.dir, self.dir_y, self.rotation + 0.25, True,
							  #self.bullet_speed)
					for e in range(math.floor(self.bullets/2) * 5):
						shoot((self.rect.centerx, self.rect.centery), self.dir, self.dir_y, self.rotation + e/(self.bullets * 10), True, self.bullet_speed)
						shoot((self.rect.centerx, self.rect.centery), self.dir, self.dir_y, self.rotation - e/(self.bullets * 10), True,self.bullet_speed)
					self.scooldown_counter = 40
				elif presicion:
					for e in enemy_group:
						if math.sqrt((e.rect.centerx - mouse_pos[0]) ** 2 + (e.rect.centery - mouse_pos[1]) ** 2) <= SIZE:
							enemy_group.remove(e)
							score += 1
					for e in civil_group:
						if math.sqrt((e.rect.centerx - mouse_pos[0]) ** 2 + (e.rect.centery - mouse_pos[1]) ** 2) <= SIZE:
							civil_group.remove(e)
							score -= 5
					if self.cooldown * 10 >= 100:
						self.scooldown_counter = self.cooldown*10
					else:
						self.scooldown_counter = 100

			if self.cooldown_counter > 0:
				self.cooldown_counter -= 1

			if self.scooldown_counter > 0:
				self.scooldown_counter -= 1

		for l in enemy_bullet_group:
			if abs(l.rect.centerx - self.rect.centerx) < self.size * 2 and abs(
					l.rect.centery - self.rect.centery) < self.size * 2 and not self.invinc:
				self.health -= 1
				l.kill()
				self.healthcounter = 100

		if self.primed_cooldown > 0:
			self.primed_cooldown -= 1

		if self.healthcounter > 0:
			self.healthcounter -= 1

		if self.health <= 0:
			self.dead = True

		self.rect.clamp_ip(screen.get_rect())


true_screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
screen = pygame.Surface((width, height))
pygame.mouse.set_visible(False)
cursor_img_rect = pygame.image.load("images/cross0.png").get_rect()

def main():
	global score
	global chance_normal
	global chance_shotgun
	global chance_spiral
	global chance_rocket
	global hp
	global cat
	global dog
	global highscore
	global civil_saved
	global civil_needed
	global boomerang
	global shotgun
	global presicion
	global SAVE_DATA

	dogb = False
	catb = False
	horseb = False

	cat = dog = horse = False

	civil_saved = 0

	catc = 300

	pygame.init()
	pygame.font.init()
	pygame.mixer.init()
	clock = pygame.time.Clock()

	shotgun = boomerang = presicion = False

	civil_needed = 2

	i = 0
	break_var = False

	level = 1
	level_counter = 0
	chance_normal = 100
	chance_shotgun = chance_spiral = chance_rocket = 0
	hp = 1

	for k in civil_group:
		civil_group.remove(k)

	font = pygame.font.Font("fonts/fourside.ttf", 75)
	title = font.render("-- Gunpoint --", 1, WHITE)
	titlepos = title.get_rect()
	titlepos.centerx = width / 2
	titlepos.centery = height / 4

	font2 = pygame.font.Font("fonts/fourside.ttf", 35)
	click = font2.render("-- Click here to Play --", 1, WHITE)
	clickpos = click.get_rect()
	clickpos.centerx = width / 2
	clickpos.centery = height / 2

	font2 = pygame.font.Font("fonts/fourside.ttf", 35)
	click1 = font2.render(("-- High : " + str(highscore) + " --"), 1, WHITE)
	click2 = font2.render(("-- Last : " + str(SAVE_DATA["lastscore"]) + " --"), 1, WHITE)

	while not break_var:
		screen.fill(BLACK)
		cursor_img_rect.center = pygame.mouse.get_pos()
		cursor_img_rect.centerx /= (true_screen.get_width()/screen.get_width())
		cursor_img_rect.centery /= (true_screen.get_width()/screen.get_width())
		screen.blit(pygame.transform.rotate(pygame.image.load(f"images/cross0.png"), 25), cursor_img_rect)
		screen.blit(title, titlepos)
		screen.blit(click1, (width / 2 - click1.get_width() / 2, height / 2 + height / 4))
		screen.blit(click2, (width / 2 - click1.get_width() / 2, height / 2 + height / 3))

		if i > 10:
			if i > 20:
				i = 0
			screen.blit(click, clickpos)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				break_var = True
		pygame.display.flip()
		i += 1
		clock.tick(60)
		true_screen.blit(pygame.transform.scale(screen, true_screen.get_rect().size), (0, 0))

	player = Player(0)
	left_click = False
	right_click = False
	clock = pygame.time.Clock()
	heart_image = pygame.image.load("images/heart.png")
	menu = False
	play = True
	weaponm = petm = False
	score = 0
	spawn_rate = 150
	lvl_time = 500
	for t in enemy_group:
		enemy_group.remove(t)

	for r in bullet_group:
		bullet_group.remove(r)

	for s in enemy_bullet_group:
		enemy_bullet_group.remove(s)
	r = 0
	r_count = 30
	while True:
		if play:
			level_counter += 1
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						left_click = True
					if event.button == 3:
						right_click = True
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						left_click = False
					if event.button == 3:
						right_click = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_e:
						play = False
						menu = True
			screen.fill(BLACK)
			if (r_count == 0):
				r = (r + 0.05) % 360
			else:
				r_count -= 1
			if catc > 0:
				catc -= 1

			if catc == 0 and cat == True and len(enemy_group) > 0:
				fir = False
				for e in enemy_group:
					if not fir:
						e.hp -= 1
						fir = True
						if e.hp <= 0:
							enemy_group.remove(e)
							score += 1
						catc = 300
			if dog:
				screen.blit(pygame.image.load("images/dog.png"), (
					pygame.Rect(player.rect.centerx - 15 + math.sin(r) * 80,
								player.rect.centery - 15 + math.cos(r) * 80, 80, 60, )))
			if cat:
				screen.blit(pygame.image.load("images/cat.png"), (
					pygame.Rect(player.rect.centerx - 15 + math.sin(r) * 80,
								player.rect.centery - 15 + math.cos(r) * 80, 60, 60, )))
			if level_counter >= lvl_time and civil_saved >= civil_needed:
				chance_normal -= 6
				chance_shotgun += 3
				chance_shotgun += 2
				chance_rocket += 1
				level_counter = 0
				level += 1
				if level % 4 == 0:
					hp += 1
				if not spawn_rate - 10 <= 0:
					spawn_rate -= 10
				lvl_time += 100
				score += 3
				civil_saved -= civil_needed
				if level % 2 == 0:
					civil_needed += 1

			if (random.randint(1, spawn_rate) == 1):
				spawn(player)

			player.update(left_click, right_click, true_screen)
			bullet_group.update()
			civil_group.update()
			enemy_bullet_group.update(player)
			enemy_group.update(enemy_bullet_group, player, screen, bullet_group)

			if random.randint(1, 500) == 1:
				new_civilian = Civilians(random.randint(0, width), 0)
				civil_group.add(new_civilian)

			for c in enemy_group:
				if c.alive:
					screen.blit(c.image, c.rect)
				else:
					c.hp -= 1
					if c.hp == 0:
						enemy_group.remove(c)
						player.souls += 1
						print(player.souls, player.soulcrystals)
						if player.souls >= player.soulspersoulcrystal:
							player.souls = 0
							player.soulcrystals += 1
						score += 1
					else:
						c.alive = True
			screen.blit(player.image, player.rect)
			enemy_bullet_group.draw(screen)
			bullet_group.draw(screen)
			civil_group.draw(screen)

			if not len(enemy_group):
				for c in civil_group:
					if (c.speed < 4 or (horse and c.speed <= 4)):
						c.speed *= 2

			if len(enemy_group):
				for c in civil_group:
					if (c.speed == 4 or (horse and c.speed == 8)):
						c.speed /= 2

			if horse and len(civil_group):
				fir = True
				for c in civil_group:
					if fir and c.speed < 4:
						c.speed *= 2
						fir = False
			if player.dead:
				if level > highscore:
					highscore = level
				with open(".store.txt", 'w') as f:
					data = {
						"highscore": highscore,
						"lastscore": level
					}
					f.write(str(data))
				with open(".store.txt", 'r') as f:
					SAVE_DATA = eval(f.read())
				main()

			for i in range(player.health):
				rect = pygame.Rect(10 + i * 30, 10, 20, 20)
				screen.blit(heart_image, rect)

			score_txt = font2.render(str(score), 1, WHITE)
			scorepos = score_txt.get_rect()
			scorepos.centerx = width - 50
			scorepos.centery = 20

			lvl_txt = font.render(str(level), 1, WHITE)
			lvlpos = lvl_txt.get_rect()
			lvlpos.centerx = width / 2
			lvlpos.centery = 50

			screen.blit(score_txt, scorepos)
			screen.blit(lvl_txt, lvlpos)
			screen.blit(font2.render(str(min(100, round((level_counter / lvl_time) * 100))) + '%', 1, WHITE), (10, 50))
			screen.blit(font2.render(str(civil_saved) + '/' + str(civil_needed), 1, WHITE), (10, 100))

			if player.dashcool/player.dashcooltime >= -1:
				num = abs(player.dashcool/player.dashcooltime) * 100
			else:
				num = 100

			screen.blit(font2.render(str(round(num)) + '%', 1, WHITE), (10, 150))

		elif menu:
			screen.fill(BLACK)
			game_menu = pygame.image.load("images/menu_2.png")
			menu_rect = pygame.Rect(width/2 - game_menu.get_width()/2, height/2 - game_menu.get_height()/2, 970, 620)
			screen.blit(game_menu, menu_rect)
			score_txt = font2.render(str(score), 1, WHITE)
			scorepos = score_txt.get_rect()
			scorepos.centerx = width - 50
			scorepos.centery = 20
			screen.blit(score_txt, scorepos)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						mouse_pos = pygame.mouse.get_pos()
						mouse_pos = (mouse_pos[0] / (true_screen.get_rect().size[0] / width),
									 mouse_pos[1] / (true_screen.get_rect().size[1] / height))
						if 781 < mouse_pos[0] < 998:
							if 464 < mouse_pos[1] < 519:
								if score >= 5:
									score -= 5
									player.speed += 4
							elif 355 < mouse_pos[1] < 412:
								if score >= 1 and player.cooldown > 1:
									score -= 1
									player.cooldown -= 1
									player.bullets += 0.5
							elif 246 < mouse_pos[1] < 301:
								if score >= 2:
									score -= 2
									player.health += 1
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RIGHT:
						petm = True
						menu = False
					if event.key == pygame.K_e:
						play = True
						menu = False
		elif petm:
			screen.fill(BLACK)
			game_menu = pygame.image.load("images/pet_menu_2.png")
			menu_rect = pygame.Rect(width/2 - game_menu.get_width()/2, height/2 - game_menu.get_height()/2, 970, 620)
			screen.blit(game_menu, menu_rect)
			score_txt = font2.render(str(score), 1, WHITE)
			scorepos = score_txt.get_rect()
			scorepos.centerx = width - 50
			scorepos.centery = 20
			screen.blit(score_txt, scorepos)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						mouse_pos = pygame.mouse.get_pos()
						mouse_pos = (mouse_pos[0] / (true_screen.get_rect().size[0] / width),
									 mouse_pos[1] / (true_screen.get_rect().size[1] / height))
						if (781 < mouse_pos[0] and mouse_pos[0] < 999 and 247 < mouse_pos[1] and mouse_pos[1] < 301):
							if (score >= 7 and not dog and dogb == False):
								dog = True
								score -= 7
								dogb = True
								cat = horse = False
							elif not dog and dogb:
								dog = True
								cat = False
						if (781 < mouse_pos[0] and mouse_pos[0] < 999 and 357 < mouse_pos[1] and mouse_pos[1] < 411):
							if (score >= 7 and not cat and catb == False):
								cat = True
								score -= 7
								catb = True
								dog = horse = False
							elif not cat and catb:
								cat = True
								dog = horse = False
						if (781 < mouse_pos[0] and mouse_pos[0] < 999 and 475 < mouse_pos[1] and mouse_pos[1] < 527):
							if (score >= 7 and not horse and horseb == False):
								horse = True
								score -= 7
								horseb = True
								dog = cat = False
							elif not cat and catb:
								horse = True
								dog = cat = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						petm = False
						menu = True
					if event.key == pygame.K_RIGHT:
						petm = False
						weaponm = True
					if event.key == pygame.K_e:
						play = True
						petm = False
		elif weaponm:
			screen.fill(BLACK)
			game_menu = pygame.image.load("images/gun_menu.png")
			menu_rect = pygame.Rect(width/2 - game_menu.get_width()/2, height/2 - game_menu.get_height()/2, 970, 620)
			screen.blit(game_menu, menu_rect)
			score_txt = font2.render(str(score), 1, WHITE)
			scorepos = score_txt.get_rect()
			scorepos.centerx = width - 50
			scorepos.centery = 20
			screen.blit(score_txt, scorepos)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						mouse_pos = pygame.mouse.get_pos()
						mouse_pos = (mouse_pos[0] / (true_screen.get_rect().size[0] / width),
									 mouse_pos[1] / (true_screen.get_rect().size[1] / height))
						print(mouse_pos)
						if (781 < mouse_pos[0] and mouse_pos[0] < 999 and 247 < mouse_pos[1] and mouse_pos[1] < 301):
							if score >= 10:
								presicion = True
								shotgun = boomerang = False
								score -= 10
						if (781 < mouse_pos[0] and mouse_pos[0] < 999 and 357 < mouse_pos[1] and mouse_pos[1] < 411):
							if score >= 10:
								boomerang = True
								shotgun = presicion = False
								score -= 10
						if (781 < mouse_pos[0] and mouse_pos[0] < 999 and 475 < mouse_pos[1] and mouse_pos[1] < 527):
							if score >= 10:
								shotgun = True
								boomerang = presicion = False
								score -= 10
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						weaponm = False
						petm = True
					if event.key == pygame.K_e:
						play = True
						weaponm = False

		cursor_img_rect.centerx = pygame.mouse.get_pos()[0]
		if weaponm or menu or petm:
			cursor_img_rect.top = pygame.mouse.get_pos()[1]
		else:
			cursor_img_rect.centery = pygame.mouse.get_pos()[1]
		cursor_img_rect.centerx /= (true_screen.get_width()/screen.get_width())
		cursor_img_rect.centery /= (true_screen.get_width()/screen.get_width())
		if presicion and not(weaponm or menu or petm):
			cursor_img_rect.centerx += random.randint(-30, 30)
			cursor_img_rect.centery += random.randint(-30, 30)
		screen.blit(pygame.transform.rotate(pygame.image.load(f"images/cross{min(3, player.soulcrystals)}.png"), 25 if (petm or weaponm or menu) else (math.atan2(player.rect.centerx - cursor_img_rect.centerx, player.rect.centery - cursor_img_rect.centery)*(180/math.pi))), cursor_img_rect)
		true_screen.blit(pygame.transform.scale(screen, true_screen.get_rect().size), (0, 0))
		pygame.display.flip()
		clock.tick(60)


main()

