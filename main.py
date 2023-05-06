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

# -------Aufgaben
# Filepath nicht mitgegeben sondern caching -> Sarah -> DONE
# Visualisieren probieren -> Fadri
# Kristina -> code verstehen

import pandas as pd
from datetime import datetime, timedelta
import os
import time
import requests
import os.path
import tkinter as tk
from tkinter import messagebox
import urllib.request as ur
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
        df_haltestellen = pd.read_csv("Haltestelle.csv")
        
        for stop, delay in top_unreliable_stops: # Für die ersten zehn
            matching_row = df_haltestellen.loc[df_haltestellen['halt_diva'] == stop] #filtern nach wo stimmen zahlen überein
            if not matching_row.empty:
                stop = matching_row['halt_lang'].values[0]  #values damit es name anzeigt und nicht spalte aus matching row
                print(f'{stop}: average delay of {delay:.2f} seconds.')

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

class Downloader: # Downloader vgl. P04
    def __init__(self, url):
        self.url = url 
        self.file_name = os.path.basename(url) #definiert den Namen des Dokuments so wie die url basis
    
    def download(self, timeout = 60000):
        #wenn es nicht im cache ist oder mehr als 60000 Sekunden (10 Stunden) her ist-> daten neu holen
        try: 
            if not os.path.isfile(self.file_name) or time.time() - os.stat(self.file_name).st_mtime > timeout:
                print(f"\nLoading data from url {self.url}")
                filename = os.path.basename(self.url)
                ur.urlretrieve(self.url, self.file_name)                
            else:
                #datei wird aus cache geladen, read only
                #f = open(self.file_name, 'r')
                print(f"Taking file {self.file_name} from cache.")                    

        except Exception as e:
            print(f'Error downloading file: {e}')
        
        file_path = os.path.abspath(self.file_name) #absoluter pfad vom cache file
        return file_path        
    
if __name__ == '__main__':
    # Alle variablen die man braucht

    #downloaden des datensets
    url = 'https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Fahrzeiten_SOLL_IST_20230319_20230325.csv'
    downloader = Downloader(url)
    data = downloader.download()

    #downloaden de datensets Haltestellen
    url_haltestelle = "https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Haltestelle.csv"
    haltestellen_downlaoder = Downloader(url_haltestelle)
    haltestelle_data = haltestellen_downlaoder.download()

    #aufrufen der Klassen und Methoden zum auswerten
    data_path = Data(data)
    dataframe = data_path.data()
    calculator = Calculator(dataframe)
    calculator.calculate()