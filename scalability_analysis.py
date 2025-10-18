import matplotlib.pyplot as plt
import numpy as np
import time
from PrimLabytinthe import PrimLabyrinthe
from AStar_Manhattan import astar_manhattan
from AStar_Euclidienne import astar_euclidienne

class AnalyseurScalabilite:
    def __init__(self):
        self.resultats = {}
    
    def analyser_scalabilite(self, tailles=[15, 25, 35, 45], nb_tests_par_taille=3):
        """
        Analyse l'évolution des performances avec la taille des grilles
        """
        
        
        # Structures pour stocker les données
        donnees_temps = {'BFS': [], 'A* Manhattan': [], 'A* Euclidienne': []}
        donnees_noeuds = {'BFS': [], 'A* Manhattan': [], 'A* Euclidienne': []}
        donnees_temps_std = {'BFS': [], 'A* Manhattan': [], 'A* Euclidienne': []}
        donnees_noeuds_std = {'BFS': [], 'A* Manhattan': [], 'A* Euclidienne': []}
        
        for taille in tailles:
            print(f"\n--- Analyse pour grille {taille}x{taille} ---")
            
            temps_taille = {'BFS': [], 'A* Manhattan': [], 'A* Euclidienne': []}
            noeuds_taille = {'BFS': [], 'A* Manhattan': [], 'A* Euclidienne': []}
            
            for test in range(nb_tests_par_taille):
                print(f"  Test {test+1}/{nb_tests_par_taille}...")
                
                # Générer labyrinthe
                laby = PrimLabyrinthe(taille)
                laby._generer()
                start = (1, 1)
                goal = (taille-2, taille-2)
                
                # Mesurer BFS
                t0 = time.perf_counter()
                chemin_bfs, noeuds_bfs = laby.bfs(start, goal)
                t1 = time.perf_counter()
                if chemin_bfs:
                    temps_taille['BFS'].append((t1 - t0) * 1000.0)
                    noeuds_taille['BFS'].append(noeuds_bfs)
                
                # Mesurer A* Manhattan
                t2 = time.perf_counter()
                chemin_man, noeuds_man = astar_manhattan(laby, start, goal)
                t3 = time.perf_counter()
                if chemin_man:
                    temps_taille['A* Manhattan'].append((t3 - t2) * 1000.0)
                    noeuds_taille['A* Manhattan'].append(noeuds_man)
                
                # Mesurer A* Euclidienne
                t4 = time.perf_counter()
                chemin_euc, noeuds_euc = astar_euclidienne(laby, start, goal)
                t5 = time.perf_counter()
                if chemin_euc:
                    temps_taille['A* Euclidienne'].append((t5 - t4) * 1000.0)
                    noeuds_taille['A* Euclidienne'].append(noeuds_euc)
            
            # Calculer moyennes et écarts-types pour cette taille
            for algo in ['BFS', 'A* Manhattan', 'A* Euclidienne']:
                if temps_taille[algo]:
                    donnees_temps[algo].append(np.mean(temps_taille[algo]))
                    donnees_noeuds[algo].append(np.mean(noeuds_taille[algo]))
                    donnees_temps_std[algo].append(np.std(temps_taille[algo]))
                    donnees_noeuds_std[algo].append(np.std(noeuds_taille[algo]))
                    
                    print(f"{algo:<18} | Temps: {donnees_temps[algo][-1]:.2f} ± {donnees_temps_std[algo][-1]:.2f} ms | "
                          f"Noeuds: {donnees_noeuds[algo][-1]:.0f} ± {donnees_noeuds_std[algo][-1]:.0f}")
        
        # Générer les graphiques
        self._generer_graphiques(tailles, donnees_temps, donnees_noeuds, 
                               donnees_temps_std, donnees_noeuds_std)
        
        return donnees_temps, donnees_noeuds
    
    def _generer_graphiques(self, tailles, donnees_temps, donnees_noeuds, 
                          donnees_temps_std, donnees_noeuds_std):
        """Génère les graphiques d'évolution avec affichage corrigé"""
        print("\n📊 Génération des graphiques...")
        
        # Création de la figure avec plus d'espace
        fig = plt.figure(figsize=(16, 10))
        
        # Ajuster les marges pour éviter le chevauchement
        plt.subplots_adjust(left=0.08, right=0.95, top=0.93, bottom=0.08, 
                           hspace=0.35, wspace=0.25)
        
        # Créer les sous-graphiques
        ax1 = plt.subplot(2, 2, 1)
        ax2 = plt.subplot(2, 2, 2)
        ax3 = plt.subplot(2, 2, 3)
        ax4 = plt.subplot(2, 2, 4)
        
        # Styles
        marqueurs = {'BFS': 'o', 'A* Manhattan': 's', 'A* Euclidienne': '^'}
        couleurs = {'BFS': 'red', 'A* Manhattan': 'blue', 'A* Euclidienne': 'green'}
        
        # Graphique 1: Temps d'exécution
        for algo in ['BFS', 'A* Manhattan', 'A* Euclidienne']:
            if donnees_temps[algo]:
                ax1.plot(tailles[:len(donnees_temps[algo])], donnees_temps[algo], 
                        marker=marqueurs[algo], color=couleurs[algo], label=algo, 
                        linewidth=2.5, markersize=8)
                ax1.fill_between(tailles[:len(donnees_temps[algo])],
                               np.array(donnees_temps[algo]) - np.array(donnees_temps_std[algo]),
                               np.array(donnees_temps[algo]) + np.array(donnees_temps_std[algo]),
                               alpha=0.2, color=couleurs[algo])
        
        ax1.set_xlabel('Taille de la grille', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Temps (ms)', fontsize=11, fontweight='bold')
        ax1.set_title('Temps d\'exécution vs Taille', fontsize=12, fontweight='bold', pad=10)
        ax1.legend(fontsize=9, loc='upper left')
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.tick_params(labelsize=9)
        
        # Graphique 2: Nombre de nœuds explorés
        for algo in ['BFS', 'A* Manhattan', 'A* Euclidienne']:
            if donnees_noeuds[algo]:
                ax2.plot(tailles[:len(donnees_noeuds[algo])], donnees_noeuds[algo],
                        marker=marqueurs[algo], color=couleurs[algo], label=algo, 
                        linewidth=2.5, markersize=8)
                ax2.fill_between(tailles[:len(donnees_noeuds[algo])],
                               np.array(donnees_noeuds[algo]) - np.array(donnees_noeuds_std[algo]),
                               np.array(donnees_noeuds[algo]) + np.array(donnees_noeuds_std[algo]),
                               alpha=0.2, color=couleurs[algo])
        
        ax2.set_xlabel('Taille de la grille', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Nœuds explorés', fontsize=11, fontweight='bold')
        ax2.set_title('Nœuds explorés vs Taille', fontsize=12, fontweight='bold', pad=10)
        ax2.legend(fontsize=9, loc='upper left')
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.tick_params(labelsize=9)
        
        # Graphique 3: Ratio d'efficacité (BFS / A*)
        if len(donnees_noeuds['BFS']) == len(donnees_noeuds['A* Manhattan']):
            ratio_man = np.array(donnees_noeuds['BFS']) / np.array(donnees_noeuds['A* Manhattan'])
            ratio_euc = np.array(donnees_noeuds['BFS']) / np.array(donnees_noeuds['A* Euclidienne'])
            
            ax3.plot(tailles[:len(donnees_noeuds['BFS'])], ratio_man,
                    'b-o', label='BFS / A* Manhattan', linewidth=2.5, markersize=8)
            ax3.plot(tailles[:len(donnees_noeuds['BFS'])], ratio_euc,
                    'g-^', label='BFS / A* Euclidienne', linewidth=2.5, markersize=8)
        
        ax3.set_xlabel('Taille de la grille', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Ratio', fontsize=11, fontweight='bold')
        ax3.set_title('Gain d\'efficacité A*', fontsize=12, fontweight='bold', pad=10)
        ax3.legend(fontsize=9, loc='upper left')
        ax3.grid(True, alpha=0.3, linestyle='--')
        ax3.tick_params(labelsize=9)
        ax3.axhline(y=1, color='red', linestyle='--', alpha=0.5, linewidth=1)
        
        # Graphique 4: Comparaison heuristiques
        if len(donnees_noeuds['A* Manhattan']) == len(donnees_noeuds['A* Euclidienne']):
            ratio_heur = np.array(donnees_noeuds['A* Euclidienne']) / np.array(donnees_noeuds['A* Manhattan'])
            ax4.plot(tailles[:len(donnees_noeuds['A* Manhattan'])], ratio_heur,
                    color='purple', marker='D', linewidth=2.5, markersize=8, 
                    label='Euclidienne / Manhattan')
            ax4.axhline(y=1, color='red', linestyle='--', alpha=0.7, linewidth=2, 
                       label='Égalité')
        
        ax4.set_xlabel('Taille de la grille', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Ratio Euc / Man', fontsize=11, fontweight='bold')
        ax4.set_title('Comparaison Heuristiques', fontsize=12, fontweight='bold', pad=10)
        ax4.legend(fontsize=9, loc='upper left')
        ax4.grid(True, alpha=0.3, linestyle='--')
        ax4.tick_params(labelsize=9)
        
        # Titre général
        fig.suptitle('ANALYSE DE SCALABILITÉ ', 
                    fontsize=14, fontweight='bold', y=0.98)
        
        plt.show()
        
        # Sauvegarder également
        fig.savefig('analyse_scalabilite.png', dpi=300, bbox_inches='tight')
        print("✓ Graphiques sauvegardés dans 'analyse_scalabilite.png'")
    
    def analyser_tendance_complexite(self, donnees_noeuds, tailles):
        """Analyse la tendance de complexité théorique"""
        print("\n" + "=" * 80)
        print("ANALYSE DE COMPLEXITÉ THÉORIQUE")
        print("=" * 80)
        
        # Approximation de la complexité
        for algo, noeuds in donnees_noeuds.items():
            if len(noeuds) == len(tailles):
                print(f"\n{algo}:")
                for i in range(1, len(tailles)):
                    if noeuds[i] > 0 and noeuds[i-1] > 0:
                        ratio = noeuds[i] / noeuds[i-1]
                        ratio_taille = tailles[i] / tailles[i-1]
                        print(f"  {tailles[i-1]:>2}→{tailles[i]:>2}: {ratio:.2f}x plus de nœuds "
                              f"(taille {ratio_taille:.2f}x)")
                
                # Estimation de l'exposant de complexité
                if len(tailles) >= 2:
                    exposant_approx = np.log(noeuds[-1] / noeuds[0]) / np.log(tailles[-1] / tailles[0])
                    print(f"  ➜ Exposant de complexité approximatif: O(n^{exposant_approx:.2f})")
                    
                    if exposant_approx < 1.5:
                        print(f"     Complexité quasi-linéaire")
                    elif exposant_approx < 2.5:
                        print(f"     Complexité quadratique")
                    else:
                        print(f"     Complexité > quadratique")

# MAIN SPÉCIFIQUE POUR PARTIE 5
if __name__ == "__main__":

    print(" ANALYSE DE SCALABILITÉ ")
   
    print("Évolution des performances avec la taille des grilles")
    
    
    analyseur_scala = AnalyseurScalabilite()
    
    # Tailles impaires pour Prim (doit être ≥ 3)
    tailles = [15, 25, 35, 45]
    
    print(f"📏 Tailles analysées: {tailles}")
    print(f" Nombre de tests par taille: 3")
    print(f"\n L'analyse peut prendre quelques minutes...\n")
    
    # Exécuter l'analyse de scalabilité
    donnees_temps, donnees_noeuds = analyseur_scala.analyser_scalabilite(
        tailles, nb_tests_par_taille=3)
    
    # Analyser les tendances de complexité
    analyseur_scala.analyser_tendance_complexite(donnees_noeuds, tailles)
