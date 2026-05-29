import pygame
import sys
import random
import copy
import os

pygame.init()
#Basic Pygame
pygame.display.set_caption("Cryptoscam: 358/2 Days")
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
clock = pygame.time.Clock()
fakescreen = screen.copy()

BG_COLOR = (30, 30, 30)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
game_speed = 1
holding_card = False
heldcard = None
hoveredcard = None
handmargin = 200
enemypoints = 3
currentwave = 0
currentstage = None
currentmarker = None
currentdifficulty = 1
loops = 0
attackphaseactive = False
HANDHEIGHT = 300
standardcardscale = 1.2

gamephase = 0
changingphase = False
currentshop = None

playerhp = 10
troverdighet = 10
dollars = 5

font = pygame.font.SysFont("Comic Sans", 13)

#Sprites
basiccard = pygame.image.load("Spillet\Media\Sprites\polaroidkort.png")
lanesprite = pygame.image.load("Spillet\Media\Sprites\Lane.png")
mapsprite = pygame.image.load("Spillet\Media\Sprites\mapv2.png")

#Spillerkort Sprites
jackalope = pygame.image.load("Spillet\Media\Sprites\polaroids\jackalope.png")
hugag = pygame.image.load("Spillet\Media\Sprites\polaroids\hugag.png")
hoopsnake = pygame.image.load(r"Spillet\Media\Sprites\polaroids\hoopsnake.png")
thylacine = pygame.image.load(r"Spillet\Media\Sprites\polaroids\thylacine.png")
jerseydevil = pygame.image.load(r"Spillet\Media\Sprites\polaroids\jerseydevil.png")
wendigo = pygame.image.load(r"Spillet\Media\Sprites\polaroids\wendigo.png")

#Fiendekort Sprites
kanin = pygame.image.load("Spillet\Media\Sprites\polaroids\Kanin.png")
ulv = pygame.image.load(r"Spillet\Media\Sprites\polaroids\Ulv.png")
bjoorn = pygame.image.load(r"Spillet\Media\Sprites\polaroids\bjørn.png")
jeger = pygame.image.load(r"Spillet\Media\Sprites\polaroids\jeger.png")

#Ability Sprites



#X Sprites
x1sprite = pygame.image.load(r"Spillet\Media\x\x1.png")
x2sprite = pygame.image.load(r"Spillet\Media\x\x2.png")
x3sprite = pygame.image.load(r"Spillet\Media\x\x3.png")

class timer:
    def __init__(self, timeamount, resultfunction, usefunctionon = "None", functionarguments = None):
        self.timeamount = timeamount
        self.resultfunction = resultfunction
        self.usefunctionon = usefunctionon
        self.starttime = pygame.time.get_ticks()
        self.functionarguments = functionarguments
        
    def checktime(self):
        if pygame.time.get_ticks() > self.starttime + self.timeamount:
            if self.usefunctionon != "None":
                usedfunction = getattr(self.usefunctionon, str(self.resultfunction))
                if self.functionarguments != None:
                    usedfunction(self.functionarguments)
                else:
                    usedfunction()
            else:
                print("attempting to call general function")
                self.resultfunction()
                
            timers.pop(timers.index(self))

timers = []
class map:
    def __init__(self, position):
        self.position = position
        self.velocity = pygame.math.Vector2(0,0)
        self.drag = 0.95

    def draw(self, surface):
        self.velocity *= self.drag
        self.position += self.velocity
        if self.position.y > -75:
            self.velocity.y -= 0.75
        if self.position.y > 0:
            self.position.y = 0
        if self.position.y < mapsprite.get_height() * -1 + 150:
            self.velocity.y += 0.75
        if self.position.y < mapsprite.get_height() * -1 + 75:
            self.position.y = mapsprite.get_height() * -1 + 75
        surface.blit(mapsprite, self.position)

areamap = map(pygame.math.Vector2((WIDTH - mapsprite.get_width())/2, mapsprite.get_height() * -1))

class mapmark:
    def __init__(self, position, connections, stage, finished):
        self.position = position
        self.visualposition = position
        self.connections = connections
        self.stage = stage
        self.finished = finished
        randomsprite = random.randint(1,3)
        if randomsprite == 1:
            self.sprite = x1sprite
        elif randomsprite == 2:
            self.sprite = x2sprite
        elif randomsprite == 3:
            self.sprite = x3sprite

    def draw(self, surface):

        markid = mapmarkers.index(self)
        if markid + 1 <= len(mapmarkers) - 1:
            self.connections = [mapmarkers[markid+1]]

        self.visualposition = pygame.math.Vector2(self.position.x + (WIDTH / 2), areamap.position.y + mapsprite.get_height() - self.position.y - 200)

        if self.connections != None:
            for connection in self.connections:
                if self.finished == False:
                    pygame.draw.line(surface, (199, 12 ,12), self.visualposition, connection.visualposition, 10)
                else:
                    pygame.draw.line(surface, (128, 8 ,8), self.visualposition, connection.visualposition, 10)

        surface.blit(self.sprite, (self.visualposition.x - self.sprite.get_width() / 2, self.visualposition.y - self.sprite.get_height() / 2))
    
    def load(self):
        global currentmarker
        global currentstage
        currentstage = self.stage
        if isinstance(self.stage, stage):
            changephase(0)
            currentmarker = self
            spawnwave(currentstage)
        elif isinstance(self.stage, shop):
            print("Clicked on Shop")
            global currentshop
            currentshop = self.stage
            currentmarker = self
            changephase(2)
            
        

mapmarkers = [
]




class card:
    def __init__(self, info, abilities, stats, image, name):
        self.rarity = info[0]
        self.played = info[1]
        self.side = info[2]
        self.abilities = abilities
        self.x = 0
        self.visualx = 0
        self.y = HEIGHT-HANDHEIGHT
        self.visualy = HEIGHT-HANDHEIGHT
        self.order = 0
        self.hp = stats.x
        self.maxhp = stats.x
        self.dmg = stats.y
        self.ogdmg = stats.y
        self.cost = stats.z
        self.ogcost = stats.z
        self.image = image
        self.name = name
        self.hover = False
        self.lerpspeed = 1
        self.detached = False
        self.animating = False
        self.orderinlane = None
        self.cardscale = standardcardscale

    def draw(self, surface):
        if self.hover == True:
            self.visualy = pygame.math.lerp(self.visualy, self.y-30, game_speed/25 * self.lerpspeed)
        else:
            self.visualy = pygame.math.lerp(self.visualy, self.y, game_speed/12 * self.lerpspeed)
        self.visualx = pygame.math.lerp(self.visualx, self.x, game_speed/12 * self.lerpspeed)
        if self.played:
            surface.blit(pygame.transform.scale(self.image, (125 / self.cardscale, 125 / self.cardscale)), (self.visualx+(12 / self.cardscale), self.visualy+(10 / self.cardscale)))
            
            surface.blit(pygame.transform.scale(basiccard, (144 / self.cardscale, 296 / self.cardscale) ), (self.visualx, self.visualy))
            
            self.addtext(surface, 4)
        loops = 0
        for ability in self.abilities:
            addedtex = pygame.image.load("Spillet/abilityicons/" + str(ability) + ".png")
            surface.blit(pygame.transform.scale(addedtex, (32 / self.cardscale, 32 /self.cardscale)), (self.visualx + 90 / self.cardscale, self.visualy + 195 / self.cardscale + (loops * 35)))
            loops += 1

        self.hover = False
            

    def addtext(self, surface, lines):
        for line in range(lines):
            if line == 0:
                text_surface = font.render(str(self.name), True, BLACK)
                text_rect = text_surface.get_rect()
                text_rect.center = (self.visualx + text_rect.w, self.visualy+(186 / self.cardscale)+(line*20))
                surface.blit(text_surface, text_rect)
            if line == 1:
                text_surface = font.render("HP: " + str(int(self.hp)) + "/" + str(int(self.maxhp)), True, BLACK)
                text_rect = text_surface.get_rect()
                text_rect.center = (self.visualx + text_rect.w, self.visualy+(186 / self.cardscale)+(line*20))
                surface.blit(text_surface, text_rect)
            if line == 2:
                text_surface = font.render("DMG: " + str(int(self.dmg)), True, BLACK)
                text_rect = text_surface.get_rect()
                text_rect.center = (self.visualx + text_rect.w, self.visualy+(186 / self.cardscale)+(line*20))
                surface.blit(text_surface, text_rect)
            if line == 3:
                text_surface = font.render("COST: " + str(int(self.cost)), True, BLACK)
                text_rect = text_surface.get_rect()
                text_rect.center = (self.visualx + text_rect.w, self.visualy+(186 / self.cardscale)+(line*20))
                surface.blit(text_surface, text_rect)
    
    def finishattackanimation(self):
        print("Finishingattackanimation")
        self.detached = False
        self.lerpspeed = 1.0
        global timers
        global loops
        if self.side == "Player":
            if spawnedenemycards[self.orderinlane] != None:
                timers.append(timer(150, "attack", spawnedenemycards[self.orderinlane], self.orderinlane))
                #spawnedenemycards[self.orderinlane].attack(self.orderinlane)
            elif self.orderinlane != 4:
                attackphase()
        if self.side == "Enemy":
            if self.orderinlane != 4:
                timers.append(timer(300, attackphase, "None"))

    def attackanimation(self):
        print("Starting Attackanimation")
        global timers
        timers.append(timer(250, "finishattackanimation", self))
        self.lerpspeed = 0.7
        self.detached = True
        if self.side == "Player":
            self.y -= 50
        else:
            self.y += 50
        
    def takedamage(self, damageamount, attacker = None):
        self.hp -= damageamount

        for ability in self.abilities:
            if ability == "Hide":
                playedcards[playedcards.index(self)] = None
                hand.append(self)
                self.y = HEIGHT-HANDHEIGHT
            if ability == "Spiky+1":
                if attacker != None:
                    attacker.hp -= 1

    def attack(self, orderinlane):
        self.orderinlane = orderinlane
        self.attackanimation()
        if(self.side == "Player"): #SpillerAngrep
            if spawnedenemycards[orderinlane] != None:
                spawnedenemycards[orderinlane].takedamage(self.dmg, self)
                

        #Attack-Abilities
        for ability in self.abilities:
            if ability == "Move Over":
                if len(spawnedenemycards) > orderinlane + 1:
                    if spawnedenemycards[orderinlane + 1] == None:
                        spawnedenemycards[orderinlane + 1] = spawnedenemycards[orderinlane]
                        spawnedenemycards[orderinlane] = None
            if ability == "Rifle":
                randomlane = random.randint(0, len(lanes) - 1)
                if playedcards[randomlane] != None:
                    playedcards[randomlane].takedamage(2)
                else:
                    damageplayer(2)

        if(self.side == "Enemy"):
            if playedcards[orderinlane] != None:
                playedcards[orderinlane].takedamage(self.dmg, self)
            else:
                damageplayer(self.dmg)
    
    def print(self):
        print(self.abilities)
    
    def addability(self, ability):
        if ability not in self.abilities:
            self.abilities.append(ability)

#Card Creation Info
#Første Array er info, [Rarity, Spillt / i hånden, Spiller eller fiende]
#Andre array er abilites
#første Vector 3 er stats
#Bildefil er etter det
#Navn på kortet til slutt

playercarddictionary = [
    card([1, True, "Player"], [], pygame.math.Vector3(2,1,1), jackalope, "Jackalope"),
    card([1, True, "Player"], [], pygame.math.Vector3(3,2,2), hugag, "Hugag"),
    card([1, True, "Player"], ["Extinct+2"], pygame.math.Vector3(2,1,2), thylacine, "Thylacine"),
    card([1, True, "Player"], ["Rolling"], pygame.math.Vector3(1,1,2), hoopsnake, "Hoop Snake"),
    card([2, True, "Player"], ["Hide"], pygame.math.Vector3(5,2,3), jackalope, "Hidebehind"),
    card([1, True, "Player"], ["Move Over"], pygame.math.Vector3(1,1,2), jackalope, "Ball-Tailed Cat"),
    card([1, True, "Player"], [], pygame.math.Vector3(4,4,3), jerseydevil, "Jersey Devil"),
    card([2, True, "Player"], ["Healing+2", "Spiky+1"], pygame.math.Vector3(3,1,4), jackalope, "Cactus Cat"),
]
def findplayercard(cardname):
    for card in playercarddictionary:
        if card.name == cardname:
            card.abilities = copy.deepcopy(card.abilities)
            return copy.copy(card)
    print("Error, found no player card with name %s" % cardname)
    sys.exit()
    pygame.quit()

enemycarddictionary = [
    card([0, True, "Enemy"], [], pygame.math.Vector3(2, 1, 1), kanin, "Kanin"),
    card([0, True, "Enemy"], [], pygame.math.Vector3(2, 2, 2), ulv, "Ulv"),
    card([0, True, "Enemy"], [], pygame.math.Vector3(4, 3, 4), bjoorn, "Bjørn"),
    card([0, True, "Enemy"], ["Rifle"], pygame.math.Vector3(6, 2, 5), jeger, "Jeger"),
    card([0, True, "Enemy"], ["Hunt"], pygame.math.Vector3(8, 8, 6), wendigo, "Wendigo"),
]
def findenemycard(cardname):
    for card in enemycarddictionary:
        if card.name == cardname:
            return copy.copy(card)
    print("Error, found no enemy card with name %s" % cardname)
    sys.exit()
    pygame.quit()

def damageplayer(damage):
    global playerhp
    playerhp -=damage
    if playerhp <= 0:
        print("Game Over")
        pygame.quit()
        sys.exit()



deck = [
    findplayercard("Jackalope"),
    findplayercard("Jackalope"),
    findplayercard("Jackalope"),
    findplayercard("Jackalope"),
    findplayercard("Jackalope"),
    findplayercard("Jackalope"),
    findplayercard("Hoop Snake"),
    findplayercard("Ball-Tailed Cat"),
    findplayercard("Hugag"),
    findplayercard("Hugag"),
    findplayercard("Hugag"),
    findplayercard("Hugag"),
]
random.shuffle(deck)

hand = []

playedcards = []


class lane:
    def __init__(self, position, laneinfo, PorE, cardinlane):
        self.position = position
        self.laneinfo = laneinfo
        self.card = cardinlane
        self.pore = PorE
    
    def draw(self, surface):
        surface.blit(lanesprite, (self.position.x, self.position.y))

class enemypool:
    def __init__(self, name, enemies):
        self.name = name
        self.enemies = enemies

enemypools = [
    enemypool("Kanin", [
        findenemycard("Kanin")
    ]),
    enemypool("UlvKanin", [
        findenemycard("Kanin"),
        findenemycard("Ulv")
    ]),
    enemypool("BjørnUlvKanin", [
        findenemycard("Kanin"),
        findenemycard("Ulv"),
        findenemycard("Bjørn")
    ]),
    enemypool("BjørnUlv", [
        findenemycard("Ulv"),
        findenemycard("Bjørn")
    ]),
    enemypool("JegerUlv", [
        findenemycard("Ulv"),
        findenemycard("Jeger")
    ]),
    enemypool("WendigoUlv", [
        findenemycard("Ulv"),
        findenemycard("Wendigo")
    ])
]

def findpool(poolname):
    for pool in enemypools:
        if pool.name == poolname:
            return copy.copy(pool)
    print("Found no pool with name %s" % poolname)

def findstage(stagename):
    for stage in stages:
        if stage.name == stagename:
            return stage
    print("Found no stage with name %s" % stagename)

class stage:
    def __init__(self, name, waves, forcedenemies, difficulty, pools):
        self.waves = waves
        self.name = name
        self.forcedenemies = forcedenemies
        self.difficulty = difficulty
        self.pools = pools
        if len(pools)/2 != waves:
            print("Error during stage creation. Waves is not equal to length of pools")
            pygame.quit()
            sys.exit()

stages = [ #Her er hva du skal skrive inn for stagen i rekkefølge: Navnet på banen, Hvor mange "Waves" banen består av, Om det er noen tvunget fiender som skal spawne (fungerer ikke akkurat nå), farlighetsgrad og til slutt hvilke pools wavesene bruker og hvor mange tokens hver wave får
    #Vanskelighetsgrad Følger denne formen: 1 - Enkel / Starterbanene, 2 - Baner som kan være en liten trussel tidlig i spillet, 3 - Tidlige bosser og Middels vanskelige baner, 4 - Litt senere bosser og andre vanskelige baner, 5 - Farligste av alle.
    stage("First Level", 3, None, 1, [ #findpool() is pool used for fetching enemies for stage, next number is how many tokens can be used to spawn enemies
        findpool("Kanin"), 2,
        findpool("Kanin"), 3,
        findpool("UlvKanin"), 4,
    ]),
    stage("Second Level", 3, None, 1, [
        findpool("Kanin"), 2,
        findpool("UlvKanin"), 3,
        findpool("UlvKanin"), 4,
    ]),
    stage("Third Level", 3, None, 1, [
        findpool("UlvKanin"), 3,
        findpool("UlvKanin"), 4,
        findpool("BjørnUlvKanin"), 5,
    ]),
    stage("Fourth Level", 3, None, 2, [
        findpool("BjørnUlvKanin"), 5,
        findpool("Kanin"), 2,
        findpool("JegerUlv"), 7,
    ]),
    stage("Sixth Level", 3, None, 1, [
        findpool("UlvKanin"), 4,
        findpool("BjørnUlvKanin"), 5,
        findpool("BjørnUlvKanin"), 7,
    ]),
    stage("WendigoBoss", 2, [findenemycard("Wendigo"), 2], 2, [
        findpool("BjørnUlvKanin"), 6,
        findpool("BjørnUlv"), 4,
    ]),
]

class shop:
    def __init__(self, type, size = 2):
        global currentdifficulty
        self.type = type
        self.size = size + currentdifficulty


        if self.type == "GetCards":
            self.cards = []
            while len(self.cards) < self.size:
                shuffleddict = playercarddictionary
                random.shuffle(shuffleddict)
                for card in shuffleddict:
                    if card.rarity <= currentdifficulty:
                        if card not in self.cards:
                            self.cards.append(card)
                            break
        

        if self.type == "BoostCards":
            rannum = random.randint(0,2)
            if rannum == 0:
                self.boosttype = "dmg"
            if rannum == 1:
                self.boosttype = "hp"
            if rannum == 2:
                self.boosttype = "cost"

def createmapmarkers(markeramount, difficulty):
    for i in range(markeramount):
        if i == 1:
            mapmarkers.append(mapmark(pygame.math.Vector2(0, i * 100), [], None, False))
        else:
            mapmarkers.append(mapmark(pygame.math.Vector2(random.randint(-250, 250), random.randint(-35, 35) + i * 100), [], None, False))
    loops = 0
    for marker in mapmarkers:
        loops += 1
        if loops == markeramount:
            print("Spawning Boss stage")
            if difficulty == 1:
                marker.stage = copy.copy(findstage("FirstBoss"))
        if loops % 2 == 0:
            shuffledstages = stages
            random.shuffle(shuffledstages)
            for stage in shuffledstages:
                if stage.difficulty == difficulty:
                    marker.stage = copy.copy(stage)
        else:
            rannum = random.randint(0,2)
            if rannum == 0:
                marker.stage = shop("GetCards")
                marker.sprite = pygame.image.load(r"Spillet\Media\markericons\getcards.png")
            elif rannum == 1:
                marker.stage = shop("BoostCards")
                marker.sprite = pygame.image.load(r"Spillet\Media\markericons\BoostCards.png")
            elif rannum == 2:
                marker.stage = shop("Transfer")
                marker.sprite = pygame.image.load(r"Spillet\Media\markericons\transfer.png")


createmapmarkers(10, currentdifficulty)

shopslots = [
    lane(pygame.math.Vector2(WIDTH / 2 - 150 - lanesprite.get_width() / 2, 350), "Standard", "Shop" ,None),
    lane(pygame.math.Vector2(WIDTH / 2 + 150 - lanesprite.get_width() / 2, 350), "Standard", "Shop" ,None),
]

waves = []
spawnedenemycards = []
lanes = []
enemylanes = []

for i in range(5):
    lanes.append(lane(pygame.math.Vector2((((WIDTH-50 * 2) / 5) * i)+50, 350), "Standard", "Player" ,None))
for i in range(5):
    enemylanes.append(lane(pygame.math.Vector2((((WIDTH-50 * 2) / 5) * i)+50, 50), "Standard", "Enemy" , None))
for i in range(len(lanes)):
    playedcards.append(None)
for i in range(len(lanes)):
    spawnedenemycards.append(None)

def spawnwave(stage):
    global currentwave
    global spawnedenemycards

    points = stage.pools[((currentwave+1)*2)-1]

    loops = 0
    while points > 0:
        print("Looping through wave spawning")
        loops += 1
        if loops >= 1024:
            print("Infinite Recursion in Enemy Spawning, breaking while loop")
            break
        if None in spawnedenemycards:
            chosenenemy = random.choice(stage.pools[((currentwave+1)*2)-2].enemies)
            while chosenenemy.cost > points:
                loops += 1
                if loops >= 1024:
                    print("Infinite Recursion in Enemy Spawning, breaking while loop")
                    break
                print("Chosen enemy costs too much , reselecting")
                chosenenemy = random.choice(stage.pools[((currentwave+1)*2)-2].enemies)
            
            chosenlane = random.randint(0,4)
            if spawnedenemycards[chosenlane] == None:
                spawnedenemycards[chosenlane] = copy.copy(chosenenemy)
                spawnedenemycards[chosenlane].visualx = enemylanes[chosenlane].position.x
                spawnedenemycards[chosenlane].visualy = enemylanes[chosenlane].position.y - 200
                points -= chosenenemy.cost
        else:
            chosenlane = random.randint(0,4)
            points += spawnedenemycards[chosenlane].cost
            mostexpensiveenemy = None
            excludedenemies = []
            for enemy in stage.pools[((currentwave+1)*2)-2].enemies:
                if enemy.name in excludedenemies:
                    print("Enemy %s is in excluded enemies") % enemy
                if mostexpensiveenemy == None:
                    mostexpensiveenemy = enemy
                elif enemy.cost > mostexpensiveenemy.cost:
                    if enemy.cost <= points:
                        mostexpensiveenemy = enemy
                        print("Grabbing most expensive enemy")
                        print(mostexpensiveenemy.name)
                    else:
                        excludedenemies.append(enemy.name)
            if mostexpensiveenemy == None:
                print("Error: Failed to find most expensive enemy")
            else:
                print("points before spawned = %s" % points)
                
                spawnedenemycards[chosenlane] = copy.copy(mostexpensiveenemy)
                spawnedenemycards[chosenlane].visualx = enemylanes[chosenlane].position.x
                spawnedenemycards[chosenlane].visualy = enemylanes[chosenlane].position.y - 200
                points -= mostexpensiveenemy.cost
                print("points after spawned = %s" % points)
    
    if stage.forcedenemies != None:
        print("Attempting to spawn forced enemies")
        if currentwave == stage.forcedenemies[1]-1:
            if None in spawnedenemycards:
                spawnedenemycards[spawnedenemycards.index(None)] = stage.forcedenemies[0]
            else:
                spawnedenemycards[random.randint(0,4)] = stage.forcedenemies[0]
            
    


def drawcard():
    if len(deck) > 0:
        hand.append(deck[0])
        deck.pop(0)



def changephase(nextphase):
    print("Changing Phase to Phase " + str(nextphase))
    global changingphase
    global gamephase
    changingphase = True
    
    if nextphase == 0:
        global troverdighet
        troverdighet = 10
        global currentwave
        currentwave = 0
        gamephase = 0
        random.shuffle(deck)
        for i in range(4):
            drawcard()
        changingphase = False
    

    if nextphase == 2:
        global shopslots
        gamephase = 2
        if currentshop.type == "GetCards":
            shopslots[0].position = pygame.math.Vector2(-1000, -1000)
            shopslots[1].position = pygame.math.Vector2(-1000, -1000)
            for card in currentshop.cards:
                card.y = 100
        else:
            if currentshop.type == "BoostCards":
                shopslots[0].position = pygame.math.Vector2(WIDTH/2 - lanesprite.get_width() / 2, 100)
                shopslots[1].position = pygame.math.Vector2(-1000, -1000)
            else:
                shopslots[0].position = pygame.math.Vector2(WIDTH / 2 + 150 - lanesprite.get_width() / 2, 100)
                shopslots[1].position = pygame.math.Vector2(WIDTH / 2 - 150 - lanesprite.get_width() / 2, 100)
                    
            for i in range(len(deck)):
                drawcard()
            for card in hand:
                card.y = HEIGHT-HANDHEIGHT
                card.visualy = HEIGHT-HANDHEIGHT
            changingphase = False
    
    if nextphase == 1:
        for card in deck:
            card.y = HEIGHT-HANDHEIGHT
            card.visualy = HEIGHT-HANDHEIGHT
            card.x = 0 - random.randint(-100,100)
        gamephase = 1
        areamap.position.y = -mapsprite.get_height()
        areamap.velocity.y = 35
        for item in hand:
            item.lerpspeed = 0.5
            item.x = -200 - random.randint(-50,50)
            print("Moving item")
        for item in playedcards:
            if item != None:
                item.lerpspeed = 0.5
                item.x = -200 - random.randint(-50,50)
        loadnewmap = True
        global mapmarkers
        for mark in mapmarkers:
            if mark.finished == False:
                loadnewmap = False

        if loadnewmap == True:  
            global currentdifficulty
            print("Creating New Map")
            currentdifficulty += 1
            mapmarkers = []
            createmapmarkers(10, currentdifficulty)
            global playerhp
            playerhp = 10
            
        
        changingphase = False
        


graveyard = [
]
enemygraveyard = [
]

def checkhealth():
    for i in range(len(lanes)):
            if playedcards[i] != None:
                if playedcards[i].hp <= 0:
                    graveyard.append(playedcards[i])
                    playedcards[i] = None
            if spawnedenemycards[i] != None:
                if spawnedenemycards[i].hp <= 0:
                    enemygraveyard.append(spawnedenemycards[i])
                    spawnedenemycards[i] = None
    for i in range(len(hand)):
        if hand[i].hp <= 0:
            graveyard.append(hand[i])
            hand.pop(i)
    
    timers.append(timer(250, finishattackphase, "None"))


def finishattackphase():
    global attackphaseactive
    drawcard()
    global troverdighet
    global playedcards
    global graveyard
    global deck
    global hand
    troverdighet += 2
    if troverdighet > 10:
        troverdighet = 10
    
    attackphaseactive = False

    #Etter angrep abilites
    for card in playedcards:
        if card != None:
            for ability in card.abilities:
                if ability == "Rolling":
                    card.dmg += 1
                if ability == "Healing+2":
                    if len(playedcards) == playedcards.index(card)-1:
                        if playedcards[playedcards.index(card)+1] != None:
                            playedcards[playedcards.index(card)+1].hp += 2
                            if playedcards[playedcards.index(card)+1].hp > playedcards[playedcards.index(card)+1].maxhp:
                                playedcards[playedcards.index(card)+1].hp = playedcards[playedcards.index(card)+1].maxhp
    

        #Sjekker om noen fiender er igjen
    for i in spawnedenemycards:
        if i != None:
            return
    global currentstage
    global currentwave
    currentwave += 1
    if currentwave < currentstage.waves:
        spawnwave(currentstage)
    else:  
        for i in graveyard:
            deck.append(i)
        graveyard = []
        for i in hand:
            deck.append(i)
        hand = []
        for i in playedcards:
            if i != None:
                deck.append(i)
        playedcards = []
        for i in range(len(lanes)):
            playedcards.append(None)
        for i in deck:
            i.y = HEIGHT-HANDHEIGHT
            i.visualy = HEIGHT-HANDHEIGHT
            i.hp = i.maxhp
            i.dmg = i.ogdmg
            i.cost = i.ogcost
        global currentmarker
        if currentmarker != None:
            currentmarker.finished = True
        print("You win!")
        pygame.image.save(fakescreen, "Backgroundphase1.jpeg")
        heldcard == None
        changephase(1)

def attackphase():
    global attackphaseactive
    attackphaseactive = True
    global loops
    if loops < len(lanes):
        if playedcards[loops] != None:
            playedcards[loops].attack(loops)
            loops += 1
        elif spawnedenemycards[loops] != None:
            spawnedenemycards[loops].attack(loops)
            loops += 1
        else:
            loops += 1
            attackphase()
        


    if loops >= len(lanes):
        loops = 0
        timers.append(timer(650, checkhealth, "None"))
        
for i in range(4):
    drawcard()

currentstage = findstage("First Level")
spawnwave(currentstage)

def delayedphase1():
    global hand
    global shopslots
    pygame.image.save(fakescreen, "Backgroundphase1.jpeg")
    if currentshop.type == "Transfer":
        shopslots[0].card = None
    for i in hand:
        if i != None:
            deck.append(i)
    hand = []
    for slot in shopslots:
        if slot.card != None:
            deck.append(copy.copy(slot.card))
            slot.card = None
    random.shuffle(deck)
    for i in deck:
        i.y = HEIGHT-HANDHEIGHT
        i.visualy = HEIGHT-HANDHEIGHT
        i.hp = i.maxhp
        i.dmg = i.ogdmg
        i.cost = i.ogcost
    changephase(1)



while True:
    for timekeeper in timers:
        timekeeper.checktime()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if gamephase == 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    drawcard() #Husk å fjerne denne før du leverer spillet
                    print("Drawing Card")
                if event.key == pygame.K_SPACE:
                    if attackphaseactive == False:
                        loops = 0
                        attackphase()
                        print("Attacking")
                if event.key == pygame.K_2:
                    for enemycard in spawnedenemycards:
                        if enemycard != None:
                            enemycard.hp = 0
                            enemycard.dmg = 0
                            #checkhealth()
                    pass
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if heldcard != None and attackphaseactive == False:
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
                                        for card in spawnedenemycards:
                                            if card != None:
                                                for ability in card.abilities:
                                                    if ability == "Hunt":
                                                        if spawnedenemycards[lanes.index(lane)] == None:
                                                            spawnedenemycards[spawnedenemycards.index(card)] = None
                                                            spawnedenemycards[lanes.index(lane)] = card

                heldcard = None
        
        if gamephase == 1:
            if event.type == pygame.MOUSEWHEEL:
                areamap.velocity.y += event.y
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for marker in mapmarkers:
                        if pygame.mouse.get_pos()[0] > marker.visualposition.x - marker.sprite.get_width() / 2 and pygame.mouse.get_pos()[1] > marker.visualposition.y - marker.sprite.get_height() / 2:
                            if pygame.mouse.get_pos()[0] < marker.visualposition.x + marker.sprite.get_width() / 2 and pygame.mouse.get_pos()[1] < marker.visualposition.y + marker.sprite.get_height() / 2:
                                print("Hit Marker %s" % mapmarkers.index(marker))
                                if marker.stage != None:
                                    print("Marker has stage")
                                    if mapmarkers.index(marker) == 0:
                                        if marker.finished == False:
                                            marker.load()
                                    for connectionmarker in mapmarkers:
                                        if marker in connectionmarker.connections:
                                            print("Found Connection")
                                            if marker.finished == False and connectionmarker.finished == True: 
                                                marker.load()
                                                print("Loading Marker")
                                                
                                break
        
        if gamephase == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if shopslots[0].card != None:
                        if currentshop.type == "BoostCards":
                            if currentshop.boosttype == "dmg":
                                shopslots[0].card.dmg += 1
                                shopslots[0].card.ogdmg += 1
                            if currentshop.boosttype == "hp":
                                shopslots[0].card.hp += 1
                                shopslots[0].card.maxhp += 1
                            if currentshop.boosttype == "cost":
                                shopslots[0].card.cost -= 1
                                shopslots[0].card.ogcost -= 1
                            currentmarker.finished = True
                            timers.append(timer(250, delayedphase1))
                        if currentshop.type == "Transfer":
                            if shopslots[1].card != None:
                                shopslots[0].card.abilities = copy.deepcopy(shopslots[0].card.abilities)
                                for ability in shopslots[1].card.abilities:
                                    if ability not in shopslots[0].card.abilities:
                                        shopslots[0].card.abilities.append(ability)
                                shopslots[1].card = None
                                deck.append(shopslots[0].card)
                                shopslots[0].card = None
                                currentmarker.finished = True
                                timers.append(timer(250, delayedphase1))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if currentshop.type == "GetCards":
                        for card in currentshop.cards:
                            if pygame.mouse.get_pos()[0] > card.visualx and pygame.mouse.get_pos()[1] > card.visualy:
                                if pygame.mouse.get_pos()[0] < card.visualx + basiccard.get_width() and pygame.mouse.get_pos()[1] < card.visualy + basiccard.get_height():
                                    deck.append(copy.copy(card))
                                    card.y += HEIGHT + 150
                                    currentmarker.finished = True
                                    timers.append(timer(100, delayedphase1))
                    else:
                        for card in reversed(hand):
                            if card == heldcard or heldcard == None:
                                if pygame.mouse.get_pos()[0] > card.visualx and pygame.mouse.get_pos()[1] > card.visualy:
                                    if pygame.mouse.get_pos()[0] < card.visualx + basiccard.get_width() and pygame.mouse.get_pos()[1] < card.visualy + basiccard.get_height():
                                        card.visualx = pygame.mouse.get_pos()[0] - (basiccard.get_width() / 2)
                                        card.visualy = pygame.mouse.get_pos()[1] - (basiccard.get_height() / 2)
                                        heldcard = card
                        for lane in shopslots:
                            card = lane.card
                            if card != None:
                                if pygame.mouse.get_pos()[0] > card.visualx and pygame.mouse.get_pos()[1] > card.visualy:
                                    if pygame.mouse.get_pos()[0] < card.visualx + basiccard.get_width() and pygame.mouse.get_pos()[1] < card.visualy + basiccard.get_height():
                                        card.visualx = pygame.mouse.get_pos()[0] - (basiccard.get_width() / 2)
                                        card.visualy = pygame.mouse.get_pos()[1] - (basiccard.get_height() / 2)
                                        heldcard = card
                                        heldcard.detached = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if heldcard != None:
                        for lane in shopslots:
                            if pygame.mouse.get_pos()[0] > lane.position.x and pygame.mouse.get_pos()[1] > lane.position.y:
                                if pygame.mouse.get_pos()[0] < lane.position.x + lanesprite.get_width() and pygame.mouse.get_pos()[1] < lane.position.y + lanesprite.get_height():
                                    if playedcards[shopslots.index(lane)] == None:
                                        if heldcard in hand:
                                            hand.remove(heldcard)
                                        for slot in shopslots:
                                            if slot.card == heldcard:
                                                slot.card = None
                                        heldcard.detached = False
                                        if lane.card != None:
                                            lane.card.y = HEIGHT-HANDHEIGHT
                                            hand.append(lane.card)
                                        lane.card = heldcard
                                    
                                        heldcard = None
                                        break
                        if lane.card == heldcard:
                            hand.append(lane.card)
                            lane.card.y = HEIGHT-HANDHEIGHT
                            lane.card = None
                            
                heldcard = None
                

                                    
                                                

    if gamephase == 0:
        handloops = 0
        for card in hand:
            if changingphase == False:
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



        fakescreen.fill(BG_COLOR)

        for lane in lanes:
            lane.draw(fakescreen)
        for lane in enemylanes:
            lane.draw(fakescreen)
        for playedcard in playedcards:
            if playedcard != None:
                if changingphase == False and playedcard.detached == False:
                    playedcard.x = lanes[(playedcards.index(playedcard))].position.x + 2
                    playedcard.y = lanes[(playedcards.index(playedcard))].position.y + 2
                playedcard.draw(fakescreen)
    
        for enemycard in spawnedenemycards:
            if enemycard != None:
                if enemycard.detached == False:
                    enemycard.x = enemylanes[(spawnedenemycards.index(enemycard))].position.x+2
                    enemycard.y = enemylanes[(spawnedenemycards.index(enemycard))].position.y+2
                enemycard.draw(fakescreen)
    
        for card in hand:
            if pygame.mouse.get_pos()[0] > card.x and pygame.mouse.get_pos()[1] > card.y:
                if pygame.mouse.get_pos()[0] < card.x + basiccard.get_width() and pygame.mouse.get_pos()[1] < card.y + basiccard.get_height():
                    if heldcard == None:
                        card.hover = True
            if not card == heldcard:
                card.draw(fakescreen)
        if not card == None:
            for card in hand:
                if card == heldcard:
                    card.draw(fakescreen)
        text_surface = font.render("HP: " + str(int(playerhp)) + "/10", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (100,20)
        fakescreen.blit(text_surface, text_rect)
        text_surface = font.render("Troverdighet: " + str(troverdighet) + "/10", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (100,40)
        fakescreen.blit(text_surface, text_rect)
        text_surface = font.render("Stagename: " + currentstage.name, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (WIDTH-200,40)
        fakescreen.blit(text_surface, text_rect)


    if gamephase == 1:
        if os.path.isfile("Backgroundphase1.jpeg"):
            backgroundimage = pygame.image.load("Backgroundphase1.jpeg")
        fakescreen.blit(backgroundimage, (0,0))
        areamap.draw(fakescreen)
        for marker in mapmarkers:
            marker.draw(fakescreen)


    if gamephase == 2:
        handloops = 0
        for card in hand:
            if pygame.mouse.get_pos()[0] > card.x and pygame.mouse.get_pos()[1] > card.y:
                if pygame.mouse.get_pos()[0] < card.x + basiccard.get_width() and pygame.mouse.get_pos()[1] < card.y + basiccard.get_height():
                    if heldcard == None:
                        card.hover = True
            if changingphase == False:
                card.order = handloops
                handloops+= 1
                if card != heldcard:
                    card.x = ((WIDTH-handmargin * 2) / len(hand)) * card.order + handmargin
        fakescreen.fill(BG_COLOR)
        if heldcard != None:
            heldcard.visualx = pygame.mouse.get_pos()[0] - (basiccard.get_width() / 2)
            heldcard.visualy = pygame.mouse.get_pos()[1] - (basiccard.get_height() / 2)
        for lane in shopslots:
            lane.draw(fakescreen)
            
        if currentshop.type == "GetCards":
            text_surface = font.render("Pick a card, any card (and keep it)", True, WHITE)
            text_rect = text_surface.get_rect()
            text_rect.center = (WIDTH/2,20)
            fakescreen.blit(text_surface, text_rect)
            loops = 1
            for card in currentshop.cards:
                card.draw(fakescreen)
                card.x = ((WIDTH-handmargin * 2) / len(currentshop.cards)) * loops + handmargin
                loops += 1
        if currentshop.type == "BoostCards" or currentshop.type == "Transfer":
            for lane in shopslots:
                if lane.card != None:
                    lane.card.draw(fakescreen)
                    lane.card.x = lane.position.x + 2
                    lane.card.y = lane.position.y + 2
            if currentshop.type == "BoostCards":
                text_surface = font.render("Boost Type is " + str(currentshop.boosttype), True, WHITE)
                text_rect = text_surface.get_rect()
                text_rect.center = (WIDTH/2,20)
                fakescreen.blit(text_surface, text_rect)
            else:
                text_surface = font.render("Transfer abilites from left card to right", True, WHITE)
                text_rect = text_surface.get_rect()
                text_rect.center = (WIDTH/2,20)
                fakescreen.blit(text_surface, text_rect)
            text_surface = font.render("Press Space to confirm", True, WHITE)
            text_rect = text_surface.get_rect()
            text_rect.center = (WIDTH/2,45)
            fakescreen.blit(text_surface, text_rect)


            for card in hand:
                card.draw(fakescreen)



    
    screen.blit(pygame.transform.scale(fakescreen, screen.get_rect().size), (0, 0))

    pygame.display.flip()
