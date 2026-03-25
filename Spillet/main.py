import pygame
import sys
import random
import copy

pygame.init()
#Basic Pygame
pygame.display.set_caption("Cryptoscam")
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BG_COLOR = (30, 30, 30)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
game_speed = 2
holding_card = False
heldcard = None
hoveredcard = None
originalcardpos = None
handmargin = 200
enemypoints = 3
currentwave = 0
currentstage = 0
gamephase = 0

playerhp = 10
troverdighet = 10

font = pygame.font.SysFont("Comic Sans", 15)

#Sprites
basiccard = pygame.image.load("Spillet\Media\Sprites\BasicKort.png")
lanesprite = pygame.image.load("Spillet\Media\Sprites\Lane.png")

jackalope = pygame.image.load("Spillet\Media\Sprites\polaroids\jackalope.png")
hugag = pygame.image.load("Spillet\Media\Sprites\polaroids\hugag.png")
kanin = pygame.image.load("Spillet\Media\Sprites\polaroids\Kanin.png")
ulv = pygame.image.load(r"Spillet\Media\Sprites\polaroids\Ulv.png")



class card:
    def __init__(self, info, abilities, stats, image, name):
        self.rarity = info[0]
        self.played = info[1]
        self.side = info[2]
        self.abilities = abilities
        self.x = 0
        self.visualx = 0
        self.y = HEIGHT-250
        self.visualy = HEIGHT-250
        self.order = 0
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
    


    def attack(self, orderinlane):
        if(self.side == "Player"): #SpillerAngrep
            if spawnedenemycards[orderinlane] != None:
                spawnedenemycards[orderinlane].hp -= self.dmg

                #Attack-Abilities
                for ability in self.abilities:
                    if ability == "Move Over":
                        if len(spawnedenemycards) > orderinlane + 1:
                            if spawnedenemycards[orderinlane + 1] == None:
                                spawnedenemycards[orderinlane + 1] = spawnedenemycards[orderinlane]
                                spawnedenemycards[orderinlane] = None

        if(self.side == "Enemy"):
            if playedcards[orderinlane] != None:
                playedcards[orderinlane].hp -= self.dmg
            else:
                damageplayer(self.dmg)
        

def damageplayer(damage):
    global playerhp
    playerhp -=damage
    if playerhp <= 0:
        print("Game Over")
        pygame.quit()
        sys.exit()

#Card Creation Info
#Første Array er info, [Rarity, Spillt / i hånden, Spiller eller fiende]
#Andre array er abilites
#Andre Vector 3 er stats
#Bildefil er etter det
#Navn på kortet etter det

deck = [
    card([0, True, "Player"], [], pygame.math.Vector3(3,2,2), hugag, "Hugag"),
    card([0, True, "Player"], [], pygame.math.Vector3(3,2,2), hugag, "Hugag"),
    card([0, True, "Player"], [], pygame.math.Vector3(2,1,1), jackalope, "Jackalope"),
    card([0, True, "Player"], [], pygame.math.Vector3(2,1,1), jackalope, "Jackalope"),
    card([0, True, "Player"], [], pygame.math.Vector3(2,1,1), jackalope, "Jackalope"),
    card([0, True, "Player"], ["Extinct+2"], pygame.math.Vector3(2,1,2), jackalope, "Ball-Tailed Cat")
]

hand = [
    card([0, True, "Player"], [], pygame.math.Vector3(2,1,1), jackalope, "Jackalope"),
    card([0, True, "Player"], [], pygame.math.Vector3(2,1,1), jackalope, "Jackalope"),
    card([0, True, "Player"], ["Rolling"], pygame.math.Vector3(1,1,2), jackalope, "Hoop Snake"),
    card([0, True, "Player"], [], pygame.math.Vector3(3,2,2), hugag, "Hugag"),
    
]

playedcards = []


class lane:
    def __init__(self, position, laneinfo, PorE, cardinlane , enemies):
        self.position = position
        self.laneinfo = laneinfo
        self.enemies = enemies
        self.card = cardinlane
        self.pore = PorE
    
    def draw(self, surface):
        surface.blit(lanesprite, (self.position.x, self.position.y))

    def spawnenemy(self):
        self.enemies[0]

class enemypool:
    def __init__(self, name, enemies):
        self.name = name
        self.enemies = enemies

enemypools = [
    enemypool("Level 1 Pool", [
        card([0, True, "Enemy"], pygame.math.Vector3(0, 0, 0), pygame.math.Vector3(2, 1 ,1), kanin, "Kanin"),
    ]),
    enemypool("Level 2 Pool", [
        card([0, True, "Enemy"], pygame.math.Vector3(0, 0, 0), pygame.math.Vector3(2, 1 ,1), kanin, "Kanin"),
        card([0, True, "Enemy"], pygame.math.Vector3(0, 0, 0), pygame.math.Vector3(2, 2 ,2), ulv, "Ulv"),
    ])
]
def findpool(poolname):
    for pool in enemypools:
        if pool.name == poolname:
            return pool
    print("Found no pool with name " + poolname)


class stage:
    def __init__(self, waves, name, forcedenemies, pools):
        self.waves = waves
        self.name = name
        self.forcedenemies = forcedenemies
        self.pools = pools
        if len(pools)/2 != waves:
            print("Error during stage creation. Waves is not equal to length of pools")
            pygame.quit()
            sys.exit()


stages = [
    stage(3, "First Level", None,[ #Enemypools[] is pool used for fetching enemies for stage, next number is how many tokens can be used to spawn enemies
        findpool("Level 1 Pool"), 2,
        findpool("Level 1 Pool"), 3,
        findpool("Level 2 Pool"), 4,
    ]),
]


waves = []
spawnedenemycards = []
lanes = []
enemylanes = []

for i in range(5):
    lanes.append(lane(pygame.math.Vector2((((WIDTH-50 * 2) / 5) * i)+50, 475), "Standard", "Player" ,None ,[]))
for i in range(5):
    enemylanes.append(lane(pygame.math.Vector2((((WIDTH-50 * 2) / 5) * i)+50, 175), "Standard", "Enemy" , None ,[]))
for i in range(len(lanes)):
    playedcards.append(None)
for i in range(len(lanes)):
    spawnedenemycards.append(None)

def spawnwave(stage):
    global currentwave

    points = stage.pools[((currentwave+1)*2)-1]
    
    while points > 0:
        chosenenemy = random.choice(stage.pools[((currentwave+1)*2)-2].enemies)
        while chosenenemy.cost > points:
            chosenenemy = random.choice(stage.pools[((currentwave+1)*2)-2].enemies)
        global spawnedenemycards
        chosenlane = random.randint(0,4)
        if spawnedenemycards[chosenlane] == None:
            spawnedenemycards[chosenlane] = copy.copy(chosenenemy)
            spawnedenemycards[chosenlane].visualx = enemylanes[chosenlane].position.x
            spawnedenemycards[chosenlane].visualy = enemylanes[chosenlane].position.y - 200
            points -= chosenenemy.cost
    


def drawcard():
    if len(deck) > 0:
        hand.append(deck[0])
        deck.pop(0)

def attackphase():
    loops = 0
    for i in lanes:
        if spawnedenemycards[loops] != None:
            spawnedenemycards[loops].attack(loops)
        if playedcards[loops] != None:
            playedcards[loops].attack(loops)
        if playedcards[loops] != None:
            if playedcards[loops].hp <= 0:
                playedcards[loops] = None
        if spawnedenemycards[loops] != None:
            if spawnedenemycards[loops].hp <= 0:
                spawnedenemycards[loops] = None
        loops +=1
    
    drawcard()

    global troverdighet
    troverdighet += 2
    if troverdighet > 10:
        troverdighet = 10
    

    #Etter angrep abilites
    for card in playedcards:
        if card != None:
            for ability in card.abilities:
                if ability == "Rolling":
                    card.dmg += 1
    

    #Sjekker om noen fiender er igjen
    for i in spawnedenemycards:
        if i != None:
            return
    
    global currentwave
    currentwave += 1
    if currentwave < stages[currentstage].waves:
        spawnwave(stages[currentstage])
    else:
        print("You win!")
        global gamephase 
        gamephase = 1


spawnwave(stages[currentstage])
while True:
    handloops = 0
    for card in hand:
        card.order = handloops
        handloops+= 1
        card.x = ((WIDTH-handmargin * 2) / len(hand)) * card.order + handmargin
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        for card in reversed(hand):
            if card == heldcard or heldcard == None:
                if pygame.mouse.get_pos()[0] > card.visualx and pygame.mouse.get_pos()[1] > card.visualy:
                    if pygame.mouse.get_pos()[0] < card.visualx + basiccard.get_width() and pygame.mouse.get_pos()[1] < card.visualy + basiccard.get_height():
                        card.visualx = pygame.mouse.get_pos()[0] - (basiccard.get_width() / 2)
                        card.visualy = pygame.mouse.get_pos()[1] - (basiccard.get_height() / 2)
                        heldcard = card
    if heldcard != None:
        heldcard.visualx = pygame.mouse.get_pos()[0] - (basiccard.get_width() / 2)
        heldcard.visualy = pygame.mouse.get_pos()[1] - (basiccard.get_height() / 2)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                drawcard()
                print("Drawing Card")
            if event.key == pygame.K_2:
                attackphase()
                print("Attacking")
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if heldcard != None:
                    for lane in lanes:
                        if pygame.mouse.get_pos()[0] > lane.position.x and pygame.mouse.get_pos()[1] > lane.position.y:
                            if pygame.mouse.get_pos()[0] < lane.position.x + lanesprite.get_width() and pygame.mouse.get_pos()[1] < lane.position.y + lanesprite.get_height():
                                if heldcard.cost <= troverdighet and playedcards[lanes.index(lane)] == None:
                                    lane.cardinlane = heldcard
                                    hand.remove(heldcard)
                                    playedcards[lanes.index(lane)] = heldcard
                                    troverdighet -= heldcard.cost

                                    for ability in heldcard.abilities:
                                        if ability == "Extinct+2":
                                            troverdighet += 2
                heldcard = None
                originalcardpos = None



    screen.fill(BG_COLOR)

    for lane in lanes:
        lane.draw(screen)
    for lane in enemylanes:
        lane.draw(screen)
    for playedcard in playedcards:
        if playedcard != None:
            playedcard.x = lanes[(playedcards.index(playedcard))].position.x + 2
            playedcard.y = lanes[(playedcards.index(playedcard))].position.y + 2
            playedcard.draw(screen)
    
    for enemycard in spawnedenemycards:
        if enemycard != None:
            enemycard.x = enemylanes[(spawnedenemycards.index(enemycard))].position.x+2
            enemycard.y = enemylanes[(spawnedenemycards.index(enemycard))].position.y+2
            enemycard.draw(screen)
    
    for card in hand:
        if heldcard == None:
            if pygame.mouse.get_pos()[0] > card.x and pygame.mouse.get_pos()[1] > card.y:
                if pygame.mouse.get_pos()[0] < card.x + basiccard.get_width() and pygame.mouse.get_pos()[1] < card.y + basiccard.get_height():
                    card.hover = True
        if not card == heldcard:
            card.draw(screen)
    if not card == None:
        for card in hand:
            if card == heldcard:
                card.draw(screen)
    text_surface = font.render("HP: " + str(int(playerhp)) + "/10", True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (100,100)
    screen.blit(text_surface, text_rect)
    text_surface = font.render("Troverdighet: " + str(troverdighet) + "/10", True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (100,120)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
