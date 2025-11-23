"""
Audio System
Manages background music and sound effects.
"""

import pygame
from typing import Dict, Optional
from enum import Enum


class MusicTrack(Enum):
    """Music tracks."""
    MAIN_THEME = "main_theme"
    FOOSHA_VILLAGE = "foosha_village"
    SHELL_TOWN = "shell_town"
    ORANGE_TOWN = "orange_town"
    SYRUP_VILLAGE = "syrup_village"
    BARATIE = "baratie"
    ARLONG_PARK = "arlong_park"
    LOGUETOWN = "loguetown"
    REVERSE_MOUNTAIN = "reverse_mountain"
    BATTLE_THEME = "battle"
    BOSS_BATTLE = "boss_battle"
    VICTORY = "victory"
    DEFEAT = "defeat"


class SoundEffect(Enum):
    """Sound effects."""
    ATTACK = "attack"
    DAMAGE = "damage"
    HEAL = "heal"
    LEVEL_UP = "level_up"
    ITEM_GET = "item_get"
    MENU_SELECT = "menu_select"
    MENU_BACK = "menu_back"
    EQUIP = "equip"
    DEVIL_FRUIT = "devil_fruit"
    CRITICAL = "critical"
    DODGE = "dodge"


class AudioManager:
    """Manages game audio."""

    def __init__(self):
        """Initialize audio manager."""
        self.music_enabled = True
        self.sound_enabled = True
        self.music_volume = 0.7
        self.sound_volume = 0.8

        # Current playing track
        self.current_track: Optional[MusicTrack] = None

        # Track paths (would be actual file paths in production)
        self.music_paths: Dict[MusicTrack, str] = {}
        self.sound_paths: Dict[SoundEffect, str] = {}

        # Loaded sounds cache
        self.loaded_sounds: Dict[SoundEffect, pygame.mixer.Sound] = {}

        # Initialize pygame mixer
        try:
            pygame.mixer.init()
            self.mixer_initialized = True
        except:
            print("Warning: Audio mixer failed to initialize")
            self.mixer_initialized = False

    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.mixer_initialized:
            pygame.mixer.music.set_volume(self.music_volume)

    def set_sound_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)."""
        self.sound_volume = max(0.0, min(1.0, volume))

    def play_music(self, track: MusicTrack, loop: bool = True):
        """
        Play background music.

        Args:
            track: Music track to play
            loop: Whether to loop the music
        """
        if not self.music_enabled or not self.mixer_initialized:
            return

        # Don't restart if already playing
        if self.current_track == track and pygame.mixer.music.get_busy():
            return

        # In production, this would load and play actual audio files
        # For now, we'll just track the current track
        self.current_track = track

        # Example of how it would work with actual files:
        # if track in self.music_paths:
        #     pygame.mixer.music.load(self.music_paths[track])
        #     pygame.mixer.music.set_volume(self.music_volume)
        #     pygame.mixer.music.play(-1 if loop else 0)

        print(f"Music: Playing {track.value}")

    def stop_music(self):
        """Stop background music."""
        if self.mixer_initialized:
            pygame.mixer.music.stop()
        self.current_track = None

    def pause_music(self):
        """Pause background music."""
        if self.mixer_initialized:
            pygame.mixer.music.pause()

    def unpause_music(self):
        """Unpause background music."""
        if self.mixer_initialized:
            pygame.mixer.music.unpause()

    def play_sound(self, sound: SoundEffect):
        """
        Play sound effect.

        Args:
            sound: Sound effect to play
        """
        if not self.sound_enabled or not self.mixer_initialized:
            return

        # In production, this would load and play actual sound files
        # Example:
        # if sound in self.loaded_sounds:
        #     self.loaded_sounds[sound].set_volume(self.sound_volume)
        #     self.loaded_sounds[sound].play()

        print(f"SFX: {sound.value}")

    def toggle_music(self):
        """Toggle music on/off."""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_music()

    def toggle_sound(self):
        """Toggle sound effects on/off."""
        self.sound_enabled = not self.sound_enabled

    def get_settings(self) -> Dict:
        """Get current audio settings."""
        return {
            "music_enabled": self.music_enabled,
            "sound_enabled": self.sound_enabled,
            "music_volume": self.music_volume,
            "sound_volume": self.sound_volume
        }


# Singleton instance
_audio_manager: Optional[AudioManager] = None


def get_audio_manager() -> AudioManager:
    """Get singleton audio manager instance."""
    global _audio_manager
    if _audio_manager is None:
        _audio_manager = AudioManager()
    return _audio_manager


def play_island_music(island_id: str):
    """Play music for specific island."""
    audio = get_audio_manager()

    island_music_map = {
        "foosha_village": MusicTrack.FOOSHA_VILLAGE,
        "shell_town": MusicTrack.SHELL_TOWN,
        "orange_town": MusicTrack.ORANGE_TOWN,
        "syrup_village": MusicTrack.SYRUP_VILLAGE,
        "baratie": MusicTrack.BARATIE,
        "arlong_park": MusicTrack.ARLONG_PARK,
        "loguetown": MusicTrack.LOGUETOWN,
        "reverse_mountain": MusicTrack.REVERSE_MOUNTAIN,
    }

    track = island_music_map.get(island_id, MusicTrack.MAIN_THEME)
    audio.play_music(track)


def play_battle_music(is_boss: bool = False):
    """Play battle music."""
    audio = get_audio_manager()
    track = MusicTrack.BOSS_BATTLE if is_boss else MusicTrack.BATTLE_THEME
    audio.play_music(track, loop=True)


def play_victory_music():
    """Play victory music."""
    get_audio_manager().play_music(MusicTrack.VICTORY, loop=False)


def play_sound_effect(effect: SoundEffect):
    """Play a sound effect."""
    get_audio_manager().play_sound(effect)
