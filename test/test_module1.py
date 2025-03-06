import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import data_wrapper as dw

csv_path = "D:\\Github Projects\\data_wrapper\\test\\test_data\\test.json"
df = dw.read_json(csv_path)
# print(df.show_head())
# print(df.info())
# print(df.describe())
# print(df.show_tail())

df = df.drop(columns = ["age"])
print(df.show_head())