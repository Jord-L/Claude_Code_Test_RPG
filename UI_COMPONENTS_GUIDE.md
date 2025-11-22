# Phase 1 Part 3 - UI System Quick Reference

## 🎮 Testing

```bash
cd E:\Github\OnePiece_RPG_PreGrandLine
python test_phase1_part3.py
```

All 6 tests should pass!

---

## 📦 Components Available

### Buttons (3)
- **Button** - Standard clickable button
- **TextButton** - Link-style text button  
- **ImageButton** - Image-based button

### Text (3)
- **TextBox** - Scrollable text with word wrap
- **Label** - Simple single-line text
- **MultilineLabel** - Auto-sized multi-line text

### Panels (3)
- **Panel** - Container for UI elements
- **ScrollablePanel** - Scrollable container
- **ModalPanel** - Centered overlay panel

### Menus (3)
- **Menu** - Vertical menu list
- **HorizontalMenu** - Horizontal menu
- **GridMenu** - Grid-based menu

**Total: 12 Components!**

---

## 🚀 Quick Usage

### Button Example
```python
from ui.button import Button

def on_click():
    print("Clicked!")

button = Button(100, 100, 200, 50, "Click Me", on_click)

# In your state:
button.handle_event(event)  # Handle events
button.update(dt)            # Update
button.render(surface)       # Draw
```

### Menu Example
```python
from ui.menu import Menu

menu = Menu(400, 300, ["Start", "Options", "Quit"])

# Handle events
selected = menu.handle_event(event)
if selected is not None:
    print(f"Selected option {selected}")

menu.update(dt)
menu.render(surface)
```

### Panel Example
```python
from ui.panel import Panel
from ui.button import Button

panel = Panel(50, 50, 500, 400, "My Panel")
button = Button(100, 100, 150, 50, "Test")

panel.add_child(button)

panel.handle_event(event)  # Passes to children
panel.update(dt)           # Updates children
panel.render(surface)      # Renders children
```

---

## ✨ Features

All components support:
- ✅ Mouse input (click, hover, scroll)
- ✅ Keyboard input (arrows, WASD, Enter, Space)
- ✅ Enable/disable states
- ✅ Show/hide visibility
- ✅ Custom colors
- ✅ Event callbacks
- ✅ Smooth animations

---

## 🎨 Common Methods

**All Components:**
- `handle_event(event)` - Process input
- `update(dt)` - Update state
- `render(surface)` - Draw to screen
- `set_visible(bool)` - Show/hide
- `set_enabled(bool)` - Enable/disable

**Containers (Panels):**
- `add_child(component)` - Add element
- `remove_child(component)` - Remove element
- `clear_children()` - Remove all

**Menus:**
- `move_selection(direction)` - Navigate
- `get_selected()` - Get selected index
- `get_selected_text()` - Get selected text
- `set_options(list)` - Change options

---

## 📝 Integration Pattern

```python
class MyState(State):
    def __init__(self, game):
        super().__init__(game)
        
        # Create UI components
        self.button = Button(x, y, w, h, text, callback)
        self.menu = Menu(x, y, options)
        self.panel = Panel(x, y, w, h, title)
        
        # Add to panel
        self.panel.add_child(self.button)
    
    def handle_event(self, event):
        self.panel.handle_event(event)
        self.menu.handle_event(event)
    
    def update(self, dt):
        self.panel.update(dt)
        self.menu.update(dt)
    
    def render(self, surface):
        surface.fill(BLACK)
        self.panel.render(surface)
        self.menu.render(surface)
```

---

## 🎯 Ready to Use!

These components are production-ready and can be used immediately in:
- Character creation (coming next!)
- Battle UI
- Inventory screens
- Menus and dialogs
- Any game interface

---

Last Updated: October 11, 2025
