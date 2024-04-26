from datetime import datetime, timedelta, timezone
tz="America/Mexico_City"


def GetNowTimeHour():
    return datetime.now(tz=America/Mexico_City).hour


def GetNowTime():
    return datetime.now(tz=America/Mexico_City)


def GetFormattedNowTime():
    return datetime.now(tz=America/Mexico_City).strftime('%Y-%m-%d %H:%M:%S')


def GetTimeStamp():
    return (int)(datetime.now(tz=America/Mexico_City).timestamp())


def TimeStampToString(timestamp):
    return datetime.fromtimestamp(timestamp)


def GetNowTimeFileName():
    return datetime.now(tz=America/Mexico_City).strftime('%Y/%m/%d.log')
