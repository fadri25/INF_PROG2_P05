
#################################################################################
#   Autoren: Sarah, Kristina, Fadri
#   Erstellungsdatum: 27.04.2023
#   Beschreibung: INF_PROG2_P05
#   Version: 1.4 (GVC)
#   Letze Änderung: 08.05.2023
#################################################################################

#(B) Report on the top 10 of most unreliable stops. Where should you never wait for your 
#transportation?
# Sollabfahrt von (technisch: soll_ab_von)
# Istabfahrt von (technisch: ist_ab_von)
# Namen geben --> RailFlow?

# -------Aufgaben
# Visualisieren probieren -> Fadri -> Visualisierung schöner
# Kristina -> code verstehen
# Vielleicht noch 

import pandas as pd
from datetime import datetime, timedelta
import os
import time
import os.path
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import filedialog
from PIL import ImageTk, Image
import urllib.request as ur
import matplotlib.pyplot as plt # pip instal matplotlib


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
        results = []
        for stop in stops:
            stop_data = self.data[self.data['halt_diva_von'] == stop] # Daten für diese Haltestelle filtern
            delay = (stop_data['effective_soll'] - stop_data['effective_ist']).mean().total_seconds() #// 60 # Delay in Sekunden (mit // 60 in Minuten) mit berechnung von datetime-Objekten
            delay_stop[stop] = delay # speichern der berechneten verspätung

        sorted_delays = sorted(delay_stop.items(), key=lambda x: x[1], reverse=True) # sortieren der Haltestellen nach Verspätung (absteigend)
        unreliable_stops = sorted_delays 
        df_haltestellen = pd.read_csv("Haltestelle.csv")
        
        for stop, delay in unreliable_stops:
            matching_row = df_haltestellen.loc[df_haltestellen['halt_diva'] == stop] #filtern wo stimmen zahlen überein
            if not matching_row.empty:
                stop = matching_row['halt_lang'].values[0]  #values damit es name anzeigt und nicht spalte aus matching row
                results.append({'stop': stop, 'delay': delay})
        
        top_unreliable_stops = sorted_delays[:10] # Top ten für ausgabe
        for stop, delay in top_unreliable_stops:
            matching_row = df_haltestellen.loc[df_haltestellen['halt_diva'] == stop] #filtern wo stimmen zahlen überein
            if not matching_row.empty:
                stop = matching_row['halt_lang'].values[0]  #values damit es name anzeigt und nicht spalte aus matching row
                print(f'{stop}: average delay of {delay:.2f} seconds.')
        
        return pd.DataFrame(results)               
        
class Visualization(tk.Frame):
    def __init__(self, dataframe=None, title=''):
        #super().__init__()
        self.root = tk.Tk()
        self.root.dataframe = dataframe
        self.root.title = title
        #self.create_widgets()
        self.create_button_close()
        self.create_button_barplot()
        self.create_button_lineplot()
        self.root.mainloop()
    
    def create_widgets(self):
        title_label = tk.Label(self.root, text=self.root.title)
        title_label.pack(side="top", fill="x", pady=10)

        treeview = tk.ttk.Treeview(self.root, columns=list(self.root.dataframe.columns), show='headings')
        for col in list(self.root.dataframe.columns):
            treeview.heading(col, text=col)
        for index, row in self.root.dataframe.iterrows():
            treeview.insert("", tk.END, values=list(row))
        treeview.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=treeview.yview)
        scrollbar.pack(side="right", fill="y")
        treeview.configure(yscrollcommand=scrollbar.set)

    
    def create_button_barplot(self):
        title_button = tk.Button(self.root, text="Balekndiagramm")
        title_button.pack(side="bottom", fill="x", pady=10)
    
    def create_button_lineplot(self):
        title_button = tk.Button(self.root, text="Verspätungen")
        title_button.pack(side="bottom", fill="x", pady=10)
        
    def create_button_close(self):
        title_button = tk.Button(self.root, text="Schliessen", command=self.close)
        title_button.pack(side="bottom", pady=10)
    
    def close(self):
        self.root.destroy()
"""

class App:
    def __init__(self, root):
        root.title("VBZ Delays")
        width=500
        height=200
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        b_delay=tk.Button(root)
        b_delay["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        b_delay["font"] = ft
        b_delay["fg"] = "#000000"
        b_delay["justify"] = "center"
        b_delay["text"] = "Verspätungen"
        b_delay.place(x=30,y=150,width=103,height=30)
        b_delay["command"] = self.b_delay_command

        b_bar=tk.Button(root)
        b_bar["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        b_bar["font"] = ft
        b_bar["fg"] = "#000000"
        b_bar["justify"] = "center"
        b_bar["text"] = "Balkendiagramm"
        b_bar.place(x=200,y=150,width=104,height=30)
        b_bar["command"] = self.b_bar_command

        b_close=tk.Button(root)
        b_close["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        b_close["font"] = ft
        b_close["fg"] = "#000000"
        b_close["justify"] = "center"
        b_close["text"] = "Schliessen"
        b_close.place(x=360,y=150,width=103,height=30)
        b_close["command"] = self.b_close_command

        l_background=tk.Label(root)
        l_background.place(x=0,y=0,width=501,height=195)
        ft = tkFont.Font(family='Times',size=10)
        l_background["font"] = ft
        l_background["fg"] = "#333333"
        l_background["justify"] = "center"
        l_background["text"] = "label"
        l_background.place(x=0,y=0,width=501,height=195)
        
        l_delay=tk.Label(root)
        ft = tkFont.Font(family='Times',size=23)
        l_delay["font"] = ft
        l_delay["fg"] = "#333333"
        l_delay["justify"] = "center"
        l_delay["text"] = "VBZ Verspätungen"
        l_delay.place(x=100,y=20,width=321,height=30)

    def b_delay_command(self):
        print("command")


    def b_bar_command(self):
        print("command")


    def b_close_command(self):
        self.root.destroy()
"""

# Neue Berechnungen für Plots integrieren
# Barplot für die ersten zehn -> funktioniert noch nicht
class Barplot:
    def __init__(self, dataframe) -> None:
        self.df = dataframe
    
    def create_barplot():
        #var = dataframe.grouby('###').###.sum()
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.set_xlabel('Funktion')
        ax.set_ylabel('Umsatz in Summe')
        ax.set_title('Umsatzvolumen nach Funktion der Filialen')
        #var.plot(kind='bar')
        plt.show()
        
# Lineplot soll für jede Station gemacht werden können per Knopf oder suche? -> funktioniert noch nicht  
class Lineplot:
    def __init__(self, dataframe):
        self.df = dataframe
    
    def create_lineplot(self):
        var = dataframe.groupby('Standort').Umsatz.sum()
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        ax1.set_xlabel('Umsatz')
        ax1.set_ylabel('Standort')
        var.plot(kind='line')
        plt.show()


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
    df = calculator.calculate()
    
    # Data vizualisation
    #root = tk.Tk()
    #app = App(root)
    #root.mainloop()
    #df_visualizer = Visualization(dataframe=df, title='RailFlow')
    #df_visualizer.pack(fill="both", expand=True)