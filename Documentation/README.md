# One Piece RPG - Pre-Grand Line

A 2D turn-based RPG set in the One Piece universe, focusing on exploration of the Four Blues with custom characters, Devil Fruit powers, and crew management.

## Project Status
**Current Phase:** Database Design & Planning  
**Engine:** Python 
**Platform:** PC  
**Version:** 0.1.0-alpha

---

## 🎮 Core Features

- ⚓ **Custom Character Creation** - Build your pirate with Devil Fruit selection
- 🏴‍☠️ **Party-Based Crew System** - Recruit and manage your pirate crew
- ⚔️ **Turn-Based Combat** - Strategic battles with Devil Fruit abilities
- 🗺️ **Open World Exploration** - Island hopping across the Four Blues
- 🚢 **Ship Management** - Upgrade and customize your pirate ship
- 📖 **Alternative Timeline** - Original story with canon inspiration
- 💪 **Devil Fruit Mastery** - Level up and awaken your fruit powers
- 🎯 **Quest System** - Main story and side quests with branching paths

---

## 📁 Project Structure

```
OnePiece_RPG_PreGrandLine/
├── Assets/                    # Unity assets (future)
│   ├── Scripts/              # C# game scripts
│   ├── Sprites/              # 2D artwork
│   ├── Prefabs/              # Unity prefabs
│   ├── Scenes/               # Game scenes
│   └── Resources/            # Loadable resources
│
├── Database/                  # ✅ COMPLETE - Game data in JSON
│   ├── DevilFruits/          # All Devil Fruit data
│   │   ├── Paramecia/        # Body manipulation fruits
│   │   ├── Logia/            # Elemental fruits
│   │   └── Zoan/             # Animal transformations
│   │       ├── Regular/      # Standard animals
│   │       ├── Ancient/      # Prehistoric creatures
│   │       └── Mythical/     # Legendary beings
│   ├── Inventory/            # Non-weapon items
│   │   ├── Consumables/      # Potions, buffs
│   │   ├── Materials/        # Crafting resources
│   │   └── KeyItems/         # Quest items
│   ├── Weapons/              # All weapon types
│   │   ├── Swords/           # Bladed weapons
│   │   ├── Guns/             # Firearms
│   │   ├── Staffs/           # Bo staffs, clima-tacts
│   │   ├── Polearms/         # Spears, tridents
│   │   ├── Bows/             # Ranged weapons
│   │   └── Fists/            # Gauntlets, knuckles
│   ├── Islands/              # World locations
│   ├── CrewManagement/       # Recruitable characters
│   ├── SaveData/             # Player save files
│   └── README.md             # Database documentation
│
├── Documentation/             # ✅ COMPLETE - Design documents
│   ├── GameDesign.md         # Complete game design doc
│   └── QuickDecisions.md     # Decision checklist
│
└── README.md                  # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Unity 2022.3 LTS or later (recommended)
- Git for version control
- Text editor for JSON editing

### Current Setup
1. Clone this repository
   ```bash
   git clone https://github.com/yourusername/OnePiece_RPG_PreGrandLine.git
   cd OnePiece_RPG_PreGrandLine
   ```

2. Review the documentation
   - Read `Documentation/GameDesign.md` for complete game design
   - Check `Database/README.md` for database structure

3. (Future) Open in Unity Hub when Unity project is initialized

---

## 📊 Development Progress

### ✅ Completed
- [x] Project initialization and Git setup
- [x] Comprehensive game design document
- [x] Complete database structure with index system
- [x] Devil Fruit categorization (Paramecia, Logia, Zoan subtypes)
- [x] Weapon categorization by type
- [x] Inventory system structure
- [x] Island database framework
- [x] Crew management system structure
- [x] Save data architecture

### 🔄 In Progress
- [ ] Populating Devil Fruit data
- [ ] Creating starting weapons
- [ ] Designing East Blue islands
- [ ] Character creation system design

### 📅 Upcoming
- [ ] Unity project initialization
- [ ] Core systems architecture
- [ ] Character creation implementation
- [ ] Basic combat prototype
- [ ] World map and movement
- [ ] First playable island

See `Documentation/GameDesign.md` Section 16 for detailed roadmap.

---

## 🎯 Current Development Focus

**Phase 1: Foundation Building**
1. **Database Population** - Fill in starting Devil Fruits, weapons, and items
2. **East Blue Design** - Plan and document first 5 islands
3. **Combat System Planning** - Finalize turn-based mechanics
4. **Unity Setup** - Initialize project with proper structure

---

## 📖 Documentation

### Main Documents
- **[Game Design Document](Documentation/GameDesign.md)** - Complete game design (20 sections)
- **[Quick Decisions](Documentation/QuickDecisions.md)** - Critical choices checklist
- **[Database README](Database/README.md)** - Database structure and usage guide

### Key Design Decisions
- **Game Type:** 2D Turn-based RPG, Open World, Party-based
- **Setting:** East Blue → All Four Blues eventually
- **Story:** Alternative timeline with canon elements
- **Combat:** Turn-based with Devil Fruit abilities
- **Progression:** Character levels, Devil Fruit mastery, crew recruitment
- **Platform:** PC (Windows/Mac/Linux)

---

## 🎨 Game Design Highlights

### Devil Fruit System
Three main types with distinct mechanics:
- **Paramecia** - Versatile body/manipulation abilities
- **Logia** - Elemental intangibility (most powerful)
- **Zoan** - Animal forms with stat boosts
  - Regular, Ancient, and Mythical subtypes

Players choose ONE Devil Fruit at character creation, with mastery levels 1-10 and awakening at max level.

### Combat System
- Turn-based strategic battles
- Devil Fruit abilities cost AP (Ability Points)
- Status effects and elemental interactions
- Party synergies and combination attacks
- Haki system unlocks late game

### World Exploration
- Open world island hopping via ship
- Multiple Blues to explore (starting with East Blue)
- Towns, dungeons, Marine bases, and hidden locations
- Dynamic encounters and events
- Weather and day/night systems

### Crew Management
- Active party of 4-6 members
- Named story characters with personal quests
- Generic recruits available for hire
- Loyalty and relationship systems
- Character-specific abilities and growth

---

## 🛠️ Technology Stack

- **Engine:** Unity 2D
- **Language:** C# for scripts
- **Data Format:** JSON for game data
- **Version Control:** Git/GitHub
- **Art Style:** 2D sprites (style TBD)
- **Platform:** PC (Windows, Mac, Linux)

---

## 🤝 Contributing

This is currently a solo development project. Design decisions and progress are tracked in the Documentation folder.

---

## 📝 Notes for Developers

### Database System
- All game data stored as JSON in the Database folder
- Each category has an index.json file for organization
- Templates provided for every data type
- IDs must be unique within each category
- See Database/README.md for detailed usage

### Naming Conventions
- Devil Fruits: Use Japanese names (GomuGomu.json)
- Items/Weapons: Descriptive English (HealthPotion.json)
- Islands: Location names (DawnIsland.json)
- IDs: lowercase_with_underscores

### Next Steps for Implementation
1. Populate starting Devil Fruits (5-8 per type)
2. Create basic weapons and items
3. Design first 3-5 East Blue islands
4. Initialize Unity project
5. Build data loading system
6. Implement character creation

---

## 🎮 Game Vision

Create an immersive One Piece RPG experience that captures the spirit of adventure, freedom, and friendship from the series while telling an original story. Players will build their own pirate legend, recruit a memorable crew, master powerful Devil Fruit abilities, and explore the vast world of the Four Blues before eventually reaching the Grand Line.

**Target Experience:**
- Deep strategic combat with meaningful choices
- Engaging character progression and customization
- Memorable crew members with their own stories
- Open-ended exploration with secrets to discover
- Compelling narrative with player agency

---

## 📜 License

[License TBD]

---

## 🔗 Links

- **Repository:** https://github.com/yourusername/OnePiece_RPG_PreGrandLine
- **Documentation:** `/Documentation/`
- **Database:** `/Database/`

---

**Last Updated:** October 11, 2025  
**Project Lead:** [Your Name]  
**Status:** Active Development - Planning Phase
