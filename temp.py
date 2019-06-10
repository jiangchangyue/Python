# coding: utf-8
import sys
import pygame
import leads
from pygame.locals import *


# 开始界面
def show_start_interface(screen, width, height):
	tfont = pygame.font.Font('./font/simhei.ttf', width//4)#设置字体
	cfont = pygame.font.Font('./font/simkai.ttf', width//20)
	title = tfont.render(u'穿越沙漠', True, (255, 255, 255))
	content1 = cfont.render(u'按1键开始游戏', True, (100, 100, 255))
	trect = title.get_rect()
	trect.midtop = (width/2, height/4)#设置文字位置
	crect1 = content1.get_rect()
	crect1.midtop = (width/2, height/1.8)
	screen.blit(title, trect)
	screen.blit(content1, crect1)#将文字加在矩阵上
	pygame.display.update()#重置
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:#用户是否关掉游戏界面
				pygame.quit()
				exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					return 1
# 结束界面
def show_end_interface(screen, width, height, is_win):
	bg_img = pygame.image.load("./images/others/background.png")
	screen.blit(bg_img, (0, 0))#设置图片位置
	if is_win:#通关
		font = pygame.font.Font('./font/simhei.ttf', width//10)
		content = font.render(u'恭喜通关！', True, (255, 100, 0))
		rect = content.get_rect()
		rect.midtop = (width/2, height/2)
		screen.blit(content, rect)
	else:
		fail_img = pygame.image.load("./images/others/gameover.png")
		rect = fail_img.get_rect()
		rect.midtop = (width/2, height/2)
		screen.blit(fail_img, rect)
	pygame.display.update()#重置
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
	screen.blit(content, rect)#将内容放在矩阵上
	pygame.display.update()
	delay_event = pygame.constants.USEREVENT
	pygame.time.set_timer(delay_event, 1000)#设置计时器，隔1000ms跳转界面
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
			if event.type == delay_event:
				return
# 墙
class Brick(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.brick = pygame.image.load('./images/scene/brick.png')
		self.rect = self.brick.get_rect()
		self.being = False#墙呈现出来
# 地图
class Map():
	def __init__(self, stage):
		self.brickGroup = pygame.sprite.Group()
		self.brick1Group  = pygame.sprite.Group()
		if stage == 1:
			self.stage1()
		elif stage == 2:
			self.stage2()
    #关卡一
	def stage1(self):
		for x in [2, 6, 7, 18, 19, 23]:
			for y in [2, 3, 4, 5, 6, 7, 8, 9, 17, 18, 19, 20]:
				self.brick = Brick()
				self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
				self.brick.being = True#子弹与墙接触墙消失
				self.brickGroup.add(self.brick)
		for x in [10, 15]:
			for y in [3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20]:
				self.brick = Brick()
				self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24#设置在画布中的左边和上边
				self.brick.being = True
				self.brickGroup.add(self.brick)
		for x in [5, 6, 7, 18, 19, 20]:
			for y in [13, 14]:
				self.brick = Brick()
				self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
				self.brick.being = True
				self.brickGroup.add(self.brick)
		for x in [12, 13]:
			for y in [16]:
				self.brick = Brick()
				self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
				self.brick.being = True
				self.brickGroup.add(self.brick)
		for x, y in [(0, 14), (1, 14), (12, 6), (13, 6), (12, 7), (13, 7), (24, 14), (25, 14)]:
			self.brick = Brick()
			self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
			self.brick.being = True
			self.brickGroup.add(self.brick)
	# 关卡二
	def stage2(self):
		for x in [2, 3, 6, 7, 18, 19, 22, 23]:
			for y in [2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22]:
				self.brick = Brick()
				self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
				self.brick.being = True
				self.brickGroup.add(self.brick)
		for x in [10, 11, 14, 15]:
			for y in [2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20]:
				self.brick = Brick()
				self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
				self.brick.being = True
				self.brickGroup.add(self.brick)
		for x in [5, 6, 7, 18, 19, 20]:
			for y in [13, 14]:
				self.brick = Brick()
				self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
				self.brick.being = True
				self.brickGroup.add(self.brick)
		for x in [12, 13]:
			for y in [16, 17]:
				self.brick = Brick()
				self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
				self.brick.being = True
				self.brickGroup.add(self.brick)
		for x, y in [(0, 14), (1, 14), (12, 6), (13, 6), (12, 7), (13, 7), (24, 14), (25, 14)]:
			self.brick = Brick()
			self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
			self.brick.being = True
			self.brickGroup.add(self.brick)
	def protect_home(self):
		for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
			self.brick = Brick()
			self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
			self.brick.being = True
			self.brickGroup.add(self.brick)

class Home(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.homes = ['./images/home/home1.png', './images/home/home2.png', './images/home/home_destroyed.png']
		self.home = pygame.image.load(self.homes[0])
		self.home = pygame.image.load(self.homes[0])
		self.rect = self.home.get_rect()
		self.rect.left, self.rect.top = (3 + 12 * 24, 3 + 24 * 24)
		self.rect.left, self.rect.top = (3+12*24,3+12*24)
		self.alive = True#敌人和主角初始地方
	def set_dead(self):
		self.home = pygame.image.load(self.homes[-1])
		self.alive = False
def main():
	pygame.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((630, 630))
	pygame.display.set_caption("穿越沙漠")
	bg_img = pygame.image.load("./images/others/background.png")
	bang_sound = pygame.mixer.Sound("./audios/bang.wav")
	bang_sound.set_volume(1)
	fire_sound = pygame.mixer.Sound("./audios/fire.wav")
	fire_sound.set_volume(1)
	start_sound = pygame.mixer.Sound("./audios/start.wav")
	start_sound.set_volume(1)#将图片音频传给变量
	# 开始界面
	num_player = show_start_interface(screen, 630, 630)
	start_sound.play()
	stage = 0
	num_stage = 2
	is_gameover = False
	clock = pygame.time.Clock()
	while not is_gameover:
		# 关卡
		stage += 1
		if stage > num_stage:
			break
		show_switch_stage(screen, 630, 630, stage)
		enemyleads_total = min(stage * 6, 80)
		enemyleads_now = 0
		enemyleads_now_max = min(max(stage * 2, 4), 8)
		# 精灵组
		leadsGroup = pygame.sprite.Group()
		myleadsGroup = pygame.sprite.Group()
		enemyleadsGroup = pygame.sprite.Group()
		bulletsGroup = pygame.sprite.Group()
		mybulletsGroup = pygame.sprite.Group()
		enemybulletsGroup = pygame.sprite.Group()
		myfoodsGroup = pygame.sprite.Group()
		#生成敌方角色
		genEnemyEvent = pygame.constants.USEREVENT
		pygame.time.set_timer(genEnemyEvent, 100)
		#敌方角色静止恢复
		recoverEnemyEvent = pygame.constants.USEREVENT
		pygame.time.set_timer(recoverEnemyEvent, 8000)
		#我方角色恢复
		noprotectMyleadEvent = pygame.constants.USEREVENT
		pygame.time.set_timer(noprotectMyleadEvent, 8000)
		map_stage = Map(stage)
		# 我方角色
		lead_player1 = leads.mylead(1)
		leadsGroup.add(lead_player1)
		myleadsGroup.add(lead_player1)
		is_switch_lead = True
		player1_moving = False
		time = 0
	# 敌方角色
		for i in range(0, 3):
			if enemyleads_total > 0:
				enemylead = leads.enemylead(i)
				leadsGroup.add(enemylead)
				enemyleadsGroup.add(enemylead)
				enemyleads_now += 1
				enemyleads_total -= 1
		index = Home()
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
			if enemyleads_total < 1 and enemyleads_now < 1:
				is_gameover = False
				break
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == genEnemyEvent:
					if enemyleads_total > 0:
						if enemyleads_now < enemyleads_now_max:
							enemylead = leads.enemylead()
							if not pygame.sprite.spritecollide(enemylead, leadsGroup, False, None):
								leadsGroup.add(enemylead)#增加敌人
								enemyleadsGroup.add(enemylead)
								enemyleads_now += 1
								enemyleads_total -= 1
				if event.type == recoverEnemyEvent:
					for each in enemyleadsGroup:
						each.can_move = True
				if event.type == noprotectMyleadEvent:
					for each in myleadsGroup:
						myleadsGroup.protected = False
			key_pressed = pygame.key.get_pressed()
			#上下左右 # 空格键射击
			if key_pressed[pygame.K_UP]:
				leadsGroup.remove(lead_player1)
				lead_player1.move_up(leadsGroup, map_stage.brickGroup, map_stage.brick1Group, index)
				leadsGroup.add(lead_player1)
				player1_moving = True
			elif key_pressed[pygame.K_DOWN]:
				leadsGroup.remove(lead_player1)
				lead_player1.move_down(leadsGroup, map_stage.brickGroup, map_stage.brick1Group, index)
				leadsGroup.add(lead_player1)
				player1_moving = True
			elif key_pressed[pygame.K_LEFT]:
				leadsGroup.remove(lead_player1)
				lead_player1.move_left(leadsGroup, map_stage.brickGroup, map_stage.brick1Group, index)
				leadsGroup.add(lead_player1)
				player1_moving = True
			elif key_pressed[pygame.K_RIGHT ]:
				leadsGroup.remove(lead_player1)
				lead_player1.move_right(leadsGroup, map_stage.brickGroup, map_stage.brick1Group, index)
				leadsGroup.add(lead_player1)
				player1_moving = True
			elif key_pressed[pygame.K_SPACE]:
				if not lead_player1.bullet.being:
					fire_sound.play()
					lead_player1.shoot()
			screen.blit(bg_img, (0, 0))
			for each in map_stage.brickGroup:
				screen.blit(each.brick, each.rect)
			# 我方角色
			if lead_player1 in myleadsGroup:
				if is_switch_lead and player1_moving:
					screen.blit(lead_player1.lead_0, (lead_player1.rect.left, lead_player1.rect.top))
					player1_moving = False
				else:
					screen.blit(lead_player1.lead_1, (lead_player1.rect.left, lead_player1.rect.top))
				if lead_player1.protected:
					screen.blit(lead_player1.protected_mask1, (lead_player1.rect.left, lead_player1.rect.top))
			for each in enemyleadsGroup:
				# 出生特效
				if each.born:
					if each.times > 0:
						each.times -= 1
						if each.times <= 10:
							screen.blit(appearances[2], (3+each.x*12*24, 3))
						elif each.times <= 20:
							screen.blit(appearances[1], (3+each.x*12*24, 3))
					else:
						each.born = False
				else:
					if is_switch_lead:
						screen.blit(each.lead_0, (each.rect.left, each.rect.top))
					else:
						screen.blit(each.lead_1, (each.rect.left, each.rect.top))
					if each.can_move:
						leadsGroup.remove(each)
						each.move(leadsGroup, map_stage.brickGroup, map_stage.brick1Group, index)
						leadsGroup.add(each)
			# 我方子弹
			for lead_player in myleadsGroup:
				if lead_player.bullet.being:
					lead_player.bullet.move()
					screen.blit(lead_player.bullet.bullet, lead_player.bullet.rect)
					# 子弹碰撞敌方子弹
					for each in enemybulletsGroup:
						if each.being:
							if pygame.sprite.collide_rect(lead_player.bullet, each):
								lead_player.bullet.being = False
								each.being = False
								enemybulletsGroup.remove(each)
								break
						else:
							enemybulletsGroup.remove(each)	
					# 子弹碰撞敌方角色
					for each in enemyleadsGroup:
						if each.being:
							if pygame.sprite.collide_rect(lead_player.bullet, each):
								each.blood = -1
								each.color = -1
								if each.blood < 0:
									bang_sound.play()
									each.being = False
									enemyleadsGroup.remove(each)
									enemyleads_now -= 1
									leadsGroup.remove(each)
								else:
									each.reload()
								lead_player.bullet.being = False
								break
						else:
							enemyleadsGroup.remove(each)
							leadsGroup.remove(each)
					# 子弹碰墙
					if pygame.sprite.spritecollide(lead_player.bullet, map_stage.brickGroup, True, None):
						lead_player.bullet.being = False
			# 敌方子弹
			for each in enemyleadsGroup:
				if each.being:
					if each.can_move and not each.bullet.being:
						enemybulletsGroup.remove(each.bullet)
						each.shoot()
						enemybulletsGroup.add(each.bullet)
					if not each.born:
						if each.bullet.being:
							each.bullet.move()
							screen.blit(each.bullet.bullet, each.bullet.rect)
							# 子弹碰撞我方角色
							for lead_player in myleadsGroup:
								if pygame.sprite.collide_rect(each.bullet, lead_player):
									if not lead_player.protected:
										bang_sound.play()
										lead_player.life -= 1
										if lead_player.life < 0:
											myleadsGroup.remove(lead_player)
											leadsGroup.remove(lead_player)
											if len(myleadsGroup) < 1:
												is_gameover = True
										else:
											lead_player.reset()
									each.bullet.being = False
									enemybulletsGroup.remove(each.bullet)
									break
							# 子弹碰墙
							if pygame.sprite.spritecollide(each.bullet, map_stage.brickGroup, True, None):
								each.bullet.being = False
								enemybulletsGroup.remove(each.bullet)
				else:
					enemyleadsGroup.remove(each)
					leadsGroup.remove(each)
			pygame.display.flip()
			clock.tick(60)
	if not is_gameover:
		show_end_interface(screen, 630, 630, True)
	else:
		show_end_interface(screen, 630, 630, False)
if __name__ == '__main__':
	main()
