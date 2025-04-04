# Projet d'Exploration - Jeu de Défense avec Pygame
Par Marilyn Diaz et Léa Evraire

## Description
Ce projet fait partie de notre classe **"Projet d'Exploration"** et constitue notre projet final. Il s'agit d'un jeu de défense de tours créé avec la bibliothèque **Pygame**. L'objectif du jeu est de défendre un territoire contre des vagues d'ennemis en plaçant des tours stratégiquement sur la carte.

Nous devions inclure deux algorithmes différents : le `Pathfinding A*` et le `Backtracking`.
Étant donné que c'est notre première expérience avec **Pygame**, 
la base du projet (le fonctionnement de la boucle de jeu et l'utilisation des classes de Pygame), ainsi que l'inclusion d'assets et d'animations, ont été créées grâce à un tutoriel YouTube détaillé, que vous pouvez trouver [ici](https://www.youtube.com/watch?v=WRuf9iPAXfM).
Pour le reste du projet, notamment les algorithmes et le "gameplay", nous avons utilisé nos connaissances et compétences acquises à travers nos études.

Des "assets" ont été utilisés pour ajouter un look plus intéressant à notre jeu. Vous pouvez les retrouver [ici](https://www.kenney.nl/assets/tower-defense-top-down) et [ici](https://fkgcluster.itch.io/survivaltowerdefense/download/eyJpZCI6MjQwNTc5NSwiZXhwaXJlcyI6MTc0Mzc4MzczNH0%3d.B4GQzia1U8Myd9DQqWM3HQuq0pc%3d)

## Prérequis

Avant de pouvoir exécuter le jeu, vous devez installer **Pygame**, une bibliothèque Python qui permet de créer des jeux 2D.

### Installation de Pygame

Si vous n'avez pas encore installé Pygame, voici les étapes à suivre :

1. Assurez-vous d'avoir **Python** installé sur votre machine. Vous pouvez télécharger la dernière version de Python ici :  
   [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. Une fois Python installé, ouvrez votre terminal (ou invite de commande) et installez Pygame avec la commande suivante :  
   ```
   pip install pygame
   ```
Notes: 

Sur Windows, si Python cause un problème, essayez d'utiliser la commande `py` à la place de `python`.

De plus, n'oubliez pas d'activer l'environnement virtuel avec la commande suivante:
```
.\venv\Scripts\activate
```

## Cloner de dépôt

1. Ouvrez votre terminal (ou invite de commande).

2. Clonez le dépôt GitHub avec la commande suivante :
   ```
   git clone https://github.com/marid1/projetExploration.git
   ```

## Lancer le jeu

1. Accédez au répertoire de projet

2. Exécutez le fichier principal du jeu avec la commande:
   ```
   python main.py
   ```
