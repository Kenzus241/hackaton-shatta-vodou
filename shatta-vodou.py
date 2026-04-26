import tkinter as tk
from tkinter import messagebox
import random

class ShattaVodouApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🃏 Shatta Vodou : Le Dé du Destin")
        self.root.geometry("500x650")
        self.root.configure(bg="#1a1a1a")

        # --- Variables de Jeu ---
        self.valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'V', 'D', 'R', 'As']
        self.couleurs = ['♥', '♦', '♣', '♠']
        # Création du paquet indexé (1 à 52)
        self.paquet = [f"{v}{c}" for v in self.valeurs for c in self.couleurs]
        
        self.carte_cible = None
        self.dernier_de = 0
        self.echecs_consecutifs = 0
        self.en_defilement = False
        self.phase_choix = True 

        self.setup_ui()

    def setup_ui(self):
        # Titre
        tk.Label(self.root, text="SHATTA VODOU", font=("Courier", 28, "bold"), 
                 bg="#1a1a1a", fg="#d4af37").pack(pady=10)

        # Affichage du Dé
        self.label_de_container = tk.Label(self.root, text="DÉ À 52 FACES", font=("Helvetica", 10), bg="#1a1a1a", fg="#888")
        self.label_de_container.pack()
        
        self.label_de_valeur = tk.Label(self.root, text="--", font=("Helvetica", 30, "bold"), 
                                        bg="#1a1a1a", fg="#e74c3c")
        self.label_de_valeur.pack(pady=5)

        # Zone de la Carte
        self.card_frame = tk.Frame(self.root, width=180, height=250, bg="#fff", 
                                   highlightbackground="#d4af37", highlightthickness=3)
        self.card_frame.pack_propagate(False)
        self.card_frame.pack(pady=20)

        self.label_carte = tk.Label(self.card_frame, text="?", font=("Helvetica", 50), bg="#fff")
        self.label_carte.place(relx=0.5, rely=0.5, anchor="center")

        # Status
        self.label_status = tk.Label(self.root, text="Lance le dé pour choisir ta carte", 
                                     font=("Helvetica", 12), bg="#1a1a1a", fg="#eee")
        self.label_status.pack(pady=10)

        self.label_stats = tk.Label(self.root, text=f"Cartes restantes : {len(self.paquet)}", 
                                     font=("Helvetica", 10), bg="#1a1a1a", fg="#666")
        self.label_stats.pack()

        # Bouton Action
        self.btn_action = tk.Button(self.root, text="LANCER LE DÉ", font=("Helvetica", 14, "bold"), 
                                    bg="#d4af37", fg="black", width=15, height=2, command=self.toggle_defilement)
        self.btn_action.pack(pady=20)

    def toggle_defilement(self):
        if not self.en_defilement:
            self.en_defilement = True
            self.btn_action.config(text="STOP", bg="#e74c3c", fg="white")
            self.animer()
        else:
            self.en_defilement = False
            self.btn_action.config(text="START" if not self.phase_choix else "LANCER LE DÉ", bg="#d4af37", fg="black")
            self.logique_jeu()

    def animer(self):
        """Anime le dé et les cartes en même temps."""
        if self.en_defilement:
            # On tire un index au hasard (le dé)
            self.dernier_de = random.randint(1, len(self.paquet))
            carte_actuelle = self.paquet[self.dernier_de - 1]

            # Mise à jour UI
            self.label_de_valeur.config(text=f"🎲 {self.dernier_de}")
            couleur_symbole = "#e74c3c" if any(x in carte_actuelle for x in ['♥', '♦']) else "#1a1a1a"
            self.label_carte.config(text=carte_actuelle, fg=couleur_symbole)
            
            self.root.after(60, self.animer)

    def logique_jeu(self):
        carte_tiree = self.label_carte.cget("text")

        if self.phase_choix:
            # Fin de phase 1 : Le dé a parlé
            self.carte_cible = carte_tiree
            messagebox.showinfo("Le Sort est jeté", f"Le dé 52 est tombé sur {self.dernier_de} !\n\nTa carte est : {self.carte_cible}")
            self.phase_choix = False
            self.label_status.config(text="Retrouve ton Shatta Vodou !")
            self.label_de_container.config(text="VALEUR DU DERNIER TIRAGE")
            random.shuffle(self.paquet)
        else:
            # Phase 2 : Recherche
            if carte_tiree == self.carte_cible:
                messagebox.showinfo("SHATTA VODOU", f"✨ {carte_tiree} ✨\nC'est ton Shatta Vodou ! Tu as gagné.")
                self.reset_jeu()
            else:
                self.echecs_consecutifs += 1
                if self.echecs_consecutifs == 2:
                    self.diviser_paquet(carte_tiree)
                    self.echecs_consecutifs = 0
                else:
                    self.label_status.config(text=f"Non... le {self.carte_cible} se cache encore.")

        self.label_stats.config(text=f"Cartes restantes : {len(self.paquet)}")

    def diviser_paquet(self, carte_perdue):
        """Applique la règle : Paire de deux, on divise par deux."""
        messagebox.showwarning("Paire de deux", f"{carte_perdue} n'est pas ton Shatta...\nPaire de deux, on divise par deux !")
        
        if self.carte_cible in self.paquet:
            self.paquet.remove(self.carte_cible)
        
        taille_reduite = len(self.paquet) // 2
        self.paquet = random.sample(self.paquet, taille_reduite)
        self.paquet.append(self.carte_cible)
        random.shuffle(self.paquet)
        self.label_status.config(text="Le paquet a rétréci... la chance augmente.")

    def reset_jeu(self):
        self.paquet = [f"{v}{c}" for v in self.valeurs for c in self.couleurs]
        self.carte_cible = None
        self.phase_choix = True
        self.echecs_consecutifs = 0
        self.label_carte.config(text="?", fg="#1a1a1a")
        self.label_de_valeur.config(text="--")
        self.btn_action.config(text="LANCER LE DÉ")
        self.label_status.config(text="Relance le dé pour une nouvelle partie")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShattaVodouApp(root)
    root.mainloop()