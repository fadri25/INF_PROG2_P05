import os.path
import urllib.request as ur
import time
import pandas as pd
import timetransformations

"""Converts the seconds in a time and returns complete dataframe"""
class Data:
    def __init__(self, data):
        self.file_path = data
        
    def data(self):
        df = pd.read_csv(self.file_path)
        df_vor = timetransformations.Timestampconverter(df)
        df = df_vor.convert_dataframe()
        return(df)

"""Downloads the inserted data from the entry box"""
class Downloader:
    def __init__(self, url):
        self.url = url
        self.file_name = os.path.basename(url)  
         
    def download(self, timeout = 600000):
        try:
            if not os.path.isfile(self.file_name) or time.time() - os.stat(self.file_name).st_mtime > timeout:
                print(f"\nLoading data from url {self.url}. \n This may take a while if files are large.")
                ur.urlretrieve(self.url, self.file_name)
                file_path = os.path.abspath(self.file_name)
                return file_path
            else:
                print(f"Taking file {self.file_name} from cache.")
                file_path = os.path.abspath(self.file_name)
                return file_path        
                        
        except Exception as e:
            print(f'Error downloading file: {e}')

if __name__ == '__main__':
    pass
