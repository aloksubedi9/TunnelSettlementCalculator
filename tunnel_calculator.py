import tkinter as tk
from tkinter import ttk
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import load_workbook
import os

class TunnelData:
    def __init__(self, chainage, data_single=None, data_left=None, data_right=None, spacing=None):
        self.chainage = chainage
        self.data_single = data_single
        self.data_left = data_left
        self.data_right = data_right
        self.spacing = spacing
        self.x_values = None
        self.S_values = None  # For single tube
        self.S_LHS = None    # For double tube LHS
        self.S_RHS = None    # For double tube RHS
        self.S_combined = None  # For double tube combined

def calculate_and_plot():
    for widget in result_frame.winfo_children():
        widget.destroy()

    section_chainage = chainage_entry.get().strip()
    tunnel_type = tunnel_var.get()

    def process_tunnel_data(data_row, prefix=""):
        D = float(entries[data_row][0].get())
        road_level = float(entries[data_row][1].get())
        tunnel_axis_level = float(entries[data_row][2].get())
        ground_surface_level = float(entries[data_row][3].get())
        Zo = ground_surface_level - tunnel_axis_level
        geo_cond = entries[data_row][4].get()
        over_cond = entries[data_row][5].get()
        VL = float(entries[data_row][6].get())
        k = float(entries[data_row][7].get())
        
        i = k * Zo
        excavation_area = (math.pi * D**2) / 4
        Smax = (VL * 10 * excavation_area) / (math.sqrt(2 * math.pi) * i)
        
        return {
            "D": D, "road_level": road_level, "tunnel_axis_level": tunnel_axis_level,
            "ground_surface_level": ground_surface_level, "Zo": Zo, "geo_cond": geo_cond,
            "over_cond": over_cond, "VL": VL, "k": k, "i": i, 
            "excavation_area": excavation_area, "Smax": Smax
        }

    x_values = np.arange(-120, 121, 1)
    if tunnel_type == "Single Tube":
        data = process_tunnel_data(0)
        spacing = None
        td = TunnelData(section_chainage, data_single=data)
        y_values = x_values
        S = (data["Smax"] / 1000) * np.exp(-(y_values**2) / (2 * data["i"]**2)) * 1000
        td.x_values = x_values
        td.S_values = S
        tunnel_data.append(td)
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, S, label=f"Tunnel Settlement ({section_chainage})", color="blue")
    else:
        data_left = process_tunnel_data(0, "Left")
        data_right = process_tunnel_data(1, "Right")
        spacing = float(spacing_entry.get())
        td = TunnelData(section_chainage, data_left=data_left, data_right=data_right, spacing=spacing)
        y_LHS = x_values + spacing / 2
        y_RHS = x_values - spacing / 2
        S_LHS = (data_left["Smax"] / 1000) * np.exp(-(y_LHS**2) / (2 * data_left["i"]**2)) * 1000
        S_RHS = (data_right["Smax"] / 1000) * np.exp(-(y_RHS**2) / (2 * data_right["i"]**2)) * 1000
        S_combined = S_LHS + S_RHS
        td.x_values = x_values
        td.S_LHS = S_LHS
        td.S_RHS = S_RHS
        td.S_combined = S_combined
        tunnel_data.append(td)
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, S_LHS, label=f"LHS Tunnel Settlement ({section_chainage})", color="blue")
        plt.plot(x_values, S_RHS, label=f"RHS Tunnel Settlement ({section_chainage})", color="red")
        plt.plot(x_values, S_combined, label=f"Combined Settlement ({section_chainage})", color="green", linestyle="dashed", linewidth=2)

    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='gray', linestyle="--", linewidth=0.5)
    plt.gca().invert_yaxis()
    plt.xlabel("Distance (m)")
    plt.ylabel("Settlement (mm)")
    plt.title(f"Settlement Profile: {section_chainage}")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Display results in GUI
    def display_results(data, col_start, row_start, prefix=""):
        labels = [
            f"{prefix}Excavation Diameter (m)", f"{prefix}Road Level (m, RL)",
            f"{prefix}Tunnel Axis Level (m, RL)", f"{prefix}Ground Surface Level (m, RL)",
            f"{prefix}Tunnel Axis Depth (m)", f"{prefix}Geological Condition",
            f"{prefix}Overburden Condition", f"{prefix}Volume Loss %",
            f"{prefix}k Parameter", f"{prefix}i (m)", f"{prefix}Excavation Area (m³/m)",
            f"{prefix}Maximum Settlement (m)"
        ]
        values = [
            data["D"], data["road_level"], data["tunnel_axis_level"],
            data["ground_surface_level"], data["Zo"], data["geo_cond"],
            data["over_cond"], data["VL"], data["k"], data["i"],
            data["excavation_area"], data["Smax"]
        ]
        
        for i, (label, value) in enumerate(zip(labels, values)):
            bg_color = "#f0fff0" if i < 9 else "#fff0f0"
            tk.Label(result_frame, text=label, bg=bg_color, font=("Arial", 10)).grid(row=row_start + i, column=col_start, padx=5, pady=2, sticky="w")
            tk.Label(result_frame, text=f"{value:.4f}" if isinstance(value, float) else value,
                    bg=bg_color, font=("Arial", 10, "bold")).grid(row=row_start + i, column=col_start + 1, padx=5, pady=2)

    for idx, td in enumerate(tunnel_data):
        row_offset = idx * 15
        tk.Label(result_frame, text=f"Section Chainage: {td.chainage}", 
                 bg="#e6f3ff", font=("Arial", 12, "bold")).grid(row=row_offset, column=0, columnspan=4, pady=5)
        
        if td.data_single:
            display_results(td.data_single, 0, row_offset + 1)
        else:
            display_results(td.data_left, 0, row_offset + 1, "LHS ")
            display_results(td.data_right, 2, row_offset + 1, "RHS ")
            tk.Label(result_frame, text="Spacing Between Tunnels (m)", 
                    bg="#f0fff0", font=("Arial", 10)).grid(row=row_offset + 13, column=0, padx=5, pady=2, sticky="w")
            tk.Label(result_frame, text=f"{td.spacing:.2f}", 
                    bg="#f0fff0", font=("Arial", 10, "bold")).grid(row=row_offset + 13, column=1, padx=5, pady=2)

    # Export to Excel
    excel_file = "settlement_data.xlsx"
    sheet_name = "Settlement Data"
    
    # Prepare data for export
    data_dict = {"Distance (m)": x_values}
    for td in tunnel_data:
        if td.data_single:
            data_dict[f"Settlement ({td.chainage})"] = td.S_values
        else:
            data_dict[f"Combined Settlement ({td.chainage})"] = td.S_combined
    
    # Create DataFrame
    df = pd.DataFrame(data_dict)
    
    # Write to Excel (append if file exists)
    if os.path.exists(excel_file):
        book = load_workbook(excel_file)
        with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        df.to_excel(excel_file, sheet_name=sheet_name, index=False)

def reset_form():
    global tunnel_data
    tunnel_data = []
    for widget in result_frame.winfo_children():
        widget.destroy()
    chainage_entry.delete(0, tk.END)
    for entry_list in entries:
        for entry in entry_list:
            entry.delete(0, tk.END)
    if tunnel_var.get() == "Double Tube":
        spacing_entry.delete(0, tk.END)

def add_chainage():
    chainage_entry.delete(0, tk.END)
    for entry_list in entries:
        for entry in entry_list:
            entry.delete(0, tk.END)
    if tunnel_var.get() == "Double Tube":
        spacing_entry.delete(0, tk.END)

def move_focus(event):
    widget = event.widget
    if event.keysym == "Up":
        widget.tk_focusPrev().focus()
    elif event.keysym == "Down":
        widget.tk_focusNext().focus()
    elif event.keysym == "Left" and tunnel_var.get() == "Double Tube":
        current_row = entries[1].index(widget) if widget in entries[1] else -1
        if current_row >= 0 and widget in entries[1]:
            entries[0][current_row].focus()
    elif event.keysym == "Right" and tunnel_var.get() == "Double Tube":
        current_row = entries[0].index(widget) if widget in entries[0] else -1
        if current_row >= 0 and widget in entries[0]:
            entries[1][current_row].focus()
    return "break"

def update_form():
    for widget in input_frame.winfo_children():
        widget.destroy()
    
    global entries, spacing_entry
    entries = []
    
    # Define the table data for V and k values
    table_data = {
        "Soil-like Material": {
            "Soil-like Material": {"C<=0": {"V": 1.0, "k": 0.3}, "C>0": {"V": 0.8, "k": 0.5}},
            "Mixed Conditions (Soil and Rock Mass)": {"C<=0": {"V": 0.6, "k": 0.3}, "C>0": {"V": 0.5, "k": 0.5}},
            "Faults and/or Weathered Bands": {"C<=0": {"V": 0.6, "k": 0.3}, "C>0": {"V": 0.5, "k": 0.5}},
            "Discontinuous Rock Mass and Weak Rock": {"C<=0": {"V": 0.4, "k": 0.6}, "C>0": {"V": 0.4, "k": 0.6}}
        },
        "Mixed Conditions (Soil and Rock Mass)": {
            "Soil-like Material": {"C<=0": {"V": 1.0, "k": 0.3}, "C>0": {"V": 0.8, "k": 0.6}},
            "Mixed Conditions (Soil and Rock Mass)": {"C<=0": {"V": 0.7, "k": 0.3}, "C>0": {"V": 0.5, "k": 0.5}},
            "Faults and/or Weathered Bands": {"C<=0": {"V": 0.7, "k": 0.3}, "C>0": {"V": 0.5, "k": 0.5}},
            "Discontinuous Rock Mass and Weak Rock": {"C<=0": {"V": 0.5, "k": 0.6}, "C>0": {"V": 0.5, "k": 0.6}}
        },
        "Faults and/or Weathered Bands": {
            "Soil-like Material": {"C<=0": {"V": 1.0, "k": 0.3}, "C>0": {"V": 0.8, "k": 0.7}},
            "Mixed Conditions (Soil and Rock Mass)": {"C<=0": {"V": 0.9, "k": 0.3}, "C>0": {"V": 0.5, "k": 0.5}},
            "Faults and/or Weathered Bands": {"C<=0": {"V": 0.9, "k": 0.3}, "C>0": {"V": 0.5, "k": 0.5}},
            "Discontinuous Rock Mass and Weak Rock": {"C<=0": {"V": 0.4, "k": 0.7}, "C>0": {"V": 0.4, "k": 0.7}}
        },
        "Discontinuous Rock Mass and Weak Rock": {
            "Soil-like Material": {"C<=0": {"V": 1.0, "k": 0.3}, "C>0": {"V": 0.8, "k": 0.7}},
            "Mixed Conditions (Soil and Rock Mass)": {"C<=0": {"V": 0.5, "k": 0.6}, "C>0": {"V": 0.5, "k": 0.6}},
            "Faults and/or Weathered Bands": {"C<=0": {"V": 0.65, "k": 0.6}, "C>0": {"V": 0.65, "k": 0.6}},
            "Discontinuous Rock Mass and Weak Rock": {"C<=0": {"V": 0.2, "k": 0.7}, "C>0": {"V": 0.2, "k": 0.7}}
        }
    }

    # Options for dropdowns
    overburden_options = [
        "Soil-like Material",
        "Mixed Conditions (Soil and Rock Mass)",
        "Faults and/or Weathered Bands",
        "Discontinuous Rock Mass and Weak Rock"
    ]
    geological_options = overburden_options  # Same options for geological condition

    # Function to update V and k based on selections
    def update_vk_values(section_entries, geo_var, over_var, vl_entry, k_entry, C_value=0):
        geo_cond = geo_var.get()
        over_cond = over_var.get()
        if geo_cond and over_cond:  # Ensure selections are made
            condition = "C<=0" if C_value <= 0 else "C>0"
            values = table_data[over_cond][geo_cond][condition]
            vl_entry.delete(0, tk.END)
            vl_entry.insert(0, str(values["V"]))
            k_entry.delete(0, tk.END)
            k_entry.insert(0, str(values["k"]))

    tunnel_type = tunnel_var.get()
    
    if tunnel_type == "Single Tube":
        labels = [
            "Excavation Diameter (m)", "Road Level (m, RL)",
            "Tunnel Axis Level (m, RL)", "Ground Surface Level (m, RL)",
            "Geological Condition", "Overburden Condition",
            "Volume Loss %", "k Parameter"
        ]
        section_entries = []
        tk.Label(input_frame, text="Tunnel Parameters", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=2)
        
        # Create entries for the first 4 labels
        for i in range(4):
            tk.Label(input_frame, text=labels[i], bg="#f0f0f0").grid(row=i+1, column=0, padx=5, pady=2, sticky="w")
            entry = tk.Entry(input_frame)
            entry.grid(row=i+1, column=1, padx=5, pady=2)
            section_entries.append(entry)
        
        # Dropdown for Geological Condition
        tk.Label(input_frame, text=labels[4], bg="#f0f0f0").grid(row=5, column=0, padx=5, pady=2, sticky="w")
        geo_var = tk.StringVar()
        geo_dropdown = ttk.Combobox(input_frame, textvariable=geo_var, values=geological_options, state="readonly")
        geo_dropdown.grid(row=5, column=1, padx=5, pady=2)
        section_entries.append(geo_dropdown)
        
        # Dropdown for Overburden Condition
        tk.Label(input_frame, text=labels[5], bg="#f0f0f0").grid(row=6, column=0, padx=5, pady=2, sticky="w")
        over_var = tk.StringVar()
        over_dropdown = ttk.Combobox(input_frame, textvariable=over_var, values=overburden_options, state="readonly")
        over_dropdown.grid(row=6, column=1, padx=5, pady=2)
        section_entries.append(over_dropdown)
        
        # Entries for Volume Loss % and k Parameter (will be auto-filled)
        tk.Label(input_frame, text=labels[6], bg="#f0f0f0").grid(row=7, column=0, padx=5, pady=2, sticky="w")
        vl_entry = tk.Entry(input_frame)
        vl_entry.grid(row=7, column=1, padx=5, pady=2)
        section_entries.append(vl_entry)
        
        tk.Label(input_frame, text=labels[7], bg="#f0f0f0").grid(row=8, column=0, padx=5, pady=2, sticky="w")
        k_entry = tk.Entry(input_frame)
        k_entry.grid(row=8, column=1, padx=5, pady=2)
        section_entries.append(k_entry)
        
        # Bind dropdown selections to update V and k (assuming C=0 for now; adjust C_value as needed)
        C_value = 0  # You can make this a user input if needed
        geo_dropdown.bind("<<ComboboxSelected>>", lambda e: update_vk_values(section_entries, geo_var, over_var, vl_entry, k_entry, C_value))
        over_dropdown.bind("<<ComboboxSelected>>", lambda e: update_vk_values(section_entries, geo_var, over_var, vl_entry, k_entry, C_value))
        
        entries.append(section_entries)
    
    else:  # Double Tube
        labels = [
            "Excavation Diameter (m)", "Road Level (m, RL)",
            "Tunnel Axis Level (m, RL)", "Ground Surface Level (m, RL)",
            "Geological Condition", "Overburden Condition",
            "Volume Loss %", "k Parameter"
        ]
        
        tk.Label(input_frame, text="LHS Tunnel", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=0, column=0, pady=2)
        tk.Label(input_frame, text="RHS Tunnel", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=0, column=2, pady=2)
        
        lhs_entries = []
        rhs_entries = []
        for i in range(4):  # First 4 entries are regular inputs
            tk.Label(input_frame, text=labels[i], bg="#f0f0f0").grid(row=i+1, column=0, padx=5, pady=2, sticky="w")
            lhs_entry = tk.Entry(input_frame)
            lhs_entry.grid(row=i+1, column=1, padx=5, pady=2)
            lhs_entries.append(lhs_entry)
            
            tk.Label(input_frame, text=labels[i], bg="#f0f0f0").grid(row=i+1, column=2, padx=5, pady=2, sticky="w")
            rhs_entry = tk.Entry(input_frame)
            rhs_entry.grid(row=i+1, column=3, padx=5, pady=2)
            rhs_entries.append(rhs_entry)
        
        # LHS Geological Condition Dropdown
        tk.Label(input_frame, text=labels[4], bg="#f0f0f0").grid(row=5, column=0, padx=5, pady=2, sticky="w")
        lhs_geo_var = tk.StringVar()
        lhs_geo_dropdown = ttk.Combobox(input_frame, textvariable=lhs_geo_var, values=geological_options, state="readonly")
        lhs_geo_dropdown.grid(row=5, column=1, padx=5, pady=2)
        lhs_entries.append(lhs_geo_dropdown)
        
        # RHS Geological Condition Dropdown
        tk.Label(input_frame, text=labels[4], bg="#f0f0f0").grid(row=5, column=2, padx=5, pady=2, sticky="w")
        rhs_geo_var = tk.StringVar()
        rhs_geo_dropdown = ttk.Combobox(input_frame, textvariable=rhs_geo_var, values=geological_options, state="readonly")
        rhs_geo_dropdown.grid(row=5, column=3, padx=5, pady=2)
        rhs_entries.append(rhs_geo_dropdown)
        
        # LHS Overburden Condition Dropdown
        tk.Label(input_frame, text=labels[5], bg="#f0f0f0").grid(row=6, column=0, padx=5, pady=2, sticky="w")
        lhs_over_var = tk.StringVar()
        lhs_over_dropdown = ttk.Combobox(input_frame, textvariable=lhs_over_var, values=overburden_options, state="readonly")
        lhs_over_dropdown.grid(row=6, column=1, padx=5, pady=2)
        lhs_entries.append(lhs_over_dropdown)
        
        # RHS Overburden Condition Dropdown
        tk.Label(input_frame, text=labels[5], bg="#f0f0f0").grid(row=6, column=2, padx=5, pady=2, sticky="w")
        rhs_over_var = tk.StringVar()
        rhs_over_dropdown = ttk.Combobox(input_frame, textvariable=rhs_over_var, values=overburden_options, state="readonly")
        rhs_over_dropdown.grid(row=6, column=3, padx=5, pady=2)
        rhs_entries.append(rhs_over_dropdown)
        
        # LHS Volume Loss % and k Parameter
        tk.Label(input_frame, text=labels[6], bg="#f0f0f0").grid(row=7, column=0, padx=5, pady=2, sticky="w")
        lhs_vl_entry = tk.Entry(input_frame)
        lhs_vl_entry.grid(row=7, column=1, padx=5, pady=2)
        lhs_entries.append(lhs_vl_entry)
        
        tk.Label(input_frame, text=labels[7], bg="#f0f0f0").grid(row=8, column=0, padx=5, pady=2, sticky="w")
        lhs_k_entry = tk.Entry(input_frame)
        lhs_k_entry.grid(row=8, column=1, padx=5, pady=2)
        lhs_entries.append(lhs_k_entry)
        
        # RHS Volume Loss % and k Parameter
        tk.Label(input_frame, text=labels[6], bg="#f0f0f0").grid(row=7, column=2, padx=5, pady=2, sticky="w")
        rhs_vl_entry = tk.Entry(input_frame)
        rhs_vl_entry.grid(row=7, column=3, padx=5, pady=2)
        rhs_entries.append(rhs_vl_entry)
        
        tk.Label(input_frame, text=labels[7], bg="#f0f0f0").grid(row=8, column=2, padx=5, pady=2, sticky="w")
        rhs_k_entry = tk.Entry(input_frame)
        rhs_k_entry.grid(row=8, column=3, padx=5, pady=2)
        rhs_entries.append(rhs_k_entry)
        
        # Spacing entry
        tk.Label(input_frame, text="Spacing Between Tunnels (m)", bg="#f0f0f0").grid(row=9, column=0, padx=5, pady=2, sticky="w")
        spacing_entry = tk.Entry(input_frame)
        spacing_entry.grid(row=9, column=1, padx=5, pady=2, sticky="w")
        
        # Bind dropdowns to update V and k (assuming C=0 for now; adjust C_value as needed)
        C_value = 0  # You can make this a user input if needed
        lhs_geo_dropdown.bind("<<ComboboxSelected>>", lambda e: update_vk_values(lhs_entries, lhs_geo_var, lhs_over_var, lhs_vl_entry, lhs_k_entry, C_value))
        lhs_over_dropdown.bind("<<ComboboxSelected>>", lambda e: update_vk_values(lhs_entries, lhs_geo_var, lhs_over_var, lhs_vl_entry, lhs_k_entry, C_value))
        rhs_geo_dropdown.bind("<<ComboboxSelected>>", lambda e: update_vk_values(rhs_entries, rhs_geo_var, rhs_over_var, rhs_vl_entry, rhs_k_entry, C_value))
        rhs_over_dropdown.bind("<<ComboboxSelected>>", lambda e: update_vk_values(rhs_entries, rhs_geo_var, rhs_over_var, rhs_vl_entry, rhs_k_entry, C_value))
        
        entries.append(lhs_entries)
        entries.append(rhs_entries)

# GUI Setup
root = tk.Tk()
root.title("Tunnel Settlement Calculator")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Section Chainage:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
chainage_entry = tk.Entry(root, width=15)
chainage_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Tunnel Type:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
tunnel_var = tk.StringVar(value="Double Tube")
tunnel_dropdown = ttk.Combobox(root, textvariable=tunnel_var, values=["Single Tube", "Double Tube"], state="readonly")
tunnel_dropdown.grid(row=1, column=1, padx=5, pady=5)
tunnel_dropdown.bind("<<ComboboxSelected>>", lambda e: update_form())

input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.grid(row=2, column=0, columnspan=2, pady=10)

result_frame = tk.Frame(root, bg="#e6f3ff")
result_frame.grid(row=3, column=0, columnspan=4, pady=10)

button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(button_frame, text="Calculate & Plot", command=calculate_and_plot, bg="#4CAF50", fg="white", 
         font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Reset", command=reset_form, bg="#FF5733", fg="white", 
         font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Add Chainage", command=add_chainage, bg="#3498DB", fg="white", 
         font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5)

tunnel_data = []
update_form()
root.mainloop()