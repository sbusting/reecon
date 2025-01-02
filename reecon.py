#!/usr/bin/env python
# coding: utf-8

#reecon_01.beta

# In[1]:

from analysis_defs import *
from calibration_defs import *
import sys

# In[2]:

print(f'\nThe reported results correspond to calibration curves using H2O solutions.\n')
#Read input file
#with open('input.txt', 'r') as file:
with open(sys.argv[1], 'r') as file:
    lines = [line.strip() for line in file]
    path_output = lines[4]
    name = lines[6]
    path_spectrum = lines[9]
    path_background = lines[11]
    # print(lines)
    print(f'Task name: {path_output + name}')
    print(f'Spectrum file: {path_spectrum}')
    print(f'Background file: {path_background}')
    
    lam_Pr, lam_Nd, lam_Dy =  int(lines[15].split()[0]), int(lines[15].split()[1]), int(lines[15].split()[2])
    lam_all = [lam_Nd, lam_Pr, lam_Dy]
    Dlam_Pr, Dlam_Nd, Dlam_Dy =  int(lines[16].split()[0]), int(lines[16].split()[1]), int(lines[16].split()[2])
    Dlam_all = [Dlam_Nd, Dlam_Pr, Dlam_Dy]
    print('\nWavelengths to be analyzed for Pr, Nd and Dy (in nm)')
    print(lam_Pr, lam_Nd, lam_Dy)
    print('Windows width to be analyzed (in nm)')
    print(Dlam_Pr, Dlam_Nd, Dlam_Dy)

inp = input('\nWould you like to have a graphical output? (y/n):')
if inp in ['y','Y','yes','Yes','YES']:
    graphical_output = 'yes'
elif inp in ['n','N','no','No','NO']:
    graphical_output = 'no'
else:
    print('Error value for graphical output variable. The script do not understand whether you selected ''yes'' or ''no''.')
    print('Run again and give a proper answer when asked about the graphical output.')
    sys.exit()
print(f'Graphical output: {graphical_output}')
    



# In[3]:


data_sp = {}
fond_sp = {}

ff1 = path_spectrum
ff2 = path_background
data  = np.loadtxt(ff1, skiprows = 2, delimiter =',', unpack = True, encoding='ISO-8859-1')
val1 = [data[0],data[2]+data[3]*1e-6]
data  = np.loadtxt(ff2, skiprows = 2, delimiter =',', unpack = True, encoding='ISO-8859-1')
val2 = [data[0],data[2]+data[3]*1e-6]
data_sp[name] = val1
fond_sp[name] = val2


#print(f'\nData loaded: {data_sp.keys()}\n')


# In[4]:


dhb_abs_single_serie, warr = get_dhb_peak_spectrum(data_sp, fond_sp, list(data_sp.keys()), lam_all, Dlam_all)


# In[5]:


# estimación de las concentraciones
# print(dhb_abs_single_serie)

print('Results:')
concentrations = {}
#Pr
con_Pr, err_con_Pr = calib_Pr_H2O(dhb_abs_single_serie[1])
concentrations['Pr'] = [con_Pr, err_con_Pr]
print(f'Concentration Pr: {con_Pr}({err_con_Pr})\n')

#Nd
con_Nd, err_con_Nd = calib_Nd_H2O(dhb_abs_single_serie[0])
concentrations['Nd'] = [con_Nd, err_con_Nd]
print(f'Concentration Nd: {con_Nd}({err_con_Nd})\n')

#Dy
con_Dy, err_con_Dy = calib_Dy_H2O(dhb_abs_single_serie[2])
concentrations['Dy'] = [con_Dy, err_con_Dy]
print(f'Concentration Dy: {con_Dy}({err_con_Dy})\n')


# In[6]:

if graphical_output == 'yes':
    plot_dhb_peak_spectrum(data_sp, fond_sp, list(data_sp.keys()), lam_all, Dlam_all, path_output, name, concentrations)
    plot_spectra(data_sp, fond_sp, list(data_sp.keys()), lam_all, path_output, name)
    print(f'Graphical output in {name}.png')
else:
    print('No graphical output')


# In[ ]:

file_output = open(path_output + name + '_results.txt', 'w')
file_output.write('Measured concentration of rare earth elements using spectrophotometry\n')
file_output.write('Pr (ppm)\terror_Pr (ppm)\tNd (ppm)\terror_Nd (ppm)\tDy (ppm)\terror_Dy (ppm)\n')
output_str = [str(con_Pr), str(err_con_Pr), str(con_Nd), str(err_con_Nd), str(con_Dy), str(err_con_Dy)]
for val in output_str:
    file_output.write(val + '\t\t')
file_output.write('\n\nThe analyzed wavelength peaks and their corresponding window sizes are\n')
file_output.write('lambda_Pr (nm)\twindow_Pr (nm)\tlambda_Nd (nm)\twindow_Nd (nm)\tlambda_Dy (nm)\twindow_Dy (nm)\n')
output_str = [str(lam_Pr), str(Dlam_Pr), str(lam_Nd), str(Dlam_Nd), str(lam_Dy), str(Dlam_Dy)]
for val in output_str:
    file_output.write(val + '\t\t')
file_output.write('\n\n')
file_output.write('The analyzed spectrum file is:\n')
file_output.write(ff1 + '\n')
file_output.write('The background file is:\n')
file_output.write(ff2 + '\n')
file_output.write('\n')
file_output.write('The output files are located in:\n')
file_output.write(path_output + '\n')
file_output.write('\n')

if warr:
    file_output.write('-----------------------------------------\n')
    file_output.write('WARNING!!\n')
    file_output.write('The minimum value to the left of some peak is in the limit of the range of analysis.\n')
    file_output.write('Check the graphical output.\n')
    file_output.write('The analysis is not reliable.\n')
    file_output.write('Check the shape of the peaks in the spectrum... or talk to someone.\n')
    file_output.write('-----------------------------------------\n\n')
file_output.write('Please read the README.txt file for more information.\n')




# In[ ]:




