# Y2P1_LabGroupProject_Kinetics
Plot kinetics data fitted to the following equation:
```
A = b - c * e ^ (-k_obs * t)
```
where 
- `A`: absorbance at a given time
- `k_obs`: pseudo first order rate constant (= `k * [OH-]`)
- `t`: time (sec)
## Instructions
1. Place `plot.py` in **the same** directory/folder as the `.csv` files containing data recorded by the photometers
(If you don't want to plot all `.csv` files, place the ones you want to plot and this Python script into a new separate folder)
2. Within the folder containing `plot.py`, open a new terminal window, e.g. `powershell` (Shift + Right-click on the folder window > *Open Powershell window here*), type `python plot.py` and then press *Enter*
3. The script will generate plots as `.png` images and also a new single `.csv` file named `plotpy_out_[TIME].csv`, containing the fit parameters `b`, `c`, and `k_obs` for each `.csv` file processed.
4. The included Excel file can be used as an alternative if the script does not work properly.
