import json
import os

import requests
from loguru import logger


class TireTypeRetriever:
    def __init__(self, filename='./cache/timing/data.txt'):
        self.filename = filename
        self.tire_types = {}
        self.retrieve_data()

    def retrieve_data(self):
        raw_data = ''
        if os.path.isfile(self.filename):
            logger.info(f"Found file {self.filename}. Loading data...")
            with open(self.filename, 'r') as f:
                raw_data = f.read()
        else:
            url = 'https://livetiming.formula1.com/static/2023/2023-05-07_Miami_Grand_Prix/2023-05-07_Race/TimingAppData.jsonStream'
            logger.info(f"Retrieving data from {url}...")
            response = requests.get(url)
            if response.status_code == 200:
                raw_data = response.text
                with open(self.filename, 'w') as f:
                    f.write(raw_data)
            else:
                logger.error(f'Error retrieving data from API. Status code: {response.status_code}')

        self.lines = [line.strip() for line in raw_data.split('\n') if line.strip()]

    def process_data(self):
        count = 0
        for timestamp_event in self.lines:
            event = json.loads(timestamp_event[12:])
            line_content = event['Lines']
            count += 1
            if count == 3:
                for driver_id in line_content:
                    start_compound = line_content[driver_id]['Stints']['0']['Compound']
                    self.tire_types[driver_id] = [(1, start_compound)]

        for driver_id in self.tire_types:
            count = 0
            lap_number = 1
            previous_total_laps = 0
            for timestamp_event in self.lines:
                count += 1
                if count > 3:
                    event = json.loads(timestamp_event[12:])
                    for driver_id_event in event["Lines"]:
                        if driver_id == driver_id_event:
                            if 'Stints' in event["Lines"][driver_id] and 'Line' not in event["Lines"][driver_id]:
                                stints = event["Lines"][driver_id]['Stints']

                                for stint_id in stints:
                                    current_stint = stints[stint_id]

                                    if 'TotalLaps' in current_stint:
                                        total_laps = current_stint['TotalLaps']
                                        if total_laps > previous_total_laps:
                                            lap_number = lap_number + 1

                                        previous_total_laps = total_laps

                                    if 'Compound' in current_stint:
                                        compound = current_stint['Compound']
                                        if compound != 'UNKNOWN':
                                            self.tire_types[driver_id].append((lap_number, current_stint['Compound']))

    def get_compound(self, driver_number, lap_number):
        driver_number = str(driver_number)
        if driver_number in self.tire_types:
            compound_list = self.tire_types[driver_number]
            compound = None
            for lap, cmp in compound_list:
                if lap <= lap_number:
                    compound = cmp
                else:
                    break
            return compound
        else:
            return None
