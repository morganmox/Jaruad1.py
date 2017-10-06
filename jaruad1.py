import arcade
import random
from models import Enemy,Bullet,Ship,EnemySubmarine,Torpedo,Greenfoot

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCALE = 1.5

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)

        #whatever setting
        arcade.set_background_color(arcade.color.AMAZON)
        self.set_mouse_visible(False) #hide cursor
        self.framecount = 0 #enemy
        self.framecount2 = 0 #enemysubmarine
        #scoring/hpremaining/upgrades
        self.score = 0
        self.score_text = None
        self.hp = 5
        self.hp_text = None
        self.gameover = False
        self.speedup = 0
        self.speeddropped = False
        self.multigun = False
        self.gundropped = False
        #Level
        self.lv2 = False
        self.lv3 = False
        #create all sprite array
        self.all_sprites_list = arcade.SpriteList()
        self.enemy_sprites_list = arcade.SpriteList()
        self.enemysub_sprites_list = arcade.SpriteList()
        self.torpedo_sprites_list = arcade.SpriteList()
        self.bullet_sprites_list = arcade.SpriteList()
        self.gun_list = arcade.SpriteList()
        self.speed_list = arcade.SpriteList()
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
        if self.framecount>7 and self.gameover!=True:
            self.framecount = 0
            enemy = Enemy("images/enemy.png", SCALE)
            self.enemy_sprites_list.append(enemy)
            self.all_sprites_list.append(enemy)

        #spawning enemy level 2 (score>50)
        if self.score>=50:
            self.lv2 = True
            self.framecount2+=1
            for enemysub in self.enemysub_sprites_list:
                if random.randrange(100)<2:
                    torpedo = Torpedo("images/torpedo.png", SCALE)
                    torpedo.center_x = enemysub.center_x
                    torpedo.top = enemysub.bottom
                    self.torpedo_sprites_list.append(torpedo)
                    self.all_sprites_list.append(torpedo)
                
        if self.framecount2>40 and self.gameover!=True and self.lv2 == True:
            self.framecount2 = 0
            enemysub = EnemySubmarine("images/enemysub.png", SCALE)
            self.enemysub_sprites_list.append(enemysub)
            self.all_sprites_list.append(enemysub)

        #speedup upgrade deployed (score>25)
        if self.score>= 25 and self.speeddropped == False:
            self.speeddropped = True
            speeder = Greenfoot("images/greenfoot.png", SCALE)
            self.speed_list.append(speeder)
            self.all_sprites_list.append(speeder)
 
        #multigun upgrade deployed (score>45)
        if self.score>= 45 and self.gundropped == False:
            self.gundropped = True
            gun = Greenfoot("images/d.png", SCALE)
            self.gun_list.append(gun)
            self.all_sprites_list.append(gun)
            
        #collision checking (bullet vs enemies)
        for bullet in self.bullet_sprites_list:
            hit = arcade.check_for_collision_with_list(bullet,self.enemy_sprites_list)
            if len(hit)!=0:
                bullet.kill()
            for enemy in hit:
                enemy.kill()
                self.score+=1
            hit2 = arcade.check_for_collision_with_list(bullet,self.enemysub_sprites_list)
            if len(hit2)!=0:
                bullet.kill()
            for enemysub in hit2:
                enemysub.kill()
                self.score+=2

        #collision checking (enemies/upgrade vs player)       
        hit = arcade.check_for_collision_with_list(self.player_sprite,self.enemy_sprites_list)#player vs tank
        if len(hit)!=0:
            for enemy in hit:
                enemy.kill()
            self.hp-=1
        hit2 = arcade.check_for_collision_with_list(self.player_sprite,self.torpedo_sprites_list)#player vs torpedo
        if len(hit2)!=0:
            for torpedo in hit2:
                torpedo.kill()
            self.hp-=1
        if self.speeddropped == True:
            hit3 = arcade.check_for_collision_with_list(self.player_sprite,self.speed_list)#player vs speedup
            if len(hit3)!=0:
                for speeder in hit3:
                    speeder.kill()
                    self.speedup += 1
                    print("Speedup activate")
        if self.gundropped == True:
            hit4 = arcade.check_for_collision_with_list(self.player_sprite,self.gun_list)#player vs multigun
            if len(hit4)!=0:
                for gun in hit4:
                    gun.kill()
                    self.multigun = True
                    print("Multigun activate")

        #gameover status
        if self.hp == 0:
            self.gameover = True
        if self.gameover == True:
            self.player_sprite.kill()
            print("Game Over")
            
    def on_key_press(self, symbol, modifiers):
        #pew pew
        if symbol == arcade.key.SPACE and self.gameover != True:
            if self.multigun == True:#upgrade
                for i in range(3):
                    bullet = Bullet("images/bullet.png",SCALE*0.9)
                    bullet.center_x = self.player_sprite.center_x-(self.player_sprite.width/2*(i-1))
                    bullet.bottom = self.player_sprite.top
                    self.bullet_sprites_list.append(bullet)
                    self.all_sprites_list.append(bullet)
            else :#no upgrade
                bullet = Bullet("images/bullet.png",SCALE*0.9)
                bullet.center_x = self.player_sprite.center_x
                bullet.bottom = self.player_sprite.top
                self.bullet_sprites_list.append(bullet)
                self.all_sprites_list.append(bullet)
        #moving
        if symbol == arcade.key.LEFT:
            self.player_sprite.vx = -1-self.speedup
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.vx = 1+self.speedup
        if symbol == arcade.key.UP:
            self.player_sprite.vy = 1+self.speedup
        elif symbol == arcade.key.DOWN:
            self.player_sprite.vy = -1-self.speedup         
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
