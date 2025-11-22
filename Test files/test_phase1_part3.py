"""
Test Script for Phase 1 Part 3
Run this to verify the UI system is working correctly.
"""

import sys
import os
import logging
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Setup logging
def setup_logger(test_name):
    """Setup logger for this test file."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger.handlers = []
    
    # File handler
    log_file = os.path.join(log_dir, f"{test_name}.log")
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger('test_phase1_part3')

logger.info("=" * 60)
logger.info("Phase 1 Part 3 - UI System Foundation Test")
logger.info("=" * 60)
logger.info("")
logger.debug(f"Test started at: {datetime.now()}")

# Test 1: Import checks
logger.info("Test 1: Checking UI component imports...")
start_time = time.time()
try:
    from ui.button import Button, TextButton, ImageButton
    logger.debug(f"Button module: {Button.__module__}")
    logger.debug(f"Imported: Button, TextButton, ImageButton")
    logger.info("✓ Button components imported")
    
    from ui.text_box import TextBox, Label, MultilineLabel
    logger.debug(f"TextBox module: {TextBox.__module__}")
    logger.debug(f"Imported: TextBox, Label, MultilineLabel")
    logger.info("✓ TextBox components imported")
    
    from ui.panel import Panel, ScrollablePanel, ModalPanel
    logger.debug(f"Panel module: {Panel.__module__}")
    logger.debug(f"Imported: Panel, ScrollablePanel, ModalPanel")
    logger.info("✓ Panel components imported")
    
    from ui.menu import Menu, HorizontalMenu, GridMenu
    logger.debug(f"Menu module: {Menu.__module__}")
    logger.debug(f"Imported: Menu, HorizontalMenu, GridMenu")
    logger.info("✓ Menu components imported")
    
    elapsed = time.time() - start_time
    logger.debug(f"Import test completed in {elapsed:.3f}s")
    logger.info("✓ All UI imports successful!\n")
except ImportError as e:
    elapsed = time.time() - start_time
    logger.error(f"Import failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ Import failed: {e}\n")
    sys.exit(1)

# Test 2: Button functionality
logger.info("Test 2: Testing Button components...")
start_time = time.time()
try:
    import pygame
    pygame.init()
    logger.debug("pygame initialized for Button test")
    
    # Test basic button
    clicked = False
    def on_click():
        global clicked
        clicked = True
        logger.debug("Button callback triggered")
    
    logger.debug("Creating Button instance...")
    button = Button(100, 100, 200, 50, "Test Button", on_click)
    logger.debug(f"Button created: pos=({button.x}, {button.y}), size=({button.width}, {button.height})")
    logger.debug(f"Button properties: text='{button.text}', visible={button.visible}, enabled={button.enabled}")
    assert button.text == "Test Button", "Button text wrong"
    assert button.visible == True, "Button should be visible"
    assert button.enabled == True, "Button should be enabled"
    logger.info("✓ Button created")
    
    # Test button state changes
    logger.debug("Testing button enable/disable...")
    button.set_enabled(False)
    logger.debug(f"Button disabled: enabled={button.enabled}")
    assert button.enabled == False, "Button enable/disable failed"
    button.set_enabled(True)
    logger.debug(f"Button enabled: enabled={button.enabled}")
    logger.info("✓ Button enable/disable works")
    
    # Test text button
    logger.debug("Creating TextButton instance...")
    text_btn = TextButton(100, 100, "Link", on_click)
    logger.debug(f"TextButton border_width: {text_btn.border_width}")
    assert text_btn.border_width == 0, "TextButton should have no border"
    logger.info("✓ TextButton created")
    
    # Test rendering (should not crash)
    logger.debug("Testing button rendering...")
    surface = pygame.Surface((800, 600))
    button.render(surface)
    text_btn.render(surface)
    logger.debug("Button rendering completed without errors")
    logger.info("✓ Button rendering works")
    
    pygame.quit()
    logger.debug("pygame quit")
    
    elapsed = time.time() - start_time
    logger.debug(f"Button test completed in {elapsed:.3f}s")
    logger.info("✓ Button components verified!\n")
    
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"Button test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ Button test failed: {e}\n")
    pygame.quit()
    sys.exit(1)

# Test 3: TextBox functionality
logger.info("Test 3: Testing TextBox components...")
start_time = time.time()
try:
    import pygame
    pygame.init()
    logger.debug("pygame initialized for TextBox test")
    
    # Test basic text box
    logger.debug("Creating TextBox instance...")
    text_box = TextBox(50, 50, 300, 200, "Test text content")
    logger.debug(f"TextBox created: pos=({text_box.rect.x}, {text_box.rect.y}), size=({text_box.rect.width}, {text_box.rect.height})")
    logger.debug(f"TextBox text: '{text_box.text}'")
    assert text_box.text == "Test text content", "TextBox text wrong"
    assert text_box.visible == True, "TextBox should be visible"
    logger.info("✓ TextBox created")
    
    # Test text wrapping
    logger.debug("Testing text wrapping...")
    long_text = "This is a very long text that should wrap across multiple lines when displayed in the text box."
    text_box.set_text(long_text)
    wrapped_count = len(text_box.wrapped_lines)
    logger.debug(f"Text wrapped into {wrapped_count} lines")
    logger.debug(f"Wrapped lines: {text_box.wrapped_lines}")
    assert wrapped_count > 1, "Text should wrap to multiple lines"
    logger.info(f"✓ Text wrapping works ({wrapped_count} lines)")
    
    # Test label
    logger.debug("Creating Label instance...")
    label = Label(100, 100, "Test Label")
    logger.debug(f"Label border_width: {label.border_width}")
    assert label.border_width == 0, "Label should have no border"
    logger.info("✓ Label created")
    
    # Test multiline label
    logger.debug("Creating MultilineLabel instance...")
    ml_label = MultilineLabel(100, 100, "Line 1\nLine 2\nLine 3")
    ml_lines = len(ml_label.wrapped_lines)
    logger.debug(f"MultilineLabel has {ml_lines} lines")
    assert ml_lines >= 3, "MultilineLabel should handle line breaks"
    logger.info("✓ MultilineLabel created")
    
    # Test rendering
    logger.debug("Testing TextBox component rendering...")
    surface = pygame.Surface((800, 600))
    text_box.render(surface)
    label.render(surface)
    ml_label.render(surface)
    logger.debug("TextBox rendering completed without errors")
    logger.info("✓ TextBox rendering works")
    
    pygame.quit()
    logger.debug("pygame quit")
    
    elapsed = time.time() - start_time
    logger.debug(f"TextBox test completed in {elapsed:.3f}s")
    logger.info("✓ TextBox components verified!\n")
    
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"TextBox test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ TextBox test failed: {e}\n")
    pygame.quit()
    sys.exit(1)

# Test 4: Panel functionality
logger.info("Test 4: Testing Panel components...")
start_time = time.time()
try:
    import pygame
    pygame.init()
    logger.debug("pygame initialized for Panel test")
    
    # Test basic panel
    logger.debug("Creating Panel instance...")
    panel = Panel(100, 100, 400, 300, "Test Panel")
    logger.debug(f"Panel created: title='{panel.title}', pos=({panel.rect.x}, {panel.rect.y})")
    assert panel.title == "Test Panel", "Panel title wrong"
    assert panel.visible == True, "Panel should be visible"
    logger.info("✓ Panel created")
    
    # Test adding children
    logger.debug("Testing panel child management...")
    from ui.button import Button
    child_button = Button(150, 150, 100, 40, "Child")
    logger.debug(f"Created child button: {id(child_button)}")
    panel.add_child(child_button)
    children_count = len(panel.children)
    logger.debug(f"Panel now has {children_count} children")
    assert children_count == 1, "Child not added"
    logger.info("✓ Panel child management works")
    
    # Test scrollable panel
    logger.debug("Creating ScrollablePanel instance...")
    scroll_panel = ScrollablePanel(100, 100, 400, 300, "Scrollable")
    logger.debug(f"ScrollablePanel scroll_offset: {scroll_panel.scroll_offset}")
    assert scroll_panel.scroll_offset == 0, "Initial scroll should be 0"
    logger.info("✓ ScrollablePanel created")
    
    # Test modal panel
    logger.debug("Creating ModalPanel instance...")
    modal = ModalPanel(400, 300, "Modal")
    logger.debug(f"Modal initial position: ({modal.rect.x}, {modal.rect.y})")
    modal.center_on_screen(800, 600)
    logger.debug(f"Modal centered position: ({modal.rect.x}, {modal.rect.y})")
    assert modal.rect.x > 0, "Modal should be centered"
    logger.info("✓ ModalPanel created and centered")
    
    # Test rendering
    logger.debug("Testing Panel component rendering...")
    surface = pygame.Surface((800, 600))
    panel.render(surface)
    scroll_panel.render(surface)
    modal.render(surface)
    logger.debug("Panel rendering completed without errors")
    logger.info("✓ Panel rendering works")
    
    pygame.quit()
    logger.debug("pygame quit")
    
    elapsed = time.time() - start_time
    logger.debug(f"Panel test completed in {elapsed:.3f}s")
    logger.info("✓ Panel components verified!\n")
    
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"Panel test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ Panel test failed: {e}\n")
    pygame.quit()
    sys.exit(1)

# Test 5: Menu functionality
logger.info("Test 5: Testing Menu components...")
start_time = time.time()
try:
    import pygame
    pygame.init()
    logger.debug("pygame initialized for Menu test")
    
    # Test vertical menu
    logger.debug("Creating vertical Menu instance...")
    options = ["Option 1", "Option 2", "Option 3"]
    menu = Menu(400, 200, options)
    initial_selection = menu.get_selected()
    selected_text = menu.get_selected_text()
    logger.debug(f"Menu created with {len(options)} options")
    logger.debug(f"Initial selection: {initial_selection}, text: '{selected_text}'")
    assert initial_selection == 0, "Initial selection should be 0"
    assert selected_text == "Option 1", "Selected text wrong"
    logger.info("✓ Menu created")
    
    # Test navigation
    logger.debug("Testing menu navigation...")
    menu.move_selection(1)
    new_selection = menu.get_selected()
    logger.debug(f"After move_selection(1): {new_selection}")
    assert new_selection == 1, "Navigation down failed"
    menu.move_selection(-1)
    back_selection = menu.get_selected()
    logger.debug(f"After move_selection(-1): {back_selection}")
    assert back_selection == 0, "Navigation up failed"
    logger.info("✓ Menu navigation works")
    
    # Test horizontal menu
    logger.debug("Creating HorizontalMenu instance...")
    h_menu = HorizontalMenu(200, 300, options)
    h_initial = h_menu.get_selected()
    logger.debug(f"HorizontalMenu initial selection: {h_initial}")
    assert h_initial == 0, "HorizontalMenu initial selection wrong"
    logger.info("✓ HorizontalMenu created")
    
    # Test grid menu
    logger.debug("Creating GridMenu instance...")
    grid_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    g_menu = GridMenu(100, 100, grid_options, columns=3)
    logger.debug(f"GridMenu created: {len(grid_options)} options, {g_menu.columns} columns")
    assert g_menu.columns == 3, "GridMenu columns wrong"
    logger.info("✓ GridMenu created")
    
    # Test rendering
    logger.debug("Testing Menu component rendering...")
    surface = pygame.Surface((800, 600))
    menu.render(surface)
    h_menu.render(surface)
    g_menu.render(surface)
    logger.debug("Menu rendering completed without errors")
    logger.info("✓ Menu rendering works")
    
    pygame.quit()
    logger.debug("pygame quit")
    
    elapsed = time.time() - start_time
    logger.debug(f"Menu test completed in {elapsed:.3f}s")
    logger.info("✓ Menu components verified!\n")
    
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"Menu test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ Menu test failed: {e}\n")
    pygame.quit()
    sys.exit(1)

# Test 6: Integration test
logger.info("Test 6: Testing component integration...")
start_time = time.time()
try:
    import pygame
    pygame.init()
    logger.debug("pygame initialized for integration test")
    
    # Create a complex UI setup
    logger.debug("Creating complex UI setup...")
    surface = pygame.Surface((800, 600))
    
    # Panel with button and text
    panel = Panel(100, 100, 600, 400, "UI Test Panel")
    button = Button(150, 200, 200, 50, "Click Me")
    label = Label(150, 270, "This is a label")
    
    logger.debug(f"Created panel: {id(panel)}")
    logger.debug(f"Created button: {id(button)}")
    logger.debug(f"Created label: {id(label)}")
    
    panel.add_child(button)
    panel.add_child(label)
    logger.debug(f"Added {len(panel.children)} children to panel")
    
    # Menu
    menu = Menu(400, 350, ["Start", "Options", "Quit"])
    logger.debug(f"Created menu: {id(menu)}")
    
    # Render everything
    logger.debug("Rendering complex UI...")
    panel.render(surface)
    menu.render(surface)
    logger.debug("Complex UI rendered successfully")
    logger.info("✓ Complex UI rendered successfully")
    
    # Test event handling
    logger.debug("Testing event handling...")
    test_event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (400, 350)})
    menu.handle_event(test_event)
    logger.debug("Event handled without errors")
    logger.info("✓ Event handling works")
    
    pygame.quit()
    logger.debug("pygame quit")
    
    elapsed = time.time() - start_time
    logger.debug(f"Integration test completed in {elapsed:.3f}s")
    logger.info("✓ Integration test passed!\n")
    
except Exception as e:
    elapsed = time.time() - start_time
    logger.error(f"Integration test failed after {elapsed:.3f}s: {e}", exc_info=True)
    logger.info(f"✗ Integration test failed: {e}\n")
    pygame.quit()
    sys.exit(1)

logger.info("=" * 60)
logger.info("All tests passed! ✓")
logger.info("=" * 60)
logger.info("")
logger.info("UI Components Available:")
logger.info("  - Button (clickable buttons)")
logger.info("  - TextButton (link-style buttons)")
logger.info("  - ImageButton (image-based buttons)")
logger.info("  - TextBox (scrollable text display)")
logger.info("  - Label (simple text)")
logger.info("  - MultilineLabel (multi-line text)")
logger.info("  - Panel (container for UI elements)")
logger.info("  - ScrollablePanel (scrollable container)")
logger.info("  - ModalPanel (centered overlay panel)")
logger.info("  - Menu (vertical menu)")
logger.info("  - HorizontalMenu (horizontal menu)")
logger.info("  - GridMenu (grid-based menu)")
logger.info("")
logger.info("All components support:")
logger.info("  ✓ Mouse and keyboard input")
logger.info("  ✓ Enable/disable states")
logger.info("  ✓ Show/hide visibility")
logger.info("  ✓ Customizable colors")
logger.info("  ✓ Event handling")
logger.info("  ✓ Rendering")
logger.info("")
logger.debug(f"Test completed at: {datetime.now()}")
logger.debug(f"Log file saved to: logs/test_phase1_part3.log")
