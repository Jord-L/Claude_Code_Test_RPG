"""
Dialogue System
Manages conversations, dialogue trees, and NPC interactions.
"""

from typing import List, Dict, Optional, Callable
from dataclasses import dataclass


@dataclass
class DialogueLine:
    """Single line of dialogue."""
    speaker: str
    text: str
    choices: List[str] = None  # If None, advance automatically
    next_dialogue_id: Optional[str] = None


class Dialogue:
    """Complete dialogue sequence."""

    def __init__(self, dialogue_id: str):
        """Initialize dialogue."""
        self.dialogue_id = dialogue_id
        self.lines: List[DialogueLine] = []
        self.current_index = 0

    def add_line(self, speaker: str, text: str, choices: List[str] = None, next_id: Optional[str] = None):
        """Add dialogue line."""
        self.lines.append(DialogueLine(speaker, text, choices, next_id))

    def get_current_line(self) -> Optional[DialogueLine]:
        """Get current dialogue line."""
        if 0 <= self.current_index < len(self.lines):
            return self.lines[self.current_index]
        return None

    def advance(self) -> bool:
        """Advance to next line. Returns False if dialogue ended."""
        self.current_index += 1
        return self.current_index < len(self.lines)

    def reset(self):
        """Reset dialogue to beginning."""
        self.current_index = 0

    def is_finished(self) -> bool:
        """Check if dialogue is complete."""
        return self.current_index >= len(self.lines)


class DialogueManager:
    """Manages all game dialogues."""

    def __init__(self):
        """Initialize dialogue manager."""
        self.dialogues: Dict[str, Dialogue] = {}
        self.current_dialogue: Optional[Dialogue] = None
        self.on_dialogue_end: Optional[Callable] = None

    def register_dialogue(self, dialogue: Dialogue):
        """Register a dialogue."""
        self.dialogues[dialogue.dialogue_id] = dialogue

    def start_dialogue(self, dialogue_id: str) -> bool:
        """Start a dialogue sequence."""
        if dialogue_id in self.dialogues:
            self.current_dialogue = self.dialogues[dialogue_id]
            self.current_dialogue.reset()
            return True
        return False

    def advance_dialogue(self) -> bool:
        """Advance current dialogue. Returns False if ended."""
        if self.current_dialogue:
            if not self.current_dialogue.advance():
                self.end_dialogue()
                return False
            return True
        return False

    def end_dialogue(self):
        """End current dialogue."""
        self.current_dialogue = None
        if self.on_dialogue_end:
            self.on_dialogue_end()

    def get_current_line(self) -> Optional[DialogueLine]:
        """Get current dialogue line."""
        if self.current_dialogue:
            return self.current_dialogue.get_current_line()
        return None

    def is_active(self) -> bool:
        """Check if dialogue is active."""
        return self.current_dialogue is not None


def create_default_dialogues() -> DialogueManager:
    """Create default game dialogues."""
    manager = DialogueManager()

    # Generic greetings
    generic = Dialogue("generic_greeting")
    generic.add_line("Villager", "Hello there, traveler!")
    generic.add_line("Villager", "Welcome to our island.")
    manager.register_dialogue(generic)

    # Mayor greeting
    mayor = Dialogue("mayor_greeting")
    mayor.add_line("Mayor", "Welcome to Foosha Village!")
    mayor.add_line("Mayor", "We're a peaceful village, but watch out for bandits in the forest.")
    manager.register_dialogue(mayor)

    # Mira greeting
    makino = Dialogue("makino_greeting")
    makino.add_line("Mira", "Welcome to my bar! Can I get you something?")
    makino.add_line("Mira", "Alex used to come here all the time as a kid.")
    manager.register_dialogue(makino)

    return manager
