#### VERSION 1.2 ####
from Buttons import Button
from Text import Text
import pygame
import random
import time
import math

pygame.mixer.pre_init(22050,-16, 2, 1024)
pygame.init()

# Display
WIDTH = 800
HEIGHT = 600
CENTER_X = int(WIDTH/2)
CENTER_Y = int(HEIGHT/2)
display = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Zombie Survival")
BACKGROUND = pygame.image.load("Background.png").convert()
LOSE_BACKGROUND = pygame.image.load("RIP.png").convert()
ICON = pygame.image.load('icon.png')
pygame.display.set_icon(ICON)
frame = pygame.time.Clock()
FPS = 120
window_size_checker = []

# Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,200,0)
DARK_GREEN = (0,200,0)
BLUE = (0,0,255)
YELLOW = (225,225,0)
TURQUOISE = (0,255,255)
PINK = (255,0,255)

# Fonts
TITLE = pygame.font.SysFont("AgencyFB", 100)
TEXT = pygame.font.SysFont("Arial", 50)
SMALL = pygame.font.SysFont("Arial", 25)

# Sounds
gunshot = pygame.mixer.Sound("gunshot.wav")
lose_sound = pygame.mixer.Sound("lose_sound.wav")

class Player(pygame.sprite.Sprite):
    """Player Class"""
    def __init__(self,x,y,enemies,wave,colour):
        self.x = x
        self.y = y
        self.colour = colour
        self.wave = wave
        self.enemies = enemies

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def next_wave(self):
        self.wave += 1

    def update(self):
        
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self, enemy):
                self.enemies.remove(enemy)
                enemy.kill()
                self.kill()
                lose_screen(self.wave)
                
        if self.x > 800:
            self.x = 800
        elif self.x < 0:
            self.x = 0

        if self.y > 600:
            self.y = 600
        elif self.y < 0:
            self.y = 0

        self.rect.center = (self.x,self.y)

class Enemy(pygame.sprite.Sprite):
    """Enemy Class"""
    def __init__(self,x,y,speed,player):
        self.x = x
        self.y = y
        self.speed = speed
        self.target = player
        
        pygame.sprite.Sprite.__init__(self)
        size = 50/self.speed
        self.image = pygame.Surface((size,size))
        colour = random.randint(145,255)
        colour = (colour,0,0)
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        

    def update(self):       
        dest_x,dest_y = self.target.x, self.target.y
        x_diff = dest_x - self.x
        y_diff = dest_y - self.y
        angle = math.atan2(y_diff, x_diff)
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

        self.x += self.change_x
        self.y += self.change_y
            
        self.rect.center = (self.x, self.y)

class AI(pygame.sprite.Sprite):
    """AI Class"""
    def __init__(self,x,y,enemies,wave):
        self.x = x
        self.y = y
        self.wave = wave
        self.enemies = enemies
        self.ultra = False

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def next_wave(self):
        self.wave += 1

    def update(self):
        distances = []
        
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self, enemy):
                self.enemies.remove(enemy)
                enemy.kill()
                self.kill()
                lose_screen(self.wave)

            distance_x = abs(self.x-enemy.x)
            distance_y = abs(self.y-enemy.y)
            distance = math.sqrt((distance_x**2)+(distance_y**2))
            distances.append(distance)
            
        try:
            index = distances.index(min(distances))
            self.target = self.enemies[index]
            if min(distances) < 100:
                self.ultra = True
        except:
            pass
        
        self.rect.center = (self.x,self.y)

class AI_Bullet(pygame.sprite.Sprite):
    """AI Bullet Class"""
    def __init__(self,px,py,dest_x,dest_y,enemies):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (px, py)
        self.enemies = enemies
        self.x = px
        self.y = py

        x_diff = dest_x - px
        y_diff = dest_y - py
        angle = math.atan2(y_diff, x_diff)
        self.change_x = math.cos(angle) * 10
        self.change_y = math.sin(angle) * 10

    def update(self):
        self.x += self.change_x
        self.y += self.change_y

        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self, enemy):
                self.enemies.remove(enemy)
                enemy.kill()
                self.kill()
    
        if self.x > 800 or self.x < 0:
            self.kill()
        elif self.y > 600 or self.y < 0:
            self.kill()
            
        self.rect.center = (self.x, self.y)

class Bullet(pygame.sprite.Sprite):
    """Bullet Class"""
    def __init__(self,px,py,enemies):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (px, py)
        self.enemies = enemies
        self.x = px
        self.y = py

        dest_x,dest_y =  pygame.mouse.get_pos()
        x_diff = dest_x - px
        y_diff = dest_y - py
        angle = math.atan2(y_diff, x_diff)
        self.change_x = math.cos(angle) * 10
        self.change_y = math.sin(angle) * 10

    def update(self):
        self.x += self.change_x
        self.y += self.change_y

        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self, enemy):
                self.enemies.remove(enemy)
                enemy.kill()
                self.kill()
    
        if self.x > 800 or self.x < 0:
            self.kill()
        elif self.y > 600 or self.y < 0:
            self.kill()
            
        self.rect.center = (self.x, self.y)

def menu():
    display.fill(BLACK)
    title_text = "Zombie survival"
    title = Text(display,CENTER_X,CENTER_Y-100,title_text,TITLE,RED)
    x = CENTER_X-350
    y = CENTER_Y
    start_button = Button(display,x,y,200,100,"PLAY",TEXT,GREEN,WHITE)
    x = CENTER_X-100
    start_button2 = Button(display,x,y,200,100,"AI",TEXT,BLUE,WHITE)
    x = CENTER_X+150
    quit_button = Button(display,x,y,200,100,"QUIT",TEXT,RED,WHITE)
    y = CENTER_Y+110
    x = CENTER_X-250
    fullscreen_button = Button(display,x,y,500,100,"TOGGLE FULLSCREEN",TEXT,BLACK,WHITE)

    pygame.mixer.music.load("menu_theme.mp3")
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.clicked():
                    pygame.mixer.music.stop()
                    return play()
                elif start_button2.clicked():
                    pygame.mixer.music.stop()
                    return ai_play()
                elif fullscreen_button.clicked():
                    return screen()
                elif quit_button.clicked():
                    pygame.quit()
                    quit()

        pygame.display.flip()

def lose_screen(wave_number):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(lose_sound)
    display.blit(LOSE_BACKGROUND, [0,0])
    title_text = "YOU DIED"
    title = Text(display,CENTER_X,CENTER_Y-200,title_text,TITLE,RED)
    wave_text = "You Got To Wave: "+str(wave_number)
    wave = Text(display,CENTER_X,CENTER_Y-100,wave_text,TITLE,RED)
    x = CENTER_X-225
    y = CENTER_Y
    start_button = Button(display,x,y,200,100,"MENU",TEXT,GREEN,WHITE)
    x = CENTER_X
    quit_button = Button(display,x,y,200,100,"QUIT",TEXT,RED,WHITE)

    pygame.mixer.music.load("menu_theme.mp3")
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.clicked():
                    pygame.mixer.music.stop()
                    menu()
                elif quit_button.clicked():
                    pygame.quit()
                    quit()

        pygame.display.flip()

def enemy_spawn():
    area = random.randint(1,4)
    if area == 1:
        x = -random.randint(0,300)
        y = random.randint(0,600)
    elif area == 2:
        x = random.randint(0,800)
        y = random.randint(600,900)
    elif area == 3:
        x = random.randint(800,1100)
        y = random.randint(0,600)
    else:
        x = random.randint(0,800)
        y = -random.randint(0,300)
    return x,y

def screen():
    window_size_checker.append(0)
    if len(window_size_checker)%2 != 0:
        display = pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN)
    else:
        display = pygame.display.set_mode((WIDTH,HEIGHT))
    menu()

def play():
    enemies = []
    wave_number = 0
    kill_number = 0
    player = Player(400,300,enemies,wave_number,GREEN)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    number_of_enemies = 1
    legacy_enemies = -1
    move_speed = 3
    y_move = 0
    x_move = 0

    wave_text = "Wave: "+str(wave_number)
    kills_text = "Kills: "+str(kill_number)
    wave = Text(display,725,25,wave_text,SMALL,DARK_GREEN)
    kills = Text(display,725,50,kills_text,SMALL,DARK_GREEN)
    
    pygame.mixer.music.load("zombie_sound.wav")
    pygame.mixer.music.play(-1)
    
    while True:

        # Event Handing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(gunshot)
                bullet = Bullet(player.x,player.y,enemies)
                all_sprites.add(bullet)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    x_move = 0
                    y_move = -move_speed
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    x_move = 0
                    y_move = move_speed
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    y_move = 0
                    x_move = -move_speed
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    y_move = 0
                    x_move = move_speed
                elif event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    menu()
        
            elif event.type == pygame.KEYUP:
                x_move = 0
                y_move = 0

        # Logic
        display.blit(BACKGROUND, [0,0])
        player.y += y_move
        player.x += x_move

        if len(enemies) == 0:
            legacy_enemies += number_of_enemies
            wave_number += 1
            player.next_wave()
            wave_text = "Wave: "+str(wave_number)
            wave.update(wave_text)
            number_of_enemies += 1
            for i in range(number_of_enemies):
                x,y = enemy_spawn()
                enemy = Enemy(x,y,random.uniform(0.5,2),player)
                all_sprites.add(enemy)
                enemies.append(enemy)

        kill_number = (number_of_enemies+legacy_enemies) - len(enemies)
        kills_text = "Kills: "+str(kill_number)

        all_sprites.update()
        all_sprites.draw(display)

        kills.update(kills_text)
        wave.update(wave_text)

        pygame.display.update()
        frame.tick(FPS)

def ai_play():
    enemies = []
    wave_number = 0
    kill_number = 0
    reload = 0
    number_of_enemies = 1
    legacy_enemies = -1

    ai = AI(400,300,enemies,wave_number)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(ai)

    wave_text = "Wave: "+str(wave_number)
    kills_text = "Kills: "+str(kill_number)
    wave = Text(display,725,25,wave_text,SMALL,DARK_GREEN)
    kills = Text(display,725,50,kills_text,SMALL,DARK_GREEN)
    pygame.mixer.music.load("zombie_sound.wav")
    pygame.mixer.music.play(-1)

    while True:

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    menu()

        display.blit(BACKGROUND, [0,0])

        if len(enemies) == 0:
            legacy_enemies += number_of_enemies
            wave_number += 1
            ai.next_wave()
            wave_text = "Wave: "+str(wave_number)
            wave.update(wave_text)
            number_of_enemies += 1
            for i in range(number_of_enemies):
                x,y = enemy_spawn()
                enemy = Enemy(x,y,random.uniform(0.5,2),ai)
                all_sprites.add(enemy)
                enemies.append(enemy)

        # Logic
        all_sprites.update()
        if ai.ultra == True:
            ai.ultra = False
            bullet = AI_Bullet(ai.x,ai.y,ai.target.x,ai.target.y,enemies)
            all_sprites.add(bullet)
            
        elif reload > 10:
            reload = 0
            if int(ai.target.x) in range(0,800) and int(ai.target.y) in range(0,600):
                pygame.mixer.Sound.play(gunshot)
                bullet = AI_Bullet(ai.x,ai.y,ai.target.x,ai.target.y,enemies)
                all_sprites.add(bullet)

        kill_number = (number_of_enemies+legacy_enemies) - len(enemies)
        kills_text = "Kills: "+str(kill_number)
        kills.update(kills_text)

        wave.update(wave_text)            
        all_sprites.draw(display)

        reload += 1
        pygame.display.update()
        frame.tick(FPS)

menu()
        

