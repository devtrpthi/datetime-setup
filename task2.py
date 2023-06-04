import datetime
import pytz

class DateUtility:
    def __init__(self,holiday_file):
        self.holidays = self.load_holidays(holiday_file)

    def load_holidays(self,holiday_file):
        holidays={}
        with open(holiday_file) as f:
            for line in f:
                file_timezone,file_date, file_holiday = line.strip().split(',')
                date= datetime.datetime.strptime(file_date, '%Y%m%d').date()
                if file_timezone not in holidays:
                    holidays[file_timezone] = {}
                holidays[file_timezone][date] = file_holiday
        return holidays
    
    def dt_conversion(self,from_date,tz_old,tz_new):
        from_tz = pytz.timezone(tz_old)
        to_tz = pytz.timezone(tz_new)
        from_date = from_tz.localize(from_date)
        new_date = from_date.astimezone(to_tz)
        return new_date

    def date_add(self,from_date,no_of_days):
        new_date = from_date + datetime.timedelta(days=no_of_days)
        return new_date

    def date_subtract(self,from_date,no_of_days):
        new_date = from_date - datetime.timedelta(days=no_of_days)
        return new_date

    def date_diff(self,from_date,to_date):
        difference = to_date - from_date
        return difference.days

    def non_weekend(self,from_date,to_date):
        day_diff = to_date.weekday() - from_date.weekday()
        non_week_days = ((to_date-from_date).days - day_diff) / 7 * 5 + min(day_diff,5) - (max(to_date.weekday() - 4, 0) % 5)
        return non_week_days

    def days_since_epoch(self,from_date):
        epoch_date = datetime.datetime.utcfromtimestamp(0)
        difference = from_date - epoch_date
        return difference.days

    def business_days(self,from_date,to_date):
        holidays = self.holidays.get(from_date.tzinfo.zone, {})
        business_days = 0
        current_date= from_date
        while current_date <= to_date:
            if current_date.weekday() < 5 and current_date.date() not in holidays:
                business_days +=1
                current_date +=datetime.timedelta(days=1)
            return business_days


utility = DateUtility('holidays.dat')

now = datetime.datetime.now() 
from_date = now.strftime('%Y/%m/%d %H:%M:%S')
new_date = utility.dt_conversion(from_date,'UTC','US/Eastern')
print(new_date)

given_days = int(input('Enter the number of days to be added or subtracted:'))
new_date = utility.date_add(from_date,given_days)
print(new_date)

given_datetime = str(input('Enter a valid date and time:'))
to_date = datetime.datetime.strptime(given_datetime, '%Y/%m/%d %H:%M:%S')
difference = utility.date_diff(from_date, to_date)
print(difference)

days_exclude = utility.non_weekend(from_date, to_date)
print(days_exclude)

since_epoch = utility.days_since_epoch(from_date)
print(since_epoch)

days_of_business = utility.business_days(from_date, to_date)  
print(days_of_business)
