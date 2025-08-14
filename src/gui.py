import tkinter as tk
from tkinter import messagebox

def show_sale_type_dialog(sale_type_options):
    """Show a GUI dialog for sale type selection"""
    selected_choice = None
    
    root = tk.Tk()
    root.title("Property Search - Sale Type")
    root.geometry("400x250")
    root.resizable(False, False)
    
    # Center the window
    root.eval('tk::PlaceWindow . center')
    
    # Title label
    title_label = tk.Label(root, text="What are you looking for?", 
                          font=("Arial", 14, "bold"), pady=10)
    title_label.pack()
    
    # Variable to store selection
    selection_var = tk.IntVar(value=-1)
    
    # Radio buttons for each option
    for idx, option in sale_type_options.items():
        radio = tk.Radiobutton(root, text=option['label'], 
                              variable=selection_var, value=idx,
                              font=("Arial", 12), pady=5)
        radio.pack(anchor="w", padx=50)
    
    def on_confirm():
        nonlocal selected_choice
        if selection_var.get() == -1:
            messagebox.showwarning("Selection Required", "Please select an option before continuing.")
            return
        selected_choice = selection_var.get()
        root.destroy()
    
    def on_cancel():
        nonlocal selected_choice
        selected_choice = None
        root.destroy()
    
    # Buttons frame
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    
    confirm_btn = tk.Button(button_frame, text="Continue", command=on_confirm,
                           bg="#007bff", fg="white", font=("Arial", 10, "bold"),
                           padx=20, pady=5)
    confirm_btn.pack(side="left", padx=10)
    
    cancel_btn = tk.Button(button_frame, text="Cancel", command=on_cancel,
                          bg="#6c757d", fg="white", font=("Arial", 10),
                          padx=20, pady=5)
    cancel_btn.pack(side="left", padx=10)
    
    # Make window modal
    root.transient()
    root.grab_set()
    root.focus_force()
    
    # Start the GUI loop
    root.mainloop()
    
    return selected_choice

def show_property_type_dialog(prop_options):
    """Show a GUI dialog for property type selection"""
    selected_choice = None
    
    root = tk.Tk()
    root.title("Property Search - Property Type")
    root.geometry("450x400")
    root.resizable(False, False)
    
    # Center the window
    root.eval('tk::PlaceWindow . center')
    
    # Title label
    title_label = tk.Label(root, text="Select Property Type", 
                          font=("Arial", 14, "bold"), pady=10)
    title_label.pack()
    
    # Variable to store selection
    selection_var = tk.IntVar(value=-1)
    
    # Buttons frame - pack first so it stays at bottom
    button_frame = tk.Frame(root)
    button_frame.pack(side="bottom", pady=15, fill="x")
    
    # Center the buttons
    button_container = tk.Frame(button_frame)
    button_container.pack()
    
    # Create a scrollable frame for radio buttons
    canvas_frame = tk.Frame(root)
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
                              variable=selection_var, value=idx,
                              font=("Arial", 11), pady=3, anchor="w")
        radio.pack(fill="x", padx=20)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def on_confirm():
        nonlocal selected_choice
        if selection_var.get() == -1:
            messagebox.showwarning("Selection Required", "Please select a property type before continuing.")
            return
        selected_choice = selection_var.get()
        root.destroy()
    
    def on_cancel():
        nonlocal selected_choice
        selected_choice = None
        root.destroy()
    
    confirm_btn = tk.Button(button_container, text="Continue", command=on_confirm,
                           bg="#007bff", fg="white", font=("Arial", 10, "bold"),
                           padx=20, pady=5)
    confirm_btn.pack(side="left", padx=10)
    
    cancel_btn = tk.Button(button_container, text="Cancel", command=on_cancel,
                          bg="#6c757d", fg="white", font=("Arial", 10),
                          padx=20, pady=5)
    cancel_btn.pack(side="left", padx=10)
    
    # Make window modal
    root.transient()
    root.grab_set()
    root.focus_force()
    
    # Start the GUI loop
    root.mainloop()
    
    return selected_choice