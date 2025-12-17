# Quick Start - Devil Fruit Selection

## 🎮 How to Play and Select Your Devil Fruit

### Launch the Game

```bash
cd /home/user/Claude_Code_Test_RPG
python main.py
```

or

```bash
cd /home/user/Claude_Code_Test_RPG
python src/main.py
```

### Character Creation Flow

```
Main Menu
    ↓
[New Game]
    ↓
┌─────────────────────────────────────┐
│  STEP 1: Enter Your Name            │
│  ─────────────────────────           │
│  > Type your pirate name             │
│  > Press Enter or click "Continue"   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  STEP 2: Choose Devil Fruit          │
│  ─────────────────────────           │
│  Filter Buttons:                     │
│  [All] [Paramecia] [Zoan] [Logia]   │
│                          [None]      │
│                                      │
│  ┌──────────────────┐  ┌──────────┐ │
│  │ Fruit List       │  │ Preview  │ │
│  │ ┌──────────────┐ │  │          │ │
│  │ │ Gomu Gomu    │ │  │ Stats    │ │
│  │ │ Bara Bara    │ │  │ Preview  │ │
│  │ │ Mera Mera  ◄─┼─┼─►│ Details  │ │
│  │ │ ...          │ │  │          │ │
│  │ └──────────────┘ │  └──────────┘ │
│  └──────────────────┘                │
│                                      │
│  Fruit Details:                      │
│  Name: Gomu Gomu no Mi              │
│  Translation: Gum-Gum Fruit          │
│  Type: Paramecia                     │
│  Rarity: Rare                        │
│  Abilities: Gum-Gum Pistol          │
│                                      │
│  [Back]              [Continue]      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  STEP 3: Confirm                     │
│  ─────────────────────────           │
│  Name: [Your Name]                   │
│  Devil Fruit: [Your Selection]       │
│                                      │
│  [Cancel]            [Confirm] ✓     │
└─────────────────────────────────────┘
    ↓
START GAME! 🏴‍☠️
```

## 📊 What's Available?

### 166 Total Devil Fruits

| Type | Count | Available at Start |
|------|-------|-------------------|
| Paramecia | 100 | ~40 |
| Logia | 12 | ~8 |
| Zoan | 54 | ~15 |
| **TOTAL** | **166** | **~63** |

### Zoan Breakdown

| Subtype | Count | Examples |
|---------|-------|----------|
| Regular | 30 | Leopard, Wolf, Tiger, Lion, Fox, Elephant |
| Ancient | 13 | Mammoth, T-Rex, Triceratops, Velociraptor |
| Mythical | 11 | Phoenix, Dragon, Nine-Tailed Fox, Thunderbird |

## 🎯 Quick Tips

### For Beginners

**Start with:**
- **Gomu Gomu no Mi** (Rubber) - Iconic and fun!
- **Mera Mera no Mi** (Fire) - Powerful Logia
- **Neko Neko no Mi, Model: Leopard** - Balanced Zoan
- **None** - Keep swimming ability, train other skills

### For Power Players

**Go for:**
- **Logia Fruits** - Intangibility and elemental power
- **Mythical Zoans** - Phoenix, Dragon, etc.
- **Strong Paramecia** - Unique abilities

### Navigation

- **↑/↓ Arrow Keys** - Scroll fruit list
- **Mouse Click** - Select fruit
- **Type Filters** - Narrow down choices
- **Details Panel** - Read before choosing!

## ⚠️ Important

- **You CANNOT change your Devil Fruit later!**
- **Devil Fruit users CANNOT swim!** (Choose "None" to keep swimming)
- **Only ONE Devil Fruit per character**
- **All fruits have unique abilities and progression**

## 🧪 Testing

Verify everything works:

```bash
# Test Devil Fruit loading (should show 166 fruits)
python test_devil_fruit_loading.py

# Expected output:
# ✅ Total: 166 fruits
# ✅ Paramecia: 100
# ✅ Logia: 12
# ✅ Zoan: 54 (30 Regular, 13 Ancient, 11 Mythical)
```

## 📖 Full Documentation

See `DEVIL_FRUIT_SELECTION_GUIDE.md` for:
- Complete fruit list
- Detailed ability descriptions
- Mastery system explanation
- Technical details
- Troubleshooting

---

## 🚀 Ready to Start?

```bash
python main.py
```

**Choose wisely, future Pirate King! ⚓🏴‍☠️**
