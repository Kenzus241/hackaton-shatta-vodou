import tkinter as tk
from tkinter import messagebox
import random

class ShattaVodouApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🃏 Shatta Vodou")
        self.root.geometry("500x600")
        self.root.configure(bg="#2c3e50")

        # --- Variables de Jeu ---
        self.valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'V', 'D', 'R', 'As']
        self.couleurs = ['♥', '♦', '♣', '♠']
        self.paquet = [f"{v}{c}" for v in self.valeurs for c in self.couleurs]
        
        self.carte_cible = None
        self.echecs_consecutifs = 0
        self.en_defilement = False
        self.phase_choix = True

        self.setup_ui()

    def setup_ui(self):
        """Initialisation de l'interface graphique."""
        # Titre
        self.label_titre = tk.Label(self.root, text="SHATTA VODOU", font=("Helvetica", 24, "bold"), 
                                    bg="#2c3e50", fg="#ecf0f1", pady=20)
        self.label_titre.pack()

        # Zone d'affichage de la carte
        self.card_frame = tk.Frame(self.root, width=200, height=280, bg="#ecf0f1", 
                                   highlightbackground="#e74c3c", highlightthickness=4)
        self.card_frame.pack_propagate(False)
        self.card_frame.pack(pady=30)

        self.label_carte = tk.Label(self.card_frame, text="?", font=("Helvetica", 60), 
                                    bg="#ecf0f1", fg="#2c3e50")
        self.label_carte.place(relx=0.5, rely=0.5, anchor="center")

        # Infos et Status
        self.label_status = tk.Label(self.root, text="Appuie sur START pour faire défiler", 
                                     font=("Helvetica", 12), bg="#2c3e50", fg="#bdc3c7")
        self.label_status.pack(pady=10)

        self.label_stats = tk.Label(self.root, text=f"Cartes dans le paquet : {len(self.paquet)}", 
                                     font=("Helvetica", 10, "italic"), bg="#2c3e50", fg="#95a5a6")
        self.label_stats.pack()

        # Boutons
        self.btn_action = tk.Button(self.root, text="START", font=("Helvetica", 14, "bold"), 
                                    bg="#27ae60", fg="white", width=15, height=2, command=self.toggle_defilement)
        self.btn_action.pack(pady=20)

    def toggle_defilement(self):
        """Gère l'alternance entre le défilement et l'arrêt."""
        if not self.en_defilement:
            self.en_defilement = True
            self.btn_action.config(text="STOP", bg="#e74c3c")
            self.label_status.config(text="Défilement en cours...")
            self.animer_defilement()
        else:
            self.en_defilement = False
            self.btn_action.config(text="START", bg="#27ae60")
            self.verifier_carte()

    def animer_defilement(self):
        """Simule visuellement le mélange des cartes."""
        if self.en_defilement:
            carte_hasard = random.choice(self.paquet)
            couleur_texte = "#e74c3c" if any(x in carte_hasard for x in ['♥', '♦']) else "#2c3e50"
            self.label_carte.config(text=carte_hasard, fg=couleur_texte)
            self.root.after(50, self.animer_defilement)

    def verifier_carte(self):
        """Logique principale du jeu lors de l'appui sur STOP."""
        carte_tirée = self.label_carte.cget("text")

        # --- PHASE 1 : Choix de la carte ---
        if self.phase_choix:
            self.carte_cible = carte_tirée
            messagebox.showinfo("Ta Carte", f"Ta carte est le {self.carte_cible} !\nRetrouve-la maintenant.")
            self.phase_choix = False
            self.label_status.config(text="Retrouve ton Shatta Vodou !")
            # On mélange bien
            random.shuffle(self.paquet)

        # --- PHASE 2 : Recherche ---
        else:
            if carte_tirée == self.carte_cible:
                messagebox.showinfo("VICTOIRE", f"🎉 {carte_tirée} est ton shatta vodou !")
                self.reset_jeu()
            else:
                self.echecs_consecutifs += 1
                if self.echecs_consecutifs == 2:
                    messagebox.showwarning("Paire de deux", f"{carte_tirée} n'est pas ton shatta vodou.\nPaire de deux, on divise par deux !")
                    self.diviser_paquet()
                    self.echecs_consecutifs = 0
                else:
                    self.label_status.config(text=f"Raté ! Ce n'est pas le {self.carte_cible}...")

        self.label_stats.config(text=f"Cartes dans le paquet : {len(self.paquet)}")

    def diviser_paquet(self):
        """Réduit le paquet de moitié en gardant la cible."""
        if self.carte_cible in self.paquet:
            self.paquet.remove(self.carte_cible)
        
        nouveau_taille = len(self.paquet) // 2
        self.paquet = random.sample(self.paquet, nouveau_taille)
        self.paquet.append(self.carte_cible)
        random.shuffle(self.paquet)

    def reset_jeu(self):
        """Remet le jeu à zéro."""
        self.paquet = [f"{v}{c}" for v in self.valeurs for c in self.couleurs]
        self.carte_cible = None
        self.echecs_consecutifs = 0
        self.phase_choix = True
        self.label_carte.config(text="?", fg="#2c3e50")
        self.label_status.config(text="Appuie sur START pour choisir une carte")
        self.label_stats.config(text=f"Cartes dans le paquet : {len(self.paquet)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShattaVodouApp(root)
    root.mainloop()
