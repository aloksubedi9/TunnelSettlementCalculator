#Tunnel Settlement Calculator
Python tool for calculating and visualizing TBM tunnel settlement using Attewell et al. (1986) method. Features a Tkinter GUI for input, dropdowns for geological/overburden conditions, Matplotlib plots, and Excel export. Includes a contour plotter for settlement visualization along the alignment. Supports single and twin tunnels with Gaussian settlement profiles.
#Features
tunnel_calculator.py: Tkinter GUI for  
1.Inputting TBM tunnel parameters (e.g., excavation diameter, depth)  
2.Dropdowns for geological/overburden conditions, auto-updating VL and k values  
3.Visualizing settlement profiles with Matplotlib  
4.Exporting data to Excel (settlement_data.xlsx)

contour_plotter.py: Generates contour plots of settlements along the tunnel alignment using Excel data.

#Installation
Clone the repository  
bash
git clone https://github.com/yourusername/TunnelSettlementCalculator.git  
cd TunnelSettlementCalculator  

#Install dependencies  
bash
pip install -r requirements.txt  

Required packages: numpy, matplotlib, pandas, openpyxl

#Usage
1.Calculate Settlements  
bash
python src/tunnel_calculator.py  

Input parameters via the GUI. Select geological/overburden conditions from dropdowns. Click "Calculate & Plot" to view results and generate settlement_data.xlsx.

2.Visualize Settlement Contours  
bash
python src/contour_plotter.py  

Ensure settlement_data.xlsx exists in the working directory. Adjust file_path in contour_plotter.py if needed.

Detailed instructions are in docs/usage.md.
Theoretical Background
The tool uses the Attewell et al. (1986) method for TBM tunnel settlement, modeling the transverse settlement trough as a Gaussian curve. For twin tunnels, superposition is applied. Learn more in docs/theory.md.
Repository Structure
src/: Python scripts
tunnel_calculator.py
contour_plotter.py  

docs/: Documentation, including theory, usage, and screenshots  

output/: Sample settlement_data.xlsx (optional)  

requirements.txt: Python dependencies  

LICENSE: MIT License

Screenshots
GUI: docs/screenshots/gui_example.png
Contour Plot: docs/screenshots/contour_plot.png
License
MIT License (see LICENSE).
Contributing

