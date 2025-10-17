from collections import deque
import random
import matplotlib.pyplot as plt

class PrimLabyrinthe:
  def __init__(self, taille): #le cstr qui s'execute automatiquement quand on crée un objet de cette classe
    self.taille=taille
    """
    1 pour mur
    0 pour cellule
    """
    self.grille=[[1 for _ in range(taille)] for _ in range(taille)]   # grille initiale tous des murs

  def _voisin(self, x, y):
      voisins=[]
      directions=[(0,1), (0,-1), (1,0), (-1,0)]
      for dx, dy in directions:
         nx, ny=x+dx, y+dy
         if 0<=nx<self.taille and 0<=ny<self.taille:
            voisins.append((nx,ny))
      return voisins

  def _generer(self):
     """
     Génère un labyrinthe parfait (chemin unique) via l'algorithme de Prim.
     Représentation: grille de taille N×N avec N>=3. Les murs restent à 1.
     Les cellules (chemins) sont sur des coordonnées impaires; les murs entre
     deux cellules sont aux coordonnées paires/impaires (entre elles). On casse
     UNIQUEMENT les murs sélectionnés pour relier deux cellules, ce qui évite les cycles.
     """
     N = self.taille
     if N < 3:
        # Cas trivial: trop petit pour un vrai labyrinthe
        if N >= 1:
           self.grille[0][0] = 0
        return self.grille

     # Point de départ sur des coordonnées impaires (à l'intérieur des bords)
     x0 = random.randrange(1, N, 2)
     y0 = random.randrange(1, N, 2)
     self.grille[x0][y0] = 0

     visites = {(x0, y0)}
     murs = []  # éléments: (wx, wy, cx, cy, nx, ny) avec (wx,wy) le mur entre (cx,cy) et (nx,ny)

     def ajouter_murs_autour(cx, cy):
        for dx, dy in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
           nx, ny = cx + dx, cy + dy
           wx, wy = cx + dx // 2, cy + dy // 2  # mur entre les deux cellules
           if 0 < nx < N - 1 and 0 < ny < N - 1:
              murs.append((wx, wy, cx, cy, nx, ny))

     ajouter_murs_autour(x0, y0)

     # Boucle principale de Prim: tant qu'il reste des murs en frontière
     while murs:
        idx = random.randrange(len(murs))
        wx, wy, cx, cy, nx, ny = murs.pop(idx)

        if (nx, ny) not in visites:
           # Casser le mur et ouvrir la nouvelle cellule
           self.grille[wx][wy] = 0
           self.grille[nx][ny] = 0
           visites.add((nx, ny))
           ajouter_murs_autour(nx, ny)

     return self.grille

  #visualisation du labyrinthe avec matplotlib
  def _afficher(self, grille=None, title=None, chemin=None):
     plt.figure(figsize=(6,6))
     data = self.grille if grille is None else grille
     plt.imshow(data, cmap='binary', interpolation='nearest')

     # Overlay du chemin en rouge (si fourni)
     if chemin:
         xs = [y + 0.5 for (x, y) in chemin]
         ys = [x + 0.5 for (x, y) in chemin]
         plt.plot(xs, ys, color='red', linewidth=2, zorder=3)
         # marquer début/fin
         sx, sy = chemin[0]
         ex, ey = chemin[-1]
         plt.scatter([sy + 0.5], [sx + 0.5], c='green', s=40, zorder=4)
         plt.scatter([ey + 0.5], [ex + 0.5], c='blue', s=40, zorder=4)

     plt.xticks([]); plt.yticks([])
     if title is None:
         plt.title(f"Labyrinthe Prim {self.taille}×{self.taille}")
     else:
         plt.title(title)
     plt.show()
  
  def bfs(self, depart, arrivee):
        """
        Retourne la liste de cases [(x,y), ...] entre depart et arrivee via BFS,
        ou None si pas de chemin.
        """
        queue   = deque([depart])
        visited = {depart}
        parent  = {}

        while queue:
            x, y = queue.popleft()
            if (x, y) == arrivee:
                # reconstruction du chemin
                chemin = []
                cur = arrivee
                while cur != depart:
                    chemin.append(cur)
                    cur = parent[cur]
                chemin.append(depart)
                return list(reversed(chemin))

            for nx, ny in self._voisin(x, y):
                if self.grille[nx][ny] == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

        return None  # aucun chemin trouvé


if __name__ == "__main__":
   taille=21  # idéalement impair pour une meilleure symétrie
   # Dans cette représentation, les cellules (chemins) sont aux coordonnées impaires
   start = (1, 1)
   end   = (taille-2, taille-2)

   laby = PrimLabyrinthe(taille)
   grille = laby._generer()

   # Labyrinthe parfait: il existe toujours un chemin unique entre deux cellules
   chemin = laby.bfs(start, end)

   if chemin is None:
        print("Aucun chemin trouvé (cas anormal).")
        laby._afficher(title="Labyrinthe (aucun chemin trouvé)")
   else:
        print("Chemin BFS :", chemin)
        laby._afficher(title="Labyrinthe parfait (Prim) + Chemin BFS", chemin=chemin)
