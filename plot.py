import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from inspect import getfullargspec
import os
import subprocess
from datetime import datetime

# ----------------------------- FITTING OPTIONS --------------------------------

# Define the form of the function to be fit to the data (default: linear m*x+c)
fit_func = lambda x, b, c, k_obs: b - c * np.exp(-k_obs * x)
# Note that the first input to the function MUST be x.

# We need to collect the fit data for each file we process
fit_data = []
data_fnames = []

# We will create a plot from every csv file passed to the program
plt.rcParams.update({"font.size": 12})

for file in os.listdir(os.getcwd()):
    fname = os.fsdecode(file)
    
    if fname.endswith(".csv"):    
        # Load the data from the csv file. 
        try:
            data = np.loadtxt(fname, delimiter = ",", skiprows = 1)
        except Exception as error:
            print("Could not process file", fname, ". It has been skipped.\nError from Python:")
            print(error.args[0])
            continue
        
        # Choose which columns of data we want to use as our x and y values.
        # Note that the column indexes start from 0, not 1.    
        x = data[:, 0]
        y = data[:, 1]

        # ----- DATA MANIPULATION ----------------------------------------------
        # Example: Convert y to ln(y)
        # y = np.log(y) 

        # ----------------------------------------------------------------------

        # Calculate a line of best fit. The best fit parameters are stored in variable fit_params.
        try:
            fit_params, pcov = curve_fit(fit_func, x, y)
            fit_data.append(fit_params)            
        except Exception as error:
            print("Could not fit a curve to your data. Check the form of func, and your data. \nThe error from Python is:")
            print(error.args[0])
            
        # Add the name of each file we will process to a list
        data_fnames.append(fname)
        
        fig = plt.figure()
        fig.set_size_inches(16, 10)
        ax = plt.axes()

        # This creates a line graph, adding a straight line between each point in the input data file
        # Replace plot with scatter for a scatter graph
        ax.scatter(x, y)
        
        #----- CALCULATE MEAN SQUARE ERROR--------------------------------------

        # Make a list of "best fit" values, each corresponding to a value   
        
        # Calculate the value of the line of the best fit at every value of x
        y_fit = fit_func(x, *fit_params)
        # Calculate the root mean square error in the line of best fit.
        rmse = np.square(y - y_fit)
        rmse = np.average(rmse)
        rmse = np.sqrt(rmse)

        # Add a line of best fit to the plot, if fit is true
        # COMMENT THIS LINE (ADD "#" BEFORE THIS LINE) to remove line of best fit
        ax.plot(
            x, fit_func(x,*fit_params), 
            label = "RMSE={}\nb={};c={}\nk_obs={}\n".format(rmse, *fit_params), color = "red"
        )

        # ----- PLOTTING DETAILS -----------------------------------------------
        # Modify the following lines to be appropriate for the graph you are currently plotting
        ax.set_xlabel("sec")
        ax.set_ylabel("Abs")
        ax.legend()
        ax.set_title(fname)

        # ----------------------------------------------------------------------
        img_name: str = os.path.splitext(fname)[0] + ".png"
        fig.savefig(img_name)
        
        try:
            subprocess.Popen(["explorer", img_name])
        except Exception as err:
            print("Error trying to open image" + str(err))
        
        plt.close()

# Output the parameters of the line of best fit for every file processed
# if len(data_fnames)>0:
np.savetxt(
    "plotpy_out_{}.csv".format(str(datetime.now()).replace("-", "_").replace(" ", "_").replace(":", "_").split(".")[0]), 
    np.vstack((data_fnames, np.array(fit_data).T)).T, delimiter = ",", header = "File Name," + ",".join(getfullargspec(fit_func)[0][1:]), 
    comments = "", fmt = "%s"
    )

print("Done.")
