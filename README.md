# Tunnel Settlement Calculator

Python tool for calculating and visualizing TBM tunnel settlement using the Attewell et al. (1986) method. Features include a Tkinter GUI for input, dropdowns for geological/overburden conditions, Matplotlib plots, and Excel export. Supports single and twin tunnels with Gaussian settlement profiles.

## Features

- **`tunnel_calculator.py`**: Tkinter GUI for:
  - Inputting TBM tunnel parameters (e.g., excavation diameter, depth)
  - Selecting geological/overburden conditions with auto-updating VL and k values
  - Visualizing settlement profiles using Matplotlib
  - Exporting data to Excel (`settlement_data.xlsx`)

- **`plot_contour.py`**: Generates contour plots of settlements along the tunnel alignment using Excel data.

## Installation

### Clone the Repository

```bash
git clone https://github.com/aloksubedi9/TunnelSettlementCalculator.git
cd TunnelSettlementCalculator
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages**: `numpy`, `matplotlib`, `pandas`, `openpyxl`

## Usage

### Calculate Settlements

```bash
python tunnel_calculator.py
```

- Input parameters via the GUI.
- Select geological/overburden conditions from dropdowns.
- Click **"Calculate & Plot"** to view results and generate `settlement_data.xlsx`.

### Visualize Settlement Contours

```bash
python plot_contour.py
```

- Ensure `settlement_data.xlsx` exists in the working directory.
- Adjust the file path in `plot_contour.py` if needed.

## Theoretical Background

The tool utilizes the Attewell et al. (1986) method for TBM tunnel settlement, modeling the transverse settlement trough as a Gaussian curve. For twin tunnels, superposition is applied.

## Repository Structure

```
TunnelSettlementCalculator/
├── tunnel_calculator.py      # Main GUI-based settlement calculator
├── plot_contour.py           # Settlement contour visualization
├── requirements.txt          # Python dependencies
├── README.md                 # Project description and instructions
├── contourexample.png        # Example contour plot image
└── settlementprofile.jpg     # Example settlement profile image
```

## Screenshots

- **Contour Plot Example**: `contourexample.png`
- **Settlement Profile Example**: `settlementprofile.jpg`

## License

MIT License (see `LICENSE`).

## Contributing

Contributions are welcome. Please open an issue or submit a pull request for improvements or bug fixes.
