import pandas as pd

from retrieve_drivers import DriverRetriever
from retrieve_lap_times import LapTimeRetriever
from retrieve_tire_types import TireTypeRetriever


class RaceDataRetriever:
    def __init__(self):
        self.driver_retriever = DriverRetriever()
        self.lap_retriever = LapTimeRetriever()
        self.tire_retriever = TireTypeRetriever()

    def load_data(self):
        self.driver_retriever.load_drivers()
        self.lap_times = self.lap_retriever.process_lap_timings()
        self.tire_retriever.retrieve_data()
        self.tire_retriever.process_data()

    def create_timing_dataframe(self):
        current_lap = 1
        for lap_time in self.lap_times:
            for timing in lap_time:
                driver_number = self.driver_retriever.get_driver_number(timing['driverId'])
                compound = self.tire_retriever.get_compound(driver_number, current_lap)
                timing['compound'] = compound
            current_lap += 1

        data_flat = [item for sublist in self.lap_times for item in sublist]

        df = pd.DataFrame(data_flat)
        df['lap_number'] = df.groupby('driverId').cumcount() + 1

        return df
