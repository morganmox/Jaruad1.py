import arcade
from models import Enemy,Bullet,Ship

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCALE = 1.5

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)

        #whatever setting
        arcade.set_background_color(arcade.color.AMAZON)
        self.set_mouse_visible(False)
        self.framecount = 0
        #scoring/hpremaining
        self.score = 0
        self.score_text = None
        self.hp = 3
        self.hp_text = None
        self.gameover = False
        #create all sprite array
        self.all_sprites_list = arcade.SpriteList()
        self.enemy_sprites_list = arcade.SpriteList()
        self.bullet_sprites_list = arcade.SpriteList()
        #giving birth to player
        self.player_sprite = Ship("images/ship.png", SCALE)
        self.all_sprites_list.append(self.player_sprite)

    def on_draw(self):
        #simply draw everything
        arcade.start_render()
        self.all_sprites_list.draw()
        #scoreboard
        output = f"Score = {self.score}"
        if not self.score_text or output != self.score_text.text:
            self.score_text = arcade.create_text(output, arcade.color.WHITE, 20)
        arcade.render_text(self.score_text, SCREEN_WIDTH/2-50, SCREEN_HEIGHT-60)
        #hp
        output2 = f"HP = {self.hp}"
        if not self.hp_text or output2 != self.hp_text.text:
            self.hp_text = arcade.create_text(output2, arcade.color.BLACK, 18)
        arcade.render_text(self.hp_text, SCREEN_WIDTH/25, SCREEN_HEIGHT/25)

    def update(self,x):
        self.all_sprites_list.update()
        self.framecount+=1
        #spawning enemy
        if self.framecount>10 and self.gameover!=True:
            self.framecount = 0
            enemy = Enemy("images/enemy.png", SCALE)
            self.enemy_sprites_list.append(enemy)
            self.all_sprites_list.append(enemy)
        #collision checking (bullet vs enemy)
        for bullet in self.bullet_sprites_list:
            hit = arcade.check_for_collision_with_list(bullet,self.enemy_sprites_list)
            #both bullet and enemy got killed for collision
            if len(hit)!=0:
                bullet.kill()
            for enemy in hit:
                enemy.kill()
                self.score+=1
        #collision checking (enemy vs player)       
        hit2 = arcade.check_for_collision_with_list(self.player_sprite,self.enemy_sprites_list)
        if len(hit2)!=0:
            for enemy in hit2:
                enemy.kill()
            self.hp-=1
        #gameover status
        if self.hp == 0:
            self.gameover = True
        if self.gameover == True:
            self.player_sprite.kill()
            
    def on_key_press(self, symbol, modifiers):
        #pew pew
        if symbol == arcade.key.SPACE:
            bullet = Bullet("images/bullet.png",SCALE)
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top
            self.bullet_sprites_list.append(bullet)
            self.all_sprites_list.append(bullet)
        #moving
        if symbol == arcade.key.LEFT:
            self.player_sprite.vx = -1
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.vx = 1
        if symbol == arcade.key.UP:
            self.player_sprite.vy = 1
        elif symbol == arcade.key.DOWN:
            self.player_sprite.vy = -1
            
    def on_key_release(self, symbol, modifiers):
        #stop moving
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
