from pygame import *
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed, size_x,size_y):
        super(). __init__()
        self.image=transform.scale(image.load(player_image),(size_x,size_y))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def recet(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Bullet_2(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Bullet_1(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
class First(GameSprite):
    def update_f(self):

        key_pressed=key.get_pressed()

        if key_pressed[K_w] and self.rect.y < 210:
            self.rect.y += self.speed
        if key_pressed[K_s] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 660:
            self.rect.x += self.speed
    def fire(self):          
        bullet_1=Bullet_1('bullet_2.png', self.rect.centerx, self.rect.top, -15, 15, 20 ) 
        bullets_1.add(bullet_1)

class Second(GameSprite):
    def update_s(self):

        key_pressed=key.get_pressed()

        if key_pressed[K_UP] and self.rect.y > 220:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y < 455:
            self.rect.y += self.speed
        if key_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 660:
            self.rect.x += self.speed
    def fire(self):          
        bullet_2=Bullet_2('bullet.png', self.rect.centerx, self.rect.top, -15, 15, 20 ) 
        bullets_2.add(bullet_2)
          
window=display.set_mode((700,500))
display.set_caption('Танчики')
background=transform.scale(image.load('background.jpg'), (700,500))
bullets_1=sprite.Group()
bullets_2=sprite.Group()  

num_fire_1=0
num_fire_2=0
rel_time_1=False #флаг, отвечающий за перезарядку
rel_time_2=False #флаг, отвечающий за перезарядку

game=True
finish=False

clock=time.Clock()
FPS=60

tank_1=First('танк1.png',300,50,3,40,40)
tank_2=Second('танк2.png',300,350,3,40,40)

font.init()
font2 = font.SysFont('Arial', 70)
font3 = font.SysFont('Arial', 30)

win1=font2.render('YELLOW WIN!', True, (225,215,0))
win2=font2.render('GREEN WIN!', True, (225,215,0))

health_1 = 0
health_2 = 0

while game:
    if finish == False:
        window.blit(background, (0,0))
        tank_1.update_f()
        tank_2.update_s()
        tank_1.recet()
        tank_2.recet()    
        bullets_1.update()
        bullets_2.update()
        
        if rel_time_1 == True:
            end_time=timer()
            if end_time - start_time <3:
                reload = font3.render('wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260,460))
        else:
            num_fire_1=0
            rel_time_1=False 

        if sprite.spritecollide(tank_1, bullets_2, True) :
            health_1 += 1
            if health_1 == 3:
                window.blit(win2, (200,200))
                finish = True

        if sprite.spritecollide(tank_2, bullets_1, True) :
            health_2 += 1
            if health_2 == 3:
                window.blit(win1, (200,200))
                finish = True
    else:
        finish = False
        num_fire_1=0
        num_fire_2=0
        rel_time_1=False
        rel_time_2=False

        health_1=0
        health_2=0
        for b in bullets_1:
            b.kill()
        for m in bullets_2:
            m.kill()
        
        time.delay(3000)
    for e in event.get():                
        if e.type == QUIT:
            game=False
        if e.type == KEYDOWN: 
            if e.key == K_SPACE:
                tank_2.fire()        
            if e.key == K_x:

                if num_fire_1 < 3 and rel_time_1 == False:
                    tank_1.fire() 
                    num_fire_1 += 1
                if num_fire_1 >= 3 and rel_time_1 == False:
                    start_time=timer()
                    rel_time_1=True
                    
    bullets_1.draw(window)
    bullets_2.draw(window)                                         
    clock.tick(FPS)
    display.update()