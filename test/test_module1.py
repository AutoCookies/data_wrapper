import sys
import os
import pandas as pd

# Thêm đường dẫn của thư mục cha vào sys.path để có thể import `data_wrapper`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import data_split từ data_splitter
from data_wrapper.tensorflow_wrap.data_splitter import data_split

# Kiểm tra đường dẫn CSV
csv_path = "D:\\Github Projects\\data_wrapper\\test\\test_data\\test.csv"

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"File {csv_path} không tồn tại.")

df = pd.read_csv(csv_path)
df_train, df_test = data_split(df)

print(df_train.shape)
print(df_test.shape)
