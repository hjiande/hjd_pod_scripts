import os
import timeLib as tl


def norm(name, year, doy):
    if doy < 1:
        year = int(year) - 1
        doy = int(doy) + 365
    tmp = name
    tmp = norm_GWKD(tmp, year, doy)
    tmp = norm_GWKDYY(tmp, year, doy)
    tmp = norm_YYYYDDD(tmp, year, doy)
    tmp = norm_YYMM(tmp, year, doy)
    return tmp


def norm_YYYYDDD(name, year, doy):
    if doy < 1:
        year = int(year) - 1
        doy = int(doy) + 365
    tmp = name
    tmp = tmp.replace('-YYYY-', '%04s' % str(year))
    tmp = tmp.replace('-DDD-', '%03d' % int(doy))
    tmp = tmp.replace('-YY-', ('%04s' % str(year))[2:])
    return tmp


def norm_GWKD(name, year, doy):
    if doy < 1:
        year = int(year) - 1
        doy = int(doy) + 365
    WWWWD = tl.gwkd(year, doy)
    WWWW = tl.gwk(year, doy)
    D = WWWWD[4:]
    tmp = name
    tmp = tmp.replace('-GWKD-', '%05s' % str(WWWWD))
    tmp = tmp.replace('-GWK-', '%04s' % str(WWWW))
    tmp = tmp.replace('-D-', '%01s' % str(D))
    return tmp


def norm_GWKDYY(name, iyear, idoy):
    if idoy < 1:
        year = int(iyear) - 1
        doy = int(idoy) + 365
    else:
        year = iyear
        doy = idoy
    wwwwd = tl.gwkd(year, doy)
    tmp = name
    tmp = tmp.replace('-GWKD-', '%04s' % str(wwwwd))
    tmp = tmp.replace('-YY-', '%02s' % str(year)[2:])
    return tmp


def norm_YYMM(name, iyear, idoy):
    if idoy < 1:
        year = int(iyear) - 1
        doy = int(idoy) + 365
    else:
        year = iyear
        doy = idoy
    mm = tl.mm(year, doy)
    yy = tl.yy(iyear)
    tmp = name
    tmp = tmp.replace('-MM-', '%02s' % str(mm))
    tmp = tmp.replace('-YY-', '%02s' % str(yy))
    return tmp
