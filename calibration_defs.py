#!/usr/bin/env python
# coding: utf-8

from math import log10, floor

#calibraciones

#defino una función que redondea a las cifras significativas de la incerteza
def round_error(x,dx):
    ret = round(x, -int(floor(log10(abs(dx)))))
    err_ret = round(dx, -int(floor(log10(abs(dx)))))
    if (err_ret >= 1):
        return int(ret), int(err_ret)
    else:
        return ret, err_ret

#calibración para Nd
def calib_Nd_H2O(dhval):
    pendiente = 22000
    error_pen = 1000
    ordenada = 30
    error_ord = 30
    con = pendiente*dhval + ordenada
    err_con = error_pen*dhval + error_ord
    concentracion, error_conc = round_error(con,err_con)
    return concentracion, error_conc

def calib_Nd_acetato(dhval):
    pendiente = 23000
    error_pen = 2000
    ordenada = 10
    error_ord = 50
    con = pendiente*dhval + ordenada
    err_con = error_pen*dhval + error_ord
    concentracion, error_conc = round_error(con,err_con)
    return concentracion, error_conc

#calibración para Pr
def calib_Pr_H2O(dhval):
    pendiente = 15250
    error_pen = 80
    ordenada = 6
    error_ord = 3
    con = pendiente*dhval + ordenada
    err_con = error_pen*dhval + error_ord
    concentracion, error_conc = round_error(con,err_con)
    return concentracion, error_conc

def calib_Pr_acetato(dhval):
    pendiente = 16900
    error_pen = 400
    ordenada = 10
    error_ord = 10
    con = pendiente*dhval + ordenada
    err_con = error_pen*dhval + error_ord
    concentracion, error_conc = round_error(con,err_con)
    return concentracion, error_conc

#calibración para Dy
def calib_Dy_H2O(dhval):
    pendiente = 84000
    error_pen = 500
    ordenada = 6
    error_ord = 3
    con = pendiente*dhval + ordenada
    err_con = error_pen*dhval + error_ord
    concentracion, error_conc = round_error(con,err_con)
    return concentracion, error_conc

def calib_Dy_acetato(dhval):
    pendiente = 87000
    error_pen = 1000
    ordenada = 14
    error_ord = 9
    con = pendiente*dhval + ordenada
    err_con = error_pen*dhval + error_ord
    concentracion, error_conc = round_error(con,err_con)
    return concentracion, error_conc


print('Calibrations loaded\n')

