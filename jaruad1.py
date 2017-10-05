import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCALE = 1

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

        super().update()

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
 
        arcade.set_background_color(arcade.color.BLACK)
        self.all_sprites_list = arcade.SpriteList()
        self.player_sprite = Ship("images/ship.png", SCALE)
        self.all_sprites_list.append(self.player_sprite)

    def on_draw(self):
        arcade.start_render()
        self.all_sprites_list.draw()

    def update(self,x):
        self.all_sprites_list.update()

    def on_key_press(self, symbol, modifiers):
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
