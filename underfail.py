import pygame
from pygame.locals import*
img = pygame.image.load('soul sprite.png')
img = pygame.transform.scale(img,(70,70))
import random
import time
import sys


class Game:
	def __init__(self, config, unlocks):
		self.config = config
		self.unlocks = unlocks

	def run(self):
		pygame.init()
		self.start_time = time.time()
		self.total_time = -1
		self.Black = (0,0,0)
		self.White = (255,255,255)
		self.yellow = (248,240,192)
		self.purple = (174,295,255)

		self.boundary_x = 400
		self.boundary_y = 400
		self.boundary_length = 1120
		self.boundary_height = 580
		self.boundary_right = self.boundary_x + self.boundary_length

		self.player_health = (50)
		self.player_x = (700)
		self.player_y = (700)
		self.player = (self.player_x, self.player_y, self.player_health)

		self.projectiles = []	
		self.hit_box = pygame.Rect(self.player_x, self.player_y, 70, 70)

		self.ScreenWidth = 1920
		self.ScreenHeight = 1080
		self.size = (self.ScreenWidth, self.ScreenHeight)
		self.screen = pygame.display.set_mode(self.size) 
		pygame.display.set_caption("underfail demo")
		self.clock = pygame.time.Clock()
		self.y_acceleration = 0
		self.x_acceleration = 0
		self.font = pygame.font.SysFont('Calibri', 25, True, False)
		self.gameover_font = pygame.font.SysFont('Calibri', 50, True, False)
		
		self.configeration = ()

		self.loop()

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.screen.fill(self.Black)
				self.done = True
				sys.exit()

			if event.type == pygame.KEYUP:
				self.x_acceleration = 0
				self.y_acceleration = 0


		#if event.type == pygame.KEYDOWN:
		keys=pygame.key.get_pressed()
		if self.hit_box.x < 1445:
			if keys[pygame.K_RIGHT]:
				if self.x_acceleration < 10:
					self.x_acceleration += 1
		else:
			if self.x_acceleration > 0:
				self.x_acceleration = 0
		
		if self.hit_box.x > 405:
			if keys[pygame.K_LEFT]:
				if self.x_acceleration > -10:
					self.x_acceleration -=1
		else:
			if self.x_acceleration < 0:
				self.x_acceleration = 0

		if self.hit_box.y < 900:
			if keys[pygame.K_DOWN]:
				if self.y_acceleration < 10:
					self.y_acceleration += 1
		else:
			if self.y_acceleration > 0:
				self.y_acceleration = 0

		if self.hit_box.y > 410:
			if keys[pygame.K_UP]:
				if self.y_acceleration > -10:
					self.y_acceleration -=1
		else:
			if self.y_acceleration < 0:
				self.y_acceleration = 0

		if self.player_health < 1:
			if keys[pygame.K_SPACE]:
				self.done =True

	def update_projectiles(self):
		# Loop through the projectiles and do stuff
		for projectile in self.projectiles:
			if projectile['x'] >= self.boundary_right:
				self.projectiles.remove(projectile)
			else:
				projectile['x'] = projectile['x'] + 10
			if self.hit_box.collidepoint(projectile['x'], projectile['y']):
				self.player_health -= self.config['player_health_deduction']
				self.projectiles.remove(projectile) 

	def update_player_health(self):
		if self.player_health < 1 and self.total_time == -1:
			self.total_time = self.time_elapsed

		if self.player_health < 1:
			self.game_over()


	def game_over(self):
		self.screen.fill(self.Black)
		time_string = time.strftime("%M:%S", time.gmtime(self.total_time))
		timetext = self.gameover_font.render(time_string, True, self.White)
		timetext_size = self.gameover_font.size(time_string)
		self.screen.blit(timetext,[(self.ScreenWidth/2)-timetext_size[0]/2,250])
		if self.config['name'] == 'easy' and self.total_time > 60:
			self.unlocks.append('hard')
		if self.config['name'] == 'hard' and self.total_time > 60:
			self.unlocks.append('epic')
		if self.config['name'] == 'epic' and self.total_time > 60:
			self.unlocks.append('legendary')
		if self.config['name'] == 'legendary' and self.total_time > 60:
			self.unlocks.append('godsent')
		if self.config['name'] == 'godsent' and self.total_time > 30:
			self.unlocks.append('devilsent')

	def draw_health(self):

		text = self.font.render("HEALTH",True, self.White)
		pygame.draw.rect(self.screen, self.White, [350, 250, self.player_health*2, 20])
		self.screen.blit(text,[250,250])

	def timer(self):		
		self.time_elapsed = time.time() - self.start_time
		timetext = self.font.render(time.strftime("%M:%S", time.gmtime(self.time_elapsed)),True, self.White)
		self.screen.blit(timetext,[1250,250])

	def drawing(self):		
		self.screen.fill(self.Black)
		self.draw_health()

		pygame.draw.rect(self.screen, self.White, [400,400, self.boundary_length, self.boundary_height],2)

		for projectile in self.projectiles:
			pygame.draw.line( self.screen, self.White,
				[projectile['x'], projectile['y']], [projectile['x'] - 30, projectile['y'] ])
		self.screen.blit(img,(self.hit_box))
	



	def loop(self):
		self.done = False
		while not self.done:

			self.handle_events()

			
			self.hit_box.x += self.x_acceleration
			self.hit_box.y += self.y_acceleration

			if random.randint(0, self.config['inverse_projectile_probability']) == 0 and len(self.projectiles) < self.config['max_projectiles']:
				self.projectiles.append({'x': random.randrange(400,450), 'y': random.randrange(400,980)})

		
			self.update_projectiles()
			self.drawing()
			self.timer()
			self.update_player_health()

			pygame.display.flip()

			self.clock.tick(60)

class Menu:
	def run(self, unlocks):
		#do something
		self.unlocks = unlocks
		self.Black = (0,0,0)
		self.White = (255,255,255)
		self.yellow = (248,240,192)
		self.purple = (174,195,255)
		self.selected_config = 'easy'
		self.button_width = 220
		self.button_height = 50
		self.easy_button_rect = pygame.Rect(290, 290, self.button_width, self.button_height)
		self.hard_button_rect = pygame.Rect(590, 290, self.button_width, self.button_height)
		self.epic_button_rect = pygame.Rect(890, 290, self.button_width, self.button_height)
		self.legendary_button_rect = pygame.Rect(1190, 290, self.button_width, self.button_height)
		self.godsent_button_rect = pygame.Rect(445, 590, self.button_width, self.button_height)
		self.devilsent_button_rect = pygame.Rect(1045, 590, self.button_width, self.button_height)

		self.ScreenWidth = 1920
		self.ScreenHeight = 1080
		self.size = (self.ScreenWidth, self.ScreenHeight)

		pygame.init()
		self.font = pygame.font.SysFont('Calibri', 25, True, False)
		self.screen = pygame.display.set_mode(self.size) 
		self.clock = pygame.time.Clock()
		self.loop()

	def config(self):
		easy_config = {
			'name': 'easy',
			'player_health_deduction': 5,
			'inverse_projectile_probability': 10,
			'max_projectiles': 10,
			'minimum_projectiles':0
		}

		hard_config = {
			'name': 'hard',
			'player_health_deduction': 10,
			'inverse_projectile_probability': 7,
			'max_projectiles': 20,
			'minimum_projectiles':0
		}
		
		epic_config = {
			'name': 'epic',
			'player_health_deduction': 15,
			'inverse_projectile_probability': 5,
			'max_projectiles': 30,
			'minimum_projectiles':0
		}

		legendary_config = {
			'name': 'legendary',
			'player_health_deduction': 20,
			'inverse_projectile_probability': 3,
			'max_projectiles': 40,
			'minimum_projectiles':0
		}

		godsent_config = {
			'name': 'godsent',
			'player_health_deduction': 35,
			'inverse_projectile_probability': 2,
			'max_projectiles': 70,
			'minimum_projectiles':0
		}

		devilsent_config = {
			'name': 'devilsent',
			'player_health_deduction': 50,
			'inverse_projectile_probability': 1,
			'max_projectiles': 85,
			'minimum_projectiles':0
		}
		# decide which config to return
		if self.selected_config == 'easy':
			return easy_config
		if self.selected_config == 'hard':
			return hard_config
		if self.selected_config == 'epic':
			return epic_config
		if self.selected_config == 'legendary':
			return legendary_config
		if self.selected_config == 'godsent':
			return godsent_config
		if self.selected_config == 'devilsent':
			return devilsent_config
	def mouse_interation(self):
		self.ev = pygame.event.get()
		for event in self.ev:
			if event.type == pygame.QUIT:
				sys.exit()			
			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				if self.easy_button_rect.collidepoint(pos):
					self.done = True
					self.selected_config = 'easy'
				if self.hard_button_rect.collidepoint(pos):
					self.done = True
					self.selected_config = 'hard'
				if self.epic_button_rect.collidepoint(pos):
					self.done = True
					self.selected_config = 'epic'
				if self.legendary_button_rect.collidepoint(pos):
					self.done = True
					self.selected_config = 'legendary'
				if self.godsent_button_rect.collidepoint(pos):
					self.done = True
					self.selected_config = 'godsent'
				if self.devilsent_button_rect.collidepoint(pos):
					self.done = True
					self.selected_config = 'devilsent'

	def drawing(self):		
		self.screen.fill(self.Black)



		easy_text = self.font.render("Easy(learn)",True, self.White)
		hard_text = self.font.render("Hard(apprentice)",True, self.White)
		epic_text = self.font.render("Epic(sensei)",True, self.White)
		legendary_text = self.font.render("Legendary(pure skill)",True, self.White)
		godsent_text = self.font.render("GodSent(god spawn)",True, self.Black)
		devilsent_text = self.font.render("DevilSent(devil spawn)",True, self.White)

			
		pygame.draw.rect(self.screen, self.White, self.easy_button_rect,2)
		self.screen.blit(easy_text,[300,300])
		
		if 'hard' in self.unlocks:	
			pygame.draw.rect(self.screen, self.White, self.hard_button_rect,2)
			self.screen.blit(hard_text,[600,300])
		
		if 'epic' in self.unlocks:	
			pygame.draw.rect(self.screen, self.White, self.epic_button_rect,2)
			self.screen.blit(epic_text,[900,300])

		if 'legendary' in self.unlocks:	
			pygame.draw.rect(self.screen, self.White, self.legendary_button_rect,2)
			self.screen.blit(legendary_text,[1200,300])
		
		if 'godsent' in self.unlocks:
			pygame.draw.rect(self.screen, self.yellow, self.godsent_button_rect,0)
			self.screen.blit(godsent_text,[450,600])

		if 'devilsent' in self.unlocks:
			pygame.draw.rect(self.screen, self.purple, self.devilsent_button_rect,0)
			self.screen.blit(devilsent_text,[1050,600])


	def loop(self):
		self.done = False
		while not self.done:

			self.mouse_interation()

			self.drawing()

			pygame.display.flip()

			self.clock.tick(60)




unlocks = []
while True:
	underfail_menu = Menu()
	underfail_menu.run(unlocks)

	config = underfail_menu.config()

	underfail_game = Game(config, unlocks)
	underfail_game.run()



























