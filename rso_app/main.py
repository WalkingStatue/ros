import tkinter as tk
import numpy as np
import os
from PIL import Image, ImageTk
import glob
import logging
from tkinter import messagebox, StringVar

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

def create_grid_size_selector(parent):
    grid_size_title = tk.Label(parent, text="Grid Size", font=("Arial", 14, "bold"), pady=10)
    grid_size_title.grid(row=0, column=0, columnspan=2, sticky="w")

    row_num = 1
    for size in grid_size_options:
        radio_button = tk.Radiobutton(parent, text=f"{size}x{size}", variable=selected_grid_size, value=size, command=update_grid_size)
        radio_button.grid(row=row_num, column=0, sticky="w")
        row_num += 1

# Grid size selector in right sidebar
create_grid_size_selector(right_sidebar_inner)

update_grid_size() #call update_grid_size to initialize grid_size

# Run Simulation button
run_button = tk.Button(root, text="Run Simulation", command=run_sim, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
run_button.grid(row=1, column=0, columnspan=3, pady=10)

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
