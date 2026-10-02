 # ASSIGNMENT 3: Interactive Desktop Puzzle Application
# Group Name 14

# Group Members:

# NAME                  STUDENT ID
# CHIDCHANOK TAEWTIM -  S408565
# BETTY JELAGAT -       S404210
# AYESHA BEGUM -        S408677


"""
This workflow demonstrates:
- Object-Oriented Programming (Abstraction, Encapsulation, Inheritance, and Polymorphism)
- OpenCV Image Processing (Image Loading, Resizing, Padding, Slicing, Transformations, and Overlays)
- Tkinter Graphical User Interface (Side-by-side Display, Mouse Events, Controls, Hints, and Score Tracking)
- Interactive Puzzle Mechanics (Tile Swapping, Rotation, Flipping, Selection, and Completion Detection)
- Difficulty Levels (Easy, Medium, and Hard)
- Timed Gameplay with Countdown and Time-limit Handling
- Dummy/Decoy Puzzle Items for Increased Difficulty
- Moving Puzzle Tiles at Higher Difficulty
- Grid-based Puzzle Generation for 3*3, 4*4, and 5*5 Puzzles
"""
 
#Import necessary libraries
import abc        # Abstract Base Class support for OOP design
import os         # Operating system interfaces
import random      # Random number generation
from typing import List, Tuple, Optional  # Type hinting support
import cv2        # OpenCV for image processing
import numpy as np  # Numerical operations on arrays
from PIL import Image  # Python Imaging Library for image manipulation. Image class provides a PIL representation of an image.

# Safely import Tkinter GUI components and ImageTk, with fallbacks if Tkinter is unavailable
try: # Attempt to import Tkinter and related GUI components
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox # Importing Tkinter themed widgets, file dialog, and message box components
    from PIL import ImageTk  # Importing ImageTk for displaying PIL images in Tkinter
    HAS_TKINTER = True  # Flag indicating that Tkinter is available
except ImportError:  # If Tkinter is not available, set all related variables to None
    HAS_TKINTER = False
    tk = None
    ttk = None
    filedialog = None
    messagebox = None
    ImageTk = None

# =============================================================================
# 1. OOP DESIGN: ABSTRACTION & POLYMORPHISM (TRANSFORMATIONS)
# =============================================================================


# TRANSFORMATION CLASSES (ROTATE, FLIP, SWAP)
class Transformation(abc.ABC):
    """
    Abstract Base Class for Tile Transformations.
    Demonstrates Abstraction and Polymorphism.
    """
    @abc.abstractmethod #Abstract method to apply the transformation to a tile.An abstract method defines a method that must be implemented by any subclass.
    def apply(self, tile: "Tile") -> None:   #function to apply the transformation to the tile
        """Apply transformation to the given tile."""
        pass   # To be implemented by subclasses

    @abc.abstractmethod              # Abstract method to get a human-readable description of the transformation
    def get_description(self) -> str: #Fuction definition to get a human-readable description of the transformation
        """Return human-readable string of the transformation."""
        pass

# ROTATE TRANSFORMATION CLASS
class RotateTransformation(Transformation):            
    """Polymorphic implementation of Tile Rotation."""
    def __init__(self, angle_degrees: int = 90): #Define a function to initialize the rotation transformation. The angle is specified in degrees and defaults to 90.
        self._angle = angle_degrees % 360       # Ensure the angle is within 0-359 degrees

    def apply(self, tile: "Tile") -> None: #Define a function to apply the rotation transformation to the tile
        tile.rotate(self._angle)           # Apply the rotation to the tile

    def get_description(self) -> str:    #Define a function to get a human-readable description of the rotation transformation
        return f"Rotate {self._angle}°"   # Return a human-readable description of the rotation transformation

# FLIP TRANSFORMATION CLASS
class FlipTransformation(Transformation):
    """Polymorphic implementation of Tile Flipping."""
    def __init__(self, direction: str = "horizontal"): #Define a function to initialize the flip transformation. The direction can be "horizontal" or "vertical" but defaults to "horizontal"
        self._direction = direction                           # Store the flip direction

    def apply(self, tile: "Tile") -> None: #Define a function to apply the flip transformation to the tile.
        tile.flip(self._direction)           # Apply the flip to the tile

    def get_description(self) -> str: #Define a function to get a human-readable description of the flip transformation
        return f"Flip {self._direction}"   # Return a human-readable description of the flip transformation     

# SWAP TRANSFORMATION CLASS
class SwapTransformation(Transformation):
    """Polymorphic implementation of Tile Position Swap."""
    def __init__(self, target_pos: Tuple[int, int]): #Define a function to initialize the swap transformation. The target position specifies the position to swap the tile to.The new position must be provided as a tuple (row, col).
        self._target_pos = target_pos                           # Store the target position for the swap

    def apply(self, tile: "Tile") -> None: #Define a function to apply the swap transformation to the tile.None of the tile's image data is modified; only its position is updated.
        tile.current_pos = self._target_pos           # Apply the swap to the tile

    def get_description(self) -> str: #Define a function to get a human-readable description of the swap transformation.
        return f"Swap to position {self._target_pos}"   # Return a human-readable description of the swap transformation

# =============================================================================
# 2. ENCAPSULATION: TILE & PUZZLE STATE
# =============================================================================

# TILE CLASS
class Tile:
    """
    Encapsulates a single puzzle tile's state and image data.
    """
    def __init__(self, tile_id: int, home_pos: Tuple[int, int], image_data: np.ndarray): #Define a function to initialize the tile with its ID, home position, and image data
        self._tile_id = tile_id                           # Store the tile ID
        self._home_pos = home_pos                           # Store the home position (row, col)
        self._current_pos = home_pos                        # Initialize the current position to the home position (row, col)
        self._original_image = image_data.copy()            # Store a copy of the original image data
        self._current_image = image_data.copy()             # Initialize the current image to the original image data
        self._rotation_angle = 0                               # Initialize rotation angle to 0 (0, 90, 180, 270)
        self._is_flipped_h = False                             # Initialize horizontal flip status to False
        self._is_flipped_v = False                             # Initialize vertical flip status to False

    @property        # Define a property to get the tile ID.  property allows you to access the tile ID as an attribute rather than calling a method.
    def tile_id(self) -> int: #Function to get the tile ID
        return self._tile_id     # Return the tile ID

    @property        # Define a property to get the home position
    def home_pos(self) -> Tuple[int, int]: #Function to get the home position
        return self._home_pos     # Return the home position (row, col)

    @property        # Define a property to get the current position
    def current_pos(self) -> Tuple[int, int]: #Function to get the current position
        return self._current_pos     # Return the current position (row, col)

    @current_pos.setter        # Define a setter for the current position
    def current_pos(self, pos: Tuple[int, int]) -> None: #Function to set the current position
        self._current_pos = pos     # Set the current position (row, col)

    @property        # Define a property to get the current image
    def current_image(self) -> np.ndarray: #Function to get the current image
        return self._current_image     # Return the current image data

    @property        # Define a property to get the rotation angle
    def rotation_angle(self) -> int: #Function to get the rotation angle
        return self._rotation_angle     # Return the rotation angle (0, 90, 180, 270)

    @property        # Define a property to get the horizontal flip status
    def is_flipped_h(self) -> bool: #Function to get the horizontal flip status
        return self._is_flipped_h     # Return the horizontal flip status (True/False)

    @property        # Define a property to get the vertical flip status
    def is_flipped_v(self) -> bool: #Function to get the vertical flip status
        return self._is_flipped_v     # Return the vertical flip status (True/False)        

    def is_correct(self) -> bool:          #Define a function to check if the tile is in its correct position, orientation, and flip status
        """Tile is correct if in home position, 0 deg rotation, and unflipped."""
        return (      # Check if the current position, rotation, and flip status match the correct state
            self._current_pos == self._home_pos and
            self._rotation_angle == 0 and
            not self._is_flipped_h and
            not self._is_flipped_v
        )

    def rotate(self, angle: int = 90) -> None:  # Define a function to rotate the tile by the specified angle (clockwise)
        """Function to rotate the tile clockwise by given angle (90, 180, 270)."""
        angle = angle % 360
        if angle == 90:
            self._current_image = cv2.rotate(self._current_image, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            self._current_image = cv2.rotate(self._current_image, cv2.ROTATE_180)
        elif angle == 270:
            self._current_image = cv2.rotate(self._current_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self._rotation_angle = (self._rotation_angle + angle) % 360

    def flip(self, direction: str = "horizontal") -> None:
        """Function to flip the tile horizontally or vertically using OpenCV."""
        if direction == "horizontal": #conditional statement for horizontal flip
            self._current_image = cv2.flip(self._current_image, 1) # Perform horizontal flip using OpenCV
            self._is_flipped_h = not self._is_flipped_h # Update the horizontal flip status
        elif direction == "vertical": #conditional statement for vertical flip
            self._current_image = cv2.flip(self._current_image, 0) # Perform vertical flip using OpenCV
            self._is_flipped_v = not self._is_flipped_v # Update the vertical flip status

    def reset_tile(self) -> None:
        """Function to reset the tile to its original image and position."""
        self._current_pos = self._home_pos
        self._current_image = self._original_image.copy()
        self._rotation_angle = 0
        self._is_flipped_h = False
        self._is_flipped_v = False


# =============================================================================
# 3. OPENCV IMAGE PROCESSING PIPELINE
# =============================================================================

# Class for handling OpenCV image processing operations
class ImageProcessor:
    """
    Handles all OpenCV image operations: loading, scaling, cropping/padding,
    grid slicing, and drawing overlays (ticks, hint circles, selection borders).
    """
    @staticmethod # Define a static method for loading and preprocessing images. A static method can be called on the class itself without creating an instance.
    def load_and_preprocess(image_path: str, grid_size: int, target_size: Tuple[int, int] = (450, 450)) -> Tuple[np.ndarray, np.ndarray]: #function to load and preprocess an image for the puzzle game
        """
        Loads an image (JPG, PNG, BMP), resizes with aspect ratio, and crops/pads
        so that width and height divide evenly by grid_size.
        Returns (original_display_image, processed_grid_image).
        """
        img = cv2.imread(image_path) # Load the image from the specified file path
        if img is None: # Check if the image was successfully loaded
            raise ValueError(f"Could not load image file: {image_path}. Check file format (JPG, PNG, BMP).") # Raise an error if the image could not be loaded

        h, w = img.shape[:2] # Get the original image height and width
        target_w, target_h = target_size # Unpack the target width and height from the target_size tuple

        # Preserve aspect ratio while resizing to fit target bounding box
        scale = min(target_w / w, target_h / h) # Calculate the scaling factor to preserve aspect ratio
        new_w, new_h = max(1, int(w * scale)), max(1, int(h * scale)) # Compute the new width and height after scaling
        resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA) # Resize the image using OpenCV with area interpolation

        # Pad image so dimensions are exact multiples of grid_size to ensure even slicing
        pad_w = (grid_size - (new_w % grid_size)) % grid_size # Calculate the required padding width
        pad_h = (grid_size - (new_h % grid_size)) % grid_size # Calculate the required padding height

        top = pad_h // 2 # Calculate top padding
        bottom = pad_h - top # Calculate bottom padding
        left = pad_w // 2 # Calculate left padding
        right = pad_w - left # Calculate right padding

        padded = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0]) # Apply padding to the resized image

        return img, padded # Return the original display image and the processed grid image

    @staticmethod # Indicates that the following method does not depend on instance state and can be called on the class itself
    def slice_into_tiles(image: np.ndarray, grid_size: int) -> List[Tile]:
        """Slices processed image into N x N numpy tile arrays and wraps in Tile objects.
        
        Args:
            image (np.ndarray): The processed image to be sliced into tiles.
            grid_size (int): The number of tiles along one dimension (N).

        Returns:
            List[Tile]: A list of Tile objects containing the sliced image data.
        """
        h, w = image.shape[:2] # Get the height and width of the image
        tile_h = h // grid_size # Calculate the height of each tile
        tile_w = w // grid_size # Calculate the width of each tile

        tiles = [] # Initialize an empty list to store the Tile objects
        tile_id = 0 # Initialize the tile ID counter
        for r in range(grid_size):
            for c in range(grid_size):
                y1, y2 = r * tile_h, (r + 1) * tile_h # Calculate the vertical slice boundaries for the current tile
                x1, x2 = c * tile_w, (c + 1) * tile_w # Calculate the horizontal slice boundaries for the current tile
                tile_data = image[y1:y2, x1:x2].copy() # Extract the tile image data
                tiles.append(Tile(tile_id=tile_id, home_pos=(r, c), image_data=tile_data)) # Create a Tile object and add it to the list
                tile_id += 1 # Increment the tile ID counter
        return tiles # Return the list of Tile objects

    @staticmethod # Indicates that the following method does not depend on instance state and can be called on the class itself
    def draw_grid_lines(canvas: np.ndarray, grid_size: int, color: Tuple[int, int, int] = (200, 200, 200), thickness: int = 1) -> np.ndarray: #function to draw grid lines on the canvas
        """Draws faint grid overlays across tile boundaries.

        Args:
            canvas (np.ndarray): The image on which to draw the grid lines.
            grid_size (int): The number of tiles along one dimension (N).
            color (Tuple[int, int, int], optional): The color of the grid lines in BGR format. Defaults to (200, 200, 200).
            thickness (int, optional): The thickness of the grid lines. Defaults to 1.

        Returns:
            np.ndarray: The image with the grid lines drawn.
        """
        out = canvas.copy() # Create a copy of the canvas to draw on
        h, w = out.shape[:2] # Get the height and width of the canvas
        tile_h = h // grid_size # Calculate the height of each tile
        tile_w = w // grid_size # Calculate the width of each tile

        for i in range(1, grid_size):# Draw the horizontal and vertical grid lines for each tile boundary
            cv2.line(out, (0, i * tile_h), (w, i * tile_h), color, thickness) # Draw horizontal grid line
            cv2.line(out, (i * tile_w, 0), (i * tile_w, h), color, thickness) # Draw vertical grid line
        return out  # Return the image with the grid lines drawn

    @staticmethod # Indicates that the following method does not depend on instance state and can be called on the class itself
    def draw_green_tick(tile_img: np.ndarray) -> np.ndarray: # Function that draws a small green tick mark overlay in the top-right corner of a completed tile
        """Draws a small green tick mark overlay in the top-right corner of a completed tile."""
        out = tile_img.copy() # Create a copy of the tile image to draw on
        h, w = out.shape[:2] # Get the height and width of the tile
        tick_color = (0, 230, 0) # Green in BGR
        thickness = max(2, min(h, w) // 25) # Determine the thickness of the tick mark based on tile size

        p1 = (int(w * 0.72), int(h * 0.22)) # First point of the tick mark
        p2 = (int(w * 0.80), int(h * 0.30)) # Second point of the tick mark
        p3 = (int(w * 0.92), int(h * 0.12)) # Third point of the tick mark

        cv2.line(out, p1, p2, tick_color, thickness, cv2.LINE_AA) # Draw the first segment of the tick mark
        cv2.line(out, p2, p3, tick_color, thickness, cv2.LINE_AA) # Draw the second segment of the tick mark
        return out # Return the image with the green tick mark drawn

    @staticmethod # Indicates that the following method does not depend on instance state and can be called on the class itself
    def draw_blue_circle(image_or_tile: np.ndarray, center: Tuple[int, int], radius: int) -> np.ndarray: # Function that draws a bright blue circle for hint overlays
        """Draws a bright blue circle for hint overlays."""
        out = image_or_tile.copy() # Create a copy of the image or tile to draw on
        blue_color = (255, 120, 0) # Blue in BGR
        cv2.circle(out, center, radius, blue_color, 3, cv2.LINE_AA) # Draw the blue circle
        return out # Return the image with the blue circle drawn

    @staticmethod # Indicates that the following method does not depend on instance state and can be called on the class itself
    def draw_selection_highlight(tile_img: np.ndarray, color: Tuple[int, int, int] = (0, 255, 255), thickness: int = 4) -> np.ndarray: # Function that draws a colored border around the selected tile
        """Draws a colored border around selected tile."""
        out = tile_img.copy() # Create a copy of the tile image to draw on
        cv2.rectangle(out, (0, 0), (out.shape[1] - 1, out.shape[0] - 1), color, thickness) # Draw the colored border
        return out # Return the image with the selection highlight drawn


# =============================================================================
# 4. GAME MANAGER / MODEL
# =============================================================================


# EXTENSIONS: DIFFICULTY SETTINGS AND DUMMY PUZZLE ITEMS


# Keep difficulty separate from grid size so each grid can use different difficulty levels.
DIFFICULTY_SETTINGS = {
    "Easy":   {"time_limit": 180, "hints": 3, "dummy_items": 0, "move_interval": 0}, # Easy difficulty settings
    "Medium": {"time_limit": 120, "hints": 2, "dummy_items": 1, "move_interval": 0}, # Medium difficulty settings
    "Hard":   {"time_limit": 90,  "hints": 1, "dummy_items": 2, "move_interval": 8}, # Hard difficulty settings
}

# CLASS FOR DUMMY PUZZLE ITEMS
class DummyPuzzleItem:
    """A temporary decoy placed over a puzzle position for Medium/Hard difficulty."""
    def __init__(self, position: Tuple[int, int]): #function to initialize a dummy puzzle item with its position
        self._position = position # Store the position of the dummy puzzle item
        self._active = True # Initially, the dummy puzzle item is active

    @property #property to get the position of the dummy puzzle item
    def position(self) -> Tuple[int, int]: #define a function returning the position of the dummy puzzle item
        return self._position # Return the position of the dummy puzzle item

    @property #property to get the active status of the dummy puzzle item   
    def active(self) -> bool: #define a function returning the active status of the dummy puzzle item
        return self._active # Return the active status of the dummy puzzle item

    def remove(self) -> None: #define a function to deactivate the dummy puzzle item
        self._active = False # Set the active status of the dummy puzzle item to False

# CLASS FOR THE MAIN PUZZLE GAME LOGIC AND STATE MANAGEMENT
class PuzzleGame:
    """
    Core Puzzle Logic and State Controller.
    Manages grid state, transformations, moves, hints, and win condition checking.
    """
    def __init__(self, grid_size: int = 3): #function to initialize the main puzzle game with a grid size of 3x3 by default
        self._grid_size = grid_size # Store the grid size of the puzzle game
        self._tiles: List[Tile] = [] # Initialize the list of puzzle tiles
        self._original_image: Optional[np.ndarray] = None # Store the original image of the puzzle. The none value indicates that no image has been set yet.
        self._processed_image: Optional[np.ndarray] = None # Store the processed image of the puzzle.None value indicates that no processed image has been set yet.
        self._move_count = 0 # Initialize the move count to zero
        self._hints_left = 3 # Initialize the number of hints left
        self._active_hint_tile_id: Optional[int] = None # Store the ID of the currently active hint tile.None value indicates that no hint tile is currently active.
        self._selected_tile_pos: Optional[Tuple[int, int]] = None # Store the position of the currently selected tile. None value indicates that no tile is currently selected.
        self._is_completed = False # Initialize the completion status of the puzzle game to False

        #set default difficulty and initialize dummy items list
        self._difficulty = "Easy" # Set the default difficulty level to Easy
        self._dummy_items: List[DummyPuzzleItem] = [] # Initialize the list of dummy puzzle items

    @property #property to get the current difficulty level of the puzzle game
    def difficulty(self) -> str: #define a function returning the current difficulty level of the puzzle game
        return self._difficulty # Return the current difficulty level of the puzzle game

    @difficulty.setter #setter to update the current difficulty level of the puzzle game
    def difficulty(self, value: str) -> None: #define a function to set the current difficulty level of the puzzle game
        if value in DIFFICULTY_SETTINGS: #check if the provided value is a valid difficulty level
            self._difficulty = value # Update the current difficulty level of the puzzle game

    @property #property to get the difficulty settings of the current difficulty level
    def difficulty_settings(self) -> dict: #define a function returning the difficulty settings of the current difficulty level
        return DIFFICULTY_SETTINGS[self._difficulty] # Return the difficulty settings of the current difficulty level

    @property #property to get the list of dummy puzzle items
    def dummy_items(self) -> List[DummyPuzzleItem]: #define a function returning the list of dummy puzzle items
        return self._dummy_items # Return the list of dummy puzzle items

    @property #property to get the current grid size of the puzzle game
    def grid_size(self) -> int: #define a function returning the current grid size of the puzzle game
        return self._grid_size # Return the current grid size of the puzzle game

    @grid_size.setter #setter to update the current grid size of the puzzle game
    def grid_size(self, size: int) -> None: #define a function to set the current grid size of the puzzle game
        if size in (3, 4, 5): #check if the provided size is a valid grid size
            self._grid_size = size # Update the current grid size of the puzzle game

    @property #property to get the current move count of the puzzle game
    def move_count(self) -> int: #define a function returning the current move count of the puzzle game
        return self._move_count # Return the current move count of the puzzle game

    @property #property to get the number of hints left in the puzzle game
    def hints_left(self) -> int: #define a function returning the number of hints left in the puzzle game
        return self._hints_left # Return the number of hints left in the puzzle game

    @property #property to check if the puzzle game is completed
    def is_completed(self) -> bool: #define a function returning whether the puzzle game is completed
        return self._is_completed # Return whether the puzzle game is completed

    @property #property to get the position of the currently selected tile
    def selected_tile_pos(self) -> Optional[Tuple[int, int]]: #define a function returning the position of the currently selected tile
        return self._selected_tile_pos # Return the position of the currently selected tile

    @property #property to get the ID of the currently active hint tile
    def active_hint_tile_id(self) -> Optional[int]: #define a function returning the ID of the currently active hint tile
        return self._active_hint_tile_id # Return the ID of the currently active hint tile  

    def load_image(self, image_path: str) -> None: #define a function to load an image and process it into puzzle tiles
        """Load image, process tiles, apply scaled random transformations."""
        self._original_image, self._processed_image = ImageProcessor.load_and_preprocess( 
            image_path, self._grid_size # Provide the image path and current grid size for preprocessing
        )
        self._tiles = ImageProcessor.slice_into_tiles(self._processed_image, self._grid_size) # Slice the processed image into individual puzzle tiles
        self.reset_round() # Reset the game state counters and restore tiles to their initial state
        self._scramble_board() # Apply initial random transformations to scramble the puzzle board

    # Define the reset round function
    def reset_round(self) -> None:
        """Reset game state counters and restore tiles."""
        # Reset or update the player's move counter . This is set to 0 at the start of a new round.
        self._move_count = 0
        # Set the number of hints available for the current difficulty
        self._hints_left = self.difficulty_settings["hints"]
        # Clear or update the tile currently highlighted by a hint
        self._active_hint_tile_id = None
        # Clear or update the player's current tile selection.
        self._selected_tile_pos = None
        # Update whether the current puzzle round has finished. This is set to False at the start of a new round.
        self._is_completed = False 
        # Loop through all real puzzle tiles
        for tile in self._tiles:
            tile.reset_tile()
        # Create the dummy items required by the selected difficulty
        self._create_dummy_items()

    # Define the create dummy items function
    def _create_dummy_items(self) -> None:
        """Create decoy puzzle items for Medium/Hard mode without replacing real tiles."""
        # Clear the dummy-item list before creating new decoys
        self._dummy_items = []
        # Determine how many dummy items are needed for this difficulty. This is based on the current difficulty settings and the total number of grid positions.
        count = min(self.difficulty_settings["dummy_items"], self._grid_size * self._grid_size)
        # Create the available puzzle grid positions. These positions will be used to randomly place the dummy items.
        positions = [(r, c) for r in range(self._grid_size) for c in range(self._grid_size)]
        # Create dummy items at randomly selected grid positions
        for pos in random.sample(positions, count):
            # Add a new dummy item at this selected grid position
            self._dummy_items.append(DummyPuzzleItem(pos))

    # Define the remove dummy at function
    def remove_dummy_at(self, pos: Tuple[int, int]) -> bool:
        """Remove a clicked decoy. Removing a decoy counts as one player move."""
        # Check whether the puzzle has already been completed
        if self._is_completed:
            # Return False to show that no valid action was completed
            return False
        # Loop through all dummy puzzle items
        for item in self._dummy_items:
            # Check whether an active dummy item occupies the clicked position
            if item.active and item.position == pos:
                item.remove()
                # Prepare the value needed for this puzzle operation. In this case, increment the move counter to reflect the player's action.
                self._move_count += 1
                # Clear or update the tile currently highlighted by a hint. This ensures that any visual hint is removed after the player interacts with a dummy item.
                self._active_hint_tile_id = None
                # Return True to show that the action was completed successfully
                return True
        # Return False to show that no valid action was completed
        return False

    # Define the move incorrect tiles function
    def move_incorrect_tiles(self) -> bool:
        """Hard-mode moving puzzle: swap two incorrect tiles without counting a player move."""
        # Check whether the puzzle has already been completed
        if self._is_completed:
            # Return False to show that no valid action was completed
            return False
        # Collect the tiles that are not yet correct
        incorrect = [t for t in self._tiles if not t.is_correct()]
        # Check whether at least two incorrect tiles are available to move
        if len(incorrect) < 2:
            # Return False to show that no valid action was completed
            return False
        # Prepare the value needed for this puzzle operation. In this case, select two incorrect tiles to swap.
        t1, t2 = random.sample(incorrect, 2)
        # Prepare the value needed for this puzzle operation. Swap the positions of the two selected incorrect tiles.   
        t1.current_pos, t2.current_pos = t2.current_pos, t1.current_pos
        # Clear or update the player's current tile selection. This ensures that no tile remains selected after the automatic swap.
        self._selected_tile_pos = None
        # Clear or update the tile currently highlighted by a hint. This ensures that any visual hint is removed after the automatic swap.
        self._active_hint_tile_id = None
        # Check whether the latest action completed the puzzle
        self._check_completion()
        # Return True to show that the action was completed successfully
        return True

    # Define the scramble board function
    def _scramble_board(self) -> None:
        """
        Apply Swap, Rotate and Flip transformations scaled to grid size.
        Each tile is targeted at most once during the initial scramble.
        The original counts 6/12/20 are retained.
        """
        # Define the scramble strength for each grid size. This determines how many transformations (swaps, rotations, flips) will be applied to the board initially.
        transform_counts = {3: 6, 4: 12, 5: 20}
        # Choose the scramble count for the current grid size. This determines how many total transformations will be applied to the board initially.
        num_transforms = transform_counts.get(self._grid_size, 6)
        # Create the available puzzle grid positions. This generates a list of all possible (row, column) coordinates on the board.
        positions = [(r, c) for r in range(self._grid_size) for c in range(self._grid_size)]
        random.shuffle(positions)  # Randomize the order of positions to ensure a varied scramble each time.

        # Include all three required transformation types on every load.
        # Limit swaps so enough unique positions remain for all operations.
        swap_count = 1 if self._grid_size == 3 else (2 if self._grid_size == 4 else 3)
        # Calculate how many rotations or flips are still required. This is the total number of transformations minus the number of swaps.
        single_count = num_transforms - swap_count
        # Calculate how many unique tile positions the scramble needs. Each swap requires two unique positions, and each single transformation requires one unique position.
        required_positions = 2 * swap_count + single_count
        # Select the unique positions that will be transformed. These positions will be used for swaps, rotations, and flips.
        chosen = positions[:required_positions]
        # Track the next unused position in the scramble list. This cursor will be incremented as positions are consumed for swaps and single transformations.
        cursor = 0

        # Swaps: every participating tile is unique.
        for _ in range(swap_count): 
            # Prepare the value needed for this puzzle operation. Select the next two unique positions for the swap.
            p1, p2 = chosen[cursor], chosen[cursor + 1]
            # Update the cursor to point to the next unused position
            cursor += 2
            # Retrieve the tiles at the selected positions. These are the tiles that will be swapped.
            t1, t2 = self.get_tile_at(p1), self.get_tile_at(p2)
            # Check that both puzzle tiles were found
            if t1 and t2:
                # Swap the current positions of the two tiles
                t1.current_pos, t2.current_pos = p2, p1

        # Remaining unique tiles receive rotations/flips. Guarantee at least one of each.
        remaining_types = ["rotate", "flip"]
        # Keep adding random rotations or flips until the required transformation count is reached
        while len(remaining_types) < single_count:
            remaining_types.append(random.choice(["rotate", "flip"]))
        random.shuffle(remaining_types)

        # Apply each remaining rotation or flip to a different tile
        for transform_type in remaining_types:
            # Prepare the value needed for this puzzle operation. Select the next unique position for the rotation/flip.
            p = chosen[cursor]
            # Update the cursor to point to the next unused position
            cursor += 1
            # Retrieve the tile at the selected position    
            tile = self.get_tile_at(p)
            # Skip this position if no puzzle tile was found
            if tile is None:
                continue
            # Check whether the selected transformation is a rotation
            if transform_type == "rotate":
                RotateTransformation(random.choice([90, 180, 270])).apply(tile)
            # Handle the remaining case
            else:
                FlipTransformation(random.choice(["horizontal", "vertical"])).apply(tile)

        # Check whether the latest action completed the puzzle
        self._check_completion()

    # Define the get tile at function
    def get_tile_at(self, pos: Tuple[int, int]) -> Optional[Tile]:
        """Find tile currently residing at grid coordinate (row, col)."""
        # Loop through all real puzzle tiles
        for tile in self._tiles:
            # Check whether this tile occupies the requested grid position
            if tile.current_pos == pos:
                # Return the matching puzzle tile
                return tile
        # Return no tile because no match was found
        return None

    # Define the get tile by id function
    def get_tile_by_id(self, tile_id: int) -> Optional[Tile]:
        """Find tile by unique ID."""
        # Loop through all real puzzle tiles
        for tile in self._tiles:
            # Check whether this is the tile with the requested ID
            if tile.tile_id == tile_id:
                # Return the matching puzzle tile
                return tile
        # Return no tile because no match was found
        return None

    # Define the handle click select swap function
    def handle_click_select_swap(self, pos: Tuple[int, int]) -> bool:
        """
        Handles Left click interaction.
        First click selects tile; second click swaps with target tile.
        """
        # Check whether the puzzle has already been completed
        if self._is_completed:
            # Return False to show that no valid action was completed
            return False

        # Clear or update the tile currently highlighted by a hint
        self._active_hint_tile_id = None # Clear hint overlay on move

        # Check whether no tile has been selected yet
        if self._selected_tile_pos is None:
            # Clear or update the player's current tile selection
            self._selected_tile_pos = pos
            # Return True to show that the action was completed successfully
            return True
        # Check whether the player clicked the already selected tile again
        elif self._selected_tile_pos == pos:
            # Clear or update the player's current tile selection
            self._selected_tile_pos = None
            # Return True to show that the action was completed successfully
            return True
        # Handle the remaining case
        else:
            # Prepare the value needed for this puzzle operation. Retrieve the first selected tile.
            t1 = self.get_tile_at(self._selected_tile_pos)
            # Prepare the value needed for this puzzle operation. Retrieve the second selected tile.
            t2 = self.get_tile_at(pos)
            # Check that both puzzle tiles were found
            if t1 and t2:
                # Prepare the value needed for this puzzle operation. Swap the positions of the two selected tiles.
                t1.current_pos, t2.current_pos = t2.current_pos, t1.current_pos
                # Prepare the value needed for this puzzle operation. Increment the move count.
                self._move_count += 1
                # Clear or update the player's current tile selection
                self._selected_tile_pos = None
                # Check whether the latest action completed the puzzle
                self._check_completion()
                # Return True to show that the action was completed successfully
                return True
        # Return False to show that no valid action was completed
        return False

    # Define the handle rotate function
    def handle_rotate(self, pos: Tuple[int, int]) -> bool:
        """Handles Right click interaction (rotates tile 90 deg clockwise)."""
        # Check whether the puzzle has already been completed
        if self._is_completed:
            # Return False to show that no valid action was completed
            return False
        # Prepare the value needed for this puzzle operation. Retrieve the tile at the specified position.
        tile = self.get_tile_at(pos)
        # Check whether a valid puzzle tile was found
        if tile:
            tile.rotate(90)
            # Prepare the value needed for this puzzle operation. Increment the move count.
            self._move_count += 1
            # Clear or update the tile currently highlighted by a hint. This ensures that the hint does not point to an outdated tile after a rotation.
            self._active_hint_tile_id = None
            # Check whether the latest action completed the puzzle
            self._check_completion()
            # Return True to show that the action was completed successfully
            return True
        # Return False to show that no valid action was completed
        return False

    # Define the handle flip function
    def handle_flip(self, pos: Tuple[int, int]) -> bool:
        """Handles Shift + Left click interaction (flips tile horizontally)."""
        # Check whether the puzzle has already been completed
        if self._is_completed:
            # Return False to show that no valid action was completed
            return False
        # Prepare the value needed for this puzzle operation. Retrieve the tile at the specified position.
        tile = self.get_tile_at(pos)
        # Check whether a valid puzzle tile was found
        if tile:
            tile.flip("horizontal") # Flip the tile horizontally.
            # Prepare the value needed for this puzzle operation. Increment the move count.
            self._move_count += 1
            # Clear or update the tile currently highlighted by a hint. This ensures that the hint does not point to an outdated tile after a flip.
            self._active_hint_tile_id = None
            # Check whether the latest action completed the puzzle
            self._check_completion()
            # Return True to show that the action was completed successfully
            return True
        # Return False to show that no valid action was completed
        return False

    # Define the get incorrect tiles count function
    def get_incorrect_tiles_count(self) -> int:
        """Count tiles not yet in correct position and orientation."""
        # Return sum(1 for t in self._tiles if not t.is_correct())
        return sum(1 for t in self._tiles if not t.is_correct())

    # Define the request hint function
    def request_hint(self) -> Tuple[Optional[Tile], Optional[Tuple[int, int]]]:
        """
        Provides a hint if hints remain.
        Returns (incorrect_tile, home_position).
        """
        # Check whether the required condition is met before continuing
        if self._hints_left <= 0 or self._is_completed:
            # Return empty values because no hint can be provided
            return None, None

        # Collect all tiles that are currently incorrect. These are potential candidates for providing a hint.
        incorrect_tiles = [t for t in self._tiles if not t.is_correct()]
        # Check whether there are no incorrect tiles left to use for a hint
        if not incorrect_tiles:
            # Return empty values because no hint can be provided
            return None, None

        # Choose one incorrect tile to highlight as a hint
        hint_tile = random.choice(incorrect_tiles)
        # Prepare the value needed for this puzzle operation. Decrement the remaining hints counter.
        self._hints_left -= 1
        # Clear or update the tile currently highlighted by a hint
        self._active_hint_tile_id = hint_tile.tile_id
        # Return the chosen incorrect tile and the position where it belongs
        return hint_tile, hint_tile.home_pos

    # Define the solve puzzle function
    def solve_puzzle(self) -> None:
        """Instantly restores all tiles to home position and orientation."""
        # Loop through all real puzzle tiles
        for tile in self._tiles:
            tile.reset_tile()  # Reset the tile to its home position and correct orientation.
        # Clear or update the tile currently highlighted by a hint
        self._active_hint_tile_id = None
        # Clear or update the player's current tile selection
        self._selected_tile_pos = None
        # Loop through all dummy puzzle items
        for item in self._dummy_items:
            item.remove()  # Remove the dummy item from the puzzle board.
        # Reset or update the player's move counter
        self._move_count = 0  # Reset the player's move counter.
        # Check whether the latest action completed the puzzle
        self._check_completion()  # Verify if the puzzle is now complete after solving.

    # Define the check completion function
    def _check_completion(self) -> None:
        """Verifies if all tiles are in home position and correct orientation."""
        # Check whether every real puzzle tile is correct. This determines if the player has correctly placed and oriented all tiles.
        all_tiles_correct = all(t.is_correct() for t in self._tiles)
        # Check whether every dummy item has been removed
        all_dummies_removed = all(not item.active for item in self._dummy_items)
        # Check whether all real tiles are correct and every dummy item has been removed
        if all_tiles_correct and all_dummies_removed:
            # Update whether the current puzzle round has finished
            self._is_completed = True


# =============================================================================
# 5. TKINTER GUI INTERFACE (Guarded for desktop execution)
# =============================================================================

# Check whether HAS_TKINTER
if HAS_TKINTER:
    # Define the class used for this part of the puzzle application
    class PuzzleApp(tk.Tk):
        """
        Main Tkinter Desktop Application Window.
        Implements Side-by-Side reference and interactive puzzle board rendering.
        """
        # Define the init function for the Tkinter application window.
        def __init__(self):
            super().__init__() # Initialize the Tkinter application window.
            # Set the application window title
            self.title("HIT137 Assignment 3 - Interactive Image Puzzle")
            # Set the starting size of the application window
            self.geometry("1100x680")
            # Set the minimum usable window size
            self.minsize(950, 600)
            # Set the main window appearance
            self.configure(bg="#2b2b2b")

            # Create the puzzle model with a 3×3 starting grid
            self._game = PuzzleGame(grid_size=3)
            # Start with no puzzle image selected. This will be updated once the user loads an image.
            self._current_image_path: Optional[str] = None

            # Store the Tkinter image used to display the tk original image.
            self._tk_orig_img: Optional[ImageTk.PhotoImage] = None
            # Store the Tkinter image used to display the tk transformed image.
            self._tk_trans_img: Optional[ImageTk.PhotoImage] = None

            # Timer and automatic moving-puzzle scheduler. This handles the countdown for each puzzle round and automatically moves puzzle pieces if needed.
            self._time_left = 0  # Initialize the remaining time for the current puzzle round.
            # Store the scheduled timer job callback reference. This is used to manage the countdown.
            self._timer_job = None
            # Store the scheduled moving job callback reference. This is used to manage automatic piece movements.
            self._moving_job = None
            # Record whether the current round has run out of time. This flag is checked to determine if the player can still make moves.   
            self._time_expired = False

            # Configure the interface styles. This sets up the visual appearance for various interface elements such as frames, labels, and buttons.
            self._init_style()
            # Create and arrange the interface controls. 
            self._build_widgets()

        # Define the init style function. This function sets up the visual styles for various interface elements.
        def _init_style(self) -> None:
            # Create the Tkinter style manager
            style = ttk.Style(self)
            style.theme_use("clam")
            # Prepare the value needed for this puzzle operation
            style.configure("TFrame", background="#2b2b2b")
            # Prepare the value needed for this puzzle operation
            style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), foreground="#ffffff", background="#2b2b2b")
            # Prepare the value needed for this puzzle operation
            style.configure("Status.TLabel", font=("Helvetica", 11, "bold"), foreground="#00e676", background="#1e1e1e")
            # Prepare the value needed for this puzzle operation
            style.configure("Info.TLabel", font=("Helvetica", 10), foreground="#cccccc", background="#2b2b2b")
            # Prepare the value needed for this puzzle operation
            style.configure("Action.TButton", font=("Helvetica", 10, "bold"), padding=6)

        # Define the build widgets function
        def _build_widgets(self) -> None:
            # Define the control frame that will hold the interface controls such as buttons and labels.
            control_frame = ttk.Frame(self, padding=(15, 10, 15, 10))
            # Place this control in the appropriate area of the interface
            control_frame.pack(side="top", fill="x")

            # Add a header label to the control frame to display the title of the puzzle game.
            ttk.Label(control_frame, text="🧩 HIT137 Image Puzzle", style="Header.TLabel").pack(side="left", padx=(0, 20))

            # Add a button to the control frame that allows the user to load an image for the puzzle.
            ttk.Button(control_frame, text="📁 Load Image", style="Action.TButton", command=self._on_load_image).pack(side="left", padx=5)

            # Add a label to the control frame to indicate the grid size selection.
            ttk.Label(control_frame, text="Grid Size:", style="Info.TLabel").pack(side="left", padx=(15, 5))
            # Store the grid-size option selected by the player. This will be used to determine the puzzle layout.
            self._grid_size_var = tk.StringVar(value="3x3")
            # Create the grid-size selection menu. This allows the player to choose the number of rows and columns for the puzzle.
            grid_combobox = ttk.Combobox(
                # Prepare the value needed for this puzzle operation
                control_frame, textvariable=self._grid_size_var, values=["3x3", "4x4", "5x5"],
                # Prepare the value needed for this puzzle operation
                state="readonly", width=6, font=("Helvetica", 10, "bold")
            )
            # Place the grid-size selection menu in the control frame.
            grid_combobox.pack(side="left", padx=5)
            # Connect the selection change event to the handler function that updates the puzzle grid.
            grid_combobox.bind("<<ComboboxSelected>>", self._on_grid_change)

            # Add a label to the control frame to indicate the difficulty selection.
            ttk.Label(control_frame, text="Difficulty:", style="Info.TLabel").pack(side="left", padx=(10, 5))
            # Store the difficulty selected by the player. This will be used to adjust the puzzle challenge level.
            self._difficulty_var = tk.StringVar(value="Easy")
            # Create the difficulty selection menu. This allows the player to choose the puzzle difficulty level.
            difficulty_combobox = ttk.Combobox(
                # Prepare the value needed for this puzzle operation
                control_frame, textvariable=self._difficulty_var, values=["Easy", "Medium", "Hard"],
                # Prepare the value needed for this puzzle operation
                state="readonly", width=8, font=("Helvetica", 10, "bold")
            )
            # Place the difficulty selection menu in the control frame.
            difficulty_combobox.pack(side="left", padx=5)
            # Connect the selection change event to the handler function that updates the puzzle difficulty.
            difficulty_combobox.bind("<<ComboboxSelected>>", self._on_difficulty_change)

            # Create the Hint button and show the remaining hint allowance. This allows the player to request hints during gameplay.
            self._hint_btn = ttk.Button(control_frame, text="💡 Hint (3 left)", style="Action.TButton", command=self._on_hint)
            # Place the Hint button in the control frame.
            self._hint_btn.pack(side="left", padx=(20, 5))

            # Create the Solve button that restores the solved puzzle.
            self._solve_btn = ttk.Button(control_frame, text="⚡ Solve", style="Action.TButton", command=self._on_solve)
            # Place the Solve button in the control frame.
            self._solve_btn.pack(side="left", padx=5)

            # Create and place the Reset button in the control frame. This allows the player to reset the puzzle to its initial state.
            ttk.Button(control_frame, text="🔄 Reset", style="Action.TButton", command=self._on_reset).pack(side="left", padx=5)

            # Status Display Bar. This area shows messages about the current game state to the player.
            status_bar = tk.Frame(self, bg="#1e1e1e", height=35, relief="sunken", bd=1)
            # Place the status bar at the top of the interface, below the control frame.
            status_bar.pack(side="top", fill="x", padx=15, pady=(0, 10))

            # Store the game-status message shown to the player
            self._status_var = tk.StringVar(value="Welcome! Select a grid size and click 'Load Image' to begin.")
            # Create the label that displays the game status. This label is placed inside the status bar.
            status_label = tk.Label(status_bar, textvariable=self._status_var, bg="#1e1e1e", fg="#00e676", font=("Helvetica", 11, "bold"))
            # Place the status label on the left side of the status bar.
            status_label.pack(side="left", padx=15, pady=5)

            # Instructions Banner
            instr_label = tk.Label(
                # Create the instructions banner that guides the player on how to interact with the puzzle.
                self, text="Controls: Left Click = Select/Swap/Remove Dummy | Right Click = Rotate 90° | Shift + Left Click = Flip Horizontal",
                # Set the background, foreground, and font for the instructions banner
                bg="#2b2b2b", fg="#aaaaaa", font=("Helvetica", 9, "italic")
            )
            # Place the instructions banner at the top of the interface, below the status bar.
            instr_label.pack(side="top", fill="x", pady=(0, 5))

            # Main Canvas Area (Side-by-Side Images)
            display_frame = ttk.Frame(self, padding=10)
            # Place the main display frame in the appropriate area of the interface.
            display_frame.pack(side="top", fill="both", expand=True)

            # Create the display area for the original reference image
            left_box = ttk.LabelFrame(display_frame, text=" Original Reference ", padding=10)
            # Place the left box (original reference image) in the appropriate area of the interface.
            left_box.pack(side="left", fill="both", expand=True, padx=5)

            # Create the canvas for the original reference image
            self._canvas_orig = tk.Canvas(left_box, bg="#1a1a1a", highlightthickness=0)
            # Place the canvas for the original reference image in the appropriate area of the interface.
            self._canvas_orig.pack(fill="both", expand=True)

            # Create the display area for the interactive puzzle
            right_box = ttk.LabelFrame(display_frame, text=" Interactive Puzzle Board ", padding=10)
            # Place the right box (interactive puzzle board) in the appropriate area of the interface.
            right_box.pack(side="right", fill="both", expand=True, padx=5)

            # Create the canvas for the interactive puzzle board
            self._canvas_trans = tk.Canvas(right_box, bg="#1a1a1a", highlightthickness=0)
            # Place the canvas for the interactive puzzle board in the appropriate area of the interface.
            self._canvas_trans.pack(fill="both", expand=True)

            # Bind Mouse Events. This allows the interactive puzzle board to respond to user actions such as clicks.
            self._canvas_trans.bind("<Button-1>", self._on_canvas_left_click) # Connect the left-click event to the function that handles it
           
            self._canvas_trans.bind("<Shift-Button-1>", self._on_canvas_shift_left_click)# Connect the shift + left-click event to the function that handles it
            
            self._canvas_trans.bind("<Button-2>", self._on_canvas_right_click)# Connect the middle-click event to the function that handles it
            
            self._canvas_trans.bind("<Button-3>", self._on_canvas_right_click) # Connect the right-click event to the function that handles it
            
           
        # Define the cancel scheduled jobs function
        def _cancel_scheduled_jobs(self) -> None:
            """Cancel previous timer/moving callbacks before starting a new round."""
            # Check whether a countdown callback is currently scheduled
            if self._timer_job is not None:
                # Cancel the previously scheduled callback. This ensures that no old timer will interfere with the new round.
                self.after_cancel(self._timer_job)
                # Store the scheduled timer job callback reference
                self._timer_job = None
            # Check whether an automatic tile-movement callback is currently scheduled
            if self._moving_job is not None:
                # Cancel the previously scheduled callback. This ensures that no old automatic tile movement will interfere with the new round.
                self.after_cancel(self._moving_job)
                # Store the scheduled moving job callback reference
                self._moving_job = None

        # Define the on difficulty change function. 
        def _on_difficulty_change(self, event=None) -> None:
            # Retrieve the selected difficulty level from the user interface and updating the game's difficulty setting accordingly.
            self._game.difficulty = self._difficulty_var.get()
            # Check whether an image is already loaded
            if self._current_image_path:
                # Reload the current image using the updated settings
                self._load_current_image()

        # Define the start round clock function
        def _start_round_clock(self) -> None:
            # Stop callbacks left from the previous round
            self._cancel_scheduled_jobs()
            # Record whether the current round has run out of time
            self._time_expired = False
            # Set the countdown from the selected difficulty's time limit
            self._time_left = self._game.difficulty_settings["time_limit"]
            # Start or continue the one-second countdown
            self._tick_timer()
            # Get the automatic movement interval for the selected difficulty
            interval = self._game.difficulty_settings["move_interval"]
            # Check whether automatic tile movement is enabled for this difficulty
            if interval > 0:
                # Store the scheduled moving job callback reference
                self._moving_job = self.after(interval * 1000, self._move_puzzle_automatically)

        # Define the tick timer function
        def _tick_timer(self) -> None:
            # Stop the timer if the puzzle is complete or the time limit has expired
            if self._game.is_completed or self._time_expired:
                # Exit the function
                return
            # Check whether the countdown has reached zero
            if self._time_left <= 0:
                # Record whether the current round has run out of time. 
                self._time_expired = True
                # Prepare the value needed for this puzzle operation
                self._game._is_completed = True  # lock puzzle input when time expires
                # Refresh the information shown in the status bar to reflect the time expiration.
                self._update_status()
                # Show the player a message about the current game state
                messagebox.showinfo("Time's Up!", "The time limit has expired. Reset or load an image to try again.")
                # Exit the function
                return
            # Refresh the information shown in the status bar. This keeps the player informed of the remaining time.
            self._update_status(show_completion_message=False)
            # Decrement the remaining time by one second.
            self._time_left -= 1
            # Store the scheduled timer job callback reference. This allows the timer to be canceled or rescheduled later if needed.
            self._timer_job = self.after(1000, self._tick_timer)

        # Define the move puzzle automatically function
        def _move_puzzle_automatically(self) -> None:
            """Move two incorrect tiles periodically in Hard mode."""
            # Store the scheduled moving job callback reference
            self._moving_job = None
            # Stop automatic movement if the round has ended
            if self._time_expired or self._game.is_completed:
                # Exit the function
                return
            # Attempt to move two incorrect tiles automatically
            if self._game.move_incorrect_tiles():
                # Redraw the reference image and puzzle board
                self._render_canvases()
                # Refresh the information shown in the status bar
                self._update_status(show_completion_message=False)
            # Get the automatic movement interval for the selected difficulty
            interval = self._game.difficulty_settings["move_interval"]
            # Continue moving tiles while moving mode is active and the puzzle is unfinished
            if interval > 0 and not self._game.is_completed:
                # Store the scheduled moving job callback reference
                self._moving_job = self.after(interval * 1000, self._move_puzzle_automatically)

        # Define the on grid change function
        def _on_grid_change(self, event=None) -> None:
            # Read the selected grid size from the interface
            selection = self._grid_size_var.get()
            # Map each grid-size label to its numeric value
            size_map = {"3x3": 3, "4x4": 4, "5x5": 5}
            # Convert the selected grid label to its numeric size
            new_size = size_map.get(selection, 3)
            #Update the game's grid size based on the user's selection.
            self._game.grid_size = new_size

            # Check whether an image is already loaded
            if self._current_image_path:
                # Reload the current image using the updated settings
                self._load_current_image()

        # Define the on load image function. This function handles the process of selecting and loading a new puzzle image.
        def _on_load_image(self) -> None:
            # Open the file dialog and store the selected image path
            file_path = filedialog.askopenfilename(
                # Open a file dialog to select an image file for the puzzle.
                title="Select Puzzle Image",
                #Specify the types of image files that can be selected. 
                filetypes=[
                    ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
                    ("JPEG Images", "*.jpg *.jpeg"),
                    ("PNG Images", "*.png"),
                    ("BMP Images", "*.bmp"),
                    ("All Files", "*.*")
                ]
            )
            # Continue only if the player selected an image file
            if file_path:
                # Start with no puzzle image selected. This ensures that the game will load the new image afresh.
                self._current_image_path = file_path
                # Reload the current image using the updated settings. This will apply any changes in difficulty or grid size to the newly selected image.
                self._load_current_image()

        # Define the load current image function
        def _load_current_image(self) -> None:
            # Stop if no puzzle image has been selected
            if not self._current_image_path:
                # Exit the function
                return
            # Run the image-loading steps and catch any errors
            try:
                # Retrieve the current difficulty setting from the user interface.
                self._game.difficulty = self._difficulty_var.get()
                # Load, process, divide, reset, and scramble the selected image
                self._game.load_image(self._current_image_path)
                # Start the countdown and optional moving-puzzle schedule
                self._start_round_clock()
                # Redraw the reference image and puzzle board
                self._render_canvases()
                # Refresh the information shown in the status bar
                self._update_status(show_completion_message=False)
            # Handle errors raised while loading the image
            except Exception as e:
                # Show the player a message about the current game state
                messagebox.showerror("Error Loading Image", f"Failed to load selected image:\n{str(e)}")

        # Define the render canvases function
        def _render_canvases(self) -> None:
            # Stop drawing if no processed puzzle image is available
            if self._game._processed_image is None:
                # Exit the function
                return

            # Get the current puzzle grid size
            grid_size = self._game.grid_size
            # Retrieve the height and width of the processed puzzle image.
            h, w = self._game._processed_image.shape[:2]

            # Left Canvas (Original Reference)
            orig_render = self._game._processed_image.copy()

            # Check whether a hint is currently active
            if self._game.active_hint_tile_id is not None:
                # Retrieve the tile object corresponding to the active hint tile ID.
                tile = self._game.get_tile_by_id(self._game.active_hint_tile_id)
                # Check whether a valid puzzle tile was found
                if tile:
                    # Retrieve the home position of the hinted tile.
                    hr, hc = tile.home_pos
                    # Calculate the height and width of each puzzle tile.
                    th, tw = h // grid_size, w // grid_size
                    # Calculate the centre of the hinted tile's correct position. To calculate this, multiply the column and row indices by the tile width and height, respectively, and add half the tile dimensions.
                    center = (hc * tw + tw // 2, hr * th + th // 2)
                    # Choose a hint-circle size that fits inside the tile. This ensures that the hint is visually clear without overlapping adjacent tiles. The radius is set to one-third of the smaller dimension of the tile.
                    radius = min(th, tw) // 3
                    # Copy the reference image so temporary overlays can be drawn safely
                    orig_render = ImageProcessor.draw_blue_circle(orig_render, center, radius)

            # Convert the reference image from BGR to RGB for Tkinter. 
            orig_rgb = cv2.cvtColor(orig_render, cv2.COLOR_BGR2RGB)
            # Convert the reference image into Pillow format. This is necessary because Tkinter works with Pillow images rather than OpenCV images.
            pil_orig = Image.fromarray(orig_rgb)
            # Store the Tkinter image used to display the tk orig img in the canvas. This step is necessary to prevent the image from being garbage collected.
            self._tk_orig_img = ImageTk.PhotoImage(image=pil_orig)

            # Clear the previous canvas contents before redrawing
            self._canvas_orig.delete("all")
            # Draw the prepared image in the canvas
            self._canvas_orig.create_image(
                # Use the horizontal centre of the canvas for image placement. This ensures that the image is centered horizontally within the canvas.
                self._canvas_orig.winfo_width() // 2,
                # Use the vertical centre of the canvas for image placement. This ensures that the image is centered vertically within the canvas.
                self._canvas_orig.winfo_height() // 2,
                # Specify the image to be drawn and its anchor point within the canvas.
                image=self._tk_orig_img, anchor="center"
            )

            # Right Canvas (Transformed Board). This section handles the rendering of the puzzle's current state on the right-hand side canvas.
            board_render = np.zeros_like(self._game._processed_image)  # Initialize an empty board representation with the same shape as the processed image. This will be used to render the current state of the puzzle.
            # Calculating the height and width of each individual tile based on the overall image dimensions and the grid size.
            tile_h, tile_w = h // grid_size, w // grid_size

            # Loop through each position along this puzzle-grid dimension
            for r in range(grid_size):
                # Loop through each position along this puzzle-grid dimension
                for c in range(grid_size):
                    # Retrieve the tile at the current grid position.
                    tile = self._game.get_tile_at((r, c))
                    # Skip this position if no puzzle tile was found
                    if tile is None:
                        continue

                    # Make a copy of the current image of the tile to avoid modifying the original.
                    tile_img = tile.current_image.copy()

                    # Check whether tile.is_correct()
                    if tile.is_correct():
                        # If the tile is in the correct position, draw a green tick on it.
                        tile_img = ImageProcessor.draw_green_tick(tile_img)

                    # Check whether the current tile is the one selected by the player.
                    if self._game.selected_tile_pos == (r, c):
                        # Highlight the selected tile to indicate it is currently active.
                        tile_img = ImageProcessor.draw_selection_highlight(tile_img, color=(0, 255, 255))

                    # Check whether the current tile is the one for which a hint is active.
                    if self._game.active_hint_tile_id == tile.tile_id:
                        # Calculate the centre of the hinted tile's correct position to draw the hint circle.
                        center = (tile_w // 2, tile_h // 2)
                        # Choose a hint-circle size that fits inside the tile
                        radius = min(tile_h, tile_w) // 3
                        # Draw a blue circle on the tile to indicate it is being hinted.
                        tile_img = ImageProcessor.draw_blue_circle(tile_img, center, radius)

                    # Calculate the vertical boundaries of the tile within the board render.
                    y1, y2 = r * tile_h, (r + 1) * tile_h
                    # Calculate the horizontal boundaries of the tile within the board render.
                    x1, x2 = c * tile_w, (c + 1) * tile_w

                    # Check whether tile_img.shape[:2] != (tile_h, tile_w)
                    if tile_img.shape[:2] != (tile_h, tile_w):
                        # Resize the tile image to match the expected tile dimensions.
                        tile_img = cv2.resize(tile_img, (tile_w, tile_h))

                    # Place the processed tile image into the corresponding location on the board render.
                    board_render[y1:y2, x1:x2] = tile_img

            # Draw active dummy/decoy items as semi-transparent warning markers
            for item in self._game.dummy_items:
                # Check whether item.active
                if item.active:
                    # Get the row and column of the dummy item's position.
                    r, c = item.position
                    # Calculate the top-left corner of the dummy item's bounding box.
                    x1, y1 = c * tile_w, r * tile_h
                    # Calculate the bottom-right corner of the dummy item's bounding box.
                    x2, y2 = (c + 1) * tile_w, (r + 1) * tile_h
                    # Create a copy of the current board render to use as an overlay for semi-transparent drawing.
                    overlay = board_render.copy()
                    # Draw a semi-transparent rectangle over the dummy item's bounding box.
                    cv2.rectangle(overlay, (x1 + 4, y1 + 4), (x2 - 4, y2 - 4), (40, 40, 40), -1)
                    # Blend the overlay with the original board render to achieve the semi-transparent effect.
                    board_render = cv2.addWeighted(overlay, 0.72, board_render, 0.28, 0)
                    # Draw a question mark over the dummy item's bounding box to indicate it is a decoy.
                    cv2.putText(board_render, "?", (x1 + tile_w // 3, y1 + (2 * tile_h) // 3),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 165, 255), 4, cv2.LINE_AA) # Draw the question mark with specified font, size, color, thickness, and line type

            # Prepare the board render with grid lines for display.
            board_render = ImageProcessor.draw_grid_lines(board_render, grid_size)

            # Convert the board render from BGR to RGB for compatibility with PIL
            board_rgb = cv2.cvtColor(board_render, cv2.COLOR_BGR2RGB)
            # Create a PIL image from the RGB board render
            pil_trans = Image.fromarray(board_rgb)
            # Store the Tkinter image used to display the transformed image
            self._tk_trans_img = ImageTk.PhotoImage(image=pil_trans)

            # Clear the previous canvas contents before redrawing
            self._canvas_trans.delete("all")
            # Draw the prepared image in the canvas
            self._canvas_trans.create_image(
                # Use the horizontal centre of the canvas for image placement
                self._canvas_trans.winfo_width() // 2,
                # Use the vertical centre of the canvas for image placement
                self._canvas_trans.winfo_height() // 2,
                # Prepare the value needed for this puzzle operation
                image=self._tk_trans_img, anchor="center"
            )

        # Define the get clicked grid pos function. This function calculates which grid cell was clicked based on the mouse event coordinates.
        def _get_clicked_grid_pos(self, event) -> Optional[Tuple[int, int]]:
            # Check whether the required condition is met before continuing
            if self._game._processed_image is None or self._tk_trans_img is None:
                # Return no tile because no match was found
                return None

            # Get the width of the canvas to calculate the relative click position
            canvas_w = self._canvas_trans.winfo_width()
            # Get the height of the canvas to calculate the relative click position
            canvas_h = self._canvas_trans.winfo_height()

            # Get the width of the transformed image for click position calculation
            img_w = self._tk_trans_img.width()
            # Get the height of the transformed image for click position calculation
            img_h = self._tk_trans_img.height()

            # Calculate the x-coordinate of the top-left corner of the image within the canvas
            img_x1 = (canvas_w - img_w) // 2
            # Calculate the y-coordinate of the top-left corner of the image within the canvas
            img_y1 = (canvas_h - img_h) // 2

            # Check whether the required condition is met before continuing
            if not (img_x1 <= event.x < img_x1 + img_w and img_y1 <= event.y < img_y1 + img_h):
                # Return no tile because no match was found
                return None

            # Calculate the relative x-coordinate of the click within the image
            rel_x = event.x - img_x1
            # Calculate the relative y-coordinate of the click within the image
            rel_y = event.y - img_y1

            # Get the current puzzle grid size
            grid_size = self._game.grid_size
            # Calculate the column index of the clicked grid cell
            col = int(rel_x // (img_w / grid_size))
            # Calculate the row index of the clicked grid cell
            row = int(rel_y // (img_h / grid_size))

            # Clamp the column index to be within the valid range
            col = max(0, min(grid_size - 1, col))
            # Clamp the row index to be within the valid range
            row = max(0, min(grid_size - 1, row))

            # Return row, col
            return row, col

        # Define the on canvas left click function
        def _on_canvas_left_click(self, event) -> None:
            # Get the grid position corresponding to the click event
            pos = self._get_clicked_grid_pos(event) 
            # Check whether the required condition is met before continuing
            if pos and self._game.remove_dummy_at(pos):
                # Redraw the reference image and puzzle board
                self._render_canvases()
                # Refresh the information shown in the status bar
                self._update_status()
                # Exit the function
                return
            # Check whether the required condition is met before continuing
            if pos and self._game.handle_click_select_swap(pos):
                # Redraw the reference image and puzzle board
                self._render_canvases()
                # Refresh the information shown in the status bar
                self._update_status()

        # Define the on canvas right click function
        def _on_canvas_right_click(self, event) -> None:
            # Get the grid position corresponding to the right click event
            pos = self._get_clicked_grid_pos(event)
            # Check whether the required condition is met before continuing
            if pos and self._game.handle_rotate(pos):
                # Redraw the reference image and puzzle board
                self._render_canvases()
                # Refresh the information shown in the status bar
                self._update_status()

        # Define the on canvas shift left click function
        def _on_canvas_shift_left_click(self, event) -> None:
            # Get the grid position corresponding to the shift left click event
            pos = self._get_clicked_grid_pos(event)
            # Check whether the required condition is met before continuing
            if pos and self._game.handle_flip(pos):
                # Redraw the reference image and puzzle board
                self._render_canvases()
                # Refresh the information shown in the status bar
                self._update_status()

        # Define the on hint function
        def _on_hint(self) -> None:
            # Check whether the required condition is met before continuing. Check if there are any hints left.
            if self._game.hints_left <= 0:
                # Show the player a message about the current game state if
                messagebox.showinfo("Hints Exhausted", "You have used all available hints for this difficulty level!")
                # Exit the function
                return

            # Request a hint from the game. This will return the hint tile and its correct position.
            hint_tile, home_pos = self._game.request_hint()
            # Check whether hint_tile
            if hint_tile:
                # Redraw the reference image and puzzle board
                self._render_canvases()
                # Refresh the information shown in the status bar
                self._update_status()
            # Handle the remaining case
            else:
                # Show the player a message about the current game state
                messagebox.showinfo("Puzzle Solved", "All tiles are already in their correct positions!")

        # Define the on solve function
        def _on_solve(self) -> None:
            # Solve the puzzle automatically.
            self._game.solve_puzzle()
            # Redraw the reference image and puzzle board
            self._render_canvases()
            # Refresh the information shown in the status bar
            self._update_status()

        # Define the on reset function
        def _on_reset(self) -> None:
            # Reset the puzzle to its initial state.
            # Check whether an image is already loaded
            if self._current_image_path:
                # Reload the current image using the updated settings
                self._load_current_image()

        # Define the update status function
        def _update_status(self, show_completion_message: bool = True) -> None:
            # Get the current player move count
            moves = self._game.move_count
            # Count the tiles that are still incorrect
            remaining = self._game.get_incorrect_tiles_count()
            # Get the number of hints remaining
            hints = self._game.hints_left
            # Count the active dummy puzzle items. These are items that are currently in play but do not contribute to solving the puzzle.
            dummy_left = sum(1 for item in self._game.dummy_items if item.active)
            # Calculate the remaining time in minutes and seconds. Ensure that the time does not go below zero.
            minutes, seconds = divmod(max(0, self._time_left), 60)
            # Format the remaining time as minutes and seconds
            time_text = f"{minutes:02d}:{seconds:02d}"

            # Update the hint button text to reflect the number of hints left.
            self._hint_btn.configure(text=f"💡 Hint ({hints} left)")
            # Check whether the required condition is met before continuing
            if hints <= 0 or self._game.is_completed:
                # Disable the hint button if no hints are left or the game is completed
                self._hint_btn.configure(state="disabled")
            # Handle the remaining case
            else:
                # Enable the hint button if hints are available and the game is not completed
                self._hint_btn.configure(state="normal")

            # Check whether the required condition is met before continuing
            if self._time_expired:
                # Update the status to indicate that the time has expired and the game is over. Also, provide relevant game details.
                self._status_var.set(f"TIME'S UP! | Difficulty: {self._game.difficulty} | Moves: {moves}")
            # Check whether the required condition is met before continuing
            elif self._game.is_completed:
                # Stop callbacks left from the previous round
                self._cancel_scheduled_jobs()
                # Update the status to indicate that the puzzle has been successfully completed.
                self._status_var.set(f"🎉 CONGRATULATIONS! Puzzle Solved in {moves} moves | Time: {time_text}")
                # Check whether show_completion_message
                if show_completion_message:
                    # Show the player a message about the current game state
                    messagebox.showinfo("Puzzle Complete!", f"Congratulations!\nYou restored the image in {moves} moves.")
            # Handle the remaining case
            else:
                # Update the status to reflect the current game state, including difficulty, time, moves, remaining tiles, dummy items, and hints left.
                self._status_var.set(
                    f"Difficulty: {self._game.difficulty} | Time: {time_text} | Moves: {moves} | "
                    f"Tiles Remaining: {remaining} | Dummy Items: {dummy_left} | Hints Left: {hints}"
                )



# MAIN ENTRY POINT


# Entry point for the HIT137 Puzzle Game application. Initializes the GUI if Tkinter is available, otherwise prints a message.
if __name__ == "__main__":
    # Check whether Tkinter is available before initializing the GUI
    if HAS_TKINTER:
        # Initialize and start the puzzle game application GUI. 
        app = PuzzleApp() # Create an instance of the PuzzleApp class
        app.mainloop()   # Start the main event loop for the GUI application
    # Handle the remaining case
    else:
        print("HIT137 Puzzle Game Engine initialized successfully.")
        print("Note: Tkinter GUI requires a desktop environment with Tk installed.")
