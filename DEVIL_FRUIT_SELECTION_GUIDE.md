# Devil Fruit Selection Guide

## Overview

The game now features a complete Devil Fruit database with **166 canonical Devil Fruits** from One Piece! Players can select their Devil Fruit during character creation or choose to start without one (and keep their swimming ability!).

## How to Select Your Devil Fruit

### Step 1: Start a New Game

1. Launch the game: `python main.py` or `python src/main.py`
2. From the main menu, select **"New Game"**
3. You'll enter the character creation screen

### Step 2: Enter Your Name

1. Type your pirate name (up to 20 characters)
2. Press **Enter** or click **"Continue"** to proceed

### Step 3: Choose Your Devil Fruit

#### Type Filters

Use the filter buttons to browse Devil Fruits by type:

- **All** - Show all 63 starting-available fruits
- **Paramecia** - Body-altering and special ability fruits (100 total)
- **Zoan** - Animal transformation fruits (54 total)
  - Regular Zoans: 30 fruits (Bison, Leopard, Wolf, Tiger, Lion, etc.)
  - Ancient Zoans: 13 fruits (Mammoth, T-Rex, Triceratops, Velociraptor, etc.)
  - Mythical Zoans: 11 fruits (Phoenix, Dragon, Nine-Tailed Fox, Thunderbird, etc.)
- **Logia** - Elemental transformation fruits (12 total)
- **None** - Start without a Devil Fruit (**You can swim!**)

#### Navigation

- **Arrow Keys (↑↓)** - Scroll through the fruit list
- **Mouse** - Click on any fruit in the list
- The list shows 8 fruits at a time with scroll indicator

#### Fruit Information Panel

When you select a fruit, you'll see:
- **Name** (Japanese and English translation)
- **Description** - What the fruit does
- **Type** - Paramecia, Zoan, or Logia
- **Rarity** - Common, Uncommon, Rare, or Legendary
- **Starting Abilities** - Powers you get at Level 1

#### Character Preview

On the right side, you'll see:
- **Character Preview** - Visual representation
- **Stats Display** - How the fruit affects your stats

### Step 4: Confirm Your Selection

1. Click **"Continue"** to proceed to confirmation
2. Review your choices:
   - Your pirate name
   - Selected Devil Fruit (or "None")
   - Character stats and preview
3. Click **"Confirm"** to start your adventure!
4. Or click **"Cancel"** to go back and change your selection

## Devil Fruit Database

### Complete Collection

✅ **166 Total Devil Fruits**
- 📘 Logia: 12 fruits
- 📗 Paramecia: 100 fruits
- 📙 Zoan: 54 fruits (30 Regular, 13 Ancient, 11 Mythical)

### Starting Available Fruits

**63 fruits** are available at character creation, including:

**Iconic Fruits:**
- Gomu Gomu no Mi (Rubber)
- Mera Mera no Mi (Fire)
- Bara Bara no Mi (Chop-Chop)
- Sube Sube no Mi (Smooth-Smooth)
- Neko Neko no Mi, Model: Leopard
- Tori Tori no Mi, Model: Falcon
- Uma Uma no Mi (Horse)

**Powerful Logia:**
- Mera Mera no Mi (Fire)
- Hie Hie no Mi (Ice)
- Pika Pika no Mi (Light)
- Moku Moku no Mi (Smoke)
- Suna Suna no Mi (Sand)

**Rare Zoan:**
- Various animal models
- Some Ancient models
- Starting Mythical options

### Choosing "None"

**Why choose no Devil Fruit?**
- ✅ **You can swim!** (Devil Fruit users cannot swim)
- ✅ Train other abilities (Haki, combat skills, weapons)
- ✅ More balanced early game
- ✅ Can potentially eat a Devil Fruit later (if found)

## Devil Fruit Effects

### Paramecia Fruits

Body-altering or special ability fruits:
- **Stat Bonuses** - Improve attack, defense, speed, etc.
- **Unique Abilities** - Special powers based on the fruit
- **Versatile** - Wide variety of effects
- **Examples:** Rubber, Chop-Chop, Love-Love, Barrier, etc.

### Zoan Fruits

Animal transformation with multiple forms:
- **Three Forms:** Human, Hybrid, Full Beast
- **Stat Modifiers** - Different stats per form
- **Physical Boosts** - Enhanced strength, speed, durability
- **Special Abilities** - Based on the animal
- **Subtypes:**
  - **Regular:** Standard animals
  - **Ancient:** Prehistoric creatures (stronger)
  - **Mythical:** Legendary beasts (strongest)

### Logia Fruits

Elemental transformation - rarest and most powerful:
- **Intangibility** - Can become the element (immune to normal attacks)
- **Elemental Powers** - Control and generate the element
- **Extreme Power** - Generally strongest fruit type
- **Examples:** Fire, Ice, Light, Lightning, Magma, etc.

## Mastery System

All Devil Fruits have a mastery progression:
- **Level 3** - First mastery bonus
- **Level 5** - Enhanced abilities
- **Level 7** - Advanced techniques
- **Level 10** - **Awakening!** (Ultimate power)

## Tips

1. **Read descriptions carefully** - Each fruit has unique strengths/weaknesses
2. **Consider your playstyle:**
   - Combat-focused? → Zoan or strong Paramecia
   - Elemental powers? → Logia
   - Unique abilities? → Paramecia
   - Versatility? → No fruit + develop other skills
3. **Check starting abilities** - These are the powers you'll have immediately
4. **Think about progression** - What will the awakening give you?
5. **Remember:** You **cannot** change your Devil Fruit once selected!

## Technical Details

### File Structure
```
Databases/
  DevilFruits/
    Paramecia/
      index.json (100 fruits)
    Logia/
      index.json (12 fruits)
    Zoan/
      index.json (54 fruits with all subtypes)
```

### Loading System
- All fruits load at game startup
- Character creation filters by `starting_available` flag
- Type filtering and search available
- Proper validation of fruit data

## Testing

Run the test scripts to verify everything works:

```bash
# Test Devil Fruit loading
python test_devil_fruit_loading.py

# Expected output:
# ✅ 166 fruits loaded
# ✅ All type counts correct
# ✅ Specific fruits found
```

## Support

If you encounter issues:
1. Check the console for error messages
2. Verify all JSON files in `Databases/DevilFruits/` are valid
3. Run test scripts to diagnose loading issues
4. Check `devil_fruit_manager.py` for loading logic

---

**Enjoy your adventure in the One Piece world! 🏴‍☠️**

Choose your Devil Fruit wisely, or embrace the freedom of swimming! ⚓
