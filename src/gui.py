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