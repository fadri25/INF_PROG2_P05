#################################################################################
#   Autoren: Sarah, Kristina, Fadri
#   Erstellungsdatum: 27.04.2023
#   Beschreibung: INF_PROG2_P05
#   Version: 1.6 (GVC)
#   Letze Änderung: 17.05.2023
#################################################################################

#(B) Report on the top 10 of most unreliable stops. Where should you never wait for your
#transportation?
# Sollabfahrt von (technisch: soll_ab_von)
# Istabfahrt von (technisch: ist_ab_von)
# Namen geben --> RailFlow

# -------Aufgaben
# Fadri
# Downloader ergänzen mit mehreren Urls zum übergeben -> Done
# Daten auswählen von bestimmten Datum -> Done
# Calculation neuer algorithmus da mehr Berechnungen -> Done einige Berechnungen müssen noch angepasst werden
# Error handling:   - URL exisitiert nicht
#                   - Datenverarbeitung Fehler
#                   --> möglicherweise konzept erarbeiten
# Visualisierung schöner

# Sarah
#vergleichen von den zwei Datensätzen einbauen -> Done

# Kristina
# code verstehen

import os.path
from datetime import datetime, timedelta, date
import os
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
from PIL import ImageTk, Image
import urllib.request as ur
import matplotlib.pyplot as plt
from difflib import get_close_matches
import pandas as pd
import threading

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
        #stops = self.data['halt_diva_von'] # Liste aller Haltestellen
        #delay_stop = {}
        results = []
        top_stops = []
        data_delay = self.data
        
        df_haltestellen = pd.read_csv("Haltestelle.csv")
        mapping_dict = df_haltestellen.set_index('halt_diva')['halt_lang'].to_dict()
        data_delay['stop'] = data_delay['halt_diva_von'].map(mapping_dict)
        data_delay['delay'] = (data_delay['effective_soll'] - data_delay['effective_ist'])
        data_delay['delay'] = data_delay['delay'].dt.total_seconds()
        data_delay = data_delay.sort_values('delay', ascending=False)
        #sorted_delays = sorted(data_delay.items(), key=lambda x: x[1], reverse=True) # sortieren der Haltestellen nach Verspätung (absteigend)
        
        result = data_delay.groupby('stop')['delay'].mean() # Timedelta falls fehler
        for stop, mean in result.items():
            results.append({'stop': stop, 'delay': mean})
        
        top_unreliable_stops_sorted = data_delay.nlargest(10, 'delay')# Top ten für ausgabe
        top_unreliable_stops = top_unreliable_stops_sorted[['stop', 'delay']].copy()

        """
        for stop in stops:
            stop_data = self.data[self.data['halt_diva_von'] == stop] # Daten für diese Haltestelle filtern
            delay = (stop_data['effective_soll'] - stop_data['effective_ist']).mean().total_seconds() #// 60 # Delay in Sekunden (mit // 60 in Minuten) mit berechnung von datetime-Objekten
            delay_stop[stop] = delay # speichern der berechneten verspätung
        """
        return pd.DataFrame(results), pd.DataFrame(top_unreliable_stops), pd.DataFrame(data_delay)
               
        
class Visualization(tk.Frame):
    def __init__(self, dataframe1, dataframe2, title1, title2):
        super().__init__()
        #self.root = tk.Tk()
        self.dataframe1 = dataframe1
        self.dataframe2 = dataframe2
        self.title1 = title1
        self.title2 = title2
        self.create_widgets()
        self.create_button_close()
        self.master.geometry("800x600")
        #self.root.mainloop()
      
    def create_widgets(self):
        # Dataframe 1
        frame = tk.Frame(self)
        frame.pack(side="left", fill="both", expand=True)
        frame1 = tk.Frame(frame)
        frame1.pack(side="left", fill="both", expand=True)
        
        title_label1 = tk.Label(frame1, text=self.title1)
        title_label1.pack(side="top", fill="x", pady=10)
        
        treeview1 = tk.ttk.Treeview(frame1, columns=list(self.dataframe1.columns), show='headings')
        for col in list(self.dataframe1.columns):
            treeview1.heading(col, text=col)
        for index, row in self.dataframe1.iterrows():
            treeview1.insert("", tk.END, values=list(row))
        treeview1.pack(side="left", fill="both", expand=True)
        
        # Dataframe 2
        frame2 = tk.Frame(frame)
        frame2.pack(side="left", fill="both", expand=True)
        
        title_label2 = tk.Label(frame2, text=self.title2)
        title_label2.pack(side="top", fill="x", pady=10)
        
        treeview2 = tk.ttk.Treeview(frame2, columns=list(self.dataframe2.columns), show='headings')
        for col in list(self.dataframe2.columns):
            treeview2.heading(col, text=col)
        for index, row in self.dataframe1.iterrows():  # Iterate over dataframe1 rows
            treeview2.insert("", tk.END, values=list(row))  # Use dataframe1 row values
        treeview2.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.on_scroll)
        scrollbar.pack(side="right", fill="y")

        # treeview beide .... zusammen?
        treeview1.configure(yscrollcommand=scrollbar.set)
        treeview2.configure(yscrollcommand=scrollbar.set)
        
    def on_scroll(self, *args):
        for treeview in self.winfo_children()[0].winfo_children():
            treeview.yview(*args)
        
    def create_button_close(self):
        title_button = tk.Button(self, text="Schliessen", command=self.close)
        title_button.pack(side="right", pady=10)
    
    def close(self):
        self.master.destroy()

class App:
    def __init__(self, root):
        root.title("VBZ Verspätungen")
        width=504
        height=195
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        background_image = ImageTk.PhotoImage(Image.open("bushaltestelle.jpg"))
        icon_path = "bus.png"
        root.iconbitmap(icon_path)
        
        l_background=tk.Label(root, image=background_image)
        l_background.place(x=0, y=0, relwidth=1, relheight=1)
        l_background.image = background_image

        b_delay=tk.Button(root)
        b_delay["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        b_delay["font"] = ft
        b_delay["fg"] = "#000000"
        b_delay["justify"] = "center"
        b_delay["text"] = "Verspätungen"
        b_delay.place(x=140,y=150,width=103,height=30)
        b_delay["command"] = self.b_delay_command

        b_bar=tk.Button(root)
        b_bar["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        b_bar["font"] = ft
        b_bar["fg"] = "#000000"
        b_bar["justify"] = "center"
        b_bar["text"] = "Balkendiagramm"
        b_bar.place(x=260,y=150,width=104,height=30)
        b_bar["command"] = self.b_bar_command

        b_close=tk.Button(root)
        b_close["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        b_close["font"] = ft
        b_close["fg"] = "#000000"
        b_close["justify"] = "center"
        b_close["text"] = "Schliessen"
        b_close.place(x=380,y=150,width=103,height=30)
        b_close["command"] = self.b_close_command
        
        b_dataframe=tk.Button(root)
        b_dataframe["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        b_dataframe["font"] = ft
        b_dataframe["fg"] = "#000000"
        b_dataframe["justify"] = "center"
        b_dataframe["text"] = "Datensätze"
        b_dataframe.place(x=20,y=150,width=104,height=30)
        b_dataframe["command"] = self.b_dataframe_command
        
        l_delay=tk.Label(root)
        ft = tkFont.Font(family='Times',size=23)
        l_delay["font"] = ft
        l_delay["fg"] = "#333333"
        l_delay["justify"] = "center"
        l_delay["text"] = "VBZ Verspätungen"
        l_delay.place(x=100,y=20,width=321,height=30)

    def b_delay_command(self):
        stops = Stops(dataframe).unique_stops()
        line_diagram = DataFrameLineDiagram(stops, data_delay1)
        line_diagram.search('stop')

    def b_bar_command(self):
        visualizer = Barvisualizer(top_stops1)
        visualizer.plot_bar()

    def b_close_command(self):
        root.destroy()

    def b_dataframe_command(self):
        title1 =f'{start_sunday} - {start_saturday}'
        title2 =f'{end_sunday} - {end_saturday}'
        df_visualizer = Visualization(dataframe1=df1, dataframe2=df2, title1 = title1, title2= title2)
        df_visualizer.pack(fill="both", expand=True)

class Barvisualizer:
    def __init__(self, top_stops):
        self.df = top_stops
    
    def plot_bar(self):
        x_values = self.df['stop']
        y_values = self.df['delay']
        plt.bar(x_values, y_values)
        plt.xlabel('Haltestellen')
        plt.ylabel('Verspätung')
        plt.title('Top 10 Haltestellen')
        plt.xticks(rotation=45) # Rotation um 45 der X-Achsenbeschriftung um lesen zu können
        plt.tight_layout() # Anpassen um überlappungen vorzubeugen
        plt.gca().xaxis.set_tick_params(pad=0) # Schrift ein wenig weiter nach links um es besser lesen zu können aber hä
        plt.show()

class DataFrameLineDiagram:
    def __init__(self, dataframe, df1):
        self.dataframe = dataframe
        self.df = df1
        self.search_results = []
        self.window = Tk()
        self.window.title("")
        self.label = Label(self.window, text="Haltestelle:")
        self.label.pack()
        self.entry = Entry(self.window)
        self.entry.pack()
        self.search_button = Button(self.window, text="Suchen", command=self.perform_search)
        self.search_button.pack()
        self.close_button = Button(self.window, text="Schliessen", command=self.close_window)
        self.close_button.pack()

    def perform_search(self):
        search_term = self.entry.get()

        # closest match -> lib?
        matches = get_close_matches(search_term, self.dataframe['stop'])
        if matches:
            match = matches[0]
            calc = Stop_calculation(self.df, match)
            lineplot = calc.find_columns_with_same_value()
            lineplot_sorted = lineplot.sort_values('effective_ist', ascending=False)
            plt.plot(lineplot_sorted['effective_ist'], lineplot_sorted['delay'])
            plt.xlabel('Zeit')
            plt.ylabel('Verspätung')
            plt.title(f'Verspätungen für {match}')
            plt.show()
        else:
            messagebox.showinfo("Suchresultat", "Keine Haltestelle gefunden.")

    def close_window(self):
        self.window.destroy()

    def search(self, column):
        self.window.mainloop()

class Stops:
    def __init__(self, data):
        self.data = data
    
    def unique_stops(self):
        data = []
        df_haltestellen = pd.read_csv("Haltestelle.csv")
        stops = self.data['halt_diva_von'].unique() # Liste aller Haltestellen
        for stop in stops:
            matching_row = df_haltestellen.loc[df_haltestellen['halt_diva'] == stop] #filtern wo stimmen zahlen überein
            if not matching_row.empty:
                stop = matching_row['halt_lang'].values[0]  #values damit es name anzeigt und nicht spalte aus matching row
                data.append({'stop': stop})
        return pd.DataFrame(data)

class Stop_calculation:
    def __init__(self, data, value):
        self.data = data
        self.value = value

    def find_columns_with_same_value(self):
        stop_df = self.data[self.data['stop'] == self.value].copy()
        return pd.DataFrame(stop_df[['effective_ist', 'delay']])

class Downloader: # Downloader vgl. P04
    #neu ein Array mitgeben mit Urls die dann downloaed werden in einer Schleife
    def __init__(self, url):
        self.url = url 
        self.file_name = os.path.basename(url)
        print (self.file_name) #definiert den Namen des Dokuments so wie die url basis
    
    def download(self, timeout = 6000000):
        #wenn es nicht im cache ist oder mehr als 60000 Sekunden (10 Stunden) her ist-> daten neu holen
        try: 
            if not os.path.isfile(self.file_name) or time.time() - os.stat(self.file_name).st_mtime > timeout:
                print(f"\nLoading data from url {self.url}. \n This may take a while if files are large.")
                ur.urlretrieve(self.url, self.file_name)                
            else:
                #datei wird aus cache geladen, read only
                #f = open(self.file_name, 'r')
                print(f"Taking file {self.file_name} from cache.")                    

        except Exception as e:
            print(f'Error downloading file: {e}')
        
        file_path = os.path.abspath(self.file_name) #absoluter pfad vom cache file
        return file_path   

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
            return formated_sunday, formated_saturday
        else:
            today = date.today()
            date_obj = datetime.strftime(today, f"%d.%m.%Y")
            sunday = date_obj - timedelta(days=date_obj.weekday() + 1)
            saturday = sunday + timedelta(days=6)
            formated_sunday = sunday.strftime(f'%Y%m%d')
            formated_saturday = saturday.strftime(f'%Y%m%d')
            return formated_sunday, formated_saturday
    
if __name__ == '__main__':
    
    #start_date = input("Geben Sie die erste Woche vom vergleich an (leer lassen für aktuelles Datum dd.mm.yyyy): ") 
    #end_date = input("Geben Sie die zweite Woche vom Datensatz an (leer lassen um keinen Vergleich zu generieren): ")
    start_date = "20.03.2023"
    end_date = "10.01.2023"
    start_date_obj = Timespan(start_date)
    if end_date is not None:
        end_date_obj = Timespan(end_date)
    else:
        end_date_obj = None   
    start_sunday, start_saturday = start_date_obj.calculate_time()
    if end_date_obj is not None:
        end_sunday, end_saturday = end_date_obj.calculate_time()

    urls = [
            f'https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Fahrzeiten_SOLL_IST_{start_sunday}_{start_saturday}.csv',
            f'https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Fahrzeiten_SOLL_IST_{end_sunday}_{end_saturday}.csv',
             "https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Haltestelle.csv"
    ]
    for url in urls:
        downloader = Downloader(url)
        file_path= downloader.download()
        if f'Fahrzeiten_SOLL_IST_{start_sunday}_{start_saturday}.csv' in file_path:
            data_path = Data(file_path)
            dataframe = data_path.data()
            calculator = Calculator(dataframe)
            df1, top_stops1, data_delay1 = calculator.calculate()
        elif f'Fahrzeiten_SOLL_IST_{end_sunday}_{end_saturday}.csv' in file_path:
            data_path = Data(file_path)
            dataframe = data_path.data()
            calculator = Calculator(dataframe)
            df2, top_stops2, data_delay2 = calculator.calculate()
    
    # Data vizualisation
    root = tk.Tk()
    app = App(root)
    root.mainloop()