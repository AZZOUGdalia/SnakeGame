# sarsa_agent.py
# -- Snake minimal en grille + SARSA (on-policy) --
# -> NE TOUCHE PAS ton jeu. Ceci tourne séparément.

import random
from collections import defaultdict
import csv
from datetime import datetime

# =========================
# Hyperparamètres (modifie)
# =========================
ALPHA = 0.2       # taux d'apprentissage
GAMMA = 0.95      # discount
EPSILON = 0.10    # exploration initiale
EPS_DECAY = 0.995 # décroissance par épisode
EPS_MIN = 0.02

EPISODES = 300
MAX_STEPS = 2000
LOG_CSV = "sarsa_training_log.csv"  # résultats

ACTIONS = ["up", "right", "down", "left"]  # 0,1,2,3

# =========================
# ENVIRONNEMENT SNAKE (grid)
# =========================
class GridSnakeEnv:
    """Snake en grille (pas de turtle), état compact pour RL."""
    def __init__(self, size=30):
        self.N = size
        self.reset()

    def reset(self):
        """Réinitialise le jeu"""
        self.dir = 0  # 0=up,1=right,2=down,3=left
        c = self.N // 2
        self.snake = [(c, c)]               # tête seule au centre
        self.snake_set = set(self.snake)    # synchro liste/set
        self.place_food()
        return self.get_state()

    def place_food(self):
        """Place la nourriture aléatoirement dans la grille"""
        while True:
            f = (random.randrange(self.N), random.randrange(self.N))
            if f not in self.snake_set:
                self.food = f
                return

    def step(self, action):
        """Fait avancer le serpent d'une étape selon l'action"""
        # anti demi-tour : si action opposée à dir -> ignore
        if (action - self.dir) % 2 == 0 and action != self.dir:
            action = self.dir
        self.dir = action

        head = self.snake[0]
        x, y = head
        if self.dir == 0:     y -= 1
        elif self.dir == 1:   x += 1
        elif self.dir == 2:   y += 1
        elif self.dir == 3:   x -= 1
        new_head = (x, y)

        reward = -0.01
        done = False

        # murs
        if not (0 <= x < self.N and 0 <= y < self.N):
            return self.get_state(), reward - 10.0, True, {}

        tail = self.snake[-1]
        will_eat = (new_head == self.food)

        # --- collision corps correcte ---
        # Autorisé de marcher sur la queue uniquement si on ne mange pas
        body_hits = (new_head in self.snake_set) and (will_eat or new_head != tail)
        if body_hits:
            return self.get_state(), reward - 10.0, True, {}

        # avance la tête
        self.snake.insert(0, new_head)
        self.snake_set.add(new_head)

        if will_eat:
            reward += 10.0
            self.place_food()  # on N'ENLÈVE PAS la queue => le snake s'allonge
        else:
            # retire la queue (utilise discard pour éviter KeyError)
            popped = self.snake.pop()
            self.snake_set.discard(popped)

        return self.get_state(), reward, done, {}

    def get_state(self):
        """Retourne un état compact pour l'agent (danger + direction + position food)"""
        def left_dir(d):  return (d - 1) % 4
        def right_dir(d): return (d + 1) % 4

        def step_in_dir(pos, d):
            x, y = pos
            if d == 0:   return (x, y-1)
            if d == 1:   return (x+1, y)
            if d == 2:   return (x, y+1)
            return (x-1, y)

        def danger_at(pos):
            x, y = pos
            if not (0 <= x < self.N and 0 <= y < self.N):
                return 1
            tail = self.snake[-1]
            if pos in self.snake_set and pos != tail:
                return 1
            return 0

        head = self.snake[0]
        ahead = step_in_dir(head, self.dir)
        leftp = step_in_dir(head, left_dir(self.dir))
        rightp = step_in_dir(head, right_dir(self.dir))

        dang_a = danger_at(ahead)
        dang_l = danger_at(leftp)
        dang_r = danger_at(rightp)

        fx, fy = self.food
        hx, hy = head
        dx = fx - hx
        dy = fy - hy
        sx = 0 if dx == 0 else (1 if dx > 0 else -1)
        sy = 0 if dy == 0 else (1 if dy > 0 else -1)

        return (dang_a, dang_l, dang_r, self.dir, sx, sy)

# ==============
#  SARSA (table)
# ==============
Q = defaultdict(float)

def epsilon_greedy(state, epsilon):
    """Politique epsilon-greedy : explore ou exploite"""
    if random.random() < epsilon:
        return random.randrange(4)
    best_a, best_q = 0, -1e18
    for a in range(4):
        q = Q[(state, a)]
        if q > best_q:
            best_q, best_a = q, a
    return best_a

def sarsa_update(s, a, r, s2, a2):
    """Mise à jour SARSA on-policy"""
    Q[(s, a)] += ALPHA * (r + GAMMA * Q[(s2, a2)] - Q[(s, a)])

# ===========
#  TRAINING
# ===========
def run():
    env = GridSnakeEnv(size=30)
    eps = EPSILON

    # préparer CSV
    with open(LOG_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["datetime", "episode", "steps", "return", "epsilon"])

    for ep in range(1, EPISODES + 1):
        s = env.reset()
        a = epsilon_greedy(s, eps)
        total_r, steps = 0.0, 0

        for t in range(MAX_STEPS):
            s2, r, done, _ = env.step(a)
            a2 = epsilon_greedy(s2, eps)
            sarsa_update(s, a, r, s2, a2)

            total_r += r
            steps += 1

            if done:
                break
            s, a = s2, a2

        eps = max(EPS_MIN, eps * EPS_DECAY)

        print(f"[EP {ep:03d}] steps={steps:4d}  R={total_r:7.2f}  eps={eps:.3f}")
        with open(LOG_CSV, "a", newline="") as f:
            w = csv.writer(f)
            w.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ep, steps, round(total_r, 2), round(eps, 3)
            ])

    print("✅ Entraînement terminé. Résultats enregistrés dans", LOG_CSV)


if __name__ == "__main__":
    run()
