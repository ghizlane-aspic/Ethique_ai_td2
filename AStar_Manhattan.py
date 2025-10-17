import heapq
import time
import random
from typing import Dict, List, Optional, Tuple

# Importer la génération de labyrinthe et BFS existants
from PrimLabytinthe import PrimLabyrinthe

Coord = Tuple[int, int]


def manhattan(a: Coord, b: Coord) -> int:
    """
    Heuristique Manhattan h(n) = |x1 - x2| + |y1 - y2|
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruire_chemin(parent: Dict[Coord, Coord], start: Coord, goal: Coord) -> List[Coord]:
    cur = goal
    chemin = [cur]
    while cur != start:
        cur = parent[cur]
        chemin.append(cur)
    chemin.reverse()
    return chemin


def astar_manhattan(laby: PrimLabyrinthe, start: Coord, goal: Coord) -> Tuple[Optional[List[Coord]], int]:
    """
    A* avec f(n) = g(n) + h(n) et heuristique Manhattan.

    Paramètres:
      - laby: instance de PrimLabyrinthe (utilise laby.grille et laby._voisin)
      - start, goal: coordonnées (x, y)

    Retourne:
      - (chemin: List[(x,y)] | None, explores: int)
        chemin est None s'il n'existe pas.
        explores = nombre de nœuds dépilés (expandus) depuis la file de priorité.
    """
    # Sécurité: si départ/arrivée sont des murs, on les ouvre
    if laby.grille[start[0]][start[1]] == 1:
        laby.grille[start[0]][start[1]] = 0
    if laby.grille[goal[0]][goal[1]] == 1:
        laby.grille[goal[0]][goal[1]] = 0

    open_heap: List[Tuple[int, int, int, Coord]] = []  # (f, g, tie, node)
    gscore: Dict[Coord, int] = {start: 0}
    parent: Dict[Coord, Coord] = {}

    # Initialisation
    tie = 0  # pour stabilité en cas d'égalité
    f0 = manhattan(start, goal)
    heapq.heappush(open_heap, (f0, 0, tie, start))

    explores = 0

    while open_heap:
        fcur, gcur, _, cur = heapq.heappop(open_heap)
        explores += 1

        # Si on a un meilleur g découvert après cet entry (obsolète), on ignore
        if gcur != gscore.get(cur, float('inf')):
            continue

        if cur == goal:
            chemin = reconstruire_chemin(parent, start, goal)
            return chemin, explores

        # Expansion
        for nx, ny in laby._voisin(cur[0], cur[1]):
            if laby.grille[nx][ny] != 0:
                continue  # mur
            tentative_g = gcur + 1
            neigh = (nx, ny)

            if tentative_g < gscore.get(neigh, float('inf')):
                parent[neigh] = cur
                gscore[neigh] = tentative_g
                tie += 1
                fval = tentative_g + manhattan(neigh, goal)
                heapq.heappush(open_heap, (fval, tentative_g, tie, neigh))

    # Aucun chemin
    return None, explores


if __name__ == "__main__":
    # Paramètres du test
    taille = 31  # idéalement impair
    start: Coord = (1, 1)
    goal: Coord = (taille - 2, taille - 2)

    # Option de reproductibilité
    random.seed(0)

    # Générer un labyrinthe parfait via Prim
    laby = PrimLabyrinthe(taille)
    _ = laby._generer()

    # A* Manhattan
    t0 = time.perf_counter()
    chemin_astar, explores_astar = astar_manhattan(laby, start, goal)
    t1 = time.perf_counter()
    duree_astar_ms = (t1 - t0) * 1000.0

    # BFS (deja implémenté dans PrimLabyrinthe)
    t2 = time.perf_counter()
    chemin_bfs, explores_bfs = laby.bfs(start, goal)
    t3 = time.perf_counter()
    duree_bfs_ms = (t3 - t2) * 1000.0

    # Longueurs (en arêtes)
    len_astar = (len(chemin_astar) - 1) if chemin_astar else None
    len_bfs = (len(chemin_bfs) - 1) if chemin_bfs else None

    # Affichage comparatif partiel
    print("\nComparaison partielle: A* (Manhattan) vs BFS sur un labyrinthe Prim")
    print(f"Taille: {taille} | Départ: {start} | Arrivée: {goal}")
    print()
    header = f"{'Méthode':<16} {'Explorés':>10} {'Temps (ms)':>12} {'Longueur':>10}"
    print(header)
    print("-" * len(header))
    print(f"{'BFS':<16} {explores_bfs:>10} {duree_bfs_ms:>12.2f} {str(len_bfs):>10}")
    print(f"{'A* (Manhattan)':<16} {explores_astar:>10} {duree_astar_ms:>12.2f} {str(len_astar):>10}")

    # Visualisation optionnelle avec le chemin A*
    if chemin_astar:
        laby._afficher(title=f"Labyrinthe + Chemin A* Manhattan (L={len_astar})", chemin=chemin_astar)
    else:
        print("Aucun chemin trouvé par A* (cas improbable dans un labyrinthe parfait).")
