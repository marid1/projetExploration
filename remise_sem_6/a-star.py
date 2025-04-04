import pygame
import heapq

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 255, 255)
GRIS = (200, 200, 200)
JAUNE = (255, 255, 0)

# Définir la grille
grille = [
    ['S', '.', '.', '#', '.', '.', '.', '.'],
    ['.', '.', '.', '#', '.', '.', '.', '.'],
    ['#', '.', '.', '.', '.', '.', '.', '.'],
    ['#', '#', '#', '.', '#', '#', '#', '.'],
    ['#', '.', '.', '.', '.', '.', '#', '.'],
    ['.', '.', '.', '#', '.', '.', '#', '.'],
    ['.', '.', '.', '#', '.', '.', '#', '#'],
    ['.', '.', '.', '#', '.', '.', '.', 'G'],
]

# Paramètres de la grille
TAILLE_GRILLE = 8
TAILLE_CELLULE = 100
TAILLE_FENETRE = TAILLE_GRILLE * TAILLE_CELLULE
ecran = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))

# Initialisation de Pygame
pygame.init()
ecran = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
pygame.display.set_caption("Visualisation du Pathfinding A*")

# Classe du nœud A*
class Case:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float('inf')  # Coût depuis le début
        self.h = 0  # Estimation du coût vers la fin
        self.f = float('inf')  # g + h
        self.parent = None  # Pour reconstruire le chemin

    def __lt__(self, autre):
        return (self.f, self.h) < (autre.f, autre.h)  # Tri par priorité

def heuristique(a, b):
    """Fonction de distance heuristique"""
    return abs(a.x - b.x) + abs(a.y - b.y)

def obtenir_voisins(case):
    """Retourne les voisins valides"""
    directions = [(0,1), (1,0), (0,-1), (-1,0)]  # Directions possibles
    voisins = []
    
    for dx, dy in directions:
        x, y = case.x + dx, case.y + dy
        if 0 <= x < TAILLE_GRILLE and 0 <= y < TAILLE_GRILLE and grille[x][y] != "#":
            voisins.append(Case(x, y))
    
    return voisins

def a_star(depart, but):
    """Affichage du pathfinding avec un pas manuel"""
    liste_ouverte = []
    heapq.heappush(liste_ouverte, (depart.f, depart.h, depart))
    depart.g = 0
    depart.h = heuristique(depart, but)  # Calcul de l'heuristique pour la case de départ
    depart.f = depart.g + depart.h  # Mise à jour du coût total f

    liste_fermee = set()
    
    while liste_ouverte:
        ecran.fill(BLANC)  # Effacer l'écran
        dessiner_grille()

        _, _, courant = heapq.heappop(liste_ouverte)

        if (courant.x, courant.y) == (but.x, but.y):
            return reconstruire_chemin(courant)

        liste_fermee.add((courant.x, courant.y))

        for voisin in obtenir_voisins(courant):
            if (voisin.x, voisin.y) in liste_fermee:
                continue

            temp_g = courant.g + 1  # coût entre les cases = 1

            # Vérifier si le chemin vers le voisin est meilleur
            if temp_g < voisin.g:
                voisin.parent = courant
                voisin.g = temp_g
                voisin.h = heuristique(voisin, but)  # Recalculer h pour chaque voisin
                voisin.f = voisin.g + voisin.h  # Mettre à jour f (g + h)

                # Mettre à jour la liste
                heapq.heappush(liste_ouverte, (voisin.f, voisin.h, voisin))

        # Visualisation des couleurs
        dessiner_cases(liste_ouverte, liste_fermee, courant)
        pygame.display.update()

        # Attendre que l'utilisateur appuie sur ESPACE pour continuer
        attendre_barre_espace()

    return None  # Si aucun chemin trouvé

def attendre_barre_espace():
    """Pause l'exécution jusqu'à ce que l'utilisateur appuie sur la touche ESPACE"""
    attente = True
    while attente:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                attente = False

def reconstruire_chemin(case):
    """Reconstruire le chemin à partir des parents des nœuds"""
    chemin = []
    while case:
        chemin.append((case.x, case.y))
        case = case.parent
    return chemin[::-1]  # Chemin inversé

def dessiner_grille():
    """Dessiner la grille à l'écran"""
    for x in range(TAILLE_GRILLE):
        for y in range(TAILLE_GRILLE):
            rect = pygame.Rect(x * TAILLE_CELLULE, y * TAILLE_CELLULE, TAILLE_CELLULE, TAILLE_CELLULE)
            pygame.draw.rect(ecran, NOIR, rect, 1)

            if grille[x][y] == "#":
                pygame.draw.rect(ecran, NOIR, rect)  # Obstacles
            elif grille[x][y] == "S":
                pygame.draw.rect(ecran, VERT, rect)  # Départ
            elif grille[x][y] == "G":
                pygame.draw.rect(ecran, ROUGE, rect)  # But

def dessiner_cases(liste_ouverte, liste_fermee, courant):
    """Colorier et afficher les coûts des nœuds en cours d'exploration"""
    font = pygame.font.Font(None, 20) 

    for x, y in liste_fermee:
        rect = pygame.Rect(x * TAILLE_CELLULE, y * TAILLE_CELLULE, TAILLE_CELLULE, TAILLE_CELLULE)
        pygame.draw.rect(ecran, GRIS, rect)  # Cases explorés

        # Afficher le coût g
        texte = font.render(f"", True, NOIR)
        ecran.blit(texte, (x * TAILLE_CELLULE + 5, y * TAILLE_CELLULE + 5))

    for _, _, case in liste_ouverte:
        rect = pygame.Rect(case.x * TAILLE_CELLULE, case.y * TAILLE_CELLULE, TAILLE_CELLULE, TAILLE_CELLULE)
        pygame.draw.rect(ecran, BLEU, rect)  # Cases à explorer

        # Afficher les coûts g, h, f
        texte_g = font.render(f"g:{case.g}", True, NOIR)
        texte_h = font.render(f"h:{case.h}", True, NOIR)
        texte_f = font.render(f"f:{case.f}", True, NOIR)

        ecran.blit(texte_g, (case.x * TAILLE_CELLULE + 5, case.y * TAILLE_CELLULE + 5))
        ecran.blit(texte_h, (case.x * TAILLE_CELLULE + 5, case.y * TAILLE_CELLULE + 20))
        ecran.blit(texte_f, (case.x * TAILLE_CELLULE + 5, case.y * TAILLE_CELLULE + 35))

    # Case actuel
    rect = pygame.Rect(courant.x * TAILLE_CELLULE, courant.y * TAILLE_CELLULE, TAILLE_CELLULE, TAILLE_CELLULE)
    pygame.draw.rect(ecran, VERT, rect)

    # Afficher les coûts
    texte_g = font.render(f"g:{courant.g}", True, NOIR)
    texte_h = font.render(f"h:{courant.h}", True, NOIR)
    texte_f = font.render(f"f:{courant.f}", True, NOIR)

    ecran.blit(texte_g, (courant.x * TAILLE_CELLULE + 5, courant.y * TAILLE_CELLULE + 5))
    ecran.blit(texte_h, (courant.x * TAILLE_CELLULE + 5, courant.y * TAILLE_CELLULE + 20))
    ecran.blit(texte_f, (courant.x * TAILLE_CELLULE + 5, courant.y * TAILLE_CELLULE + 35))

def dessiner_chemin(chemin):
    """Dessiner le chemin final."""
    for x, y in chemin:
        rect = pygame.Rect(x * TAILLE_CELLULE, y * TAILLE_CELLULE, TAILLE_CELLULE, TAILLE_CELLULE)
        pygame.draw.rect(ecran, JAUNE, rect)  # Chemin (jaune)

# Trouver les positions de départ et d'arrivée
debut_pos, but_pos = None, None
for x in range(TAILLE_GRILLE):
    for y in range(TAILLE_GRILLE):
        if grille[x][y] == "S":
            debut_pos = (x, y)
        elif grille[x][y] == "G":
            but_pos = (x, y)

debut = Case(*debut_pos)
but = Case(*but_pos)

# Exécution
chemin = a_star(debut, but)

# Afficher le chemin final
if chemin:
    dessiner_chemin(chemin)
    pygame.display.update()

# Boucle de jeu
en_cours = True
while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

pygame.quit()