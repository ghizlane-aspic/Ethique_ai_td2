import heapq
import math
import time
import random
from typing import Dict, List, Optional, Tuple

# Importer la génération de labyrinthe et BFS existants
from PrimLabytinthe import PrimLabyrinthe
# Réutiliser l'implémentation A* Manhattan pour la comparaison
from AStar_Manhattan import astar_manhattan

Coord = Tuple[int, int]


def euclidienne(a: Coord, b: Coord) -> float:
    """
    Heuristique Euclidienne h(n) = sqrt((x1 - x2)^2 + (y1 - y2)^2)
    """
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.hypot(dx, dy)


def reconstruire_chemin(parent: Dict[Coord, Coord], start: Coord, goal: Coord) -> List[Coord]:
    cur = goal
    chemin = [cur]
    while cur != start:
        cur = parent[cur]
        chemin.append(cur)
    chemin.reverse()
    return chemin


def astar_euclidienne(laby: PrimLabyrinthe, start: Coord, goal: Coord) -> Tuple[Optional[List[Coord]], int]:
    """
    A* avec f(n) = g(n) + h(n) et heuristique Euclidienne.

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

    open_heap: List[Tuple[float, int, int, Coord]] = []  # (f, g, tie, node)
    gscore: Dict[Coord, int] = {start: 0}
    parent: Dict[Coord, Coord] = {}

    # Initialisation
    tie = 0  # pour stabilité en cas d'égalité
    f0 = euclidienne(start, goal)
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
                fval = tentative_g + euclidienne(neigh, goal)
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

    # BFS (deja implémenté dans PrimLabyrinthe)
    t0 = time.perf_counter()
    chemin_bfs, explores_bfs = laby.bfs(start, goal)
    t1 = time.perf_counter()
    duree_bfs_ms = (t1 - t0) * 1000.0

    # A* Manhattan
    t2 = time.perf_counter()
    chemin_astar_m, explores_astar_m = astar_manhattan(laby, start, goal)
    t3 = time.perf_counter()
    duree_astar_m_ms = (t3 - t2) * 1000.0

    # A* Euclidienne
    t4 = time.perf_counter()
    chemin_astar_e, explores_astar_e = astar_euclidienne(laby, start, goal)
    t5 = time.perf_counter()
    duree_astar_e_ms = (t5 - t4) * 1000.0

    # Longueurs (en arêtes)
    len_bfs = (len(chemin_bfs) - 1) if chemin_bfs else None
    len_astar_m = (len(chemin_astar_m) - 1) if chemin_astar_m else None
    len_astar_e = (len(chemin_astar_e) - 1) if chemin_astar_e else None

    # Affichage comparatif complet
    print("\nComparaison complète: BFS vs A* (Manhattan) vs A* (Euclidienne) sur un labyrinthe Prim")
    print(f"Taille: {taille} | Départ: {start} | Arrivée: {goal}")
    print()
    header = f"{'Méthode':<18} {'Explorés':>10} {'Temps (ms)':>12} {'Longueur':>10}"
    print(header)
    print("-" * len(header))
    print(f"{'BFS':<18} {explores_bfs:>10} {duree_bfs_ms:>12.2f} {str(len_bfs):>10}")
    print(f"{'A* (Manhattan)':<18} {explores_astar_m:>10} {duree_astar_m_ms:>12.2f} {str(len_astar_m):>10}")
    print(f"{'A* (Euclidienne)':<18} {explores_astar_e:>10} {duree_astar_e_ms:>12.2f} {str(len_astar_e):>10}")

    # Identification de la meilleure heuristique (par défaut: moins de nœuds explorés, puis temps)
    meilleure = None
    critere = None
    if explores_astar_m < explores_astar_e:
        meilleure = "Manhattan"
        critere = "nœuds explorés"
    elif explores_astar_e < explores_astar_m:
        meilleure = "Euclidienne"
        critere = "nœuds explorés"
    else:
        # Égalité en explorations -> comparer le temps
        if duree_astar_m_ms < duree_astar_e_ms:
            meilleure = "Manhattan"
            critere = "temps"
        elif duree_astar_e_ms < duree_astar_m_ms:
            meilleure = "Euclidienne"
            critere = "temps"
        else:
            meilleure = "Égalité"
            critere = "—"

    print()
    if meilleure == "Égalité":
        print("Meilleure heuristique: Égalité (mêmes explorations et temps comparables)")
    else:
        print(f"Meilleure heuristique: {meilleure} (selon {critere})")

    # Visualisation optionnelle avec le chemin A* Euclidienne
    if chemin_astar_e:
        laby._afficher(title=f"Labyrinthe + Chemin A* Euclidienne (L={len_astar_e})", chemin=chemin_astar_e)
    else:
        print("Aucun chemin trouvé par A* Euclidienne (cas improbable dans un labyrinthe parfait).")
