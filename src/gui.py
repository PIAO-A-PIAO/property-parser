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
        
        # Navigation stack to track user's journey
        self.nav_stack = []
        self.current_step = None
        self.step_data = {}
        
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
        
        # Track this step in navigation
        self.current_step = 'sale_type'
        if 'sale_type' not in self.nav_stack:
            self.nav_stack.append('sale_type')
        
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
        
        # Buttons (only Continue button for first step)
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        confirm_btn = tk.Button(button_frame, text="Continue", command=self._on_confirm,
                               bg="#007bff", fg="white", font=("Arial", 10, "bold"),
                               padx=20, pady=5)
        confirm_btn.pack()
        
        self.root.mainloop()
        return self.selected_choice
    
    def show_property_type_selection(self, prop_options):
        """Show property type selection in the same window"""
        self.clear_content()
        self.root.title("Property Search - Property Type")
        self.root.geometry("450x600")
        
        # Track this step in navigation
        self.current_step = 'property_type'
        if 'property_type' not in self.nav_stack:
            self.nav_stack.append('property_type')
        
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
        
        back_btn = tk.Button(button_container, text="Back", command=self._on_back,
                              bg="#6c757d", fg="white", font=("Arial", 10),
                              padx=20, pady=5)
        back_btn.pack(side="left", padx=10)
        
        self.root.mainloop()
        return self.selected_choice
    
    def show_location_input(self):
        """Show location keyword input in the same window"""
        self.clear_content()
        self.root.title("Property Search - Location")
        self.root.geometry("450x500")
        
        # Track this step in navigation
        self.current_step = 'location_input'
        if 'location_input' not in self.nav_stack:
            self.nav_stack.append('location_input')
        
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
        
        back_btn = tk.Button(button_frame, text="Back", command=self._on_back,
                              bg="#6c757d", fg="white", font=("Arial", 10),
                              padx=20, pady=5)
        back_btn.pack(side="left", padx=15)
        
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
        
        # Track this step in navigation
        self.current_step = 'location_options'
        if 'location_options' not in self.nav_stack:
            self.nav_stack.append('location_options')
        
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
        
        back_btn = tk.Button(button_container, text="Back", command=self._on_back,
                              bg="#6c757d", fg="white", font=("Arial", 10),
                              padx=20, pady=15)
        back_btn.pack(side="left", padx=10)
        
        self.root.mainloop()
        return self.selected_choice
    
    def show_price_range_selection(self, price_options):
        """Show combined price range selection and input in the same window"""
        self.clear_content()
        self.root.title("Property Search - Price Range")
        self.root.geometry("450x750")
        
        # Track this step in navigation
        self.current_step = 'price_range'
        if 'price_range' not in self.nav_stack:
            self.nav_stack.append('price_range')
        
        # Store price options for later use
        self.price_options = price_options
        
        # Title label
        title_label = tk.Label(self.main_frame, text="Price Range Selection", 
                              font=("Arial", 14, "bold"), pady=10)
        title_label.pack()
        
        # Instruction label
        instruction_label = tk.Label(self.main_frame, 
                                   text="Select a price range type and optionally enter specific values:", 
                                   font=("Arial", 11), pady=10)
        instruction_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.main_frame)
        content_frame.pack(fill="both", expand=True, padx=20)
        
        # Price range options section
        options_section = tk.LabelFrame(content_frame, text="Price Range Type", 
                                       font=("Arial", 12, "bold"), pady=10)
        options_section.pack(fill="x", pady=(0, 15))
        
        # Create scrollable frame for radio buttons
        canvas = tk.Canvas(options_section, height=120)
        scrollbar = tk.Scrollbar(options_section, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Radio buttons for each price option
        for idx, option in price_options.items():
            radio = tk.Radiobutton(scrollable_frame, text="CAD/"+option['text'], 
                                  variable=self.selection_var, value=idx,
                                  font=("Arial", 11), pady=3, anchor="w",
                                  command=self._on_price_type_selected)
            radio.pack(fill="x", padx=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Price values section
        values_section = tk.LabelFrame(content_frame, text="Price Values (Optional)", 
                                      font=("Arial", 12, "bold"), pady=10)
        values_section.pack(fill="x", pady=(0, 15))
        
        # Unit label (initially empty)
        self.unit_display = tk.Label(values_section, text="Select a price type above to see unit", 
                                    font=("Arial", 10), fg="#666", pady=5)
        self.unit_display.pack()
        
        # Min price frame
        min_frame = tk.Frame(values_section)
        min_frame.pack(fill="x", pady=5, padx=20)
        
        min_label = tk.Label(min_frame, text="Minimum:", font=("Arial", 11), width=12)
        min_label.pack(side="left")
        
        self.min_price_entry = tk.Entry(min_frame, font=("Arial", 11), width=15)
        self.min_price_entry.pack(side="left", padx=(5, 5))
        
        self.min_unit_label = tk.Label(min_frame, text="", font=("Arial", 11), fg="#666")
        self.min_unit_label.pack(side="left")
        
        # Max price frame
        max_frame = tk.Frame(values_section)
        max_frame.pack(fill="x", pady=5, padx=20)
        
        max_label = tk.Label(max_frame, text="Maximum:", font=("Arial", 11), width=12)
        max_label.pack(side="left")
        
        self.max_price_entry = tk.Entry(max_frame, font=("Arial", 11), width=15)
        self.max_price_entry.pack(side="left", padx=(5, 5))
        
        self.max_unit_label = tk.Label(max_frame, text="", font=("Arial", 11), fg="#666")
        self.max_unit_label.pack(side="left")
        
        # Instructions
        instruction2_label = tk.Label(values_section, 
                                    text="Leave blank to skip specific price values", 
                                    font=("Arial", 9), fg="#888", pady=5)
        instruction2_label.pack()
        
        # Buttons frame
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        confirm_btn = tk.Button(button_frame, text="Continue", command=self._on_confirm_combined_price,
                               bg="#007bff", fg="white", font=("Arial", 11, "bold"),
                               padx=25, pady=8)
        confirm_btn.pack(side="left", padx=8)
        
        skip_btn = tk.Button(button_frame, text="Skip", command=self._on_skip,
                            bg="#28a745", fg="white", font=("Arial", 11),
                            padx=25, pady=8)
        skip_btn.pack(side="left", padx=8)
        
        back_btn = tk.Button(button_frame, text="Back", command=self._on_back,
                              bg="#6c757d", fg="white", font=("Arial", 11),
                              padx=25, pady=8)
        back_btn.pack(side="left", padx=8)
        
        self.root.mainloop()
        return self.selected_choice
    
    def _on_price_type_selected(self):
        """Update unit labels when price type is selected"""
        if self.selection_var.get() != -1 and hasattr(self, 'price_options'):
            selected_idx = self.selection_var.get()
            if selected_idx in self.price_options:
                unit = self.price_options[selected_idx]['text']
                unit_text = f"CAD/{unit}"
                
                # Update unit display and input labels
                self.unit_display.config(text=f"Selected unit: {unit_text}")
                self.min_unit_label.config(text=unit_text)
                self.max_unit_label.config(text=unit_text)
    
    def _on_confirm_combined_price(self):
        """Handle combined price selection and input confirmation"""
        if self.selection_var.get() == -1:
            messagebox.showwarning("Selection Required", "Please select a price range type before continuing.")
            return
        
        selected_price_type = self.selection_var.get()
        min_price = self.min_price_entry.get().strip()
        max_price = self.max_price_entry.get().strip()
        
        # Create combined result object
        result = {
            'price_type': selected_price_type,
            'min_value': min_price if min_price else None,
            'max_value': max_price if max_price else None,
            'unit_label': self.price_options[selected_price_type]['text']
        }
        
        self.selected_choice = result
        self.root.quit()
    
    
    def show_price_input(self, unit_label):
        """Show price input dialog with min/max fields"""
        self.clear_content()
        self.root.title("Property Search - Price Range")
        self.root.geometry("450x550")
        
        # Track this step in navigation
        self.current_step = 'price_input'
        if 'price_input' not in self.nav_stack:
            self.nav_stack.append('price_input')
        
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
        
        back_btn = tk.Button(button_frame, text="Back", command=self._on_back,
                              bg="#6c757d", fg="white", font=("Arial", 10),
                              padx=15, pady=8)
        back_btn.pack(side="left", padx=15)
        
        # Set focus to first input
        self.min_price_entry.focus_set()
        
        self.root.mainloop()
        return self.selected_choice
    
    def show_space_input(self):
        """Show space input dialog with min/max fields in SF"""
        self.clear_content()
        self.root.title("Property Search - Space Size")
        self.root.geometry("450x550")
        
        # Track this step in navigation
        self.current_step = 'space_input'
        if 'space_input' not in self.nav_stack:
            self.nav_stack.append('space_input')
        
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
        
        back_btn = tk.Button(button_frame, text="Back", command=self._on_back,
                              bg="#6c757d", fg="white", font=("Arial", 10),
                              padx=15, pady=8)
        back_btn.pack(side="left", padx=15)
        
        # Set focus to first input
        self.min_space_entry.focus_set()
        
        self.root.mainloop()
        return self.selected_choice
    
    def _add_buttons(self):
        """Add Continue and Back buttons"""
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        confirm_btn = tk.Button(button_frame, text="Continue", command=self._on_confirm,
                               bg="#007bff", fg="white", font=("Arial", 10, "bold"),
                               padx=20, pady=5)
        confirm_btn.pack(side="left", padx=10)
        
        back_btn = tk.Button(button_frame, text="Back", command=self._on_back,
                              bg="#6c757d", fg="white", font=("Arial", 10),
                              padx=20, pady=5)
        back_btn.pack(side="left", padx=10)
    
    def _on_confirm(self):
        if self.selection_var.get() == -1:
            messagebox.showwarning("Selection Required", "Please select an option before continuing.")
            return
        self.selected_choice = self.selection_var.get()
        self.root.quit()
    
    def _on_back(self):
        if len(self.nav_stack) > 1:
            # Remove current step and go back to previous
            current_step = self.nav_stack.pop()
            previous_step = self.nav_stack[-1]
            
            # Clear any stored data for steps that come after the previous step
            self._clear_subsequent_step_data(previous_step)
            
            self.selected_choice = {'action': 'back', 'step': previous_step}
        else:
            # First step, cancel the entire process
            self.selected_choice = None
        self.root.quit()
        
    def _clear_subsequent_step_data(self, current_step):
        """Clear stored data for steps that come after the current step"""
        step_order = ['sale_type', 'property_type', 'location_input', 'location_options', 'price_range', 'space_input']
        
        try:
            current_index = step_order.index(current_step)
            # Clear step_data for all subsequent steps
            for step in step_order[current_index + 1:]:
                if step in self.step_data:
                    del self.step_data[step]
        except ValueError:
            pass  # Current step not in order list
    
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
    
    def show_completion_message(self):
        """Show completion message with finish button"""
        self.clear_content()
        self.root.title("Property Search - Complete")
        self.root.geometry("500x600")
        
        # Success icon/title
        success_label = tk.Label(self.main_frame, text="🎉 Process Complete!", 
                               font=("Arial", 18, "bold"), fg="#28a745", pady=30)
        success_label.pack()
        
        # Main message
        message_label = tk.Label(self.main_frame, 
                               text="Property data has been successfully collected and saved.\nCheck your output file for the results.", 
                               font=("Arial", 12), pady=20, justify="center")
        message_label.pack()
        
        # Summary info
        summary_label = tk.Label(self.main_frame, 
                               text="✅ Search parameters configured\n✅ Data collection completed\n✅ Results saved to CSV file", 
                               font=("Arial", 11), pady=20, justify="left", fg="#666")
        summary_label.pack()
        
        # Finish button
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=40)
        
        finish_btn = tk.Button(button_frame, text="Finish", command=self._on_finish,
                             bg="#28a745", fg="white", font=("Arial", 14, "bold"),
                             padx=40, pady=12)
        finish_btn.pack()
        
        # Focus on the finish button
        finish_btn.focus_set()
        
        # Allow Enter key to close
        self.root.bind('<Return>', lambda event: self._on_finish())
    
    def _on_finish(self):
        """Handle finish button click"""
        self.root.destroy()
    
    def show_failure_message(self):
        """Show failure message when access is denied after retries"""
        self.clear_content()
        self.root.title("Property Search - Connection Failed")
        self.root.geometry("500x600")
        
        # Error icon/title
        error_label = tk.Label(self.main_frame, text="❌ Connection Failed", 
                              font=("Arial", 16, "bold"), fg="#dc3545", pady=20)
        error_label.pack()
        
        # Main message
        message_label = tk.Label(self.main_frame, 
                                text="Unable to access LoopNet.ca after multiple attempts.\nThe website may be blocking access or temporarily unavailable.", 
                                font=("Arial", 12), pady=20, justify="center")
        message_label.pack()
        
        # Instructions
        instructions = tk.Label(self.main_frame, 
                               text="Please try the following:\n\n" +
                               "• Wait a few minutes and run the application again\n" +
                               "• Check your internet connection\n" +
                               "• Try using a VPN if available\n" +
                               "• Contact support if the problem persists",
                               font=("Arial", 11), pady=20, justify="left")
        instructions.pack()
        
        # Close button
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=30)
        
        close_btn = tk.Button(button_frame, text="Close Application", command=self._on_close_app,
                             bg="#dc3545", fg="white", font=("Arial", 12, "bold"),
                             padx=30, pady=10)
        close_btn.pack()
    
    def _on_close_app(self):
        """Handle application close from failure screen"""
        import sys
        self.root.destroy()
        sys.exit(0)
    
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

def show_failure_screen():
    """Show failure screen when connection fails after retries"""
    gui = get_gui_instance()
    gui.show_failure_message()
    gui.root.mainloop()  # Keep GUI open until user closes

def show_completion_screen():
    """Show completion screen with finish button"""
    gui = get_gui_instance()
    gui.show_completion_message()
    gui.root.mainloop()  # Keep GUI open until user clicks finish

def close_gui():
    """Close the persistent GUI window"""
    global _gui_instance
    if _gui_instance:
        _gui_instance.close()
        _gui_instance = None

