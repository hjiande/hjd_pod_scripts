#!/usr/bin/python3
import gnsscal
import os

# form yyyy and doy get the time
def yyyydoy(iyear, idoy):
    date = gnsscal.yrdoy2date(iyear, idoy)
    (year, doy) = gnsscal.date2doy(date)
    return ('%04d%03d' % (year,doy))

# form gps week and week of day get the time
def gwkd2yyyydoy(gwk, gwd):
    (year, doy) = gnsscal.gpswd2yrdoy(gwk,gwd)
    return (year, doy)
    
def yyyy(iyear):
    return ('%04d' % int(iyear))
    
def yy(iyear):
    tmp = str('%04d' % int(iyear))
    return tmp[2:]

def mm(iyear, idoy):
    date_time = gnsscal.yrdoy2date(iyear, idoy)
    month =  date_time.month
    return ('%02d' % int(month))

def dd(iyear, idoy):
    date_time = gnsscal.yrdoy2date(iyear, idoy)
    day = date_time.day
    return ('%02d' % int(day) )
    
def gwkd(iyear, idoy):
    (week, day) = gnsscal.yrdoy2gpswd(iyear, idoy)
    return ('%04s' % week) + '%d' % int(day)  
    
def gwk(iyear, idoy):
    (week, day) = gnsscal.yrdoy2gpswd(iyear, idoy)
    return ('%04s' % week) 
    
def gwd(iyear, idoy):
    (week, day) = gnsscal.yrdoy2gpswd(iyear, idoy)
    return '%d' % int(day)  
        

    