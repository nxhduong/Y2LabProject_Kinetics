# Y2LabProject_Kinetics
Plot kinetics data fitted to the equation:
```
A = b - c * e ^ (-k_obs * t)
```
where 
- `A`: absorbance at a given time
- `k_obs`: pseudo first order rate constant
## Instructions
1. Place `plot.py` in **the same** directory as the `.csv` data files
(If you don't want to plot all `.csv` files, copy the ones you want to plot and this Python script into a new separate folder)
2. Within the above directory, open `powershell` ("Shift + Right-click > Open Powershell window here"), then type `python plot.py` and press `Enter`
3. The script will generate plots as `.png` images and also a new `.csv` file named `plotpy_out_(TIME).csv`, containing the fit parameters `b`, `c`, and `k_obs` for each `.csv` file processed.