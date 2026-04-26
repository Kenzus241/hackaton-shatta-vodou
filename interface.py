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
