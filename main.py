import pygame
import imageio
from gif import *
from classe import *
from time import sleep


pygame.init()

info = pygame.display.Info()

largeur_ecran = info.current_w
hauteur_ecran = info.current_h

# intro
'''
loading = pygame.display.set_mode((largeur_ecran/2,hauteur_ecran/2),pygame.NOFRAME | pygame.SWSURFACE)
w,h = pygame.display.get_surface().get_size()
pygame.display.set_caption("Loading")

POLICE_ARIAL = pygame.font.SysFont("Arial",35,1,1)
with open('version.txt', 'r') as fichier:
    v = fichier.readline()
version = "version: "+str(v)
Text = POLICE_ARIAL.render(version,1,BLANC)
text_rect = Text.get_rect()
#print(text_rect[3],text_rect)
loading.blit(Text,(w/2-text_rect[2]/2,h/2-text_rect[3]/2))

pygame.display.flip()

sleep(4)

pygame.quit()
'''



left = 0
right = 0
space = 0
fondx = 0

elapsed_time = 0
start_time = 0

marge = 0.1

xblocs = 0
yblocs = 0

colision_yperso = True
colision_xperso = True

ecran = pygame.display.set_mode((1300,650),pygame.RESIZABLE)
w,h = pygame.display.get_surface().get_size()
pygame.display.set_caption("Mario Bros","Mario Bros")

# Charger l'icône
icone = pygame.image.load("champignon.png")

# Définir l'icône de la fenêtre
pygame.display.set_icon(icone)

nombre_manettes = pygame.joystick.get_count()
for i in range(nombre_manettes):
    manette = pygame.joystick.Joystick(i)
    manette.init()

background = pygame.Surface(ecran.get_size())
background.fill(NOIR)



fond = pygame.image.load("fond.png").convert_alpha()
ma_liste2 = []


# Ouvrir le fichier en mode lecture
with open('map4.pg', 'r') as fichier:
    # Lire toutes les lignes du fichier dans une liste
    lignes = fichier.readlines()
    fichier.seek(0)
    lines = fichier.read()


XX = 0
YY = 0
nb = 0
for l in range(len(lignes)):
    for s in range(len(lignes[l])):
        if lines[nb]=="C":
            _box = BOX(XX*TUILE_TAILLE, YY*TUILE_TAILLE)
            LISTE_BOX.add(_box)
            LISTE_GLOBALE_SPRITES.add(_box)
        if lines[nb]=="M":
            _mur = MUR(XX*TUILE_TAILLE, YY*TUILE_TAILLE)
            LISTE_MURS.add(_mur)
            LISTE_GLOBALE_SPRITES.add(_mur)
        if lines[nb]=="S" or lines[nb]== "s" or lines[nb]== "T" or lines[nb]== "-":
            _sol = SOL(XX*TUILE_TAILLE, YY*TUILE_TAILLE,lines[nb])
            LISTE_SOLS.add(_sol)
            LISTE_GLOBALE_SPRITES.add(_sol)
        if lines[nb]=="G":
            _gomb = goomba(XX*TUILE_TAILLE, YY*TUILE_TAILLE)
            LISTE_GOOMBA.add(_gomb)
            VIVANT.add(_gomb)
            LISTE_GLOBALE_SPRITES.add(_gomb)
        if lines[nb]=="." or lines[nb]=="*":
            ma_liste.append([XX*TUILE_TAILLE, YY*TUILE_TAILLE, lines[nb]])
            ma_liste2.append([XX*TUILE_TAILLE, YY*TUILE_TAILLE])
            _point = SOL_POINT(XX*TUILE_TAILLE, YY*TUILE_TAILLE)
            LISTE_point.add(_point)
            LISTE_GLOBALE_SPRITES.add(_point)

        XX = XX + 1
        nb+=1
    XX = 0
    YY = YY + 1

# Fonction de tri personnalisée
def custom_sort(item):
    return (item[0], item[2] != '*')
# Trier la liste en utilisant la fonction de tri personnalisée
lp = sorted(ma_liste, key=custom_sort)
lpp = sorted(ma_liste2, key=lambda x: x[0])

lpp.insert(0, [0,h])
end = lpp[len(lpp)-1][0]
lpp.insert(0, [end,h])

print(w,h,lpp)


w,h = pygame.display.get_surface().get_size()

for i in range(len(lp)-1):
    x1,y1 = lp[i][0],lp[i][1]
    x2,y2 = lp[i+1][0],lp[i+1][1]
    pente = (y2-y1)/(x2-x1)
    coté1 = lp[i+1][0]-lp[i][0]
    coté2 = lp[i+1][1]-lp[i][1]
    coté3 = math.sqrt(coté1*coté1+coté2*coté2)
    angle = math.degrees(math.atan2(coté1, coté2))-90
    test = Sol_line(0,0,angle,"S")
    larg = test.rect[2]
    print(larg)
    print(angle, "°")
    for n in range(int(coté3/TUILE_TAILLE)):
        x = x1+n*TUILE_TAILLE
        y = y1+(x1 +n*TUILE_TAILLE-x1)*(y2-y1)/(x2-x1)
        _sol = Sol_line(x,y-angle/34*20,angle,"S")
        LISTE_GLOBALE_SPRITES.add(_sol)

print("fin")

def affich_map(av):
    LISTE_AFFICH.empty()
    if personnag.vie > 0:
        LISTE_AFFICH.add(personnag)
    for sprite in LISTE_GLOBALE_SPRITES:
        if left == 1:
            personnag.direction = "l"
            sprite.rect.x += personnag.avance_gauche*1.4
            
        if right ==1:
            personnag.direction = "r"
            sprite.rect.x -= personnag.avance_droite*1.4

        
        if sprite.rect.x < w and sprite.rect.x > -TUILE_TAILLE and sprite.etat and sprite.vie == 1:
            LISTE_AFFICH.add(sprite)
    for i in range(len(lp)):
        if left == 1:
            lp[i][0] += personnag.avance_gauche*1.4
        if right == 1: 
            lp[i][0] -= personnag.avance_gauche*1.4
    for i in range(len(lpp)):
        if left == 1:
            lpp[i][0] += personnag.avance_gauche*1.4
        if right == 1: 
            lpp[i][0] -= personnag.avance_gauche*1.4


personnag = perso()
VIVANT.add(personnag)
LISTE_AFFICH.add(personnag)




continuer=True

while continuer:
    
    w,h = pygame.display.get_surface().get_size()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left=1
            if event.key == pygame.K_RIGHT:
                right=1
            if event.key == pygame.K_SPACE:
                space=1
                start_time = pygame.time.get_ticks()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left=0
            if event.key == pygame.K_RIGHT:
                right=0
            if event.key == pygame.K_SPACE:
                space=0
                elapsed_time = pygame.time.get_ticks() - start_time + 50
                if elapsed_time > 150:
                    elapsed_time = 150



        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 1:
                space = 1

        if event.type == pygame.JOYBUTTONUP:
            if event.button == 1:
                space = 0


        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:

                if event.value < -0.5:
                    left = 1
                elif event.value > 0.5:
                    right = 1
                elif -marge < event.value < marge:
                    left = 0
                    right = 0


    if left==1 and personnag.rect.x>0 and personnag.avance_gauche>0:
        fondx=fondx+1
    elif right==1 and personnag.avance_droite>0:
        fondx=fondx-1
    if fondx>0:
        fondx=0

    if pygame.time.get_ticks() - start_time > 180 and space == 1:
        space = 0
        elapsed_time = 170

    symmetrical_frame = pygame.transform.flip(frames[current_frame], True, False)


    ecran.blit(fond,(fondx,0))
    pygame.draw.polygon(ecran, (227, 153, 76), lpp)
    affich_map(personnag.av)
    LISTE_AFFICH.update(ecran)
    liste_de_sprites = list(LISTE_point)
    print(LISTE_GOOMBA)
    for sprite in LISTE_GOOMBA:
        sprite.collision(right, left, ecran, lp)
    if personnag.vie > 0:
        personnag.avancer(right, left, space, ecran, elapsed_time, lp)
        personnag.collision(right, left, ecran, lp)
    elapsed_time = 0


    LISTE_AFFICH.draw(ecran)
    CADEAUX.draw(ecran)
    #LISTE_point.update(ecran)

    if personnag.vie == 0:
        #del personnag
        POLICE_ARIAL = pygame.font.SysFont("Arial",100,1,1)
        gameover = POLICE_ARIAL.render("GAMEOVER",1,ROUGE)
        gameover_rect = gameover.get_rect()
        ecran.blit(gameover,(w/2-gameover_rect[2]/2,h/2-gameover_rect[3]/2))


    # Limiter la vitesse de l'animation
    clock.tick(personnag.frame_rate)


    pygame.display.flip()

pygame.quit()
