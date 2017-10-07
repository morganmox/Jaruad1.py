import arcade
import random
#Must match with main program's setting for accurate display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCALE = 1.4

class EnemyRed(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.center_y = SCREEN_HEIGHT
        self.center_x = SCREEN_WIDTH/2
        if random.randrange(2) == 0:
            self.dirx = 1
        else:
            self.dirx = -1

    def update(self):
        self.center_y-=2
        self.center_x+=self.dirx*4
        if self.center_x >SCREEN_WIDTH-50 or self.center_x <50 or random.randrange(100)<1:
            self.dirx*=-1

class Redbullet(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.vy = 2

    def update(self):
        self.vy+=1
        self.center_y-=self.vy
        if self.center_y<0:
            self.kill()

class EnemyAirforce(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.center_y = SCREEN_HEIGHT-random.randrange(SCREEN_HEIGHT/8)
        self.center_x = 0

    def update(self):
        self.center_y -= 9
        self.center_x += 7
        if self.center_x>SCREEN_WIDTH or self.center_y<0:
            self.kill()
   
class EnemySubmarine(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.center_y = SCREEN_HEIGHT-random.randrange(200)-20
        self.center_x = SCREEN_WIDTH
        
    def update(self):
        self.center_x-=random.randrange(15)
        if self.center_x<0:
            self.kill()

class Torpedo(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)

    def update(self):
        self.center_y-=7
        if self.center_y<0:
            self.kill()

class Enemy(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.center_y = SCREEN_HEIGHT
        self.center_x = random.randrange(SCREEN_WIDTH)
        self.vy = random.randrange(5)+5
        
    def update(self):
        self.center_y-=self.vy
        if self.center_y<0:
            self.kill()

class Bullet(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)

    def update(self):
        self.center_y+=11
        if self.center_y>SCREEN_HEIGHT:
            self.kill()

class Ship(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.center_x = SCREEN_WIDTH/2
        self.center_y = SCREEN_HEIGHT/2
        self.vx = 0
        self.vy = 0

    def update(self):
        self.center_x+=self.vx*5
        self.center_y+=self.vy*5

        if self.center_x>SCREEN_WIDTH:
            self.center_x = 0
        if self.center_x<0:
            self.center_x = SCREEN_WIDTH
        if self.center_y>SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT-25
        if self.center_y<0:
            self.center_y = 25

class Greenfoot(arcade.Sprite):#upgrades
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.center_x = random.randrange(SCREEN_WIDTH)
        self.center_y = random.randrange(SCREEN_HEIGHT)
        self.vx = random.randrange(7)+3
        self.vy = random.randrange(7)+3

    def update(self):
        self.center_x+=self.vx
        self.center_y+=self.vy
        if self.center_y>SCREEN_HEIGHT or self.center_y<0:
            self.vy*=-1
        if self.center_x>SCREEN_WIDTH or self.center_x<0:
            self.vx*=-1
