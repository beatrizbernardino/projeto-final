# Importando as bibliotecas que usaremos no decorrer do código.
import random
import pygame
from os import path
pygame.init()

#Algumas informações sobre o jogo
#cores
WHITE = (255, 255, 255) 
vermelhozinho = (190, 2, 20)
#frames per second
FPS=27
#largura e altura da tela, respectivamente
width=900
height=600
#determina o tamanho da tela 
win = pygame.display.set_mode((900,600))
#Nome do jogo 
pygame.display.set_caption("Missão Polar")
#indica a pasta que contém os sons e as figuras 
walkRight = [pygame.image.load('papainoel3.png'), pygame.image.load('papainoel4.png'), pygame.image.load('papainoel5.png')]
walkLeft = [pygame.image.load('papainoel0.png'), pygame.image.load('papainoel1.png'), pygame.image.load('papainoel2.png')]
walkpoderR = [pygame.image.load('papainoel5p.png'), pygame.image.load('papainoel6p.png'), pygame.image.load('papainoel7p.png')]
walkpoderL = [pygame.image.load('papainoel1p.png'), pygame.image.load('papainoel3p.png'), pygame.image.load('papainoel4p.png')]
stan=pygame.image.load('papainp.png')
snd_dir = path.join(path.dirname(__file__))
img_dir=path.join(path.dirname(__file__))
bg = pygame.image.load('snow.png')
char  = pygame.image.load('papain.png')
pew = pygame.image.load("tiro.png").convert_alpha()
som=pygame.mixer.Sound(path.join(snd_dir, 'tiro.wav'))
boom=pygame.mixer.Sound(path.join(snd_dir, 'expl6.wav'))
bgsong=pygame.mixer.Sound(path.join(snd_dir, 'bg.wav'))
inicial=pygame.image.load('bbg.png')
final=pygame.image.load('final.jpg').convert()
vida=pygame.image.load('ra.jpg').convert()
player_img = pygame.image.load('pegiga.png')
#informações sobre a escala das imagens na tela 
vida.set_colorkey((255,255,255))
tamanhov=60,40
Bg=pygame.transform.scale(bg,(900,600))
telafinal=pygame.transform.scale(final,(900,600))
vida0=pygame.transform.scale(vida,(tamanhov))
vida1=pygame.transform.scale(vida,(tamanhov))
vida2=pygame.transform.scale(vida,(tamanhov))
# Variável para o ajuste de velocidade
clock = pygame.time.Clock()
#cria varios grupos
all_sprites=pygame.sprite.Group()
playergroup = pygame.sprite.Group()
enemygroup = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_platforms=pygame.sprite.Group()
# Classe Player que representa o jogador 
class Player(pygame.sprite.Sprite):
    # Construtor da classe Player
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.transform.scale(char,(48,64))
        self.image.set_colorkey((0,0,0))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.invencivel=0
        self.speedx=0
        self.speedy=0
        self.pulo = False
        self.vel = 10
        self.jumpCount = 10
        self.direita = True
        self.esquerda = False
        self.parado = False
        self.radius = 32
        self.sprite_right=0
        self.sprite_left=0    
        self.sprite_invencivel=0

    # Função que faz a animação do player     
    def update_sprite(self):
        if self.direita:
            self.sprite_right += 1
            if self.sprite_right == len(walkRight) - 1:
                self.sprite_right = 0
            self.image = pygame.transform.scale(walkRight[self.sprite_right],(48,64))
            
        if self.esquerda:
            self.sprite_left += 1
            if self.sprite_left == len(walkLeft) - 1:
                self.sprite_left = 0
            self.image = pygame.transform.scale(walkLeft[self.sprite_left],(48,64))

        if self.invencivel>0:
            if self.esquerda:
                self.sprite_invencivel += 1
                if self.sprite_invencivel == len(walkpoderL) - 1:
                    self.sprite_invencivel = 0
                self.image = pygame.transform.scale(walkpoderL[self.sprite_invencivel],(48,64))
            if self.direita:
                self.sprite_invencivel += 1
                if self.sprite_invencivel == len(walkpoderR) - 1:
                    self.sprite_invencivel = 0
                self.image = pygame.transform.scale(walkpoderR[self.sprite_invencivel],(48,64))
                
 
            if self.pulo or self.parado and self.speedx==0:
                self.image = pygame.transform.scale(stan,(48,64))

        else:
            
            if self.pulo or self.parado and self.speedx==0:
                self.image = pygame.transform.scale(char,(48,64))
    # Função que atualiza a posição do player na tela
    def update(self):
        self.rect.x += self.speedx
        self.rect.y+=self.speedy
        if not self.parado:
            self.speedy += 1 # Gravidade 
        if self.speedx != 0:
            man.parado = False
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0          
        if self.invencivel > 0: # para o super poder durar 10 seg
            self.invencivel -= 1

# Classe enemy que representa o inimigo 
class enemy(pygame.sprite.Sprite):
    # Construtor da classe enemy
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image= pygame.transform.scale(player_img,(80,80))
        self.image.set_colorkey((0,0,0))
        self.rect=self.image.get_rect() 
        self.rect.y = y 
        self.rect.x = x
        self.speedx = 5 
        self.speedy = 5
        self.herox = 0
        self.heroy = 0
        self.visible=True
        self.radius=27
    # Função que atualiza a posição do inimigo    
    def update(self):
        if self.visible:
            if(self.rect.x - 16 > self.herox):
               self.rect.x -= self.speedx
            
            elif(self.rect.x + 16 < self.herox):
               self.rect.x += self.speedx
           
            if(self.rect.y - 16 > self.heroy):
               self.rect.y -= self.speedy
            
            elif(self.rect.y + 16 < self.heroy):
                self.rect.y += self.speedy
    #Função que faz com que o inimigo va ate o Player            
    def sethero(self, x, y):
        self.herox = x
        self.heroy = y

# Classe projetil que representa o tiro
class projetil(pygame.sprite.Sprite):
    # Construtor da classe projetil 
    def __init__(self,x,y,pew,facing):
        pygame.sprite.Sprite.__init__(self)
        self.image=pew
        self.image = pygame.transform.scale(pew, (70, 50))
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedx=20 * facing
        self.facing = facing
    # Função que atualiza a posição do projétil
    def update(self):
        self.rect.centerx += (self.speedx)
        if self.rect.centerx>width or self.rect.centerx<0:
            self.kill()
# Classe Platform que representa as tres plataformas
class Platform(pygame.sprite.Sprite):
    # Construtor da classe Platform
    def __init__(self,x,y,w,h, tipo):
        pygame.sprite.Sprite.__init__(self)
        filename = ''
        if tipo == 'left':
            filename = 'snow_76.png'
        elif tipo == 'right':
            filename = 'snow_77.png'
        elif tipo== "middle":
           filename='snow_54.png'
        player_img=pygame.image.load(path.join(img_dir,filename)).convert()
        self.image=player_img 
        self.image=pygame.transform.scale(player_img,(w,h))    
        self.rect=self.image.get_rect()
        self.rect.height = 5
        self.rect.centerx=x
        self.rect.bottom=y
        self.image.set_colorkey((0,0,0))
   
#colocando as plataformas em ordem na tela
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
        all_platforms.add(p1)

#função que atualiza todos os sprites, e mostra as vidas na tela            
def RestaurarJanela(man):

    man.update_sprite() 
    all_sprites.update()
    win.blit(Bg, (0,0))
    all_sprites.draw(win)
    placar=font.render("Score: " + str(score), 1, (190,2,20))
    power1=font.render("Press S to Power: " + str(power), 1, (190,2,20))
    win.blit(placar,(730,70))
    win.blit(power1,(3,3))
     
    if lives==3:
        win.blit(vida0,(730,10))
        win.blit(vida1,(785,10))
        win.blit(vida2,(840,10))
    if lives==2:
        win.blit(vida0,(730,10))
        win.blit(vida1,(785,10))
    if lives==1:
         win.blit(vida0,(730,10))

    if man.invencivel > 0:
        
        total_sec = man.invencivel//FPS
        msg = "Acabou!!"
        if man.invencivel>FPS:
            msg = "Poder ativado: 0:"+str(total_sec)
        text = font.render(msg, True, vermelhozinho)
        win.blit(text, (355, 50))
    # Depois de desenhar, inverte o display
    pygame.display.update()


# cria nosso personagem  
man=Player(1,450,64,64)
playergroup.add(man)
all_sprites.add(man)

projeteis=[]
#estabelece a fonte da 
font = pygame.font.SysFont("Britannic Bold",40,True)
count=0
#inicia o looping principal
run = True
 
#abre o arquivo em texto que guarda o High Score, lê e fecha      
high_score_file = open("high_score_file.txt", "r")
high_score = int(high_score_file.read())
high_score_file.close()  
#quantidade de flocos de neve
numeroparticulas=100;
#cria uma lista para fazer o mecanismo da neve se mexer
neve_list=[]
#mecanismo para cair a neve
for i in range(numeroparticulas):
    x = random.randrange(0, 900)
    y = random.randrange(0, 600)
    neve_list.append([x,y])    
#para iniciar o jogo clicando no botão do mouse
end_it=False
while not end_it:
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN:
            end_it=True
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
            
    win.blit(inicial, (0,0))    
    pygame.display.flip()
    
try:
    #para iniciar o som
    bgsong.play(loops=-1)
    #estabelece algumas variáveis
    score=0
    lives=3
    power=2
    #iniciando o looping principal
    while run:
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        #collide da plataforma com o player
        hits = pygame.sprite.groupcollide(all_platforms, playergroup, False, False)
        for hit in hits:
            if man.speedy > 0:
                man.rect.bottom = hit.rect.top
                man.speedy = 0
                man.pulo = False
                man.parado = True
            elif man.speedy < 0:
                man.rect.top = hit.rect.bottom
                man.speedy = 0
                man.pulo = False
         
        #collide do player com o inimigo
        hits = pygame.sprite.groupcollide(enemygroup, playergroup, True, False, pygame.sprite.collide_circle)
        if hits:
             if man.invencivel==0:
                 lives -= 1

        #abre o arquivo e escreve nele o score, retirando o score que estava escrito anteriomente, somente se tal score for maior que todos os anteriores    
        if lives == 0:
            if score>high_score:
                high_score_file = open("high_score_file.txt", "w")
                high_score_file.write(str(score))
                high_score_file.close()
                high_score = score
            a= False
            pygame.mouse.get_pressed()
            
            #tela final do jogo
            while not a:
                myfont=pygame.font.SysFont("Britannic Bold", 60)
                vitorlindo=pygame.font.SysFont("Britannic Bold", 100)
                b=myfont.render("Score:"+ str(score),2, vermelhozinho )
                nlabel=vitorlindo.render("Game Over", 1, vermelhozinho)
                sco=myfont.render("HighScore:"+ str(high_score),2, vermelhozinho )
                #Quando o jogo acaba, a tela final feita é exibida  (linhas: 372 a 375) , e nela podemos ver uma oportunidade  de reduzir acoplamento, pois toda as informações que devem aparecer nela estão em função do width, height, anteriormente estabelecidos, e outros valores que são hardcoded. Portanto, teremos valores hardcoded em função de outros valores hardcoded.
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        quit()
                    win.blit(telafinal,(0,0))
                    win.blit(nlabel,(width/2,height-550))
                    win.blit(b,(150,height-100))
                    win.blit(sco,(150,height-150))
                    # Depois de desenhar, inverte o display.
                    pygame.display.flip()
                    run =False
           
            
        #collide do inimigo com os tiros                
        hits =pygame.sprite.groupcollide(enemygroup,bullets , True, False, ) 
        if hits:
             boom.play()
             score+=1
             
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #o que apertar para atirar, pular, andar para a esquerda e para a direita
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if man.esquerda:
                    facing = -1
                else:
                    facing = 1
            if not(man.pulo):
                if keys[pygame.K_w]:
                    man.pulo = True
                    man.speedy = -20
                    man.parado = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    man.speedx -= man.vel
                    man.direita = False
                    man.esquerda= True
                    man.parado = False                   
                if event.key == pygame.K_d:
                    man.speedx += man.vel
                    man.direita = True
                    man.esquerda = False
                    man.parado = False
                if event.key == pygame.K_SPACE:
                    bullet=projetil(man.rect.centerx,man.rect.bottom,pew,facing)
                    bullet.rect.centerx=man.rect.x +10
                    bullet.rect.bottom=man.rect.y + 40
                    som.play()
                    projeteis.append(bullet)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                #apertar "s" para ficar invencivel
                if power>0:
                     if event.key == pygame.K_s:
                         man.invencivel= FPS * 10
                         power-=1
            #quando retira o dedo da tecla, ele para de fazer o comando que estava sendo executado  
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    man.speedx = 0
                if event.key == pygame.K_d:
                    man.speedx = 0           
        #mecanismo de aparição de inimigos
        if score>20: 
            if count == 50:             
                en= enemy(random.randrange(0,width), random.randrange(0,height))
                enemygroup.add(en)
                all_sprites.add(en)
                count=0
        else:
            if count == 80:               
                en= enemy(random.randrange(0,width), random.randrange(0,height))
                enemygroup.add(en)
                all_sprites.add(en)
                count=0
        count+=1
        RestaurarJanela(man)
        #mecanismo para o inimigo seguir o personagem
        for en in enemygroup:
            en.sethero(man.rect.x, man.rect.y)
        #para a neve se mover 
        for point in neve_list:
            point[1]+=1
            pygame.draw.circle(win, WHITE, point, 2)
            if(point[1] >= height):
                point[0] = random.randrange(0, 900)
                point[1] = random.randrange(-10, -5)
        # Depois de desenhar, inverte o display.
        pygame.display.flip()
#finaliza o jogo 
finally:
    pygame.quit()
    #evita travamentos
    quit()