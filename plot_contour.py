import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the Excel file
file_path = "settlement_data.xlsx"  # Change this to your actual file path
df = pd.read_excel(file_path, sheet_name='Settlement Data')

# Extract distances and settlements
distances = df["Distance (m)"].values  # X-axis (along alignment)

# Extract chainages from column names and convert to numerical values
chainages = [float(col.split("(")[-1].split(")")[0].replace("+", "")) for col in df.columns[1:]]
original_chainages = np.array(chainages)

# Extract settlement values as a 2D array
settlements = df.iloc[:, 1:].values  # Y-axis (chainage) vs X-axis (distance)

# Create a mesh grid for plotting with original data only
X, Y = np.meshgrid(distances, original_chainages)
Z = settlements.T  # Transpose to match meshgrid shape

# Create the contour plot
plt.figure(figsize=(10, 5))
contour = plt.contourf(X, Y, Z, levels=20, cmap="jet")

# Add pink horizontal lines at each original chainage
for chainage in original_chainages:
    plt.axhline(y=chainage, color='pink', linestyle='--', linewidth=0.5, alpha=0.7)

# Add more visible vertical lines at 10m intervals
for distance in np.arange(min(distances), max(distances) + 10, 10):
    plt.axvline(x=distance, color='darkgray', linestyle='--', linewidth=1.0, alpha=1.0)

# Add a dark vertical line at distance 0
plt.axvline(x=0, color='black', linestyle='-', linewidth=1.5, alpha=1.0)

# Add colorbar and labels
plt.colorbar(contour, label="Settlement (m)")
plt.xlabel("Distance along alignment (m)")
plt.ylabel("Chainage (m)")
plt.title("Settlement Contour along the Alignment")

# Set custom tick intervals
plt.xticks(np.arange(min(distances), max(distances) + 10, 10))  # X interval = 10m
plt.yticks(np.arange(min(original_chainages), max(original_chainages) + 100, 100))  # Y interval = 100m, from first to last chainage

# Show the plot
plt.show()