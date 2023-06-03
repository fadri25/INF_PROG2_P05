import pandas as pd

class Calculator:
    def __init__(self, data):
        self.data = data
                 
    def data_delay(self, condition):
        data_delay = self.data # Make a copy of the data
        df_haltestellen = pd.read_csv("Haltestelle.csv") # Read the 'Haltestelle.csv' into DataFrame
        mapping_dict = df_haltestellen.set_index('halt_diva')['halt_lang'].to_dict() # Create a mapping dictionary from 'halt_diva' to 'halt_lang'
        data_delay['stop'] = data_delay['halt_diva_von'].map(mapping_dict) # Map 'halt_diva_von' to 'halt_lang' using the mapping dictionary
        data_delay['delay'] = (data_delay['effective_ist'] - data_delay['effective_soll']) # Calculate the delay for each row
        data_delay['delay'] = data_delay['delay'].dt.total_seconds().round(1) # Calculates the delay in seconds
        data_delay = data_delay.sort_values('delay', ascending=False) # Sorts the DataFrame
        result = data_delay.groupby('stop')['delay'].mean().round(1) # Calculates the mean delay for each unique 'stop' and only gets columns 'stop' and 'delay'
        result_delay = data_delay.groupby(['stop', 'halt_diva_von']).agg({'delay': 'mean'}).round(1) # DataFrame with 'stop' 'halt_diva_von' and the mean delay for each station
        if condition:
            return result, data_delay # Return for DataFrame of first week
        else:
            return result_delay # Return for DataFrame of second week
          
    def calculate_df1(self):
        result, data_delay = self.data_delay(True) # Calculations for first DataFrame
        top_means = result.nlargest(10, keep='all')
        topppp = pd.DataFrame({'stop': top_means.index, 'delay': top_means.values.round(1)})
        meandelay = data_delay[['stop', 'halt_diva_von', 'delay']]
        sorted_df = meandelay.groupby(['stop', 'halt_diva_von']).agg({'delay': 'mean'}).round(1)
        sorted_df = sorted_df.sort_values(by=['delay'], ascending=False)
        return pd.DataFrame(topppp), pd.DataFrame(data_delay), sorted_df

    def calculate_df2(self):
        result = self.data_delay(False) # Calculations for second DataFrame
        results = []
        for (stop, halt_diva_von), mean in result.groupby(['stop', 'halt_diva_von'])['delay'].mean().round(1).items():
            results.append({'stop': stop, 'halt_diva_von': halt_diva_von, 'delay': mean})
        return pd.DataFrame(results)
     
class Meancalculator:
    def __init__(self, dataframe, match):
        self.dataframe = dataframe
        self.match = match
        
    def calculate_mean(self):
        search = self.dataframe[self.dataframe['stop'] == self.match] # Calculates the mean delay for a specific station from the entry box
        grouped = search.groupby(['stop', 'betriebsdatum'])
        mean_values = grouped['delay'].mean().reset_index()
        return mean_values

class Stops:
    def __init__(self, data):
        self.data = data
        
    def unique_stops(self):
        data = [] # Gets all unique stops for the autocomplete entrybox
        df_haltestellen = pd.read_csv("Haltestelle.csv")
        stops = self.data['halt_diva_von'].unique()
        for stop in stops:
            matching_row = df_haltestellen.loc[df_haltestellen['halt_diva'] == stop]
            if not matching_row.empty:
                stop = matching_row['halt_lang'].values[0]
                data.append({'stop': stop})
        return pd.DataFrame(data)

class Stopcalculation:
    def __init__(self, data, value):
        self.data = data
        self.value = value

    def find_columns_with_same_value(self):
        data = Meancalculator(self.data, self.value) # Triggered when a station is passed in the autocomplete entrybox to get the mean delays for the specific station
        data_mean = data.calculate_mean()
        return pd.DataFrame(data_mean)

if __name__ == '__main__':
    pass
