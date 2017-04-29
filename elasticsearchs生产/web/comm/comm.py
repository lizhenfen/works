import time
import functools
import datetime
import calendar

def outer(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        start_time = time.time()
        res = func(*args,**kwargs)
        end_time = time.time()
        if isinstance(res,dict):
            res["time"] = '{:.2f}'.format(end_time-start_time)
        return res
    return inner

def getMonthFirstDayAndLastDay(year=None, month=None):
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year

    if month:
        month = int(month)
    else:
        month = datetime.date.today().month

    day  = datetime.date.today().day
    # 获取当月第一天的星期和当月的总天数
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)

    # 获取当月的第一天
    firstDay = datetime.date(year=year, month=month, day=1)
    today    = datetime.date(year=year, month=month, day=day)
    lastDay = datetime.date(year=year, month=month, day=monthRange)
    if lastDay > today:
        lastDay = today
    f = datetime.datetime.strftime(firstDay, "%Y/%m/%d")
    l = datetime.datetime.strftime(lastDay, "%Y/%m/%d")
    return (f,l)

if __name__ == "__main__":
    t = getMonthFirstDayAndLastDay()
    print(t)