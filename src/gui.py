import tkinter as tk
from tkinter import messagebox

class PropertySearchGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Property Search")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        self.root.eval('tk::PlaceWindow . center')
        self.root.transient()
        self.root.grab_set()
        self.root.focus_force()
        
        self.selected_choice = None
        self.selection_var = tk.IntVar(value=-1)
        
        # Create main container
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        
    def clear_content(self):
        """Clear all content from the main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.selection_var.set(-1)
        self.selected_choice = None
    
    def show_sale_type_selection(self, sale_type_options):
        """Show sale type selection in the same window"""
        self.clear_content()
        self.root.title("Property Search - Sale Type")
        self.root.geometry("400x250")
        
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
        self.root.geometry("450x400")
        
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

def close_gui():
    """Close the persistent GUI window"""
    global _gui_instance
    if _gui_instance:
        _gui_instance.close()
        _gui_instance = None

