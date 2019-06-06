解决关卡问题，目前设置两关后通关

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
