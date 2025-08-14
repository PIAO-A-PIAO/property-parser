import tkinter as tk
from tkinter import messagebox

class PropertySearchGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Property Search")
        self.root.geometry("450x700")
        self.root.resizable(False, False)
        self.root.eval('tk::PlaceWindow . center')
        self.root.transient()
        self.root.grab_set()
        self.root.focus_force()
        
        self.selected_choice = None
        self.selection_var = tk.IntVar(value=-1)
        
        # Create main container with log section
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))
        
        # Main content area
        self.main_frame = tk.Frame(self.content_frame)
        self.main_frame.pack(fill="both", expand=True)
        
        # Log section at bottom
        self.log_frame = tk.Frame(self.content_frame)
        self.log_frame.pack(fill="x", side="bottom", pady=(10, 10))
        
        log_title = tk.Label(self.log_frame, text="Activity Log:", font=("Arial", 9, "bold"))
        log_title.pack(anchor="w")
        
        # Create scrollable log area
        log_scroll_frame = tk.Frame(self.log_frame)
        log_scroll_frame.pack(fill="x")
        
        self.log_text = tk.Text(log_scroll_frame, height=4, font=("Arial", 8), 
                               bg="#f8f9fa", fg="#333", state="disabled", wrap="word")
        log_scrollbar = tk.Scrollbar(log_scroll_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")
        
    def clear_content(self):
        """Clear all content from the main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.selection_var.set(-1)
        self.selected_choice = None
    
    def log_message(self, message):
        """Add a message to the log area"""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state="disabled")
        # Auto-scroll to bottom
        self.log_text.see(tk.END)
        # Update GUI immediately
        self.root.update_idletasks()
    
    def show_sale_type_selection(self, sale_type_options):
        """Show sale type selection in the same window"""
        self.clear_content()
        self.root.title("Property Search - Sale Type")
        self.root.geometry("400x450")
        
        # Title label
        title_label = tk.Label(self.main_frame, text="What are you looking for?", 
                              font=("Arial", 14, "bold"), pady=10)
        title_label.pack()
        
        # Radio buttons for each option
        for idx, option in sale_type_options.items():
            radio = tk.Radiobutton(self.main_frame, text=option['label'], 
                                  variable=self.selection_var, value=idx,
                                  font=("Arial", 12), pady=5)
            radio.pack(anchor="w", padx=50)
        
        # Buttons
        self._add_buttons()
        
        self.root.mainloop()
        return self.selected_choice
    
    def show_property_type_selection(self, prop_options):
        """Show property type selection in the same window"""
        self.clear_content()
        self.root.title("Property Search - Property Type")
        self.root.geometry("450x600")
        
        # Title label
        title_label = tk.Label(self.main_frame, text="Select Property Type", 
                              font=("Arial", 14, "bold"), pady=10)
        title_label.pack()
        
        # Buttons frame - pack first so it stays at bottom
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(side="bottom", pady=15, fill="x")
        
        # Center the buttons
        button_container = tk.Frame(button_frame)
        button_container.pack()
        
        # Create scrollable frame for radio buttons
        canvas_frame = tk.Frame(self.main_frame)
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        canvas = tk.Canvas(canvas_frame)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Radio buttons for each property type option
        for idx, option in prop_options.items():
            radio = tk.Radiobutton(scrollable_frame, text=option['text'], 
                                  variable=self.selection_var, value=idx,
                                  font=("Arial", 11), pady=3, anchor="w")
            radio.pack(fill="x", padx=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add buttons to the button container
        confirm_btn = tk.Button(button_container, text="Continue", command=self._on_confirm,
                               bg="#007bff", fg="white", font=("Arial", 10, "bold"),
                               padx=20, pady=5)
        confirm_btn.pack(side="left", padx=10)
        
        cancel_btn = tk.Button(button_container, text="Cancel", command=self._on_cancel,
                              bg="#6c757d", fg="white", font=("Arial", 10),
                              padx=20, pady=5)
        cancel_btn.pack(side="left", padx=10)
        
        self.root.mainloop()
        return self.selected_choice
    
    def show_location_input(self):
        """Show location keyword input in the same window"""
        self.clear_content()
        self.root.title("Property Search - Location")
        self.root.geometry("450x500")
        
        # Title label
        title_label = tk.Label(self.main_frame, text="Enter Location Keyword", 
                              font=("Arial", 14, "bold"), pady=20)
        title_label.pack()
        
        # Instruction label
        instruction_label = tk.Label(self.main_frame, 
                                   text="Enter a location keyword (e.g., Toronto, Warehouse, etc.):", 
                                   font=("Arial", 11), pady=10)
        instruction_label.pack()
        
        # Entry field
        self.location_entry = tk.Entry(self.main_frame, font=("Arial", 12), width=40)
        self.location_entry.pack(pady=10)
        self.location_entry.focus_set()  # Set focus to the entry field
        
        # Bind Enter key to confirm
        self.location_entry.bind('<Return>', lambda event: self._on_confirm_location())
        
        # Buttons
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        confirm_btn = tk.Button(button_frame, text="Continue", command=self._on_confirm_location,
                               bg="#007bff", fg="white", font=("Arial", 10, "bold"),
                               padx=20, pady=5)
        confirm_btn.pack(side="left", padx=15)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self._on_cancel,
                              bg="#6c757d", fg="white", font=("Arial", 10),
                              padx=20, pady=5)
        cancel_btn.pack(side="left", padx=15)
        
        self.root.mainloop()
        return self.selected_choice
    
    def _on_confirm_location(self):
        """Handle location input confirmation"""
        location_text = self.location_entry.get().strip()
        if not location_text:
            messagebox.showwarning("Input Required", "Please enter a location keyword.")
            self.location_entry.focus_set()
            return
        self.selected_choice = location_text
        self.root.quit()
    
    def show_location_options_selection(self, location_options):
        """Show location autocomplete options selection in the same window"""
        self.clear_content()
        self.root.title("Property Search - Select Location")
        self.root.geometry("450x600")
        
        # Title label
        title_label = tk.Label(self.main_frame, text="Select Location", 
                              font=("Arial", 14, "bold"), pady=10)
        title_label.pack()
        
        # Buttons frame - pack first so it stays at bottom
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(side="bottom", pady=15, fill="x")
        
        # Center the buttons
        button_container = tk.Frame(button_frame)
        button_container.pack()
        
        # Create scrollable frame for radio buttons
        canvas_frame = tk.Frame(self.main_frame)
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        canvas = tk.Canvas(canvas_frame)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Radio buttons for each location option
        for idx, option in location_options.items():
            radio = tk.Radiobutton(scrollable_frame, text=option['text'], 
                                  variable=self.selection_var, value=idx,
                                  font=("Arial", 11), pady=3, anchor="w")
            radio.pack(fill="x", padx=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add buttons to the button container
        confirm_btn = tk.Button(button_container, text="Continue", command=self._on_confirm,
                               bg="#007bff", fg="white", font=("Arial", 10, "bold"),
                               padx=20, pady=15)
        confirm_btn.pack(side="left", padx=10)
        
        cancel_btn = tk.Button(button_container, text="Cancel", command=self._on_cancel,
                              bg="#6c757d", fg="white", font=("Arial", 10),
                              padx=20, pady=15)
        cancel_btn.pack(side="left", padx=10)
        
        self.root.mainloop()
        return self.selected_choice
    
    def show_price_range_selection(self, price_options):
        """Show price range options selection in the same window"""
        self.clear_content()
        self.root.title("Property Search - Price Range")
        self.root.geometry("450x600")
        
        # Title label
        title_label = tk.Label(self.main_frame, text="Select Price Range Type", 
                              font=("Arial", 14, "bold"), pady=10)
        title_label.pack()
        
        # Instruction label
        instruction_label = tk.Label(self.main_frame, 
                                   text="Choose a price range option or skip to continue:", 
                                   font=("Arial", 11), pady=10)
        instruction_label.pack()
        
        # Buttons frame - pack first so it stays at bottom
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(side="bottom", pady=15, fill="x")
        
        # Center the buttons
        button_container = tk.Frame(button_frame)
        button_container.pack()
        
        # Create scrollable frame for radio buttons
        canvas_frame = tk.Frame(self.main_frame)
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        canvas = tk.Canvas(canvas_frame)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Radio buttons for each price option
        for idx, option in price_options.items():
            radio = tk.Radiobutton(scrollable_frame, text=option['text'], 
                                  variable=self.selection_var, value=idx,
                                  font=("Arial", 11), pady=3, anchor="w")
            radio.pack(fill="x", padx=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add buttons to the button container
        confirm_btn = tk.Button(button_container, text="Select & Continue", command=self._on_confirm,
                               bg="#007bff", fg="white", font=("Arial", 10, "bold"),
                               padx=15, pady=8)
        confirm_btn.pack(side="left", padx=8)
        
        skip_btn = tk.Button(button_container, text="Skip", command=self._on_skip,
                            bg="#28a745", fg="white", font=("Arial", 10),
                            padx=20, pady=8)
        skip_btn.pack(side="left", padx=8)
        
        cancel_btn = tk.Button(button_container, text="Cancel", command=self._on_cancel,
                              bg="#6c757d", fg="white", font=("Arial", 10),
                              padx=15, pady=8)
        cancel_btn.pack(side="left", padx=8)
        
        self.root.mainloop()
        return self.selected_choice
    
    def show_price_input(self, unit_label):
        """Show price input dialog with min/max fields"""
        self.clear_content()
        self.root.title("Property Search - Price Range")
        self.root.geometry("450x550")
        
        # Title label
        title_label = tk.Label(self.main_frame, text=f"Enter Price Range ({unit_label})", 
                              font=("Arial", 14, "bold"), pady=20)
        title_label.pack()
        
        # Min price frame
        min_frame = tk.Frame(self.main_frame)
        min_frame.pack(pady=10)
        
        min_label = tk.Label(min_frame, text="Minimum Price:", font=("Arial", 12))
        min_label.pack(side="left", padx=(0, 10))
        
        self.min_price_entry = tk.Entry(min_frame, font=("Arial", 12), width=15)
        self.min_price_entry.pack(side="left", padx=(0, 5))
        
        min_unit_label = tk.Label(min_frame, text=unit_label, font=("Arial", 12))
        min_unit_label.pack(side="left")
        
        # Max price frame
        max_frame = tk.Frame(self.main_frame)
        max_frame.pack(pady=10)
        
        max_label = tk.Label(max_frame, text="Maximum Price:", font=("Arial", 12))
        max_label.pack(side="left", padx=(0, 10))
        
        self.max_price_entry = tk.Entry(max_frame, font=("Arial", 12), width=15)
        self.max_price_entry.pack(side="left", padx=(0, 5))
        
        max_unit_label = tk.Label(max_frame, text=unit_label, font=("Arial", 12))
        max_unit_label.pack(side="left")
        
        # Instruction label
        instruction_label = tk.Label(self.main_frame, 
                                   text="Enter values or leave blank to skip", 
                                   font=("Arial", 10), pady=20, fg="gray")
        instruction_label.pack()
        
        # Buttons
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        confirm_btn = tk.Button(button_frame, text="Continue", command=self._on_confirm_price,
                               bg="#007bff", fg="white", font=("Arial", 10, "bold"),
                               padx=20, pady=8)
        confirm_btn.pack(side="left", padx=15)
        
        skip_btn = tk.Button(button_frame, text="Skip", command=self._on_skip,
                            bg="#28a745", fg="white", font=("Arial", 10),
                            padx=20, pady=8)
        skip_btn.pack(side="left", padx=15)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self._on_cancel,
                              bg="#6c757d", fg="white", font=("Arial", 10),
                              padx=15, pady=8)
        cancel_btn.pack(side="left", padx=15)
        
        # Set focus to first input
        self.min_price_entry.focus_set()
        
        self.root.mainloop()
        return self.selected_choice
    
    def show_space_input(self):
        """Show space input dialog with min/max fields in SF"""
        self.clear_content()
        self.root.title("Property Search - Space Size")
        self.root.geometry("450x550")
        
        # Title label
        title_label = tk.Label(self.main_frame, text="Enter Space Size Range", 
                              font=("Arial", 14, "bold"), pady=20)
        title_label.pack()
        
        # Min space frame
        min_frame = tk.Frame(self.main_frame)
        min_frame.pack(pady=10)
        
        min_label = tk.Label(min_frame, text="Minimum Space:", font=("Arial", 12))
        min_label.pack(side="left", padx=(0, 10))
        
        self.min_space_entry = tk.Entry(min_frame, font=("Arial", 12), width=15)
        self.min_space_entry.pack(side="left", padx=(0, 5))
        
        min_sf_label = tk.Label(min_frame, text="SF", font=("Arial", 12))
        min_sf_label.pack(side="left")
        
        # Max space frame
        max_frame = tk.Frame(self.main_frame)
        max_frame.pack(pady=10)
        
        max_label = tk.Label(max_frame, text="Maximum Space:", font=("Arial", 12))
        max_label.pack(side="left", padx=(0, 10))
        
        self.max_space_entry = tk.Entry(max_frame, font=("Arial", 12), width=15)
        self.max_space_entry.pack(side="left", padx=(0, 5))
        
        max_sf_label = tk.Label(max_frame, text="SF", font=("Arial", 12))
        max_sf_label.pack(side="left")
        
        # Instruction label
        instruction_label = tk.Label(self.main_frame, 
                                   text="Enter values in square feet or leave blank to skip", 
                                   font=("Arial", 10), pady=20, fg="gray")
        instruction_label.pack()
        
        # Buttons
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        confirm_btn = tk.Button(button_frame, text="Continue", command=self._on_confirm_space,
                               bg="#007bff", fg="white", font=("Arial", 10, "bold"),
                               padx=20, pady=8)
        confirm_btn.pack(side="left", padx=15)
        
        skip_btn = tk.Button(button_frame, text="Skip", command=self._on_skip,
                            bg="#28a745", fg="white", font=("Arial", 10),
                            padx=20, pady=8)
        skip_btn.pack(side="left", padx=15)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self._on_cancel,
                              bg="#6c757d", fg="white", font=("Arial", 10),
                              padx=15, pady=8)
        cancel_btn.pack(side="left", padx=15)
        
        # Set focus to first input
        self.min_space_entry.focus_set()
        
        self.root.mainloop()
        return self.selected_choice
    
    def _add_buttons(self):
        """Add Continue and Cancel buttons"""
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        confirm_btn = tk.Button(button_frame, text="Continue", command=self._on_confirm,
                               bg="#007bff", fg="white", font=("Arial", 10, "bold"),
                               padx=20, pady=5)
        confirm_btn.pack(side="left", padx=10)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self._on_cancel,
                              bg="#6c757d", fg="white", font=("Arial", 10),
                              padx=20, pady=5)
        cancel_btn.pack(side="left", padx=10)
    
    def _on_confirm(self):
        if self.selection_var.get() == -1:
            messagebox.showwarning("Selection Required", "Please select an option before continuing.")
            return
        self.selected_choice = self.selection_var.get()
        self.root.quit()
    
    def _on_cancel(self):
        self.selected_choice = None
        self.root.quit()
    
    def _on_skip(self):
        self.selected_choice = "skip"
        self.root.quit()
    
    def _on_confirm_price(self):
        """Handle price input confirmation"""
        min_price = self.min_price_entry.get().strip()
        max_price = self.max_price_entry.get().strip()
        self.selected_choice = {"min": min_price, "max": max_price}
        self.root.quit()
    
    def _on_confirm_space(self):
        """Handle space input confirmation"""
        min_space = self.min_space_entry.get().strip()
        max_space = self.max_space_entry.get().strip()
        self.selected_choice = {"min": min_space, "max": max_space}
        self.root.quit()
    
    def show_loading_message(self, message="Loading..."):
        """Show a loading message in the same window"""
        self.clear_content()
        self.root.title("Property Search - Loading")
        self.root.geometry("400x400")
        
        # Loading label
        loading_label = tk.Label(self.main_frame, text=message, 
                               font=("Arial", 14), pady=40)
        loading_label.pack()
        
        # Progress indicator (simple dots animation)
        self.dots_label = tk.Label(self.main_frame, text="...", 
                                 font=("Arial", 16), pady=10)
        self.dots_label.pack()
        
        # Force update to show the loading message immediately
        self.root.update()
        self._animate_dots()
    
    def _animate_dots(self):
        """Animate loading dots"""
        current_text = self.dots_label.cget("text")
        if len(current_text) >= 6:  # Reset after "......"
            new_text = "."
        else:
            new_text = current_text + "."
        
        try:
            self.dots_label.config(text=new_text)
            self.root.update()
            # Schedule next animation frame
            self.root.after(500, self._animate_dots)
        except tk.TclError:
            # Window was destroyed, stop animation
            pass
    
    def close(self):
        """Close the GUI window"""
        self.root.destroy()

# Create global GUI instance
_gui_instance = None

def get_gui_instance():
    """Get or create the GUI instance"""
    global _gui_instance
    if _gui_instance is None:
        _gui_instance = PropertySearchGUI()
    return _gui_instance

def show_sale_type_dialog(sale_type_options):
    """Show a GUI dialog for sale type selection using persistent window"""
    gui = get_gui_instance()
    return gui.show_sale_type_selection(sale_type_options)

def show_property_type_dialog(prop_options):
    """Show a GUI dialog for property type selection using persistent window"""
    gui = get_gui_instance()
    return gui.show_property_type_selection(prop_options)

def show_location_input_dialog():
    """Show a GUI dialog for location keyword input using persistent window"""
    gui = get_gui_instance()
    return gui.show_location_input()

def show_location_options_dialog(location_options):
    """Show a GUI dialog for location options selection using persistent window"""
    gui = get_gui_instance()
    return gui.show_location_options_selection(location_options)

def show_price_range_dialog(price_options):
    """Show a GUI dialog for price range selection using persistent window"""
    gui = get_gui_instance()
    return gui.show_price_range_selection(price_options)

def show_price_input_dialog(unit_label):
    """Show a GUI dialog for price input using persistent window"""
    gui = get_gui_instance()
    return gui.show_price_input(unit_label)

def show_space_input_dialog():
    """Show a GUI dialog for space input using persistent window"""
    gui = get_gui_instance()
    return gui.show_space_input()

def show_loading_message(message="Loading..."):
    """Show a loading message using persistent window"""
    gui = get_gui_instance()
    gui.show_loading_message(message)

def log_message(message):
    """Log a message to the GUI log section"""
    gui = get_gui_instance()
    gui.log_message(message)

def close_gui():
    """Close the persistent GUI window"""
    global _gui_instance
    if _gui_instance:
        _gui_instance.close()
        _gui_instance = None

