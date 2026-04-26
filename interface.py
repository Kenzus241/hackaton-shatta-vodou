import tkinter as tk
from tkinter import messagebox
import random

class ShattaVodouApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🃏 Shatta Vodou : Le Dé du Destin")
        self.root.geometry("1800x950") # Fenêtre légèrement agrandie
        self.root.configure(bg="#2F2E22") # Fond noir profond mystique

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
        # Titre principal "Dark Mystique"
        tk.Label(self.root, text="SHATTA VODOU", font=("Courier", 32, "bold"), 
                 bg="#0B0C10", fg="#D4AF37").pack(pady=(20, 5))
        tk.Label(self.root, text="ÉDITION LE DÉ DU DESTIN", font=("Helvetica", 10, "italic"), 
                 bg="#0B0C10", fg="#66FCF1").pack(pady=(0, 20))

        # Zone du Dé
        self.frame_de = tk.Frame(self.root, bg="#1F2833", bd=2, relief="ridge")
        self.frame_de.pack(pady=10, padx=50, fill="x")

        self.label_de_container = tk.Label(self.frame_de, text="JEU DE CARTE", font=("Helvetica", 10, "bold"), 
                                           bg="#1F2833", fg="#C5C6C7")
        self.label_de_container.pack(pady=(10, 0))
        
        self.label_de_valeur = tk.Label(self.frame_de, text="--", font=("Helvetica", 36, "bold"), 
                                        bg="#1F2833", fg="#45A29E")
        self.label_de_valeur.pack(pady=(0, 10))

        # Zone de la Carte (Effet Casino)
        self.card_frame = tk.Frame(self.root, width=200, height=280, bg="#FFFFFF", 
                                   highlightbackground="#D4AF37", highlightthickness=4)
        self.card_frame.pack_propagate(False)
        self.card_frame.pack(pady=20)

        # Ajout d'un motif subtil au dos/fond de la carte
        self.label_carte = tk.Label(self.card_frame, text="?", font=("Helvetica", 65, "bold"), bg="#FFFFFF")
        self.label_carte.place(relx=0.5, rely=0.5, anchor="center")

        # Zone de Statut
        self.label_status = tk.Label(self.root, text="C'est le moment de choisir ton SHATTA VODOU.", 
                                     font=("Helvetica", 14), bg="#0B0C10", fg="#FFFFFF")
        self.label_status.pack(pady=10)

        self.label_stats = tk.Label(self.root, text=f"Cartes dans le paquet : {len(self.paquet)} / 52", 
                                     font=("Helvetica", 11), bg="#0B0C10", fg="#C5C6C7")
        self.label_stats.pack()

        # Bouton Action stylisé
        self.btn_action = tk.Button(self.root, text="PIOCHE UNE CARTE", font=("Helvetica", 16, "bold"), 
                                    bg="#D4AF37", fg="#0B0C10", activebackground="#F3E5AB", 
                                    activeforeground="#000000", width=18, height=2, 
                                    cursor="hand2", relief="raised", borderwidth=3, 
                                    command=self.toggle_defilement)
        self.btn_action.pack(pady=30)

    def toggle_defilement(self):
        if not self.en_defilement:
            self.en_defilement = True
            self.btn_action.config(text="PIOCHE", bg="#E74C3C", fg="white", activebackground="#C0392B")
            self.animer()
        else:
            self.en_defilement = False
            self.btn_action.config(text="START" if not self.phase_choix else "MELANGER LE PACKET", 
                                   bg="#D4AF37", fg="#0B0C10", activebackground="#F3E5AB")
            self.logique_jeu()

    def animer(self):
        """Anime le dé et les cartes en même temps."""
        if self.en_defilement:
            # On tire un index au hasard (le dé)
            self.dernier_de = random.randint(1, len(self.paquet))
            carte_actuelle = self.paquet[self.dernier_de - 1]

            # Mise à jour UI avec couleurs adaptées
            self.label_de_valeur.config(text=f"🎲 {self.dernier_de}")
            couleur_symbole = "#E74C3C" if any(x in carte_actuelle for x in ['♥', '♦']) else "#0B0C10"
            self.label_carte.config(text=carte_actuelle, fg=couleur_symbole)
            
            self.root.after(50, self.animer) # Légèrement accéléré pour la fluidité (50ms)

    def logique_jeu(self):
        carte_tiree = self.label_carte.cget("text")

        if self.phase_choix:
            # Fin de phase 1 : Le dé a parlé
            self.carte_cible = carte_tiree
            messagebox.showinfo("🔮 Le Sort est jeté", f"Ta carte à été piocher,ton shatta vodou est \n : {self.carte_cible}")
            self.phase_choix = False
            self.label_status.config(text="Le paquet défile... Traque ton Shatta Vodou !", fg="#66FCF1")
            self.label_de_container.config(text="DERNIER TIRAGE")
            random.shuffle(self.paquet)
        else:
            # Phase 2 : Recherche
            if carte_tiree == self.carte_cible:
                messagebox.showinfo("👑 SHATTA VODOU", f"✨ {carte_tiree} ✨\nLe sort est brisé ! Tu as trouvé ton SHATTA VODOU.")
                self.reset_jeu()
            else:
                self.echecs_consecutifs += 1
                if self.echecs_consecutifs == 2:
                    self.diviser_paquet(carte_tiree)
                    self.echecs_consecutifs = 0
                else:
                    self.label_status.config(text=f"Échec... le {self.carte_cible} t'échappe encore.", fg="#E74C3C")

        self.label_stats.config(text=f"Cartes dans le paquet : {len(self.paquet)}")

    def diviser_paquet(self, carte_perdue):
        """Applique la règle : Paire de deux, on divise par deux."""
        messagebox.showwarning("⚠️ Malédiction : Paire de deux", f"{carte_perdue} n'est pas ta cible.\nPaire de deux : Trouvera tu ton shatta vodou !")
        
        if self.carte_cible in self.paquet:
            self.paquet.remove(self.carte_cible)
        
        taille_reduite = len(self.paquet) // 2
        self.paquet = random.sample(self.paquet, taille_reduite)
        self.paquet.append(self.carte_cible)
        random.shuffle(self.paquet)
        self.label_status.config(text="Le paquet s'est réduit... tes chances augmentent.", fg="#D4AF37")

    def reset_jeu(self):
        self.paquet = [f"{v}{c}" for v in self.valeurs for c in self.couleurs]
        self.carte_cible = None
        self.phase_choix = True
        self.echecs_consecutifs = 0
        self.label_carte.config(text="?", fg="#0B0C10")
        self.label_de_valeur.config(text="--", fg="#45A29E")
        self.btn_action.config(text="LANCER LE DÉ")
        self.label_status.config(text="C'est le moment de choisir ton SHATTA VODOU.", fg="#FFFFFF")
        self.label_de_container.config(text="Jeu de cartes")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShattaVodouApp(root)
    root.mainloop()