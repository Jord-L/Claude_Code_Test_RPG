"""
Save Game Manager
Handles saving and loading game save files with character-based directories.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from utils.logger import get_logger


class SaveManager:
    """Manages game save file persistence with character-based organization."""

    def __init__(self, saves_dir: str = "saves"):
        """
        Initialize save manager.

        Args:
            saves_dir: Directory where save files are stored
        """
        self.logger = get_logger()
        self.saves_dir = saves_dir
        self.logger.debug(f"Save manager initialized with directory: {saves_dir}")

        # Ensure saves directory exists
        os.makedirs(saves_dir, exist_ok=True)

    def save_game(self, character_data: Dict[str, Any], character_name: str = None, slot: int = 1) -> bool:
        """
        Save game data to a save file in character's directory.

        Args:
            character_data: Character data dictionary
            character_name: Character name (used for directory). If None, extracted from character_data
            slot: Save slot number within character's directory

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get character name
            if character_name is None:
                character_name = character_data.get('name', 'Unknown')

            # Sanitize character name for filesystem
            safe_char_name = self._sanitize_filename(character_name)

            # Create character directory
            char_dir = os.path.join(self.saves_dir, safe_char_name)
            os.makedirs(char_dir, exist_ok=True)

            # Create save data structure
            save_data = {
                "version": "2.0",  # Updated version for new format
                "timestamp": datetime.now().isoformat(),
                "slot": slot,
                "character": character_data,
                "progress": {
                    "current_location": "Tutorial Island",
                    "story_flags": [],
                    "completed_quests": [],
                    "active_quests": []
                },
                "playtime": character_data.get('playtime', 0)  # Get playtime from character data
            }

            # Generate filename
            filename = f"save_{slot}.json"
            filepath = os.path.join(char_dir, filename)

            # Write to file
            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=4)

            self.logger.info(f"Game saved for {character_name} to slot {slot}: {filepath}")
            return True

        except Exception as e:
            self.logger.error(f"Error saving game: {e}")
            return False

    def load_game(self, character_name: str = None, slot: int = 1) -> Optional[Dict[str, Any]]:
        """
        Load game data from a save file.

        Args:
            character_name: Character name (for new format). If None, tries old format
            slot: Save slot number

        Returns:
            Save data dictionary, or None if load fails
        """
        try:
            if character_name:
                # New format: saves/CharacterName/save_X.json
                safe_char_name = self._sanitize_filename(character_name)
                char_dir = os.path.join(self.saves_dir, safe_char_name)
                filepath = os.path.join(char_dir, f"save_{slot}.json")
            else:
                # Old format: saves/save_slot_X.json (backward compatibility)
                filename = self._get_save_filename(slot)
                filepath = os.path.join(self.saves_dir, filename)

            if not os.path.exists(filepath):
                self.logger.info(f"No save file found: {filepath}")
                return None

            with open(filepath, 'r') as f:
                save_data = json.load(f)

            self.logger.info(f"Game loaded from: {filepath}")
            self.logger.debug(f"Character: {save_data.get('character', {}).get('name', 'Unknown')}")
            return save_data

        except Exception as e:
            self.logger.error(f"Error loading game: {e}")
            return None

    def delete_save(self, slot: int) -> bool:
        """
        Delete a save file.

        Args:
            slot: Save slot number (1-3)

        Returns:
            True if successful, False otherwise
        """
        try:
            filename = self._get_save_filename(slot)
            filepath = os.path.join(self.saves_dir, filename)

            if os.path.exists(filepath):
                os.remove(filepath)
                self.logger.info(f"Deleted save in slot {slot}")
                return True
            else:
                self.logger.warning(f"No save file to delete in slot {slot}")
                return False

        except Exception as e:
            self.logger.error(f"Error deleting save: {e}")
            return False

    def get_all_saves(self) -> List[Dict[str, Any]]:
        """
        Get information about all save files.

        Returns:
            List of save info dictionaries
        """
        saves = []

        for slot in range(1, 4):  # Slots 1-3
            filename = self._get_save_filename(slot)
            filepath = os.path.join(self.saves_dir, filename)

            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r') as f:
                        save_data = json.load(f)

                    # Extract key info
                    character = save_data.get('character', {})
                    saves.append({
                        'slot': slot,
                        'exists': True,
                        'character_name': character.get('name', 'Unknown'),
                        'level': character.get('level', 1),
                        'class': character.get('class', 'Unknown'),
                        'timestamp': save_data.get('timestamp', 'Unknown'),
                        'playtime': save_data.get('playtime', 0),
                        'location': save_data.get('progress', {}).get('current_location', 'Unknown')
                    })
                except Exception as e:
                    self.logger.error(f"Error reading save slot {slot}: {e}")
                    saves.append({
                        'slot': slot,
                        'exists': False
                    })
            else:
                saves.append({
                    'slot': slot,
                    'exists': False
                })

        return saves

    def save_exists(self, slot: int) -> bool:
        """
        Check if a save file exists in a slot.

        Args:
            slot: Save slot number (1-3)

        Returns:
            True if save exists, False otherwise
        """
        filename = self._get_save_filename(slot)
        filepath = os.path.join(self.saves_dir, filename)
        return os.path.exists(filepath)

    def get_all_characters(self) -> List[Dict[str, Any]]:
        """
        Get all character directories with their latest save info.

        Returns:
            List of character info dictionaries
        """
        characters = []

        try:
            # Check for character directories
            if not os.path.exists(self.saves_dir):
                return characters

            for item in os.listdir(self.saves_dir):
                item_path = os.path.join(self.saves_dir, item)

                # Skip old save files (backward compatibility check)
                if item.startswith("save_slot_") and item.endswith(".json"):
                    continue

                # Check if it's a directory
                if os.path.isdir(item_path):
                    # Get the latest save from this character's directory
                    latest_save = self.get_character_latest_save(item)

                    if latest_save:
                        char_data = latest_save.get('character', {})
                        playtime_seconds = latest_save.get('playtime', 0)

                        # Format playtime
                        hours = int(playtime_seconds // 3600)
                        minutes = int((playtime_seconds % 3600) // 60)

                        characters.append({
                            'character_name': char_data.get('name', item),
                            'directory_name': item,
                            'level': char_data.get('level', 1),
                            'playtime_seconds': playtime_seconds,
                            'playtime_formatted': f"{hours}h {minutes}m",
                            'timestamp': latest_save.get('timestamp', 'Unknown'),
                            'latest_slot': latest_save.get('slot', 1)
                        })

        except Exception as e:
            self.logger.error(f"Error getting characters: {e}")

        return characters

    def get_character_latest_save(self, character_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the most recent save for a character.

        Args:
            character_name: Character name (directory name)

        Returns:
            Save data dictionary or None
        """
        try:
            safe_char_name = self._sanitize_filename(character_name)
            char_dir = os.path.join(self.saves_dir, safe_char_name)

            if not os.path.exists(char_dir) or not os.path.isdir(char_dir):
                return None

            # Find all save files in character directory
            latest_save = None
            latest_time = None

            for filename in os.listdir(char_dir):
                if filename.startswith("save_") and filename.endswith(".json"):
                    filepath = os.path.join(char_dir, filename)

                    try:
                        mtime = os.path.getmtime(filepath)
                        if latest_time is None or mtime > latest_time:
                            with open(filepath, 'r') as f:
                                latest_save = json.load(f)
                            latest_time = mtime
                    except Exception as e:
                        self.logger.error(f"Error reading {filepath}: {e}")

            return latest_save

        except Exception as e:
            self.logger.error(f"Error getting latest save for {character_name}: {e}")
            return None

    def get_character_saves(self, character_name: str) -> List[Dict[str, Any]]:
        """
        Get all saves for a specific character.

        Args:
            character_name: Character name (directory name)

        Returns:
            List of save info dictionaries
        """
        saves = []

        try:
            safe_char_name = self._sanitize_filename(character_name)
            char_dir = os.path.join(self.saves_dir, safe_char_name)

            if not os.path.exists(char_dir) or not os.path.isdir(char_dir):
                return saves

            for filename in os.listdir(char_dir):
                if filename.startswith("save_") and filename.endswith(".json"):
                    filepath = os.path.join(char_dir, filename)

                    try:
                        with open(filepath, 'r') as f:
                            save_data = json.load(f)

                        # Extract slot number from filename
                        slot = int(filename.replace("save_", "").replace(".json", ""))

                        saves.append({
                            'slot': slot,
                            'filepath': filepath,
                            'data': save_data
                        })
                    except Exception as e:
                        self.logger.error(f"Error reading {filepath}: {e}")

        except Exception as e:
            self.logger.error(f"Error getting saves for {character_name}: {e}")

        return saves

    def _sanitize_filename(self, name: str) -> str:
        """
        Sanitize a name for use as a filename/directory.

        Args:
            name: Name to sanitize

        Returns:
            Sanitized name safe for filesystem
        """
        # Remove or replace unsafe characters
        unsafe_chars = '<>:"/\\|?*'
        safe_name = name
        for char in unsafe_chars:
            safe_name = safe_name.replace(char, '_')

        # Limit length and strip whitespace
        safe_name = safe_name.strip()[:50]

        return safe_name if safe_name else "Character"

    def _get_save_filename(self, slot: int) -> str:
        """
        Get the filename for a save slot (old format).

        Args:
            slot: Save slot number

        Returns:
            Filename string
        """
        return f"save_slot_{slot}.json"

    def get_latest_save_slot(self) -> Optional[int]:
        """
        Get the slot number of the most recently saved game.

        Returns:
            Slot number, or None if no saves exist
        """
        latest_slot = None
        latest_time = None

        for slot in range(1, 4):
            filename = self._get_save_filename(slot)
            filepath = os.path.join(self.saves_dir, filename)

            if os.path.exists(filepath):
                try:
                    mtime = os.path.getmtime(filepath)
                    if latest_time is None or mtime > latest_time:
                        latest_time = mtime
                        latest_slot = slot
                except Exception as e:
                    self.logger.error(f"Error checking save slot {slot}: {e}")

        return latest_slot


# Global save manager instance
_save_manager = None


def get_save_manager() -> SaveManager:
    """
    Get the global save manager instance.

    Returns:
        SaveManager instance
    """
    global _save_manager
    if _save_manager is None:
        _save_manager = SaveManager()
    return _save_manager
