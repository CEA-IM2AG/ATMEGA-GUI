import matplotlib.pyplot as plt
import numpy as np

def print_bitmap(matrix, zoom=False):
    """
        prend une matrice 32x32 de valeurs de modification
            0 = bit inchange
            1 = bit set
            2 = bit reset
            3 = court-jus

        plot le bitmap de la RAM

        :param matrix: matrice des valeurs de modification
        :param zoom: option de zoom pour ignorer les lignes de bits inchanges
    """
    borne_x = 31 # indice de la derniere colonne de matrix
    borne_y = 31 # indice de la dernere ligne de matrix
    if zoom: # option zoom activable depuis
    # la fenetre de visualisation
        can_zoom = True # indique si la ligne
        # peut etre supprimee
        while can_zoom:
            if matrix[0] == [0]*(borne_x+1):
            # ligne de bits inchanges
                matrix.pop(0)
                borne_y -= 1
            else:
                can_zoom = False
        can_zoom = True
        # refaire pour le "bas" de la matrice
        while can_zoom:
            if matrix[borne_y] == [0]*(borne_x+1):
                matrix.pop(borne_y)
                borne_y -= 1
            else:
                can_zoom = False
        can_zoom = True
        # refaire pour la "gauche" de la matrice
        while can_zoom:
            for i in range(borne_y+1):
                if matrix[i][0] != 0:
                    can_zoom = False
            if can_zoom:
                for i in range(borne_y+1):
                    matrix[i].pop(0)
                borne_x -= 1
            else:
                can_zoom = False
        can_zoom = True
        # refaire pour la "droite" de la matrice
        while can_zoom:
            for i in range(borne_y+1):
                if matrix[i][borne_x] != 0:
                    can_zoom = False
            if can_zoom:
                for i in range(borne_y+1):
                    matrix[i].pop(borne_x)
                borne_x -= 1
            else:
                can_zoom = False
        
    colors = [[0 for i in range(borne_x+1)] for j in range(borne_y+1)]
    # colors est une copie de matrix ou chaque element est remplace par une couleur
    for i in range(borne_y+1):
        for j in range(borne_x+1):
            x = matrix[i][j]
            if x == 0:
                colors[i][j] = [255, 255, 255]
            elif x == 1:
                colors[i][j] = [255, 0, 0]
            elif x == 2:
                colors[i][j] = [0, 0, 255]
            else:
                colors[i][j] = [255, 255, 0]    
    plt.imshow(colors)
    plt.axis('off')
    plt.show()
