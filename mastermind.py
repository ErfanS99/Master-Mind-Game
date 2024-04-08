"""
The Mastermind game is a Python program with a GUI where you guess a secret code of colors. 
You get feedback on your guesses and try to crack the code. 
Just click colors, submit your guess, and see if you are right!
Install Python, run the code, and play the game. 
It is fun and challenging!
"""

import random  # Importing the random module for generating random values
import tkinter as tk  # Importing the tkinter module for GUI
from collections import Counter  # Importing Counter for advanced counting operations

# Mapping of color values to color names
COLORS = {  # Dictionary to map color values to color names
    1: "red",
    2: "blue",
    3: "green",
    4: "yellow",
    5: "orange",
    6: "purple"
}

class Checker:
    """Class responsible for checking the correctness of a guess."""
    
    @staticmethod
    def check_guess(secret_code:list[int], guess:list[int]) -> tuple[int, int, dict]:
        """Check the guess against the secret code and calculate correct positions and colors."""
        correct_positions = {}  # Dictionary to store correct positions
        for i in range(len(secret_code)):  # Loop through the secret code
            if secret_code[i] == guess[i]:  # Check if code matches guess
                correct_positions[i] = COLORS[secret_code[i]]  # Store correct position and color
        correct_positions_num = len(correct_positions)  # Count of correct positions
        
        secret_freq = {}  # Dictionary to store frequency of colors in secret code
        guess_freq = {}  # Dictionary to store frequency of colors in guess
        for i in range(len(secret_code)):  # Iterate through secret code
            secret_freq[secret_code[i]] = secret_freq.get(secret_code[i], 0) + 1  # Count frequency of colors in secret code
            guess_freq[guess[i]] = guess_freq.get(guess[i], 0) + 1  # Count frequency of colors in guess
        
        # Calculate total correct colors excluding correct positions
        total_correct_colors = sum(min(secret_freq.get(color, 0), count) for color, count in guess_freq.items())
        correct_colors = total_correct_colors - correct_positions_num  # Count of correct colors
        
        return correct_positions_num, correct_colors, correct_positions  # Return results of checking

class Board:
    """Class representing the game board, storing the secret code and player guesses."""
    
    def __init__(self):
        """Initialize the game board with a randomly generated secret code and an empty list of guesses."""
        self.secret_code = [random.choice(list(COLORS.keys())) for _ in range(4)]  # Generate secret code
        self.guesses = []  # Initialize empty list to store guesses

    def add_guess(self, guess):
        """Add a player's guess to the list of guesses."""
        self.guesses.append(guess)  # Append player's guess to the list

class Display:
    """Class representing the GUI display for the Mastermind game."""
    
    def __init__(self, root: tk, board: Board):
        """Initialize the GUI with labels, color selection buttons, and submit button."""
        self.root = root  # Set the root window for GUI
        self.root.geometry("375x110")  # Set window size
        self.root.title("Mastermind Game")  # Set window title
        self.board = board  # Store the game board
        self.turn_label = tk.Label(self.root, text=f"Turn: {len(self.board.guesses) + 1}")  # Label to display turn
        self.turn_label.pack()  # Place turn label in the GUI
        text = u"\U00002B24 " * 4  # Unicode character for peg symbol
        self.secret_label = tk.Label(self.root, text="Secret Code: " + text)  # Label for secret code
        self.secret_label.pack()  # Place secret code label in the GUI

        self.guess_label = tk.Label(self.root, text="Your Guess:")  # Label for player's guess
        self.guess_label.pack()  # Place guess label in the GUI

        self.color_buttons = []  # List to store color selection buttons

        # Create color selection buttons based on COLORS dictionary
        for color in COLORS.values():
            button = tk.Button(self.root, bg=color, width=2, height=1, command=lambda c=color: self.select_color(c))
            button.pack(side=tk.LEFT)  # Align buttons horizontally
            self.color_buttons.append(button)  # Append button to the list of color buttons

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_guess)  # Submit button
        self.submit_button.pack()  # Place submit button in the GUI

        self.result_label = tk.Label(self.root, text="")  # Label to display game results
        self.result_label.pack()  # Place result label in the GUI

        self.selected_colors = []  # List to store selected colors by the player

    def select_color(self, color):
        """Select a color for the guess when a color button is clicked."""
        
        if len(self.selected_colors) < 4:  # Allowing selection of up to 4 colors
            self.selected_colors.append(color)  # Append selected color
            self.update_guess_label()  # Update GUI display with selected colors

    def update_guess_label(self):
        """Update the guess label to display the selected colors."""
        guess_str = " ".join(self.selected_colors)  # Create a string with selected colors
        self.guess_label.config(text=f"Your Guess: {guess_str}")  # Update the guess label with selected colors

    def submit_guess(self):
        """Handle the submission of a player's guess."""
        if len(self.selected_colors) < 4:  # Check if 4 colors are selected
            self.result_label.config(text="Please select 4 colors for your guess.")  # Prompt to select 4 colors
            return
        
        guess = []  # Initialize guess list
        for color in self.selected_colors:  # Map selected colors to values
            for key in list(COLORS.keys()):
                    if COLORS[key] == color:
                        guess.append(key)

        correct_positions_num, correct_colors, correct_positions = Checker.check_guess(self.board.secret_code, guess)  # Check guess
        self.board.add_guess(guess)  # Add guess to the board
        self.turn_label.config(text=f"Turn: {len(self.board.guesses) + 1}")  # Update turn label
        
        if correct_positions_num == 4:  # Check if all positions are correct
            self.result_label.config(text="Congratulations! You cracked the code.")  # Congratulate the player
        else:
            self.result_label.config(text=f"Correct positions: {correct_positions_num}, Correct colors: {correct_colors}")  # Display correct positions and colors
            text = ""  # Initialize text for secret code display
            if correct_positions_num > 0:  # Check if there are correct positions
                for j in range(len(guess)):
                    try: 
                        if correct_positions[j]:  # Display characters for correct positions
                            text += correct_positions[j] + " "
                    except KeyError:
                        text += u"\U00002B24 "  # Display peg symbol for correct colors that are not in the right position
                self.secret_label.config(text="Secret Code: " + text)  # Update secret code display
        
        self.selected_colors = []  # Reset selected colors
        for button in self.color_buttons:  # Reset color buttons
            button.config(relief=tk.RAISED)
        self.update_guess_label()  # Update guess label

if __name__ == "__main__":
    root = tk.Tk()  # Create the main tkinter window
    game_board = Board()  # Initialize the game board
    game_display = Display(root, game_board)  # Initialize the game display
    root.mainloop()  # Start the tkinter event loop