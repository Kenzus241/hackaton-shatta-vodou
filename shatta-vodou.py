import random

def creer_paquet():
    '''
    crée le jeu de carte
    '''
    valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi', 'As']
    couleurs = ['Cœur', 'Carreau', 'Trèfle', 'Pique']
    return [f"{v} de {c}" for v in valeurs for c in couleurs]

def jouer_shatta_vodou():
    '''
    fonction principal du jeu
    '''
    print("🃏 === BIENVENUE DANS LE SHATTA VODOU === 🃏\n")
    
    # Initialisation
    paquet = creer_paquet()
    random.shuffle(paquet)
    
    # --- PHASE 1 : Choix de la carte ---
    print("Le maître du jeu fait défiler les cartes...")
    input("👉 Appuie sur 'Entrée' pour dire STOP et choisir ta carte !")
    
    # Tirage aléatoire simulant le moment où le joueur dit stop
    carte_cible = random.choice(paquet)
    print(f"\nTu as dit STOP sur : ** {carte_cible} **")
    print("Cette carte devient la tienne. Elle est remise dans le paquet et le jeu est mélangé.\n")
    
    # --- PHASE 2 : Retrouver la carte ---
    echecs_consecutifs = 0
    
    while True:
        print("-" * 40)
        print(f"[Taille actuelle du paquet : {len(paquet)} cartes]")
        input("👉 Le paquet défile... Appuie sur 'Entrée' pour dire STOP !")
        
        carte_tiree = random.choice(paquet)
        
        # Condition de victoire
        if carte_tiree == carte_cible:
            print(f"\n🎉 {carte_tiree} est ton shatta vodou ! 🎉")
            print("Bien joué, la partie est terminée.")
            break
            
        # Mauvaise carte
        else:
            echecs_consecutifs += 1
            
            # Si 2 échecs d'affilée
            if echecs_consecutifs == 2:
                print(f"\n❌ {carte_tiree} n'est pas ton shatta vodou...")
                print("⚠️  Paire de deux, on divise par deux !")
                
                # On divise le paquet par deux
                # Étape 1 : On met la carte cible en sécurité pour ne pas la perdre
                paquet.remove(carte_cible)
                
                # Étape 2 : On réduit la taille du paquet de moitié
                moitie = len(paquet) // 2
                paquet = random.sample(paquet, moitie)
                
                # Étape 3 : On remet la carte cible et on mélange
                paquet.append(carte_cible)
                random.shuffle(paquet)
                
                # On réinitialise le compteur d'échecs après la division
                echecs_consecutifs = 0
                
            # Si 1 seul échec
            else:
                print(f"\n❌ {carte_tiree} n'est pas ton shatta vodou.")

# Lancement du jeu
if __name__ == "__main__":
    jouer_shatta_vodou()