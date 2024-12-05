import tkinter as tk
import numpy as np
import os
from PIL import Image, ImageTk
import glob
import logging
from tkinter import messagebox, StringVar, ttk
from enum import Enum
import premade_levels

try:
    from grid import create_grid, ObstacleType, AgentType, SurvivorType
except ImportError as e:
    messagebox.showerror("Import Error", f"Could not import from 'grid.py': {e}")
    exit()

try:
    from simulation import run_simulation
except ImportError as e:
    messagebox.showerror("Import Error", f"Could not import from 'simulation.py': {e}")
    exit()

try:
    from grid_utils import reset_grid
except ImportError as e:
    messagebox.showerror("Import Error", f"Could not import from 'grid_utils.py': {e}")
    exit()


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
                    logging.error(f"Error: Could not load image {image_path}")
            except (IOError, OSError) as e:
                logging.error(f"Error loading image {image_path}: {e}")
                messagebox.showerror("Image Load Error", f"Could not load image {image_path}: {e}")
                return None
        if not item_images[item_type]:
            logging.warning(f"Warning: No images found for item type: {item_type.name}")
    return item_images


# Function to create the grid UI
def create_grid_ui(parent, grid):
    cell_size = 60
    grid_buttons = {}
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            button = tk.Button(parent, width=cell_size // 10, height=cell_size // 20, bg="white", relief="flat")
            button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            button.bind("<Button-3>", lambda event, r=row, c=col: remove_item(event, r, c))
            button.bind("<Double-Button-1>", lambda event, r=row, c=col: replace_item(event, r, c))
            button.bind("<Button-1>", lambda event, r=row, c=col, b=button: select_grid(event, r, c, b))
            grid_buttons[(row, col)] = button
    return grid_buttons

# Function to create the sidebar with draggable items
def create_sidebar(sidebar_frame, item_images):
    if item_images is None:
        return
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
    global agent_location
    logging.info(f"Placing item of type: {item_type} at {row}, {col} - grid_buttons key: {(row,col)}")
    grid[row, col] = item_type.value
    grid_buttons[(row, col)].config(bg="black", image=image)
    if item_type == AgentType.AGENT:
        agent_location = (row, col)


def remove_item(event, row, col):
    global agent_location
    grid[row, col] = 0
    grid_buttons[(row, col)].config(bg="white", image="")
    if grid[row, col] == AgentType.AGENT.value:
        agent_location = None


def replace_item(event, row, col):
    remove_item(event, row, col)

#Selecting grid
selected_grid = None
def select_grid(event, row, col, button):
    global selected_grid
    if selected_grid:
        selected_grid.config(bg="white")
    selected_grid = button
    selected_grid.config(bg="lightblue")

# Drag-and-drop functionality
def start_drag(event, item_type, image):
    global dragged_item
    dragged_item = (item_type, image)

def stop_drag(event):
    global dragged_item, selected_grid
    if dragged_item and selected_grid:
        item_type, image = dragged_item
        try:
            row, col = (selected_grid.grid_info()["row"], selected_grid.grid_info()["column"])
            place_item(item_type, image, row, col)
        except KeyError:
            logging.error("Error: Could not find button coordinates in grid_buttons.")
            messagebox.showerror("Error", "Could not place item. Button coordinates not found.")
        selected_grid = None
        dragged_item = None

# Function to run the simulation
agent_location = None
def run_sim():
    global item_images, agent_location
    if agent_location is None:
        logging.error("Error: Agent location not set. Please place the agent.")
        messagebox.showerror("Simulation Error", "Agent location not set.")
        return
    if item_images is None:
        messagebox.showerror("Image Error", "Images could not be loaded.")
        return
    status_text.set("Simulation running...")
    root.update()
    try:
        run_simulation(grid, agent_location, grid_buttons, root, item_images, status_text)
    except Exception as e:
        logging.exception(f"An unexpected error occurred during simulation: {e}")
        messagebox.showerror("Simulation Error", f"An unexpected error occurred: {e}")
    finally:
        status_text.set("Simulation finished.")

def reset_sim():
    global grid, grid_buttons, agent_location, grid_size
    grid = create_grid(grid_size, grid_size) # Reset to default grid size
    grid_frame.destroy()
    grid_frame = tk.Frame(root)
    grid_frame.grid(row=0, column=1, sticky="nsew")
    grid_frame.bind("<ButtonRelease-1>", stop_drag)
    grid_buttons = create_grid_ui(grid_frame, grid)
    agent_location = None
    status_text.set("Simulation reset.")
    for key, button in grid_buttons.items():
        button.config(image="")
        button.config(bg="white")

def save_grid_state():
    logging.info(f"Grid state on closing: \n{np.array_str(grid)}")
    # Add your grid saving logic here if needed.  For example, you could save to a file.

# Function to handle window closing
def on_closing(root):
    save_grid_state()
    root.destroy()

# Function to toggle fullscreen
def toggle_fullscreen():
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)

def load_level(level_name):
    global grid, grid_buttons, grid_size, grid_frame, agent_location
    try:
        level_index = int(level_name.split()[1]) - 1
        level_data = premade_levels.levels[level_index]
        grid_size = len(level_data)
        grid = np.array(level_data)
        grid_frame.destroy()
        grid_frame = tk.Frame(root)
        grid_frame.grid(row=0, column=1, sticky="nsew")
        grid_frame.bind("<ButtonRelease-1>", stop_drag)
        grid_buttons = create_grid_ui(grid_frame, grid)
        agent_location = None #This line was causing the issue
        agent_row, agent_col = np.where(grid == AgentType.AGENT.value)
        if agent_row.size > 0:
            agent_location = (agent_row[0], agent_col[0])
        canvas.config(width=grid_size * 60, height=grid_size * 60)
        sidebar.config(height=grid_size * 60)
        right_sidebar.config(height=grid_size * 60)
        root.geometry(f"{grid_size * 60 + 450}x{grid_size * 60 + 100}")
        root.update()
        update_images_on_grid()
        status_text.set(f"Level {level_index + 1} loaded.")
    except (IndexError, ValueError):
        logging.error(f"Error: Invalid level name: {level_name}")
        messagebox.showerror("Level Load Error", f"Invalid level name: {level_name}")

def update_images_on_grid():
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            item_type = grid[r,c]
            if item_type == 0:
                grid_buttons[(r,c)].config(image="", bg="white")
            elif item_type == ObstacleType.BUILDING.value:
                grid_buttons[(r,c)].config(image=item_images[ObstacleType.BUILDING][0], bg="black")
            elif item_type == ObstacleType.RUBBLE.value:
                grid_buttons[(r,c)].config(image=item_images[ObstacleType.RUBBLE][0], bg="black")
            elif item_type == ObstacleType.FALLEN_TREE.value:
                grid_buttons[(r,c)].config(image=item_images[ObstacleType.FALLEN_TREE][0], bg="black")
            elif item_type == AgentType.AGENT.value:
                grid_buttons[(r,c)].config(image=item_images[AgentType.AGENT][0], bg="black")
            elif item_type == SurvivorType.SURVIVOR.value:
                grid_buttons[(r,c)].config(image=item_images[SurvivorType.SURVIVOR][0], bg="black")


# Initialize the main window
root = tk.Tk()
root.title("Rescue Operation Simulator")

# Grid size selection
grid_size_options = [5, 10, 12]
selected_grid_size = tk.IntVar(value=10)  # Default grid size

def update_grid_size():
    global grid, grid_buttons, canvas_width, canvas_height, grid_size, cell_size, grid_frame
    grid_size = selected_grid_size.get()
    grid = create_grid(grid_size, grid_size)
    cell_size = 60
    canvas_width = grid_size * cell_size
    canvas_height = grid_size * cell_size
    canvas.config(width=canvas_width, height=canvas_height)
    if 'grid_frame' in locals():
        grid_frame.destroy()
    grid_frame = tk.Frame(root)
    grid_frame.grid(row=0, column=1, sticky="nsew")
    grid_frame.bind("<ButtonRelease-1>", stop_drag)
    grid_buttons = create_grid_ui(grid_frame, grid)
    sidebar.config(height=canvas_height)
    right_sidebar.config(height=canvas_height)
    root.geometry(f"{canvas_width + 450}x{canvas_height + 100}")
    root.update()
    for key, button in grid_buttons.items():
        button.config(image="")
        button.config(bg="white")

# Create the canvas for the grid
canvas = tk.Canvas(root, width=10*60, height=10*60) # Initialize canvas with default size
canvas.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)


# Sidebar for item selection with a proper frame for scrollbar
sidebar_frame = tk.Frame(root)
sidebar_frame.grid(row=0, column=0, sticky="ns", padx=10)

# Scrollable sidebar
sidebar = tk.Canvas(sidebar_frame, width=200, height=10*60, relief="sunken", borderwidth=2) # Initialize with default height
sidebar.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(sidebar_frame, orient="vertical", command=sidebar.yview)
scrollbar.pack(side="right", fill="y")
sidebar.config(yscrollcommand=scrollbar.set)

# Create item selection in the sidebar
sidebar_inner = tk.Frame(sidebar)
sidebar.create_window((0, 0), window=sidebar_inner, anchor="nw")

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
item_images = load_images(image_dir)
if item_images is None:
    root.destroy()
    exit()

# Load level images (placeholder - replace with actual image loading)
level_images = {
    "Level 1": ImageTk.PhotoImage(Image.new("RGB", (50, 50), "red")),
    "Level 2": ImageTk.PhotoImage(Image.new("RGB", (50, 50), "blue")),
    "Level 3": ImageTk.PhotoImage(Image.new("RGB", (50, 50), "green")),
    "Level 4": ImageTk.PhotoImage(Image.new("RGB", (50, 50), "green")),
    "Level 5": ImageTk.PhotoImage(Image.new("RGB", (50, 50), "green")),
}

create_sidebar(sidebar_inner, item_images)

# Ensure the sidebar's inner frame resizes and scrolls properly
sidebar_inner.update_idletasks()
sidebar.config(scrollregion=sidebar.bbox("all"))


# Right sidebar for grid size selection
right_sidebar_frame = tk.Frame(root)
right_sidebar_frame.grid(row=0, column=2, sticky="ns", padx=10)

right_sidebar = tk.Canvas(right_sidebar_frame, width=200, height=10*60, relief="sunken", borderwidth=2)
right_sidebar.pack(side="left", fill="both", expand=True)

right_scrollbar = tk.Scrollbar(right_sidebar_frame, orient="vertical", command=right_sidebar.yview)
right_scrollbar.pack(side="right", fill="y")
right_sidebar.config(yscrollcommand=right_scrollbar.set)

right_sidebar_inner = tk.Frame(right_sidebar)
right_sidebar.create_window((0, 0), window=right_sidebar_inner, anchor="nw")

def create_grid_size_selector(parent, row_num): # Pass row_num as parameter
    grid_size_label = ttk.Label(parent, text="Grid Size:", font=("Arial", 12))
    grid_size_label.grid(row=row_num, column=0, sticky="w", padx=5, pady=5)

    for size in grid_size_options:
        radio_button = tk.Radiobutton(parent, text=f"{size}x{size}", variable=selected_grid_size, value=size, command=update_grid_size)
        row_num += 1
        radio_button.grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
    return row_num # Return updated row_num


# Grid size selector in right sidebar
row_num = 0
row_num = create_grid_size_selector(right_sidebar_inner, row_num) # Pass row_num and get updated value
row_num += 1 # Add extra spacing

# Add premade levels to the right sidebar
level_label = ttk.Label(right_sidebar_inner, text="Premade Levels:", font=("Arial", 12))
level_label.grid(row=row_num, column=0, sticky="w", padx=5, pady=(10, 5)) # Added pady
row_num += 1

for i, level_name in enumerate(map(lambda x: f"Level {x+1}", range(len(premade_levels.levels)))):
    level_button = tk.Button(right_sidebar_inner, text=level_name,
                             command=lambda name=level_name: load_level(name),
                             relief=tk.RAISED, bd=2, padx=10, pady=5, font=("Arial", 10)) #Added styling
    level_button.grid(row=row_num + i, column=0, sticky="w", pady=2)


update_grid_size()

# Run Simulation button
run_button = tk.Button(root, text="Run Simulation", command=run_sim, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
run_button.grid(row=1, column=0, columnspan=1, pady=10)

# Reset Simulation button
reset_button = tk.Button(root, text="Reset Simulation", command=reset_sim, bg="#f44336", fg="white", font=("Arial", 12, "bold"))
reset_button.grid(row=1, column=0, columnspan=4, pady=10, padx=(0,10))

# Status bar
status_text = StringVar()
status_bar = tk.Label(root, textvariable=status_text, bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.grid(row=2, column=0, columnspan=3, sticky="ew")

# Configure the window layout
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

# Set weight to 0 for the first column and first row (prevents stretching)
root.columnconfigure(0, weight=0)
root.columnconfigure(2, weight=0)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=0)
root.rowconfigure(3, weight=0)


# Handle window close event
root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

# Fullscreen toggle
is_fullscreen = False
root.bind("<F11>", lambda event: toggle_fullscreen())

# Start the main loop
root.mainloop()
