import pyxel
from math import *

# Définitions de la configuration du jeu.
SCREEN_SIZE = 256
TILE_SIZE = 32

VOID = [0, 0, 0]

CAVE_1 = [0, 32, 0]
CAVE_2 = [0, 32, 32]
BAKERY = [0, 64, 0]

TOWER = [0, 160, 0]

ZOMBIE = [0, 128, 0]

WALL = [0, 96, 160]
PROJ = [0, 128, 32]

PATH = [0, 96, 0]
PATH_2 = [0, 96, 32]
PATH_3 = [0, 96, 64]
PATH_4 = [0, 96, 96]
PATH_5 = [0, 96, 128]

defeat = False

bakery_hp = 100
# 'matrix' ici représente le terrain de jeu. C'est une matrice
# de 8x8 avec chaque case contenant un tableau de 3 nombres:
#### Numéro de la banque d'images, Abscisse et Ordonnée dans l'image.
matrix = [[VOID for line in range(8)] for column in range(8)]

matrix[0][0] = CAVE_1
matrix[1][0] = CAVE_2
matrix[6][7] = BAKERY
matrix[7][7] = PATH_5

test_person = [0, 0]
zombies = [[0, 0]]
projectiles = []
idx_zombie = 0
dir_r_or_d = False

config = 0

def priority(case, coef=1):
    global dir_r_or_d
    if case[1] < 7*coef:
        if dir_r_or_d and matrix[case[1]//coef][case[0]//coef] == VOID:
            matrix[case[1]//coef][case[0]//coef] = PATH_2
        elif not dir_r_or_d and matrix[case[1]//coef][case[0]//coef] == VOID:
            matrix[case[1]//coef][case[0]//coef] = PATH
        case[1] += 1
        dir_r_or_d = False
    elif case[0] < 7*coef:
        if dir_r_or_d and matrix[case[1]//coef][case[0]//coef] == VOID:
            matrix[case[1]//coef][case[0]//coef] = PATH_4
        elif not dir_r_or_d and matrix[case[1]//coef][case[0]//coef] == VOID:
            matrix[case[1]//coef][case[0]//coef] = PATH_3
        case[0] += 1
        dir_r_or_d = False
    return case

def path_finder(case, config, coef=1):
    global matrix, dir_r_or_d, idx_zombie, zombies
    if config == 2 or config == 3 or config == 10 or config == 8:
        if dir_r_or_d and matrix[case[1]//coef][case[0]//coef] == VOID:
            matrix[case[1]//coef][case[0]//coef] = PATH_2
        elif not dir_r_or_d and matrix[case[1]//coef][case[0]//coef] == VOID:
            matrix[case[1]//coef][case[0]//coef] = PATH
        case[1] += 1
        dir_r_or_d = False
    elif config == 4 or config == 13 or config == 12 or config == 5:
        if dir_r_or_d and matrix[case[1]//coef][case[0]//coef] == VOID:
            matrix[case[1]//coef][case[0]//coef] = PATH_4
        elif not dir_r_or_d and matrix[case[1]//coef][case[0]//coef] == VOID:
            matrix[case[1]//coef][case[0]//coef] = PATH_3
        case[0] += 1
        dir_r_or_d = True
    elif config == 6 or config == 7 or config == 14:
        return case
    elif config == 15:
        zombies.pop(idx_zombie)
    else:
        case = priority(case, coef)
    return case

class tower_defense:
    cnt = 1
    def update(self):
        global towers, matrix
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and matrix[pyxel.mouse_y//32][pyxel.mouse_x//32] == VOID:
            matrix[pyxel.mouse_y//32][pyxel.mouse_x//32] = TOWER

    def draw(self):
        global config, bakery_hp, zombies, defeat, projectiles
        if bakery_hp == 0:
            defeat = True
        pyxel.cls(0)
        if defeat:
            pyxel.cls(8)
            return

        # Dessin de la matrice.
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                pyxel.blt(x*32, y*32, matrix[y][x][0], matrix[y][x][1], matrix[y][x][2], TILE_SIZE, TILE_SIZE)
                if matrix[y][x] == TOWER and self.cnt%pyxel.rndi(30, 60) == 0:
                    if len(zombies) == 0:
                        break
                    nearest_zombie = zombies[0]
                    for zombie in zombies:
                        if ((zombie[0]-(x*32))**2+(zombie[1]-(y*32))**2)**(1/2) < ((nearest_zombie[0]-(x*32))**2+(nearest_zombie[1]-(y*32))**2)**(1/2):
                            nearest_zombie = zombie
                    projectiles.append([x*32, y*32, 8*(x*32 < nearest_zombie[0]*8)-8*(x*32 > nearest_zombie[0]*8), 8*(y*32 < nearest_zombie[1]*8)-8*(y*32 > nearest_zombie[1]*8), 0])
        for projectile in projectiles:
            projectile[4] += 1
            if len(zombies) == 0:
                break
            nearest_zombie = zombies[0]
            for zombie in zombies:
                if ((zombie[0]-(x*32))**2+(zombie[1]-(y*32))**2)**(1/2) < ((nearest_zombie[0]-(x*32))**2+(nearest_zombie[1]-(y*32))**2)**(1/2):
                            nearest_zombie = zombie
            pyxel.blt(projectile[0], projectile[1], PROJ[0], PROJ[1], PROJ[2], 16, 16)
            projectile[0] += projectile[2]
            projectile[1] += projectile[3]
            if pyxel.sqrt((nearest_zombie[0]*8-projectile[0])**2+(nearest_zombie[1]*8-projectile[1])**2) <= 100:
                projectiles.remove(projectile)
                zombies.remove(nearest_zombie)
            elif projectile[4] == 120:
                projectiles.remove(projectile)
        for zombie in zombies:
            if zombie[0] != 7*8 or zombie[1] != 7*8:
                if zombie[1] == 7*8:
                    config += 4
                elif matrix[zombie[1]//8+1][zombie[0]//8] == WALL:
                    config += 4
                if zombie[1] == 0:
                    config += 1
                elif matrix[zombie[1]//8-1][zombie[0]//8] == WALL:
                    config += 1
                if zombie[0] == 7*8:
                    config += 2
                elif matrix[zombie[1]//8][zombie[0]//8+1] == WALL:
                    config += 2
                if zombie[0] == 0:
                    config += 8
                elif matrix[zombie[1]//8][zombie[0]//8-1] == WALL:
                    config += 8
                zombie = path_finder(zombie, config, 8)
                pyxel.blt(zombie[0]*4+8, zombie[1]*4+8, ZOMBIE[0], ZOMBIE[1], ZOMBIE[2], 16, 16)
            else:
                zombies.remove(zombie)
                bakery_hp -= 10
        self.cnt += 1
        if self.cnt == 60:
            zombies.append([0, 0])
            self.cnt = 0

    def __init__(self):
        global test_person, config
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE, "Zombies to Bakery")

        # Import des images fixes reliés aux endroits.
        pyxel.images[CAVE_1[0]].load(CAVE_1[1], CAVE_1[2], "cave_1.png")
        pyxel.images[CAVE_2[0]].load(CAVE_2[1], CAVE_2[2], "cave_2.png")
        pyxel.images[PATH[0]].load(PATH[1], PATH[2], "path_1.png")
        pyxel.images[PATH_2[0]].load(PATH_2[1], PATH_2[2], "path_2.png")
        pyxel.images[PATH_3[0]].load(PATH_3[1], PATH_3[2], "path_3.png")
        pyxel.images[PATH_4[0]].load(PATH_4[1], PATH_4[2], "path_4.png")
        pyxel.images[PATH_5[0]].load(PATH_5[1], PATH_5[2], "path_5.png")
        pyxel.images[BAKERY[0]].load(BAKERY[1], BAKERY[2], "bakery.png")
        pyxel.images[ZOMBIE[0]].load(ZOMBIE[1], ZOMBIE[2], "zombie.png")
        pyxel.images[TOWER[0]].load(TOWER[1], TOWER[2], "tower.png")
        pyxel.images[PROJ[0]].load(PROJ[1], PROJ[2], "bowl.png")
 
        while test_person[0] < 7 or test_person[1] < 7:
            if test_person[1] == 7:
                config += 4
            elif matrix[test_person[1]+1][test_person[0]] == WALL:
                config += 4
            if test_person[1] == 0:
                config += 1
            elif matrix[test_person[1]-1][test_person[0]] == WALL:
                config += 1
            if test_person[0] == 7:
                config += 2
            elif matrix[test_person[1]][test_person[0]+1] == WALL:
                config += 2
            if test_person[0] == 0:
                config += 8
            elif matrix[test_person[1]][test_person[0]-1] == WALL:
                config += 8
            test_person = path_finder(test_person, config)
            config = 0
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

tower_defense()
