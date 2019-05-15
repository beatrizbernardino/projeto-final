
import pygame
from os import path
pygame.init()


width=900
height=600
win = pygame.display.set_mode((900,600))
pygame.display.set_caption("Projeto Final")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
bg_rect = bg.get_rect()
char = pygame.image.load('standing.png')
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
#walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
clock = pygame.time.Clock()


all_sprites=pygame.sprite.Group()
all_platforms=pygame.sprite.Group()
img_dir=path.join(path.dirname(__file__))

class player(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.pulo = False
        self.state = 0 # 0 stand, 1 = right, 2 = left
        self.walkCount = 0
        self.jumpCount = 10
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.image = self.getImage()        
        self.rect = self.image.get_rect()
        
        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.bottom = 570
        self.rect.centerx = width/2

    def getImage(self):
        if self.state == 1:
            return walkRight
        elif self.state == 2:
            return walkLeft
        else:
            return char
        
    def update(self):
        if self.walkCount +1 >= 27:
            self.walkCount = 0
        self.image = self.getImage()
        if self.state != 0:
            self.walkCount +=1

#
#        if not(self.standing):
#            if self.left:
#                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
#                self.walkCount +=1
#            elif self.right:
#                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
#                self.walkCount +=1
#        else:
#            if self.right:
#                win.blit(walkRight[0], (self.x,self.y))
#            else:
#                win.blit(walkLeft[0], (self.x,self.y))
#            self.hitbox=self.hitbox = (self.x + 17, self.y + 11, 29, 52)
#            pygame.draw.rect(win,(255,0,0), self.hitbox,2)#para desenhar o hit box no boneco. ta no update pois tem q atualizar toda vez que ele anda

class inimigo(pygame.sprite.Sprite):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft= [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self,x,y,width,height,end):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]  #Onde começa e onde termina
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)#EXPLICAÇÃO
        self.vida=10
        self.visible=True
    def update(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0 
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20,50,10))                        #EXPLICAÇÃO
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20,50 - (5*(10 - self.vida)), 10))#EXPLICAÇÃO
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)#EXPLICAÇÃO
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x>self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
    def hit(self):
        if self.vida>0:
            self.vida -=1
        else:
            self.visible = False
        print("hit")
    
class projetil(pygame.sprite.Sprite):
    def __init__(self,x,y,radius,color,facing):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 20 * facing
           
    def update(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
 
class Platform(pygame.sprite.Sprite):

    def __init__(self,x,y,w,h, tipo):
        pygame.sprite.Sprite.__init__(self)
        filename = ''
        if tipo == 'left':
            filename = 'grassCliffLeftAlt.png'
        elif tipo == 'right':
            filename = 'grassCliffRightAlt.png'
        elif tipo== "middle":
           filename='grassMid.png'
        player_img=pygame.image.load(path.join(img_dir,filename)).convert()
        self.image=player_img
        
        self.image=pygame.transform.scale(player_img,(w,h))
        
        self.rect=self.image.get_rect()
        
        self.rect.centerx=x
        self.rect.bottom=y
        self.image.set_colorkey((0,0,0))
        
for i in range (3):
    if i==0:
        for i in range (4):
    
            if i==0:
                p1=Platform(width/2-150+i*100,height-120,100,50,'left')
            elif i==3:
                p1=Platform(width/2-150+i*100,height-120,100,50,'right')
            else:
                p1=Platform(width/2-150+i*100,height-120,100,50,'middle')
        
            all_sprites.add(p1)
            all_platforms.add(p1)
        
    if i ==1:
         for i in range (4):
    
            if i==0:
                p1=Platform(width/2-400+i*70,height-300,70,45,'left')
            elif i==3:
                p1=Platform(width/2-400+i*70,height-300,70,45,'right')
            else:
                p1=Platform(width/2-400+i*70,height-300,70,45,'middle')
        
            all_sprites.add(p1)
            all_platforms.add(p1)
    if i ==2:
        
         for i in range (4):
    
            if i==0:
                p1=Platform(width/2+190+i*70,height-300,70,45,'left')
            elif i==3:
                p1=Platform(width/2+190+i*70,height-300,70,45,'right')
            else:
                p1=Platform(width/2+190+i*70,height-300,70,45,'middle')
        
            all_sprites.add(p1)
            all_platforms.add(p1)

def RestaurarJanela():
    win.blit(bg, bg_rect)
    #all_sprites.draw(win)
   # man.update()
    all_sprites.update()
    inimg.update(win)
    text=font.render("Score: " + str(score), 1, (255,215,0))
    win.blit(text,(750,10))
    for proj in projeteis:
        proj.update(win)
    pygame.display.update()

inimg= inimigo(1,510,64,64,800)    
man=player(1,510,64,64)
all_sprites.add(man)
projeteis=[]
score=0
font = pygame.font.SysFont("comicsana",40,True)

run = True

while run:
    clock.tick(27)
    
    hits = pygame.sprite.spritecollide(man, all_platforms, False)
        
    for hit in hits:
        print("bateu")


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for proj in projeteis:
        if proj.y - proj.radius < inimg.hitbox[1] + inimg.hitbox[3] and proj.y + proj.radius > inimg.hitbox[1]:     #EXPLICAÇÃO
            if proj.x + proj.radius > inimg.hitbox[0] and proj.x - proj.radius < inimg.hitbox[0] + inimg.hitbox[2]: #EXPLICAÇÃO
                inimg.hit()
                score += 1
                projeteis.pop(projeteis.index(proj))
        
        
        if proj.x <900 and proj.x >0:
            proj.x += proj.vel
        else:
            projeteis.pop(projeteis.index(proj))

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(projeteis) <1:
            projeteis.append(projetil(round(man.x+man.width//2),round(man.y+man.height//2),6,(0,0,0),facing))#EXPLICAÇÃO
    
    if keys[pygame.K_a] and man.x>man.vel:
        man.x -= man.vel
        man.state = 2
    elif keys[pygame.K_d] and man.x < 900 - man.vel - man.width:
        man.x += man.vel
        man.state = 1
        
    else:
        man.state = 0
        walkCount = 0
    
    if not(man.pulo):
        if keys[pygame.K_w]:
            man.pulo = True
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.jumpCount = 10
            man.pulo = False
            
    RestaurarJanela()
    all_sprites.draw(win)
    all_sprites.update()    
pygame.quit()
quit()