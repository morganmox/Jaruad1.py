import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCALE = 1.75

class Enemy(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)
        self.center_y = SCREEN_HEIGHT
        self.center_x = random.randrange(SCREEN_WIDTH)
        
    def update(self):
        self.center_y-=5
        if self.center_y<0:
            self.kill()

class Bullet(arcade.Sprite):
    def __init__(self,filename,scale):
        super().__init__(filename,scale)

    def update(self):
        self.center_y+=8
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
            self.center_y = 0
        if self.center_y<0:
            self.center_y = SCREEN_HEIGHT  

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
 
        arcade.set_background_color(arcade.color.BLACK)
        self.framecount = 0
        self.all_sprites_list = arcade.SpriteList()
        self.player_sprite = Ship("images/ship.png", SCALE)
        self.all_sprites_list.append(self.player_sprite)

    def on_draw(self):
        arcade.start_render()
        self.all_sprites_list.draw()

    def update(self,x):
        self.all_sprites_list.update()
        self.framecount+=1
        if self.framecount%30==0:
            self.framecount = 0
            self.enemy_sprite = Enemy("images/enemy.png", SCALE)
            self.all_sprites_list.append(self.enemy_sprite)
            
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.SPACE:
            bullet = Bullet("images/bullet.png",SCALE)
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top
            self.all_sprites_list.append(bullet)   
        if symbol == arcade.key.LEFT:
            self.player_sprite.vx = -1
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.vx = 1
        if symbol == arcade.key.UP:
            self.player_sprite.vy = 1
        elif symbol == arcade.key.DOWN:
            self.player_sprite.vy = -1
            
    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.player_sprite.vx = 0
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.vx = 0
        if symbol == arcade.key.UP:
            self.player_sprite.vy = 0
        elif symbol == arcade.key.DOWN:
            self.player_sprite.vy = 0            
 
if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
