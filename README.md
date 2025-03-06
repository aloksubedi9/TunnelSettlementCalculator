# TunnelSettlementCalculator
# Tunnel Settlement Calculator

A Python-based tool for calculating and visualizing ground settlement due to tunneling, developed for the Mumbai Underground Road Tunnel Connectivity project. Implements the Attewell et al. (1986) and Rankin (1988) method for vertical settlement assessment.

## Features
- Tkinter GUI (`tunnel_calculator.py`) for inputting tunnel parameters.
- Dropdown menus for geological and overburden conditions, auto-updating VL and k values.
- Settlement visualization with Matplotlib.
- Export to Excel (`settlement_data.xlsx`) for further analysis.
- Contour plotting script (`contour_plotter.py`) to visualize settlement contours along the alignment.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TunnelSettlementCalculator.git
   cd TunnelSettlementCalculator
