import tkinter as tk
from tkinter import messagebox
import random
import pygame  # Nécessaire pour le son

class ShattaVodouApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🃏 Shatta Vodou : Le Dé du Destin")
        self.root.geometry("500x780")
        self.root.configure(bg="#1a1a1a")

        # --- Initialisation du Son ---
        pygame.mixer.init()
        # Note : Prépare des petits fichiers .wav ou .mp3 pour ces noms :
        try:
            self.son_roulette = pygame.mixer.Sound("roulette.mp3")
            self.son_victoire = pygame.mixer.Sound("win.mp3")
            self.son_erreur = pygame.mixer.Sound("Fail.mp3")
            self.son_division = pygame.mixer.Sound("Slice.mp3")
        except:
            print("Fichiers audio non trouvés, le jeu tournera en mode muet.")
            self.son_roulette = self.son_victoire = self.son_erreur = self.son_division = None

        # --- Variables de Jeu ---
        self.valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'V', 'D', 'R', 'As']
        self.couleurs = ['♥', '♦', '♣', '♠']
        self.paquet = [f"{v}{c}" for v in self.valeurs for c in self.couleurs]
        
        self.carte_cible = None
        self.dernier_de = 0
        self.echecs_consecutifs = 0
        self.en_defilement = False
        self.phase_choix = True 
        self.points = 0
        self.nb_divisions = 0
        self.symboles_casino = ["🍒", "🔔", "🍋", "🍉", "⭐"]

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="SHATTA VODOU", font=("Courier", 28, "bold"), bg="#1a1a1a", fg="#d4af37").pack(pady=10)

        self.label_points = tk.Label(self.root, text=f"Points : {self.points}", font=("Helvetica", 14, "bold"), bg="#1a1a1a", fg="#e74c3c")
        self.label_points.pack()

        self.label_de_container = tk.Label(self.root, text="DÉ À 52 FACES", font=("Helvetica", 10), bg="#1a1a1a", fg="#888")
        self.label_de_container.pack()
        
        self.label_de_valeur = tk.Label(self.root, text="--", font=("Helvetica", 30, "bold"), bg="#1a1a1a", fg="#e74c3c")
        self.label_de_valeur.pack(pady=5)

        self.card_frame = tk.Frame(self.root, width=180, height=250, bg="#fff", highlightbackground="#d4af37", highlightthickness=3)
        self.card_frame.pack_propagate(False)
        self.card_frame.pack(pady=10)

        self.label_carte = tk.Label(self.card_frame, text="?", font=("Helvetica", 50), bg="#fff")
        self.label_carte.place(relx=0.5, rely=0.5, anchor="center")

        self.label_status = tk.Label(self.root, text="Lance le dé pour choisir ta carte", font=("Helvetica", 12), bg="#1a1a1a", fg="#eee")
        self.label_status.pack(pady=5)

        self.label_stats = tk.Label(self.root, text=f"Cartes restantes : {len(self.paquet)}", font=("Helvetica", 10), bg="#1a1a1a", fg="#666")
        self.label_stats.pack()

        self.btn_action = tk.Button(self.root, text="LANCER LE DÉ", font=("Helvetica", 14, "bold"), bg="#d4af37", fg="black", width=15, height=2, command=self.toggle_defilement)
        self.btn_action.pack(pady=15)

        self.casino_frame = tk.Frame(self.root, bg="#000", highlightbackground="#d4af37", highlightthickness=1)
        self.casino_frame.pack(side="bottom", pady=20, fill="x", padx=60)
        self.label_roulette = tk.Label(self.casino_frame, text="[ 🎰 | 🎰 | 🎰 ]", font=("Segoe UI Symbol", 22), bg="#000", fg="#d4af37")
        self.label_roulette.pack(pady=10)

    def play_sound(self, sound):
        if sound:
            sound.play()

    def toggle_defilement(self):
        if not self.en_defilement:
            if not self.phase_choix and len(self.paquet) == 1 and self.label_carte.cget("text") != self.carte_cible:
                messagebox.showerror("PERDU", "Dernière carte... ce n'est pas le shatta voudou, tu as perdu !")
                self.reset_jeu()
                return
            self.en_defilement = True
            self.btn_action.config(text="STOP", bg="#e74c3c", fg="white")
            self.animer()
        else:
            self.en_defilement = False
            self.btn_action.config(text="START" if not self.phase_choix else "LANCER LE DÉ", bg="#d4af37", fg="black")
            self.logique_jeu()

    def animer(self):
        if self.en_defilement:
            self.play_sound(self.son_roulette) # Son à chaque changement
            self.dernier_de = random.randint(1, len(self.paquet))
            carte_actuelle = self.paquet[self.dernier_de - 1]
            self.label_de_valeur.config(text=f"🎲 {self.dernier_de}")
            couleur_symbole = "#e74c3c" if any(x in carte_actuelle for x in ['♥', '♦']) else "#1a1a1a"
            self.label_carte.config(text=carte_actuelle, fg=couleur_symbole)
            
            s = random.choices(self.symboles_casino + ["💎"], k=3)
            self.label_roulette.config(text=f"[ {s[0]} | {s[1]} | {s[2]} ]")
            self.root.after(60, self.animer)

    def logique_jeu(self):
        carte_tiree = self.label_carte.cget("text")
        if self.phase_choix:
            self.carte_cible = carte_tiree
            messagebox.showinfo("Le Sort est jeté", f"Le dé 52 est tombé sur {self.dernier_de} !\n\nTa carte est : {self.carte_cible}")
            self.phase_choix = False
            self.label_status.config(text="Retrouve ton Shatta Vodou !")
            self.label_de_container.config(text="VALEUR DU DERNIER TIRAGE")
            random.shuffle(self.paquet)
        else:
            if carte_tiree == self.carte_cible:
                self.play_sound(self.son_victoire) # JACKPOT
                self.label_roulette.config(text="[ 💎 | 💎 | 💎 ]")
                self.root.update()
                messagebox.showinfo("SHATTA VODOU", f"✨ {carte_tiree} ✨\nTu as gagné !\nScore final : {self.points}")
                self.reset_jeu()
            else:
                self.play_sound(self.son_erreur) # FAIL
                s = random.choices(self.symboles_casino, k=3)
                self.label_roulette.config(text=f"[ {s[0]} | {s[1]} | {s[2]} ]")
                self.points += (2 if self.nb_divisions >= 2 else 1)
                self.label_points.config(text=f"Points : {self.points}")
                self.echecs_consecutifs += 1
                if self.echecs_consecutifs == 2:
                    self.diviser_paquet(carte_tiree)
                    self.echecs_consecutifs = 0
                else:
                    self.label_status.config(text=f"Non... le {self.carte_cible} se cache encore.")
        self.label_stats.config(text=f"Cartes restantes : {len(self.paquet)}")

    def diviser_paquet(self, carte_perdue):
        self.play_sound(self.son_division) # DIVISION
        self.nb_divisions += 1
        messagebox.showwarning("Paire de deux", f"{carte_perdue} n'est pas ton Shatta...\nOn divise par deux !")
        if self.carte_cible in self.paquet: self.paquet.remove(self.carte_cible)
        self.paquet = random.sample(self.paquet, len(self.paquet) // 2)
        self.paquet.append(self.carte_cible)
        random.shuffle(self.paquet)
        self.label_status.config(text="Le paquet a rétréci...")

    def reset_jeu(self):
        self.paquet = [f"{v}{c}" for v in self.valeurs for c in self.couleurs]
        self.carte_cible, self.phase_choix, self.echecs_consecutifs, self.points, self.nb_divisions = None, True, 0, 0, 0
        self.label_points.config(text="Points : 0")
        self.label_carte.config(text="?", fg="#1a1a1a")
        self.label_de_valeur.config(text="--")
        self.label_roulette.config(text="[ 🎰 | 🎰 | 🎰 ]")
        self.btn_action.config(text="LANCER LE DÉ", bg="#d4af37", fg="black")
        self.label_status.config(text="Relance le dé pour une nouvelle partie")
        self.label_stats.config(text=f"Cartes restantes : {len(self.paquet)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShattaVodouApp(root)
    root.mainloop()