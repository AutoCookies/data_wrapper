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

    
