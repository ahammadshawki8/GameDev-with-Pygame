import pygame
from pygame.locals import *
pygame.init()

win = pygame.display.set_mode((500,480))
pygame.display.set_caption("FIRST GAME")
screen_width = 480
bg = pygame.image.load("resources/bg.jpg")
clock = pygame.time.Clock()

# first we need to load in our sounds
#bulletSound = pygame.mixer.Sound("bullet.ogg")
#hitSound = pyagme.mixer.Sound("hit.ogg")
music = pygame.mixer.music.load("music.mp3")

# we need to play the music continuosly, so we can do that by
pygame.mixer.music.play(-1)


# now we need to play the sound effects.

class Player():
    walkRight = [pygame.image.load("resources/R1.png"), pygame.image.load("resources/R2.png"), pygame.image.load("resources/R3.png"), pygame.image.load("resources/R4.png"), pygame.image.load("resources/R5.png"), pygame.image.load("resources/R6.png"), pygame.image.load("resources/R7.png"), pygame.image.load("resources/R8.png"), pygame.image.load("resources/R9.png")] 
    walkLeft = [pygame.image.load("resources/L1.png"), pygame.image.load("resources/L2.png"), pygame.image.load("resources/L3.png"), pygame.image.load("resources/L4.png"), pygame.image.load("resources/L5.png"), pygame.image.load("resources/L6.png"), pygame.image.load("resources/L7.png"), pygame.image.load("resources/L8.png"), pygame.image.load("resources/L9.png")]

    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.vel = 10
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x+20, self.y+8, 28, 60)    

    def draw(self,win):
        if self.walkCount+1 >= 27:
            self.walkCount = 0
        
        if not self.standing:
            if self.left:
                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(self.walkRight[0], (self.x,self.y))
            else:
                win.blit(self.walkLeft[0], (self.x,self.y))
        
        self.hitbox = (self.x+20, self.y+8, 28, 60)
            

class Projectile():
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 15 * facing

    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)


class Enemy:
    walkRight = [pygame.image.load("resources/R1E.png"), pygame.image.load("resources/R2E.png"), pygame.image.load("resources/R3E.png"), pygame.image.load("resources/R4E.png"), pygame.image.load("resources/R5E.png"), pygame.image.load("resources/R6E.png"), pygame.image.load("resources/R7E.png"), pygame.image.load("resources/R8E.png"), pygame.image.load("resources/R9E.png"), pygame.image.load("resources/R10E.png"), pygame.image.load("resources/R11E.png")] 
    walkLeft = [pygame.image.load("resources/L1E.png"), pygame.image.load("resources/L2E.png"), pygame.image.load("resources/L3E.png"), pygame.image.load("resources/L4E.png"), pygame.image.load("resources/L5E.png"), pygame.image.load("resources/L6E.png"), pygame.image.load("resources/L7E.png"), pygame.image.load("resources/L8E.png"), pygame.image.load("resources/L9E.png"), pygame.image.load("resources/L10E.png"), pygame.image.load("resources/L11E.png")]
    
    def __init__(self,x,y,w,h,end):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.end = end
        self.walkCount = 0
        self.vel = 7
        self.path = [self.x,self.end]
        self.hitbox = (self.x+13, self.y, 40, 60)
        self.health = 10
        self.visible = True
        
     
    
    def draw(self,win):
        self.move()

        if self.visible:
            if self.walkCount+1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            
            self.hitbox = (self.x+13, self.y, 40, 60)


            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1]-20,50,8))
            pygame.draw.rect(win, (0,0,255), (self.hitbox[0], self.hitbox[1]-20,self.health*5,8))

    

    def move(self):

        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
                
    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False

    

    
man = Player(50,400,54,64)
goblin = Enemy(80,405,64,64,450)
shootLoop = 0
score = 0
font = pygame.font.SysFont("comicsans", 30, True, True)


def reDrawGameWindow():    
    win.blit(bg, (0,0))
    
    text = font.render("Score: " + str(score), 1, (0,0,0)) 
    win.blit(text, (20,20))
    
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
        
    pygame.display.update()   
     
        
bullets = []
run = True
while run:
    clock.tick(27)
    
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # when our gblin gets hit, we need to play hitSound
    for bullet in bullets:
        if goblin.visible:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x -bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    goblin.hit()
                    hitSound.play()
                    bullets.remove(bullet)
                    score += 1
                
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.remove(bullet)
            
    
    keys = pygame.key.get_pressed()
    
    # when we shoot the bullet we need to play bulletSound
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(Projectile(round(man.x + man.w//2), round(man.y + man.h//2), 3, (0,0,0), facing))
            bulletSound.play()
            
        shootLoop = 1

    if keys[pygame.K_LEFT] and (man.x-man.vel) > 0:
        man.x -= man.vel
        man.left = True 
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and (man.x+man.h+man.vel) < screen_width:
        man.x += man.vel
        man.left = False 
        man.right = True
        man.standing = False

    else:
        man.standing = True
        man.walkCount = 0

    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) *0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False 
            man.jumpCount = 10

    reDrawGameWindow()
            
pygame.quit()
