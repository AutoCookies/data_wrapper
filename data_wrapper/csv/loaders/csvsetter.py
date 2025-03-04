import csv
import logging
from .csvgetter import CSVGetter

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class CSVSetter(CSVGetter):
    """
    Class extending CSVGetter to provide additional data manipulation functionalities.
    """
    
    def __setitem__(self, column_name, values):
        """Allow adding a new column dynamically."""
        if not self.data:
            logging.warning("No data loaded, cannot add a column.")
            return
        
        if len(values) != len(self.data):
            raise ValueError(f"Column length mismatch: expected {len(self.data)}, got {len(values)}")

        for row, value in zip(self.data, values):
            row[column_name] = value

    def to_csv(self, filename):
        """
        Save the modified data to a new CSV file.

        Args:
            filename (str): The name of the file to save.
        """
        if not self.data:
            logging.warning("No data to save.")
            return

        try:
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.data[0].keys())
                writer.writeheader()
                writer.writerows(self.data)
            logging.info(f"Data successfully saved to {filename}")
        except Exception as e:
            logging.error(f"Failed to save CSV: {e}")
