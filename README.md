# 🃏 Shatta Vodou : Edition "Le Dé du Destin"

Une implémentation moderne et graphique du célèbre jeu **Shatta Vodou**. Alliez le hasard pur d'un dé à 52 faces à la mystique des cartes pour retrouver votre cible avant que le paquet ne disparaisse !

---

## 📖 Le Concept

Le **Shatta Vodou** est un jeu de probabilités interactif. Le but est de sélectionner une carte fétiche via un dé rituel, puis de la traquer dans un paquet en mouvement. Plus vous échouez, plus les forces du "Vodou" vous aident en réduisant la taille du paquet.

### 🎮 Règles du Jeu

1.  **L'Invocation (Phase 1) :** Lancez le **dé à 52 faces (d52)**. Le résultat détermine votre carte cible parmi les 52 cartes du paquet.
2.  **La Traque (Phase 2) :** Le paquet défile. Cliquez sur **STOP** pour tenter d'immobiliser votre carte.
3.  **La Victoire :** Si vous trouvez la carte, vous gagnez la partie !
4.  **La Malédiction "Paire de deux" :** Si vous manquez votre cible deux fois de suite, le sort s'active : le paquet est **divisé par deux**, augmentant radicalement vos chances de succès au tour suivant.

---

## ✨ Caractéristiques de la version Pro

* **Interface Graphique (GUI) :** Une fenêtre immersive avec un thème "Dark Mystique".
* **Animation Fluide :** Défilement des cartes et du dé à haute fréquence pour un effet "Casino".
* **Logique de Probabilité :** Algorithme intelligent qui divise le paquet tout en protégeant la carte cible.
* **Feedback Visuel :** Détection des couleurs (Cœurs/Carreaux en rouge) et messages d'alerte interactifs.

---

## 🚀 Installation & Lancement

### 📋 Prérequis

Le projet nécessite **Python 3** et la bibliothèque **Tkinter**.

#### Sur Linux (Ubuntu/Debian/Kali) :
Tkinter n'est pas toujours installé par défaut. Exécutez la commande suivante :
```bash
sudo apt update && sudo apt install python3-tk