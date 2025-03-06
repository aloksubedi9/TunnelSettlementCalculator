# TunnelSettlementCalculator
# Tunnel Settlement Calculator

Python tool for calculating and visualizing TBM tunnel settlement using Attewell et al. (1986) method. Features a Tkinter GUI for input, dropdowns for geological/overburden conditions, Matplotlib plots, and Excel export. Includes a contour plotter for settlement visualization along the alignment. Supports single and twin tunnels with Gaussian settlement profiles.
Features
tunnel_calculator.py: Tkinter GUI for:
Inputting TBM tunnel parameters (e.g., excavation diameter, depth).

Dropdowns for geological/overburden conditions, auto-updating VL and k values.

Visualizing settlement profiles with Matplotlib.

Exporting data to Excel (settlement_data.xlsx).

contour_plotter.py: Generates contour plots of settlements along the tunnel alignment using Excel data.

