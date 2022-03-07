import pygame, sys, random, math, idkanymore

width = 970
height = 620

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

highscore = 0

civil_saved = 0
civil_needed = 3

class Civilians(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        font = pygame.font.Font("fonts/fourside.ttf", 70)
        if (not dog):
            self.image = font.render("!", 1, WHITE)
        else:
            self.image = font.render("!", 1, GREEN)
        self.rect = pygame.Rect(x, y, 40, 40)
        self.size = 40
        self.tick = 1
        self.rotation = 1
        self.dir = 1
        self.cooldown = 30
        self.speed = 1

    def update(self):
        global score
        global civil_saved
        if self.cooldown == 0:
            self.image = pygame.image.load('images/civilian.png')
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
                score -= 10
                self.kill()


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
        self.lifetime = 2000

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.lifetime -= 1
        if self.lifetime == 0:
            bullet_group.remove(self)

def shoot(shooter_coordinates, dir, dir_y, rotation, player, speed):
    if player:
        new_bullet = Bullet(shooter_coordinates, math.cos(rotation) *dir * speed, math.sin(rotation) *dir_y * speed, pygame.image.load("images/player_bullet.png"))
        bullet_group.add(new_bullet)
    else:
        new_bullet = Bullet(shooter_coordinates, math.cos(rotation) *dir * speed, math.sin(rotation) *dir_y * speed, pygame.image.load("images/enemy_bullet.png"))
        enemy_bullet_group.add(new_bullet)


def spawn(player):
    if len(enemy_group) < 15:
        random_num = random.randint(1, 100)
        if random_num <= chance_rocket:
            t = idkanymore.Enemy(idkanymore.enemy_type_rocket, (random.randrange(height // 5, width * 4 // 5), 0), player, hp, dog)
        if chance_rocket <= random_num and random_num <= chance_spiral + chance_rocket:
            t = idkanymore.Enemy(idkanymore.enemy_type_spiral, (random.randrange(height // 5, width * 4 // 5), 0), player, hp, dog)
        if chance_spiral + chance_rocket <= random_num and random_num <= chance_shotgun + chance_spiral + chance_rocket:
            t = idkanymore.Enemy(idkanymore.enemy_type_shotgun, (random.randrange(height // 5, width * 4 // 5), 0), player, hp, dog)
        if chance_shotgun + chance_spiral + chance_rocket <= random_num and random_num <= 100:
            t = idkanymore.Enemy(idkanymore.enemy_type_regular, (random.randrange(height // 5, width * 4 // 5), 0), player, hp, dog)
        enemy_group.add(t)

class Player:
    def __init__(self, gamemode):
        self.image = pygame.image.load("images/character.png")
        self.rect = pygame.Rect(width/2, height/2, 40, 40)
        self.size = 10
        self.speed = 1
        self.rotation = 0
        self.dir = 1
        self.dir_y = 1
        self.cooldown_counter = 0
        self.cooldown = 20
        self.health = 5
        self.healthcounter = 0
        self.dead = False
        self.bullet_speed = 10
        self.weapon = 0
        self.primed = False
        self.bomb = None
        self.primed_cooldown = 0
        self.gamemode = gamemode
        self.dashcool = -1000
        self.dashlen = 10
        self.dashspeed = 5
        self.dashcooltime = 250

    def update(self, left_clicked, right_clicked, true_screen):
        self.dashcool -= 1
        if self.dashcool == 0:
            self.speed /= self.dashspeed
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0] / (true_screen.get_rect().size[0]/width), mouse_pos[1] / (true_screen.get_rect().size[1]/height))
        print((true_screen.get_rect().size[0]/width))
        key = pygame.key.get_pressed()
        if key[pygame.K_l]:
            self.dead = True
        if self.rect.centerx - mouse_pos[0] != 0:
            self.rotation = math.atan(abs(self.rect.centery - mouse_pos[1])/abs(self.rect.centerx - mouse_pos[0]))
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
            if key[pygame.K_SPACE] and self.dashcool <= -self.dashcooltime:
                self.speed *= self.dashspeed
                self.dashcool = self.dashlen
        if self.weapon == 0:
            if left_clicked and self.cooldown_counter == 0:
                shoot((self.rect.centerx, self.rect.centery), self.dir, self.dir_y, self.rotation, True, self.bullet_speed)
                self.cooldown_counter = self.cooldown

            if self.cooldown_counter > 0:
                self.cooldown_counter -= 1

        for l in enemy_bullet_group:
            if abs(l.rect.centerx - self.rect.centerx) < self.size * 2 and abs(l.rect.centery - self.rect.centery) < self.size * 2: #and self.healthcounter >= 0:
                self.health -= 1
                l.kill()
                self.healthcounter = 100

        if self.primed_cooldown > 0:
            self.primed_cooldown -= 1

        if self.healthcounter > 0:
            self.healthcounter -= 1

        if self.health <= 0:
            self.dead = True


true_screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
screen = pygame.Surface((width, height))


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

    dogb = False
    catb = False
    horseb = False

    cat = dog = horse = False

    catc = 300

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    civil_needed = 3

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
    titlepos.centerx = width/2
    titlepos.centery = height/4

    font2 = pygame.font.Font("fonts/fourside.ttf", 35)
    click = font2.render("-- Click here to Play --", 1, WHITE)
    clickpos = click.get_rect()
    clickpos.centerx = width/2
    clickpos.centery = height/2

    font2 = pygame.font.Font("fonts/fourside.ttf", 35)
    click1 = font2.render(("-- High : " + str(highscore) + " --"), 1, WHITE)
    clickpos1 = click1.get_rect()
    clickpos1.centerx = width/2
    clickpos1.centery = height/2 + height / 4

    while not break_var:
        screen.fill(BLACK)
        screen.blit(title, titlepos)
        screen.blit(click1, clickpos1)
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
    score = 0
    spawn_rate = 150
    lvl_time = 1000
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
                    if event.key == pygame.K_q:
                        play = False
                        petm = True
                    elif event.key == pygame.K_e:
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
                screen.blit(pygame.image.load("images/dog.png"), (pygame.Rect(player.rect.centerx - 15 + math.sin(r) * 80, player.rect.centery - 15 + math.cos(r) * 80, 80, 60 ,)))
            if cat:
                screen.blit(pygame.image.load("images/cat.png"), (pygame.Rect(player.rect.centerx - 15 + math.sin(r) * 80, player.rect.centery - 15 + math.cos(r) * 80, 60, 60 ,)))
            if level_counter >= lvl_time and civil_saved >= civil_needed:
                chance_normal -= 6
                chance_shotgun += 3
                chance_shotgun += 2
                chance_rocket += 1
                level_counter = 0
                level += 1
                if level % 4 == 0:
                    hp += 1
                spawn_rate += 10
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
                        score += 1
                    else:
                        c.alive = True
            screen.blit(player.image, player.rect)
            enemy_bullet_group.draw(screen)
            bullet_group.draw(screen)
            civil_group.draw(screen)
            
            if not len(enemy_group):
                for c in civil_group:
                    if (c.speed < 2 or (horse and c.speed <= 2)):
                        c.speed *= 2

            if len(enemy_group):
                for c in civil_group:
                    if (c.speed == 2 or (horse and c.speed == 4)):
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
                main()

            for i in range(player.health):
                rect = pygame.Rect(10 + i*30, 10, 20, 20)
                screen.blit(heart_image, rect)

            score_txt = font2.render(str(score), 1, WHITE)
            scorepos = score_txt.get_rect()
            scorepos.centerx = width - 50
            scorepos.centery = 20

            lvl_txt = font.render(str(level), 1, WHITE)
            lvlpos = lvl_txt.get_rect()
            lvlpos.centerx = width/2
            lvlpos.centery = 50

            screen.blit(score_txt, scorepos)
            screen.blit(lvl_txt, lvlpos)
            screen.blit(font2.render(str(min(100, round((level_counter/lvl_time)*100))) + '%', 1, WHITE), (10, 50))
            screen.blit(font2.render(str(civil_saved) + '/' + str(civil_needed), 1, WHITE), (10, 100))
        elif menu:
            screen.fill(WHITE)
            game_menu = pygame.image.load("images/menu_2.png")
            menu_rect = pygame.Rect(0, 0, 970, 620)
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
                        mouse_pos = (mouse_pos[0] / (true_screen.get_rect().size[0]/width), mouse_pos[1] / (true_screen.get_rect().size[1]/height))
                        if 623 < mouse_pos[0] < 844:
                            if 420 < mouse_pos[1] < 465:
                                if score >= 5:
                                    score -= 5
                                    player.speed += 4
                            elif 313 < mouse_pos[1] < 357:
                                if score >= 1 and player.cooldown > 1:
                                    score -= 1
                                    player.cooldown -= 1
                            elif 201 < mouse_pos[1] < 245:
                                if score >= 2:
                                    score -= 2
                                    player.health += 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        play = True
                        menu = False
        elif petm:
            screen.fill(WHITE)
            game_menu = pygame.image.load("images/pet_menu_2.png")
            menu_rect = pygame.Rect(0, 0, 970, 620)
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
                        mouse_pos = (mouse_pos[0] / (true_screen.get_rect().size[0]/width), mouse_pos[1] / (true_screen.get_rect().size[1]/height))
                        if (630 < mouse_pos[0] and mouse_pos[0] < 838 and 202 < mouse_pos[1] and mouse_pos[1] < 244):
                            if(score >= 7 and not dog and dogb == False):
                                dog = True
                                score -= 7
                                dogb = True
                                cat = horse = False
                            elif not dog and dogb:
                                dog = True
                                cat = False
                        if (630 < mouse_pos[0] and mouse_pos[0] < 838 and 313 < mouse_pos[1] and mouse_pos[1] < 355):
                            if(score >= 7 and not cat and catb == False):
                                cat = True
                                score -= 7
                                catb = True
                                dog = horse = False
                            elif not cat and catb:
                                cat = True
                                dog = horse = False
                        if (630 < mouse_pos[0] and mouse_pos[0] < 838 and 431 < mouse_pos[1] and mouse_pos[1] < 474):
                            if(score >= 7 and not horse and horseb == False):
                                horse = True
                                score -= 7
                                horseb = True
                                dog = cat = False
                            elif not cat and catb:
                                horse = True
                                dog = cat = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        play = True
                        petm = False

        true_screen.blit(pygame.transform.scale(screen, true_screen.get_rect().size), (0, 0))
        pygame.display.flip()
        clock.tick(60)

main()
