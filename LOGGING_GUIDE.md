# Logging System Guide

## Overview
The game now has a comprehensive logging system that logs to both console and files. This makes debugging and tracking issues much easier during development.

## Features
- **Console Output**: Shows INFO level and above in the console
- **Session Log Files**: Detailed DEBUG level logs for each game session
- **General Log File**: Persistent log across all sessions
- **Automatic Timestamping**: All log entries include timestamps
- **Exception Tracking**: Automatic traceback logging for errors
- **Multiple Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

## Log Files Location
All log files are stored in: `E:\Github\OnePiece_RPG_PreGrandLine\logs\`

### Types of Log Files:
1. **Session Logs**: `game_YYYYMMDD_HHMMSS.log`
   - One file per game session
   - Contains detailed DEBUG level information
   - Useful for tracking specific issues

2. **General Log**: `game_general.log`
   - Persistent across all sessions
   - Contains INFO level and above
   - Good for spotting patterns over time

## Using the Logger in Your Code

### Basic Usage:
```python
from utils.logger import get_logger

# In your class __init__
self.logger = get_logger()

# Log messages
self.logger.debug("Detailed debug information")
self.logger.info("General information")
self.logger.warning("Warning message")
self.logger.error("Error message")
self.logger.critical("Critical error!")
```

### Exception Logging:
```python
try:
    # Some code that might fail
    result = risky_operation()
except Exception as e:
    # Logs the error AND the full traceback
    self.logger.exception(f"Failed to do operation: {e}")
```

### Formatting Tips:
```python
# Section headers
self.logger.section("INITIALIZATION")

# Separators
self.logger.separator()  # Default "=" * 70
self.logger.separator("-", 50)  # Custom character and length

# Structured information
self.logger.info(f"Loading {item_name} with ID: {item_id}")
self.logger.debug(f"Parameters: {parameters}")
```

## Log Levels Explained

### DEBUG (Most Verbose)
- Detailed diagnostic information
- Function entry/exit points
- Variable states
- Only appears in log files, not console

```python
self.logger.debug("Entering _initialize_weapons()")
self.logger.debug(f"Loaded {len(items)} items from database")
```

### INFO (Standard)
- General informational messages
- Major events and state changes
- Appears in both console and files

```python
self.logger.info("Game initialized successfully")
self.logger.info("Player created: Captain Luffy")
```

### WARNING
- Something unexpected but not critical
- Deprecated features
- Recoverable errors

```python
self.logger.warning("Save file not found, using defaults")
self.logger.warning("FPS dropped below 30")
```

### ERROR
- Errors that affect functionality
- But don't crash the game
- Use with exception handling

```python
self.logger.error(f"Failed to load texture: {filename}")
self.logger.error("Combat calculation returned invalid value")
```

### CRITICAL
- Severe errors that may crash the game
- Should be rare
- Usually followed by exception

```python
self.logger.critical("Database corruption detected!")
self.logger.critical("Unable to initialize graphics system")
```

## Quick Examples

### Class with Logging:
```python
from utils.logger import get_logger

class MyGameSystem:
    def __init__(self):
        self.logger = get_logger()
        self.logger.debug("MyGameSystem initializing...")
        
        try:
            self._load_data()
            self.logger.info("MyGameSystem initialized successfully")
        except Exception as e:
            self.logger.exception("Failed to initialize MyGameSystem")
            raise
    
    def _load_data(self):
        self.logger.debug("Loading data from files...")
        # Load data
        self.logger.info("Data loaded: 100 items")
```

### Function with Logging:
```python
from utils.logger import get_logger

def process_combat_turn(attacker, defender):
    logger = get_logger()
    logger.debug(f"Combat turn: {attacker.name} vs {defender.name}")
    
    damage = calculate_damage(attacker, defender)
    logger.info(f"{attacker.name} deals {damage} damage to {defender.name}")
    
    if defender.hp <= 0:
        logger.info(f"{defender.name} has been defeated!")
```

## Debugging with Logs

### When the Game Crashes:
1. Open the latest session log file in `logs/`
2. Look for ERROR or CRITICAL messages
3. Check the traceback for the exact line that failed

### Finding Performance Issues:
1. Look for WARNING messages about FPS
2. Check how long operations take using DEBUG logs
3. Use timestamps to identify slow sections

### Tracking State Changes:
1. Search for "State:" in the logs
2. See all state transitions
3. Identify where unexpected transitions occur

## In-Game Debug Keys

Press these keys while the game is running:

- **F3**: Toggle FPS display
- **F12**: Dump debug info to log (current state, FPS, etc.)

## Best Practices

### DO:
✅ Log important events (state changes, player actions, errors)
✅ Use appropriate log levels
✅ Include context in messages (IDs, names, values)
✅ Use exception() for caught exceptions
✅ Log before and after critical operations

### DON'T:
❌ Log every frame (too verbose)
❌ Log sensitive information (passwords, etc.)
❌ Use print() instead of logger
❌ Log huge data structures
❌ Ignore exceptions without logging

## Example Log Output

```
[2025-11-03 10:30:15] [INFO    ] [OnePieceRPG] ======================================================================
[2025-11-03 10:30:15] [INFO    ] [OnePieceRPG]  ONE PIECE RPG - PRE-GRAND LINE
[2025-11-03 10:30:15] [INFO    ] [OnePieceRPG] ======================================================================
[2025-11-03 10:30:15] [INFO    ] [OnePieceRPG] Version: 0.1.0-alpha (Phase 1 Development)
[2025-11-03 10:30:15] [DEBUG   ] [OnePieceRPG] Initializing Game class...
[2025-11-03 10:30:15] [DEBUG   ] [OnePieceRPG] Initializing Pygame...
[2025-11-03 10:30:15] [INFO    ] [OnePieceRPG] Game window created: One Piece RPG: Pre-Grand Line
[2025-11-03 10:30:15] [INFO    ] [OnePieceRPG] Resolution: 1280x720
[2025-11-03 10:30:15] [DEBUG   ] [OnePieceRPG] Registering state: menu -> MenuState
[2025-11-03 10:30:15] [INFO    ] [OnePieceRPG] Starting with main menu state...
[2025-11-03 10:30:15] [INFO    ] [OnePieceRPG] Pushed state: menu (Stack depth: 1)
[2025-11-03 10:30:15] [INFO    ] [OnePieceRPG] Entering main game loop
```

## Troubleshooting

### Problem: No log files created
- Check that the `logs/` directory exists
- Make sure you have write permissions
- Look for error messages in the console

### Problem: Too much output
- Change console_level in main.py:
  ```python
  logger = init_logger(console_level=logging.WARNING)  # Less verbose
  ```

### Problem: Not enough detail
- Check the session log file (always has DEBUG level)
- Add more debug statements to your code

## Quick Reference Card

```
DEBUG   - Detailed diagnostics (file only)
INFO    - General information (console + file)
WARNING - Something unexpected (console + file)
ERROR   - Functionality affected (console + file)
CRITICAL- May crash (console + file)

Log files: logs/game_YYYYMMDD_HHMMSS.log
General log: logs/game_general.log

Press F12 in-game for debug dump
```

---

**Remember**: Good logging is like having a flight recorder - when something goes wrong, you'll know exactly what happened! 🎯
