# reecon
**Script to extract rare earth elements concentration from spectrophotometric measurements.**

This is an script to measure Pr, Nd, and Dy concentrations using spectrophotometric measurements.
The reported results correspond to calibration curves using H2O solutions. (ADD acetate solutions)
Calibrations depend on the used equipement. Used calibrations are imported from the file 'calibration_defs.py'

## Pre-defined funcionts
File 'analysis_defs.py' contains pre-defined functions used in the analysis. In the current version only the following functions are used:
- get_dhb_peak_spectrum(): search for the difference between the selected RE peaks and the corresponding minimum values. (MORE DETAIL NEEDED HERE)
- plot_dhb_peak_spectrum(): export a png plot with graphical information. (MORE DETAIL NEEDED HERE)

## Needed modules to run in python3:
- sys
- os
- numpy
- pylab
- statsmodels
- math
- termcolor

## Characteristic wavelengths
The script find the height of the characteristic peaks for each REE.

Characteristic peaks:
- lambda = 365 nm for Dy
- lambda = 444 nm for Pr
- lambda = 740 nm for Nd

The local minima around each peak is searched within a window [lambda-delta, lambda+delta]
- delta = 15 nm for Dy
- delta = 27 nm for Pr
- delta = 50 nm for Nd

If the local minima are equal to either window limit, a warning message is displayed using the war variable.

These values are defined in the input.txt file as:

`#Pr	Nd	Dy`

`444	740	365`

`17	50	15`
    
When the graphical output is set, it plots the analyzed spectra.
- Vertical lines correspond to the analyzed characteristic peaks.
- Shaded rectangles around each peak correspond to the analysis window.

## More information
For more information check the accompanying file reecon_pkg.html in your preferred browser.

## Run python run
To run in a terminal:
`python3 reecon.py input.txt`

## Licence
This project is made by Enio Lima Jr., Javier Curiale and Sebastian Bustingorry, from Bariloche, Argentina.

Licensed under the MIT License - see the LICENSE file for details.
