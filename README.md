# 工地血戰 (Construction Bloodbath)

Enterprise‑grade 2D side‑scrolling shooter built with Python 3.11 and Pygame. This repository contains a production‑ready foundation for a Contra‑like action game featuring responsive controls, modular architecture, data‑driven levels, and an assets pipeline optimized for iteration.

- Runtime: Python 3.11 + Pygame
- Entry point: [app.py](app.py)
- Config: [configs/settings.py](configs/settings.py)
- Assets: [assets/](assets), Maps: [assets/data/map.tmx](assets/data/map.tmx), Tilesets: [assets/data/Platforms.tsx](assets/data/Platforms.tsx), [assets/data/Subway_tiles_x4.tsx](assets/data/Subway_tiles_x4.tsx), [assets/data/wall_subway.tsx](assets/data/wall_subway.tsx)
- Dependencies: [requirements.txt](requirements.txt)
- License: [LICENSE](LICENSE)

## Overview

Iron Vortex is a fast‑paced single‑player side‑scroll shooter blending classic run‑and‑gun with modern polish. You play as an Ares Unit operative infiltrating Helix Dominion facilities to destroy the ultimate weapon “Iron Vortex.” Core design goals focus on tight input latency, readable combat, scalable content, and clear separation of concerns for maintainability.

## Features

- Tight movement and combat loop (move, jump, shoot; responsive and predictable)
- Weapon system with level‑up and timed decay mechanics (spec in docs)
- Enemy compositions (infantry, heavy infantry, bosses — see docs)
- Data‑driven level layout via Tiled: [assets/data/map.tmx](assets/data/map.tmx), tilesets in [assets/data/](assets/data)
- Audio/visual feedback: SFX ([assets/audio/](assets/audio)), sprites ([assets/graphics/](assets/graphics))
- Configuration‑first runtime via [configs/settings.py](configs/settings.py)
- Deterministic startup and asset smoke checks: [scripts/smoke_test_assets.py](scripts/smoke_test_assets.py)

## Architecture

Layered, modular organization designed for clarity and extendability:

- Application layer
  - [app.py](app.py): process bootstrap, game loop orchestration, scene lifecycle
- Domain layer
  - [model/entity/](model/entity): game entities (player, enemies, projectiles, tiles)
  - [model/service/](model/service): domain services (collision, physics, spawning, combat rules)
  - [model/factory/](model/factory): factories/builders for entities and level objects
- Configuration layer
  - [configs/settings.py](configs/settings.py): runtime constants, rendering, input, tuning params
- Assets and Data
  - [assets/data/](assets/data): Tiled TMX/TSX maps and tilesets
  - [assets/graphics/](assets/graphics): sprites and UI art
  - [assets/audio/](assets/audio): music and sound effects

This separation keeps the game loop lean, isolates domain logic, and allows content iteration without code changes.

## Getting Started

### Prerequisites

- Python 3.11
- pip, venv (or your environment manager of choice)

### Installation

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

If the smoke test passes, assets are present and loadable.

## Configuration

All runtime configuration lives in [configs/settings.py](configs/settings.py). Typical parameters include:
- Window/screen settings (resolution, caption, FPS)
- Input mappings
- Physics and tuning (gravity, move speed, jump force)
- Combat tuning (damage, cooldowns, projectile speeds)
- Content toggles and debug flags

Adopt a configuration‑first workflow: tune values in config, keep constants out of game loop code.

## Run and Debug

- Run from terminal:
```sh
python app.py
```
- In VS Code: open the workspace, run [app.py](app.py) with the built‑in debugger (recommended). Use the integrated terminal and Output pane for logs.

## Gameplay and Controls

- Arrow Keys: Move/Jump
- Space: Shoot

Game flow: Main Menu → Stage progression (enemies → power‑ups → Boss) → Results.

## Assets and Maps

- Levels authored in Tiled: [assets/data/map.tmx](assets/data/map.tmx), tilesets in [assets/data/](assets/data)
- Graphics: [assets/graphics/](assets/graphics) (e.g., bullet sprite at [assets/graphics/bullet.png](assets/graphics/bullet.png))
- Audio: [assets/audio/](assets/audio) (e.g., [bullet.wav](assets/audio/bullet.wav), [hit.wav](assets/audio/hit.wav), [music.wav](assets/audio/music.wav))

## Project Structure

```
ConstructionBloodbath/
├─ app.py
├─ requirements.txt
├─ configs/
│  └─ settings.py
├─ model/
│  ├─ entity/
│  ├─ factory/
│  └─ service/
└─ assets/
   ├─ audio/
   ├─ graphics/
   └─ data/
      ├─ map.tmx
      ├─ Platforms.tsx
      ├─ Subway_tiles_x4.tsx
      └─ wall_subway.tsx
```

## Quality and Tooling

- Code style: PEP 8, type hints encouraged for domain services/entities
- Formatting/Linting: integrate Black/Flake8/Mypy as needed
- Coverage: Python coverage supported (see IDE config traces in project settings)

## Roadmap

- Expand enemy behaviors and boss patterns (see docs)
- Implement full weapon level/decay system per spec
- Add save/load and scoring
- Introduce CI workflow (lint, type check, smoke test)
- Packaging and distribution (itch.io/Steam‑ready build scripts)

## Contributing

- Fork the repo, create a feature branch, open a PR
- Keep gameplay constants in [configs/settings.py](configs/settings.py)
- Follow domain boundaries: entity/factory/service separation
- Add/update smoke tests for new assets

## License

Auralytics is licensed under the Apache License 2.0. You are free to use, modify, and distribute the project, as long as you comply with the terms of the license, including proper attribution and inclusion of the license notice.

This project is licensed under the MIT License. See [LICENSE](LICENSE).

## Contact Us

If you have any questions or suggestions, feel free to reach out to us:

Email: twcch1218 [at] gmail.com

Thank you for your interest in ConstructionBloodbath! We look forward to your contributions and hope you enjoy using and improving this project.

## Acknowledgements

- Course: National Cheng Kung University — “Python Programming and Interactive Game Design”
- Inspirations: Contra, Metal Slug
- See design doc for creative direction and narrative:
