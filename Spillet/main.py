import pygame
import sys

pygame.init()
#Basic Pygame
pygame.display.set_caption("Cryptoscam")
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BG_COLOR = (30, 30, 30)
BLACK = (0,0,0)
game_speed = 2
holding_card = False
heldcard = None

font = pygame.font.SysFont("Comic Sans", 15)

#Sprites
basiccard = pygame.image.load("Spillet\Media\Sprites\BasicKort.png")
jackalope = pygame.image.load("Spillet\Media\Sprites\polaroids\jackalope.png")
hugag = pygame.image.load("Spillet\Media\Sprites\polaroids\hugag.png")
kanin = pygame.image.load("Spillet\Media\Sprites\polaroids\Kanin.png")
ulv = pygame.image.load(r"Spillet\Media\Sprites\polaroids\Ulv.png")

class card:
    def __init__(self, info, position, stats, image, name):
        self.rarity = info.x
        if info.y == 0:
            self.played = False
        else:
            self.played = True
        self.lane = info.z
        self.x = position.x
        self.visualx = position.x
        self.y = position.y
        self.visualy = position.y
        self.hp = stats.x
        self.maxhp = stats.x
        self.dmg = stats.y
        self.cost = stats.z
        self.image = image
        self.name = name
        self.hover = False

    def draw(self, surface):
        if self.hover == True:
            self.visualy = pygame.math.lerp(self.visualy, self.y-30, game_speed/50)
        else:
            self.visualy = pygame.math.lerp(self.visualy, self.y, game_speed/25)
        self.visualx = pygame.math.lerp(self.visualx, self.x, game_speed/25)
        if self.played:
            if self.rarity == 0:
                surface.blit(basiccard, (self.visualx, self.visualy))
            surface.blit(self.image, (self.visualx+18, self.visualy+12))
            self.addtext(surface, 4)

        self.hover = False
            

    def addtext(self, surface, lines):
        for line in range(lines):
            if line == 0:
                text_surface = font.render(str(self.name), True, BLACK)
                text_rect = text_surface.get_rect()
                text_rect.center = (self.visualx + text_rect.w, self.visualy+136+(line*20))
                surface.blit(text_surface, text_rect)
            if line == 1:
                text_surface = font.render("HP: " + str(int(self.hp)) + "/" + str(int(self.maxhp)), True, BLACK)
                text_rect = text_surface.get_rect()
                text_rect.center = (self.visualx + text_rect.w, self.visualy+136+(line*20))
                surface.blit(text_surface, text_rect)
            if line == 2:
                text_surface = font.render("DMG: " + str(int(self.dmg)), True, BLACK)
                text_rect = text_surface.get_rect()
                text_rect.center = (self.visualx + text_rect.w, self.visualy+136+(line*20))
                surface.blit(text_surface, text_rect)
            if line == 3:
                text_surface = font.render("COST: " + str(int(self.cost)), True, BLACK)
                text_rect = text_surface.get_rect()
                text_rect.center = (self.visualx + text_rect.w, self.visualy+136+(line*20))
                surface.blit(text_surface, text_rect)

cards = [
    card(pygame.math.Vector3(0, 1, 0), pygame.math.Vector2(100,100), pygame.math.Vector3(2,1,1), jackalope, "Jackalope"),
    card(pygame.math.Vector3(0, 1, 0), pygame.math.Vector2(250,100), pygame.math.Vector3(3,2,2), hugag, "Hugag"),
    card(pygame.math.Vector3(0, 1, 0), pygame.math.Vector2(400,100), pygame.math.Vector3(2,1,1), kanin, "Kanin"),
    card(pygame.math.Vector3(0, 1, 0), pygame.math.Vector2(550,100), pygame.math.Vector3(2,2,1), ulv, "Ulv")
]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                heldcard = None

    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        for card in cards:
            if card == heldcard or heldcard == None:
                if pygame.mouse.get_pos()[0] > card.x and pygame.mouse.get_pos()[1] > card.y:
                    if pygame.mouse.get_pos()[0] < card.x + basiccard.get_width() and pygame.mouse.get_pos()[1] < card.y + basiccard.get_height():
                        card.x = pygame.mouse.get_pos()[0] - (basiccard.get_width() / 2)
                        card.y = pygame.mouse.get_pos()[1] - (basiccard.get_height() / 2)
                        heldcard = card
            
                        
            
            
    screen.fill(BG_COLOR)
    
    for card in cards:
        if heldcard == None:
            if pygame.mouse.get_pos()[0] > card.x and pygame.mouse.get_pos()[1] > card.y:
                if pygame.mouse.get_pos()[0] < card.x + basiccard.get_width() and pygame.mouse.get_pos()[1] < card.y + basiccard.get_height():
                    card.hover = True
        if not card == heldcard:
            card.draw(screen)
    if not card == None:
        for card in cards:
            if card == heldcard:
                card.draw(screen)

    pygame.display.flip()
