import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_wrapper import CSVExporter as csv

csv_path = "D:\\Github Projects\\data_wrapper\\test\\test_data\\train.csv"
data = csv.from_csv(csv_path)
print(data.get_head(3))
data.to_xml("train")