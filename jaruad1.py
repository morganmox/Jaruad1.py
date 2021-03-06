import arcade,random,sys,math
from models import *
from welcome import *
SCREEN_WIDTH = 600;SCREEN_HEIGHT = 600;SCALE = 1

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.set_background_color(arcade.color.AMAZON)
        self.framecount = 0
        #scoring/starting hp/gameover status
        self.score_list = [30,100,300,500,1000,1400,2000,2800,3800,4500,5500,6500,10000000]
        self.hp = HEART
        self.hp_text = None
        self.score = 0
        self.score_text = None
        self.boss_hp = 0
        self.boss_hp_text = None
        self.current_lv = 1
        self.current_lv_text = None
        self.fenceproof = FENCE
        self.fenceproof_text = None
        self.currentbossname = ''
        self.gameover = False
        self.finalscore = 0
        self.curse = 0
        self.timestop = 0
        #upgrade status
        self.upgrades_list = ['speed','auto','multi','heal','lifesteal','rapid','satanic','funnel']#upgrade list not being deployed
        self.speedup = 0
        self.firedelay = 7
        self.leechamount = 1
        self.multigun = False
        self.automatic = False
        self.lifesteal = False
        self.funnel = False
        #boss status
        self.boss_list = ['prayed','nasus','timewizard']
        self.bossdefeat = 0
        self.BOSS = False
        self.nasusstack = 6
        self.tmp = 0
        #สร้างที่เก็บของแต่ละอย่างไว้ check collision
        self.all_sprites_list = arcade.SpriteList() #เก็บทุกอย่างไว้สั่งวาดทุกอย่างในคำสั่งเดียว
        self.bullet_sprites_list = arcade.SpriteList() #player bullet
        self.enemy_sprites_list = arcade.SpriteList() #enemy
        self.enemy_bullet_sprites_list = arcade.SpriteList() #enemy bullet
        self.fence_sprites_list = arcade.SpriteList() #fence
        self.funnel_sprites_list = arcade.SpriteList() #funnel (test)
        self.upgrade_sprites_list = arcade.SpriteList() #upgrades
        self.player_sprite = Ship("images/ship.png", SCALE*0.95) #spawn ตัวคนเล่น
        self.all_sprites_list.append(self.player_sprite) #ยัดตัวคนเล่นเข้าไปใน list ที่จะวาด
        print("You play as a",STATUS,"Game start with Hp =",self.hp,",Fenceproof(s) =",self.fenceproof)
        
    def on_draw(self):
        arcade.start_render()
        self.all_sprites_list.draw()#วาดทุกอย่างที่สร้าง
        output = f"Score : {self.score}"#scoreboard
        if not self.score_text or output != self.score_text.text:
            self.score_text = arcade.create_text(output, arcade.color.WHITE, 17)
        arcade.render_text(self.score_text, SCREEN_WIDTH/25, SCREEN_HEIGHT*2.44/25)
        output2 = f"Player's HP : {self.hp}"#hp
        if not self.hp_text or output2 != self.hp_text.text:
            self.hp_text = arcade.create_text(output2, arcade.color.WHITE, 17)
        arcade.render_text(self.hp_text, SCREEN_WIDTH/25, SCREEN_HEIGHT/25)
        if self.BOSS == True:#bosshp
            output3 = f"{self.currentbossname} : {self.boss_hp}"
            if not self.boss_hp_text or output3 != self.boss_hp_text.text:
                self.boss_hp_text = arcade.create_text(output3, arcade.color.RED, 17)
            arcade.render_text(self.boss_hp_text, SCREEN_WIDTH*16.5/25, SCREEN_HEIGHT/25)
        output4 = f"Level : {self.current_lv}"#level ปัจจุบัน
        if not self.current_lv_text or output4 != self.current_lv_text.text:
            self.current_lv_text = arcade.create_text(output4, arcade.color.WHITE, 17)
        arcade.render_text(self.current_lv_text, SCREEN_WIDTH/25, SCREEN_HEIGHT*3.12/25)
        output5 = f"Fenceproof : {self.fenceproof}"#รั้ว
        if not self.fenceproof_text or output5 != self.fenceproof_text.text:
            self.fenceproof_text = arcade.create_text(output5, arcade.color.WHITE, 17)
        arcade.render_text(self.fenceproof_text, SCREEN_WIDTH/25, SCREEN_HEIGHT*1.72/25)
        
    def shooting(self,owner,typed,image,scale,number,adjust):#pew pew
        for i in range(number):
            bullet = Bullet(image,SCALE*scale)
            bullet.type = typed
            bullet.center_x = owner.center_x-(owner.width/2*(i-1+adjust))
            bullet.bottom = owner.top
            self.bullet_sprites_list.append(bullet)
            self.all_sprites_list.append(bullet)
            
    def update(self,x):
        def spawnenemy(typed,hp,damage,worth):
            if typed == 'Vanilla Tank':enemy = Enemy("images/enemy.png", SCALE)
            elif  typed == 'Submarine':enemy = EnemySubmarine("images/enemysub.png", SCALE)
            elif typed == 'Kamikaze':enemy = EnemyAirforce("images/enemyair.png", SCALE*1.1)
            elif typed == 'Elite Tank':enemy = EnemyRed("images/enemyred.png", SCALE)
            elif typed == 'Thorn Tank':enemy = EnemyBlue("images/enemyblue.png", SCALE)
            elif typed == 'Plague Tank':enemy = Enemy("images/enemyplague.png",SCALE)
            elif typed == 'Xhamster':enemy = Hamtaro("images/hamtaro.png",SCALE)
            elif typed == 'Versatile Tank':enemy = Enemy("images/enemyorange.png",SCALE)
            elif typed == 'Ghost Plane':enemy = Stealth("images/ghost.png", SCALE)
            elif typed == 'Balloon Tank':enemy = Enemy("images/enemy.png",SCALE)
            elif typed == 'Black Tank':enemy = Enemy("images/enemyblack.png",SCALE)
            elif typed == 'Jaruad2.py':enemy = Hamtaro("images/ship2.png",SCALE*0.95)
            elif typed == 'F-22 Falcon':enemy = Falcon("images/Falcon.png", SCALE);enemy.soulripped = False
            elif typed == 'General Prayeth' or typed == 'Nasus' or typed == 'Sakuya Izayoi':
                if typed == 'General Prayeth':
                    enemy = BOSS("images/prayed.png", SCALE)
                elif typed == 'Sakuya Izayoi':
                    enemy = BOSS("images/sakuya.png",SCALE);enemy.ultimate = False;enemy.second = False
                else:
                    enemy = BOSS("images/nasus.png", SCALE);enemy.ultimate = False
                self.BOSS = True
                self.currentbossname = typed
                print("BOSS incoming!",typed,".")
                self.boss_hp = hp
            elif typed == 'nuclear':
                enemy = Redbullet("images/nuclear.png",SCALE)
                enemy.center_x = random.randrange(SCREEN_WIDTH-30)+30
                enemy.center_y = SCREEN_HEIGHT
            enemy.type = typed;enemy.hp = hp;enemy.damage = damage;enemy.worth = worth
            self.enemy_sprites_list.append(enemy);self.all_sprites_list.append(enemy)
        
        def enemyshoot(host,typed,damage):
            if host == 'Elite Tank' or host == 'General Prayeth' or host == 'Versatile Tank':enemybullet = Redbullet("images/bulletenemy.png", SCALE*0.9)
            elif host == 'Submarine':enemybullet = Torpedo("images/torpedo.png", SCALE)
            elif host == 'Xhamster':enemybullet = Seed("images/shit.png", SCALE*0.9)
            elif host == 'Nasus':enemybullet = Falconbullet("images/cane.png",SCALE*1.2)
            if host == 'F-22 Falcon':#unique (2 bullets)
                for i in range(2):
                    enemybullet = Falconbullet("images/falconbullet.png",SCALE*0.9)
                    enemybullet.center_x = enemy.center_x-(enemy.width/4)+(enemy.width/2*i)
                    enemybullet.top = enemy.bottom
                    enemybullet.damage = damage
                    enemybullet.type = typed
                    self.enemy_bullet_sprites_list.append(enemybullet)
                    self.all_sprites_list.append(enemybullet)
            elif host == 'Jaruad2.py' or host == 'Sakuya Izayoi':#aim at player
                if host == 'Jaruad2.py':
                    enemybullet = arcade.Sprite("images/bulletenemy.png",SCALE*0.9);enemybullet.center_y = enemy.center_y;enemybullet.center_x = enemy.center_x
                    enemybullet.angle = math.degrees(math.atan2(self.player_sprite.center_y-enemybullet.center_y,self.player_sprite.center_x-enemybullet.center_x))
                    enemybullet.change_x = math.cos(math.atan2(self.player_sprite.center_y-enemybullet.center_y,self.player_sprite.center_x-enemybullet.center_x))*8
                    enemybullet.change_y = math.sin(math.atan2(self.player_sprite.center_y-enemybullet.center_y,self.player_sprite.center_x-enemybullet.center_x))*8
                elif host == 'Sakuya Izayoi':#sakuya
                    if typed == 'Knife' or typed == 'Random Knife':
                        if typed == 'Knife':
                            enemybullet = arcade.Sprite("images/knife.png",SCALE)
                            enemybullet.center_x = enemy.center_x
                            enemybullet.center_y = enemy.bottom
                        else:#random knife
                            enemybullet = arcade.Sprite("images/knife3.png",SCALE)
                            enemybullet.center_x = random.randrange(SCREEN_WIDTH-5)+5
                            enemybullet.center_y = random.randrange(SCREEN_HEIGHT-5)+5
                        enemybullet.angle = math.degrees(math.atan2(self.player_sprite.center_y-enemybullet.center_y,self.player_sprite.center_x-enemybullet.center_x))
                        enemybullet.change_x = math.cos(math.atan2(self.player_sprite.center_y-enemybullet.center_y,self.player_sprite.center_x-enemybullet.center_x))*8
                        enemybullet.change_y = math.sin(math.atan2(self.player_sprite.center_y-enemybullet.center_y,self.player_sprite.center_x-enemybullet.center_x))*8
                    else:
                        enemybullet = arcade.Sprite("images/knife2.png",SCALE)
                        enemybullet.center_y = enemy.center_y
                        enemybullet.center_x = enemy.center_x
                        enemybullet.angle = math.degrees(self.tmp*9)
                        enemybullet.change_x = math.cos(self.tmp*9)*8
                        enemybullet.change_y = math.sin(self.tmp*9)*8
                        self.tmp+=1
                enemybullet.damage = damage;enemybullet.type = typed
                self.enemy_bullet_sprites_list.append(enemybullet);self.all_sprites_list.append(enemybullet)
            else:#typical (1 bullet)
                enemybullet.center_x = enemy.center_x;enemybullet.top = enemy.bottom
                enemybullet.damage = damage;enemybullet.type = typed
                self.enemy_bullet_sprites_list.append(enemybullet);self.all_sprites_list.append(enemybullet)
                
        for enemybullet in self.enemy_bullet_sprites_list:
            if enemybullet.top<0:
                enemybullet.kill()
                
        def upgrade(typed,images,mul):
            upgrade = Greenfoot(images, SCALE*mul)
            upgrade.type = typed
            self.upgrade_sprites_list.append(upgrade);self.all_sprites_list.append(upgrade)
            
        self.all_sprites_list.update();self.framecount+=1

        if self.score>=self.score_list[0]:#levelup
            self.score_list.pop(0);self.current_lv+=1
        
        if self.framecount%75==0 and self.currentbossname != 'Sakuya Izayoi': #รั้วลวดหนาม
            fence = Torpedo("images/fence.png", 1.2)
            fence.center_y = SCREEN_HEIGHT
            fence.center_x = random.randrange(SCREEN_WIDTH)+20
            self.fence_sprites_list.append(fence)
            self.all_sprites_list.append(fence)

        if self.framecount%160==0 and self.BOSS==False and STATUS!='monkey.' and STATUS!='human.':
            spawnenemy('Jaruad2.py',self.current_lv*2,self.current_lv*2,self.current_lv*2)
        if self.framecount%12==0 and self.current_lv<=6:#lv 1-6
            spawnenemy('Vanilla Tank',1,1,1)
        if self.framecount%30==0 and self.current_lv>=2 and self.current_lv<=7:#lv 2-7
            spawnenemy('Submarine',2,0,2)
        if self.framecount%36==0 and self.current_lv>=3 and self.current_lv<=8:#lv 3-8
            spawnenemy('Kamikaze',random.randrange(3)+4,0,3)
        if self.framecount%150==0 and self.current_lv>=4 and self.current_lv<=9:#lv 4-9
            spawnenemy('Elite Tank',9,2,5)
        if self.current_lv>=5 and 'prayed' in self.boss_list:#BOSS (lv 5)
            self.boss_list.remove('prayed');spawnenemy('General Prayeth',150,-666,44)
        if self.BOSS == True and self.currentbossname == 'General Prayeth' and self.framecount%40==0:#Prayeth's weapon
            spawnenemy('nuclear',6,3,0)
        if self.framecount%180==0 and self.current_lv>=6 and self.bossdefeat >=1 and self.current_lv<=10:#lv 6-10
            spawnenemy('Thorn Tank',15,6,20)
        if self.framecount%30==0 and self.current_lv>=7 and self.current_lv<=11 and self.bossdefeat >=1:#lv 7-11
            spawnenemy('Ghost Plane',8,1,10)
        if self.framecount%45==0 and self.current_lv>=8 and self.BOSS==False:#lv 8++(-boss2)
            spawnenemy('F-22 Falcon',12,0,20)
        if self.framecount%25==0 and self.current_lv>=9 and self.current_lv<=13 and self.BOSS == False:#lv 9-13(-boss2)
            spawnenemy('Plague Tank',10,10,10)
        if self.framecount%21==0 and self.current_lv>=9 and self.current_lv<=13 and self.BOSS == False:#curse dps
            self.hp-=self.curse;print("You are cursed! Hp-",self.curse);self.curse = 0
        if self.framecount%180==0 and self.current_lv>=10 and self.BOSS==False:#lv 10-14(-boss2)
            spawnenemy('Xhamster',25,5,30)
        if self.framecount%20==0 and self.current_lv==11:#lv 11
            spawnenemy('Versatile Tank',15,5,25)
        if self.current_lv>=12 and 'nasus' in self.boss_list:#BOSS (lv 12)
            self.boss_list.remove('nasus');spawnenemy('Nasus',300,-666,350)
        if self.framecount%40==0 and self.current_lv>=13 and self.BOSS==False:#lv 13
            spawnenemy('Balloon Tank',20,25,35)
        if self.framecount%170==0 and self.current_lv>=14 and self.BOSS==False:#lv 14
            spawnenemy('Black Tank',35,-666,100)
        if 'timewizard' in self.boss_list and self.current_lv>=15:#BOSS (LV 15)
            self.boss_list.remove('timewizard');spawnenemy('Sakuya Izayoi',500,-666,600);self.hp = int(600/MUL)
        #spawnenemy(ชื่อ,hp,damage เวลาชน,คะแนนที่ได้เวลาฆ่า)
            
        for enemy in self.enemy_sprites_list:#ศัตรูตัวที่มีลูกเล่นพิเศษ
            if enemy.type == 'Elite Tank':
                if self.framecount%40==0:enemyshoot('Elite Tank','Bullet',1)
            elif enemy.type == 'Submarine':
                if random.randrange(100)<2:enemyshoot('Submarine','Torpedo',1)
            elif enemy.type == 'General Prayeth':
                if self.framecount%25==0:enemyshoot('General Prayeth','Pistol',2)
            elif enemy.type == 'F-22 Falcon':
                if self.framecount%20==0:enemyshoot('F-22 Falcon','Ruin king',1)
            elif enemy.type == 'Plague Tank':
                if self.framecount%21==0:self.curse+=1
            elif enemy.type == 'Xhamster':
                if self.framecount%21==0:enemyshoot('Xhamster','Hamster shit',2)
            elif enemy.type == 'Versatile Tank':
                if self.framecount%20==0:enemyshoot('Versatile Tank','Bullet',4)
            elif enemy.type == 'Jaruad2.py':
                enemy.angle = math.degrees(math.atan2(self.player_sprite.center_y-enemy.center_y,self.player_sprite.center_x-enemy.center_x))-90
                if random.randrange(75)<1:enemyshoot('Jaruad2.py','Bullet',self.current_lv)
            elif enemy.type == 'Nasus':
                if enemy.ultimate == False:
                    if self.framecount%40==0:enemyshoot('Nasus','Cane',self.nasusstack)
                else:
                    if self.framecount%20==0:enemyshoot('Nasus','Cane',self.nasusstack)
                    if self.framecount%40==0:self.hp = int(self.hp*95/100)-1;enemy.hp+=5;self.boss_hp+=5
            elif enemy.type == 'Sakuya Izayoi':
                self.timestop-=1
                if self.framecount%12==0:enemyshoot('Sakuya Izayoi','Knife',5)
                if enemy.second == True and self.framecount%70 == 0:
                    for i in range(30):
                        enemyshoot('Sakuya Izayoi','Knif3',5)
                    self.tmp = 0
                if self.framecount%150==0:
                    self.player_sprite.vx = 0;self.player_sprite.vy = 0
                    if enemy.ultimate == True:
                        self.timestop = 25
                        for i in range(20):
                            enemyshoot('Sakuya Izayoi','Random Knife',5)
                    else:self.timestop = 50
                    print("Time Freeze!")
                if self.timestop>0:arcade.set_background_color(arcade.color.BLACK)
                else:arcade.set_background_color(arcade.color.AMAZON)        
        #enemyshoot(ชื่อคนยิง,ชื่อกระสุน,damage ตอนโดน)

        if self.funnel == True:#funnel ยิง
            for funnel in self.funnel_sprites_list:
                if self.framecount%self.firedelay==0:
                    self.shooting(funnel,1,"images/falconbullet.png",0.7,1,1)

        if self.automatic == True:#เปิดยิง auto
            if self.framecount%self.firedelay==0 and self.timestop<1:
                if self.multigun == True:#เปิดยิง 3 ลูก
                    self.shooting(self.player_sprite,0,"images/bullet.png",0.9,3,0)
                else :#no upgrade
                    self.shooting(self.player_sprite,0,"images/bullet.png",0.9,1,1)

        #upgrades
        if self.score>= 20 and 'speed' in self.upgrades_list:
            self.upgrades_list.remove('speed') #speedup upgrade deployed
            upgrade('Speed',"images/greenfoot.png",1)
        if self.score>= 80 and 'multi' in self.upgrades_list:
            self.upgrades_list.remove('multi') #multigun upgrade deployed
            upgrade('Multi',"images/d.png",1)
        if self.score>=40 and 'auto' in self.upgrades_list:
            self.upgrades_list.remove('auto') #automatic upgrade deployed
            upgrade('Auto',"images/d2.png",1)
        if self.bossdefeat == 1 and 'heal' in self.upgrades_list:
            self.upgrades_list.remove('heal') #heal deployed after boss defeated
            upgrade('Heal',"images/d3.png",1)
        if self.current_lv>=9 and self.score<=3800: #heal deploy constantly after level 9
            if self.framecount%350==0:
                upgrade('Heal',"images/d3.png",1)
        if self.current_lv>=8 and 'lifesteal' in self.upgrades_list:
            self.upgrades_list.remove('lifesteal') #lifesteal deployed after level 8
            upgrade('Lifesteal',"images/d4.png",1)
        if self.score>=2500 and 'rapid' in self.upgrades_list:
            self.upgrades_list.remove('rapid') #rapidfire deployed after score>=2500
            upgrade('Gatling',"images/d5.png",1)
        if self.score>=3800 and 'satanic' in self.upgrades_list:
            self.upgrades_list.remove('satanic') #improve lifesteal
            upgrade('SATANIC',"images/d6.png",1)
        if 'funnel' in self.upgrades_list and self.current_lv>=4:
            self.upgrades_list.remove('funnel')
            upgrade('funnel',"images/ship.png",0.55)

        #collision checking (enemies vs player)       
        hit = arcade.check_for_collision_with_list(self.player_sprite,self.enemy_sprites_list)
        if len(hit)!=0:
            for enemy in hit:
                if enemy.type == 'Submarine':#do nothing
                    self.hp-=0
                elif enemy.type == 'Ghost Plane':#lifesteal
                    if self.framecount%5==0:
                        enemy.hp+=1;self.hp-=1
                elif enemy.type == 'Kamikaze':#damage = remaining hp
                    self.hp-=enemy.hp;enemy.kill()
                    print("Hitted by Kamikaze! Hp-",enemy.hp)
                elif enemy.damage == -666:#Fatal damage
                    print(enemy.type,"does fatal damage! Instant death.")
                    self.gameover = True
                elif enemy.type == 'F-22 Falcon':#Falcon's soulrip
                    if enemy.soulripped == False:
                        enemy.soulripped = True
                        if self.hp > 50:
                            self.hp = int(self.hp/2);print("Heavy damage from F-22 Falcon! Hp halved.")
                        else :
                            print("Heavy damage from F-22 Falcon! Instant kill.(Hp<=50)");self.gameover = True
                else:
                    self.hp-=enemy.damage
                    print("Hitted by",enemy.type,"! Hp-",enemy.damage)
                    enemy.kill()

        #collision checking 2 (player bullet vs enemies)
        for bullet in self.bullet_sprites_list:
            hit2 = arcade.check_for_collision_with_list(bullet,self.enemy_sprites_list)
            if len(hit2)!=0:
                if self.lifesteal == True and bullet.type == 0:
                    self.hp+=self.leechamount
                bullet.kill()
            for enemy in hit2:
                if enemy.type == 'General Prayeth' or enemy.type == 'Nasus' or enemy.type == 'Sakuya Izayoi':#boss hp display
                    self.boss_hp-=1
                    if enemy.type == 'Nasus':
                        if enemy.ultimate == False and enemy.hp<=50:#nasus ulti
                            enemy.ultimate = True;enemy.width+=30;enemy.height+=40;enemy.hp +=300;self.boss_hp +=300;print("Nasus activate fury of the sand!")
                    elif enemy.type == 'Sakuya Izayoi' and enemy.hp<=400:
                        if enemy.ultimate == False:enemy.ultimate = True
                        if enemy.hp<=200 and enemy.second == False:enemy.second = True;enemy.hp +=300;self.boss_hp +=300;enemy.texture = arcade.load_texture("images/sakuya2.png")
                elif (enemy.type == 'Thorn Tank' or enemy.type == 'Versatile Tank') and bullet.type == 0:
                    self.hp-=1
                elif enemy.type == 'Balloon Tank':
                    enemy.width+=4;enemy.height+=4;enemy.damage+=4
                enemy.hp-=1
                if enemy.hp<=0:
                    if enemy.type == 'Black Tank':
                        self.gameover = True
                        print("Black Tank dragged player down to grave!")
                    if enemy.type == 'General Prayeth' or enemy.type == 'Nasus' or enemy.type == 'Sakuya Izayoi':#BOSS down
                        self.current_lv+=1;self.currentbossname = '';self.BOSS = False;self.bossdefeat+=1;self.timestop = 0;arcade.set_background_color(arcade.color.AMAZON)
                    self.score+=enemy.worth
                    print(enemy.type,"has been killed. score+",enemy.worth)
                    enemy.kill()

        #collision checking 3 (player vs upgrades)
        hit3 = arcade.check_for_collision_with_list(self.player_sprite,self.upgrade_sprites_list)
        if len(hit3)!=0:
            for upgrade in hit3:
                if upgrade.type == 'Auto':
                    self.automatic = True;print("Automatic activated!")
                elif upgrade.type == 'Speed':
                    self.speedup+=0.6;print("Speed up!")
                elif upgrade.type == 'Multi':
                    self.multigun = True;print("Triple shot activated!")
                elif upgrade.type == 'Lifesteal':
                    self.lifesteal = True;print("Lifesteal activated!")
                elif upgrade.type == 'Gatling':
                    if self.firedelay>1:
                        self.firedelay-=2;print("Firerate increased!")
                elif upgrade.type == 'Heal':
                    self.hp +=HEART-50;print("Heal! hp+",HEART-50)
                elif upgrade.type == 'SATANIC':
                    self.leechamount+=1;print("Lifessteal increased!")
                elif upgrade.type == 'funnel':
                    self.funnel = True
                    print("You got some assistants!")
                    for i in range(2):
                        funnel = Funnel("images/ship.png", SCALE*0.55)
                        self.funnel_sprites_list.append(funnel)
                        self.all_sprites_list.append(funnel)
                upgrade.kill()

        #collision checking 4 (player vs fence)
        hit4 = arcade.check_for_collision_with_list(self.player_sprite,self.fence_sprites_list)
        if len(hit4)!=0:
            if self.fenceproof >0:
                for fence in hit4:
                    fence.kill()
                self.fenceproof -=1;print("You used your fenceproof!")
            else:
                print("Fence does fatal damage! Instant death.");self.gameover = True

        #collision checking 5 (player vs enemy bullet)
        hit5 = arcade.check_for_collision_with_list(self.player_sprite,self.enemy_bullet_sprites_list)
        if len(hit5)!=0:
            for enemybullet in hit5:
                if enemybullet.type == 'Ruin king':
                    self.hp = int(self.hp*96/100)-enemybullet.damage
                    print("Got hit by Falcon's bullet! hp-4% in addition.")
                elif enemybullet.type == 'Cane':
                    self.nasusstack+=3
                    self.hp-=enemybullet.damage
                    print("The cane just got stronger! hp-",enemybullet.damage,"(stack+3)")
                elif enemybullet.type == 'Hamster shit':
                    if random.randrange(100)>5:
                        self.hp-=enemybullet.damage
                        self.score-=1
                        print("Hamster's shit makes you sick! hp-2, score-1")
                    else:
                        self.hp = int(self.hp*9/10)-enemybullet.damage
                        print("Critical shit! hp-10% in addition.")
                else:
                    self.hp-=enemybullet.damage
                    print("Got hit by",enemybullet.type,"! hp-",enemybullet.damage)
                enemybullet.kill()

        #gameover status
        if self.hp <= 0:
            self.gameover = True
        if self.gameover == True:
            self.finalscore = int((self.score+(self.current_lv-1)*150+(self.bossdefeat)*200)*MUL)
            text_file = open("Score.txt","a")
            text_file.write(f"\n{self.finalscore}:{name} ({STATUS})")
            print("\nGame Over!")
            print("Score =",self.score)
            print("Level reached :",self.current_lv-1,"x 150 =",(self.current_lv-1)*150)
            print("Total boss(es) defeated :",self.bossdefeat ,"x 200 =",self.bossdefeat*200)
            print("Difficulty multiplier :",STATUS,"x",MUL)     
            print("Final score =",self.finalscore)
            if self.bossdefeat >= 3:print("Game complete! Thanks for playing.");text_file.write(" [CLEARED]\n")
            else:text_file.write("\n")
            text_file.close()
            import scoresort
            sys.exit(0)
      
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.SPACE and self.automatic == False and self.timestop<1:
            if self.multigun == True:#เปิดยิง 3 ลูก
                self.shooting(self.player_sprite,0,"images/bullet.png",0.9,3,0)
            else :#no upgrade
                self.shooting(self.player_sprite,0,"images/bullet.png",0.9,1,1)
        if symbol == arcade.key.LEFT and self.timestop<1:self.player_sprite.vx = -1-self.speedup
        if symbol == arcade.key.RIGHT and self.timestop<1:self.player_sprite.vx = 1+self.speedup
        if symbol == arcade.key.UP and self.timestop<1:self.player_sprite.vy = 1+self.speedup
        if symbol == arcade.key.DOWN and self.timestop<1:self.player_sprite.vy = -1-self.speedup
            
    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:self.player_sprite.vx = 0
        elif symbol == arcade.key.UP or symbol == arcade.key.DOWN:self.player_sprite.vy = 0
     
if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
