import csv
import logging
from abc import ABC

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class CSVLoader(ABC):
    """
    Class for loading CSV data without pandas, designed to behave like pandas.read_csv.
    """

    def __init__(self, csv_path: str):
        """
        Initializes the CSVLoader with the provided CSV file path.
        """
        self.csv_path = csv_path
        self.data = []
        self.columns = []
        self._load_data()

    def _load_data(self):
        """
        Reads the CSV file and loads the data into a list of dictionaries.
        Also sets the column names.
        """
        try:
            with open(self.csv_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.data = list(reader)  # Convert iterator to list
                if not self.data:
                    logging.warning(f"CSV file '{self.csv_path}' is empty or contains only headers.")

                self.columns = reader.fieldnames if reader.fieldnames else []
        except FileNotFoundError:
            logging.error(f"CSV file not found: {self.csv_path}")
        except csv.Error as e:
            logging.error(f"Error reading CSV file: {e}")
        except Exception as e:
            logging.error(f"An error occurred while reading the CSV file: {e}")

    @classmethod
    def from_csv(cls, csv_path: str):
        """
        Alternative constructor to read a CSV file directly.

        Args:
            csv_path (str): The path to the CSV file.

        Returns:
            CSVLoader: An instance of CSVLoader with loaded data.
        """
        return cls(csv_path)

    def get_columns(self):
        """
        Returns a list of column names in the CSV file.

        Returns:
            list: Column names.
        """
        return self.columns
