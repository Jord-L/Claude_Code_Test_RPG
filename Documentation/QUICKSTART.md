# Phase 1 Part 1 - Quick Start Guide

## 🎮 Running the Game

### Option 1: Run the Test Suite (Recommended First)
```bash
cd E:\Github\OnePiece_RPG_PreGrandLine
python test_phase1_part1.py
```

This will verify all systems are working correctly before running the game.

### Option 2: Run the Game
```bash
cd E:\Github\OnePiece_RPG_PreGrandLine
python src/main.py
```

### Expected Results
- A window should open (1280x720)
- Title: "One Piece RPG: Pre-Grand Line"
- FPS counter in top-right corner
- Text: "Press ESC to exit"
- Stable 60 FPS

### Controls
- **ESC** - Exit the game
- **X button** - Close window

---

## ✅ Verification Checklist

Run through these checks to ensure everything works:

1. **Test Script Passes**
   - [ ] Run `python test_phase1_part1.py`
   - [ ] All 5 tests pass
   - [ ] No errors displayed

2. **Game Runs**
   - [ ] Window opens without errors
   - [ ] Title displays correctly
   - [ ] FPS counter shows ~60 FPS
   - [ ] No console errors

3. **Exit Works**
   - [ ] ESC key exits cleanly
   - [ ] Window X button exits cleanly
   - [ ] No pygame warnings
   - [ ] Terminal returns to prompt

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'pygame'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### "No module named 'utils'"
**Solution:** Make sure you're running from the project root
```bash
cd E:\Github\OnePiece_RPG_PreGrandLine
python src/main.py
```

### Game Window Doesn't Open
**Solution:** Check if pygame installed correctly
```bash
python -c "import pygame; print(pygame.ver)"
```

### Low FPS
- Check if other programs are using GPU
- Try running in fullscreen mode (future feature)
- Verify pygame version is 2.5.0+

---

## 📁 Files Created

### Core Files
```
src/
├── main.py                    # ✅ Entry point
├── game.py                    # ✅ Main game loop
└── utils/
    ├── constants.py           # ✅ Already existed
    ├── helpers.py             # ✅ Utility functions
    └── resource_loader.py     # ✅ Asset loading
```

### Test Files
```
test_phase1_part1.py          # ✅ Test suite
QUICKSTART.md                  # ✅ This file
```

---

## 🎯 What's Working

✅ **Game Loop**
- 60 FPS locked
- Stable delta time
- Event handling
- Update/render cycle

✅ **Window Management**
- Proper initialization
- Clean shutdown
- Title and size correct

✅ **Helper Systems**
- Math utilities
- Text rendering
- Resource loading
- File path resolution

---

## 🔜 Next Phase Preview

**Phase 1 Part 2: State Management**

Will add:
- Menu system
- State transitions
- Better UI structure
- Navigation between screens

Stay tuned!

---

## 📊 Performance Metrics

Current performance (should see):
- **FPS:** ~60 (locked)
- **Memory:** ~50-100 MB
- **CPU:** <5% (idle window)

---

## 💬 Need Help?

If you encounter issues:
1. Run the test script first
2. Check error messages in console
3. Verify pygame installation
4. Make sure you're in the project directory

---

**Ready to code? Let's build the state system next!** 🚀

---

Last Updated: October 11, 2025
