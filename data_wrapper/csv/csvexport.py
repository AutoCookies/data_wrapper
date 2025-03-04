import json
from .csvaggregator import CSVAggregator
import logging
import csv
from openpyxl import Workbook

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class CSVExporter(CSVAggregator):
    """
    Class extending CSVGetter to export data to other formats.
    """

    def to_json(self, filename):
        """Save data as JSON."""
        if not self.data:
            logging.warning("No data to save.")
            return
        
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)
        logging.info(f"Data successfully saved to {filename}")

    def to_excel(self, filename):
        """
        Save data as an actual Excel (.xlsx) file using openpyxl.

        Args:
            filename (str): The name of the Excel file to save.
        """
        if not self.data:
            logging.warning("No data to save.")
            return

        try:
            workbook = Workbook()
            sheet = workbook.active

            # Write headers
            headers = list(self.data[0].keys())
            sheet.append(headers)

            # Write data rows
            for row in self.data:
                sheet.append([row[header] for header in headers])

            # Save the file
            workbook.save(filename)
            logging.info(f"Data successfully saved to {filename}")
        except Exception as e:
            logging.error(f"Failed to save Excel: {e}")
            
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
            
    def to_txt(self, filename):
        """
        Save data as a formatted text file.

        Args:
            filename (str): The name of the file to save.
        """
        if not self.data:
            logging.warning("No data to save.")
            return

        try:
            with open(filename, "w", encoding="utf-8") as file:
                headers = list(self.data[0].keys())
                file.write(" | ".join(headers) + "\n")
                file.write("-" * (len(headers) * 10) + "\n")

                for row in self.data:
                    file.write(" | ".join(str(row[col]) for col in headers) + "\n")

            logging.info(f"Data successfully saved to {filename}")
        except Exception as e:
            logging.error(f"Failed to save TXT: {e}")


    def to_xml(self, filename):
        """
        Save data as an XML file.

        Args:
            filename (str): The name of the file to save.
        """
        if not self.data:
            logging.warning("No data to save.")
            return

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write("<dataset>\n")
                for row in self.data:
                    file.write("  <row>\n")
                    for key, value in row.items():
                        file.write(f"    <{key}>{value}</{key}>\n")
                    file.write("  </row>\n")
                file.write("</dataset>\n")

            logging.info(f"Data successfully saved to {filename}")
        except Exception as e:
            logging.error(f"Failed to save XML: {e}")

