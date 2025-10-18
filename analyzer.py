import matplotlib.pyplot as plt
import numpy as np
import time
from PrimLabytinthe import PrimLabyrinthe
from AStar_Manhattan import astar_manhattan
from AStar_Euclidienne import astar_euclidienne

class AnalyseurPerformance:
    def __init__(self):
        self.resultats = {}
    
    def executer_comparaison_complete(self, taille=31, nb_tests=5):
        """
        Exécute une comparaison complète sur plusieurs labyrinthes
        """
        print("=" * 80)
        print("ANALYSE COMPARATIVE COMPLÈTE - PARTIE 4")
        print("=" * 80)
        
        stats = {
            'BFS': {'temps': [], 'noeuds': [], 'longueurs': []},
            'A* Manhattan': {'temps': [], 'noeuds': [], 'longueurs': []},
            'A* Euclidienne': {'temps': [], 'noeuds': [], 'longueurs': []}
        }
        
        for i in range(nb_tests):
            print(f"\n--- Test {i+1}/{nb_tests} ---")
            
            # Générer un nouveau labyrinthe
            laby = PrimLabyrinthe(taille)
            laby._generer()
            start = (1, 1)
            goal = (taille-2, taille-2)
            
            # BFS
            t0 = time.perf_counter()
            chemin_bfs, noeuds_bfs = laby.bfs(start, goal)
            t1 = time.perf_counter()
            temps_bfs = (t1 - t0) * 1000.0
            
            # A* Manhattan
            t2 = time.perf_counter()
            chemin_man, noeuds_man = astar_manhattan(laby, start, goal)
            t3 = time.perf_counter()
            temps_man = (t3 - t2) * 1000.0
            
            # A* Euclidienne
            t4 = time.perf_counter()
            chemin_euc, noeuds_euc = astar_euclidienne(laby, start, goal)
            t5 = time.perf_counter()
            temps_euc = (t5 - t4) * 1000.0
            
            # Stocker les résultats
            for algo, chemin, noeuds, temps in [
                ('BFS', chemin_bfs, noeuds_bfs, temps_bfs),
                ('A* Manhattan', chemin_man, noeuds_man, temps_man),
                ('A* Euclidienne', chemin_euc, noeuds_euc, temps_euc)
            ]:
                if chemin:
                    stats[algo]['temps'].append(temps)
                    stats[algo]['noeuds'].append(noeuds)
                    stats[algo]['longueurs'].append(len(chemin) - 1)
            
            # Afficher résultats du test
            self._afficher_resultats_test(i+1, stats, taille)
        
        # Calcul des moyennes
        self._calculer_moyennes(stats)
        return stats
    
    def _afficher_resultats_test(self, test_num, stats, taille):
        """Affiche les résultats d'un test individuel"""
        print(f"Grille {taille}x{taille} - Test {test_num}:")
        print(f"{'Algorithme':<18} {'Noeuds':<10} {'Temps (ms)':<12} {'Longueur':<10}")
        print("-" * 60)
        
        for algo in ['BFS', 'A* Manhattan', 'A* Euclidienne']:
            if stats[algo]['noeuds']:
                idx = test_num - 1
                noeuds = stats[algo]['noeuds'][idx]
                temps = stats[algo]['temps'][idx]
                longueur = stats[algo]['longueurs'][idx]
                print(f"{algo:<18} {noeuds:<10} {temps:<12.2f} {longueur:<10}")
    
    def _calculer_moyennes(self, stats):
        """Calcule et affiche les moyennes"""
        print("\n" + "=" * 80)
        print("MOYENNES SUR TOUS LES TESTS")
        print("=" * 80)
        print(f"{'Algorithme':<18} {'Noeuds moy':<12} {'Temps moy (ms)':<15} {'Longueur moy':<12}")
        print("-" * 80)
        
        for algo in ['BFS', 'A* Manhattan', 'A* Euclidienne']:
            if stats[algo]['noeuds']:
                noeuds_moy = np.mean(stats[algo]['noeuds'])
                temps_moy = np.mean(stats[algo]['temps'])
                longueur_moy = np.mean(stats[algo]['longueurs'])
                
                print(f"{algo:<18} {noeuds_moy:<12.0f} {temps_moy:<15.2f} {longueur_moy:<12.2f}")
    
    def repondre_questions_theoriques(self):
        """Répond aux questions théoriques de la partie 4"""
        print("\n" + "=" * 80)
        print("RÉPONSES AUX QUESTIONS THÉORIQUES - PARTIE 4")
        print("=" * 80)
        
        reponses = [
            "1. Quelle heuristique est la plus efficace ?",
            "   → Manhattan est généralement plus efficace pour les déplacements en 4 directions",
            "   car elle correspond exactement au coût réel. Euclidienne peut être plus précise",
            "   mais nécessite des calculs plus lourds (racine carrée).",
            "",
            "2. Que se passe-t-il si l'heuristique surestime le coût réel ?",
            "   → L'heuristique n'est plus admissible. A* peut alors trouver un chemin sous-optimal",
            "   ou explorer plus de nœuds que nécessaire. L'optimalité n'est plus garantée.",
            "",
            "3. Peut-on avoir une solution non optimale avec A* ?",
            "   → OUI, dans deux cas :",
            "     - Si l'heuristique n'est pas admissible (surestimation)",
            "     - Si l'heuristique n'est pas cohérente (inégalité triangulaire non respectée)",
            "   Avec Manhattan/Euclidienne sur grille, les solutions sont optimales.",
            "",
            "4. Quelle est la complexité moyenne d'A* par rapport à BFS ?",
            "   → BFS: O(b^d) dans le pire cas, où b = facteur de branchement, d = profondeur",
            "   → A*: O(b^d) dans le pire cas, mais en pratique O(b^(d/2)) avec une bonne heuristique",
            "   → A* explore généralement 2-10x moins de nœuds que BFS selon la qualité de l'heuristique",
            "",
            "5. Dans quel contexte BFS reste-t-il utile ?",
            "   → Quand on veut TOUS les chemins optimaux (BFS les trouve naturellement)",
            "   → Quand l'espace de recherche est petit et simple",
            "   → Quand on n'a pas de bonne heuristique disponible",
            "   → Pour la validation (BFS donne toujours le chemin optimal comme référence)",
            "   → Dans les graphes non pondérés où l'optimalité est cruciale",
        ]
        
        for reponse in reponses:
            print(reponse)

# MAIN SPÉCIFIQUE POUR PARTIE 4
if __name__ == "__main__":
    print("  ANALYSE COMPARATIVE")
    print("Comparaison BFS vs A* Manhattan vs A* Euclidienne")
    print("=" * 60)
    
    analyseur = AnalyseurPerformance()
    
    # Exécuter la comparaison
    stats = analyseur.executer_comparaison_complete(taille=25, nb_tests=3)
    
    # Répondre aux questions théoriques
    analyseur.repondre_questions_theoriques()
    
    print("\n" + "=" * 80)
   