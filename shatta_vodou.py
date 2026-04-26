import tkinter as tk
from tkinter import messagebox
import random

# --- GESTIONNAIRE DE FENÊTRES PRINCIPAL ---
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🃏 Shatta Vodou : Le Dé du Destin")
        self.geometry("900x800")
        self.configure(bg="#0B0C10")
        
        # Variables globales pour les paramètres
        self.son_active = tk.BooleanVar(value=True)
        self.animations_rapides = tk.BooleanVar(value=False)

        # Conteneur principal qui va stocker nos écrans (Frames)
        container = tk.Frame(self, bg="#0B0C10")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Initialisation de tous les écrans
        for F in (MenuPrincipal, Parametres, JeuShatta, EcranFin):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # On superpose toutes les frames au même endroit
            frame.grid(row=0, column=0, sticky="nsew")

        # Afficher le menu principal au démarrage
        self.show_frame("MenuPrincipal")

    def show_frame(self, page_name, **kwargs):
        """Affiche un écran spécifique et lui passe des arguments si besoin (ex: score de fin)"""
        frame = self.frames[page_name]
        if hasattr(frame, 'on_show'):
            frame.on_show(**kwargs)
        frame.tkraise()

# --- ÉCRAN 1 : MENU PRINCIPAL ---
class MenuPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0B0C10")
        self.controller = controller

        # Titres
        tk.Label(self, text="SHATTA VODOU", font=("Courier", 45, "bold"), bg="#0B0C10", fg="#D4AF37").pack(pady=(100, 10))
        tk.Label(self, text="ÉDITION LE DÉ DU DESTIN", font=("Helvetica", 16, "italic"), bg="#0B0C10", fg="#66FCF1").pack(pady=(0, 60))

        # Boutons de navigation
        btn_jouer = tk.Button(self, text="LANCER LE RITUEL", font=("Helvetica", 18, "bold"), bg="#D4AF37", fg="#0B0C10", 
                              width=20, height=2, cursor="hand2", command=lambda: controller.show_frame("JeuShatta"))
        btn_jouer.pack(pady=15)

        btn_param = tk.Button(self, text="PARAMÈTRES", font=("Helvetica", 14), bg="#1F2833", fg="#C5C6C7", 
                              width=20, cursor="hand2", command=lambda: controller.show_frame("Parametres"))
        btn_param.pack(pady=10)

        btn_quitter = tk.Button(self, text="QUITTER", font=("Helvetica", 14), bg="#E74C3C", fg="white", 
                                width=20, cursor="hand2", command=controller.quit)
        btn_quitter.pack(pady=10)

# --- ÉCRAN 2 : PARAMÈTRES ---
class Parametres(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0B0C10")
        self.controller = controller

        tk.Label(self, text="⚙️ PARAMÈTRES", font=("Courier", 30, "bold"), bg="#0B0C10", fg="#D4AF37").pack(pady=(80, 50))

        # Checkboxes liées aux variables globales de l'app
        tk.Checkbutton(self, text="Activer le Son (Mockup)", variable=controller.son_active, font=("Helvetica", 14), 
                       bg="#0B0C10", fg="#C5C6C7", selectcolor="#1F2833", cursor="hand2").pack(pady=10)
        
        tk.Checkbutton(self, text="Animations Rapides", variable=controller.animations_rapides, font=("Helvetica", 14), 
                       bg="#0B0C10", fg="#C5C6C7", selectcolor="#1F2833", cursor="hand2").pack(pady=10)

        btn_retour = tk.Button(self, text="RETOUR AU MENU", font=("Helvetica", 14, "bold"), bg="#1F2833", fg="#C5C6C7", 
                               width=20, cursor="hand2", command=lambda: controller.show_frame("MenuPrincipal"))
        btn_retour.pack(pady=60)

# --- ÉCRAN 3 : LE JEU EN LUI-MÊME ---
class JeuShatta(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2F2E22")
        self.controller = controller
        
        # Variables de Jeu
        self.valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'V', 'D', 'R', 'As']
        self.couleurs = ['♥', '♦', '♣', '♠']
        self.paquet = []
        self.carte_cible = None
        self.echecs_consecutifs = 0
        self.en_defilement = False
        self.phase_choix = True 

        self.setup_ui()

    def on_show(self):
        """Fonction appelée à chaque fois qu'on affiche cet écran"""
        self.reset_jeu()

    def setup_ui(self):
        tk.Label(self, text="SHATTA VODOU", font=("Courier", 24, "bold"), bg="#2F2E22", fg="#D4AF37").pack(pady=(20, 5))

        self.frame_de = tk.Frame(self, bg="#1F2833", bd=2, relief="ridge")
        self.frame_de.pack(pady=10, padx=50, fill="x")

        self.label_de_container = tk.Label(self.frame_de, text="JEU DE CARTE", font=("Helvetica", 10, "bold"), bg="#1F2833", fg="#C5C6C7")
        self.label_de_container.pack(pady=(10, 0))
        
        self.label_de_valeur = tk.Label(self.frame_de, text="--", font=("Helvetica", 36, "bold"), bg="#1F2833", fg="#45A29E")
        self.label_de_valeur.pack(pady=(0, 10))

        self.card_frame = tk.Frame(self, width=200, height=280, bg="#FFFFFF", highlightbackground="#D4AF37", highlightthickness=4)
        self.card_frame.pack_propagate(False)
        self.card_frame.pack(pady=20)

        self.label_carte = tk.Label(self.card_frame, text="?", font=("Helvetica", 65, "bold"), bg="#FFFFFF")
        self.label_carte.place(relx=0.5, rely=0.5, anchor="center")

        self.label_status = tk.Label(self, text="C'est le moment de choisir ton SHATTA VODOU.", font=("Helvetica", 14), bg="#2F2E22", fg="#FFFFFF")
        self.label_status.pack(pady=10)

        self.label_stats = tk.Label(self, text="", font=("Helvetica", 11), bg="#2F2E22", fg="#C5C6C7")
        self.label_stats.pack()

        self.btn_action = tk.Button(self, text="PIOCHE UNE CARTE", font=("Helvetica", 16, "bold"), bg="#D4AF37", fg="#0B0C10", 
                                    activebackground="#F3E5AB", width=18, height=2, cursor="hand2", command=self.toggle_defilement)
        self.btn_action.pack(pady=20)
        
        # Bouton d'abandon (optionnel)
        tk.Button(self, text="Abandonner", font=("Helvetica", 10), bg="#E74C3C", fg="white", cursor="hand2", 
                  command=lambda: self.controller.show_frame("MenuPrincipal")).pack()

    def toggle_defilement(self):
        if not self.en_defilement:
            self.en_defilement = True
            self.btn_action.config(text="STOP", bg="#E74C3C", fg="white", activebackground="#C0392B")
            self.animer()
        else:
            self.en_defilement = False
            self.btn_action.config(text="START" if not self.phase_choix else "MÉLANGER LE PAQUET", bg="#D4AF37", fg="#0B0C10")
            self.logique_jeu()

    def animer(self):
        if self.en_defilement:
            index_de = random.randint(1, len(self.paquet))
            carte_actuelle = self.paquet[index_de - 1]

            self.label_de_valeur.config(text=f"🎲 {index_de}")
            couleur_symbole = "#E74C3C" if any(x in carte_actuelle for x in ['♥', '♦']) else "#0B0C10"
            self.label_carte.config(text=carte_actuelle, fg=couleur_symbole)
            
            # Ajustement vitesse selon les paramètres
            vitesse = 20 if self.controller.animations_rapides.get() else 50
            self.after(vitesse, self.animer)

    def logique_jeu(self):
        carte_tiree = self.label_carte.cget("text")

        if self.phase_choix:
            self.carte_cible = carte_tiree
            messagebox.showinfo("🔮 Le Sort est jeté", f"Ta carte a été piochée, ton shatta vodou est : \n{self.carte_cible}")
            self.phase_choix = False
            self.label_status.config(text="Le paquet défile... Traque ton Shatta Vodou !", fg="#66FCF1")
            self.label_de_container.config(text="DERNIER TIRAGE")
            random.shuffle(self.paquet)
        else:
            if carte_tiree == self.carte_cible:
                # VICTOIRE : On bascule sur l'écran de fin
                self.controller.show_frame("EcranFin", victoire=True, carte=self.carte_cible)
            else:
                self.echecs_consecutifs += 1
                if self.echecs_consecutifs == 2:
                    self.diviser_paquet(carte_tiree)
                    self.echecs_consecutifs = 0
                else:
                    self.label_status.config(text=f"Échec... le {self.carte_cible} t'échappe encore.", fg="#E74C3C")
                
                # DÉFAITE : Si c'est la dernière carte et ce n'est pas la bonne
                if len(self.paquet) <= 1 and carte_tiree != self.carte_cible:
                    self.controller.show_frame("EcranFin", victoire=False, carte=self.carte_cible)

        self.label_stats.config(text=f"Cartes dans le paquet : {len(self.paquet)}")

    def diviser_paquet(self, carte_perdue):
        messagebox.showwarning("⚠️ Malédiction : Paire de deux", f"{carte_perdue} n'est pas ta cible.\nPaire de deux : Le paquet se divise !")
        if self.carte_cible in self.paquet:
            self.paquet.remove(self.carte_cible)
        taille_reduite = max(1, len(self.paquet) // 2) # S'assure qu'on ne descend pas sous 1
        self.paquet = random.sample(self.paquet, taille_reduite)
        self.paquet.append(self.carte_cible)
        random.shuffle(self.paquet)
        self.label_status.config(text="Le paquet s'est réduit... tes chances augmentent.", fg="#D4AF37")

    def reset_jeu(self):
        self.paquet = [f"{v}{c}" for v in self.valeurs for c in self.couleurs]
        self.carte_cible = None
        self.phase_choix = True
        self.echecs_consecutifs = 0
        self.en_defilement = False
        self.label_carte.config(text="?", fg="#0B0C10")
        self.label_de_valeur.config(text="--", fg="#45A29E")
        self.btn_action.config(text="PIOCHE UNE CARTE", bg="#D4AF37")
        self.label_status.config(text="C'est le moment de choisir ton SHATTA VODOU.", fg="#FFFFFF")
        self.label_de_container.config(text="JEU DE CARTE")
        self.label_stats.config(text=f"Cartes dans le paquet : {len(self.paquet)} / 52")

# --- ÉCRAN 4 : FIN DE PARTIE (VICTOIRE / DÉFAITE) ---
class EcranFin(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0B0C10")
        self.controller = controller

        self.label_titre = tk.Label(self, text="", font=("Courier", 40, "bold"), bg="#0B0C10")
        self.label_titre.pack(pady=(120, 20))

        self.label_message = tk.Label(self, text="", font=("Helvetica", 18), bg="#0B0C10", fg="#C5C6C7")
        self.label_message.pack(pady=20)

        self.label_carte = tk.Label(self, text="", font=("Helvetica", 50, "bold"), bg="#0B0C10", fg="#D4AF37")
        self.label_carte.pack(pady=20)

        btn_rejouer = tk.Button(self, text="REJOUER", font=("Helvetica", 16, "bold"), bg="#D4AF37", fg="#0B0C10", 
                                width=15, cursor="hand2", command=lambda: controller.show_frame("JeuShatta"))
        btn_rejouer.pack(pady=15)

        btn_menu = tk.Button(self, text="MENU PRINCIPAL", font=("Helvetica", 14), bg="#1F2833", fg="#C5C6C7", 
                             width=20, cursor="hand2", command=lambda: controller.show_frame("MenuPrincipal"))
        btn_menu.pack(pady=10)

    def on_show(self, victoire=True, carte=""):
        """Met à jour l'affichage selon si le joueur a gagné ou perdu"""
        self.label_carte.config(text=carte)
        if victoire:
            self.label_titre.config(text="👑 VICTOIRE 👑", fg="#D4AF37")
            self.label_message.config(text="Le sort est brisé ! Tu as trouvé ton SHATTA VODOU.")
        else:
            self.label_titre.config(text="💀 DÉFAITE 💀", fg="#E74C3C")
            self.label_message.config(text="Les esprits t'ont trompé... La carte t'a échappé.")

# --- LANCEMENT ---
if __name__ == "__main__":
    app = Application()
    app.mainloop()