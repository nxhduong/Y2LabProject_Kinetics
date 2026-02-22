import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from inspect import getfullargspec
import os
import subprocess
from datetime import datetime

# Define the form of the function to be fit to the data
# Note that the first input to the function MUST be x
fit_func = lambda x, b, c, k_obs: b - c * np.exp(-k_obs * x)

# We need to collect the fit data for each file we process
fit_data = []
data_fnames = []

plt.rcParams.update({"font.size": 12})

for file in os.listdir(os.getcwd()):
    fname = os.fsdecode(file)
    
    if fname.endswith(".csv"): 
        try:
            data = np.loadtxt(fname, delimiter = ",", skiprows = 1)
        except Exception as err:
            print("Couldn't process ", fname, ". Skipped. Error: ")
            print(err.args[0])
            continue
        
        # Choose which columns of data we want to use as our x and y values.
        # Note that the column indexes start from 0, not 1.    
        x = data[:, 0]
        y = data[:, 1]

        # Calculate a line of best fit. The best fit parameters are stored in variable fit_params.
        try:
            fit_params, pcov = curve_fit(fit_func, x, y)
            fit_data.append(fit_params)            
        except Exception as error:
            print("Couldn't fit curve to your data. Check your data. Error from Python:")
            print(error.args[0])
        
        # Add the name of each file we will process to a list
        data_fnames.append(fname)
        
        # This creates a scatter graph
        fig = plt.figure()
        fig.set_size_inches(16, 10)
        ax = plt.axes()
        ax.scatter(x, y)
        
        # Calculate the root mean square error in the line of best fit and R-squared value.
        res = np.square(y - fit_func(x, *fit_params))
        r_2 = 1 - (np.sum(res) / np.sum((y - np.mean(y)) ** 2))
        rmse = np.sqrt(np.average(res))

        # Add a line of best fit to the plot, if fit is true
        # COMMENT THIS LINE (ADD "#" BEFORE THIS LINE) to remove line of best fit
        ax.plot(
            x, fit_func(x, *fit_params), 
            label = "RMSE={};r^2={};\nb={};c={};\nk_obs={}".format(rmse, r_2, *fit_params), 
            color = "red"
        )

        ax.set_xlabel("sec")
        ax.set_ylabel("Abs")
        ax.legend()
        ax.set_title(fname)
        
        img_name: str = os.path.splitext(fname)[0] + ".png"
        fig.savefig(img_name)
        
        try:
            subprocess.Popen(["explorer", img_name])
        except Exception as err:
            print("Error trying to open image: " + str(err))
        
        plt.close()

# Output the parameters of the line of best fit for every file processed
# if len(data_fnames) > 0:
np.savetxt(
    "plotpy_out_{}.csv".format(
        str(datetime.now())
            .replace("-", "_")
            .replace(" ", "_")
            .replace(":", "_")
            .split(".")[0]
    ), 
    np.vstack((data_fnames, np.array(fit_data).T)).T, 
    delimiter = ",", 
    header = "File Name," + ",".join(getfullargspec(fit_func)[0][1:]), 
    comments = "", 
    fmt = "%s"
)

print("Done.")