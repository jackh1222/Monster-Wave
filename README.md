# Monster Waves 怪兽来袭

**Monster Waves** is a 2D platformer game built with Python and Pygame. Guide your character through multiple levels of increasingly fierce Goomba-like enemies, jump across platforms, and blast foes with timely shots to survive.

---

## Game Overview

* **Objective**: Clear all enemies in each level to progress. Enemies double in count on each new level.
* **Player Mechanics**:

  * **Move**: ← / → arrows
  * **Jump**: SPACE (gravity, landing, and collision detection)
  * **Shoot**: Z (bullets travel horizontally; 3 hits kill an enemy)
* **Enemies**:

  * Patrol randomly left or right
  * Bounce at platform edges and walls
  * Display corpse frame for 0.5s after 3 hits, then disappear
* **UI & Game States**:

  * **Main Menu** with **Start** / **Rules**
  * **Rules** screen explaining controls
  * **Game Over** screen with **Restart**
  * **Level Cleared** screen with **Next Level**

---

## File Structure

```
Monster Wave/
├── main.py           # Entry point & game state manager
├── config.py         # Global constants (screen size, FPS, gravity)
├── tilemap.py        # Platform & level layout loader
├── player.py         # Player sprite class (movement, collisions, animations)
├── entities.py       # Enemy & Bullet sprite classes (AI, death logic)
├── animation.py      # Sprite-sheet loader utility
├── combine_sprite.py # (Optional) Pipelines individual PNG frames into a sheet
├── level1.csv        # Sample level layout (tilemap CSV)
├── sprite_sheet.png  # Packed sprites for player & enemies
├── assets/           # (Optional) folder for additional art & sounds
└── README.md         # Project overview and usage instructions
```

---

## Installation & Running

1. **Clone** this repository:

   ```bash
   git clone https://github.com/yourusername/monster-wave.git
   cd monster-wave
   ```
2. **Create** and **activate** a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install** dependencies:

   ```bash
   pip install pygame pillow
   ```
4. **Run** the game:

   ```bash
   python main.py
   ```

---

## Controls & Rules

* **Main Menu**: Use mouse to click **Start** or **Rules**.
* **Rules Screen**: Read instructions, click **Back** to return.
* **In-Game**:

  * ← / → : Move left/right
  * SPACE : Jump
  * Z     : Shoot bullets (3 hits required per enemy)
* **Objective**: Eliminate all enemies to unlock **Next Level**. Enemies double each level.
* **Game Over**: Touching an enemy kills you. Click **Restart** to retry the same level.

---

## Customization

* **Levels**: Create additional CSV maps and load them by modifying `setup_level()` in `main.py`.
* **Sprites**: Replace `sprite_sheet.png` with your own art; adjust `animation.py` states.
* **Mechanics**: Tweak `config.py` parameters (gravity, speeds, bullet count) for different gameplay feel.

---
