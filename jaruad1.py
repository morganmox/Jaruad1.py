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
        #scoring/starting hp/gameover status
        self.hp = 175
        self.score = 0
        self.score_text = None
        self.hp_text = None
        self.boss_hp = 100
        self.boss_hp_text = None
        self.current_lv = '1'
        self.current_lv_text = None
        self.gameover = False
        #upgrade status
        self.speedup = 0
        self.multigun = False
        self.automatic = False
        self.lifesteal = False
        #upgrade/heal deploy status
        self.gundropped = False
        self.speeddropped = False
        self.autodropped = False
        self.healdropped = False
        self.lifestealdropped = False
        #boss status
        self.bossspawned = False
        self.bossdefeat = False
        #Level
        self.lv2 = False
        self.lv3 = False
        self.lv4 = False
        self.BOSS = False
        self.lv6 = False
        self.lv7 = False
        self.lv8 = False
        #create all sprite array
        self.all_sprites_list = arcade.SpriteList() # for drawing
        self.bullet_sprites_list = arcade.SpriteList() # player bullet
        self.enemy_sprites_list = arcade.SpriteList() #enemy
        self.enemy_bullet_sprites_list = arcade.SpriteList() #enemy bullet
        self.fence_sprites_list = arcade.SpriteList()
        self.upgrade_sprites_list = arcade.SpriteList() # upgrades
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
        elif self.bossdefeat == True and self.score >=1000 and self.score <1400:
            self.current_lv = '7'
        elif self.bossdefeat == True and self.score>=1400:
            self.current_lv = '8'

        #spawning fence
        if self.framecount%75==0:
            fence = Torpedo("images/fence.png", SCALE*1.1)
            fence.center_y = SCREEN_HEIGHT
            fence.center_x = random.randrange(SCREEN_WIDTH)+20
            self.fence_sprites_list.append(fence)
            self.all_sprites_list.append(fence)

        #spawning enemy : Vanilla Tank
        if self.framecount%12==0 and self.lv7 == False:
            enemy = Enemy("images/enemy.png", SCALE)
            enemy.hp = 1
            enemy.damage = 1
            enemy.worth = 1
            enemy.type = 'Vanilla Tank'
            self.enemy_sprites_list.append(enemy)
            self.all_sprites_list.append(enemy)

        #spawning enemy level 2 :Submarine
        if self.score>=30:
            self.lv2 = True
                
        if self.framecount%30==0 and self.lv2 == True and self.lv8 == False:
            enemy = EnemySubmarine("images/enemysub.png", SCALE)
            enemy.hp = 2
            enemy.worth = 2
            enemy.type = 'Submarine'
            self.enemy_sprites_list.append(enemy)
            self.all_sprites_list.append(enemy)

        #spawning enemy level 3 : Kamikaze
        if self.score>=100:
            self.lv3 = True

        if self.framecount%36==0 and self.lv3 == True:
            enemy = EnemyAirforce("images/enemyair.png", SCALE*1.1)
            if enemy.center_x> SCREEN_WIDTH/2:
                enemy.angle = 180
            enemy.hp = random.randrange(3)+3
            enemy.damage = 0
            enemy.worth = 3
            enemy.type = 'Kamikaze'
            self.enemy_sprites_list.append(enemy)
            self.all_sprites_list.append(enemy)

        #spawning enemy level 4 : Elite Tank
        if self.score>=300:
            self.lv4 = True

        if self.framecount%150==0 and self.lv4 == True:
            enemy = EnemyRed("images/enemyred.png", SCALE)
            enemy.hp = 9
            enemy.damage = 2
            enemy.worth = 5
            enemy.type = 'Elite Tank'
            self.enemy_sprites_list.append(enemy)
            self.all_sprites_list.append(enemy)

        #spawning enemy BOSS : General Prayeth
        if self.score>=500 and self.bossspawned == False:
            self.BOSS = True
            self.bossspawned = True
            print("BOSS incoming! General Prayeth (hp:100,weapon:nuclear,subweapon:pistol)")
            enemy = BOSS("images/prayed.png", SCALE)
            enemy.hp = 100
            enemy.damage = -666
            enemy.worth = 44
            enemy.type = 'General Prayeth'
            self.enemy_sprites_list.append(enemy)
            self.all_sprites_list.append(enemy)
            
        #spawning nuclear (Boss's weapon)
        if self.BOSS == True and self.framecount%40==0:
            enemy = Redbullet("images/nuclear.png",SCALE)
            enemy.center_x = random.randrange(SCREEN_WIDTH-40)+40
            enemy.center_y = SCREEN_HEIGHT
            enemy.hp = 6
            enemy.damage = 3
            enemy.worth = 0
            enemy.type = 'nuclear'
            self.enemy_sprites_list.append(enemy)
            self.all_sprites_list.append(enemy)

        #spawning enemy level 6 :  Thorn Tank
        if self.bossdefeat == True:
            self.lv6 = True
        if self.framecount%180==0 and self.lv6 == True:
            enemy = EnemyBlue("images/enemyblue.png", SCALE)
            if enemy.center_y < SCREEN_HEIGHT/2:
                enemy.angle = 180
            enemy.hp = 15
            enemy.damage = 3
            enemy.worth = 20
            enemy.type = 'Thorn Tank'
            self.enemy_sprites_list.append(enemy)
            self.all_sprites_list.append(enemy)

        #spawning enemy level 7 : Ghost Plane
        if self.score>=1000 and self.bossdefeat == True:
            self.lv7 = True
        if self.framecount%30==0 and self.lv7 == True:
            enemy = Stealth("images/ghost.png", SCALE)
            enemy.hp = 8
            enemy.damage = 1
            enemy.worth = 15
            enemy.unknown = True
            enemy.type = 'Ghost Plane'
            self.enemy_sprites_list.append(enemy)
            self.all_sprites_list.append(enemy)

        #spawning enemy level 8 : F-22 Falcon
        if self.score>=1400 and self.bossdefeat == True:
            self.lv8 = True
        if self.framecount%22==0 and self.lv8 == True:
            enemy = Falcon("images/Falcon.png", SCALE)
            enemy.hp = 12
            enemy.damage = 0
            enemy.soulripped = False
            enemy.worth = 20
            enemy.type = 'F-22 Falcon'
            self.enemy_sprites_list.append(enemy)
            self.all_sprites_list.append(enemy)

        #bullet from enemies
        for enemy in self.enemy_sprites_list:
            if enemy.type == 'Elite Tank':
                if self.framecount%40==0:
                    enemybullet = Redbullet("images/bulletenemy.png", SCALE*0.9)
                    enemybullet.center_x = enemy.center_x
                    enemybullet.top = enemy.bottom
                    enemybullet.damage = 1
                    enemybullet.type = 'Bullet'
                    self.enemy_bullet_sprites_list.append(enemybullet)
                    self.all_sprites_list.append(enemybullet)
            elif enemy.type == 'Submarine':
                if random.randrange(100)<2:
                    enemybullet = Torpedo("images/torpedo.png", SCALE)
                    enemybullet.center_x = enemy.center_x
                    enemybullet.top = enemy.bottom
                    enemybullet.damage = 1
                    enemybullet.type = 'Torpedo'
                    self.enemy_bullet_sprites_list.append(enemybullet)
                    self.all_sprites_list.append(enemybullet)
            elif enemy.type == 'General Prayeth':
                if self.framecount%25==0:
                    enemybullet = Redbullet("images/bulletenemy.png", SCALE*0.9)
                    enemybullet.center_x = enemy.center_x
                    enemybullet.top = enemy.bottom
                    enemybullet.damage = 2
                    enemybullet.type = 'Pistol'
                    self.enemy_bullet_sprites_list.append(enemybullet)
                    self.all_sprites_list.append(enemybullet)
            elif enemy.type == 'F-22 Falcon':
                if self.framecount%15==0:
                    for i in range(2):
                        enemybullet = Falconbullet("images/bulletenemy.png",SCALE*0.9)
                        enemybullet.center_x = enemy.center_x-(enemy.width/4)+(enemy.width/2*i)
                        enemybullet.top = enemy.bottom
                        enemybullet.damage = 1
                        enemybullet.type = 'Bullet'
                        self.enemy_bullet_sprites_list.append(enemybullet)
                        self.all_sprites_list.append(enemybullet)

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

        #speedup upgrade deployed
        if self.score>= 20 and self.speeddropped == False:
            self.speeddropped = True
            upgrade = Greenfoot("images/greenfoot.png", SCALE)
            upgrade.type = 'Speed'
            self.upgrade_sprites_list.append(upgrade)
            self.all_sprites_list.append(upgrade)
 
        #multigun upgrade deployed
        if self.score>= 80 and self.gundropped == False:
            self.gundropped = True
            upgrade = Greenfoot("images/d.png", SCALE)
            upgrade.type = 'Multi'
            self.upgrade_sprites_list.append(upgrade)
            self.all_sprites_list.append(upgrade)

        #automatic upgrade deployed
        if self.score>=40 and self.autodropped == False:
            self.autodropped = True
            upgrade = Greenfoot("images/d2.png",SCALE)
            upgrade.type = 'Auto'
            self.upgrade_sprites_list.append(upgrade)
            self.all_sprites_list.append(upgrade)

        #heal deployed after boss defeated
        if self.bossdefeat == True and self.healdropped == False:
            self.healdropped = True
            upgrade = Greenfoot("images/d3.png",SCALE)
            upgrade.type = 'Heal'
            self.upgrade_sprites_list.append(upgrade)
            self.all_sprites_list.append(upgrade)

        #lifesteal deployed after level 8
        if self.lv8 == True and self.lifestealdropped == False:
            self.lifestealdropped = True
            upgrade = Greenfoot("images/d4.png",SCALE)
            upgrade.type = 'Lifesteal'
            self.upgrade_sprites_list.append(upgrade)
            self.all_sprites_list.append(upgrade)

        #collision checking (enemies vs player)       
        hit = arcade.check_for_collision_with_list(self.player_sprite,self.enemy_sprites_list)
        if len(hit)!=0:
            for enemy in hit:
                if enemy.type == 'Submarine':#do nothing
                    print("Submarine is harmless.")
                elif enemy.type == 'Ghost Plane':#lifesteal
                    if self.framecount%5==0:
                        enemy.hp+=1
                        self.hp-=1
                        print("Ghost Plane consumed your soul! Hp-1")
                elif enemy.type == 'Kamikaze':#damage = remaining hp
                    self.hp-=enemy.hp
                    enemy.kill()
                    print("Hitted by Kamikaze! Hp-",enemy.hp)
                elif enemy.type == 'General Prayeth':#Fatal damage (Boss)
                    print("Coup by General Prayeth! Instant death.")
                    self.gameover = True
                elif enemy.type == 'F-22 Falcon':#Falcon's soulrip
                    if enemy.soulripped == False:
                        enemy.soulripped = True
                        if self.hp > 40:
                            self.hp = int(self.hp/2)
                            print("Heavy damage from F-22 Falcon! Hp halved.")
                        else :
                            print("Heavy damage from F-22 Falcon! Instant kill.(Hp<=40)")
                            self.gameover = True
                else:
                    self.hp-=enemy.damage
                    print("Hitted by",enemy.type,"! Hp-",enemy.damage)
                    enemy.kill()

        #collision checking 2 (player bullet vs enemies)
        for bullet in self.bullet_sprites_list:
            hit2 = arcade.check_for_collision_with_list(bullet,self.enemy_sprites_list)
            if len(hit2)!=0:
                bullet.kill()
                if self.lifesteal == True:
                    self.hp+=1   
            for enemy in hit2:
                if enemy.type == 'General Prayeth':
                    enemy.hp-=1
                    self.boss_hp-=1
                elif enemy.type == 'Thorn Tank':
                    self.hp-=1
                    enemy.hp-=1
                    print("Thorn tank reflect your bullet! Hp-1")
                elif enemy.type == 'Ghost Plane':
                    if enemy.unknown == True:
                        enemy.unknown = False
                        print("Invisible object detected! Be careful.")
                    enemy.hp-=1
                else:
                    enemy.hp-=1
                if enemy.hp<=0:
                    if enemy.type == 'General Prayeth':
                        self.BOSS = False
                        self.bossdefeat= True
                    self.score+=enemy.worth
                    print(enemy.type,"has been killed. score+",enemy.worth)
                    enemy.kill()

        #collision checking 3 (player vs upgrades)
        hit3 = arcade.check_for_collision_with_list(self.player_sprite,self.upgrade_sprites_list)
        if len(hit3)!=0:
            for upgrade in hit3:
                if upgrade.type == 'Auto':
                    self.automatic = True
                    print("Automatic activated!")
                elif upgrade.type == 'Speed':
                    self.speedup+=0.8
                    print("Speed up!")
                elif upgrade.type == 'Multi':
                    self.multigun = True
                    print("Triple shot activated!")
                elif upgrade.type == 'Heal':
                    self.hp +=250
                    print("Heal! hp+250")
                elif upgrade.type == 'Lifesteal':
                    self.lifesteal = True
                    print("Lifesteal activated!")
                upgrade.kill()

        #collision checking 4 (player vs fence)
        hit4 = arcade.check_for_collision_with_list(self.player_sprite,self.fence_sprites_list)
        if len(hit4)!=0:
            print("Fence does fatal damage! Instant death.")
            self.gameover = True

        #collision checking 5 (player vs enemybullet)
        hit5 = arcade.check_for_collision_with_list(self.player_sprite,self.enemy_bullet_sprites_list)
        if len(hit5)!=0:
            for enemybullet in hit5:
                self.hp-=enemybullet.damage
                print("Got hit by",enemybullet.type,"! hp-",enemybullet.damage)
                enemybullet.kill()

        #gameover status
        if self.hp <= 0:
            self.gameover = True
        if self.gameover == True:
            print("Game Over!")
            print("Final score = ",self.score)
            if self.BOSS == True and self.bossspawned == True:
                print("So close, yet so far.")
            elif self.BOSS == False and self.bossspawned == False:
                print("Not even close, baby!")
            elif self.BOSS == False and self.bossspawned == True:
                print("You win! Thanks for playing. :D")
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
