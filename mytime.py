from datetime import datetime, timedelta, timezone

# Create a timezone object for UTC-6 (Central Standard Time)
tz_utc_minus_6 = timezone(timedelta(hours=-6))

def GetNowTimeHour():
    return datetime.now(tz=tz_utc_minus_6).hour

def GetNowTime():
    return datetime.now(tz=tz_utc_minus_6)

def GetFormattedNowTime():
    return datetime.now(tz=tz_utc_minus_6).strftime('%Y-%m-%d %H:%M:%S')

def GetTimeStamp():
    return int(datetime.now(tz=tz_utc_minus_6).timestamp())

def TimeStampToString(timestamp):
    return datetime.fromtimestamp(timestamp, tz=tz_utc_minus_6)

def GetNowTimeFileName():
    return datetime.now(tz=tz_utc_minus_6).strftime('%Y/%m/%d.log')
