import arcade
import random
import sys
from models import Enemy,Bullet,Ship,EnemySubmarine,Torpedo,Greenfoot,EnemyAirforce,EnemyRed,Redbullet

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCALE = 1.4

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)

        #bg setting,framecount
        arcade.set_background_color(arcade.color.AMAZON)
        self.framecount = 0
        #scoring/starting hp/upgrades
        self.score = 0
        self.score_text = None
        self.hp = 30
        self.hp_text = None
        self.gameover = False
        self.speedup = 0
        self.speeddropped = False
        self.multigun = False
        self.gundropped = False
        self.automatic = False
        self.autodropped = False
        #Level
        self.lv2 = False
        self.lv3 = False
        self.lv4 = False
        #create all sprite array
        self.all_sprites_list = arcade.SpriteList()
        self.enemy_sprites_list = arcade.SpriteList()
        self.enemysub_sprites_list = arcade.SpriteList()
        self.torpedo_sprites_list = arcade.SpriteList()
        self.enemyair_sprites_list = arcade.SpriteList()
        self.enemyred_sprites_list = arcade.SpriteList()
        self.enemyred_bullet_sprites_list = arcade.SpriteList()
        self.gun_auto_list = arcade.SpriteList()
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

        #spawning enemy : Vanilla Tank
        if self.framecount%13==0:
            enemy = Enemy("images/enemy.png", SCALE)
            self.enemy_sprites_list.append(enemy)
            self.all_sprites_list.append(enemy)

        #spawning enemy level 2 :Submarine
        if self.score>=30:
            self.lv2 = True
            for enemysub in self.enemysub_sprites_list:#spawning torpedo from submarine
                if random.randrange(100)<2:
                    torpedo = Torpedo("images/torpedo.png", SCALE)
                    torpedo.center_x = enemysub.center_x
                    torpedo.top = enemysub.bottom
                    self.torpedo_sprites_list.append(torpedo)
                    self.all_sprites_list.append(torpedo)
                
        if self.framecount%30==0 and self.lv2 == True:
            enemysub = EnemySubmarine("images/enemysub.png", SCALE)
            self.enemysub_sprites_list.append(enemysub)
            self.all_sprites_list.append(enemysub)

        #spawning enemy level 3 : Kamikaze
        if self.score>=100:
            self.lv3 = True

        if self.framecount%35==0 and self.lv3 == True:
            enemyair = EnemyAirforce("images/enemyair.png", SCALE*1.2)
            enemyair.hp = random.randrange(4)+3
            self.enemyair_sprites_list.append(enemyair)
            self.all_sprites_list.append(enemyair)

        #spawning enemy level 4 : Elite Tank
        if self.score>=300:
            self.lv4 = True
            if self.framecount%40==0:
                for enemyred in self.enemyred_sprites_list:#spawning bullet from elite tank
                    redbullet = Redbullet("images/bulletenemy.png", SCALE*0.9)
                    redbullet.center_x = enemyred.center_x
                    redbullet.top = enemyred.bottom
                    self.enemyred_bullet_sprites_list.append(redbullet)
                    self.all_sprites_list.append(redbullet)

        if self.framecount%150==0 and self.lv4 == True:
            enemyred = EnemyRed("images/enemyred.png", SCALE)
            enemyred.hp = 8
            self.enemyred_sprites_list.append(enemyred)
            self.all_sprites_list.append(enemyred)

        #automatic shooting
        if self.automatic == True:
            if self.framecount%8==0:
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
        
        #spawning fence
        if self.framecount%75==0:
            fence = Torpedo("images/fence.png", SCALE*1.2)
            fence.center_y = SCREEN_HEIGHT
            fence.center_x = random.randrange(SCREEN_WIDTH)+20
            self.fence_list.append(fence)
            self.all_sprites_list.append(fence)

        #speedup upgrade deployed
        if self.score>= 20 and self.speeddropped == False:
            self.speeddropped = True
            speeder = Greenfoot("images/greenfoot.png", SCALE)
            self.speed_list.append(speeder)
            self.all_sprites_list.append(speeder)
 
        #multigun upgrade deployed
        if self.score>= 40 and self.gundropped == False:
            self.gundropped = True
            gun = Greenfoot("images/d.png", SCALE)
            self.gun_list.append(gun)
            self.all_sprites_list.append(gun)

        #automatic upgrade deployed
        if self.score>=60 and self.autodropped == False:
            self.autodropped = True
            gunauto = Greenfoot("images/d2.png",SCALE)
            self.gun_auto_list.append(gunauto)
            self.all_sprites_list.append(gunauto)
            
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
                    print("Killed a kamikaze. score+3")
            hit4 = arcade.check_for_collision_with_list(bullet,self.enemyred_sprites_list)
            if len(hit4)!=0:
                bullet.kill()
            for enemyred in hit4:
                enemyred.hp-=1
                if enemyred.hp<=0:
                    enemyred.kill()
                    self.score+=5
                    print("Killed an elite tank. score+5")

        #collision checking (enemies/upgrade vs player)       
        hit = arcade.check_for_collision_with_list(self.player_sprite,self.enemy_sprites_list)#player vs tank
        if len(hit)!=0:
            for enemy in hit:
                enemy.kill()
            print("Hitted by a vanilla tank! Hp-1")
            self.hp-=1
        if self.lv2 == True:  
            hit2 = arcade.check_for_collision_with_list(self.player_sprite,self.torpedo_sprites_list)#player vs torpedo
            if len(hit2)!=0:
                for torpedo in hit2:
                    torpedo.kill()
                    self.hp-=1 
                    print("Hitted by a torpedo! Hp-1")
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
            self.gameover = True
        if self.lv3 == True:
            hit6 = arcade.check_for_collision_with_list(self.player_sprite,self.enemyair_sprites_list)#player vs airforce
            if len(hit6)!=0:
                for enemyair in hit6:
                    self.hp-=enemyair.hp
                    enemyair.kill()
                    print("Hitted by a kamikaze! Hp-",enemyair.hp)
        if self.lv4 == True:
            hit7 = arcade.check_for_collision_with_list(self.player_sprite,self.enemyred_sprites_list)#player vs elite tank
            if len(hit7)!=0:
                for enemyred in hit7:
                    self.hp-=2
                    enemyred.kill()
                    print("Hitted by an elite tank! Hp-2")
            hit8 = arcade.check_for_collision_with_list(self.player_sprite,self.enemyred_bullet_sprites_list)#player vs elite tank's bullet
            if len(hit8)!=0:
                for redbullet in hit8:
                    self.hp-=1
                    redbullet.kill()
                    print("Hitted by a bullet! Hp-1")
        if self.autodropped == True:
            hit9 = arcade.check_for_collision_with_list(self.player_sprite,self.gun_auto_list)#player vs autogun
            if len(hit9)!=0:
                for gunauto in hit9:
                    gunauto.kill()
                    self.automatic = True
                    print("Autogun activated.")

        #gameover status
        if self.hp <= 0:
            self.gameover = True
        if self.gameover == True:
            print("Game Over")
            print("Final score = ",self.score)
            sys.exit()
            
    def on_key_press(self, symbol, modifiers):
        #pew pew
        if symbol == arcade.key.SPACE and self.automatic == False:
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
