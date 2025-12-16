# Getting Started - Phase 1

## Setup Instructions

### 1. Install Python
Make sure you have Python 3.8 or higher installed.

Check with:
```bash
python --version
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Game
```bash
python main.py
```

---

## Current Features (Phase 1.1 - Basic Game Loop)

✅ **Implemented:**
- Main game loop with 60 FPS
- State management system
- Main menu with keyboard navigation
- Basic UI rendering

❌ **Not Yet Implemented:**
- Character creation
- Combat system
- World/movement
- Save/load system

---

## Controls

### Main Menu
- **Arrow Keys / WASD** - Navigate menu
- **Enter / Space** - Select option
- **ESC** - Quit game

---

## Project Structure

```
OnePiece_RPG_PreGrandLine/
├── main.py                    # Entry point - RUN THIS
├── requirements.txt           # Python dependencies
│
├── src/                       # Source code
│   ├── game.py               # Main game class
│   ├── states/               # Game states
│   │   ├── state.py          # Base state class
│   │   ├── state_manager.py  # State management
│   │   └── menu_state.py     # Main menu
│   └── utils/
│       ├── constants.py      # Game constants
│       └── helpers.py        # Helper functions
│
├── Database/                  # JSON game data
│   ├── DevilFruits/          # Devil Fruit data
│   ├── Weapons/              # Weapon data
│   ├── Inventory/            # Item data
│   └── ...                   # Other game data
│
└── Documentation/            # Design docs
    ├── GameDesign.md         # Complete game design
    ├── Phase1_Implementation_Plan.md  # Implementation guide
    └── QuickDecisions.md     # Decision checklist
```

---

## Development Roadmap

### Phase 1.1 - Basic Game Loop ✅ COMPLETE
- Main game loop
- State management
- Main menu

### Phase 1.2 - Character System (NEXT)
- Character data structure
- Devil Fruit loading
- Character creation screen

### Phase 1.3 - Combat System
- Turn-based battle
- Basic attacks
- Devil Fruit abilities

### Phase 1.4 - Basic World
- Simple map
- Player movement
- Random encounters

---

## Troubleshooting

### "No module named pygame"
```bash
pip install pygame
```

### "ImportError: cannot import name X"
Make sure you're running from the project root directory (where main.py is)

### Game window doesn't open
Check that pygame is properly installed and no other errors in console

### FPS is low
Check console for errors. May need to close other programs.

---

## Next Steps for Development

1. **Test Current Build**
   - Run `python main.py`
   - Navigate menu with arrow keys
   - Verify FPS counter shows ~60

2. **Create Test Data**
   - Add 2-3 Devil Fruits to Database
   - Add 1-2 test enemies

3. **Begin Phase 1.2**
   - Implement character data structure
   - Create Devil Fruit loading system
   - Build character creation screen

---

## Need Help?

- Check `Documentation/Phase1_Implementation_Plan.md` for detailed implementation guide
- Review `Documentation/GameDesign.md` for game design decisions
- Check source code comments for usage examples

---

**Last Updated:** October 11, 2025  
**Current Phase:** Phase 1.1 Complete - Ready for Phase 1.2
