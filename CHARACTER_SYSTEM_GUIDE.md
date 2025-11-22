# Phase 1 Part 5 - Character System Quick Reference

## 🧪 Testing

```bash
cd E:\Github\OnePiece_RPG_PreGrandLine
python test_phase1_part5.py
```

All 6 tests should pass!

---

## 📦 Classes Available

### Stats
7 primary stats + 8 derived stats

### DevilFruit
Mastery system with ability unlocking

### Character
Base class for all characters

### Player
Extended Character with inventory, berries, reputation

---

## 🚀 Quick Usage

### Create a Player
```python
from entities.player import Player

player = Player("Luffy", level=1)
player.add_berries(5000)
```

### Equip Devil Fruit
```python
from systems.devil_fruit_manager import devil_fruit_manager

fruit_data = devil_fruit_manager.get_fruit_by_id("gomu_gomu")
player.equip_devil_fruit(fruit_data)
```

### Combat
```python
# Take damage
damage_taken = player.take_damage(30)

# Heal
healed = player.heal(50)

# Use ability
if player.use_ap(10):
    # Cast ability
    pass
```

### Leveling
```python
# Gain experience
leveled_up = player.gain_experience(100)

# Level up Devil Fruit
player.devil_fruit.gain_mastery_exp(50)
```

### Inventory
```python
# Add items
player.add_item("health_potion", 3)

# Use items
item_data = item_manager.get_item_by_id("health_potion")
player.use_item("health_potion", item_data)

# Check items
has_it = player.has_item("health_potion", 2)
quantity = player.get_item_quantity("health_potion")
```

### Save/Load
```python
# Save
save_data = player.to_dict()

# Load
loaded_player = Player.from_dict(save_data)
```

---

## 📊 Stats System

### 7 Primary Stats
- **STR** - Strength (physical attack)
- **DEF** - Defense (damage reduction)
- **AGI** - Agility (speed, evasion)
- **INT** - Intelligence (special abilities)
- **WILL** - Willpower (AP, resistance)
- **CHA** - Charisma (prices, interactions)
- **LCK** - Luck (crits, loot)

### 8 Derived Stats
- **Max HP** = Base + (Lvl × 10) + (STR × 2)
- **Max AP** = 50 + (Lvl × 5) + (WILL × 1)
- **Attack** = Base + (STR × 2)
- **Defense** = Base + (DEF × 2)
- **Speed** = Base + (AGI × 2)
- **Crit Chance** = 5% + (LCK × 0.5%)
- **Crit Damage** = 150% + (LCK × 1%)
- **Evasion** = 5% + (AGI × 0.5%)

---

## 🍎 Devil Fruit System

### Mastery Levels (1-10)
- **Level 1** - Basic abilities
- **Level 3** - Mastery bonus 1
- **Level 5** - Mastery bonus 2
- **Level 7** - Mastery bonus 3
- **Level 10** - Awakening!

### Types
- **Paramecia** - Varied abilities
- **Zoan** - Forms (Human/Hybrid/Beast)
- **Logia** - Intangibility

### Usage
```python
# Check abilities
abilities = player.devil_fruit.get_available_abilities(player.current_ap)

# Use ability
ability = abilities[0]
ap_cost = ability.get("ap_cost", 10)
if player.use_ap(ap_cost):
    # Apply ability effects
    pass

# Change Zoan form
if player.devil_fruit.fruit_type == "zoan":
    player.devil_fruit.change_form("hybrid")
```

---

## 🎮 Common Patterns

### Battle Loop
```python
while player.is_alive and enemy.is_alive:
    # Player turn
    damage = player.get_attack_power()
    enemy.take_damage(damage)
    
    # Enemy turn
    if enemy.is_alive:
        damage = enemy.get_attack_power()
        player.take_damage(damage)

# Check winner
if enemy.is_alive:
    player.gain_experience(50)
    player.record_battle_victory()
```

### Shop Purchase
```python
# Check price
item_price = 100

if player.has_berries(item_price):
    if player.spend_berries(item_price):
        player.add_item("sword", 1)
        print("Purchased!")
```

### Level Up Rewards
```python
old_level = player.level
player.gain_experience(100)

if player.level > old_level:
    print(f"Level up! Now level {player.level}")
    print(f"Max HP: {player.max_hp}")
    print(f"Attack: {player.get_attack_power()}")
```

---

## 💾 Save Format

```json
{
  "name": "Luffy",
  "level": 5,
  "experience": 250,
  "current_hp": 180,
  "current_ap": 100,
  "berries": 5000,
  "bounty": 30000000,
  "inventory": [
    {"id": "health_potion", "quantity": 3}
  ],
  "devil_fruit": {
    "fruit_id": "gomu_gomu",
    "mastery_level": 3,
    "awakened": false
  },
  "equipment": {
    "weapon": "iron_sword",
    "armor": null,
    "accessory": null
  },
  "discovered_islands": ["dawn_island", "shells_town"],
  "reputation": {
    "pirates": 20,
    "marines": -30,
    "civilians": 10
  }
}
```

---

## 🎯 Integration Points

### With Data Managers
```python
# Load Devil Fruit
fruit_data = devil_fruit_manager.get_fruit_by_id("gomu_gomu")
player.equip_devil_fruit(fruit_data)

# Load Weapon
weapon_data = item_manager.get_weapon_by_id("iron_sword")
player.equip_item("weapon", weapon_data)

# Load Item
item_data = item_manager.get_item_by_id("health_potion")
player.use_item("health_potion", item_data)
```

### With UI
```python
# Display stats
print(f"Level: {player.level}")
print(f"HP: {player.current_hp}/{player.max_hp}")
print(f"Attack: {player.get_attack_power()}")
print(f"Defense: {player.get_defense_power()}")
print(f"Speed: {player.get_speed()}")

# Show Devil Fruit
if player.devil_fruit:
    print(f"Fruit: {player.devil_fruit.name}")
    print(f"Mastery: {player.devil_fruit.mastery_level}/10")
    progress = player.devil_fruit.get_mastery_progress()
    print(f"Progress: {int(progress * 100)}%")
```

---

## ⚠️ Important Notes

1. **Always check is_alive** before actions
2. **Devil Fruit can only be equipped once**
3. **Berries can't go negative** (spend checks return bool)
4. **HP/AP can't exceed max** (automatically clamped)
5. **Modifiers stack** (equipment + Devil Fruit + buffs)
6. **Save frequently** using `to_dict()`

---

## 🔜 Ready For

Character system is ready for:
- ✅ Character creation screen (next!)
- ✅ Combat system
- ✅ Inventory UI
- ✅ Shop systems
- ✅ Save/load systems
- ✅ Any gameplay feature needing characters!

---

Last Updated: October 11, 2025
