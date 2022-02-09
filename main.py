import pygame, sys, random, math, idkanymore

width = 970
height = 620

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (127, 127, 127)

bullet_group = pygame.sprite.Group()
char_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()

chance_normal = 100
chance_spiral = 0
chance_shotgun = 0
chance_rocket = 0

chance_spawn = 250

hp = 1

score = 0

lvl_time = 1000

bullet_groupt = pygame.sprite.Group()


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
    if len(char_group) < 15:
        random_num = random.randint(1, 200)
        if random_num <= chance_rocket:
            t = idkanymore.Enemy(idkanymore.enemy_type_rocket, (random.randrange(height // 5, width * 4 // 5), 0), player, hp)
        elif chance_rocket <= random_num and random_num <= chance_spiral + chance_rocket:
            t = idkanymore.Enemy(idkanymore.enemy_type_spiral, (random.randrange(height // 5, width * 4 // 5), 0), player, hp)
        elif chance_spiral + chance_rocket <= random_num and random_num <= chance_shotgun + chance_spiral + chance_rocket:
            t = idkanymore.Enemy(idkanymore.enemy_type_shotgun, (random.randrange(height // 5, width * 4 // 5), 0), player, hp)
        elif chance_shotgun + chance_spiral + chance_rocket <= random_num and random_num <= 100:
            t = idkanymore.Enemy(idkanymore.enemy_type_regular, (random.randrange(height // 5, width * 4 // 5), 0), player, hp)
        elif random_num >= 100s:
            t = idkanymore.Enemy(idkanymore.enemy_type_spiral, (random.randrange(height // 5, width * 4 // 5), 0), player, 1, "G")
        char_group.add(t)

class Player:s
    def __init__(self, gamemode):
        self.image = pygame.image.load("images/character.png")
        self.rect = pygame.Rect(width/2, height/2, 40, 40)
        self.size = 10
        self.speed = 1
        self.rotation = 0
        self.dir = 1
        self.dir_y = 1
        self.cooldown_counter = 0
        self.cooldown = 10
        self.health = 5
        self.healthcounter = 0
        self.dead = False
        self.bullet_speed = 10
        self.weapon = 0
        self.primed = False
        self.bomb = None
        self.primed_cooldown = 0
        self.gamemode = gamemode

    def update(self, left_clicked, right_clicked, screen):
        mouse_pos = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()
        if key[pygame.K_l]:
            self.health = 100000
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
        if self.weapon == 0:
            if left_clicked and self.cooldown_counter == 0:
                shoot((self.rect.centerx, self.rect.centery), self.dir, self.dir_y, self.rotation, True, self.bullet_speed)
                self.cooldown_counter = self.cooldown

            if self.cooldown_counter > 0:
                self.cooldown_counter -= 1

        for l in enemy_bullet_group:
            if abs(l.rect.centerx - self.rect.centerx) < self.size * 2 and abs(l.rect.centery - self.rect.centery) < self.size * 2 and self.healthcounter == 0:
                self.health -= 1
                self.healthcounter = 10

        if self.primed_cooldown > 0:
            self.primed_cooldown -= 1

        if self.healthcounter > 0:
            self.healthcounter -= 1

        if self.health <= 0:
            self.dead = True


def main():
    global score
    global chance_normal
    global chance_shotgun
    global chance_spiral
    global chance_rocket
    global hp
    global chance_spawn
    global lvl_time

    chance_normal = 100
    chance_rocket = chance_shotgun = chance_spiral = 0
    hp = 1
    chance_spawn = 250
    lvl_time = 1000

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    i = 0
    break_var = False

    level = 1
    level_counter = 0

    font = pygame.font.Font("fonts/fourside.ttf", 75)
    title = font.render("-- Shooter --", 1, BLACK)
    titlepos = title.get_rect()
    titlepos.centerx = width/2
    titlepos.centery = height/4

    font2 = pygame.font.Font("fonts/fourside.ttf", 35)
    click = font2.render("-- Click here to Play --", 1, BLACK)
    clickpos = click.get_rect()
    clickpos.centerx = width/2
    clickpos.centery = height/2

    while not break_var:
        screen.fill(WHITE)
        screen.blit(title, titlepos)
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

    screen = pygame.display.set_mode((width, height))
    player = Player(0)
    left_click = False
    right_click = False
    clock = pygame.time.Clock()
    heart_image = pygame.image.load("images/heart image resize.png")
    menu = False
    play = True
    score = 0
    for t in char_group:
        char_group.remove(t)

    for r in bullet_group:
        bullet_group.remove(r)

    for s in enemy_bullet_group:
        enemy_bullet_group.remove(s)

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
                    if event.button == 2:
                        menu = True
                        play = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        left_click = False
                    if event.button == 3:
                        right_click = False
            screen.fill(WHITE)

            if level_counter == lvl_time:
                chance_normal -= 6
                chance_shotgun += 3
                chance_shotgun += 2
                chance_rocket += 1
                level_counter = 0
                level += 1
                chance_spawn -= 20
                hp += 1
                lvl_time += 100

            if (random.randint(1, chance_spawn) == 1):
                spawn(player)

            player.update(left_click, right_click, screen)
            bullet_group.update()
            enemy_bullet_group.update(player)
            char_group.update(enemy_bullet_group, player, screen, bullet_group)

            for c in char_group:
                if c.alive:
                    screen.blit(c.image, c.rect)
                else:
                    c.hp -= 1
                    if c.hp == 0:
                        char_group.remove(c)
                        if c.t == "R":
                            score += 1
                        else:
                            score -= 10
                    else:
                        c.alive = True
            screen.blit(player.image, player.rect)
            enemy_bullet_group.draw(screen)
            bullet_group.draw(screen)

            if player.dead:
                main()

            for i in range(player.health):
                rect = pygame.Rect(10 + i*30, 10, 20, 20)
                screen.blit(heart_image, rect)

            score_txt = font2.render(str(score), 1, BLACK)
            scorepos = score_txt.get_rect()
            scorepos.centerx = width - 50
            scorepos.centery = 20

            lvl_txt = font.render(str(level), 1, BLACK)
            lvlpos = lvl_txt.get_rect()
            lvlpos.centerx = width/2
            lvlpos.centery = 50

            screen.blit(score_txt, scorepos)
            screen.blit(lvl_txt, lvlpos)
        elif menu:
            screen.fill(WHITE)
            game_menu = pygame.image.load("images/menu.png")
            menu_rect = pygame.Rect(0, 0, 970, 620)
            screen.blit(game_menu, menu_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 2:
                        menu = False
                        play = True
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if 579 < mouse_pos[0] < 922:
                            if 180 < mouse_pos[1] < 260:
                                if score >= 5:
                                    score -= 5
                                    player.speed += 10
                            elif 318 < mouse_pos[1] < 400:
                                if score >= 1 and player.cooldown > 1:
                                    score -= 1
                                    player.cooldown -= 1
                            elif 466 < mouse_pos[1] < 547:
                                if score >= 2:
                                    score -= 2
                                    player.health += 1
        pygame.display.flip()
        clock.tick(60)

main()
