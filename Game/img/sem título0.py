# -*- coding: utf-8 -*-
"""
Created on Thu May 16 12:01:32 2019

@author: Vitor Bandeira
"""

import random
import pygame
from os import path
pygame.init()

WIDTH=600
HEIGHT=600
width=900
height=600
win = pygame.display.set_mode((900,600))
pygame.display.set_caption("Projeto Final")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')
pew = pygame.image.load("tiro.png").convert()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
clock = pygame.time.Clock()

player_img = pygame.image.load('R8E.png')
all_sprites=pygame.sprite.Group()
playergroup = pygame.sprite.Group()
enemygroup = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_platforms=pygame.sprite.Group()
img_dir=path.join(path.dirname(__file__))

class player(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image= char
        self.image= pygame.transform.scale(char,(64,64))
        self.image.set_colorkey((0,0,0))
        self.rect=self.image.get_rect()
        self.rect.x=1
        self.rect.y=510
        self.speedx=0
        self.pulo = False
        self.vel = 5
        self.jumpCount = 10
    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0







'''
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.pulo = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.rect = pygame.Rect(self.x + 17, self.y + 11, 29, 52)
        self.rect.x=width/2
        self.rect.y=510
        
    def update(self,win):
        if self.walkCount +1 >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x,self.y))
            else:
                win.blit(walkLeft[0], (self.x,self.y))
            self.hitbox=self.hitbox = (self.x + 17, self.y + 11, 29, 52)
            self.rect = pygame.Rect(self.x + 17, self.y + 11, 29, 52)
            pygame.draw.rect(win,(255,0,0), self.hitbox,2)#para desenhar o hit box no boneco. ta no update pois tem q atualizar toda vez que ele anda
'''
class enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey((0,0,0))
        self.rect=self.image.get_rect() 
        self.rect.y = y 
        self.rect.x = x
        self.speedx = 10 
        self.speedy = 10
        self.herox = WIDTH//2
        self.heroy = HEIGHT//2
        
    def update(self):
        #WIDTH=900 
        #HEIGHT=600    
        if(self.rect.x - 16 > self.herox):
           self.rect.x -= self.speedx
        
        elif(self.rect.x + 16 < self.herox):
           self.rect.x += self.speedx
       
        if(self.rect.y - 16 > self.heroy):
           self.rect.y -= self.speedy
        
        elif(self.rect.y + 16 < self.heroy):
           self.rect.y += self.speedy
           
    def sethero(self, x, y):
        self.herox = x
        self.heroy = y


#class inimigo(pygame.sprite.Sprite):
#    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
#    walkLeft= [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
#
#    def __init__(self,x,y,width,height,end):
#        pygame.sprite.Sprite.__init__(self)
#        self.x = x
#        self.y = y
#        self.width = width
#        self.height = height
#        self.path = [x, end]  #Onde começa e onde termina
#        self.walkCount = 0
#        self.vel = 3
#        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
#        self.vida=10
#        self.visible=True
#    def update(self):
#        self.move()
#        if self.visible:
#            if self.walkCount + 1 >= 33:
#                self.walkCount = 0 
#            if self.vel > 0:
#                win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
#                self.walkCount += 1
#            else:
#                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
#                self.walkCount += 1
#            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20,50,10))                        #EXPLICAÇÃO
#            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20,50 - (5*(10 - self.vida)), 10))#EXPLICAÇÃO
#            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
#    def move(self):
#        if self.vel > 0:
#            if self.x < self.path[1] + self.vel:
#                self.x += self.vel
#            else:
#                self.vel = self.vel * -1
#                self.x += self.vel
#                self.walkCount = 0
#        else:
#            if self.x>self.path[0] - self.vel:
#                self.x += self.vel
#            else:
#                self.vel = self.vel * -1
#                self.x += self.vel
#                self.walkCount = 0
#    def hit(self):
#        if self.vida>0:
#            self.vida -=1
#        else:
#            self.visible = False
#        print("hit")

class projetil(pygame.sprite.Sprite):
    def __init__(self,x,y,pew):
        pygame.sprite.Sprite.__init__(self)
        self.image=pew
        self.image = pygame.transform.scale(pew, (30, 20))
        self.image.set_colorkey((0,255,0))
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedx=20
        #self.radius = radius
        #self.color = color
        #self.facing = facing

    def update(self):
       # pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
        self.rect.centerx+=self.speedx
        if self.rect.centerx>width or self.rect.centerx<0:
            self.kill()

'''    
class projetil(pygame.sprite.Sprite):
    def __init__(self,x,y,pew):
        pygame.sprite.Sprite.__init__(self)
        self.image = pew
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.facing = facing
        self.vel = 20 * facing
           
    def update(self,win):
        self.rect.x += self.vel
        if self.rect.x <0:
            self.kill()
'''        

 
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
   

for i in range (4):
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

    if i ==3:
        
        p1=Platform(width/2,height,900,30,'middle')
        
        all_sprites.add(p1)
            
def RestaurarJanela():
    all_sprites.update()

    win.blit(bg, (0,0))
    all_sprites.draw(win)
#    man.update()
#    inimg.update(win)
#    all_platforms.update()
#    playergroup.update()
#    bullets.update()
    text=font.render("Score: " + str(score), 1, (255,215,0))
    win.blit(text,(750,10))
#    for proj in projeteis:
#        proj.update(win)
#        all_sprites.add(proj)
    pygame.display.update()


inimg= enemy(1,510)    
man=player(1,510,64,64)
playergroup.add(man)
all_sprites.add(man)
all_sprites.add(inimg)
projeteis=[]
score=0
font = pygame.font.SysFont("comicsana",40,True)
count=0
run = True

try:
    while run:
        clock.tick(27)
        
        hits = pygame.sprite.groupcollide(all_platforms, playergroup, False, False)
        for hit in hits:
            print("bateu")
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
        #for proj in projeteis:
        #    if proj.rect.y - proj.radius < inimg.hitbox[1] + inimg.hitbox[3] and proj.rect.y + proj.radius > inimg.hitbox[1]:     #EXPLICAÇÃO
       #         if proj.rect.x + proj.radius > inimg.hitbox[0] and proj.rect.x - proj.radius < inimg.hitbox[0] + inimg.hitbox[2]: #EXPLICAÇÃO
      #              inimg.hit()
     #               score += 1
    #                projeteis.pop(projeteis.index(proj))
            
            
   #         if proj.x <900 and proj.x >0:
  #              proj.x += proj.vel
 #           else:
#                projeteis.pop(projeteis.index(proj))
                
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            #facing = -1
            bullet=projetil(man.rect.centerx,man.rect.bottom,pew)
            bullet.rect.centerx=man.rect.x
            bullet.rect.bottom=man.rect.y + 40
            projeteis.append(bullet)
            all_sprites.add(bullet)
            bullets.add(bullet)
            
        if keys[ pygame.K_a]:
            man.rect.x -= man.vel


        elif keys[pygame.K_d]:
            man.rect.x += man.vel

            
        
        if not(man.pulo):
            if keys[pygame.K_w]:
                man.pulo = True

        else:
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
                man.rect.y -= (man.jumpCount ** 2) * 0.5 * neg
                man.jumpCount -= 1
            else:
                man.jumpCount = 10
                man.pulo = False
                
        if count == 1000:
            
            en= enemy(random.randrange(0,WIDTH), random.randrange(0,HEIGHT))
            enemygroup.add(en)
            all_sprites.add(en)
            count=0
        count+=1
                
        RestaurarJanela()
        for en in enemygroup:
            en.sethero(man.rect.x, man.rect.y)
finally:
    pygame.quit()
    quit()