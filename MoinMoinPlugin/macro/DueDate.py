import time

############################################################################
lboundyear = 1881
uboundyear = 2050
sunlunar_data = ("1212122322121", "1212121221220", "1121121222120", #1881
                 "2112132122122", "2112112121220", "2121211212120",
                 "2212321121212", "2122121121210", "2122121212120",
                 "1232122121212", "1212121221220", "1121123221222", #1890
                 "1121121212220", "1212112121220", "2121231212121",
                 "2221211212120", "1221212121210", "2123221212121",
                 "2121212212120", "1211212232212", "1211212122210",
                 "2121121212220", "1212132112212", "2212112112210",
                 "2212211212120", "1221412121212", "1212122121210",
                 "2112212122120", "1231212122212", "1211212122210",
                 "2121123122122", "2121121122120", "2212112112120",
                 "2212231212112", "2122121212120", "1212122121210",
                 "2132122122121", "2112121222120", "1211212322122",
                 "1211211221220", "2121121121220", "2122132112122", #1920
                 "1221212121120", "2121221212110", "2122321221212",
                 "1121212212210", "2112121221220", "1231211221222",
                 "1211211212220", "1221123121221", "2221121121210",
                 "2221212112120", "1221241212112", "1212212212120",
                 "1121212212210", "2114121212221", "2112112122210",
                 "2211211412212", "2211211212120", "2212121121210",
                 "2212214112121", "2122122121120", "1212122122120",
                 "1121412122122", "1121121222120", "2112112122120",
                 "2231211212122", "2121211212120", "2212121321212",
                 "2122121121210", "2122121212120", "1212142121212", #1950
                 "1211221221220", "1121121221220", "2114112121222",
                 "1212112121220", "2121211232122", "1221211212120",
                 "1221212121210", "2121223212121", "2121212212120",
                 "1211212212210", "2121321212221", "2121121212220",
                 "1212112112210", "2223211211221", "2212211212120",
                 "1221212321212", "1212122121210", "2112212122120",
                 "1211232122212", "1211212122210", "2121121122210",
                 "2212312112212", "2212112112120", "2212121232112",
                 "2122121212110", "2212122121210", "2112124122121",
                 "2112121221220", "1211211221220", "2121321122122", #1980
                 "2121121121220", "2122112112322", "1221212112120",
                 "1221221212110", "2122123221212", "1121212212210",
                 "2112121221220", "1211231212222", "1211211212220",
                 "1221121121220", "1223212112121", "2221212112120",
                 "1221221232112", "1212212122120", "1121212212210",
                 "2112132212221", "2112112122210", "2211211212210",
                 "2221321121212", "2212121121210", "2212212112120",
                 "1232212121212", "1212122122120", "1121212322122", #2004
                 "1121121222120", "2112112122120", "2211231212122",
                 "2121211212120", "2122121121210", "2124212112121", #2010
                 "2122121212120", "1212121223212", "1211212221220",
                 "1121121221220", "2112132121222", "1212112121220",
                 "2121211212120", "2122321121212", "1221212121210",
                 "2121221212120", "1232121221212", "1211212212210",
                 "2121123212221", "2121121212220", "1212112112220",
                 "1221231211221", "2212211211220", "1212212121210",
                 "2123212212121", "2112122122120", "1211212322212",
                 "1211212122210", "2121121122120", "2212114112122",
                 "2212112112120", "2212121211210", "2212232121211",
                 "2122122121210", "2112122122120", "1231212122212", #2040
                 "1211211221220", "2121121321222", "2121121121220",
                 "2122112112120", "2122141211212", "1221221212110",
                 "2121221221210", "2114121221221")                  #2049

class DateError(Exception):
    pass

def lun2sol(lyyyy, lmm, ldd, yundal=0):

    lday = [31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if (lyyyy <= lboundyear) or (lyyyy >= uboundyear):
        raise DateError
    if lmm > 12 or lmm < 1 or ldd < 1:
        raise DateError

    pyear = lyyyy - lboundyear;
    if sunlunar_data[pyear][12] == "0":
        if yundal == 1:
            raise DateError
        if int(sunlunar_data[pyear][lmm-1]) + 28 < ldd:
            raise DateError
    else:
        if yundal == 1:
            if sunlunar_data[pyear][lmm] <= "2":
                raise DateError
            if int(sunlunar_data[pyear][lmm]) + 26 < ldd:
                raise DateError
        else:
            after_yundal = 0
            for i in range(lmm):
                if sunlunar_data[pyear][i] > "2":
                    after_yundal = 1
                    break
            if int(sunlunar_data[pyear][lmm-1+after_yundal]) + 28 < ldd:
                raise DateError

    pyear = 0;
    total_date = 0;

    if (lyyyy > lboundyear) and (lyyyy < uboundyear):
        pyear = lyyyy - lboundyear;
        for i in range(pyear):
            for j in range(13):
                total_date = total_date + int(sunlunar_data[i][j])
            if sunlunar_data[i][12] == "0":
                total_date = total_date + 336
            else:
                total_date = total_date + 362
    else:
        gf_lun2sol = 0

    pmonth = lmm - 1;
    m2 = -1;

    while 1:
        m2 = m2 + 1
        if sunlunar_data[pyear][m2] > "2":
            total_date = total_date + 26 + int(sunlunar_data[pyear][m2])
            pmonth = pmonth + 1
        else:
            if m2 == pmonth:
                if yundal:
                    total_date = total_date + 28 + int(sunlunar_data[pyear][m2])
                break
            else:
                total_date = total_date + 28 + int(sunlunar_data[pyear][m2])
    total_date = total_date + ldd + 29

    m1 = 1880

    while 1:
        m1 = m1 + 1
        if ((m1 % 400) == 0) or ((m1 % 100) != 0) and ((m1 % 4) == 0):
            leap = 1
        else:
            leap = 0

        if leap == 1:
            m2 = 366
        else:
            m2 = 365

        if total_date < m2: break
        total_date = total_date - m2

    syyyy = m1
    lday[1] = m2 - 337

    m1 = 0

    while 1:
        m1 = m1 + 1
        if total_date <= lday[m1-1]:
            break
        total_date = total_date - lday[m1-1]

    smm = m1
    sdd = total_date
    gf_lun2sol = 1

    return (syyyy, smm, sdd)


def sol2lun(syyyy, smm, sdd):

    lday = [31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    dayinyear = []
    for i in range(len(sunlunar_data)):
        dayinyear.append(0)
        for j in range(13):
            t = sunlunar_data[i][j]
            if t == "1" or t == "3":
                dayinyear[i] = dayinyear[i] + 29
            elif t == "2" or t == "4":
                dayinyear[i] = dayinyear[i] + 30

    lyear = lboundyear - 1
    td1 = lyear * 365 + int(lyear/4) - int(lyear/100) + int(lyear/400) + 30
    k11 = syyyy - 1
    td2 = k11 * 365 + int(k11/4) - int(k11/100) + int(k11/400)
    if (syyyy % 400 == 0) or (syyyy % 100 != 0) and (syyyy % 4 == 0):
        lday[1] = 29
    else:
        lday[1] = 28

    if smm > 13:
        raise DateError
    if sdd > lday[smm-1]:
        raise DateError

    for i in range(smm-1):
        td2 = td2 + lday[i]

    td2 = td2 + sdd
    td = td2 - td1 + 1
    td0 = dayinyear[0]

    for i in range(len(sunlunar_data)-1):
        if td <= td0:
            break
        td0 = td0 + dayinyear[i+1]

    lyyyy = i + lboundyear
    td0 = td0 - dayinyear[i]
    td = td - td0

    if sunlunar_data[i][12] == "0":
        jcount = 11
    else:
        jcount = 12
    lmm = 0

    for j in range(jcount+1):
        if sunlunar_data[i][j] <= "2":
            lmm = lmm + 1
            m1 = int(sunlunar_data[i][j]) + 28
            yundal = 0
        else:
            m1 = int(sunlunar_data[i][j]) + 26
            yundal = 1
        if td <= m1:
            break
        td = td - m1

    ldd = td
    return (lyyyy, lmm, ldd, yundal)
#############################################################################


def getFullTimeLuna(aText,aTime):
    year,month,day=aTime[0],aTime[1],aTime[2]
    if len(aText)==2:
        if aText<"%02d"%day:
            month+=1
        if month>12:
            year,month=year+1,1
        aText="%04d%02d"%(year,month)+aText
    elif len(aText)==4:
        if aText<"%02d%02d"%(month,day):
            year+=1
        aText="%04d"%year+aText
    return time.strptime(aText,"%Y%m%d")

def getFullTime(aText,aTime):
    year,month,day=aTime[0],aTime[1],aTime[2]
    if len(aText)==2:
        if aText<"%02d"%day:
            month+=1
        if month>12:
            year,month=year+1,1
        aText="%04d%02d"%(year,month)+aText
    elif len(aText)==4:
        if aText<"%02d%02d"%(month,day):
            year+=1
        aText="%04d"%year+aText
    return time.strptime(aText,"%Y%m%d")

def execute(macro, text, args=""):
    convertLuna = False
    args = text.split(',')

    if len(args) == 1:
        text = args[0]
    elif len(args) == 2:
        text = args[0]
        convertLuna = (args[1].lower() == "true")
    else:
        return u"<b>invalid argument count</b>"

    localtime = time.localtime()
    localtime = localtime[0],localtime[1],localtime[2],0,0,0,0,0,0

    if len(text) not in [2,4,8]: return u"<b>invalid date length</b>"

    if convertLuna:
        #?????? ??????
        today_luna = sol2lun(localtime[0],localtime[1],localtime[2])
        today_luna = today_luna[0],today_luna[1],today_luna[2],0,0,0,0,0,0
        ddayTuple=getFullTime(text,today_luna)
        ddayTuple = lun2sol(ddayTuple[0], ddayTuple[1], ddayTuple[2])
        ddayTuple = ddayTuple[0],ddayTuple[1],ddayTuple[2],0,0,0,0,0,0
    else:
        ddayTuple=getFullTime(text,localtime)

    timeDiff=(time.mktime(ddayTuple)-time.mktime(localtime))/86400
    date=time.strftime("(%Y/%m/%d) ",ddayTuple)
    if timeDiff >0:
        msg = u'%d days remain until %s' % (timeDiff, date)
    elif timeDiff == 0 :
        msg = u'%s is TODAY' % date
    else:
        msg = u'%d days elapsed from %s' % (abs(timeDiff), date)
    return msg