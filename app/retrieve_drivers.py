import json
import os

from loguru import logger


class DriverRetriever:
    def __init__(self, driver_cache_file='./cache/drivers/drivers.json'):
        self.driver_cache_file = driver_cache_file

    def load_drivers(self):
        """Return a list of drivers from the cache file.

        Raises:
            FileNotFoundError: If the driver cache file cannot be found.
        """
        if not os.path.isfile(self.driver_cache_file):
            logger.error(f"Driver cache file not found: {self.driver_cache_file}")
            raise FileNotFoundError(f"Cache file not found: {self.driver_cache_file}")

        logger.info(f"Reading driver cache file: {self.driver_cache_file}")
        with open(self.driver_cache_file, 'r') as f:
            raw_data = f.read()

        logger.info("Parsing JSON data")
        json_data = json.loads(raw_data)

        logger.info(f"Loaded {len(json_data)} drivers from cache")
        self.drivers = json_data

    def get_driver_number(self, driver_id):
        """Return the driver number for the given driver ID."""
        for driver in self.drivers:
            if driver['id'] == driver_id:
                return driver['number']

        logger.error(f"Driver ID {driver_id} not found in driver cache")
        return None
