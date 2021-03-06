import arcade
import random
#ตรงนี้อย่าซน
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCALE = 1

class Funnel(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.vx = 0
        self.ran = 0
        self.center_x = SCREEN_WIDTH/2
        self.center_y = 50
    def update(self):
        self.center_x+=self.vx*6
        if random.randrange(10)<2:
            self.ran = random.randrange(5)
            if self.ran==0:
                self.vx = 0
            elif self.ran==1 or self.ran==2:
                self.vx = 1
            elif self.ran==3 or self.ran==4:
                self.vx = -1
        if self.center_x > SCREEN_WIDTH:
            self.center_x = 0
        if self.center_x < 0:
            self.center_x = SCREEN_WIDTH

class Hamtaro(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.center_x = random.randrange(SCREEN_WIDTH-30)+30
        self.center_y = SCREEN_HEIGHT
        self.randomstop = random.randrange(80)+80

    def update(self):
        if self.center_y > SCREEN_HEIGHT-self.randomstop:
            self.center_y-=2
            
class Seed(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        if random.randrange(2)==0:
            self.vx = 6
        else:
            self.vx = -6

    def update(self):
        self.center_y-=2
        self.center_x+=self.vx
        if self.center_x>SCREEN_WIDTH or self.center_x<0:
            self.vx*=-1
        if self.center_y<0:
            self.kill()
        
class Falcon(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.center_y = SCREEN_HEIGHT
        self.center_x = random.randrange(SCREEN_WIDTH-25)+25
        
    def update(self):
        self.center_y-=12
        if self.center_y<0:
            self.kill()

class Falconbullet(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        
    def update(self):
        self.center_y-=18
        if self.center_y<0:
            self.kill()

class Stealth(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.center_y = SCREEN_HEIGHT
        self.center_x = random.randrange(SCREEN_WIDTH-25)+25
        self.vy = 25
        
    def update(self):
        if self.vy>=4:
            self.vy-=1
        self.center_y-=self.vy
        if self.center_y<0:
            self.kill()

class EnemyBlue(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.initpos = "top"
        if random.randrange(2)==0:
            self.initpos = "bottom"
            self.center_y = 0
            self.angle = 180
        else:
            self.center_y = SCREEN_HEIGHT
        self.center_x = random.randrange(SCREEN_WIDTH-40)+40

    def update(self):
        if self.initpos == "top":
            self.center_y -=2
            if self.center_y<0:
                self.kill()
        else:
            self.center_y +=2
            if self.center_y>SCREEN_HEIGHT:
                self.kill()

class BOSS(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.center_x = SCREEN_WIDTH/2
        self.center_y = SCREEN_HEIGHT
        self.vx = 3

    def update(self):
        if self.center_y > SCREEN_HEIGHT-120:
            self.center_y-=1
        else:
            self.center_x +=self.vx
            if self.center_x >SCREEN_WIDTH-60 or self.center_x <60 or random.randrange(100)<1:
                self.vx*=-1     

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
        self.center_y-=1
        self.center_x+=self.dirx*3
        if self.center_x >SCREEN_WIDTH-50 or self.center_x <50 or random.randrange(100)<1:
            self.dirx*=-1
        if self.center_y<0:
            self.kill()

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
        if random.randrange(2)==0:
            self.initleft = True
        else:
            self.initleft = False
        self.center_y = random.randrange(SCREEN_HEIGHT*3/4)+30
        self.vx = 0
        if self.initleft == True:
            self.center_x = 0
        else:
            self.center_x = SCREEN_WIDTH
            self.angle = 180

    def update(self):
        if random.randrange(5)==0:
            if self.initleft == True:
                self.vx+=1
            else:
                self.vx-=1
        self.center_x += self.vx
        if self.initleft == True:
            if self.center_x > SCREEN_WIDTH:
                self.kill()
        else:
            if self.center_x < 0:
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
        self.center_x = random.randrange(SCREEN_WIDTH-5)+5
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
        self.center_y = 100
        self.vx = 0
        self.vy = 0

    def update(self):
        self.center_x+=self.vx*7
        self.center_y+=self.vy*7

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
