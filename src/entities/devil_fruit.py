"""
Devil Fruit Class
Represents a Devil Fruit equipped by a character.
"""

from typing import Dict, List, Optional


class DevilFruit:
    """
    Represents a Devil Fruit and its current state for a character.
    Tracks mastery level, unlocked abilities, and provides stat bonuses.
    """
    
    def __init__(self, fruit_data: Dict):
        """
        Initialize a Devil Fruit from data.
        
        Args:
            fruit_data: Devil Fruit data dictionary from database
        """
        self.fruit_id = fruit_data.get("id", "unknown")
        self.name = fruit_data.get("name", "Unknown Fruit")
        self.translation = fruit_data.get("translation", "")
        self.description = fruit_data.get("description", "")
        self.fruit_type = self._determine_type(fruit_data)
        self.rarity = fruit_data.get("rarity", "Common")
        
        # Store full fruit data
        self.data = fruit_data
        
        # Mastery system
        self.mastery_level = 1
        self.max_mastery = 10
        self.mastery_exp = 0
        self.mastery_exp_to_next = 100
        
        # Abilities
        self.all_abilities = fruit_data.get("abilities", [])
        self.unlocked_abilities = []
        self._unlock_starting_abilities()
        
        # Weaknesses and strengths
        self.weaknesses = fruit_data.get("weaknesses", [])
        self.strengths = fruit_data.get("strengths", [])
        
        # Zoan specific
        self.current_form = "human" if self.fruit_type == "zoan" else None
        self.forms = fruit_data.get("forms", {})
        
        # Logia specific
        self.intangibility = fruit_data.get("intangibility", False)
        self.element = fruit_data.get("element", None)
        
        # Awakening
        self.awakened = False
    
    def _determine_type(self, fruit_data: Dict) -> str:
        """Determine fruit type from data."""
        # Check explicit type field
        if "type" in fruit_data:
            return fruit_data["type"].lower()
        
        # Check for type indicators
        if "intangibility" in fruit_data:
            return "logia"
        elif "forms" in fruit_data:
            return "zoan"
        else:
            return "paramecia"
    
    def _unlock_starting_abilities(self):
        """Unlock abilities available at mastery level 1."""
        for ability in self.all_abilities:
            required_level = ability.get("level_required", 1)
            if required_level <= self.mastery_level:
                if ability not in self.unlocked_abilities:
                    self.unlocked_abilities.append(ability)
    
    # Mastery system
    
    def gain_mastery_exp(self, amount: int):
        """
        Gain mastery experience.
        
        Args:
            amount: Experience to gain
        """
        if self.mastery_level >= self.max_mastery:
            return
        
        self.mastery_exp += amount
        
        # Check for level up
        while self.mastery_exp >= self.mastery_exp_to_next:
            self.level_up_mastery()
    
    def level_up_mastery(self):
        """Level up Devil Fruit mastery."""
        if self.mastery_level >= self.max_mastery:
            return
        
        self.mastery_level += 1
        self.mastery_exp -= self.mastery_exp_to_next
        self.mastery_exp_to_next = int(self.mastery_exp_to_next * 1.5)
        
        # Unlock new abilities
        for ability in self.all_abilities:
            required_level = ability.get("level_required", 1)
            if required_level <= self.mastery_level:
                if ability not in self.unlocked_abilities:
                    self.unlocked_abilities.append(ability)
                    print(f"Unlocked ability: {ability['name']}!")
        
        # Check for awakening
        if self.mastery_level >= self.max_mastery:
            self.awaken()
        
        print(f"Devil Fruit Mastery increased to level {self.mastery_level}!")
    
    def awaken(self):
        """Awaken the Devil Fruit (max mastery)."""
        if self.awakened:
            return
        
        self.awakened = True
        
        # Get awakening bonus from data
        mastery_bonuses = self.data.get("mastery_bonuses", {})
        awakening_bonus = mastery_bonuses.get("level_10_awakening", "Unknown power")
        
        print(f"Devil Fruit Awakened! {awakening_bonus}")
    
    # Ability access
    
    def get_available_abilities(self, current_ap: int = 999) -> List[Dict]:
        """
        Get abilities that can currently be used.
        
        Args:
            current_ap: Character's current AP
        
        Returns:
            List of usable abilities
        """
        available = []
        for ability in self.unlocked_abilities:
            ap_cost = ability.get("ap_cost", 0)
            if ap_cost <= current_ap:
                available.append(ability)
        return available
    
    def get_ability_by_name(self, name: str) -> Optional[Dict]:
        """
        Get an ability by name.
        
        Args:
            name: Ability name
        
        Returns:
            Ability data or None
        """
        for ability in self.unlocked_abilities:
            if ability.get("name", "").lower() == name.lower():
                return ability
        return None
    
    # Stat bonuses
    
    def get_stat_modifiers(self) -> Dict[str, int]:
        """
        Get stat modifiers from the fruit.
        
        Returns:
            Dictionary of stat modifiers
        """
        modifiers = {}
        
        # Zoan form bonuses
        if self.fruit_type == "zoan" and self.current_form:
            form_data = self.forms.get(self.current_form, {})
            form_mods = form_data.get("stat_modifiers", {})
            
            # Apply modifiers
            for stat, value in form_mods.items():
                if isinstance(value, str) and '%' in value:
                    # Percentage modifier (handled separately)
                    continue
                else:
                    modifiers[stat] = int(value)
        
        return modifiers
    
    def get_percent_modifiers(self) -> Dict[str, float]:
        """
        Get percentage stat modifiers from the fruit.
        
        Returns:
            Dictionary of percentage modifiers
        """
        modifiers = {}
        
        # Zoan form bonuses
        if self.fruit_type == "zoan" and self.current_form:
            form_data = self.forms.get(self.current_form, {})
            form_mods = form_data.get("stat_modifiers", {})
            
            # Extract percentage modifiers
            for stat, value in form_mods.items():
                if isinstance(value, str) and '%' in value:
                    # Convert "+20%" to 0.20
                    percent_str = value.replace('+', '').replace('%', '')
                    modifiers[stat] = float(percent_str) / 100.0
        
        return modifiers
    
    # Zoan form management
    
    def change_form(self, form_name: str) -> bool:
        """
        Change Zoan form.
        
        Args:
            form_name: "human", "hybrid", or "full_beast"
        
        Returns:
            True if successful
        """
        if self.fruit_type != "zoan":
            return False
        
        if form_name not in self.forms:
            return False
        
        self.current_form = form_name
        return True
    
    def get_current_form_description(self) -> str:
        """Get description of current Zoan form."""
        if self.fruit_type != "zoan" or not self.current_form:
            return ""
        
        form_data = self.forms.get(self.current_form, {})
        return form_data.get("description", "")
    
    # Utility methods
    
    def can_swim(self) -> bool:
        """Check if character can swim (always False with Devil Fruit)."""
        return False
    
    def is_weak_to_water(self) -> bool:
        """Check if weak to water (always True)."""
        return True
    
    def is_weak_to_seastone(self) -> bool:
        """Check if weak to seastone (always True)."""
        return True
    
    def has_intangibility(self) -> bool:
        """Check if fruit grants intangibility (Logia)."""
        return self.intangibility and self.fruit_type == "logia"
    
    def get_mastery_progress(self) -> float:
        """
        Get mastery progress to next level.
        
        Returns:
            Progress as percentage (0.0 to 1.0)
        """
        if self.mastery_level >= self.max_mastery:
            return 1.0
        return self.mastery_exp / self.mastery_exp_to_next
    
    # Saving/loading
    
    def to_dict(self) -> Dict:
        """
        Convert to dictionary for saving.
        
        Returns:
            Dictionary representation
        """
        return {
            "fruit_id": self.fruit_id,
            "mastery_level": self.mastery_level,
            "mastery_exp": self.mastery_exp,
            "mastery_exp_to_next": self.mastery_exp_to_next,
            "awakened": self.awakened,
            "current_form": self.current_form,
            "unlocked_abilities": [
                ability.get("name", "") for ability in self.unlocked_abilities
            ]
        }
    
    @classmethod
    def from_dict(cls, save_data: Dict, fruit_data: Dict) -> 'DevilFruit':
        """
        Create DevilFruit from save data.
        
        Args:
            save_data: Saved fruit state
            fruit_data: Full fruit data from database
        
        Returns:
            DevilFruit instance
        """
        fruit = cls(fruit_data)
        
        # Restore state
        fruit.mastery_level = save_data.get("mastery_level", 1)
        fruit.mastery_exp = save_data.get("mastery_exp", 0)
        fruit.mastery_exp_to_next = save_data.get("mastery_exp_to_next", 100)
        fruit.awakened = save_data.get("awakened", False)
        fruit.current_form = save_data.get("current_form", "human")
        
        # Restore unlocked abilities
        unlocked_names = save_data.get("unlocked_abilities", [])
        fruit.unlocked_abilities = [
            ability for ability in fruit.all_abilities
            if ability.get("name", "") in unlocked_names
        ]
        
        return fruit
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.name} (Mastery: {self.mastery_level}/{self.max_mastery})"
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"DevilFruit({self.fruit_id}, mastery={self.mastery_level})"
