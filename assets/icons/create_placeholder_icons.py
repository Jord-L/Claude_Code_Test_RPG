"""
Create placeholder icons for items
Simple colored squares with symbols for different item types
"""

import pygame
import os

# Initialize pygame
pygame.init()

# Icon size
SIZE = 32

def create_icon(filename, bg_color, symbol=None, symbol_color=(255, 255, 255)):
    """Create a simple icon with background and optional symbol."""
    surface = pygame.Surface((SIZE, SIZE))
    surface.fill(bg_color)

    # Add border
    pygame.draw.rect(surface, (200, 200, 200), (0, 0, SIZE, SIZE), 2)

    if symbol:
        font = pygame.font.Font(None, 24)
        text = font.render(symbol, True, symbol_color)
        text_rect = text.get_rect(center=(SIZE//2, SIZE//2))
        surface.blit(text, text_rect)

    # Save
    pygame.image.save(surface, filename)
    print(f"Created: {filename}")

# Create icon directory if needed
os.makedirs("items", exist_ok=True)

# Weapon icons
create_icon("items/sword_icon.png", (150, 150, 200), "⚔", (255, 255, 255))
create_icon("items/gun_icon.png", (120, 120, 180), "🔫", (255, 255, 255))
create_icon("items/staff_icon.png", (140, 100, 200), "🎯", (255, 255, 255))

# Armor icons
create_icon("items/armor_light.png", (100, 150, 100), "🛡", (255, 255, 255))
create_icon("items/armor_heavy.png", (80, 120, 80), "🛡", (200, 200, 200))

# Accessory icons
create_icon("items/ring_icon.png", (200, 150, 100), "💍", (255, 255, 100))
create_icon("items/amulet_icon.png", (180, 120, 200), "📿", (255, 255, 255))

# Consumable icons
create_icon("items/potion_hp.png", (200, 50, 50), "❤", (255, 100, 100))
create_icon("items/potion_ap.png", (50, 100, 200), "✦", (100, 150, 255))
create_icon("items/food_icon.png", (200, 150, 50), "🍖", (255, 200, 100))

# Material icons
create_icon("items/material_wood.png", (139, 90, 43), "🪵", (210, 180, 140))
create_icon("items/material_metal.png", (128, 128, 128), "⚙", (200, 200, 200))

# Key item icon
create_icon("items/key_item.png", (220, 180, 0), "🔑", (255, 215, 0))

print("\nAll placeholder icons created in items/ directory!")
print("To use: set item.icon = 'items/sword_icon.png' in item data")

pygame.quit()
