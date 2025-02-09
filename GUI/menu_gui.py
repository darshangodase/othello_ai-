import pygame
import sys
from GUI.othello_gui import OthelloGUI, run_game
from GUI.button_gui import Button

# Constants and colors
WIDTH, HEIGHT = 480, 560
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
GREEN_COLOR = (0, 128, 0)
SUBMENU_SPACING = 75  # Increase the vertical spacing between submenu buttons
BACKGROUND_IMAGE_PATH = "./utils/pictures/othello_blurred.jpg"


class Menu:
    def __init__(self):
        """
        A class representing the main menu of the Othello game.

        Attributes:
            win (pygame.Surface): The Pygame window.
            menu_font (pygame.font.Font): The font used for rendering the menu items.
            menu_items (list): The list of menu items displayed on the main menu.
            submenu_items (list): The list of submenu items displayed after selecting "Start Game".
            return_button (Button): The button to return to the main menu from the credit screen.
        """
        self.win = self.initialize_pygame()
        self.menu_font = pygame.font.SysFont(None, 36)
        self.menu_items = ["Start Game", "Exit"]
        # self.menu_items = ["Start Game", "Credit", "Exit"]
        self.submenu_items = [
            "Multi-player\n(Play with Friend)",
            "Single-player\n(Play with AI)",
            "Return to Main Menu",  # Add "Return to Main Menu" option
        ]
        self.return_button = None
        self.background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        self.background_image = pygame.transform.scale(
            self.background_image, (WIDTH, HEIGHT)
        )

    def initialize_pygame(self):
        """
        Initialize Pygame and create a window for the main menu.

        Returns:
            pygame.Surface: The Pygame window.
        """
        pygame.init()
        win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Othello - Main Menu")
        return win

    def draw_menu(self):
        """
        Draw the main menu on the Pygame window.
        """
        self.win.blit(self.background_image, (0, 0))  # Draw the background image

        buttons = []
        for i, item in enumerate(self.menu_items):
            button = Button(
                WIDTH // 2, 200 + i * 50, 200, 40, item, self.menu_font
            )  # Adjust vertical position to accommodate the picture
            buttons.append(button)
            button.draw(self.win)

        pygame.display.update()
        self.handle_input_menu(buttons)

    def draw_submenu(self):
        """
        Draw the submenu on the Pygame window.
        """
        self.win.blit(self.background_image, (0, 0))  # Draw the background image

        buttons = []
        num_submenu_items = len(self.submenu_items)
        submenu_height = num_submenu_items * SUBMENU_SPACING
        submenu_top_margin = (HEIGHT - submenu_height) // 2

        for i, item in enumerate(self.submenu_items):
            button_y = submenu_top_margin + i * SUBMENU_SPACING
            button = Button(
                WIDTH // 2, button_y, 200, 30, item, self.menu_font
            )  # Adjust height to 30
            buttons.append(button)
            button.draw(self.win)

        pygame.display.update()
        self.handle_input_submenu(buttons)

   
    def handle_input_menu(self, buttons):
        """
        Handle input events for the main menu.

        Parameters:
            buttons (list): The list of buttons in the main menu.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for button in buttons:
                        if button.check_collision((x, y)):
                            if button.text == "Start Game":
                                self.draw_submenu()
                            # elif button.text == "Credit":
                            #     self.draw_credit()
                            elif button.text == "Exit":
                                pygame.quit()
                                sys.exit()

    def handle_input_submenu(self, buttons):
        """
        Handle input events for the submenu.

        Parameters:
            buttons (list): The list of buttons in the submenu.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for button in buttons:
                        if button.check_collision((x, y)):
                            if button.text == "Multi-player\n(Play with Friend)":
                                othello_gui = OthelloGUI()
                                # Pass the draw_menu function as a callback to return to the main menu
                                othello_gui.run_game(
                                    return_to_menu_callback=self.draw_menu
                                )

                            elif button.text == "Single-player\n(Play with AI)":
                                othello_gui = OthelloGUI(player_mode="ai")
                                # Pass the draw_menu function as a callback to return to the main menu
                                othello_gui.run_game(
                                    return_to_menu_callback=self.draw_menu
                                )

                            elif button.text == "Return to Main Menu":
                                self.draw_menu()  # Go back to the main menu

    def run_single_player_game(self):
        """
        Start a single-player game with AI.
        """
        # Pass "ai" as the player_mode to indicate the single-player mode with AI
        othello_gui = OthelloGUI(player_mode="ai")
        othello_gui.run_game()


    def perform_action(self, action):
        """
        Perform the specified action.

        Parameters:
            action (callable): The function to be called as the action.
        """
        if action is None:
            pygame.quit()
            sys.exit()
        else:
            action()


def run_menu():
    """
    Start the main menu of the Othello game.
    """
    menu = Menu()
    menu.draw_menu()