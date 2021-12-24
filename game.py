import pygame, random
from pygame.locals import*
#from pre_game import*
   
size = [400, 500]
screen = pygame.display.set_mode(size)
ship = pygame.image.load("GalagaSprite.jpg")
top_ship = screen.get_height() - ship.get_height()/2
left_ship = screen.get_width()/2 - ship.get_width()/6
ship = pygame.transform.scale(ship,(30, 30))
ship_x = screen.get_width()/2 - ship.get_width()/6
RIGHT = "right"
LEFT = "left"
fire = pygame.image.load("fire.jpg")
words = pygame.font.SysFont("Emulogic", 14)
lives = 3
lvl_count = 1
frame_rate = 60
frame_count = 0
exp_fc = 0
self_hit_lis = pygame.sprite.Group()
ship_pos = [left_ship, top_ship]
#other variables imported from pre_game
pygame.init()
grunt1_pos = []
grunt2_pos = []
enemy3_pos = []
f_c = 0
D_fc = 0
movement_fc = 0
win_count = 0
pygame.mixer.init()
enemy_is_kill_sound = pygame.mixer.Sound("enemy_is_kil.ogg")
shooting_sound = pygame.mixer.Sound("firing_sound.ogg")
self_death = pygame.mixer.Sound("level_start.ogg")

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.ships_kill = 0
        self.text_color = (red)
        self.font = pygame.font.SysFont('Emulogic', 14)
        self.x_score_position, self.y_score_position = 10.0, 20.0
    def prep_scores(self):
        self.score_string = str(self.ships_kill)
        self.score_image = self.font.render(self.score_string, True, self.text_color)
 
    def blitme(self):
        # Turn individual scoring elements into images that can be drawn
        self.prep_scores()
        # Draw individual scoring elements
        self.screen.blit(self.score_image, (self.x_score_position, self.y_score_position))

def load_image(name, size):
    image = pygame.image.load(name)
    image = pygame.transform.scale(image, size)
    return image

class FIRE(pygame.sprite.Sprite):
    image = None
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if FIRE.image is None:
            FIRE.image = pygame.image.load("fire.jpg")
        self.image = FIRE.image
        self.image = pygame.transform.scale(fire,(4, 15))
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.y -= 10

class enemy_fire(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("enemy_fire.png", (4, 15))
        self.rect = self.image.get_rect()
        
    def update(self):
        if lvl_count == 1:
            self.rect.y += 4
        elif lvl_count == 2:
            self.rect.y += 6
        elif lvl_count == 3:
            self.rect.y += 10
        elif lvl_count == 4:
            self.rect.y += 14
        elif lvl_count == 5:
            self.rect.y += 16
        
enemy_lis = pygame.sprite.Group()
bullet_lis = pygame.sprite.Group()
all_sprites_lis = pygame.sprite.Group()
hit_list = pygame.sprite.Group()
fire_lis = pygame.sprite.Group()
player_lis = pygame.sprite.Group()
grunt_1 = pygame.sprite.Group()
grunt_2 = pygame.sprite.Group()
enemy_3 = pygame.sprite.Group()
SHOTS_hit= pygame.sprite.Group()
SHOTS_missed = pygame.sprite.Group()
SHOTS_fired = pygame.sprite.Group()                

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        global ship_pos
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("GalagaSprite.jpg", (30, 30))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x = ship_pos[0]
        self.rect.y = ship_pos[1]
             
    def move_right(self):
        global ship_pos, all_sprites_lis
        ship_pos = [ship_pos[0]+5, top_ship]
        if (ship_pos[0] > screen.get_width() - 32):
            ship_pos[0] -= 5

    def move_left(self):
        global ship_pos, all_sprites_lis
        ship_pos = [ship_pos[0]-5, top_ship]
        if (ship_pos[0] < 0):
            ship_pos[0] += 5
            
#initialize player sprite            
player = Player()
all_sprites_lis.add(player)
player_lis.add(player)

class Grunt_1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(load_image("enemy1.png", (30, 28)))
        self.images.append(load_image("enemy1_alt.png", (29, 27)))
        self.images.append(load_image("exp.png", (30, 30)))
        self.images.append(load_image("exp2.png", (30, 30)))
        self.images.append(load_image("exp3.png", (30, 30)))
        self.images.append(load_image("exp4.png", (30, 30)))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
                                  
    def update(self):
        global frame_count, frame_rate
        seconds = frame_count // frame_rate
        frame_count += 1
        if 0 < seconds <= 1:
            self.index += 1
            if self.index >= 2:
                self.index = 0
            self.image = self.images[self.index]
            frame_count = 0

    def fire(self):
        global grunt1_pos
        fire = enemy_fire()
        b = len(grunt1_pos)
        #if all enemies of type are kill
        if b == 0:
            return None
        num = random.randrange(b)
        fire.rect.x = grunt1_pos[num][0] + 13
        fire.rect.y = grunt1_pos[num][1]
        all_sprites_lis.add(fire)
        fire_lis.add(fire) 
        

class Grunt_2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(load_image("enemy2.png", (30, 28)))
        self.images.append(load_image("enemy2_alt.png", (29, 27)))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def update(self):
        global frame_count, frame_rate
        seconds = frame_count // frame_rate
        frame_count += 1
        if 0 < seconds <= 1:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            frame_count = 0

    def fire(self):
        global grunt2_pos
        fire = enemy_fire()
        b = len(grunt2_pos)
        #error if all enemies dead
        if b == 0:
            return None
        num = random.randrange(b)
        fire.rect.x = grunt2_pos[num][0] + 13
        fire.rect.y = grunt2_pos[num][1]
        all_sprites_lis.add(fire)
        fire_lis.add(fire)   

class Enemy_3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(load_image(("enemy4.png"), (32, 30)))
        self.images.append(load_image(("enemy4_alt.png"), (31, 29)))
        self.images.append(load_image(("enemy3.png"), (30, 30)))
        self.images.append(load_image(("enemy3_alt.png"), (29, 29)))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        
    def update(self):
        global frame_count, frame_rate
        movement_fc = 0
        seconds = frame_count // frame_rate
        secs = movement_fc // frame_rate
        frame_count += 1
        if 0 < seconds <= 1:
            self.index += 1
            if self.index >= 2:
                self.index = 0
            self.image = self.images[self.index]
            frame_count = 0
        # enemy shoot
    
    def fire(self):
        global enemy3_pos
        fire = enemy_fire()
        b = len(enemy3_pos)
        #error if all enemies dead
        if b == 0:
            return None
        num = random.randrange(b)
        fire.rect.x = enemy3_pos[num][0] + 13
        fire.rect.y = enemy3_pos[num][1]
        all_sprites_lis.add(fire)
        fire_lis.add(fire)         
            
        
def find_index(lis, location):
    c = -1
    for item in lis:
        c += 1
        if item == location:
            return c
        else:
            None
            
#For the sake of randomization of enemy fire seperate _is_kill functions
#Probably could have been done better..
 #Removes enemy from lis so its position is no longer available in randomizer
def Grunt1_is_kill():
    global bullet_lis, hit_list, all_sprites_lis, grunt1_pos
    for bullet in bullet_lis:
        hit_list = pygame.sprite.spritecollide(bullet, grunt_1, True)
        for enemy in hit_list:
            a = find_index(grunt1_pos,(enemy.rect.x, enemy.rect.y))
            grunt1_pos.pop(a)
            enemy_is_kill_sound.play()
            SHOTS_hit.add(bullet)
            SHOTS_fired.add(bullet)
            bullet_lis.remove(bullet)
            all_sprites_lis.remove(bullet)
            scoreboard.ships_kill += 100
        if bullet.rect.y < 0:
            SHOTS_fired.add(bullet)
            SHOTS_missed.add(bullet)
            bullet_lis.remove(bullet)
            all_sprites_lis.remove(bullet)

def Grunt2_is_kill():
    global bullet_lis, hit_list, all_sprites_lis, grunt2_pos
    for bullet in bullet_lis:
        hit_list = pygame.sprite.spritecollide(bullet, grunt_2, True)
        for enemy in hit_list:
            a = find_index(grunt2_pos,(enemy.rect.x, enemy.rect.y))
            grunt2_pos.pop(a)
            enemy_is_kill_sound.play()
            SHOTS_hit.add(bullet)
            SHOTS_fired.add(bullet)
            bullet_lis.remove(bullet)
            all_sprites_lis.remove(bullet)
            scoreboard.ships_kill += 100
        if bullet.rect.y < 0:
            SHOTS_fired.add(bullet)
            SHOTS_missed.add(bullet)
            bullet_lis.remove(bullet)
            all_sprites_lis.remove(bullet)

            
def enemy3_is_kill():
    global bullet_lis, hit_list, all_sprites_lis, enemy3_pos
    for bullet in bullet_lis:
        hit_list = pygame.sprite.spritecollide(bullet, enemy_3, True)
        for enemy in hit_list:
            a = find_index(enemy3_pos,(enemy.rect.x, enemy.rect.y))
            enemy3_pos.pop(a)
            enemy_is_kill_sound.play()
            SHOTS_hit.add(bullet)
            SHOTS_fired.add(bullet)
            bullet_lis.remove(bullet)
            all_sprites_lis.remove(bullet)
            scoreboard.ships_kill += 100
        if bullet.rect.y < 0:
            SHOTS_fired.add(bullet)
            SHOTS_missed.add(bullet)
            bullet_lis.remove(bullet)
            all_sprites_lis.remove(bullet)
        

def death_situation():
    global player_lis, words, D_fc, lives
    if len(player_lis) == 0:
        frame_rate = 3.0
        secs = D_fc // frame_rate
        D_fc += 1
        if lives == 2 or lives == 1:
            death = words.render("GET READY!", True, yellow)
            screen.blit(death,(screen.get_width()/3+20, screen.get_height()/2))
        if (secs > 50) and lives > 0:
            all_sprites_lis.add(player)
            player_lis.add(player)
            D_fc = 0
            return True
           
def self_is_kill():
    global lives
    for shot_fired in fire_lis:
        self_hit_lis = pygame.sprite.spritecollide(shot_fired, player_lis, True)
        for self in self_hit_lis:
            fire_lis.remove(shot_fired)
            all_sprites_lis.remove(shot_fired)
            lives -= 1
        if shot_fired.rect.y > 500:
            fire_lis.remove(shot_fired)
            all_sprites_lis.remove(shot_fired)


def draw_grunt_1():
    global lvl_count, grunt1_pos
    for i in range(120, 180, 30):
        for j in range(55, 355, 30):
            enemy = Grunt_1()
            enemy.rect.x = j 
            enemy.rect.y = i
            grunt1_pos.append((enemy.rect.x, enemy.rect.y))
            all_sprites_lis.add(enemy)
            grunt_1.add(enemy)
            enemy_lis.add(enemy)

def draw_grunt_2():
    global lvl_count, grunt2_pos
    for i in range(60, 120, 30):
        for j in range(85, 325, 30):
            enemy = Grunt_2()      
            enemy.rect.x = j 
            enemy.rect.y = i
            grunt2_pos.append((enemy.rect.x, enemy.rect.y))
            all_sprites_lis.add(enemy)
            grunt_2.add(enemy)
            enemy_lis.add(enemy)
            

def draw_enemy_3():
    global lvl_count, enemy3_pos
    for i in range(30, 60, 30):
        for j in range(125, 285, 40):
            enemy = Enemy_3()      
            enemy.rect.x = j 
            enemy.rect.y = i
            enemy3_pos.append((enemy.rect.x, enemy.rect.y))
            all_sprites_lis.add(enemy)
            enemy_3.add(enemy)
            enemy_lis.add(enemy)       

def draw_grunts():
    draw_grunt_1()
    draw_grunt_2()
    draw_enemy_3()
   
 
draw_grunts()      
             
def lvl_display():
    global lvl_count
    lvl = pygame.image.load("lvl1-4.jpg")
    lvl = pygame.transform.scale(lvl,(25,30))
    lvl5 = pygame.image.load("lvl5.jpg")
    lvl5 = pygame.transform.scale(lvl5,(25, 30))
    if lvl_count == 1:
        # 375, 470
        screen.blit(lvl,(screen.get_width() - 25, screen.get_height() - 30))
    if lvl_count == 2:
        #350, 470
        screen.blit(lvl,(screen.get_width() - 25, screen.get_height() - 30))
        screen.blit(lvl,(screen.get_width() - 50, screen.get_height() - 30))
    if lvl_count == 3:
        screen.blit(lvl,(screen.get_width() - 25, screen.get_height() - 30))
        screen.blit(lvl,(screen.get_width() - 50, screen.get_height() - 30))
        screen.blit(lvl,(screen.get_width() - 75, screen.get_height() - 30))
    if lvl_count == 4:
        screen.blit(lvl,(screen.get_width() - 25, screen.get_height() - 30))
        screen.blit(lvl,(screen.get_width() - 50, screen.get_height() - 30))
        screen.blit(lvl,(screen.get_width() - 75, screen.get_height() - 30))
        screen.blit(lvl,(screen.get_width() - 100, screen.get_height() - 30))
    if lvl_count == 5:
        screen.blit(lvl5,(screen.get_width() - 25, screen.get_height() - 30))

#I have a lot of these random variables for counting time
C = 0       
def lives_display():
    global ship, lives, words, done, C
    if lives == 3:
        screen.blit(ship,(0, 470))
        screen.blit(ship,(30, 470))
    if lives == 2:
        screen.blit(ship,(0, 470))
    if lives == 0:
        frame_rate = 3.0
        secs = C // frame_rate
        C += 1
        if 1 < secs < 40:
            death = words.render("GAME OVER", True, yellow)
            screen.blit(death,(screen.get_width()/3+20, screen.get_height()/2))
        if secs > 55:
            HIT = int((((len(SHOTS_hit))/float(len(SHOTS_fired))*100)) - ((len(SHOTS_hit))/float(len(SHOTS_fired)) *100)%1)
            results = words.render("-RESULTS-", True, red)
            shots = words.render("SHOTS FIRED: %s" % (len(SHOTS_fired)), \
                                 True, yellow)
            hits = words.render("NUMBER OF HITS: %s" % (len(SHOTS_hit)), \
                                True, yellow)
            ratio = words.render("HIT MISS RATIO: %s %s" % ("%", HIT), True, yellow)
            screen.blit(results,(screen.get_width()/3, screen.get_height()/2))
            screen.blit(shots,(screen.get_width()/6, screen.get_height()/2+30))
            screen.blit(hits,(screen.get_width()/6, screen.get_height()/2+60))
            screen.blit(ratio,(screen.get_width()/6, screen.get_height()/2+90))
    

def misc_display():
    global score, lvl_count, words
    text = words.render("1UP", True, red)
    screen.blit(text, (10, 4))
    if len(enemy_lis) == 0 and lvl_count == 1:
        s_2 = words.render("STAGE 2", True, yellow)
        screen.blit(s_2,(screen.get_width()/3-20, screen.get_height()/2))
    if len(enemy_lis) == 0 and lvl_count == 2:
        s_3 = words.render("STAGE 3", True, yellow)
        screen.blit(s_3,(screen.get_width()/3-20, screen.get_height()/2))
    if len(enemy_lis) == 0 and lvl_count == 3:
        s_4 = words.render("STAGE 4", True, yellow)
        screen.blit(s_4,(screen.get_width()/3-20, screen.get_height()/2))
    if len(enemy_lis) == 0 and lvl_count == 4:
        s_5 = words.render("STAGE 5", True, yellow)
        screen.blit(s_5,(screen.get_width()/3-20, screen.get_height()/2))
    if len(enemy_lis) == 0 and lvl_count == 5:
        win = words.render("YOU WIN", True, yellow)
        screen.blit(win,(screen.get_width()/3+20, screen.get_height()/2))    
        


def fire_event_three():
    global f_c
    frame_rate = 3.0
    seconds = f_c // frame_rate
    f_c += 1
    if  seconds%30 == 0:
        Enemy_3().fire()

def fire_event_one():
    global f_c
    frame_rate = 3.0
    seconds = f_c // frame_rate
    f_c += 1
    if  seconds%100 == 0:
        Grunt_1().fire()

def fire_event_two():
    global f_c
    frame_rate = 3.0
    seconds = f_c // frame_rate
    f_c += 1
    if  seconds%200 == 0:
        Grunt_2().fire()

def fire_events():
    fire_event_one()
    fire_event_two()
    fire_event_three()

    
pygame.key.set_repeat(10, 25)    
scoreboard = Scoreboard(screen)
#Double-Click to start game
#Click after you beat a level to continue
#pre_game()
lives_fc = 0
while done == False:
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYUP:
            #won't allow player to fire if death_situation
            if event.key == K_SPACE and len(player_lis) == 1:
                bullet = FIRE()
                bullet.rect.x = ship_pos[0] + 13
                bullet.rect.y = top_ship
                bullet_lis.add(bullet)
                all_sprites_lis.add(bullet)
                shooting_sound.play()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(enemy_lis) == 0:
                lvl_count += 1
                if lvl_count == 2:
                    draw_grunts()
                if lvl_count == 3:
                    draw_grunts()
                if lvl_count == 4:
                    draw_grunts()
                if lvl_count == 5:
                    draw_grunts()
   
    keys = pygame.key.get_pressed()
    enemy3_is_kill()
    Grunt2_is_kill()
    Grunt1_is_kill()
    self_is_kill()
    #moves player object
    if (keys[K_RIGHT]):
        player.move_right()
    elif (keys[K_LEFT]):
        player.move_left()
       
    screen.fill(black)
    lives_display()

    #Enemies will stop firing in death_situation
    if len(player_lis) == 1:
        fire_events()
        
    if lives == 0:
        #not actually seconds, but..yeah
        frame_rate = 3.0
        secs = lives_fc // frame_rate
        lives_fc += 1
        if secs > 180:
            done = True
    
    if len(enemy_lis) == 0 and lvl_count == 5:
        #none of my timer variables are seconds
        frame_rate = 3.0
        seconds = win_count // frame_rate
        win_count += 1
        if seconds > 30:
            done = True
            
    death_situation()
    bullet_lis.update()
    scoreboard.blitme()
    #function imported from pre_game()
    #pygame.display.set_caption("GALAGA")
    #Sprites
    stars()  
    lvl_display()
    misc_display()
    all_sprites_lis.update()
    all_sprites_lis.draw(screen)
    pygame.display.flip()

pygame.quit()

