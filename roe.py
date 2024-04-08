import baostock as bs
import pandas as pd
import datetime
import numpy as np
import time

from allstocks import getAllstocks

#np.seterr(invalid='ignore')
lg = bs.login()
datalist = []


#获取roe变异系数
def getCV(arr):
    cv = 0
    try:
        cv = np.std(arr, ddof=1)/np.mean(arr)
    except:
        pass
    return cv

#获取净利润增长率
def getYOYNI(code, year=2015,quarter=1):
    rs = bs.query_growth_data(code, year, quarter)
    re = 0
    try:
        re = rs.get_row_data()[5]
        re = round(float(re), 2)
    except:
        pass
    return re

#上市时间函数
def compare(time1,time2,days=365):
    d1 = datetime.datetime.strptime(time1, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(time2, '%Y-%m-%d')
    delta = d1 - d2
    # print(delta)
    if delta.days > days:
        return True
    else:
        return False
def getROE(code="SH.603998", year=2015):
    rs_dupont = bs.query_dupont_data(code=code, year=year, quarter=4)
    re = 0
    try:
        re = rs_dupont.get_row_data()[3]
        re = round(float(re) * 100, 2)
    except:
        pass

    return re

def getName(code):
    rs = bs.query_stock_basic(code)
    return rs.get_row_data()[1]

#获取上市时间
def getIPO(code):
    re = 0
    try:
        rs = bs.query_stock_basic(code)
        re = rs.get_row_data()[2]
    except:
        pass

    return re

#获取所属分类
def getIndustry(code):
    rs = bs.query_stock_industry(code)
    return rs.get_row_data()[3]

def getClosePrise(code):
    rs = bs.query_history_k_data_plus(code, "close")
    re = rs.get_row_data()[0]
    re = round(float(re), 2)
    return re

#加工组合
def Combine(code):
    time.sleep(0.1)
    tmp = []
    roe2015 = getROE(code, 2015)
    roe2016 = getROE(code, 2016)
    roe2017 = getROE(code, 2017)
    roe2018 = getROE(code, 2018)
    roe2019 = getROE(code, 2019)

    time1 = "2015-05-01"
    time2 = getIPO(code)
    YOYNI = getYOYNI(code)
    cv = getCV([roe2015, roe2016, roe2017, roe2018, roe2019])
    try:
         if roe2015>0.05 and roe2016>0.05 and roe2017>0.05 and roe2018>0.05 and roe2019>0.05 and compare(time1, time2, 365*6) and  YOYNI>-1 and cv >0 and cv<0.4:
            tmp.append(code)
            tmp.append(getName(code))
            tmp.append(getClosePrise(code))
            tmp.append(getIndustry(code))
            tmp.append(YOYNI)
            tmp.append(roe2015)  # 结果excel中首先年份roe可人工过滤为>10
            tmp.append(roe2016)  # 结果excel中首先年份roe可人工过滤为>10
            tmp.append(roe2017)  # 结果excel中首先年份roe可人工过滤为>10
            tmp.append(roe2018)  # 结果excel中首先年份roe可人工过滤为>10
            tmp.append(roe2019)  # 结果excel中首先年份roe可人工过滤为>10
            tmp.append(cv)       # 结果excel中其次CV可人工过滤为<0.3
            tmp.append(time2)
         else:
            print(str(code) + " not valid and had passed")
    except:
        print(roe2015)
        print(roe2016)
        print(roe2017)
        print(roe2018)
        print(roe2019)
        pass
    return tmp

def main():
    for s in getAllstocks():
        re = Combine(s)
        if re:
            print(re)
            datalist.append(re)

    result = pd.DataFrame(datalist)
    result.to_csv("C:\\test/test-money\\baostock-0.8.8\\select_gupiao\\gupiaohebing.csv", encoding="gbk", index=False)

#re = Combine("sz.002605")
#print(re)
main()



bs.logout()
