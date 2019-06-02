# -*- coding: utf-8 -*-
"""
Created on Fri May 31 23:59:21 2019

@author: Jiang123
"""

import sys
import pygame
#import leads
import random
from pygame.locals import *

# 子弹类
class Bullet(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.bullets = ['./images/bullet/bullet_up.png', './images/bullet/bullet_down.png', './images/bullet/bullet_left.png', './images/bullet/bullet_right.png']
		# 子弹方向(默认向上)
		self.direction_x, self.direction_y = 0, -1
		self.bullet = pygame.image.load(self.bullets[0])
		self.rect = self.bullet.get_rect()
		self.rect.left, self.rect.right = 0, 0
		self.speed = 10
		self.being = False
		self.stronger = False
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
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		# 到地图边缘后消失
		if (self.rect.top < 3) or (self.rect.bottom > 630 - 3) or (self.rect.left < 3) or (self.rect.right > 630 - 3):
			self.being = False

# 我方角色类
class mylead(pygame.sprite.Sprite):
	def __init__(self, player):
		pygame.sprite.Sprite.__init__(self)
		self.leads = ['./images/mylead/lead_T1_0.png', './images/mylead/lead_T1_1.png', './images/mylead/lead_T1_2.png']
		self.level = 0
		# 载入(两个lead为了特效)
		self.lead = pygame.image.load(self.leads[self.level]).convert_alpha()
		self.lead_0 = self.lead.subsurface((0, 0), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 0), (48, 48))
		self.rect = self.lead_0.get_rect()
		self.direction_x, self.direction_y = 0, -1
		self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24
		self.speed = 8
		self.being = True
		self.life = 3
		self.protected = False
		self.bullet = Bullet()
	# 射击
	def shoot(self):
		self.bullet.being = True
		self.bullet.turn(self.direction_x, self.direction_y)
		if self.direction_x == 0 and self.direction_y == -1:
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.bottom = self.rect.top - 1
		elif self.direction_x == 0 and self.direction_y == 1:
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.top = self.rect.bottom + 1
		elif self.direction_x == -1 and self.direction_y == 0:
			self.bullet.rect.right = self.rect.left - 1
			self.bullet.rect.top = self.rect.top + 20
		elif self.direction_x == 1 and self.direction_y == 0:
			self.bullet.rect.left = self.rect.right + 1
			self.bullet.rect.top = self.rect.top + 20
		else:
			raise ValueError('mylead class -> direction value error.')
		if self.level == 0:
			self.bullet.speed = 12
			self.bullet.stronger = False
		elif self.level == 1:
			self.bullet.speed = 12
			self.bullet.stronger = False
		elif self.level == 2:
			self.bullet.speed = 12
			self.bullet.stronger = True
		elif self.level == 3:
			self.bullet.speed = 16
			self.bullet.stronger = True
		else:
			raise ValueError('mylead class -> level value error.')
	# 等级提升
	def up_level(self):
		if self.level < 3:
			self.level += 1
		try:
			self.lead = pygame.image.load(self.leads[self.level]).convert_alpha()
		except:
			self.lead = pygame.image.load(self.leads[-1]).convert_alpha()
	# 向上
	def move_up(self, leadGroup, brickGroup, ironGroup, myhome):
		self.direction_x, self.direction_y = 0, -1
		# 先移动后判断
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.lead_0 = self.lead.subsurface((0, 0), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 0), (48, 48))
		# 是否可以移动
		is_move = True
		# 地图顶端
		if self.rect.top < 3:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞墙
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
			pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞其他角色
		if pygame.sprite.spritecollide(self, leadGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 向下
	def move_down(self, leadGroup, brickGroup, ironGroup, myhome):
     #def move_down(self, leadGroup, brickGroup, ironGroup):
		self.direction_x, self.direction_y = 0, 1
		# 先移动后判断
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.lead_0 = self.lead.subsurface((0, 48), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 48), (48, 48))
		# 是否可以移动
		is_move = True
		# 地图底端
		if self.rect.bottom > 630 - 3:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞墙
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
			pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞其他角色
		if pygame.sprite.spritecollide(self, leadGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 向左
	def move_left(self, leadGroup, brickGroup, ironGroup, myhome):
		self.direction_x, self.direction_y = -1, 0
		# 先移动后判断
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.lead_0 = self.lead.subsurface((0, 96), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 96), (48, 48))
		# 是否可以移动
		is_move = True
		# 地图左端
		if self.rect.left < 3:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞墙
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
			pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞其他角色
		if pygame.sprite.spritecollide(self, leadGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 向右
	def move_right(self, leadGroup, brickGroup, ironGroup, myhome):
		self.direction_x, self.direction_y = 1, 0
		# 先移动后判断
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.lead_0 = self.lead.subsurface((0, 144), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 144), (48, 48))
		# 是否可以移动
		is_move = True
		# 地图右端
		if self.rect.right > 630 - 3:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞墙
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
			pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞其他角色
		if pygame.sprite.spritecollide(self, leadGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 死后重置
	def reset(self):
		self.level = 0
		self.protected = False
		self.lead = pygame.image.load(self.leads[self.level]).convert_alpha()
		self.lead_0 = self.lead.subsurface((0, 0), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 0), (48, 48))
		self.rect = self.lead_0.get_rect()
		self.direction_x, self.direction_y = 0, -1
		self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24
		self.speed = 8
# 敌方角色类
global enemylead
class enemylead(pygame.sprite.Sprite):
	def __init__(self, x=None, kind=None, is_red=None):
		pygame.sprite.Sprite.__init__(self)
		# 用于给刚生成的角色播放出生特效
		self.born = True
		self.times = 90
		if kind is None:
			self.kind = random.randint(0, 3)
		else:
			self.kind = kind
		# 所有角色
		self.leads1 = ['./images/enemylead/enemy_1_0.png', './images/enemylead/enemy_1_1.png', './images/enemylead/enemy_1_2.png', './images/enemylead/enemy_1_3.png']
		self.leads2 = ['./images/enemylead/enemy_2_0.png', './images/enemylead/enemy_2_1.png', './images/enemylead/enemy_2_2.png', './images/enemylead/enemy_2_3.png']
		self.leads3 = ['./images/enemylead/enemy_3_0.png', './images/enemylead/enemy_3_1.png', './images/enemylead/enemy_3_2.png', './images/enemylead/enemy_3_3.png']
		self.leads4 = ['./images/enemylead/enemy_4_0.png', './images/enemylead/enemy_4_1.png', './images/enemylead/enemy_4_2.png', './images/enemylead/enemy_4_3.png']
		self.leads = [self.leads1, self.leads2, self.leads3, self.leads4]
		# 是否携带食物(红色的角色携带食物)
		if is_red is None:
			self.is_red = random.choice((True, False, False, False, False))
		else:
			self.is_red = is_red
		if self.is_red:
			self.color = 3
		else:
			self.color = random.randint(0, 2)
		self.blood = self.color
		self.lead = pygame.image.load(self.leads[self.kind][self.color]).convert_alpha()
		self.lead_0 = self.lead.subsurface((0, 48), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 48), (48, 48))
		self.rect = self.lead_0.get_rect()
		# 角色位置
		if x is None:
			self.x = random.randint(0, 2)
		else:
			self.x = x
		self.rect.left, self.rect.top = 3 + self.x * 12 * 24, 3
		self.can_move = True
		self.speed = max(3 - self.kind, 1)
		self.direction_x, self.direction_y = 0, 1
		self.being = True
		self.bullet = Bullet()
	# 射击
	def shoot(self):
		self.bullet.being = True
		self.bullet.turn(self.direction_x, self.direction_y)
		if self.direction_x == 0 and self.direction_y == -1:
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.bottom = self.rect.top - 1
		elif self.direction_x == 0 and self.direction_y == 1:
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.top = self.rect.bottom + 1
		elif self.direction_x == -1 and self.direction_y == 0:
			self.bullet.rect.right = self.rect.left - 1
			self.bullet.rect.top = self.rect.top + 20
		elif self.direction_x == 1 and self.direction_y == 0:
			self.bullet.rect.left = self.rect.right + 1
			self.bullet.rect.top = self.rect.top + 20
		else:
			raise ValueError('enemylead class -> direction value error.')
	# 随机移动
	def move(self, leadGroup, brickGroup, ironGroup, myhome):
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		is_move = True
		if self.direction_x == 0 and self.direction_y == -1:
			self.lead_0 = self.lead.subsurface((0, 0), (48, 48))
			self.lead_1 = self.lead.subsurface((48, 0), (48, 48))
			if self.rect.top < 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		elif self.direction_x == 0 and self.direction_y == 1:
			self.lead_0 = self.lead.subsurface((0, 48), (48, 48))
			self.lead_1 = self.lead.subsurface((48, 48), (48, 48))
			if self.rect.bottom > 630 - 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		elif self.direction_x == -1 and self.direction_y == 0:
			self.lead_0 = self.lead.subsurface((0, 96), (48, 48))
			self.lead_1 = self.lead.subsurface((48, 96), (48, 48))
			if self.rect.left < 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		elif self.direction_x == 1 and self.direction_y == 0:
			self.lead_0 = self.lead.subsurface((0, 144), (48, 48))
			self.lead_1 = self.lead.subsurface((48, 144), (48, 48))
			if self.rect.right > 630 - 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		else:
			raise ValueError('enemylead class -> direction value error.')
		if pygame.sprite.spritecollide(self, brickGroup, False, None) \
			or pygame.sprite.spritecollide(self, ironGroup, False, None) \
			or pygame.sprite.spritecollide(self, leadGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
			is_move = False
		if pygame.sprite.collide_rect(self, myhome):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
			is_move = False
		return is_move
	# 重新载入角色
	def reload(self):
		self.lead = pygame.image.load(self.leads[self.kind][self.color]).convert_alpha()
		self.lead_0 = self.lead.subsurface((0, 48), (48, 48))
		self.lead_1 = self.lead.subsurface((48, 48), (48, 48))
# 开始界面
def show_start_interface(screen, width, height):
	tfont = pygame.font.Font('./font/simhei.ttf', width//4)
	cfont = pygame.font.Font('./font/simkai.ttf', width//20)
	title = tfont.render(u'闯关竞技', True, (255, 255, 255))
	content1 = cfont.render(u'按1键开始游戏', True, (100, 100, 255))
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
# 结束界面
def show_end_interface(screen, width, height, is_win):
	bg_img = pygame.image.load("./images/others/background.png")
	screen.blit(bg_img, (0, 0))
	if is_win:
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
# 墙
class Brick(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.brick = pygame.image.load('./images/scene/brick.png')
		self.rect = self.brick.get_rect()
		self.being = False
# 地图
class Map():
	def __init__(self, stage):
		self.brickGroup = pygame.sprite.Group()
		self.ironGroup  = pygame.sprite.Group()
		self.iceGroup = pygame.sprite.Group()
		self.riverGroup = pygame.sprite.Group()
		self.treeGroup = pygame.sprite.Group()
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
				self.brick.being = True
				self.brickGroup.add(self.brick)
		for x in [10, 15]:
			for y in [3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20]:
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
		self.alive = True
	def set_dead(self):
		self.home = pygame.image.load(self.homes[-1])
		self.alive = False
def main():
	pygame.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((630, 630))
	pygame.display.set_caption("闯关竞技")
	bg_img = pygame.image.load("./images/others/background.png")
	bang_sound = pygame.mixer.Sound("./audios/bang.wav")
	bang_sound.set_volume(1)
	fire_sound = pygame.mixer.Sound("./audios/fire.wav")
	fire_sound.set_volume(1)
	start_sound = pygame.mixer.Sound("./audios/start.wav")
	start_sound.set_volume(1)
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
		# 	-生成敌方角色
		genEnemyEvent = pygame.constants.USEREVENT
		pygame.time.set_timer(genEnemyEvent, 100)
		# 	-敌方角色静止恢复
		recoverEnemyEvent = pygame.constants.USEREVENT
		pygame.time.set_timer(recoverEnemyEvent, 8000)
		# 	-我方角色无敌恢复
		noprotectMyleadEvent = pygame.constants.USEREVENT
		pygame.time.set_timer(noprotectMyleadEvent, 8000)
		map_stage = Map(stage)
		# 我方角色
		lead_player1 = mylead(1)
		leadsGroup.add(lead_player1)
		myleadsGroup.add(lead_player1)
		is_switch_lead = True
		player1_moving = False
		time = 0
	# 敌方角色
		for i in range(0, 3):
			if enemyleads_total > 0:
				enemyleadss = enemylead(i)
				leadsGroup.add(enemyleadss)
				enemyleadsGroup.add(enemyleadss)
				enemyleads_now += 1
				enemyleads_total -= 1
		myhome = Home()
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
							enemylead = enemylead()
							if not pygame.sprite.spritecollide(enemylead, leadsGroup, False, None):
								leadsGroup.add(enemylead)
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
				lead_player1.move_up(leadsGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
				leadsGroup.add(lead_player1)
				player1_moving = True
			elif key_pressed[pygame.K_DOWN]:
				leadsGroup.remove(lead_player1)
				lead_player1.move_down(leadsGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
				leadsGroup.add(lead_player1)
				player1_moving = True
			elif key_pressed[pygame.K_LEFT]:
				leadsGroup.remove(lead_player1)
				lead_player1.move_left(leadsGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
				leadsGroup.add(lead_player1)
				player1_moving = True
			elif key_pressed[pygame.K_RIGHT ]:
				leadsGroup.remove(lead_player1)
				lead_player1.move_right(leadsGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
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
						each.move(leadsGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
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
								if each.is_red == True:
									each.is_red = False
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
