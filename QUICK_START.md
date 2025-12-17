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
│  Random Selection:                   │
│  [🎲 Random (Filter)] [🎲 Random (All)]│
│                                      │
│  ┌──────────────────┐  ┌──────────┐ │
│  │ Fruit List       │  │ Preview  │ │
│  │ (Alphabetical)   │  │          │ │
│  │ ┌──────────────┐ │  │ Stats    │ │
│  │ │ Ame Ame      │ │  │ Preview  │ │
│  │ │ Ami Ami      │ │  │ Details  │ │
│  │ │ Ato Ato    ◄─┼─┼─►│          │ │
│  │ │ ...          │ │  │          │ │
│  │ └──────────────┘ │  └──────────┘ │
│  └──────────────────┘                │
│  (ALL 166 fruits available!)         │
│                                      │
│  Fruit Details:                      │
│  Name: Ato Ato no Mi                │
│  Translation: Art-Art Fruit          │
│  Type: Paramecia                     │
│  Rarity: Rare                        │
│  Abilities: ...                      │
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

### 166 Total Devil Fruits - ALL SELECTABLE!

| Type | Count | Available at Creation |
|------|-------|----------------------|
| Paramecia | 100 | ✅ ALL 100 |
| Logia | 12 | ✅ ALL 12 |
| Zoan | 54 | ✅ ALL 54 |
| **TOTAL** | **166** | **✅ ALL 166** |

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
- **🎲 Random (All)** - Let fate decide!
- **None** - Keep swimming ability, train other skills

### For Power Players

**Go for:**
- **Logia Fruits** - Intangibility and elemental power
- **Mythical Zoans** - Phoenix, Dragon, Nine-Tailed Fox, etc.
- **Legendary Paramecia** - Gura Gura, Ope Ope, etc.
- **🎲 Random (Filter: Logia)** - Random legendary power!

### Navigation

- **↑/↓ Arrow Keys** - Scroll fruit list
- **Mouse Click** - Select fruit
- **Type Filters** - Narrow down choices
- **🎲 Random (Filter)** - Random fruit from current filter
- **🎲 Random (All)** - Completely random fruit
- **Details Panel** - Read before choosing!

### 🎲 Random Selection Features

**🎲 Random (Filter)**
- Randomizes within your current filter
- **[All]** selected? → Random from all 166 fruits
- **[Paramecia]** selected? → Random Paramecia
- **[Zoan]** selected? → Random Zoan (any subtype)
- **[Logia]** selected? → Random Logia
- Perfect for when you want a specific type but can't decide!

**🎲 Random (All)**
- Completely random from all 166 fruits
- Automatically switches to the fruit's type filter
- Auto-scrolls to show your selection
- True surprise - could be anything!
- Great for adventurous players!

**Pro Tip:** Use Random (Filter: Logia) to guarantee a powerful elemental fruit! 🔥❄️⚡

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

# Test random selection and all fruits available
python test_random_selection.py

# Expected output:
# ✅ All 166 fruits available
# ✅ Random selection works
# ✅ 103 non-starting fruits now accessible
# ✅ Alphabetical sorting working
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
