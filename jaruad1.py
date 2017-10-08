import arcade
import random
import sys
from models import * #* = เอามาแม่งให้หมดอ่ะ
#ตรงนี้อย่าซน
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
        self.hp = 200
        self.hp_text = None
        self.boss_hp = 100
        self.boss_hp_text = None
        self.current_lv = '1'
        self.current_lv_text = None
        self.gameover = False
        self.speedup = 0
        self.speeddropped = False
        self.multigun = False
        self.gundropped = False
        self.automatic = False
        self.autodropped = False
        self.healdropped = False
        self.bossspawned = False
        self.bossdefeat = False
        #Level
        self.lv2 = False
        self.lv3 = False
        self.lv4 = False
        self.BOSS = False
        self.lv6 = False
        self.lv7 = False
        #create all sprite array
        self.all_sprites_list = arcade.SpriteList()
        self.enemy_sprites_list = arcade.SpriteList()
        self.enemysub_sprites_list = arcade.SpriteList()
        self.torpedo_sprites_list = arcade.SpriteList()
        self.enemyair_sprites_list = arcade.SpriteList()
        self.enemyred_sprites_list = arcade.SpriteList()
        self.enemyred_bullet_sprites_list = arcade.SpriteList()
        self.boss_sprite = arcade.SpriteList()
        self.nuclear_sprites_list = arcade.SpriteList()
        self.enemyblue_sprites_list = arcade.SpriteList()
        self.ghost_sprites_list = arcade.SpriteList()
        self.gun_auto_list = arcade.SpriteList()
        self.heal_list = arcade.SpriteList()
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
        output = f"Score : {self.score}"
        if not self.score_text or output != self.score_text.text:
            self.score_text = arcade.create_text(output, arcade.color.WHITE, 20)
        arcade.render_text(self.score_text, SCREEN_WIDTH/25, SCREEN_HEIGHT*1.72/25)
        #hp
        output2 = f"Player's HP : {self.hp}"
        if not self.hp_text or output2 != self.hp_text.text:
            self.hp_text = arcade.create_text(output2, arcade.color.WHITE, 20)
        arcade.render_text(self.hp_text, SCREEN_WIDTH/25, SCREEN_HEIGHT/25)
        #bosshp
        if self.BOSS == True:
            output3 = f"General Prayeth : {self.boss_hp}"
            if not self.boss_hp_text or output3 != self.boss_hp_text.text:
                self.boss_hp_text = arcade.create_text(output3, arcade.color.RED, 20)
            arcade.render_text(self.boss_hp_text, SCREEN_WIDTH*17/25, SCREEN_HEIGHT/25)
        #current level
        output4 = f"Level : {self.current_lv}"
        if not self.current_lv_text or output4 != self.current_lv_text.text:
            self.current_lv_text = arcade.create_text(output4, arcade.color.WHITE, 20)
        arcade.render_text(self.current_lv_text, SCREEN_WIDTH/25, SCREEN_HEIGHT*2.44/25)

    def update(self,x):
        self.all_sprites_list.update()
        self.framecount+=1
        #update current level
        if self.score>=0 and self.score <30:
            self.current_lv = '1'
        elif self.score>=30 and self.score <100:
            self.current_lv = '2'
        elif self.score>=100 and self.score <300:
            self.current_lv = '3'
        elif self.score>=300 and self.score <500:
            self.current_lv = '4'
        elif self.score>=500 and self.bossdefeat == False:
            self.current_lv = '5 (BOSS)'
        elif self.bossdefeat == True and self.score <1000:
            self.current_lv = '6'
        elif self.bossdefeat == True and self.score >=1000:
            self.current_lv = '7'

        #spawning enemy : Vanilla Tank
        if self.framecount%12==0 and self.lv7 == False:
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

        if self.framecount%36==0 and self.lv3 == True:
            enemyair = EnemyAirforce("images/enemyair.png", SCALE*1.1)
            if enemyair.center_x> SCREEN_WIDTH/2:
                enemyair.angle = 180
            enemyair.hp = random.randrange(5)+4
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
            enemyred.hp = 15
            self.enemyred_sprites_list.append(enemyred)
            self.all_sprites_list.append(enemyred)

        #spawning enemy BOSS : General Prayeth
        if self.score>=500 and self.bossspawned == False:
            self.BOSS = True
            self.bossspawned = True
            print("BOSS incoming! General Prayeth (hp:100,weapon:nuclear,subweapon:pistol)")
            prayeth = BOSS("images/prayed.png", SCALE)
            prayeth.hp = 100
            self.boss_sprite.append(prayeth)
            self.all_sprites_list.append(prayeth)

        if self.BOSS == True:
            if self.framecount%40==0:#Prayeth's weapon no.1
                nuclear = Redbullet("images/nuclear.png",SCALE)
                nuclear.center_x = random.randrange(SCREEN_WIDTH-40)+40
                nuclear.center_y = SCREEN_HEIGHT
                nuclear.hp = 6
                self.nuclear_sprites_list.append(nuclear)
                self.all_sprites_list.append(nuclear)
            if self.framecount%25==0:#Prayeth's weapon no.2
                for prayeth in self.boss_sprite:#spawning bullet from prayeth
                    redbullet = Redbullet("images/bulletenemy.png", SCALE*0.9)
                    redbullet.center_x = prayeth.center_x
                    redbullet.top = prayeth.bottom
                    self.enemyred_bullet_sprites_list.append(redbullet)
                    self.all_sprites_list.append(redbullet)

        #spawning enemy level 6 :  Thorn Tank
        if self.bossdefeat == True:
            self.lv6 = True
        if self.framecount%150==0 and self.lv6 == True:
            enemyblue = EnemyBlue("images/enemyblue.png", SCALE)
            if enemyblue.center_y < SCREEN_HEIGHT/2:
                enemyblue.angle = 180
            enemyblue.hp = 20
            self.enemyblue_sprites_list.append(enemyblue)
            self.all_sprites_list.append(enemyblue)

        #spawning enemy level 7 : Ghost Plane
        if self.score>=1000 and self.bossdefeat == True:
            self.lv7 = True
        if self.framecount%25==0 and self.lv7 == True:
            ghost = Stealth("images/ghost.png", SCALE)
            ghost.hp = 8
            self.ghost_sprites_list.append(ghost)
            self.all_sprites_list.append(ghost)

        #automatic shooting
        if self.automatic == True:
            if self.framecount%7==0:
                if self.multigun == True:#upgrade
                    for i in range(3):
                        bullet = Bullet("images/bullet.png",SCALE*0.9)
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
            fence = Torpedo("images/fence.png", SCALE*1.1)
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
        if self.score>= 80 and self.gundropped == False:
            self.gundropped = True
            gun = Greenfoot("images/d.png", SCALE)
            self.gun_list.append(gun)
            self.all_sprites_list.append(gun)

        #automatic upgrade deployed
        if self.score>=40 and self.autodropped == False:
            self.autodropped = True
            gunauto = Greenfoot("images/d2.png",SCALE)
            self.gun_auto_list.append(gunauto)
            self.all_sprites_list.append(gunauto)

        #heal deployed after boss defeated
        if self.bossdefeat == True and self.healdropped == False:
            self.healdropped = True
            heal = Greenfoot("images/d3.png",SCALE)
            self.heal_list.append(heal)
            self.all_sprites_list.append(heal)
        
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
            hit5 = arcade.check_for_collision_with_list(bullet,self.boss_sprite)
            if len(hit5)!=0:
                bullet.kill()
            for prayeth in hit5:
                prayeth.hp-=1
                self.boss_hp-=1
                if prayeth.hp<=0:
                    prayeth.kill()
                    self.score+=44
                    self.BOSS = False
                    self.bossdefeat = True
                    print("Killed general Prayeth! score+44")
            hit6 = arcade.check_for_collision_with_list(bullet,self.nuclear_sprites_list)
            if len(hit6)!=0:
                bullet.kill()
            for nuclear in hit6:
                nuclear.hp-=1
                if nuclear.hp<=0:
                    nuclear.kill()
            hit7 = arcade.check_for_collision_with_list(bullet,self.enemyblue_sprites_list)
            if len(hit7)!=0:
                bullet.kill()
            for enemyblue in hit7:
                enemyblue.hp-=1
                self.hp-=1
                print("Thorn tank reflect your bullet! Hp-1")
                if enemyblue.hp<=0:
                    self.score+=20
                    enemyblue.kill()
                    print("Killed a thorn tank. score+20")
            hit8 = arcade.check_for_collision_with_list(bullet,self.ghost_sprites_list)
            if len(hit8)!=0:
                bullet.kill()
            for ghost in hit8:
                ghost.hp-=1
                if ghost.hp<=0:
                    self.score+=15
                    ghost.kill()
                    print("Killed a ghost plane. score+15")

        #collision checking (enemies/upgrade vs player)       
        hit = arcade.check_for_collision_with_list(self.player_sprite,self.enemy_sprites_list)#player vs tank
        if len(hit)!=0:
            for enemy in hit:
                enemy.kill()
                self.hp-=1
                print("Hitted by a vanilla tank! Hp-1")       
 
        hit2 = arcade.check_for_collision_with_list(self.player_sprite,self.torpedo_sprites_list)#player vs torpedo
        if len(hit2)!=0:
            for torpedo in hit2:
                torpedo.kill()
                self.hp-=1 
                print("Hitted by a torpedo! Hp-1")
 
        hit3 = arcade.check_for_collision_with_list(self.player_sprite,self.speed_list)#player vs speedup
        if len(hit3)!=0:
            for speeder in hit3:
                speeder.kill()
                self.speedup += 1
                print("Speedup activated.")

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
 
        hit6 = arcade.check_for_collision_with_list(self.player_sprite,self.enemyair_sprites_list)#player vs airforce
        if len(hit6)!=0:
            for enemyair in hit6:
                self.hp-=enemyair.hp
                enemyair.kill()
                print("Hitted by a kamikaze! Hp-",enemyair.hp)
 
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

        hit9 = arcade.check_for_collision_with_list(self.player_sprite,self.gun_auto_list)#player vs autogun
        if len(hit9)!=0:
            for gunauto in hit9:
                gunauto.kill()
                self.automatic = True
                print("Autogun activated.")

        hit10 = arcade.check_for_collision_with_list(self.player_sprite,self.boss_sprite)#player vs boss
        if len(hit10)!=0:
            print("Coup by Prayeth! Instakill.")
            self.gameover = True
            
        hit11 = arcade.check_for_collision_with_list(self.player_sprite,self.nuclear_sprites_list)#player vs nuclear
        if len(hit11)!=0:
            for nuclear in hit11:
                self.hp-=3
                nuclear.kill()
                print("Hitted by a nuclear! Hp-3")

        hit12 = arcade.check_for_collision_with_list(self.player_sprite,self.heal_list)#player vs heal
        if len(hit12)!=0:
            for heal in hit12:
                self.hp+=200
                heal.kill()
                print("Healed! Hp+200")

        hit13 = arcade.check_for_collision_with_list(self.player_sprite,self.enemyblue_sprites_list)#player vs thorn tank
        if len(hit13)!=0:
            for enemyblue in hit13:
                enemyblue.kill()
                self.hp-=3
                print("Hitted by a thorn tank! Hp-3")

        hit14 = arcade.check_for_collision_with_list(self.player_sprite,self.ghost_sprites_list)
        if len(hit14)!=0:
            for ghost in hit14:
                if self.framecount%5==0:
                    self.hp-=1
                    ghost.hp+=1
                    print("A ghost plane consumed your soul! Hp-1 rapidly.")
        

        #gameover status
        if self.hp <= 0:
            self.gameover = True
        if self.gameover == True:
            print("Game Over!")
            if self.BOSS == True and self.bossspawned == True:
                print("So close, yet so far.")
            elif self.BOSS == False and self.bossspawned == False:
                print("Not even close, baby!")
            elif self.BOSS == False and self.bossspawned == True:
                print("You win! Thanks for playing. :D")
            print("Final score = ",self.score)
            sys.exit()
            
    def on_key_press(self, symbol, modifiers):
        #pew pew
        if symbol == arcade.key.SPACE and self.automatic == False:
            if self.multigun == True:#upgrade
                for i in range(3):
                    bullet = Bullet("images/bullet.png",SCALE*0.9)
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
        if symbol == arcade.key.RIGHT:
            self.player_sprite.vx = 1+self.speedup
        if symbol == arcade.key.UP:
            self.player_sprite.vy = 1+self.speedup
        if symbol == arcade.key.DOWN:
            self.player_sprite.vy = -1-self.speedup         
    def on_key_release(self, symbol, modifiers):
        #stop moving
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.player_sprite.vx = 0
        elif symbol == arcade.key.UP or symbol == arcade.key.DOWN:
            self.player_sprite.vy = 0          
 
if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
