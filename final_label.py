import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog, filedialog

# Sample blueprint dimensions (you can replace this with your blueprint image)
sample_blueprint = plt.imread('Box-Clamp-1(Edited).png')

# Initialize empty list to store user-added points and labels
user_data = []

# Initialize variables for click-drag functionality and zoom
start_x = None
start_y = None
scale = 1.0  # Initial zoom scale

# Create a function to update the side panel with labels
def update_side_panel():
    side_panel.delete('1.0', tk.END)  # Clear previous labels

    for (point_x, point_y), label in user_data:
        side_panel.insert(tk.END, f"Point: ({point_x:.2f}, {point_y:.2f})\nLabel: {label}\n\n")

def update_blueprint():
    # Clear any previous user-added points and text boxes
    plt.clf()
    
    # Plot user-added points with white pointer and black label color
    for (point_x, point_y), label in user_data:
        plt.scatter([point_x], [point_y], s=50, marker='o', facecolors='none', edgecolors='white')
        plt.annotate(label, (point_x, point_y), textcoords="offset points", xytext=(0, 10), ha='center', color='black')
    
    # Display the blueprint with zoom
    plt.imshow(sample_blueprint, extent=[0, sample_blueprint.shape[1]*scale, 0, sample_blueprint.shape[0]*scale])
    plt.axis('off')
    
    # Update the Matplotlib canvas
    canvas.draw()



def on_canvas_click(event):
    global start_x, start_y
    # Get the coordinates of the mouse click event
    x, y = event.xdata, event.ydata

    if x is not None and y is not None:
        # Create a text box at the clicked location
        label = simpledialog.askstring("Label", "Enter a label for this point:")
        if label:
            # Add the point and label to the list of user-added data
            user_data.append(((x, y), label))
            update_blueprint()
            update_side_panel()

def on_canvas_scroll(event):
    global scale
    # Get the mouse scroll direction (up or down)
    delta = event.delta

    # Calculate the new scale factor based on scroll direction
    if delta > 0:
        scale *= 1.1  # Zoom in
    else:
        scale /= 1.1  # Zoom out

    # Limit the scale factor to reasonable bounds
    scale = max(0.1, min(2.0, scale))

    # Update the blueprint display with the new scale
    update_blueprint()

def save_user_data():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            for (point_x, point_y), label in user_data:
                file.write(f"Point: ({point_x:.2f}, {point_y:.2f})\nLabel: {label}\n\n")
        print(f"User data saved to {file_path}")

def save_blueprint_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
    if file_path:
        plt.savefig(file_path, bbox_inches='tight', pad_inches=0, dpi=300)
        print(f"Blueprint image saved to {file_path}")

# Create a Tkinter window
root = tk.Tk()
root.title("Blueprint Editor")

# Create a Matplotlib figure for displaying the blueprint
fig = plt.figure(figsize=(6, 6))
plt.imshow(sample_blueprint)
plt.axis('off')

# Create a Matplotlib canvas for displaying the blueprint
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Create a side panel to display labels
side_panel = tk.Text(root, width=20, height=20)
side_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

# Create a Save User Data button
save_data_button = tk.Button(root, text="Save User Data", command=save_user_data)
save_data_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Create a Save Blueprint Image button
save_image_button = tk.Button(root, text="Save Blueprint Image", command=save_blueprint_image)
save_image_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Bind the canvas click event to the on_canvas_click function
canvas.mpl_connect("button_press_event", on_canvas_click)

# Bind the canvas scroll event to the on_canvas_scroll function
canvas_widget.bind("<MouseWheel>", on_canvas_scroll)

root.mainloop()
