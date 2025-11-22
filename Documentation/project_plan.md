# One Piece RPG - Pre-Grand Line
## Project Planning Document

### Game Overview
- **Genre**: 2D Turn-Based Party RPG
- **Setting**: One Piece Universe - Pre-Grand Line (Starting in East Blue)
- **Platform**: PC (Python/Pygame)
- **Story**: Alternative timeline with custom protagonist

### Core Features

#### Phase 1 - Foundation (MVP)
1. **Basic Game Loop**
   - Main menu
   - Game state management
   - Basic rendering

2. **Character System**
   - Custom character creation
   - Devil Fruit selection at start
   - Base stats (HP, Attack, Defense, Speed, Devil Fruit Power)
   - Character classes/roles

3. **Combat System**
   - Turn-based battle engine
   - Party of up to 5 characters
   - Basic attacks and abilities
   - Devil Fruit powers in combat

4. **Basic World**
   - Starting island (Foosha Village or custom)
   - Simple tile-based movement
   - Basic collision detection

#### Phase 2 - Core Gameplay
5. **Party Management**
   - Recruit crew members
   - Party formations
   - Character switching

6. **Inventory System**
   - Items, weapons, equipment
   - Berries (currency)
   - Devil Fruits (findable)

7. **Quest System**
   - Main story quests
   - Side quests
   - Bounty system

8. **Extended World**
   - Multiple islands in East Blue
   - Town exploration
   - NPC dialogue system

#### Phase 3 - Advanced Features
9. **Ship System**
   - Ship management
   - Naval travel between islands
   - Ship upgrades

10. **Naval Combat**
    - Ship-to-ship battles
    - Boarding mechanics

11. **Advanced Progression**
    - Skill trees
    - Haki system (basic forms)
    - Character development paths

12. **Additional Content**
    - More Devil Fruits
    - Legendary weapons
    - Hidden islands/secrets

#### Phase 4 - Expansion
13. **Other Blues**
    - North, South, West Blue
    - Unique islands per region

14. **Enhanced Systems**
    - Reputation system
    - Wanted level/Marines
    - Crew loyalty/relationships

### Devil Fruit System (Initial Selection)

#### Paramecia Types (Starting Options)
- Gomu Gomu no Mi (Rubber) - Versatile melee fighter
- Bara Bara no Mi (Chop-Chop) - Cannot be cut, evasion boost
- Sube Sube no Mi (Smooth-Smooth) - Defense and charm
- Bomu Bomu no Mi (Bomb-Bomb) - Explosive attacks
- Kilo Kilo no Mi (Kilo-Kilo) - Weight manipulation
- Hana Hana no Mi (Flower-Flower) - Extra limbs/tactics
- Original Paramecia options

#### Zoan Types
- Standard animals (increased stats based on type)
- Original Zoan options

#### Logia Types (Rare/Late game)
- Would be too powerful at start
- Can find/unlock later

### Technical Architecture

#### Folder Structure
```
OnePiece_RPG_PreGrandLine/
├── assets/
│   ├── sprites/
│   │   ├── characters/
│   │   ├── enemies/
│   │   ├── items/
│   │   └── ui/
│   ├── maps/
│   ├── audio/
│   │   ├── music/
│   │   └── sfx/
│   └── fonts/
├── data/
│   ├── devil_fruits.json
│   ├── items.json
│   ├── characters.json
│   ├── enemies.json
│   ├── quests.json
│   └── dialogue.json
├── src/
│   ├── main.py
│   ├── game.py
│   ├── states/
│   │   ├── menu_state.py
│   │   ├── world_state.py
│   │   ├── battle_state.py
│   │   └── character_creation_state.py
│   ├── entities/
│   │   ├── character.py
│   │   ├── enemy.py
│   │   ├── party.py
│   │   └── npc.py
│   ├── combat/
│   │   ├── battle_system.py
│   │   ├── abilities.py
│   │   └── devil_fruit_powers.py
│   ├── world/
│   │   ├── map.py
│   │   ├── island.py
│   │   └── location.py
│   ├── systems/
│   │   ├── inventory.py
│   │   ├── quest_manager.py
│   │   ├── save_system.py
│   │   └── dialogue_system.py
│   ├── ui/
│   │   ├── menu.py
│   │   ├── hud.py
│   │   └── battle_ui.py
│   └── utils/
│       ├── constants.py
│       └── helpers.py
├── saves/
├── requirements.txt
├── README.md
└── project_plan.md
```

### Development Roadmap

**Week 1-2**: Setup & Foundation
- Project structure
- Basic Pygame setup
- Main game loop
- State management system

**Week 3-4**: Character Creation
- Character creation screen
- Devil Fruit selection
- Basic character class

**Week 5-6**: Basic Combat
- Turn-based battle system
- Basic attacks
- Simple enemy AI

**Week 7-8**: World Building
- Tile-based map system
- Player movement
- First island layout

**Week 9-12**: Core Systems
- Party management
- Inventory system
- Basic quests

### Data Structure Examples

#### Character Stats
```python
{
    "name": "Player Name",
    "level": 1,
    "exp": 0,
    "stats": {
        "max_hp": 100,
        "current_hp": 100,
        "attack": 10,
        "defense": 8,
        "speed": 12,
        "df_power": 15  # Devil Fruit Power
    },
    "devil_fruit": "gomu_gomu",
    "abilities": [],
    "equipment": {},
    "inventory": []
}
```

#### Devil Fruit Data
```python
{
    "gomu_gomu": {
        "name": "Gomu Gomu no Mi",
        "type": "paramecia",
        "description": "Grants rubber body properties",
        "weakness": "Cutting attacks, drowning",
        "abilities": [
            "gomu_pistol",
            "gomu_bazooka",
            "gomu_gatling"
        ],
        "stat_mods": {
            "defense": +5,
            "speed": +3
        }
    }
}
```

### Next Steps
1. Set up development environment
2. Create folder structure
3. Install dependencies
4. Begin with basic game loop and state management
5. Build character creation system
