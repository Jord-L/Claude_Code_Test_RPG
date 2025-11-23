"""
Party Helper Functions
Utility functions for initializing and managing party members.
"""

from systems.party_manager import PartyManager, PartyFactory, CrewMember
from entities.player import Player
from systems.devil_fruit_manager import DevilFruitManager


def create_starter_crew(party_manager: PartyManager) -> None:
    """
    Create a starter crew for testing/demo purposes.
    Inspired by One Piece Straw Hat crew.

    Args:
        party_manager: PartyManager to add crew to
    """
    # Zoro - Swordsman/Fighter
    zoro = PartyFactory.create_fighter("Roronoa Zoro", level=5, epithet="Pirate Hunter")
    zoro.set_dream("To become the world's greatest swordsman")
    zoro.loyalty = 100
    party_manager.add_member(zoro, to_active=True)

    # Nami - Navigator
    nami = PartyFactory.create_navigator("Nami", level=4, epithet="Cat Burglar")
    nami.set_dream("To draw a map of the entire world")
    nami.loyalty = 95
    party_manager.add_member(nami, to_active=True)

    # Usopp - Sniper
    usopp = PartyFactory.create_sniper("Usopp", level=3, epithet="God Usopp")
    usopp.set_dream("To become a brave warrior of the sea")
    usopp.loyalty = 100
    party_manager.add_member(usopp, to_active=True)

    # Sanji - Cook
    sanji = PartyFactory.create_cook("Sanji", level=5, epithet="Black Leg")
    sanji.set_dream("To find the All Blue")
    sanji.loyalty = 100
    party_manager.add_member(sanji, to_active=False)  # In reserve

    # Chopper - Doctor
    chopper = PartyFactory.create_doctor("Tony Tony Chopper", level=2, epithet="Cotton Candy Lover")
    chopper.set_dream("To cure any disease")
    chopper.loyalty = 100
    party_manager.add_member(chopper, to_active=False)

    print(f"Created starter crew: {party_manager.get_total_count()} members")
    print(f"Active: {[m.name for m in party_manager.get_active_party()]}")
    print(f"Reserve: {[m.name for m in party_manager.get_reserve_party()]}")


def add_devil_fruit_to_member(member: CrewMember, fruit_id: str) -> bool:
    """
    Add a Devil Fruit to a crew member.

    Args:
        member: Crew member to give fruit to
        fruit_id: Devil Fruit ID from database

    Returns:
        True if successful
    """
    try:
        df_manager = DevilFruitManager()
        fruit_data = df_manager.get_fruit(fruit_id)

        if not fruit_data:
            print(f"Devil Fruit {fruit_id} not found")
            return False

        # Import here to avoid circular dependency
        from entities.devil_fruit import DevilFruit

        devil_fruit = DevilFruit(fruit_data)
        member.devil_fruit = devil_fruit

        # Give them AP for abilities
        member.max_ap = 100
        member.current_ap = 100

        print(f"{member.name} ate the {devil_fruit.name}!")
        return True

    except Exception as e:
        print(f"Error adding Devil Fruit: {e}")
        return False


def recruit_custom_member(
    party_manager: PartyManager,
    name: str,
    role: str,
    level: int = 1,
    epithet: str = "",
    dream: str = "",
    to_active: bool = False
) -> bool:
    """
    Recruit a custom crew member.

    Args:
        party_manager: PartyManager to add to
        name: Character name
        role: Character role
        level: Starting level
        epithet: Character epithet
        dream: Character's dream
        to_active: Add to active party

    Returns:
        True if successfully recruited
    """
    # Create member based on role
    role_creators = {
        "Fighter": PartyFactory.create_fighter,
        "Sniper": PartyFactory.create_sniper,
        "Navigator": PartyFactory.create_navigator,
        "Cook": PartyFactory.create_cook,
        "Doctor": PartyFactory.create_doctor,
        "Archaeologist": PartyFactory.create_archaeologist,
        "Shipwright": PartyFactory.create_shipwright,
        "Musician": PartyFactory.create_musician
    }

    creator = role_creators.get(role, PartyFactory.create_fighter)
    member = creator(name, level, epithet)

    if dream:
        member.set_dream(dream)

    success = party_manager.add_member(member, to_active=to_active)

    if success:
        print(f"Recruited {name} as {role}!")

    return success


def heal_party(party_manager: PartyManager):
    """
    Fully heal all party members (like resting at an inn).

    Args:
        party_manager: PartyManager to heal
    """
    party_manager.heal_all_members()
    party_manager.revive_fallen_members()
    print("Party fully healed!")


def get_party_summary(party_manager: PartyManager) -> str:
    """
    Get a text summary of the party.

    Args:
        party_manager: PartyManager to summarize

    Returns:
        Formatted summary string
    """
    lines = [
        f"=== PARTY SUMMARY ===",
        f"Captain: {party_manager.captain.name} (Lv.{party_manager.captain.level})",
        f"",
        f"Active Party ({len(party_manager.active_party)}/{party_manager.MAX_ACTIVE}):"
    ]

    for member in party_manager.get_active_party():
        status = "ALIVE" if member.is_alive else "FALLEN"
        lines.append(f"  - {member.name} (Lv.{member.level}) [{status}] HP: {member.current_hp}/{member.max_hp}")

    lines.append(f"")
    lines.append(f"Reserve Party ({len(party_manager.reserve_party)}/{party_manager.MAX_RESERVE}):")

    for member in party_manager.get_reserve_party():
        status = "ALIVE" if member.is_alive else "FALLEN"
        role = f"({member.role})" if isinstance(member, CrewMember) else ""
        lines.append(f"  - {member.name} {role} (Lv.{member.level}) [{status}]")

    lines.append(f"")
    lines.append(f"Total Recruited: {party_manager.total_recruited}")

    return "\n".join(lines)
