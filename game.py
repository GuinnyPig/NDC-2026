import pyxel

# Définitions des dimensions de l'écran et une "tuile" de l'écran.
SCREEN_SIZE = 256
TILE_SIZE = 32

CAVE = [0, 32, 0]
CAVE2 = [0, 32, 32]
VOID = [0, 0, 0]
CASTEL = [0, 64, 0]

# Matrice de 8x8 avec chaque case contenant un tableau de 3 nombres:
#   numéro de la banque d'images, abscisse et ordonnée dans l'image.
# La matrice ici représente l'écran.
matrix = [[VOID for line in range(8)] for column in range(8)]
matrix[0][0] = CAVE
matrix[1][0] = CAVE2
class App:
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(11)

        # Dessin de la matrice.
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                if x == 7 and y == 7:
                    pyxel.rect(x*32, y*32, TILE_SIZE, TILE_SIZE, 2)
                else: 
                    pyxel.blt(x*32, y*32, matrix[y][x][0], matrix[y][x][1], matrix[y][x][2], TILE_SIZE, TILE_SIZE)

    def __init__(self):
        pyxel.init(SCREEN_SIZE, SCREEN_SIZE, "Tower Defense")

        # Import des images fixes reliés aux endroits.
        pyxel.images[CAVE[0]].load(CAVE[1], CAVE[2], "cave.png")

        pyxel.run(self.update, self.draw)

App()