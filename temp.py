# coding: utf-8
import sys
import pygame
import scene
import tanks
import home
import random
from pygame.locals import *


# 开始界面显示
def show_start_interface(screen, width, height):
	tfont = pygame.font.Font('./font/simhei.ttf', width//4)
	cfont = pygame.font.Font('./font/simhei.ttf', width//20)
	title = tfont.render(u'闯关竞技', True, (255, 0, 0))
	content1 = cfont.render(u'按1键开始游戏', True, (0, 0, 255))
	trect = title.get_rect()
	trect.midtop = (width/2, height/4)
	crect1 = content1.get_rect()
	crect1.midtop = (width/2, height/1.8)
	screen.blit(title, trect)
	screen.blit(content1, crect1)
	pygame.display.update()
   
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					return 1
# 结束界面显示
def show_end_interface(screen, width, height, is_win):
	bg_img = pygame.image.load("./images/others/background.png")
	screen.blit(bg_img, (0, 0))
	if is_win:
		font = pygame.font.Font('./font/simhei.ttf', width//10)
		content = font.render(u'恭喜通关！', True, (255, 0, 0))
		rect = content.get_rect()
		rect.midtop = (width/2, height/2)
		screen.blit(content, rect)
	else:
		fail_img = pygame.image.load("./images/others/gameover.png")
		rect = fail_img.get_rect()
		rect.midtop = (width/2, height/2)
		screen.blit(fail_img, rect)
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()


# 关卡切换
def show_switch_stage(screen, width, height, stage):
	bg_img = pygame.image.load("./images/others/background.png")
	screen.blit(bg_img, (0, 0))
	font = pygame.font.Font('./font/simhei.ttf', width//10)
	content = font.render(u'第%d关' % stage, True, (0, 255, 0))
	rect = content.get_rect()
	rect.midtop = (width/2, height/2)
	screen.blit(content, rect)
	pygame.display.update()
	delay_event = pygame.constants.USEREVENT
	pygame.time.set_timer(delay_event, 1000)
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
			if event.type == delay_event:
				return


# 子弹类
class Bullet(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# 子弹四个方向(上下左右)
		self.bullets = ['./images/bullet/bullet_up.png', './images/bullet/bullet_down.png', './images/bullet/bullet_left.png', './images/bullet/bullet_right.png']
		# 子弹方向(默认向上)
		self.direction_x, self.direction_y = 0, -1
		self.bullet = pygame.image.load(self.bullets[0])
		self.rect = self.bullet.get_rect()
		# 在坦克类中再赋实际值
		self.rect.left, self.rect.right = 0, 0
		# 速度
		self.speed = 100000
	# 改变子弹方向
	def turn(self, direction_x, direction_y):
		self.direction_x, self.direction_y = direction_x, direction_y
		if self.direction_x == 0 and self.direction_y == -1:
			self.bullet = pygame.image.load(self.bullets[0])
		elif self.direction_x == 0 and self.direction_y == 1:
			self.bullet = pygame.image.load(self.bullets[1])
		elif self.direction_x == -1 and self.direction_y == 0:
			self.bullet = pygame.image.load(self.bullets[2])
		elif self.direction_x == 1 and self.direction_y == 0:
			self.bullet = pygame.image.load(self.bullets[3])
		else:
			raise ValueError('Bullet class -> direction value error.')
	# 移动
	def move(self):
		#self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.rect = self.rect.move(self.speed, self.speed)
		# 到地图边缘后消失
		if (self.rect.top < 3) or (self.rect.bottom > 630 - 3) or (self.rect.left < 3) or (self.rect.right > 630 - 3):
			self.being = False


# 主函数
def main():
	# 初始化
	pygame.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((630, 630))
	pygame.display.set_caption("闯关竞技")
	# 加载图片
	bg_img = pygame.image.load("./images/others/background.png")
	# 加载音效
	add_sound = pygame.mixer.Sound("./audios/add.wav")
	add_sound.set_volume(1)
	bang_sound = pygame.mixer.Sound("./audios/bang.wav")
	bang_sound.set_volume(1)
	blast_sound = pygame.mixer.Sound("./audios/blast.wav")
	blast_sound.set_volume(1)
	fire_sound = pygame.mixer.Sound("./audios/fire.wav")
	fire_sound.set_volume(1)
	Gunfire_sound = pygame.mixer.Sound("./audios/Gunfire.wav")
	Gunfire_sound.set_volume(1)
	hit_sound = pygame.mixer.Sound("./audios/hit.wav")
	hit_sound.set_volume(1)
	start_sound = pygame.mixer.Sound("./audios/start.wav")
	start_sound.set_volume(1)
	# 开始界面
	num_player = show_start_interface(screen, 630, 630)
	# 播放游戏开始的音乐
	start_sound.play()
	# 关卡
	stage = 0
	num_stage = 2
	# 游戏是否结束
	is_gameover = False
	# 时钟
	clock = pygame.time.Clock()
	# 主循环
	while not is_gameover:
		# 关卡
		stage += 1
		if stage > num_stage:
			break
		show_switch_stage(screen, 630, 630, stage)
		# 该关卡坦克总数量
		enemytanks_total = min(stage * 3, 80)
		# 场上存在的敌方坦克总数量
		enemytanks_now = 0
		# 场上可以存在的敌方坦克总数量
		enemytanks_now_max = min(max(stage * 2, 4), 8)
		# 精灵组
		tanksGroup = pygame.sprite.Group()
		mytanksGroup = pygame.sprite.Group()
		enemytanksGroup = pygame.sprite.Group()
		bulletsGroup = pygame.sprite.Group()
		mybulletsGroup = pygame.sprite.Group()
		enemybulletsGroup = pygame.sprite.Group()
		myfoodsGroup = pygame.sprite.Group()
		# 自定义事件
		# 	-生成敌方坦克事件
		genEnemyEvent = pygame.constants.USEREVENT
		pygame.time.set_timer(genEnemyEvent, 100)
		# 	-敌方坦克静止恢复事件
		recoverEnemyEvent = pygame.constants.USEREVENT
		pygame.time.set_timer(recoverEnemyEvent, 8000)
		# 	-我方坦克无敌恢复事件
		noprotectMytankEvent = pygame.constants.USEREVENT
		pygame.time.set_timer(noprotectMytankEvent, 8000)
		# 关卡地图
		map_stage = scene.Map(stage)
		# 我方坦克
		tank_player1 = tanks.myTank(1)
		tanksGroup.add(tank_player1)
		mytanksGroup.add(tank_player1)
		is_switch_tank = True
		player1_moving = False
		# 为了轮胎的动画效果
		time = 0
	# 敌方坦克
		for i in range(0, 3):
			if enemytanks_total > 0:
				enemytank = tanks.enemyTank(i)
				tanksGroup.add(enemytank)
				enemytanksGroup.add(enemytank)
				enemytanks_now += 1
				enemytanks_total -= 1
		# 大本营
		myhome = home.Home()
		# 出场特效
		appearance_img = pygame.image.load("./images/others/appear.png").convert_alpha()
		appearances = []
		appearances.append(appearance_img.subsurface((0, 0), (48, 48)))
		appearances.append(appearance_img.subsurface((48, 0), (48, 48)))
		appearances.append(appearance_img.subsurface((96, 0), (48, 48)))
        
		# 关卡主循环
		while True:
			if is_gameover is True:
				break
			if enemytanks_total < 1 and enemytanks_now < 1:
				is_gameover = False
				break
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == genEnemyEvent:
					if enemytanks_total > 0:
						if enemytanks_now < enemytanks_now_max:
							enemytank = tanks.enemyTank()
							if not pygame.sprite.spritecollide(enemytank, tanksGroup, False, None):
								tanksGroup.add(enemytank)
								enemytanksGroup.add(enemytank)
								enemytanks_now += 1
								enemytanks_total -= 1
				if event.type == recoverEnemyEvent:
					for each in enemytanksGroup:
						each.can_move = True
				if event.type == noprotectMytankEvent:
					for each in mytanksGroup:
						mytanksGroup.protected = False
			# 检查用户键盘操作
			key_pressed = pygame.key.get_pressed()
			# 玩家
			# WSAD -> 上下左右
			# 空格键射击
			if key_pressed[pygame.K_UP]:
				tanksGroup.remove(tank_player1)
				tank_player1.move_up(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
				tanksGroup.add(tank_player1)
				player1_moving = True
			elif key_pressed[pygame.K_DOWN]:
				tanksGroup.remove(tank_player1)
				tank_player1.move_down(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
				tanksGroup.add(tank_player1)
				player1_moving = True
			elif key_pressed[pygame.K_LEFT]:
				tanksGroup.remove(tank_player1)
				tank_player1.move_left(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
				tanksGroup.add(tank_player1)
				player1_moving = True
			elif key_pressed[pygame.K_RIGHT ]:
				tanksGroup.remove(tank_player1)
				tank_player1.move_right(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
				tanksGroup.add(tank_player1)
				player1_moving = True
			elif key_pressed[pygame.K_SPACE]:
				if not tank_player1.bullet.being:
					fire_sound.play()
					tank_player1.shoot()
			# 背景
			screen.blit(bg_img, (0, 0))
			# 石头墙
			for each in map_stage.brickGroup:
				screen.blit(each.brick, each.rect)
			# 钢墙
			for each in map_stage.ironGroup:
				screen.blit(each.iron, each.rect)

			# 我方坦克
			if tank_player1 in mytanksGroup:
				if is_switch_tank and player1_moving:
					screen.blit(tank_player1.tank_0, (tank_player1.rect.left, tank_player1.rect.top))
					player1_moving = False
				else:
					screen.blit(tank_player1.tank_1, (tank_player1.rect.left, tank_player1.rect.top))
				if tank_player1.protected:
					screen.blit(tank_player1.protected_mask1, (tank_player1.rect.left, tank_player1.rect.top))
			for each in enemytanksGroup:
				# 出生特效
				if each.born:
					if each.times > 0:
						each.times -= 1
						if each.times <= 10:
							screen.blit(appearances[2], (3+each.x*12*24, 3))
						elif each.times <= 20:
							screen.blit(appearances[1], (3+each.x*12*24, 3))
						'''elif each.times <= 30:
							screen.blit(appearances[0], (3+each.x*12*24, 3))
						elif each.times <= 40:
							screen.blit(appearances[2], (3+each.x*12*24, 3))
						elif each.times <= 50:
							screen.blit(appearances[1], (3+each.x*12*24, 3))
						elif each.times <= 60:
							screen.blit(appearances[0], (3+each.x*12*24, 3))
						elif each.times <= 70:
							screen.blit(appearances[2], (3+each.x*12*24, 3))
						elif each.times <= 80:
							screen.blit(appearances[1], (3+each.x*12*24, 3))
						elif each.times <= 90:
							screen.blit(appearances[0], (3+each.x*12*24, 3))'''
					else:
						each.born = False
				else:
					if is_switch_tank:
						screen.blit(each.tank_0, (each.rect.left, each.rect.top))
					else:
						screen.blit(each.tank_1, (each.rect.left, each.rect.top))
					if each.can_move:
						tanksGroup.remove(each)
						each.move(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
						tanksGroup.add(each)
			# 我方子弹
			for tank_player in mytanksGroup:
				if tank_player.bullet.being:
					tank_player.bullet.move()
					screen.blit(tank_player.bullet.bullet, tank_player.bullet.rect)
					# 子弹碰撞敌方子弹
					for each in enemybulletsGroup:
						if each.being:
							if pygame.sprite.collide_rect(tank_player.bullet, each):
								tank_player.bullet.being = False
								each.being = False
								enemybulletsGroup.remove(each)
								break
						else:
							enemybulletsGroup.remove(each)	
					# 子弹碰撞敌方坦克
					for each in enemytanksGroup:
						if each.being:
							if pygame.sprite.collide_rect(tank_player.bullet, each):
								if each.is_red == True:
									each.is_red = False
								each.blood = -1
								each.color = -1
								if each.blood < 0:#射击死亡次数
									bang_sound.play()
									each.being = False
									enemytanksGroup.remove(each)
									enemytanks_now -= 1
									tanksGroup.remove(each)
								else:
									each.reload()
								tank_player.bullet.being = False
								break
						else:
							enemytanksGroup.remove(each)
							tanksGroup.remove(each)
					# 子弹碰撞石头墙
					if pygame.sprite.spritecollide(tank_player.bullet, map_stage.brickGroup, True, None):
						tank_player.bullet.being = False
					# 子弹碰钢墙
					if tank_player.bullet.stronger:
						if pygame.sprite.spritecollide(tank_player.bullet, map_stage.ironGroup, True, None):
							tank_player.bullet.being = False
					else:
						if pygame.sprite.spritecollide(tank_player.bullet, map_stage.ironGroup, False, None):
							tank_player.bullet.being = False
			# 敌方子弹
			for each in enemytanksGroup:
				if each.being:
					if each.can_move and not each.bullet.being:
						enemybulletsGroup.remove(each.bullet)
						each.shoot()
						enemybulletsGroup.add(each.bullet)
					if not each.born:
						if each.bullet.being:
							each.bullet.move()
							screen.blit(each.bullet.bullet, each.bullet.rect)
							# 子弹碰撞我方坦克
							for tank_player in mytanksGroup:
								if pygame.sprite.collide_rect(each.bullet, tank_player):
									if not tank_player.protected:
										bang_sound.play()
										tank_player.life -= 1
										if tank_player.life < 0:
											mytanksGroup.remove(tank_player)
											tanksGroup.remove(tank_player)
											if len(mytanksGroup) < 1:
												is_gameover = True
										else:
											tank_player.reset()
									each.bullet.being = False
									enemybulletsGroup.remove(each.bullet)
									break
							# 子弹碰撞石头墙
							if pygame.sprite.spritecollide(each.bullet, map_stage.brickGroup, True, None):
								each.bullet.being = False
								enemybulletsGroup.remove(each.bullet)
							# 子弹碰钢墙
							if each.bullet.stronger:
								if pygame.sprite.spritecollide(each.bullet, map_stage.ironGroup, True, None):
									each.bullet.being = False
							else:
								if pygame.sprite.spritecollide(each.bullet, map_stage.ironGroup, False, None):
									each.bullet.being = False
				else:
					enemytanksGroup.remove(each)
					tanksGroup.remove(each)
		
			pygame.display.flip()
			clock.tick(60)
	if not is_gameover:
		show_end_interface(screen, 630, 630, True)
	else:
		show_end_interface(screen, 630, 630, False)


if __name__ == '__main__':
	main()
