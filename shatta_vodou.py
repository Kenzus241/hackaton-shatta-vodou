import tkinter as tk
from tkinter import messagebox
import random
import pygame
import os

# --- GESTIONNAIRE DE FENÊTRES PRINCIPAL ---
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🃏 Shatta Vodou : Ultimate Edition")
        self.geometry("600x850")
        self.configure(bg="#0B0C10")
        
        # Initialisation Audio
        pygame.mixer.init()
        self.charger_sons()

        # Variables globales
        self.son_active = tk.BooleanVar(value=True)
        self.animations_rapides = tk.BooleanVar(value=False)

        container = tk.Frame(self, bg="#0B0C10")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MenuPrincipal, Parametres, JeuShatta, EcranFin):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuPrincipal")

    def charger_sons(self):
        try:
            self.sons = {
                "roulette": pygame.mixer.Sound("roulette.mp3"),
                "victoire": pygame.mixer.Sound("win.mp3"),
                "erreur": pygame.mixer.Sound("Fail.mp3"),
                "division": pygame.mixer.Sound("Slice.mp3")
            }
            if os.path.exists("background.mp3"):
                pygame.mixer.music.load("background.mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
        except:
            self.sons = None

    def play_fx(self, key):
        if self.son_active.get() and self.sons and key in self.sons:
            self.sons[key].play()

    def show_frame(self, page_name, **kwargs):
        frame = self.frames[page_name]
        if hasattr(frame, 'on_show'):
            frame.on_show(**kwargs)
        frame.tkraise()

# --- ÉCRAN 1 : MENU PRINCIPAL ---
class MenuPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0B0C10")
        tk.Label(self, text="SHATTA VODOU", font=("Courier", 40, "bold"), bg="#0B0C10", fg="#D4AF37").pack(pady=(100, 10))
        tk.Label(self, text="L'ULTIME RITUEL", font=("Helvetica", 14, "italic"), bg="#0B0C10", fg="#66FCF1").pack(pady=(0, 60))

        buttons = [
            ("LANCER LE RITUEL", "#D4AF37", "#0B0C10", lambda: controller.show_frame("JeuShatta")),
            ("PARAMÈTRES", "#1F2833", "#C5C6C7", lambda: controller.show_frame("Parametres")),
            ("QUITTER", "#E74C3C", "white", controller.quit)
        ]

        for text, bg, fg, cmd in buttons:
            tk.Button(self, text=text, font=("Helvetica", 14, "bold"), bg=bg, fg=fg, width=20, height=2, cursor="hand2", command=cmd).pack(pady=10)

# --- ÉCRAN 2 : PARAMÈTRES ---
class Parametres(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0B0C10")
        tk.Label(self, text="⚙️ CONFIGURATION", font=("Courier", 25, "bold"), bg="#0B0C10", fg="#D4AF37").pack(pady=50)
        
        opts = [("Activer les sons", controller.son_active), ("Animations Turbo", controller.animations_rapides)]
        for text, var in opts:
            tk.Checkbutton(self, text=text, variable=var, font=("Helvetica", 14), bg="#0B0C10", fg="#C5C6C7", selectcolor="#1F2833", activebackground="#0B0C10").pack(pady=10)

        tk.Button(self, text="RETOUR", font=("Helvetica", 12, "bold"), bg="#1F2833", fg="#C5C6C7", command=lambda: controller.show_frame("MenuPrincipal")).pack(pady=50)

# --- ÉCRAN 3 : LE JEU (FUSIONNÉ) ---
class JeuShatta(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1A1A1A")
        self.controller = controller
        self.particules = []
        self.symboles = ["🍒", "🔔", "🍋", "🍉", "⭐"]
        self.setup_ui()
        self.update_particules()

    def setup_ui(self):
        # Header Stats
        stats_frame = tk.Frame(self, bg="#1A1A1A")
        stats_frame.pack(fill="x", pady=10)
        self.label_points = tk.Label(stats_frame, text="Points : 0", font=("Helvetica", 14, "bold"), bg="#1A1A1A", fg="#E74C3C")
        self.label_points.pack(side="left", padx=20)
        self.label_paquet = tk.Label(stats_frame, text="Cartes : 52", font=("Helvetica", 12), bg="#1A1A1A", fg="#66FCF1")
        self.label_paquet.pack(side="right", padx=20)

        # Zone Dé
        self.label_de_valeur = tk.Label(self, text="🎲 --", font=("Helvetica", 30, "bold"), bg="#1A1A1A", fg="#D4AF37")
        self.label_de_valeur.pack()

        # Canvas Carte (pour particules)
        self.canvas = tk.Canvas(self, width=200, height=280, bg="#FFFFFF", highlightthickness=3, highlightbackground="#D4AF37")
        self.canvas.pack(pady=20)
        self.card_text = self.canvas.create_text(100, 140, text="?", font=("Helvetica", 60, "bold"), fill="#1A1A1A")

        # Status & Bouton
        self.label_status = tk.Label(self, text="Invoquez votre Shatta Vodou...", font=("Helvetica", 12), bg="#1A1A1A", fg="#C5C6C7")
        self.label_status.pack(pady=10)

        self.btn_action = tk.Button(self, text="LANCER LE DÉ", font=("Helvetica", 16, "bold"), bg="#D4AF37", width=15, height=2, command=self.toggle_defilement)
        self.btn_action.pack(pady=10)

        # Casino Display
        self.label_roulette = tk.Label(self, text="[ 🎰 | 🎰 | 🎰 ]", font=("Segoe UI Symbol", 20), bg="#000", fg="#D4AF37")
        self.label_roulette.pack(pady=20, fill="x")

    def on_show(self):
        self.reset_jeu()

    def reset_jeu(self):
        self.paquet = [f"{v}{c}" for v in ['2','3','4','5','6','7','8','9','10','V','D','R','As'] for c in ['♥','♦','♣','♠']]
        self.carte_cible, self.phase_choix, self.echecs, self.points, self.en_defilement = None, True, 0, 0, False
        self.update_ui_state()

    def update_ui_state(self):
        self.label_points.config(text=f"Points : {self.points}")
        self.label_paquet.config(text=f"Cartes : {len(self.paquet)}")
        self.canvas.itemconfig(self.card_text, text="?")
        self.btn_action.config(text="LANCER LE DÉ", bg="#D4AF37")

    def toggle_defilement(self):
        if not self.en_defilement:
            if not self.phase_choix and len(self.paquet) == 1:
                self.verifier_victoire(self.canvas.itemcget(self.card_text, "text"))
                return
            self.en_defilement = True
            self.btn_action.config(text="STOP", bg="#E74C3C", fg="white")
            self.animer()
        else:
            self.en_defilement = False
            self.btn_action.config(text="START" if not self.phase_choix else "SUIVANT", bg="#D4AF37", fg="black")
            self.logique_jeu()

    def animer(self):
        if self.en_defilement:
            self.controller.play_fx("roulette")
            idx = random.randint(1, len(self.paquet))
            carte = self.paquet[idx-1]
            color = "#E74C3C" if any(x in carte for x in ['♥', '♦']) else "#1A1A1A"
            self.canvas.itemconfig(self.card_text, text=carte, fill=color)
            self.label_de_valeur.config(text=f"🎲 {idx}")
            
            s = random.choices(self.symboles, k=3)
            self.label_roulette.config(text=f"[ {s[0]} | {s[1]} | {s[2]} ]")
            
            ms = 25 if self.controller.animations_rapides.get() else 60
            self.after(ms, self.animer)

    def logique_jeu(self):
        carte_tiree = self.canvas.itemcget(self.card_text, "text")
        if self.phase_choix:
            self.carte_cible = carte_tiree
            self.creer_explosion("#D4AF37")
            messagebox.showinfo("🔮 Rituel", f"Le dé a parlé. Votre Shatta Vodou est :\n{self.carte_cible}")
            self.phase_choix = False
            self.label_status.config(text="Traquez votre cible !")
            random.shuffle(self.paquet)
        else:
            self.verifier_victoire(carte_tiree)

    def verifier_victoire(self, carte_tiree):
        if carte_tiree == self.carte_cible:
            self.creer_explosion("#66FCF1")
            self.controller.play_fx("victoire")
            self.controller.show_frame("EcranFin", victoire=True, carte=self.carte_cible, points=self.points)
        else:
            self.controller.play_fx("erreur")
            self.echecs += 1
            self.points += 1
            if self.echecs == 2:
                self.diviser_paquet()
                self.echecs = 0
            
            if len(self.paquet) <= 1 and carte_tiree != self.carte_cible:
                self.controller.show_frame("EcranFin", victoire=False, carte=self.carte_cible, points=self.points)
        
        self.label_points.config(text=f"Points : {self.points}")
        self.label_paquet.config(text=f"Cartes : {len(self.paquet)}")

    def diviser_paquet(self):
        self.controller.play_fx("division")
        messagebox.showwarning("⚠️ Malédiction", "Paire de deux ! Le paquet se divise par deux.")
        if self.carte_cible in self.paquet: self.paquet.remove(self.carte_cible)
        self.paquet = random.sample(self.paquet, max(1, len(self.paquet)//2))
        self.paquet.append(self.carte_cible)
        random.shuffle(self.paquet)

    # --- Particules ---
    def creer_explosion(self, color):
        for _ in range(15):
            p = {
                "id": self.canvas.create_oval(95, 135, 105, 145, fill=color, outline=""),
                "vx": random.uniform(-5, 5), "vy": random.uniform(-5, 5), "vie": 20
            }
            self.particules.append(p)

    def update_particules(self):
        for p in self.particules[:]:
            self.canvas.move(p["id"], p["vx"], p["vy"])
            p["vie"] -= 1
            if p["vie"] <= 0:
                self.canvas.delete(p["id"])
                self.particules.remove(p)
        self.after(30, self.update_particules)

# --- ÉCRAN 4 : FIN ---
class EcranFin(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0B0C10")
        self.controller = controller
        self.label_titre = tk.Label(self, text="", font=("Courier", 35, "bold"), bg="#0B0C10")
        self.label_titre.pack(pady=100)
        self.label_msg = tk.Label(self, text="", font=("Helvetica", 14), bg="#0B0C10", fg="#C5C6C7")
        self.label_msg.pack(pady=20)
        
        tk.Button(self, text="REJOUER", font=("Helvetica", 14, "bold"), bg="#D4AF37", command=lambda: controller.show_frame("JeuShatta")).pack(pady=10)
        tk.Button(self, text="MENU", font=("Helvetica", 12), bg="#1F2833", fg="#C5C6C7", command=lambda: controller.show_frame("MenuPrincipal")).pack(pady=5)

    def on_show(self, victoire=True, carte="", points=0):
        if victoire:
            self.label_titre.config(text="👑 VICTOIRE 👑", fg="#D4AF37")
            self.label_msg.config(text=f"Vous avez capturé le {carte} !\nScore de Malchance : {points}")
        else:
            self.label_titre.config(text="💀 DÉFAITE 💀", fg="#E74C3C")
            self.label_msg.config(text=f"Le {carte} vous a échappé dans les ténèbres...")

if __name__ == "__main__":
    app = Application()
    app.mainloop()