import pandas as pd

class Calculator:
    def __init__(self, data):
        self.data = data # Einlesen Daten
        
    def calculate(self):
        results = []
        data_delay = self.data
        df_haltestellen = pd.read_csv("Haltestelle.csv")
        mapping_dict = df_haltestellen.set_index('halt_diva')['halt_lang'].to_dict()
        data_delay['stop'] = data_delay['halt_diva_von'].map(mapping_dict)
        data_delay['delay'] = (data_delay['effective_ist'] - data_delay['effective_soll'])
        data_delay['delay'] = data_delay['delay'].dt.total_seconds().round(1)
        data_delay = data_delay.sort_values('delay', ascending=False)
        result = data_delay.groupby('stop')['delay'].mean().round(1) # Timedelta falls fehler 
        for stop, mean in result.items():
            results.append({'stop': stop, 'delay': mean})
        top_means = result.nlargest(10, keep='all')
        topppp = pd.DataFrame({'stop': top_means.index, 'delay': top_means.values.round(1)})
        sorted_delay = pd.DataFrame(result)
        sorted_df = sorted_delay.sort_values(by=['delay'], ascending=True)
        return pd.DataFrame(results), pd.DataFrame(topppp), pd.DataFrame(data_delay), sorted_df  
    
class Meancalculator:
    def __init__(self, dataframe, match):
        self.dataframe = dataframe
        self.match = match
    
    def calculate_mean(self):
        filter = self.dataframe[self.dataframe['stop'] == self.match]
        grouped = filter.groupby(['stop', 'betriebsdatum'])
        mean_values = grouped['delay'].mean().reset_index()
        return mean_values

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
        data = Meancalculator(self.data, self.value)
        data_mean = data.calculate_mean()
        return pd.DataFrame(data_mean)

if __name__ == '__main__':
    pass
