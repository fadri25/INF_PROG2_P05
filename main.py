import csv

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


# Kristina ist die beste 

#lololo