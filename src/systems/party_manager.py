"""
Party Management System
Handles party composition, member management, and formation switching.
"""

from typing import List, Optional, Dict
from entities.character import Character
from entities.player import Player
from utils.logger import get_logger

logger = get_logger(__name__)


class PartyFormation:
    """Represents different party formations for strategic positioning."""
    BALANCED = "balanced"
    OFFENSIVE = "offensive"
    DEFENSIVE = "defensive"
    SPEED = "speed"


class CrewMember(Character):
    """
    Extended Character class for crew members with additional features.
    """

    def __init__(self, name: str, level: int = 1, role: str = "Fighter"):
        """
        Initialize crew member.

        Args:
            name: Character name
            level: Starting level
            role: Combat role (Fighter, Support, Tank, etc.)
        """
        super().__init__(name, level)

        # Crew-specific attributes
        self.role = role  # Fighter, Support, Tank, Sniper, Navigator, etc.
        self.loyalty = 100  # 0-100, affects combat performance
        self.join_chapter = 1  # Chapter when they joined

        # One Piece flavor
        self.dream = ""  # Character's personal dream
        self.bounty = 0  # Individual bounty
        self.epithet = ""  # "Straw Hat", "Pirate Hunter", etc.

        # Recruitment
        self.is_recruitable = True
        self.recruitment_requirements = {}

        # Personal quest
        self.personal_quest_id = None
        self.personal_quest_complete = False

    def set_dream(self, dream: str):
        """Set character's personal dream."""
        self.dream = dream

    def set_epithet(self, epithet: str):
        """Set character's epithet/title."""
        self.epithet = epithet

    def modify_loyalty(self, amount: int):
        """
        Modify loyalty value.

        Args:
            amount: Amount to change (+/-)
        """
        self.loyalty = max(0, min(100, self.loyalty + amount))

        if self.loyalty < 50:
            logger.warning(f"{self.name}'s loyalty is low ({self.loyalty})!")

    def get_loyalty_bonus(self) -> float:
        """
        Get combat stat multiplier based on loyalty.

        Returns:
            Multiplier (0.8 to 1.2)
        """
        # 50 loyalty = 1.0x, 100 loyalty = 1.2x, 0 loyalty = 0.8x
        return 0.8 + (self.loyalty / 100) * 0.4

    def __repr__(self) -> str:
        """String representation."""
        return f"CrewMember({self.name}, Lv.{self.level}, {self.role})"


class PartyManager:
    """
    Manages party composition with active and reserve members.
    One Piece themed - captain + crew management.
    """

    MAX_ACTIVE = 4  # Maximum active party members
    MAX_RESERVE = 6  # Maximum reserve members
    MAX_TOTAL = 10  # Total crew size

    def __init__(self, captain: Player):
        """
        Initialize party manager.

        Args:
            captain: Player character (captain)
        """
        self.captain = captain

        # Party composition
        self.active_party: List[Character] = [captain]  # Captain always in active
        self.reserve_party: List[CrewMember] = []

        # Formation
        self.current_formation = PartyFormation.BALANCED

        # Statistics
        self.total_recruited = 0
        self.members_lost = 0

        logger.info(f"Party Manager initialized with captain: {captain.name}")

    # Core party management

    def add_member(self, member: CrewMember, to_active: bool = True) -> bool:
        """
        Add a new crew member to the party.

        Args:
            member: Crew member to add
            to_active: Whether to add to active party (if space available)

        Returns:
            True if successfully added
        """
        # Check total party size
        total_size = len(self.active_party) + len(self.reserve_party)
        if total_size >= self.MAX_TOTAL:
            logger.warning(f"Party is full! Cannot add {member.name}")
            return False

        # Try to add to active party
        if to_active and len(self.active_party) < self.MAX_ACTIVE:
            self.active_party.append(member)
            logger.info(f"{member.name} joined the active party!")

        # Otherwise add to reserve
        elif len(self.reserve_party) < self.MAX_RESERVE:
            self.reserve_party.append(member)
            logger.info(f"{member.name} joined the reserve party")

        else:
            logger.warning(f"No space for {member.name}!")
            return False

        self.total_recruited += 1
        return True

    def remove_member(self, member: Character) -> bool:
        """
        Remove a member from the party.

        Args:
            member: Member to remove

        Returns:
            True if successfully removed
        """
        # Cannot remove captain
        if member == self.captain:
            logger.warning("Cannot remove the captain!")
            return False

        # Remove from active
        if member in self.active_party:
            self.active_party.remove(member)
            logger.info(f"{member.name} left the active party")
            self.members_lost += 1
            return True

        # Remove from reserve
        if member in self.reserve_party:
            self.reserve_party.remove(member)
            logger.info(f"{member.name} left the reserve party")
            self.members_lost += 1
            return True

        return False

    def swap_members(self, active_member: Character, reserve_member: CrewMember) -> bool:
        """
        Swap an active member with a reserve member.

        Args:
            active_member: Member currently in active party
            reserve_member: Member currently in reserve

        Returns:
            True if swap successful
        """
        # Cannot swap captain
        if active_member == self.captain:
            logger.warning("Cannot remove captain from active party!")
            return False

        # Verify members are in correct parties
        if active_member not in self.active_party:
            logger.warning(f"{active_member.name} is not in active party!")
            return False

        if reserve_member not in self.reserve_party:
            logger.warning(f"{reserve_member.name} is not in reserve party!")
            return False

        # Perform swap
        self.active_party.remove(active_member)
        self.reserve_party.remove(reserve_member)

        self.active_party.append(reserve_member)
        self.reserve_party.append(active_member)

        logger.info(f"Swapped {active_member.name} ↔ {reserve_member.name}")
        return True

    def move_to_active(self, member: CrewMember) -> bool:
        """
        Move a reserve member to active party.

        Args:
            member: Reserve member to activate

        Returns:
            True if successful
        """
        if member not in self.reserve_party:
            return False

        if len(self.active_party) >= self.MAX_ACTIVE:
            logger.warning("Active party is full!")
            return False

        self.reserve_party.remove(member)
        self.active_party.append(member)
        logger.info(f"{member.name} moved to active party")
        return True

    def move_to_reserve(self, member: Character) -> bool:
        """
        Move an active member to reserve.

        Args:
            member: Active member to move to reserve

        Returns:
            True if successful
        """
        # Cannot move captain
        if member == self.captain:
            return False

        if member not in self.active_party:
            return False

        if len(self.reserve_party) >= self.MAX_RESERVE:
            logger.warning("Reserve party is full!")
            return False

        self.active_party.remove(member)
        self.reserve_party.append(member)
        logger.info(f"{member.name} moved to reserve")
        return True

    # Party queries

    def get_active_party(self) -> List[Character]:
        """Get list of active party members."""
        return self.active_party.copy()

    def get_reserve_party(self) -> List[CrewMember]:
        """Get list of reserve party members."""
        return self.reserve_party.copy()

    def get_all_members(self) -> List[Character]:
        """Get all party members (active + reserve)."""
        return self.active_party + self.reserve_party

    def get_member_by_name(self, name: str) -> Optional[Character]:
        """
        Find a member by name.

        Args:
            name: Member name

        Returns:
            Member or None if not found
        """
        for member in self.get_all_members():
            if member.name.lower() == name.lower():
                return member
        return None

    def get_active_count(self) -> int:
        """Get number of active members."""
        return len(self.active_party)

    def get_reserve_count(self) -> int:
        """Get number of reserve members."""
        return len(self.reserve_party)

    def get_total_count(self) -> int:
        """Get total party size."""
        return len(self.active_party) + len(self.reserve_party)

    def has_space_active(self) -> bool:
        """Check if there's space in active party."""
        return len(self.active_party) < self.MAX_ACTIVE

    def has_space_reserve(self) -> bool:
        """Check if there's space in reserve."""
        return len(self.reserve_party) < self.MAX_RESERVE

    def has_space_total(self) -> bool:
        """Check if there's space in the party."""
        return self.get_total_count() < self.MAX_TOTAL

    def is_in_party(self, member: Character) -> bool:
        """Check if member is in the party (active or reserve)."""
        return member in self.active_party or member in self.reserve_party

    def is_in_active(self, member: Character) -> bool:
        """Check if member is in active party."""
        return member in self.active_party

    # Party management

    def set_formation(self, formation: str):
        """
        Set party formation.

        Args:
            formation: Formation type
        """
        self.current_formation = formation
        logger.info(f"Formation changed to: {formation}")

    def heal_all_members(self, amount: Optional[int] = None):
        """
        Heal all party members.

        Args:
            amount: Amount to heal (None = full heal)
        """
        for member in self.get_all_members():
            if amount is None:
                member.current_hp = member.max_hp
                member.current_ap = member.max_ap
            else:
                member.heal(amount)

    def revive_fallen_members(self):
        """Revive all fallen party members (like at an inn)."""
        for member in self.get_all_members():
            if not member.is_alive:
                member.revive()

    def get_party_level_average(self) -> int:
        """Get average level of active party."""
        if not self.active_party:
            return 1

        total_level = sum(m.level for m in self.active_party)
        return total_level // len(self.active_party)

    def get_strongest_member(self) -> Optional[Character]:
        """Get member with highest attack power."""
        if not self.active_party:
            return None

        return max(self.active_party, key=lambda m: m.stats.strength.value)

    def get_fastest_member(self) -> Optional[Character]:
        """Get member with highest speed."""
        if not self.active_party:
            return None

        return max(self.active_party, key=lambda m: m.stats.speed.value)

    # Save/Load support

    def to_dict(self) -> Dict:
        """
        Serialize party data for saving.

        Returns:
            Dictionary of party data
        """
        return {
            "active_party": [m.name for m in self.active_party],
            "reserve_party": [m.name for m in self.reserve_party],
            "current_formation": self.current_formation,
            "total_recruited": self.total_recruited,
            "members_lost": self.members_lost
        }

    def __repr__(self) -> str:
        """String representation."""
        return f"PartyManager(Active: {len(self.active_party)}, Reserve: {len(self.reserve_party)})"


class PartyFactory:
    """Factory for creating crew members with proper stats and roles."""

    @staticmethod
    def create_fighter(name: str, level: int = 1, epithet: str = "") -> CrewMember:
        """Create a fighter-type crew member."""
        member = CrewMember(name, level, "Fighter")
        member.set_epithet(epithet)

        # Fighter stats: High STR, DEF
        member.stats.strength.set_base(15)
        member.stats.defense.set_base(12)
        member.stats.speed.set_base(8)
        member.stats.skill.set_base(10)

        return member

    @staticmethod
    def create_sniper(name: str, level: int = 1, epithet: str = "") -> CrewMember:
        """Create a sniper-type crew member."""
        member = CrewMember(name, level, "Sniper")
        member.set_epithet(epithet)

        # Sniper stats: High SKILL, SPD
        member.stats.strength.set_base(10)
        member.stats.defense.set_base(8)
        member.stats.speed.set_base(12)
        member.stats.skill.set_base(15)

        return member

    @staticmethod
    def create_navigator(name: str, level: int = 1, epithet: str = "") -> CrewMember:
        """Create a navigator-type crew member."""
        member = CrewMember(name, level, "Navigator")
        member.set_epithet(epithet)

        # Navigator stats: Balanced with high WILL
        member.stats.strength.set_base(8)
        member.stats.defense.set_base(9)
        member.stats.speed.set_base(11)
        member.stats.skill.set_base(12)
        member.stats.will.set_base(15)

        return member

    @staticmethod
    def create_cook(name: str, level: int = 1, epithet: str = "") -> CrewMember:
        """Create a cook-type crew member."""
        member = CrewMember(name, level, "Cook")
        member.set_epithet(epithet)

        # Cook stats: High STR, DEF (kicks!)
        member.stats.strength.set_base(14)
        member.stats.defense.set_base(11)
        member.stats.speed.set_base(13)
        member.stats.skill.set_base(9)

        return member

    @staticmethod
    def create_doctor(name: str, level: int = 1, epithet: str = "") -> CrewMember:
        """Create a doctor-type crew member."""
        member = CrewMember(name, level, "Doctor")
        member.set_epithet(epithet)

        # Doctor stats: Support-oriented
        member.stats.strength.set_base(9)
        member.stats.defense.set_base(10)
        member.stats.speed.set_base(10)
        member.stats.skill.set_base(14)
        member.stats.will.set_base(12)

        return member

    @staticmethod
    def create_archaeologist(name: str, level: int = 1, epithet: str = "") -> CrewMember:
        """Create an archaeologist-type crew member."""
        member = CrewMember(name, level, "Archaeologist")
        member.set_epithet(epithet)

        # Archaeologist stats: Intelligence and technique
        member.stats.strength.set_base(10)
        member.stats.defense.set_base(9)
        member.stats.speed.set_base(9)
        member.stats.skill.set_base(15)
        member.stats.will.set_base(13)

        return member

    @staticmethod
    def create_shipwright(name: str, level: int = 1, epithet: str = "") -> CrewMember:
        """Create a shipwright-type crew member."""
        member = CrewMember(name, level, "Shipwright")
        member.set_epithet(epithet)

        # Shipwright stats: Balanced physical
        member.stats.strength.set_base(13)
        member.stats.defense.set_base(14)
        member.stats.speed.set_base(9)
        member.stats.skill.set_base(11)

        return member

    @staticmethod
    def create_musician(name: str, level: int = 1, epithet: str = "") -> CrewMember:
        """Create a musician-type crew member."""
        member = CrewMember(name, level, "Musician")
        member.set_epithet(epithet)

        # Musician stats: Speed and technique
        member.stats.strength.set_base(11)
        member.stats.defense.set_base(9)
        member.stats.speed.set_base(14)
        member.stats.skill.set_base(13)
        member.stats.charisma.set_base(15)

        return member
