import arcade
import random
import sys
from models import Enemy,Bullet,Ship,EnemySubmarine,Torpedo,Greenfoot,EnemyAirforce

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCALE = 1.4

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)

        #whatever setting
        arcade.set_background_color(arcade.color.AMAZON)
        self.framecount = 0 #enemy
        self.framecount2 = 0 #enemysubmarine
        self.framecount3 = 0 #fence
        self.framecount4 = 0 #enemyair
        #scoring/starting hp/upgrades
        self.score = 0
        self.score_text = None
        self.hp = 8
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
        self.enemyair_sprites_list = arcade.SpriteList()
        self.bullet_sprites_list = arcade.SpriteList()
        self.gun_list = arcade.SpriteList()
        self.speed_list = arcade.SpriteList()
        self.fence_list = arcade.SpriteList()
        #giving birth to player
        self.player_sprite = Ship("images/ship.png", SCALE*0.95)
        self.all_sprites_list.append(self.player_sprite)
        print("Game start with Hp =",self.hp)

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
        self.framecount3+=1

        #spawning enemy
        if self.framecount>8:
            self.framecount = 0
            enemy = Enemy("images/enemy.png", SCALE)
            self.enemy_sprites_list.append(enemy)
            self.all_sprites_list.append(enemy)

        #spawning enemy level 2 (score>50)
        if self.score>=50:
            self.lv2 = True
            self.framecount2+=1
            for enemysub in self.enemysub_sprites_list:#spawning torpedo from submarine
                if random.randrange(100)<2:
                    torpedo = Torpedo("images/torpedo.png", SCALE)
                    torpedo.center_x = enemysub.center_x
                    torpedo.top = enemysub.bottom
                    self.torpedo_sprites_list.append(torpedo)
                    self.all_sprites_list.append(torpedo)
                
        if self.framecount2>30 and self.lv2 == True:
            self.framecount2 = 0
            enemysub = EnemySubmarine("images/enemysub.png", SCALE)
            self.enemysub_sprites_list.append(enemysub)
            self.all_sprites_list.append(enemysub)

        #spawning enemy level 3 (score>300)
        if self.score>=300:
            self.lv3 = True
            self.framecount4+=1

        if self.framecount4>40 and self.lv3 == True:
            self.framecount4 = 0
            enemyair = EnemyAirforce("images/enemyair.png", SCALE*1.2)
            enemyair.hp = 5
            self.enemyair_sprites_list.append(enemyair)
            self.all_sprites_list.append(enemyair)
        
        #spawning fence
        if self.framecount3>80:
            self.framecount3 = 0
            fence = Torpedo("images/fence.png", SCALE*1.1)
            fence.center_y = SCREEN_HEIGHT
            fence.center_x = random.randrange(SCREEN_WIDTH)+50
            self.fence_list.append(fence)
            self.all_sprites_list.append(fence)

        #speedup upgrade deployed (score>25)
        if self.score>= 25 and self.speeddropped == False:
            self.speeddropped = True
            speeder = Greenfoot("images/greenfoot.png", SCALE)
            self.speed_list.append(speeder)
            self.all_sprites_list.append(speeder)
 
        #multigun upgrade deployed (score>60)
        if self.score>= 60 and self.gundropped == False:
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
                print("Killed a vanilla tank. score+1")
            hit2 = arcade.check_for_collision_with_list(bullet,self.enemysub_sprites_list)
            if len(hit2)!=0:
                bullet.kill()
            for enemysub in hit2:
                enemysub.kill()
                self.score+=2
                print("Killed a submarine. score+2")
            hit3 = arcade.check_for_collision_with_list(bullet,self.enemyair_sprites_list)
            if len(hit3)!=0:
                bullet.kill()
            for enemyair in hit3:
                enemyair.hp-=1
                if enemyair.hp<=0:
                    enemyair.kill()
                    self.score+=3
                    print("Killed an airforce. score+3")

        #collision checking (enemies/upgrade vs player)       
        hit = arcade.check_for_collision_with_list(self.player_sprite,self.enemy_sprites_list)#player vs tank
        if len(hit)!=0:
            for enemy in hit:
                enemy.kill()
            print("Hitted by a vanilla tank! Hp-1")
            self.hp-=1            
        hit2 = arcade.check_for_collision_with_list(self.player_sprite,self.torpedo_sprites_list)#player vs torpedo
        if len(hit2)!=0:
            for torpedo in hit2:
                torpedo.kill()
            print("Hitted by a torpedo! Hp-1")
            self.hp-=1   
        if self.speeddropped == True:
            hit3 = arcade.check_for_collision_with_list(self.player_sprite,self.speed_list)#player vs speedup
            if len(hit3)!=0:
                for speeder in hit3:
                    speeder.kill()
                    self.speedup += 1
                    print("Speedup activated.")
        if self.gundropped == True:
            hit4 = arcade.check_for_collision_with_list(self.player_sprite,self.gun_list)#player vs multigun
            if len(hit4)!=0:
                for gun in hit4:
                    gun.kill()
                    self.multigun = True
                    print("Multigun activated.")

        hit5 = arcade.check_for_collision_with_list(self.player_sprite,self.fence_list)#player vs fence
        if len(hit5)!=0:
            print("Hitted by a fence! Instakill.")
            self.hp = 0

        if self.lv3 == True:
            hit6 = arcade.check_for_collision_with_list(self.player_sprite,self.enemyair_sprites_list)#player vs airforce
            if len(hit6)!=0:
                for enemyair in hit6:
                    self.hp-=enemyair.hp
                    enemyair.kill()
                    print("Hitted by an airforce! Hp-",enemyair.hp)

        #gameover status
        if self.hp <= 0:
            self.gameover = True
        if self.gameover == True:
            self.player_sprite.kill()
            print("Game Over")
            print("Final score = ",self.score)
            sys.exit()
            
    def on_key_press(self, symbol, modifiers):
        #pew pew
        if symbol == arcade.key.SPACE and self.gameover != True:
            if self.multigun == True:#upgrade
                for i in range(3):
                    bullet = Bullet("images/bullet.png",SCALE*0.8)
                    bullet.center_x = self.player_sprite.center_x-(self.player_sprite.width/2*(i-1))
                    bullet.bottom = self.player_sprite.top
                    self.bullet_sprites_list.append(bullet)
                    self.all_sprites_list.append(bullet)
            else :#no upgrade
                bullet = Bullet("images/bullet.png",SCALE)
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
