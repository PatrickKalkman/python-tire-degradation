import json
import os
import random
import time

import requests
from loguru import logger


class LapTimeRetriever:
    def __init__(self, cache_path='./cache/lap_times/'):
        self.cache_path = cache_path
        self.url = 'https://ergast.com/api/f1/2023/5/laps/'

    @staticmethod
    def laptime_to_seconds(laptime):
        minutes, seconds = map(float, laptime.split(":"))
        return minutes * 60 + seconds

    def get_lap_timings(self, lap_number):
        lap_time_cache_path = f'{self.cache_path}{lap_number}.json'
        if os.path.isfile(lap_time_cache_path):
            logger.info(f"Found cached lap times for lap {lap_number}")
            with open(lap_time_cache_path, 'r') as f:
                raw_data = f.read()
            from_cache = True
        else:
            logger.info(f"Retrieving lap times for lap {lap_number} from API")
            response = requests.get(f"{self.url}{lap_number}.json")
            raw_data = response.text
            if response.status_code == 200:
                with open(lap_time_cache_path, 'w') as f:
                    f.write(raw_data)
            from_cache = False

        raw_data = json.loads(raw_data)
        if not raw_data['MRData']['RaceTable']['Races']:
            return [], from_cache

        # Add the tire compound information to the lap timings
        lap_timings = raw_data['MRData']['RaceTable']['Races'][0]['Laps'][0]['Timings']
        for timing in lap_timings:
            timing['compound'] = 'MEDIUM'
            timing['laptime_seconds'] = self.laptime_to_seconds(timing['time'])

        return lap_timings, from_cache

    def process_lap_timings(self, total_laps=57):
        all_lap_timings = []
        for lap_number in range(1, total_laps+1):
            lap_timings, from_cache = self.get_lap_timings(lap_number)
            all_lap_timings.append(lap_timings)
            if not from_cache:
                wait_time = random.uniform(2, 8)
                logger.info(f"Waiting for {wait_time} seconds before next request")
                time.sleep(wait_time)
        return all_lap_timings
