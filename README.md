## Mode Agent RL vs Agent RL

```markdown
# Pong — Agent RL vs Agent RL

## Description
Dans ce mode, deux agents RL s’affrontent.
Chaque agent utilise l’algorithme Q-learning et apprend simultanément
à partir des récompenses reçues pendant le jeu.

## Fichiers
- `agent.py` : définition de l’agent Q-learning.
- `game.py` : gestion du jeu avec deux agents RL.
- `main.py` : lancement de l’apprentissage et visualisation des performances.

## Objectif
Analyser la coévolution de deux agents intelligents dans un environnement compétitif.

## Remarque
L’apprentissage est plus instable car les deux agents évoluent en même temps.

## Exécution
```bash
python main.py
