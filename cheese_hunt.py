import pygame
import random
import os
import time
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 735
HEIGHT = 735
M = 21 #columns
N = 21 #rows
tile_size = WIDTH / M
FPS = 60 #Frames per second

#Colours
WHITE = (255, 255, 255)
BLACK = (0,0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#Speeds
player_speed = tile_size/15
chef_speed = tile_size/35

pygame.init() #initialize all imported pygame modules
pygame.mixer.init() #initializes the mixer module (used for loading and playing sounds)
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #initializes a screen for display
pygame.display.set_caption("Noname") #Set the current window caption
clock = pygame.time.Clock() #create an object to help track time

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, BLUE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surf.blit(text_surface, text_rect)

class Maze(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(wall_img, (tile_size, tile_size))
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.radius = int(tile_size * .475)
		#pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(player_img, (tile_size, tile_size))
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.radius = int(tile_size *.475)
		#pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.centerx = 3*tile_size/2
		self.rect.top = tile_size
		self.index = 22
		self.speedx = 0 
		self.speedy = 0
		self.state = 3
		self.prevstate = 3

	def update(self):
		self.speedx = 0
		self.speedy = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			#if self.index % M != 0 and maze[self.index - 1] == 0:				
				self.state = 0
				new_image = pygame.transform.rotate(self.image, (self.prevstate-self.state)*90)
				old_center = self.rect.center
				self.image = new_image
				self.rect = self.image.get_rect()
				self.rect.center = old_center
				self.speedx = -player_speed
				#self.index -= 1
		elif keystate[pygame.K_RIGHT]:
			#if self.index % M != M-1 and maze[self.index + 1] == 0:
				self.state = 2
				new_image = pygame.transform.rotate(self.image, (self.prevstate-self.state)*90)
				old_center = self.rect.center
				self.image = new_image
				self.rect = self.image.get_rect()
				self.rect.center = old_center
				self.speedx = player_speed
				#self.index += 1
		elif keystate[pygame.K_UP]:
			#if self.index > M-1 and maze[self.index - M] == 0:
				self.state = 1
				new_image = pygame.transform.rotate(self.image, (self.prevstate-self.state)*90)
				old_center = self.rect.center
				self.image = new_image
				self.rect = self.image.get_rect()
				self.rect.center = old_center
				self.speedy = -player_speed
				#self.index -= M
		elif keystate[pygame.K_DOWN]:
			#if self.index < N * M - M and maze[self.index + M] == 0:
				self.state = 3
				new_image = pygame.transform.rotate(self.image, (self.prevstate-self.state)*90)
				old_center = self.rect.center
				self.image = new_image
				self.rect = self.image.get_rect()
				self.rect.center = old_center
				self.speedy = player_speed
				#self.index += M
		self.prevstate = self.state
		self.rect.x += self.speedx
		# Check to see if the wall hit the player
		hits = pygame.sprite.spritecollide(player, mazes, False, pygame.sprite.collide_circle)  
		if hits:
			self.rect.x -= self.speedx
		self.rect.y += self.speedy
		# Check to see if the wall hit the player
		hits = pygame.sprite.spritecollide(player, mazes, False, pygame.sprite.collide_circle)  
		if hits:
			self.rect.y -= self.speedy

class Cheese(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(cheese_img, (tile_size, tile_size))
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.radius = int(tile_size * .475)
		i = 0
		while maze[i] != 0:
			i = random.randrange(0, M * N - 1)
		self.rect.centerx = (i % M)*tile_size + tile_size/2
		self.rect.top = (int(i / M))*tile_size

class Chef(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(chef_img, (int(tile_size), int(tile_size)))
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.radius = int(tile_size * .5)
		#pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
		i = 0
		while maze[i] != 0 or (i / M) < (M / 4) or (i % M) < (M / 4):
			i = random.randrange(0, M * N )
		self.rect.centerx = (i % M)*tile_size + tile_size/2
		self.rect.top = int(i / M)*tile_size
		self.speedx = 0 
		self.speedy = 0
		self.dir = random.randrange(0,4)
		self.index = i

	def update(self):
		self.speedx = 0
		self.speedy = 0
		
		if self.dir == 1: #Left
			if maze[self.index - 1] == 0:
				if self.rect.centerx < ((self.index - 1) % M)*tile_size + tile_size/2:
					self.index -= 1
					self.speedx = 0
				else:
					self.speedx = -chef_speed
			else:
				self.dir = random.randrange(0,4)
		elif self.dir == 2: #Up
			if maze[self.index - M] == 0:
				if self.rect.centery < int((self.index - M) / M)*tile_size + tile_size/2:
					self.index -= M
					self.speedy = 0
				else:
					self.speedy = -chef_speed
			else:
				self.dir = random.randrange(0,4)
		elif self.dir == 3: #Right
			if maze[self.index + 1] == 0:
				if self.rect.centerx > ((self.index + 1) % M)*tile_size + tile_size/2:
					self.index += 1
					self.speedx = 0
				else:
					self.speedx = chef_speed
			else:
				self.dir = random.randrange(0,4)
		elif self.dir == 0: #Down
			if maze[self.index + M] == 0:
				if self.rect.centery > int((self.index + M) / M)*tile_size + tile_size/2:
					self.index += M
					self.speedy = 0
				else:
					self.speedy = chef_speed
			else:
				self.dir = random.randrange(0,4)

		self.rect.x += self.speedx
		# Check to see if a wall hit the chef
		hits = pygame.sprite.spritecollide(self, mazes, False, pygame.sprite.collide_circle)  
		if hits:
			self.rect.x -= self.speedx
			self.dir = random.randrange(0,4)

		self.rect.y += self.speedy
		# Check to see if a wall hit the chef
		hits = pygame.sprite.spritecollide(self, mazes, False, pygame.sprite.collide_circle)  
		if hits:
			self.rect.y -= self.speedy
			self.dir = random.randrange(0,4)

# Load all images
player_img = pygame.image.load(path.join(img_dir, "mouse2.png")).convert()
chef_img = pygame.image.load(path.join(img_dir, "chef.jpg")).convert()
wall_img = pygame.image.load(path.join(img_dir, "wall2.jpg")).convert()
cheese_img = pygame.image.load(path.join(img_dir, "cheese.jpg")).convert()

all_sprites = pygame.sprite.Group()
mazes = pygame.sprite.Group()
cheese = pygame.sprite.Group()
chef = pygame.sprite.Group()
maze =  [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
		  1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 
		  1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 
		  1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 
		  1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 
		  1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 
		  1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 
		  1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 
		  1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 
		  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 
		  1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 
		  1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 
		  1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 
		  1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 
		  1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 
		  1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 
		  1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 
		  1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 
		  1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 
		  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 
		  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
bx = 0
by = 0
for i in maze:
	if maze[ bx + (by * M) ] == 1:
		n = Maze()
		n.rect.centerx = bx * tile_size + tile_size/2
		n.rect.top = by*tile_size
		all_sprites.add(n)
		mazes.add(n)
	bx = bx + 1
	if bx > M - 1:
		bx = 0
		by = by + 1

for i in range(3):
	n = Cheese()
	all_sprites.add(n)
	cheese.add(n)

for i in range(10):
	n = Chef()
	all_sprites.add(n)
	chef.add(n)

player = Player()
all_sprites.add(player)
score = 0

# Game loop
running = True
while running:
	# Keep the loop running at the right speed
	clock.tick(FPS)
	# Process input (events)
	for event in pygame.event.get():
		#check for closing window
		if event.type == pygame.QUIT:
			running = False

	# Update
	all_sprites.update()

	# Check to see if the player hits a cheese
	hits = pygame.sprite.spritecollide(player, cheese, True, pygame.sprite.collide_circle)  
	if hits:
		score += 10
		#draw_text(screen, "10", 40, player.rect.x, player.rect.y)
		#time.sleep(0.1)
		n = Cheese()
		all_sprites.add(n)
		cheese.add(n)

	# Check to see if the player hits a chef
	hits = pygame.sprite.spritecollide(player, chef,False, pygame.sprite.collide_circle)  
	if hits:
		print("Your Score: " + str(score))
		running = False
	# Draw
	screen.fill(WHITE)
	#self.maze.draw(screen, wall_img)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 40, WIDTH / 2, -2)
	# After drawing everything, flip the display
	pygame.display.flip()