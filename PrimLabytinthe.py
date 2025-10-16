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
     #choix du point de depart au hasarh
     x0, y0=random.randrange(self.taille), random.randrange(self.taille)
     self.grille[x0][y0]=0
     #stocker les murs voisins du cellule avec set
     murs=set(self._voisin(x0, y0))
     #condition d'arrêt c'est quand la liste des murs est vide
     while murs:
        
        #choix aleatoire d'un mur avec pop
        mx, my=murs.pop()
        chemins_adj=[(nx,ny) for(nx,ny) in self._voisin(mx,my) if self.grille[nx][ny]==0] #liste des voisins du murs qui sont visités
        if len(chemins_adj)==1:
           self.grille[mx][my]=0
           #i++
           for n in self._voisin(mx,my):
              if self.grille[n[0]][n[1]]==1:
                 murs.add(n)
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
   taille=21
   start= (0, 0)
   end = (taille-1, taille-1)
   laby=PrimLabyrinthe(taille)
   grille=laby._generer()

   # S'assurer que start et end sont des cellules vides
   for pt in (start, end):
        if laby.grille[pt[0]][pt[1]] == 1:
            laby.grille[pt[0]][pt[1]] = 0

   # Calcul du chemin BFS
   chemin = laby.bfs(start, end)

   if chemin is None:
        print("Aucun chemin trouvé en BFS.")
        laby._afficher(title="Labyrinthe sans chemin")
   else:
        print("Chemin BFS :", chemin)
        laby._afficher(title="Labyrinthe + Chemin BFS", chemin=chemin)
