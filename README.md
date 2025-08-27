# Construction Bloodbath (工地血戰)

Enterprise-grade 2D side-scrolling shooter built with Python 3.11 and Pygame.
This repository provides a production-ready foundation for a Contra-style action game, featuring responsive controls, modular architecture, data-driven levels, and an asset pipeline optimized for iteration.

## Features

- Smooth movement / jumping / shooting loops (predictable and responsive)
- Data-driven maps: Tiled TMX/TSX ([assets/data/map.tmx](assets/data/map.tmx))
- Clear layered architecture: Application / Domain / Config / Assets
- Centralized adjustable parameters in [configs/settings.py](configs/settings.py)
- Sprite / sound asset loading with startup validation (extensible)
- Encapsulated scene and level management ([core/scene_manager.py](core/scene_manager.py), [core/level_manager.py](core/level_manager.py))
- Extensible Entity / Factory / Service patterns ([model/entity/](model/entity), [model/factory/](model/factory), [model/service/](model/service))
- HUD / UI example ([ui/hud.py](ui/hud.py))
- MIT License allowing commercial use and derivative works ([LICENSE](LICENSE))

## Goals & Design Philosophy

- Data first: values and tuning live in configs or data files, not hard-coded.
- Hot-swappable content: add sprites, levels, or enemy types without touching the main loop.
- Separation of rendering and logic: supports alternative rendering layers or performance profiling.
- Clear lifecycle: startup, asset load, scene push/pop, level reset.

## Project Structure

```
ConstructionBloodbath/
├─ app.py                       # Entry point: initialization, main loop, scene dispatch
├─ configs/
│  └─ settings.py               # Global configuration and tuning parameters
├─ core/
│  ├─ game_app.py               # High-level application wrapper
│  ├─ scene_manager.py          # Scene stack / transitions
│  └─ level_manager.py          # Level loading and reset
├─ model/
│  ├─ entity/                   # Game entities
│  ├─ factory/                  # Builders / assemblers
│  └─ service/                  # Logic services (collision, physics, combat, etc.)
├─ ui/
│  └─ hud.py                    # HUD / UI
├─ assets/
│  ├─ data/                     # Tiled: map.tmx / *.tsx
│  ├─ graphics/                 # Sprites and animations
│  └─ audio/                    # Sound effects / music
└─ build/                       # (Optional) packaged artifacts / cross-reference outputs

```

## Key Modules

- Entry point: [app.py](app.py)
- Configuration: [configs/settings.py](configs/settings.py)
- Core loop: [core/game_app.py](core/game_app.py)
- Scene management: [core/scene_manager.py](core/scene_manager.py)
- Level management: [core/level_manager.py](core/level_manager.py)
- HUD: [ui/hud.py](ui/hud.py)

## Setup

### Prerequisites

- Python 3.11
- pip / venv

### Installation

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run & Debug

### Direct execution

```sh
python app.py
```

### VS Code

- Open the project folder
- Run [app.py](app.py) in debug mode
- Use “Terminal” and “Output” to inspect logs

## Configuration

Centralized in [configs/settings.py](configs/settings.py):

- Window: resolution, title, FPS
- Input mapping
- Physics: gravity, movement speed, jump force
- Combat: damage, cooldown, fire rate
- Debug toggles and flags
- Tuning workflow:

Adjust parameters:

- Restart or hot-reload (if implemented)
- Verify gameplay feel / performance

## Game Loop (Overview)

- Collect events (input)
- Update states (physics / AI / shooting / timers)
- Handle collisions and outcomes
- Evaluate scene / level conditions
- Render (background / entities / UI)

Scenes are managed by [core/scene_manager.py](core/scene_manager.py) ; levels are loaded and reset by [core/level_manager.py](core/level_manager.py).

## Assets & Data

- Maps: [assets/data/map.tmx](assets/data/map.tmx) with corresponding tilesets (e.g. [assets/data/Platforms.tsx](assets/data/Platforms.tsx), [assets/data/Subway_tiles_x4.tsx](assets/data/Subway_tiles_x4.tsx), [assets/data/wall_subway.tsx](assets/data/wall_subway.tsx))
- Graphics: [assets/graphics/](assets/graphics/)
- Audio: [assets/audio/](assets/audio/)
- Fonts: [assets/font/](assets/font/)
 (including CJK fonts if needed)

Naming conventions:

- Animation sequences: direction/state/frame (e.g. player/right/0.png)
- Separate static objects, interactive objects, and enemy folders



## Extension Guidelines

| Type | Suggested Steps |
| ---- | -------- |
| New enemy | Add model/entity/... → Factory instantiation → Configure behavior service |
| New weapon | Define attributes → Shooting/Projectile service → Bind to input mapping |
| New level | Create TMX in Tiled → Place into assets/data → Load via Level Manager |
| New UI item | Implement UI class → Inject into render pipeline → Use config parameters |

## Build / Distribution

When packaging with PyInstaller (or similar), place outputs in [build/](build).

Guidelines:
- Use relative paths for assets (avoid hard-coding absolute paths)
- Exclude unused heavy dependencies from the binary
- Test cross-platform font/encoding support

## Validation

Basic smoke tests:
- Start without exceptions
- Sprites and audio load correctly
- Characters can move / jump / shoot
- Scene transitions are smooth

Can be gradually added:
- Units: numerical calculations / services (collision, cooldown)
- Behaviors: AI decision-making
- Regression: level nodes / event triggers

## Roadmap

- More comprehensive event bus / system events
- Plug-in AI behavior trees
- Save / Load profile
- Particle systems and post-processing
- Net code (for potential multiplayer)

## Contributing

We enthusiastically welcome contributions from the community! Every pull request (PR) is carefully reviewed, and we strive to incorporate meaningful improvements into the production environment.
How to Contribute:

1. Fork the repository.
2. Create a new branch for your feature/fix.
3. Make sure to follow the existing project structure to make you change and test them locally.
4. Update the relevant documentations.
5. Submit a pull request with a clear description.

## License

Auralytics is licensed under the Apache License 2.0. You are free to use, modify, and distribute the project, as long as you comply with the terms of the license, including proper attribution and inclusion of the license notice.

This project is licensed under the MIT License. See [LICENSE](LICENSE).

## Contact Us

If you have any questions or suggestions, feel free to reach out to us:

Email: twcch1218 [at] gmail.com

Thank you for your interest in ConstructionBloodbath! We look forward to your contributions and hope you enjoy using and improving this project.
