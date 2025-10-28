# 🐍 SnakeGame — Python Turtle

Petit **Snake** en Python (module `turtle`) — pratique pour jouer *et* le transformer ensuite en **environnement de Reinforcement Learning** (SARSA / Q-Learning / DQN).

<p align="center">
  <img src="assets/demo.gif" alt="Demo gif" width="500">
</p>

## ✨ Features
- Déplacements au clavier **ZQSD / WASD / Flèches**
- **Escape** pour quitter proprement (pas d’erreur `turtle.Terminator`)
- Boucle de jeu simple → idéale pour l’étendre (pomme, score, collisions)
- Base parfaite pour un **env Gym-like** (états, actions, récompenses)

## 🚀 Lancer le jeu
```bash
python snake_game.py
