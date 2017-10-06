import arcade
import random
#Must match with main program's setting for accurate display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCALE = 1.5

class EnemySubmarine(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.center_y = SCREEN_HEIGHT-random.randrange(200)-10
        self.center_x = SCREEN_WIDTH
        
    def update(self):
        self.center_x-=5
        if self.center_x<0:
            self.kill()

class Torpedo(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)

    def update(self):
        self.center_y-=10
        if self.center_y<0:
            self.kill()

class Enemy(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.center_y = SCREEN_HEIGHT
        self.center_x = random.randrange(SCREEN_WIDTH)
        
    def update(self):
        self.center_y-=8
        if self.center_y<0:
            self.kill()

class Bullet(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)

    def update(self):
        self.center_y+=10
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
