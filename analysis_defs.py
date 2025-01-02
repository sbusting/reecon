#!/usr/bin/env python
# coding: utf-8

# In[30]:


#get_ipython().run_line_magic('matplotlib', 'inline')
import os
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
import statsmodels.api as sm
from termcolor import colored

# In[32]:


#formateo opcional, como sale en la presentacion
rcParams['text.usetex'] = True
# rcParams['text.latex.unicode'] = True
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
rcParams['axes.labelsize'] = 20
rcParams['legend.fontsize'] = 14
rcParams['figure.titlesize'] = 16
rcParams['font.size'] = 18
rcParams['font.family'] = 'serif'


# In[33]:


color1 = '#21897e'
color2 = '#3ba99c'
color3 = '#69d1c5'
color4 = '#7ebce6'
color5 = '#8980f5'
color6 = '#505050'
color7 = '#ffdf01'
colist = [color1, color2, color3, color4, color5, color6, color7]


# In[38]:


#linear fit
def fit_linear(x,y):
    model = sm.OLS(y, sm.add_constant(x))
    results = model.fit()
    return results.params, results.bse, results
# print(result.summary())


# In[39]:


def get_max_peak(dic, fon, ccc, lam):
    max_list = []
    for ii in range(len(ccc)):
        auxlist = list(dic.get(ccc[ii])[0])
        auxindex = auxlist.index(lam)
        fondo = fon.get(ccc[ii])[1]
        minvalue = min(dic.get(ccc[ii])[1]-fondo)
        max_list.append(dic.get(ccc[ii])[1][auxindex]-fondo[auxindex]-minvalue)
    return max_list

def plot_max_peak(dic, fon, ccc, lam, legtitle):
    max_list = []
    for ii in range(len(ccc)):
        auxlist = list(dic.get(ccc[ii])[0])
        auxindex = auxlist.index(lam)
        fondo = fon.get(ccc[ii])[1]
        minvalue = min(dic.get(ccc[ii])[1]-fondo)
        plt.plot(dic.get(ccval[ii])[0],dic.get(ccval[ii])[1]-fondo-minvalue, label = ccc[ii])
        max_list.append(dic.get(ccc[ii])[1][auxindex]-fondo[auxindex]-minvalue)
    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), title = legtitle)
    plt.plot([lam,lam],[0,1.5*max(max_list)], '--', color = 'grey')
    plt.plot(lam*np.ones(len(max_list)),max_list,'ok')
    plt.xlabel('$\lambda$(nm)')
    plt.ylabel('absorbance')
    plt.xlim(lam-50,lam+50)
        


# In[40]:


def get_dhb_peak(dic, fon, ccc, lam, dlam):
    max_list = []
    for ii in range(len(ccc)):
        fondo = fon.get(ccc[ii])[1]
        # auxlist = list(dic.get(ccc[ii])[0])
        lamlist = list(dic.get(ccc[ii])[0])
        auxindex = lamlist.index(lam)
        minrangeindex = lamlist.index(lam-dlam)
        maxrangeindex = lamlist.index(lam+dlam)
        
        diflist = list(dic.get(ccc[ii])[1]-fondo)
        
        minabs = min(diflist[minrangeindex:auxindex])
        indices = [ind for ind, ele in enumerate(diflist[minrangeindex:auxindex]) if ele == minabs]
        minlam = lamlist[minrangeindex + max(indices)]
        maxabs = min(diflist[auxindex:maxrangeindex])
        indices = [ind for ind, ele in enumerate(diflist[auxindex:maxrangeindex]) if ele == maxabs]
        maxlam = lamlist[auxindex + max(indices)]
        auxabs = (minabs-maxabs)/(minlam-maxlam)*(lamest-minlam)+minabs
        hvalue = diflist[auxindex]-auxabs
        
        max_list.append(hvalue)

    return max_list

def plot_dhb_peak(dic, fon, ccc, lam, dlam, name):
    max_list = []
    for ii in range(len(ccc)):
        fondo = fon.get(ccc[ii])[1]
        # auxlist = list(dic.get(ccc[ii])[0])
        lamlist = list(dic.get(ccc[ii])[0])
        auxindex = lamlist.index(lam)
        minrangeindex = lamlist.index(lam-dlam)
        maxrangeindex = lamlist.index(lam+dlam)
        
        diflist = list(dic.get(ccc[ii])[1]-fondo)
        
        minabs = min(diflist[minrangeindex:auxindex])
        indices = [ind for ind, ele in enumerate(diflist[minrangeindex:auxindex]) if ele == minabs]
        minlam = lamlist[minrangeindex + max(indices)]
        maxabs = min(diflist[auxindex:maxrangeindex])
        indices = [ind for ind, ele in enumerate(diflist[auxindex:maxrangeindex]) if ele == maxabs]
        maxlam = lamlist[auxindex + max(indices)]
        auxabs = (minabs-maxabs)/(minlam-maxlam)*(lamest-minlam)+minabs
        hvalue = diflist[auxindex]-auxabs

        max_list.append(hvalue)
                
        plt.plot(dic.get(ccc[ii])[0],dic.get(ccc[ii])[1]-fondo, label = ccc[ii])
        plt.plot([minlam,lamest,maxlam],[minabs,auxabs,maxabs],'o:', color = 'grey')
        plt.plot([lamest,lamest],[auxabs,diflist[auxindex]],'o:', color = 'grey')

    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), title = name)
    plt.fill_between([lam-dlam,lam+dlam],0,1.5*max(max_list), color = color2, alpha = 0.5)
    
    plt.xlabel('$\lambda$(nm)')
    plt.ylabel('absorbance')
    plt.xlim(lam-dlam-25,lam+dlam+25)

def get_single_dic(dic, fon, ccc, ind):
    auxdic = {}
    auxdic[ccc[ind]] = [dic.get(ccc[ind])[0], dic.get(ccc[ind])[1]]
    auxfon = {}
    auxfon[ccc[ind]] = [fon.get(ccc[ind])[0], fon.get(ccc[ind])[1]]
    auxccc = []
    auxccc.append(ccc[ind])

    return auxdic, auxfon, auxccc


# In[41]:


def get_dhb_peak_spectrum(dic, fon, ccc, lam, dlam, war = False):
    '''
    Find the height of the characteristic peaks for each REE.
    Characteristic peaks:
       lambda = 365 nm for Dy
       lambda = 444 nm for Pr
       lambda = 740 nm for Nd
    The local minima around each peak is searched within a window [lambda-delta, lambda+delta]
       delta = 15 nm for Dy
       delta = 27 nm for Pr
       delta = 50 nm for Nd
    If the local minima are equal to either window limit, a warning message is displayed using the war variable.
    '''
    RRE_list = ['Nd','Pr','Dy']
    max_list = []
    for ii in range(len(lam)):
        fondo = fon.get(ccc[0])[1]
        # auxlist = list(dic.get(ccc[ii])[0])
        lamlist = list(dic.get(ccc[0])[0])
        auxindex = lamlist.index(lam[ii])
        minrangeindex = lamlist.index(lam[ii]-dlam[ii])
        maxrangeindex = lamlist.index(lam[ii]+dlam[ii])
        
        diflist = list(dic.get(ccc[0])[1]-fondo)
        
        minabs = min(diflist[minrangeindex:auxindex])
        indices = [ind for ind, ele in enumerate(diflist[minrangeindex:auxindex]) if ele == minabs]
        minlam = lamlist[minrangeindex + max(indices)]
        if minlam == lam[ii]-dlam[ii]:
            print('-----------------------------------------')
            print(colored('WARNING!\tWARNING!\tWARNING!\tWARNING!','red',attrs = ['reverse','bold']))
            print(f'The minimum value to the left of the {RRE_list[ii]} peak is in the limit of the range of analysis.')
            print('Check the graphical output.')
            print('The analysis is not reliable.')
            print('Check the shape of the peaks in the spectrum... or talk to someone.\n')
            print('-----------------------------------------')
            war = True
        maxabs = min(diflist[auxindex:maxrangeindex])
        indices = [ind for ind, ele in enumerate(diflist[auxindex:maxrangeindex]) if ele == maxabs]
        maxlam = lamlist[auxindex + max(indices)]
        if maxlam == lam[ii]+dlam[ii]:
            print('-----------------------------------------')
            print(colored('WARNING!\tWARNING!\tWARNING!\tWARNING!','red',attrs = ['reverse','bold']))
            print(f'The minimum value to the right of the {RRE_list[ii]} peak is in the limit of the range of analysis.')
            print('Check the graphical output.')
            print('The analysis is not reliable.')
            print('Check the shape of the peaks in the spectrum... or talk to someone.\n')
            print('-----------------------------------------')
            war = True
        auxabs = (minabs-maxabs)/(minlam-maxlam)*(lam[ii]-minlam)+minabs
        hvalue = diflist[auxindex]-auxabs

        max_list.append(hvalue)

    return max_list, war

def plot_dhb_peak_spectrum(dic, fon, ccc, lam, dlam, path, name, conc):
    '''
    Plot the analyzed spectra.
    Vertical lines correspond to the analyzed characteristic peaks.
    Shaded rectangles around each peak correspond to the analysis window.
    '''
    con_Nd, err_con_Nd = conc.get('Nd')[0], conc.get('Nd')[1]
    con_Pr, err_con_Pr = conc.get('Pr')[0], conc.get('Pr')[1]
    con_Dy, err_con_Dy = conc.get('Dy')[0], conc.get('Dy')[1]
    max_list = []
    for ii in range(len(lam)):
        fondo = fon.get(ccc[0])[1]
        # auxlist = list(dic.get(ccc[ii])[0])
        lamlist = list(dic.get(ccc[0])[0])
        auxindex = lamlist.index(lam[ii])
        minrangeindex = lamlist.index(lam[ii]-dlam[ii])
        maxrangeindex = lamlist.index(lam[ii]+dlam[ii])
        
        diflist = list(dic.get(ccc[0])[1]-fondo)
        
        minabs = min(diflist[minrangeindex:auxindex])
        indices = [ind for ind, ele in enumerate(diflist[minrangeindex:auxindex]) if ele == minabs]
        minlam = lamlist[minrangeindex + max(indices)]
        maxabs = min(diflist[auxindex:maxrangeindex])
        indices = [ind for ind, ele in enumerate(diflist[auxindex:maxrangeindex]) if ele == maxabs]
        maxlam = lamlist[auxindex + max(indices)]
        auxabs = (minabs-maxabs)/(minlam-maxlam)*(lam[ii]-minlam)+minabs
        hvalue = diflist[auxindex]-auxabs

        max_list.append(hvalue)

        plt.plot([minlam,lam[ii],maxlam],[minabs,auxabs,maxabs],'o:', color = 'grey')
        plt.plot([lam[ii],lam[ii]],[auxabs,diflist[auxindex]],'o:', color = 'grey')
        
        if minlam == lam[ii]-dlam[ii] or maxlam == lam[ii]+dlam[ii]:
            plt.fill_between([lam[ii]-dlam[ii],lam[ii]+dlam[ii]],min(diflist),1.1*max(diflist), color = 'red', alpha = 0.5)
        else:
            plt.fill_between([lam[ii]-dlam[ii],lam[ii]+dlam[ii]],min(diflist),1.1*max(diflist), color = color2, alpha = 0.5)
        

    plt.plot(dic.get(ccc[0])[0],dic.get(ccc[0])[1]-fondo, label = ccc[0])
#    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), title = name)
    plt.title(name)
    
    textstr = '\n'.join(('Concentrations', f'Pr: {con_Pr}({err_con_Pr}) ppm', f'Nd: {con_Nd}({err_con_Nd}) ppm', f'Dy: {con_Dy}({err_con_Dy}) ppm'))
    plt.text(500, 1.1*max(diflist), textstr, fontsize=14, verticalalignment='top', bbox = dict(boxstyle='round', facecolor=color2, alpha=0.5))
    
    plt.xlabel('$\lambda$(nm)')
    plt.ylabel('absorbance')
    plt.xlim(300,900)

    plt.savefig(path + name + '_analysis.png', dpi = 300, format = 'png', bbox_inches = 'tight')
    plt.close()
    
    
def plot_spectra(dic, fon, ccc, lam, path, name):
    '''
    Plot the spectra to be analyzed.
    Vertical lines correspond to the analyzed characteristic peaks.
    '''

    plt.plot(dic.get(ccc[0])[0],dic.get(ccc[0])[1], color = color1, label = 'spectra')
    plt.plot(fon.get(ccc[0])[0],fon.get(ccc[0])[1], '--', color = color3, label = 'background')
    
    for ii in range(len(lam)):
        plt.plot([lam[ii],lam[ii]],[0,1.1*max(dic.get(ccc[0])[1])],':', color = 'grey')
    plt.text(lam[1]+10,max(dic.get(ccc[0])[1]), 'Pr')
    plt.text(lam[0]+10,max(dic.get(ccc[0])[1]), 'Nd')
    plt.text(lam[2]+10,max(dic.get(ccc[0])[1]), 'Dy')
    
    plt.title(name)
    plt.xlabel('$\lambda$(nm)')
    plt.ylabel('absorbance')
    plt.xlim(300,900)
    plt.ylim(0,1.15*max(dic.get(ccc[0])[1]))
    plt.legend(loc='upper center')
    plt.savefig(path + name + '_spectra.png', dpi = 300, format = 'png', bbox_inches = 'tight')
    plt.close()

print('Analysis functions loaded\n')


