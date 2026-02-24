import pygame
import sys

pygame.init()

pygame.display.set_caption("Menu Example")
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BG_COLOR = (30, 30, 30)
game_speed = 2
move_direction = 0

basiccard = pygame.image.load("BasicKort.png")

class card:
    def __init__(self, rarity,x,y):
        self.rarity = rarity
        self.x = x
        self.y = y

    def draw(self, surface):
        if self.rarity == 0:
            surface.blit(basiccard, (self.x, self.y))

cards = [
    card(0, 100, 100)
]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill(BG_COLOR)
    
    for card in cards:
        card.draw(screen)
    if cards[0].x <= 101:
        move_direction = 0
    if cards[0].x >= 399:
        move_direction = 1
    if move_direction == 0:
        cards[0].x = pygame.math.lerp(cards[0].x, 400, game_speed/500)
    if move_direction == 1:
        cards[0].x = pygame.math.lerp(cards[0].x, 100, game_speed/500)

    pygame.display.flip()
