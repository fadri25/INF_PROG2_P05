from datetime import datetime, timedelta, date
import requests

"""Calculates the timestamp of the departures and the resulting delay"""
class Timestampconverter:
    def __init__(self, df):
        self.df = df
        self.midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
    def seconds_to_time(self, seconds):
        if seconds > 86400: # Add one day because train departed after midnight
            days = seconds // 86400
            seconds %= 86400
            return self.midnight + timedelta(days=days) + timedelta(seconds=seconds)
        if seconds < 0: # If vaule is negative, train departed too early
            days = seconds // 86400
            seconds %= 86400
            return self.midnight - timedelta(days=days ) - timedelta(seconds=seconds)
        else: # If no condidion is true, simply return the timedelta
            return self.midnight + timedelta(seconds=seconds)
        
    """Adds the timestamps to the DataFrame"""
    def convert_dataframe(self):
        self.df['effective_soll'] = self.df['soll_ab_von'].apply(self.seconds_to_time)
        self.df['effective_ist'] = self.df['ist_ab_von'].apply(self.seconds_to_time)
        return self.df

"""Calculates the saturdays and sundays for the inserted weeks from the entrybox"""
class Timespan:
    def __init__(self, date_data):
        self.date = date_data
   
    def calculate_time(self):
        if self.date is not None:
            date_obj = datetime.strptime(self.date, f'%d.%m.%Y')
            sunday = date_obj - timedelta(days=date_obj.weekday() + 1)
            saturday = sunday + timedelta(days=6)
            formated_sunday = sunday.strftime(f'%Y%m%d')
            formated_saturday = saturday.strftime(f'%Y%m%d')
            try:
                response = requests.head(f"https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Fahrzeiten_SOLL_IST_{formated_sunday}_{formated_saturday}.csv")
                if response.status_code == 200: # Check if link is valid for the download
                    return formated_sunday, formated_saturday
            except requests.ConnectionError:
                return None

        else:
            today = date.today() # To handle errors better it just gets the date from today if no value is inserted
            date_obj = datetime.strftime(today, f"%d.%m.%Y")
            sunday = date_obj - timedelta(days=date_obj.weekday() + 1)
            saturday = sunday + timedelta(days=6)
            formated_sunday = sunday.strftime(f'%Y%m%d')
            formated_saturday = saturday.strftime(f'%Y%m%d')
            try:
                response = requests.head(f"https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Fahrzeiten_SOLL_IST_{formated_sunday}_{formated_saturday}.csv")
                if response.status_code == 200:
                    return formated_sunday, formated_saturday
                else:
                    return None
            except requests.ConnectionError:
                return None

if __name__ == '__main__':
    pass
