import tkinter as tk
from tkinter import messagebox, Label, Button, Frame
import random
import os
from PIL import Image, ImageTk
import time

class VerificationSystem:
    """Visual Campus Verification System for Automated Access Control with 3 Levels"""
    
    def __init__(self, root):
        """Initialize the verification system with the root window"""
        self.root = root
        self.root.title("Campus Verification System")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f0f0")
        
        # Paths to campus and external images
        self.campus_images_path = "C:\\Users\\ultra\\meME\\campus_images"
        self.external_images_path = "C:\\Users\\ultra\\meME\\external_images"
        
        # Load image lists from directories
        self.all_campus_images = [f for f in os.listdir(self.campus_images_path) 
                                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        self.all_external_images = [f for f in os.listdir(self.external_images_path) 
                                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Level tracking (reversed order)
        self.current_level = 1  # Now starting with what was previously level 3
        self.selected_images = []
        
        # Points system
        self.total_points = 0
        self.points_per_correct = 5
        
        # Timer variables
        self.time_remaining = 0
        self.timer_id = None
        self.timer_label = None
        
        # Time limits for each level (in seconds)
        self.time_limits = {
            1: 30,    # Level 1: 30 seconds
            2: 60,    # Level 2: 1 minute
            3: 120    # Level 3: 2 minutes
        }
        
        # UI elements
        self.header_label = None
        self.instruction_label = None
        self.image_frame = None
        self.submit_button = None
        self.image_buttons = []
        self.current_images = []
        self.points_label = None
        
        # Start the verification process
        self.create_ui()
        self.load_level()
    
    def create_ui(self):
        """Create the user interface elements"""
        # Header
        self.header_label = Label(
            self.root, 
            text="Campus Verification System", 
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            pady=10
        )
        self.header_label.pack(fill=tk.X)
        
        # Points and Timer display frame
        info_frame = Frame(self.root, bg="#f0f0f0")
        info_frame.pack(fill=tk.X, pady=5)
        
        # Points display
        self.points_label = Label(
            info_frame,
            text="Total Points: 0",
            font=("Arial", 14, "bold"),
            fg="#007bff",
            bg="#f0f0f0",
            pady=5
        )
        self.points_label.pack(side=tk.LEFT, padx=20)
        
        # Timer display
        self.timer_label = Label(
            info_frame,
            text="Time: 00:00",
            font=("Arial", 14, "bold"),
            fg="#e74c3c",  # Red color for urgency
            bg="#f0f0f0",
            pady=5
        )
        self.timer_label.pack(side=tk.RIGHT, padx=20)
        
        # Instructions
        self.instruction_label = Label(
            self.root,
            text="",
            font=("Arial", 12),
            bg="#f0f0f0",
            pady=10,
            wraplength=750
        )
        self.instruction_label.pack(fill=tk.X)
        
        # Image frame
        self.image_frame = Frame(self.root, bg="#f0f0f0")
        self.image_frame.pack(pady=10)
        
        # Button frame for better layout
        button_frame = Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        # Submit button (improved styling)
        self.submit_button = Button(
            button_frame,
            text="Submit Selection",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            command=self.validate_selection,
            state=tk.DISABLED
        )
        self.submit_button.pack(side=tk.LEFT, padx=10)
        
        # Status bar
        self.status_bar = Label(
            self.root,
            text="Level 1 of 3",
            font=("Arial", 10),
            bg="#e0e0e0",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_level(self):
        """Load images for the current level"""
        # Clear any existing selection
        self.selected_images = []
        
        # Cancel any existing timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        # Update UI for current level
        if self.current_level == 1:  # Original level 3
            # Level 1: 2x2 grid with 1 campus image to select
            time_text = "30 seconds"
            self.instruction_label.config(
                text=f"LEVEL 1: Select the ONE campus image from the 2x2 grid below. Each correct campus image is worth 5 points. You have {time_text}."
            )
            self.status_bar.config(text="Level 1 of 3")
            
            # Make sure we have enough images
            if len(self.all_campus_images) < 1 or len(self.all_external_images) < 3:
                messagebox.showerror("Error", "Not enough images in directories. Please add more images.")
                return
            
            campus_images = random.sample(self.all_campus_images, 1)
            external_images = random.sample(self.all_external_images, 3)
            self.current_images = campus_images + external_images
            random.shuffle(self.current_images)
            
            # Create a 2x2 grid
            self.display_image_grid(2, 2)
            
        elif self.current_level == 2:  # Original level 2 with modification
            # Level 2: 3x3 grid with 3 campus images to select (changed from 4)
            time_text = "1 minute"
            self.instruction_label.config(
                text=f"LEVEL 2: Select all 3 campus images from the 3x3 grid below. Each correct campus image is worth 5 points. You have {time_text}."
            )
            self.status_bar.config(text="Level 2 of 3")
            
            # Check if we have enough images for this level
            if len(self.all_campus_images) < 3 or len(self.all_external_images) < 6:
                messagebox.showerror("Error", "Not enough images in directories. Please add more images.")
                return
            
            campus_images = random.sample(self.all_campus_images, 3)  # Changed from 4 to 3
            external_images = random.sample(self.all_external_images, 6)  # Changed from 5 to 6
            self.current_images = campus_images + external_images
            random.shuffle(self.current_images)
            
            # Create a 3x3 grid
            self.display_image_grid(3, 3)
            
        elif self.current_level == 3:  # Original level 1
            # Level 3: 4x4 grid with 6 campus images to select
            time_text = "2 minutes"
            self.instruction_label.config(
                text=f"LEVEL 3: Select all 6 campus images from the 4x4 grid below. Each correct campus image is worth 5 points. You have {time_text}."
            )
            self.status_bar.config(text="Level 3 of 3")
            
            # Check if we have enough images for this level
            if len(self.all_campus_images) < 6 or len(self.all_external_images) < 10:
                messagebox.showerror("Error", "Not enough images in directories. Please add more images.")
                return
            
            campus_images = random.sample(self.all_campus_images, 6)
            external_images = random.sample(self.all_external_images, 10)
            self.current_images = campus_images + external_images
            random.shuffle(self.current_images)
            
            # Create a 4x4 grid
            self.display_image_grid(4, 4)
        
        # Start the timer for this level
        self.time_remaining = self.time_limits[self.current_level]
        self.update_timer_display()
        self.start_timer()
    
    def display_image_grid(self, rows, cols):
        """Display images in a grid layout"""
        # Clear existing image frame content
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        
        self.image_buttons = []
        
        # Determine image size based on grid
        if rows == 4:
            image_size = 150
        elif rows == 3:
            image_size = 180
        else:  # 2x2 grid
            image_size = 220
        
        # Create a nested frame for the grid
        grid_frame = Frame(self.image_frame, bg="#f0f0f0")
        grid_frame.pack(pady=10)
        
        # Make sure we're using the right number of images for each level
        total_cells = rows * cols
        
        # Print debug info
        print(f"Creating {rows}x{cols} grid for level {self.current_level}")
        print(f"Total images available: {len(self.current_images)}")
        
        # Ensure we have exactly the right number of images
        if len(self.current_images) != total_cells:
            print(f"Warning: Expected {total_cells} images for level {self.current_level}, but got {len(self.current_images)}")
        
        for i in range(total_cells):
            frame = Frame(
                grid_frame,
                width=image_size,
                height=image_size,
                bd=2,
                relief=tk.RAISED
            )
            frame.grid(row=i//cols, column=i%cols, padx=5, pady=5)
            frame.grid_propagate(False)
            
            if i < len(self.current_images):
                # Determine if this is a campus image
                image_name = self.current_images[i]
                is_campus = image_name in self.all_campus_images
                
                # Load the actual image
                if is_campus:
                    img_path = os.path.join(self.campus_images_path, image_name)
                else:
                    img_path = os.path.join(self.external_images_path, image_name)
                
                try:
                    # Load and resize the image
                    pil_img = Image.open(img_path)
                    pil_img = pil_img.resize((image_size-4, image_size-4), Image.LANCZOS)
                    tk_img = ImageTk.PhotoImage(pil_img)
                    
                    # Create a label to display the image
                    img_label = tk.Label(frame, image=tk_img)
                    img_label.image = tk_img  # Keep a reference to prevent garbage collection
                    img_label.pack(fill=tk.BOTH, expand=True)
                    
                    # Store image info and selection state
                    img_label.is_selected = False
                    img_label.is_campus = is_campus
                    img_label.image_index = i
                    
                    # Bind click event
                    img_label.bind("<Button-1>", self.toggle_selection)
                    
                    self.image_buttons.append(img_label)
                except Exception as e:
                    # Handle image loading errors
                    print(f"Error loading image {img_path}: {e}")
                    # Create a fallback colored rectangle
                    color = "#a3c4bc" if is_campus else "#e6a57e"
                    canvas = tk.Canvas(frame, width=image_size-4, height=image_size-4, bg=color)
                    canvas.pack(fill=tk.BOTH, expand=True)
                    
                    # Add text label with filename
                    canvas.create_text(
                        image_size//2, 
                        image_size//2, 
                        text=image_name,
                        font=("Arial", 10),
                        fill="#000000",
                        width=image_size-20  # Wrap text if filename is long
                    )
                    
                    canvas.is_selected = False
                    canvas.is_campus = is_campus
                    canvas.image_index = i
                    canvas.bind("<Button-1>", self.toggle_selection)
                    self.image_buttons.append(canvas)
            else:
                # If we don't have enough images, create an empty cell
                # This should not happen if our image counts are correct
                print(f"Warning: Not enough images for cell {i} in {rows}x{cols} grid")
                empty_label = tk.Label(frame, text="No Image", bg="#f0f0f0")
                empty_label.pack(fill=tk.BOTH, expand=True)
    
    def toggle_selection(self, event):
        """Toggle the selection state of an image"""
        widget = event.widget
        
        # For level 1, deselect all other images first
        if self.current_level == 1:
            for button in self.image_buttons:
                if button != widget:
                    if isinstance(button, tk.Label):
                        button.config(bd=0)
                    else:  # It's a Canvas
                        button.config(highlightthickness=0)
                    button.is_selected = False
                    if button.image_index in self.selected_images:
                        self.selected_images.remove(button.image_index)
        
        if widget.is_selected:
            # Deselect
            if isinstance(widget, tk.Label):
                widget.config(bd=0)
            else:  # It's a Canvas
                widget.config(highlightthickness=0)
            widget.is_selected = False
            if widget.image_index in self.selected_images:
                self.selected_images.remove(widget.image_index)
        else:
            # Select
            if isinstance(widget, tk.Label):
                widget.config(bd=3, borderwidth=3, relief=tk.SOLID)
            else:  # It's a Canvas
                widget.config(highlightthickness=3, highlightbackground="#007bff")
            widget.is_selected = True
            if widget.image_index not in self.selected_images:
                self.selected_images.append(widget.image_index)
        
        # Enable/disable submit button based on selection count
        if len(self.selected_images) > 0:
            self.submit_button.config(state=tk.NORMAL)
        else:
            self.submit_button.config(state=tk.DISABLED)
    
    def _get_required_selection_count(self):
        """Get the required number of selections for the current level"""
        if self.current_level == 1:  # Original level 3
            return 1  # Level 1: select 1 campus image
        elif self.current_level == 2:  # Original level 2 (modified)
            return 3  # Level 2: select 3 campus images (changed from 4)
        else:  # Level 3 (original level 1)
            return 6  # Level 3: select 6 campus images
    
    def validate_selection(self):
        """Validate the user's selection"""
        # Stop the timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        # Check if all selected images are campus images
        all_correct = True
        incorrect_selections = []
        
        for idx in self.selected_images:
            widget = self.image_buttons[idx]
            if not widget.is_campus:
                all_correct = False
                incorrect_selections.append(idx)
        
        # Check if we selected all required campus images
        required_campus_count = self._get_required_selection_count()
        selected_campus_images = [idx for idx in self.selected_images if self.image_buttons[idx].is_campus]
        campus_count = len(selected_campus_images)
        
        # Calculate points for this level
        level_points = campus_count * self.points_per_correct
        
        # Add to total points
        self.total_points += level_points
        self.points_label.config(text=f"Total Points: {self.total_points}")
        
        if all_correct and campus_count == required_campus_count:
            if self.current_level < 3:
                messagebox.showinfo("Success", f"Level {self.current_level} completed successfully!\nYou earned {level_points} points!\nProceeding to Level {self.current_level + 1}.")
                self.current_level += 1
                self.load_level()
            else:
                messagebox.showinfo("Verification Complete", f"Congratulations! You have successfully completed all levels of verification!\nFinal score: {self.total_points} points!")
                # In a real system, this would trigger an access grant
                self.root.after(1500, self.reset_verification)
        else:
            # Highlight incorrect selections in red
            for idx in incorrect_selections:
                widget = self.image_buttons[idx]
                if isinstance(widget, tk.Label):
                    widget.config(bd=3, borderwidth=3, relief=tk.SOLID, highlightbackground="#ff0000", highlightthickness=3)
                else:  # It's a Canvas
                    widget.config(highlightthickness=3, highlightbackground="#ff0000")
            
            messagebox.showerror("Verification Failed", f"Incorrect selection.\nYour final score: {self.total_points} points.")
            # Reset to Level 1 on failure
            self.root.after(1500, self.reset_verification)
    
    def reset_verification(self):
        """Reset the verification process back to Level 1"""
        self.current_level = 1
        self.total_points = 0
        self.points_label.config(text="Total Points: 0")
        self.load_level()
    
    def start_timer(self):
        """Start the countdown timer for the current level"""
        if self.time_remaining > 0:
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.time_expired()
    
    def update_timer(self):
        """Update the timer countdown"""
        self.time_remaining -= 1
        self.update_timer_display()
        
        if self.time_remaining <= 0:
            self.time_expired()
        else:
            self.timer_id = self.root.after(1000, self.update_timer)
    
    def update_timer_display(self):
        """Update the timer display label"""
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
        
        # Change color to red when time is running out (less than 20% of time remaining)
        time_limit = self.time_limits[self.current_level]
        if self.time_remaining < time_limit * 0.2:
            self.timer_label.config(fg="#ff0000")  # Bright red
        else:
            self.timer_label.config(fg="#e74c3c")  # Normal red
    
    def time_expired(self):
        """Handle time expiration"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        messagebox.showwarning("Time Expired", f"Time's up! You didn't complete Level {self.current_level} in time.\nYour final score: {self.total_points} points.")
        self.reset_verification()
    
    def simulate_bot_attack(self):
        """
        A method to demonstrate how the system would perform against a simulated bot attack.
        In a real implementation, this would be separate and used for testing only.
        """
        # Calculate theoretical success probabilities
        # Level 1: Select exactly 1 campus image from 4 total (1 campus, 3 external)
        level1_prob = 1/4  # This would be 1/4
        
        # Level 2: Select exactly 3 campus images from 9 total (3 campus, 6 external)
        level2_prob = 1/binom(9, 3)  # This would be C(3,3)/C(9,3)
        
        # Level 3: Select exactly 6 campus images from
        # 16 total (6 campus, 10 external)
        level3_prob = 1/binom(16, 6)  # This would be C(6,6)/C(16,6)
        
        # Combined probability (all three levels must be passed)
        combined_prob = level1_prob * level2_prob * level3_prob
        
        print(f"Theoretical bot success probability:")
        print(f"Level 1: {level1_prob:.10f}")
        print(f"Level 2: {level2_prob:.10f}")
        print(f"Level 3: {level3_prob:.10f}")
        print(f"Overall: {combined_prob:.15f}")

def binom(n, k):
    """Calculate the binomial coefficient C(n,k)"""
    from math import factorial
    return factorial(n) // (factorial(k) * factorial(n - k))

def main():
    """Main function to start the application"""
    root = tk.Tk()
    app = VerificationSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()