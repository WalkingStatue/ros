import tkinter as tk
import numpy as np
import os
from PIL import Image, ImageTk
import glob

from grid import create_grid, ObstacleType, AgentType, SurvivorType
from simulation import run_simulation

# Function to load images
def load_images(image_dir):
    item_images = {}
    for item_type, image_glob in item_image_paths.items():
        item_images[item_type] = []
        for image_path in glob.glob(image_glob):
            try:
                img = Image.open(image_path)
                if img:
                    img = img.resize((50, 50), Image.Resampling.LANCZOS)
                    item_images[item_type].append(ImageTk.PhotoImage(img))
                else:
                    print(f"Error: Could not load image {image_path}")
            except (IOError, OSError) as e:
                print(f"Error loading image {image_path}: {e}")
        if not item_images[item_type]:
            print(f"Warning: No images found for item type: {item_type.name}")
    return item_images

# Function to create the grid UI
def create_grid_ui(parent, grid):
    cell_size = 60
    grid_buttons = {}
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            button = tk.Button(parent, width=cell_size // 10, height=cell_size // 20, bg="white", relief="flat")
            button.grid(row=row, column=col, sticky="nsew")
            button.bind("<Button-3>", lambda event, r=row, c=col: remove_item(event, r, c))
            button.bind("<Double-Button-1>", lambda event, r=row, c=col: replace_item(event, r, c))
            grid_buttons[(row, col)] = button
    return grid_buttons

# Function to create the sidebar with draggable items
def create_sidebar(sidebar_frame, item_images):
    for item_type, images in item_images.items():
        item_frame = tk.LabelFrame(sidebar_frame, text=item_type.name, padx=10, pady=5)
        item_frame.pack(pady=10)
        for image in images:
            label = tk.Label(item_frame, image=image, relief="groove")
            label.image = image
            label.bind("<Button-1>", lambda event, it=item_type, img=image: start_drag(event, it, img))
            label.bind("<ButtonRelease-1>", stop_drag)
            label.pack(pady=2)

# Functions for placing and removing items from the grid
def place_item(item_type, image, row, col):
    print(f"Placing item of type: {item_type} at {row}, {col} - grid_buttons key: {(row,col)}")
    grid[row, col] = item_type.value
    try:
        grid_buttons[(row, col)].config(bg="black", image=image)
    except KeyError as e:
        print(f"KeyError: {e} - grid_buttons dictionary does not contain key for this location.")

def remove_item(event, row, col):
    grid[row, col] = 0
    grid_buttons[(row, col)].config(bg="white", image="")

def replace_item(event, row, col):
    remove_item(event, row, col)

# Drag-and-drop functionality
def start_drag(event, item_type, image):
    global dragged_item
    dragged_item = (item_type, image)

def stop_drag(event):
    global dragged_item, is_fullscreen
    if dragged_item:
        item_type, image = dragged_item
        try:
            x = event.x_root - grid_frame.winfo_rootx()
            y = event.y_root - grid_frame.winfo_rooty()
            print(f"Raw Mouse Coordinates: x={x}, y={y}")

            # Adjust y coordinate for canvas scroll position
            canvas_y_offset = sidebar.yview()[0] * sidebar_inner.winfo_height()
            y -= canvas_y_offset

            # Adjust for fullscreen (you'll need to fine-tune these values)
            if is_fullscreen:
                x -= 5
                y -= 30

            # Adjust for button size
            button_width = grid_buttons[(0,0)].winfo_width()
            button_height = grid_buttons[(0,0)].winfo_height()
            x -= button_width // 2
            y -= button_height // 2

            col = int(x // cell_size)
            row = int(y // cell_size)
            print(f"Calculated Grid Coordinates: row={row}, col={col}")

            if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                place_item(item_type, image, row, col)
            else:
                print("Error: Drop outside grid boundaries")
        except Exception as e:
            print(f"An error occurred: {e}")
        dragged_item = None

# Function to run the simulation
def run_sim():
    run_simulation(grid)

# Function to handle window closing
def on_closing(root):
    print(np.array_str(grid))
    root.destroy()

# Function to toggle fullscreen
def toggle_fullscreen():
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)

# Initialize the main window
root = tk.Tk()
root.title("Rescue Operation Simulator")
grid_size = 10
cell_size = 60
canvas_width = grid_size * cell_size
canvas_height = grid_size * cell_size
root.geometry(f"{canvas_width + 250}x{canvas_height + 100}")

# Create the grid
grid = create_grid(grid_size, grid_size)

# Create the canvas for the grid
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# Directory for images
image_dir = os.path.join(os.path.dirname(__file__), "images")

# Paths for different item images
item_image_paths = {
    ObstacleType.BUILDING: os.path.join(image_dir, "buildings", "*.png"),
    ObstacleType.RUBBLE: os.path.join(image_dir, "ruins", "*.png"),
    ObstacleType.FALLEN_TREE: os.path.join(image_dir, "trees", "*.png"),
    AgentType.AGENT: os.path.join(image_dir, "persons", "agent.png"),
    SurvivorType.SURVIVOR: os.path.join(image_dir, "persons", "survivor.png"),
}

# Load item images
item_images = load_images(image_dir)  # Load images here

# Create the grid UI
grid_frame = tk.Frame(root)
grid_frame.grid(row=0, column=1, sticky="nsew")
grid_buttons = create_grid_ui(grid_frame, grid)

# Sidebar for item selection with a proper frame for scrollbar
sidebar_frame = tk.Frame(root)
sidebar_frame.grid(row=0, column=0, sticky="ns", padx=10)

# Scrollable sidebar
sidebar = tk.Canvas(sidebar_frame, width=200, height=canvas_height, relief="sunken", borderwidth=2)
sidebar.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(sidebar_frame, orient="vertical", command=sidebar.yview)
scrollbar.pack(side="right", fill="y")
sidebar.config(yscrollcommand=scrollbar.set)

# Create item selection in the sidebar
sidebar_inner = tk.Frame(sidebar)
sidebar.create_window((0, 0), window=sidebar_inner, anchor="nw")
create_sidebar(sidebar_inner, item_images)

# Ensure the sidebar's inner frame resizes and scrolls properly
sidebar_inner.update_idletasks()
sidebar.config(scrollregion=sidebar.bbox("all"))

# Run Simulation button
run_button = tk.Button(root, text="Run Simulation", command=run_sim, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
run_button.grid(row=1, column=0, columnspan=2, pady=10)

# Configure the window layout
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

# Set weight to 0 for the first column and first row (prevents stretching)
root.columnconfigure(0, weight=0)
root.rowconfigure(1, weight=0)

# Handle window close event
root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

# Fullscreen toggle
is_fullscreen = False
root.bind("<F11>", lambda event: toggle_fullscreen())

# Start the main loop
root.mainloop()
