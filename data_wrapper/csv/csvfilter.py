from .csvsetter import CSVSetter
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class CSVFilter (CSVSetter):
    """
    Class extending CSVGetter to filter data based on conditions.
    """

    def filter(self, condition):
        """
        Filter rows based on a condition function.

        Args:
            condition (function): A function that takes a row (dict) and returns True/False.

        Returns:
            list[dict]: A filtered list of rows.
        """
        if not self.data:
            logging.warning("No data loaded.")
            return []
        
        return [row for row in self.data if condition(row)]
