import arcade
 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.BLACK)

        self.v_x = 0
        self.v_y = 0
        self.ship = arcade.Sprite('images/ship.png')
        self.ship.set_position(400,400)
 
    def on_draw(self):
        arcade.start_render()
        self.ship.draw()

    def on_key_press(self, symbol, modifiers):
        ship = self.ship
        if symbol == arcade.key.LEFT:
            self.v_x=-1
        if symbol == arcade.key.RIGHT:
            self.v_x=1
        if symbol == arcade.key.UP:
            self.v_y=1
        if symbol == arcade.key.DOWN:
            self.v_y=-1
            
    def on_key_release(self, symbol, modifiers):
        ship = self.ship
        if symbol == arcade.key.LEFT:
            self.v_x=0
        if symbol == arcade.key.RIGHT:
            self.v_x=0
        if symbol == arcade.key.UP:
            self.v_y=0
        if symbol == arcade.key.DOWN:
            self.v_y=0
        
    def update(self, delta):
        ship = self.ship
        ship.set_position(ship.center_x+(self.v_x*5), ship.center_y+(self.v_y*5))        
        if ship.center_y > SCREEN_HEIGHT:
            ship.center_y = 0
        if ship.center_y < 0:
            ship.center_y = SCREEN_HEIGHT
        if ship.center_x > SCREEN_WIDTH:
            ship.center_x = 0
        if ship.center_x < 0:
            ship.center_x = SCREEN_WIDTH           
 
if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
