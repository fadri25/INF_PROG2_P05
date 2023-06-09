# Erster Versuch (ohne delay ausgabe)
"""    
df = self.data.dropna(subset=['effective_soll', 'effective_ist']) # Entfernt Zeilen wo keine Zeit steht
#df['delay_minutes'] = (df['effective_ist'] - df['effective_soll'])# / 60 Berechnung verspaetung
df['delay_seconds'] = (df['ist_ab_von'] - df['soll_ab_von']) # Delay in secunden
df_avg_delay = df.groupby('halt_diva_von')['delay_seconds'].mean().reset_index() # Durchschnittliche Verspätung für jeden Stop
df_sorted = df_avg_delay.sort_values(by='delay_seconds', ascending=False) # Sortieren um die ersten 10 identifizieren zu können
print('Top 10 most unreliable stops:') # Ausgabe erste 10
for halt_diva_von in df_sorted['halt_diva_von'][:10]:
    print(halt_diva_von)
"""

"""
for stop, delay in top_unreliable_stops: # Für die ersten zehn
    print(f'Stop {stop}: average delay of {delay:.2f} seconds.') # Ausgabe
"""

"""
#alter downlaoder mit path angabe
class Downloader: # Downloader selbsterklärend vgl. P04?
    def __init__(self, url, path):
        self.url = url 
        self.file_path = path
        
    def download(self, timeout=60000):
        try:
            file_age = time.time() - os.path.getmtime(self.file_path)
            if file_age < timeout:
                print(f'Using cached file: {self.file_path}')
                return self.file_path
            
            response = requests.get(self.url)
            with open(self.file_path, 'wb') as f:
                f.write(response.content)
            print(f'Downloaded file: {self.file_path}')
            return self.file_path
        except Exception as e:
            print(f'Error downloading file: {e}')

if __name__ == '__main__':
    # Alle variablen die man braucht
    url = 'https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Fahrzeiten_SOLL_IST_20230319_20230325.csv'
    path = r'C:\Users\fadri\Downloads\Fahrzeiten_SOLL_IST_20230319_20230325.csv'


    #downloaden des datensets
    #url = 'https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Fahrzeiten_SOLL_IST_20230319_20230325.csv'
    #downloader = Downloader(url)
    #data = downloader.download()

    #zweiter Datensatz -> geht nicht mit url, nimmt gleiches dokument
    #url2 = 'https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Fahrzeiten_SOLL_IST_20230108_20230114.csv'
    #downloader2 = Downloader(url2)
    #data2 = downloader.download()

    #downloaden de datensets Haltestellen
    #url_haltestelle = "https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Haltestelle.csv"
    #haltestellen_downlaoder = Downloader(url_haltestelle)
    #haltestelle_data = haltestellen_downlaoder.download()

    #aufrufen der Klassen und Methoden zum auswerten
    #data_path = Data(data)
    #dataframe = data_path.data()
    #calculator = Calculator(dataframe)
    #df = calculator.calculate()
    
    
    for stop in stops:
        stop_data = self.data[self.data['halt_diva_von'] == stop] # Daten für diese Haltestelle filtern
        delay = (stop_data['effective_soll'] - stop_data['effective_ist']).mean().total_seconds() #// 60 # Delay in Sekunden (mit // 60 in Minuten) mit berechnung von datetime-Objekten
        delay_stop[stop] = delay # speichern der berechneten verspätung
"""
        #sorted_delays = sorted(data_delay.items(), key=lambda x: x[1], reverse=True) # sortieren der Haltestellen nach Verspätung (absteigend)

"""
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
        """
        #return pd.DataFrame(results), pd.DataFrame(top_unreliable_stops), pd.DataFrame(data_delay)
        #datei wird aus cache geladen, read only
        #f = open(self.file_name, 'r')

#start_date = input("Geben Sie die erste Woche vom vergleich an (leer lassen für aktuelles Datum dd.mm.yyyy): ") 
#end_date = input("Geben Sie die zweite Woche vom Datensatz an (leer lassen um keinen Vergleich zu generieren): ")
"""
start_date = "20.03.2023"
end_date = "10.01.2023"
start_date_obj = timetransformations.Timespan(start_date)
if end_date is not None:
    end_date_obj = timetransformations.Timespan(end_date)
else:
    end_date_obj = None   
start_sunday, start_saturday = start_date_obj.calculate_time()
if end_date_obj is not None:
    end_sunday, end_saturday = end_date_obj.calculate_time()
"""