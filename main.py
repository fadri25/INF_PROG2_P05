import csv
#kommentar
#neuer Kommentar
# neuerer Kommentar
class Stop:
    def __init__(self, stop_id, name):
        self.stop_id = stop_id
        self.name = name
        self.num_delays = 0
        self.total_delay = 0

    def add_delay(self, delay):
        self.num_delays += 1
        self.total_delay += delay

    def get_average_delay(self):
        if self.num_delays > 0:
            return self.total_delay / self.num_delays
        else:
            return None

class Dataset:
    def __init__(self, file_path):
        self.stops = {}
        with open(file_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                stop_id = row['halt_diva_von']
                if stop_id not in self.stops:
                    self.stops[stop_id] = Stop(stop_id, row['halt_kurz_von1'])
                delay = self.calculate_delay(row)
                if delay:
                    self.stops[stop_id].add_delay(delay)

    def calculate_delay(self, row):
        scheduled_arrival = row['soll_an_von']
        actual_arrival = row['ist_an_von']
        if actual_arrival and scheduled_arrival:
            delay = int(actual_arrival) - int(scheduled_arrival)
            return delay
        else:
            return None

    def get_most_unreliable_stops(self, num_stops=10):
        sorted_stops = sorted(self.stops.values(), key=lambda x: x.get_average_delay() or 0, reverse=True)
        return sorted_stops[:num_stops]

if __name__ == '__main__':

    dataset = Dataset('Fahrzeiten_SOLL_IST_20230319_20230325.excerpt.csv')
    most_unreliable_stops = dataset.get_most_unreliable_stops(num_stops=10)
    print("The top 10 most unreliable stops are:")
    for stop in most_unreliable_stops:
        print(f"{stop.name} ({stop.stop_id}): average delay {stop.get_average_delay()} seconds, {stop.num_delays} delays in total.")
        
"""
#################################################################################
#   Autoren: Sarah, Kristina, Fadri
#   Erstellungsdatum: 27.04.2023
#   Beschreibung: INF_PROG2_P05
#   Version: 1.4 (GVC)
#   Letze Änderung: 04.05.2023
#################################################################################

import pandas as pd
from datetime import datetime, timedelta
import os
import time
import requests
#import matplotlib.pyplot as plt
import os.path

class Downloader:
    def __init__(self, url, file_path):
        self.url = url
        self.filename = file_path
        
    def download(self, timeout=600):
        try:
            file_age = time.time() - os.path.getmtime(self.filename)
            if file_age < timeout:
                print(f'Using cached file: {self.filename}')
                return file_path
            
            response = requests.get(self.url)
            with open(self.filename, 'wb') as f:
                f.write(response.content)
            print(f'Downloaded file: {self.filename}')
        except Exception as e:
            print(f'Error downloading file: {e}')


class Vehicle:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.routes = {}
    
    def add_route(self, line, direction, route):
        key = (line, direction)
        if key not in self.routes:
            self.routes[key] = []
        self.routes[key].append(route)
    
    def get_delays(self):
        delays = {}
        for key, routes in self.routes.items():
            planned_time = None
            for route in routes:
                for stop in route.stops:
                    if stop.vehicle == self.vehicle_id:
                        if planned_time is None:
                            planned_time = stop.planned_arrival
                        else:
                            delay = stop.actual_arrival - planned_time
                            if key not in delays:
                                delays[key] = []
                            delays[key].append(delay)
        return delays
    
class Route:
    def __init__(self, line, direction, course):
        self.line = line
        self.direction = direction
        self.course = course
        self.stops = []
    
    def add_stop(self, stop):
        self.stops.append(stop)
    
class Stop:
    def __init__(self, vehicle, line, direction, course, stop_id, planned_arrival, planned_arrival_time, actual_arrival, actual_arrival_time):
        self.vehicle = vehicle
        self.line = line
        self.direction = direction
        self.course = course
        self.stop_id = stop_id
        self.planned_arrival = pd.Timestamp(planned_arrival) # wie mit sekunden
        self.actual_arrival = pd.Timestamp(actual_arrival) # same here
        self.planned_arrival_time = TimestampConverter('soll_an_von') # timestamp converter
        self.actual_arrival_time = TimestampConverter('ist_an_von')

    def convert_timestamps(self):
        self.planned_arrival = self.converter.seconds_to_time(self.planned_arrival)
        self.actual_arrival = self.converter.seconds_to_time(self.actual_arrival)

class TimestampConverter:
    def __init__(self, timestamp_col):
        self.timestamp_col = timestamp_col
        self.midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
    def seconds_to_time(self, seconds):
        return self.midnight + timedelta(seconds=seconds)
        
    def convert_dataframe(self, df):
        df['effective_time'] = df[self.timestamp_col].apply(self.seconds_to_time)
        return df

class MobilityDataset:
    def __init__(self, file_path):
        self.routes = {}
        self.vehicles = {}
        self.stops = []
        self.load_dataset(file_path)
    
    def load_dataset(self, file_path):
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            vehicle_id = row['fahrzeug'] # Fahrzeugnummer
            line = row['linie'] # VBZ Liniennummer
            direction = row['richtung'] # Richtung der Fahrt 1/2
            course = row['kurs'] # Kursnummer, relevant?
            stop_id = row['halt_diva_von'] # VBZ intern Haltestellennummer "von"
            planned_arrival = row['soll_an_von'] # Sollankunft (Werte zwischen 0 und 86399)
            actual_arrival = row['ist_an_von'] # Effektive Ankunft (kann werte drüber enthalten wegen verspätung)
            planned_arrival_time = row['']
            actual_arrival_time = row['']
            
            if vehicle_id not in self.vehicles:
                self.vehicles[vehicle_id] = Vehicle(vehicle_id)
            vehicle = self.vehicles[vehicle_id]
            
            key = (line, direction)
            if key not in self.routes:
                self.routes[key] = {}
            if course not in self.routes[key]:
                self.routes[key][course] = Route(line, direction, course)
            route = self.routes[key][course]
            
            stop = Stop(vehicle_id, line, direction, course, stop_id, planned_arrival, planned_arrival_time, actual_arrival, actual_arrival_time )
            route.add_stop(stop)
            self.stops.append(stop)
            vehicle.add_route(line, direction, route)
    
    def get_delays_by_line_and_direction(self, line, direction):
        delays = {}
        for vehicle in self.vehicles.values():
            for key, value in vehicle.get_delays().items():
                if key == (line, direction):
                    if key not in delays:
                        delays[key] = []
                    delays[key].extend(value)
        return delays
        # wenn kein delay return none   

if __name__ == "__main__":
    #downloader = DataDownloader('https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Fahrzeiten_SOLL_IST_20230319_20230325.csv')
    #data = Download('https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Fahrzeiten_SOLL_IST_20230319_20230325.csv')   
    #dataset = MobilityDataset(downloader)
    url = 'https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/download/Fahrzeiten_SOLL_IST_20230319_20230325.csv'
    file_path = r'C:\Users\fadri\Downloads\Fahrzeiten_SOLL_IST_20230319_20230325.csv'
    downloader = Downloader(url, file_path)
    df = downloader.download()
    delays = df.get_delays_by_line_and_direction(10, 1)
    print(delays)

    
"""

# Kristina ist die beste 

#lololo