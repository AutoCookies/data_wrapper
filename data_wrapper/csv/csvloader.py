import csv
import json
import yaml
import sqlite3
import xml.etree.ElementTree as ET
import pickle
import logging
from abc import ABC

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class CSVLoader(ABC):
    """
    Class for loading data from various formats (CSV, JSON, XML, SQLite, etc.) without pandas,
    designed to behave like pandas.read_csv.
    """

    def __init__(self, file_path: str, file_type: str = "csv"):
        """
        Initializes the CSVLoader with the provided file path and type.
        """
        self.file_path = file_path
        self.file_type = file_type.lower()
        self.data = []
        self.columns = []
        self._load_data()

    def _load_data(self):
        """
        Reads the file and loads the data based on the file type.
        Also sets the column names.
        """
        try:
            if self.file_type == "csv":
                self._load_csv()
            elif self.file_type == "json":
                self._load_json()
            elif self.file_type == "xml":
                self._load_xml()
            elif self.file_type == "sqlite":
                self._load_sqlite()
            elif self.file_type == "tsv":
                self._load_tsv()
            elif self.file_type == "yaml":
                self._load_yaml()
            elif self.file_type == "pickle":
                self._load_pickle()
            else:
                logging.error(f"Unsupported file type: {self.file_type}")
        except FileNotFoundError:
            logging.error(f"File not found: {self.file_path}")
        except Exception as e:
            logging.error(f"An error occurred while reading the file: {e}")

    def _load_csv(self):
        with open(self.file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.data = list(reader)
            self.columns = reader.fieldnames if reader.fieldnames else []

    def _load_json(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            self.data = json.load(file)
            self.columns = list(self.data[0].keys()) if self.data else []

    def _load_xml(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        self.data = [{child.tag: child.text for child in elem} for elem in root]
        self.columns = list(self.data[0].keys()) if self.data else []

    def _load_sqlite(self):
        conn = sqlite3.connect(self.file_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            table_name = tables[0][0]
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            self.columns = [desc[0] for desc in cursor.description]
            self.data = [dict(zip(self.columns, row)) for row in rows]
        conn.close()

    def _load_tsv(self):
        with open(self.file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter="\t")
            self.data = list(reader)
            self.columns = reader.fieldnames if reader.fieldnames else []

    def _load_yaml(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            self.data = yaml.safe_load(file)
            self.columns = list(self.data[0].keys()) if self.data else []

    def _load_pickle(self):
        with open(self.file_path, "rb") as file:
            self.data = pickle.load(file)
            self.columns = list(self.data[0].keys()) if self.data else []

    def export_to_csv(self, output_path):
        """
        Exports the loaded data to a CSV file.
        """
        if not self.data:
            logging.warning("No data to export.")
            return

        try:
            with open(output_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.columns)
                writer.writeheader()
                writer.writerows(self.data)
            logging.info(f"Data exported successfully to {output_path}")
        except Exception as e:
            logging.error(f"Error exporting data to CSV: {e}")

    @classmethod
    def from_file(cls, file_path: str, file_type: str):
        """
        Alternative constructor to read a file directly.
        """
        return cls(file_path, file_type)

    def get_columns(self):
        """
        Returns a list of column names in the file.
        """
        return self.columns
