# Phase 2 Test Suite

Comprehensive testing for all Phase 2 systems with detailed logging.

## Test Files

### 1. `test_imports.py` - Import Tests
**Run this first!** Tests that all modules can be imported.

```bash
python test_imports.py
```

**What it tests:**
- All entity classes (Character, Player, Enemy, NPC)
- All world systems (Map, Island, Camera, etc.)
- All game systems (Party, Inventory, Equipment, etc.)
- All UI components
- All combat systems

**Output:**
- Console output showing each import
- Detailed log in `test_logs/` directory
- Clear pass/fail for each module

### 2. `test_phase2.py` - Comprehensive System Tests
**Run after imports pass.** Tests all systems with real data.

```bash
python test_phase2.py
```

**What it tests:**

1. **Party System**
   - Create party manager
   - Add crew members
   - Check active/reserve slots

2. **Inventory & Equipment**
   - Create inventory
   - Load items from database
   - Add items to inventory
   - Initialize equipment slots

3. **Island System**
   - Create all 8 islands
   - Register with island manager
   - Check island data (NPCs, connections, maps)

4. **Dialogue System**
   - Create dialogue manager
   - Load default dialogues
   - Test dialogue playback

5. **Shop System**
   - Create all shops
   - Test buying items
   - Check inventory integration

6. **Quest System**
   - Load default quests
   - Start a quest
   - Check objectives

7. **Ship System**
   - Create player ship
   - Test upgrades
   - Check ship stats

8. **Devil Fruit System**
   - Load all devil fruits
   - Check abilities
   - Test mastery system

9. **Advanced Combat**
   - Test combo system
   - Test critical hits
   - Test status effects

10. **Haki System**
    - Create Haki user
    - Unlock Haki types
    - Test Haki abilities

11. **Audio System**
    - Initialize audio manager
    - Test music playback
    - Test sound effects

12. **NPC System**
    - Create NPCs
    - Test interactions
    - Check range detection

**Output:**
- Detailed test results for each system
- Pass/fail summary
- Complete log file in `test_logs/`

## Log Files

All tests create detailed log files in the `test_logs/` directory:

- **Session logs**: `game_YYYYMMDD_HHMMSS.log` - Full details of each test run
- **General log**: `game_general.log` - Cumulative log of all test runs

## Quick Start

```bash
# Step 1: Test imports
python test_imports.py

# Step 2: If imports pass, run full tests
python test_phase2.py

# Step 3: Check logs for details
cat test_logs/game_*.log
```

## Interpreting Results

### Success
```
✓ PASSED: System Name
```
The system works correctly.

### Failure
```
✗ FAILED: System Name - Error message
```
Check the log file for full traceback.

## Common Issues

### Import Errors
- **Problem**: Module not found
- **Solution**: Check that `src/` directory structure is correct

### Missing Dependencies
- **Problem**: ImportError for pygame, etc.
- **Solution**: `pip install pygame`

### Logger Errors
- **Problem**: `get_logger()` errors
- **Solution**: Check that logger is initialized correctly

## After Testing

If all tests pass:
1. Run the main game: `python main_debug.py`
2. Test in-game features manually
3. Check for any runtime errors

If tests fail:
1. Check the log file for detailed errors
2. Fix the failing system
3. Re-run tests
4. Repeat until all pass

## Test Coverage

**Phase 2 Systems:**
- [x] Week 1-2: Art Asset Integration
- [x] Week 3: Party System
- [x] Week 4: Inventory & Equipment
- [x] Week 5-6: 8 Islands
- [x] Week 7: NPC System
- [x] Week 8: Dialogue System
- [x] Week 9: Shop System
- [x] Week 10: Quest System
- [x] Week 11: Ship System
- [x] Week 12: Extended Devil Fruits
- [x] Week 13: Advanced Combat
- [x] Week 14: Haki System
- [x] Week 15: Sound & Music

**Total:** 15 weeks of systems tested! 🎉
