"""
Quest System
Manages quests, objectives, and rewards.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum


class QuestStatus(Enum):
    """Quest status."""
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class QuestObjective:
    """Single quest objective."""
    description: str
    target_type: str  # defeat_enemy, collect_item, talk_to_npc, visit_location
    target_id: str
    required_count: int = 1
    current_count: int = 0

    def is_complete(self) -> bool:
        """Check if objective is complete."""
        return self.current_count >= self.required_count

    def progress(self, amount: int = 1):
        """Progress objective."""
        self.current_count = min(self.current_count + amount, self.required_count)


@dataclass
class Quest:
    """Quest with objectives and rewards."""
    quest_id: str
    name: str
    description: str
    objectives: List[QuestObjective] = field(default_factory=list)
    status: QuestStatus = QuestStatus.NOT_STARTED

    # Rewards
    exp_reward: int = 0
    berries_reward: int = 0
    item_rewards: List[str] = field(default_factory=list)

    # Requirements
    required_level: int = 1
    required_quests: List[str] = field(default_factory=list)

    def can_start(self, player_level: int, completed_quests: List[str]) -> bool:
        """Check if quest can be started."""
        if player_level < self.required_level:
            return False

        for req_quest in self.required_quests:
            if req_quest not in completed_quests:
                return False

        return True

    def is_complete(self) -> bool:
        """Check if all objectives are complete."""
        return all(obj.is_complete() for obj in self.objectives)

    def get_progress(self) -> str:
        """Get quest progress string."""
        completed = sum(1 for obj in self.objectives if obj.is_complete())
        return f"{completed}/{len(self.objectives)} objectives complete"


class QuestManager:
    """Manages all quests."""

    def __init__(self):
        """Initialize quest manager."""
        self.quests: Dict[str, Quest] = {}
        self.active_quests: List[str] = []
        self.completed_quests: List[str] = []

    def register_quest(self, quest: Quest):
        """Register a quest."""
        self.quests[quest.quest_id] = quest

    def start_quest(self, quest_id: str, player_level: int) -> bool:
        """Start a quest."""
        if quest_id not in self.quests:
            return False

        quest = self.quests[quest_id]

        if not quest.can_start(player_level, self.completed_quests):
            return False

        if quest_id not in self.active_quests:
            self.active_quests.append(quest_id)
            quest.status = QuestStatus.ACTIVE
            print(f"Quest started: {quest.name}")
            return True

        return False

    def complete_quest(self, quest_id: str) -> Dict:
        """Complete a quest and get rewards."""
        if quest_id not in self.quests:
            return {"success": False}

        quest = self.quests[quest_id]

        if not quest.is_complete():
            return {"success": False, "message": "Quest objectives not complete"}

        # Mark complete
        quest.status = QuestStatus.COMPLETED
        if quest_id in self.active_quests:
            self.active_quests.remove(quest_id)
        self.completed_quests.append(quest_id)

        return {
            "success": True,
            "exp": quest.exp_reward,
            "berries": quest.berries_reward,
            "items": quest.item_rewards
        }

    def update_objective(self, target_type: str, target_id: str, amount: int = 1):
        """Update quest objectives."""
        for quest_id in self.active_quests:
            quest = self.quests[quest_id]
            for obj in quest.objectives:
                if obj.target_type == target_type and obj.target_id == target_id:
                    obj.progress(amount)
                    print(f"Quest objective progress: {obj.description} ({obj.current_count}/{obj.required_count})")

    def get_active_quests(self) -> List[Quest]:
        """Get list of active quests."""
        return [self.quests[qid] for qid in self.active_quests if qid in self.quests]


def create_default_quests() -> QuestManager:
    """Create default game quests."""
    manager = QuestManager()

    # Recruit Kane
    recruit_zoro = Quest(
        "recruit_zoro",
        "The Demon Blade",
        "Help Kane and recruit him to your crew."
    )
    recruit_zoro.objectives.append(QuestObjective(
        "Defeat Captain Morgan's forces",
        "defeat_enemy",
        "marine_soldier",
        5
    ))
    recruit_zoro.objectives.append(QuestObjective(
        "Talk to Kane",
        "talk_to_npc",
        "zoro",
        1
    ))
    recruit_zoro.exp_reward = 500
    recruit_zoro.berries_reward = 1000
    manager.register_quest(recruit_zoro)

    # Save Orange Town
    save_orange = Quest(
        "save_orange_town",
        "Defeat Buggy the Clown",
        "Save Orange Town from Buggy's pirate crew."
    )
    save_orange.objectives.append(QuestObjective(
        "Defeat Buggy Pirates",
        "defeat_enemy",
        "pirate",
        10
    ))
    save_orange.exp_reward = 1000
    save_orange.berries_reward = 5000
    save_orange.required_level = 5
    manager.register_quest(save_orange)

    return manager
