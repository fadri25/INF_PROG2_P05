#################################################################################
#   Autoren: Sarah, Kristina, Fadri
#   Erstellungsdatum: 27.04.2023
#   Beschreibung: INF_PROG2_P05
#   Version: 1.4 (GVC)
#   Letze Änderung: 05.05.2023
#################################################################################

#(B) Report on the top 10 of most unreliable stops. Where should you never wait for your 
#transportation?
# Sollabfahrt von (technisch: soll_ab_von)
# Istabfahrt von (technisch: ist_ab_von)
# Namen geben --> RailFlow?

import pandas as pd
from datetime import datetime, timedelta
import os
import time
import requests
import os.path
import tkinter as tk
from tkinter import messagebox
#import tensorflow as tf?

class TimestampConverter:
    def __init__(self, df):
        self.df = df # Dataframe einlesen in class
        self.midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) # Mitternacht im Zeitformat generieren
        
    def seconds_to_time(self, seconds):
        return self.midnight + timedelta(seconds=seconds) # Umrechnung Sekunden in Zeit
        
    def convert_dataframe(self):
        self.df['effective_soll'] = self.df['soll_ab_von'].apply(self.seconds_to_time) # Zeile hinzufügen mit Uhrzeit
        self.df['effective_ist'] = self.df['ist_ab_von'].apply(self.seconds_to_time) # ''
        return self.df # Ausgabe neues dataframe

class Data:
    def __init__(self, data):
        self.file_path = data # Daten einlesen
    
    def data(self):
        df = pd.read_csv(self.file_path) # Daten in Dataframe verpacken
        df_vor = TimestampConverter(df) # daten in classe Timestampconverter einlesen
        df = df_vor.convert_dataframe() # Umrechnung --> siehe class Timestampconverter
        return(df) # Ausgabe neues dataframe für berechnungen

class Calculator:
    def __init__(self, data):
        self.data = data # Einlesen Daten
        
    def calculate(self):
        stops = self.data['halt_diva_von'].unique() # Liste aller Haltestellen
        delay_stop = {}
        for stop in stops:
            stop_data = self.data[self.data['halt_diva_von'] == stop] # Daten für diese Haltestelle filtern
            delay = (stop_data['effective_soll'] - stop_data['effective_ist']).mean().total_seconds() #// 60 # Delay in Sekunden (mit // 60 in Minuten) mit berechnung von datetime-Objekten
            delay_stop[stop] = delay # speichern der berechneten verspätung

        sorted_delays = sorted(delay_stop.items(), key=lambda x: x[1], reverse=True) # sortieren der Haltestellen nach Verspätung (absteigend)
        #for stop, delay in sorted_delays:
            #print(f'Stop {stop} average delay {delay:.2f} seconds')
        #time.sleep(10)
        top_unreliable_stops = sorted_delays[:10] # Die ersten zehn haltestellen bekommen
        for stop, delay in top_unreliable_stops: # Für die ersten zehn
            print(f'Stop {stop}: average delay of {delay:.2f} seconds.') # Ausgabe
        #show = Visualization(delay_stop)
        #app = Visualization()
        #app.mainloop()
        
        # Tabelle mit verzögerungen ausgeben --> Ausgegeben!! ziehe z. 60-63
        
class Visualization(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Railflow')
        self.geometry('300x50')

        self.label = tk.Label(self, text='Test label')
        self.label.pack()
        
        self.button = tk.Button(self, text='Button')
        self.button['command'] = self.button_clicked
        self.button.pack()
    
    def button_clicked(self):
        messagebox.showinfo(title='Information', message='Hello TKINTER!!!')
        
    def structure_data(self):  
        pass
    
    def show(self):
        pass

class Downloader: # Downloader selbsterklärend vgl. P04?
    def __init__(self, url):
        self.url = url 
        self.file_path = "daten.csv"
        
    def download(self, timeout=60000):
        try:
            file_age = time.time() - os.path.getmtime(self.file_path)
            if file_age < timeout:
                print(f'Using cached file: {self.file_path}')
                print(self.file_path)
                return self.file_path
            
            response = requests.get(self.url)
            print("hier geprinted", self.file_path)
            with open(self.file_path, 'wb') as f:
                f.write(response.content)
            print(f'Downloaded file: {self.file_path}')
            return self.file_path
        except Exception as e:
            print(f'Error downloading file: {e}')
    # Daten speichern

if __name__ == '__main__':
    # Alle variablen die man braucht
    url = 'https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Fahrzeiten_SOLL_IST_20230319_20230325.csv'
    downloader = Downloader(url)
    data = downloader.download()
    
    data_path = Data(data)
    dataframe = data_path.data()
    calculator = Calculator(dataframe)
    calculator.calculate()