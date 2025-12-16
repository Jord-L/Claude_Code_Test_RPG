"""
Save Game Manager
Handles saving and loading game save files.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from utils.logger import get_logger


class SaveManager:
    """Manages game save file persistence."""

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

    def save_game(self, character_data: Dict[str, Any], slot: int = 1) -> bool:
        """
        Save game data to a save file.

        Args:
            character_data: Character data dictionary
            slot: Save slot number (1-3)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create save data structure
            save_data = {
                "version": "1.0",
                "timestamp": datetime.now().isoformat(),
                "slot": slot,
                "character": character_data,
                "progress": {
                    "current_location": "Tutorial Island",
                    "story_flags": [],
                    "completed_quests": [],
                    "active_quests": []
                },
                "playtime": 0  # In seconds
            }

            # Generate filename
            filename = self._get_save_filename(slot)
            filepath = os.path.join(self.saves_dir, filename)

            # Write to file
            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=4)

            self.logger.info(f"Game saved to slot {slot}: {filepath}")
            self.logger.debug(f"Character: {character_data.get('name', 'Unknown')}")
            return True

        except Exception as e:
            self.logger.error(f"Error saving game: {e}")
            return False

    def load_game(self, slot: int = 1) -> Optional[Dict[str, Any]]:
        """
        Load game data from a save file.

        Args:
            slot: Save slot number (1-3)

        Returns:
            Save data dictionary, or None if load fails
        """
        try:
            filename = self._get_save_filename(slot)
            filepath = os.path.join(self.saves_dir, filename)

            if not os.path.exists(filepath):
                self.logger.info(f"No save file found in slot {slot}")
                return None

            with open(filepath, 'r') as f:
                save_data = json.load(f)

            self.logger.info(f"Game loaded from slot {slot}: {filepath}")
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

    def _get_save_filename(self, slot: int) -> str:
        """
        Get the filename for a save slot.

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
