"""
Character Creation State
Handles the character creation process with Devil Fruit selection.
"""

import pygame
from typing import Optional, List, Dict
from states.state import State
from entities.player import Player
from systems.devil_fruit_manager import devil_fruit_manager
from ui.button import Button
from ui.text_box import CenteredText
from ui.panel import Panel
from ui.character_preview import CharacterPreview
from ui.stat_display import StatDisplay
from utils.save_manager import get_save_manager
from utils.constants import *


class CharacterCreationState(State):
    """
    Character creation screen allowing name input and Devil Fruit selection.
    """
    
    def __init__(self, game):
        """
        Initialize character creation state.
        
        Args:
            game: Game instance
        """
        super().__init__(game)
        
        # Creation stages
        self.stage = "name"  # name, devil_fruit, confirm
        
        # Player data
        self.player_name = ""
        self.selected_fruit_id = None
        self.selected_fruit_data = None
        
        # UI Components
        self.title_text = None
        self.name_input_box = None
        self.instruction_text = None
        
        # Devil Fruit selection
        self.fruit_type_filter = "all"  # all, paramecia, zoan, logia, none
        self.fruit_list: List[Dict] = []
        self.selected_fruit_index = 0
        self.fruit_scroll_offset = 0
        self.max_visible_fruits = 8
        
        # Panels
        self.main_panel = None
        self.fruit_info_panel = None
        self.preview_panel = None
        
        # Preview components
        self.character_preview = None
        self.stat_display = None
        
        # Buttons
        self.buttons = []
        self.continue_button = None
        self.back_button = None
        self.confirm_button = None
        self.cancel_button = None
        
        # Type filter buttons
        self.type_buttons = []
        
        # Input handling
        self.input_active = True
        self.max_name_length = 20
        
        # Load Devil Fruits
        if not devil_fruit_manager.loaded:
            devil_fruit_manager.load_all_fruits()
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up all UI elements."""
        # Title
        self.title_text = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=40,
            text="Create Your Pirate",
            font_size=48,
            color=UI_TEXT_COLOR,
            centered=True
        )
        
        # Main panel for content
        self.main_panel = Panel(
            x=SCREEN_WIDTH // 2 - 400,
            y=120,
            width=800,
            height=500
        )
        self.main_panel.bg_color = UI_BG_COLOR
        self.main_panel.border_color = UI_BORDER_COLOR
        self.main_panel.border_width = 3
        
        # Preview panel (right side)
        self.preview_panel = Panel(
            x=SCREEN_WIDTH // 2 + 250,
            y=120,
            width=300,
            height=500
        )
        self.preview_panel.bg_color = UI_BG_COLOR
        self.preview_panel.border_color = UI_BORDER_COLOR
        self.preview_panel.border_width = 3
        
        # Character preview
        self.character_preview = CharacterPreview(
            x=SCREEN_WIDTH // 2 + 400,
            y=200
        )
        
        # Stat display
        self.stat_display = StatDisplay(
            x=SCREEN_WIDTH // 2 + 270,
            y=380,
            width=260
        )
        
        # Continue button
        self.continue_button = Button(
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=50,
            text="Continue",
            callback=self._on_continue
        )
        
        # Back button
        self.back_button = Button(
            x=SCREEN_WIDTH // 2 - 320,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=50,
            text="Back",
            callback=self._on_back
        )
        
        # Confirm button
        self.confirm_button = Button(
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=50,
            text="Confirm",
            callback=self._on_confirm
        )
        
        # Cancel button  
        self.cancel_button = Button(
            x=SCREEN_WIDTH // 2 + 120,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=50,
            text="Cancel",
            callback=self._on_cancel
        )
        
        self.buttons = [
            self.continue_button,
            self.back_button,
            self.confirm_button,
            self.cancel_button
        ]
        
        # Set up stage-specific UI
        self._setup_name_stage()
    
    def _setup_name_stage(self):
        """Set up UI for name input stage."""
        self.stage = "name"
        self.input_active = True

        # Instruction text
        self.instruction_text = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=180,
            text="Enter your pirate name:",
            font_size=32,
            color=UI_TEXT_COLOR,
            centered=True
        )

        # Name input box
        self.name_input_box = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=250,
            text=self.player_name if self.player_name else "Type here...",
            font_size=36,
            color=WHITE if self.player_name else GRAY,
            centered=True
        )

        # Show continue and exit buttons
        self.continue_button.visible = True
        self.back_button.visible = True  # Exit button
        self.back_button.text = "Exit"  # Change text to "Exit" for name stage
        self.confirm_button.visible = False
        self.cancel_button.visible = False
    
    def _setup_devil_fruit_stage(self):
        """Set up UI for Devil Fruit selection stage."""
        self.stage = "devil_fruit"
        self.input_active = False
        
        # Instruction text
        self.instruction_text = CenteredText(
            x=SCREEN_WIDTH // 2 - 250,
            y=140,
            text="Choose Your Devil Fruit (or None):",
            font_size=28,
            color=UI_TEXT_COLOR,
            centered=False
        )
        
        # Type filter buttons
        filter_types = [
            ("All", "all"),
            ("Paramecia", "paramecia"),
            ("Zoan", "zoan"),
            ("Logia", "logia"),
            ("None", "none")
        ]
        
        self.type_buttons.clear()
        button_width = 140
        button_spacing = 10
        start_x = SCREEN_WIDTH // 2 - (len(filter_types) * (button_width + button_spacing)) // 2
        
        for i, (label, filter_type) in enumerate(filter_types):
            button = Button(
                x=start_x + i * (button_width + button_spacing),
                y=180,
                width=button_width,
                height=40,
                text=label,
                callback=lambda ft=filter_type: self._set_fruit_filter(ft)
            )
            self.type_buttons.append(button)

        # Random buttons (below filter buttons)
        random_button_width = 180
        random_start_x = SCREEN_WIDTH // 2 - random_button_width - 5

        # Random (Filter) button
        self.random_filter_button = Button(
            x=random_start_x,
            y=230,
            width=random_button_width,
            height=35,
            text="🎲 Random (Filter)",
            callback=self._random_fruit_current_filter
        )
        self.type_buttons.append(self.random_filter_button)

        # Random (All) button
        self.random_all_button = Button(
            x=random_start_x + random_button_width + 10,
            y=230,
            width=random_button_width,
            height=35,
            text="🎲 Random (All)",
            callback=self._random_fruit_all
        )
        self.type_buttons.append(self.random_all_button)

        # Load fruit list based on filter
        self._update_fruit_list()

        # Fruit info panel (adjusted y to account for random buttons)
        self.fruit_info_panel = Panel(
            x=SCREEN_WIDTH // 2 - 380,
            y=280,
            width=600,
            height=310
        )
        self.fruit_info_panel.bg_color = UI_BG_COLOR
        self.fruit_info_panel.border_color = UI_BORDER_COLOR
        self.fruit_info_panel.border_width = 2
        
        # Show back and continue buttons
        self.continue_button.visible = True
        self.back_button.visible = True
        self.back_button.text = "Back"  # Change text back to "Back" for devil fruit stage
        self.confirm_button.visible = False
        self.cancel_button.visible = False
    
    def _setup_confirm_stage(self):
        """Set up UI for final confirmation stage."""
        self.stage = "confirm"
        self.input_active = False
        
        # Instruction text
        self.instruction_text = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=160,
            text="Confirm Your Character:",
            font_size=32,
            color=UI_TEXT_COLOR,
            centered=True
        )
        
        # Show confirm and cancel buttons
        self.continue_button.visible = False
        self.back_button.visible = False
        self.confirm_button.visible = True
        self.cancel_button.visible = True
    
    def _update_fruit_list(self):
        """Update the list of fruits based on current filter."""
        if self.fruit_type_filter == "none":
            self.fruit_list = []
            self.selected_fruit_id = None
            self.selected_fruit_data = None
        elif self.fruit_type_filter == "all":
            # Get ALL fruits (no starting_available filter)
            self.fruit_list = devil_fruit_manager.get_all_fruits()
        else:
            # Get all fruits of specific type (no starting_available filter)
            self.fruit_list = devil_fruit_manager.get_fruits_by_type(self.fruit_type_filter)

        # Sort fruits by name for easier browsing
        self.fruit_list = sorted(self.fruit_list, key=lambda f: f.get("name", ""))

        # Reset selection
        self.selected_fruit_index = 0
        self.fruit_scroll_offset = 0

        # Select first fruit if available
        if self.fruit_list:
            self._select_fruit(0)
    
    def _select_fruit(self, index: int):
        """
        Select a fruit from the list.
        
        Args:
            index: Fruit index in the list
        """
        if 0 <= index < len(self.fruit_list):
            self.selected_fruit_index = index
            fruit = self.fruit_list[index]
            self.selected_fruit_id = fruit.get("id")
            self.selected_fruit_data = fruit
            
            # Update preview
            self._update_preview()
    
    def _set_fruit_filter(self, filter_type: str):
        """
        Set the fruit type filter.

        Args:
            filter_type: "all", "paramecia", "zoan", "logia", or "none"
        """
        self.fruit_type_filter = filter_type
        self._update_fruit_list()

    def _random_fruit_current_filter(self):
        """Select a random fruit from the current filter."""
        import random

        if self.fruit_type_filter == "none":
            # No fruit selected
            self.selected_fruit_id = None
            self.selected_fruit_data = None
            return

        if not self.fruit_list:
            print("No fruits available in current filter!")
            return

        # Select random index
        random_index = random.randint(0, len(self.fruit_list) - 1)
        self._select_fruit(random_index)

        # Update scroll to show selected fruit
        if random_index < self.fruit_scroll_offset:
            self.fruit_scroll_offset = random_index
        elif random_index >= self.fruit_scroll_offset + self.max_visible_fruits:
            self.fruit_scroll_offset = random_index - self.max_visible_fruits + 1

        print(f"Random fruit selected: {self.selected_fruit_data.get('name')}")

    def _random_fruit_all(self):
        """Select a completely random fruit from all available fruits."""
        import random

        # Get all fruits
        all_fruits = devil_fruit_manager.get_all_fruits()

        if not all_fruits:
            print("No fruits available!")
            return

        # Select random fruit
        random_fruit = random.choice(all_fruits)

        # Determine the type and set filter
        fruit_type = random_fruit.get("type", "paramecia").lower()

        # Update filter to show the type
        self.fruit_type_filter = fruit_type
        self._update_fruit_list()

        # Find the fruit in the list and select it
        for i, fruit in enumerate(self.fruit_list):
            if fruit.get("id") == random_fruit.get("id"):
                self._select_fruit(i)

                # Update scroll to show selected fruit
                if i < self.fruit_scroll_offset:
                    self.fruit_scroll_offset = i
                elif i >= self.fruit_scroll_offset + self.max_visible_fruits:
                    self.fruit_scroll_offset = i - self.max_visible_fruits + 1

                break

        print(f"Random fruit selected: {random_fruit.get('name')} ({fruit_type})")

    def _update_preview(self):
        """Update character preview with current selections."""
        # Create temporary player for preview
        temp_player = Player(self.player_name if self.player_name else "Preview")
        
        # Equip selected fruit
        if self.selected_fruit_data:
            temp_player.equip_devil_fruit(self.selected_fruit_data)
        
        # Update displays
        self.character_preview.set_character(temp_player)
        self.stat_display.set_character(temp_player)
    
    def _on_continue(self):
        """Handle continue button click."""
        if self.stage == "name":
            # Validate name
            if not self.player_name or len(self.player_name.strip()) == 0:
                print("Please enter a name!")
                return
            
            # Move to devil fruit selection
            self._setup_devil_fruit_stage()
            
        elif self.stage == "devil_fruit":
            # Move to confirmation
            self._setup_confirm_stage()
            self._update_preview()
    
    def _on_back(self):
        """Handle back button click."""
        if self.stage == "devil_fruit":
            # Go back to name entry
            self._setup_name_stage()
        elif self.stage == "name":
            # Exit to main menu
            print("Character creation: Exiting to main menu")
            self.state_manager.change_state(STATE_MENU)
    
    def _on_confirm(self):
        """Handle confirm button - create character and start game."""
        print("\n" + "="*60)
        print("CONFIRM BUTTON CLICKED - Starting character creation...")
        print("="*60)

        # Create the player
        player = Player(self.player_name, level=1)
        print(f"✓ Player object created: {player.name}")

        # Equip Devil Fruit if selected
        if self.selected_fruit_data:
            player.equip_devil_fruit(self.selected_fruit_data)
            print(f"✓ {player.name} ate the {self.selected_fruit_data.get('name')}!")
        else:
            print(f"✓ {player.name} starts without a Devil Fruit!")

        # Store player for cleanup to pass to world state
        self.created_player = player
        print(f"✓ Player stored in self.created_player")

        print(f"\n📋 Character Summary:")
        print(f"   Name: {player.name}")
        print(f"   Level: {player.level}")
        print(f"   Devil Fruit: {player.devil_fruit.name if player.devil_fruit else 'None'}")

        # Save the character to character directory
        print(f"\n💾 Saving character to save file...")
        save_manager = get_save_manager()
        character_data = player.to_dict()

        # Save to character's directory (slot 1 by default for new characters)
        save_slot = 1
        print(f"   Creating character directory: {player.name}")
        print(f"   Using save slot {save_slot}")

        if save_manager.save_game(character_data, character_name=player.name, slot=save_slot):
            print(f"✓ Character saved successfully to {player.name}/save_{save_slot}.json!")
        else:
            print(f"✗ Failed to save character (game will continue)")

        print(f"\n🎮 Transitioning to world state...")
        print("="*60 + "\n")

        # Transition to world state - player data will be passed via cleanup()
        self.state_manager.change_state("world")

    def _on_cancel(self):
        """Handle cancel button - go back to previous stage or main menu."""
        if self.stage == "confirm":
            # Go back to devil fruit selection
            self._setup_devil_fruit_stage()
        elif self.stage == "devil_fruit":
            # Go back to name entry
            self._setup_name_stage()
        elif self.stage == "name":
            # Go back to main menu
            self.state_manager.change_state(STATE_MENU)
    
    def handle_event(self, event: pygame.event.Event):
        """
        Handle input events.

        Args:
            event: Pygame event
        """
        # ESC key - return to main menu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Character creation: ESC pressed - returning to main menu")
                self.state_manager.change_state(STATE_MENU)
                return

        # Handle text input for name
        if self.stage == "name" and self.input_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                    self._update_name_display()
                elif event.key == pygame.K_RETURN:
                    # Enter key - continue
                    self._on_continue()
                elif len(self.player_name) < self.max_name_length:
                    # Add character if valid
                    char = event.unicode
                    if char.isprintable() and (char.isalnum() or char.isspace()):
                        self.player_name += char
                        self._update_name_display()
        
        # Handle fruit selection navigation
        elif self.stage == "devil_fruit":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # Select previous fruit
                    new_index = max(0, self.selected_fruit_index - 1)
                    self._select_fruit(new_index)
                    
                    # Scroll if needed
                    if new_index < self.fruit_scroll_offset:
                        self.fruit_scroll_offset = new_index
                        
                elif event.key == pygame.K_DOWN:
                    # Select next fruit
                    new_index = min(len(self.fruit_list) - 1, self.selected_fruit_index + 1)
                    self._select_fruit(new_index)
                    
                    # Scroll if needed
                    if new_index >= self.fruit_scroll_offset + self.max_visible_fruits:
                        self.fruit_scroll_offset = new_index - self.max_visible_fruits + 1
        
        # Handle button clicks
        for button in self.buttons:
            if button.visible:
                button.handle_event(event)
        
        # Handle type filter buttons
        if self.stage == "devil_fruit":
            for button in self.type_buttons:
                button.handle_event(event)
    
    def _update_name_display(self):
        """Update the name input display."""
        display_text = self.player_name if self.player_name else "Type here..."
        color = WHITE if self.player_name else GRAY
        
        self.name_input_box = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=250,
            text=display_text,
            font_size=36,
            color=color,
            centered=True
        )
    
    def update(self, dt: float):
        """
        Update state logic.
        
        Args:
            dt: Delta time
        """
        # Update buttons
        for button in self.buttons:
            if button.visible:
                button.update(dt)
        
        # Update type buttons
        if self.stage == "devil_fruit":
            for button in self.type_buttons:
                button.update(dt)
        
        # Update preview components
        if self.stage in ["devil_fruit", "confirm"]:
            self.character_preview.update(dt)
            self.stat_display.update(dt)
    
    def render(self, screen: pygame.Surface):
        """
        Render the character creation screen.
        
        Args:
            screen: Pygame surface to render to
        """
        # Clear screen
        screen.fill(BLACK)
        
        # Render title
        self.title_text.render(screen)
        
        # Render stage-specific content
        if self.stage == "name":
            self._render_name_stage(screen)
        elif self.stage == "devil_fruit":
            self._render_devil_fruit_stage(screen)
        elif self.stage == "confirm":
            self._render_confirm_stage(screen)
        
        # Render buttons
        for button in self.buttons:
            if button.visible:
                button.render(screen)
    
    def _render_name_stage(self, screen: pygame.Surface):
        """Render name input stage."""
        # Main panel
        self.main_panel.render(screen)
        
        # Instruction
        self.instruction_text.render(screen)
        
        # Name input box
        self.name_input_box.render(screen)
        
        # Hint text
        hint = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=320,
            text="Press Enter to continue",
            font_size=18,
            color=GRAY,
            centered=True
        )
        hint.render(screen)
    
    def _render_devil_fruit_stage(self, screen: pygame.Surface):
        """Render Devil Fruit selection stage."""
        # Main panel
        self.main_panel.render(screen)
        
        # Preview panel
        self.preview_panel.render(screen)
        
        # Instruction
        self.instruction_text.render(screen)
        
        # Type filter buttons (first 5 are type filters, last 2 are random buttons)
        for i, button in enumerate(self.type_buttons):
            # Highlight selected filter (only for first 5 buttons)
            if i < 5:
                if (i == 0 and self.fruit_type_filter == "all") or \
                   (i == 1 and self.fruit_type_filter == "paramecia") or \
                   (i == 2 and self.fruit_type_filter == "zoan") or \
                   (i == 3 and self.fruit_type_filter == "logia") or \
                   (i == 4 and self.fruit_type_filter == "none"):
                    button.color = UI_HIGHLIGHT_COLOR
                else:
                    button.color = UI_BG_COLOR
            else:
                # Random buttons keep default color
                button.color = UI_BG_COLOR

            button.render(screen)
        
        # Fruit list panel
        if self.fruit_info_panel:
            self.fruit_info_panel.render(screen)
        
        # Render fruit list
        self._render_fruit_list(screen)
        
        # Render fruit details
        self._render_fruit_details(screen)
        
        # Render preview
        self.character_preview.render(screen)
        self.stat_display.render(screen)
    
    def _render_fruit_list(self, screen: pygame.Surface):
        """Render the scrollable fruit list."""
        if self.fruit_type_filter == "none":
            # Show "No Devil Fruit" option
            no_fruit_text = CenteredText(
                x=SCREEN_WIDTH // 2 - 350,
                y=310,
                text="[No Devil Fruit - Can Swim!]",
                font_size=24,
                color=UI_HIGHLIGHT_COLOR,
                centered=False
            )
            no_fruit_text.render(screen)
            return

        if not self.fruit_list:
            # No fruits available
            no_fruits_text = CenteredText(
                x=SCREEN_WIDTH // 2 - 350,
                y=310,
                text="No fruits available",
                font_size=20,
                color=GRAY,
                centered=False
            )
            no_fruits_text.render(screen)
            return

        # Render visible fruits (adjusted for random buttons)
        list_start_y = 290
        item_height = 35
        
        visible_start = self.fruit_scroll_offset
        visible_end = min(len(self.fruit_list), visible_start + self.max_visible_fruits)
        
        for i in range(visible_start, visible_end):
            fruit = self.fruit_list[i]
            y_pos = list_start_y + (i - visible_start) * item_height
            
            # Highlight selected fruit
            is_selected = (i == self.selected_fruit_index)
            
            if is_selected:
                # Draw selection background
                selection_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - 370,
                    y_pos - 5,
                    250,
                    30
                )
                pygame.draw.rect(screen, UI_HIGHLIGHT_COLOR, selection_rect, 2)
            
            # Fruit name
            fruit_name = fruit.get("name", "Unknown")
            color = WHITE if is_selected else LIGHT_GRAY
            
            fruit_text = CenteredText(
                x=SCREEN_WIDTH // 2 - 360,
                y=y_pos,
                text=fruit_name,
                font_size=18 if is_selected else 16,
                color=color,
                centered=False
            )
            fruit_text.render(screen)
        
        # Scroll indicator
        if len(self.fruit_list) > self.max_visible_fruits:
            scroll_text = CenteredText(
                x=SCREEN_WIDTH // 2 - 100,
                y=list_start_y + self.max_visible_fruits * item_height + 10,
                text=f"({visible_start + 1}-{visible_end} of {len(self.fruit_list)})",
                font_size=14,
                color=GRAY,
                centered=False
            )
            scroll_text.render(screen)
    
    def _render_fruit_details(self, screen: pygame.Surface):
        """Render details of selected fruit."""
        if self.fruit_type_filter == "none" or not self.selected_fruit_data:
            return
        
        fruit = self.selected_fruit_data
        
        # Translation
        translation = fruit.get("translation", "")
        if translation:
            trans_text = CenteredText(
                x=SCREEN_WIDTH // 2 - 70,
                y=300,
                text=f"({translation})",
                font_size=18,
                color=CYAN,
                centered=False
            )
            trans_text.render(screen)

        # Description
        description = fruit.get("description", "")
        # Wrap text
        desc_lines = self._wrap_text(description, 35)
        for i, line in enumerate(desc_lines[:3]):  # Max 3 lines
            desc_text = CenteredText(
                x=SCREEN_WIDTH // 2 - 70,
                y=330 + i * 22,
                text=line,
                font_size=16,
                color=WHITE,
                centered=False
            )
            desc_text.render(screen)

        # Type/Rarity
        fruit_type = fruit.get("type", "paramecia").capitalize()
        rarity = fruit.get("rarity", "Common")

        type_text = CenteredText(
            x=SCREEN_WIDTH // 2 - 70,
            y=410,
            text=f"Type: {fruit_type}",
            font_size=16,
            color=YELLOW,
            centered=False
        )
        type_text.render(screen)

        rarity_text = CenteredText(
            x=SCREEN_WIDTH // 2 - 70,
            y=435,
            text=f"Rarity: {rarity}",
            font_size=16,
            color=YELLOW,
            centered=False
        )
        rarity_text.render(screen)

        # Starting abilities
        abilities = fruit.get("abilities", [])
        starting_abilities = [a for a in abilities if a.get("level_required", 1) == 1]

        if starting_abilities:
            ability_header = CenteredText(
                x=SCREEN_WIDTH // 2 - 70,
                y=470,
                text="Starting Abilities:",
                font_size=16,
                color=GREEN,
                centered=False
            )
            ability_header.render(screen)

            for i, ability in enumerate(starting_abilities[:2]):  # Max 2 (reduced from 3)
                ability_name = ability.get("name", "Unknown")
                ability_text = CenteredText(
                    x=SCREEN_WIDTH // 2 - 60,
                    y=495 + i * 22,
                    text=f"• {ability_name}",
                    font_size=14,
                    color=LIGHT_GRAY,
                    centered=False
                )
                ability_text.render(screen)
    
    def _render_confirm_stage(self, screen: pygame.Surface):
        """Render confirmation stage."""
        # Main panel
        self.main_panel.render(screen)
        
        # Preview panel
        self.preview_panel.render(screen)
        
        # Instruction
        self.instruction_text.render(screen)
        
        # Character summary
        name_text = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=220,
            text=f"Name: {self.player_name}",
            font_size=28,
            color=WHITE,
            centered=True
        )
        name_text.render(screen)
        
        fruit_name = "None (Can Swim!)" if not self.selected_fruit_data else self.selected_fruit_data.get("name", "Unknown")
        fruit_text = CenteredText(
            x=SCREEN_WIDTH // 2,
            y=260,
            text=f"Devil Fruit: {fruit_name}",
            font_size=24,
            color=CYAN if self.selected_fruit_data else GREEN,
            centered=True
        )
        fruit_text.render(screen)
        
        # Render preview
        self.character_preview.render(screen)
        self.stat_display.render(screen)
    
    def _wrap_text(self, text: str, max_chars: int) -> List[str]:
        """
        Wrap text to multiple lines.
        
        Args:
            text: Text to wrap
            max_chars: Maximum characters per line
        
        Returns:
            List of text lines
        """
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            if current_length + word_length + len(current_line) <= max_chars:
                current_line.append(word)
                current_length += word_length
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = word_length
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return lines
    
    def startup(self, persistent):
        """Called when state becomes active."""
        print("Entering Character Creation")
    
    def cleanup(self):
        """Called when state is removed."""
        print("\n" + "="*60)
        print("CHARACTER CREATION CLEANUP - Preparing data for next state")
        print("="*60)

        # Return created player if it exists
        if hasattr(self, 'created_player'):
            print(f"✓ Returning player data: {self.created_player.name}")
            print(f"   Level: {self.created_player.level}")
            print(f"   Devil Fruit: {self.created_player.devil_fruit.name if self.created_player.devil_fruit else 'None'}")
            print("="*60 + "\n")
            return {"player": self.created_player}
        else:
            print("⚠ No player data to return (character creation was cancelled)")
            print("="*60 + "\n")
            return {}
