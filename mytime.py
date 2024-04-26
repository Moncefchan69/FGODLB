from croniter import croniter
from datetime import datetime, timedelta, timezone

tz_utc_-6 = timezone(timedelta(hours=-6))


def GetNowTimeHour():
    return datetime.now(tz=tz_utc_-6).hour


def GetNowTime():
    return datetime.now(tz=tz_utc_-6)


def GetFormattedNowTime():
    return datetime.now(tz=tz_utc_-6).strftime('%Y-%m-%d %H:%M:%S')


def GetTimeStamp():
    return (int)(datetime.now(tz=tz_utc_8).timestamp())


def TimeStampToString(timestamp):
    return datetime.fromtimestamp(timestamp)


def GetNowTimeFileName():
    return datetime.now(tz=tz_utc_-6).strftime('%Y/%m/%d.log')
