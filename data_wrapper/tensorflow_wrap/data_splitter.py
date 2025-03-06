import pandas as pd
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def data_split(df, train_size=0.7, val_size=None, random_state=None, is_save=False, index=False):
    """
    Chia DataFrame thành 3 phần: train, validation, test.
    
    Args:
        df (pd.DataFrame): DataFrame cần chia.
        train_size (float): Tỉ lệ dữ liệu train (mặc định 70%).
        val_size (float, optional): Tỉ lệ dữ liệu validation (mặc định 15%). Nếu không có, chỉ chia thành train và test.
        random_state (int, optional): Seed để tái lập kết quả.
        is_save (bool, optional): Nếu True, lưu các tập dữ liệu vào file CSV.
        index (bool, optional): Nếu True, lưu chỉ mục vào file CSV.
    
    Returns:
        tuple: (train_df, val_df, test_df) nếu có val_size, ngược lại (train_df, test_df)
    """
    if train_size + (val_size if val_size else 0) > 1:
        raise ValueError("Tổng train_size, val_size không được lớn hơn 1.")
    
    test_size = 1 - train_size - (val_size if val_size else 0)
    
    if val_size:
        assert train_size + val_size + test_size == 1, "Tổng train_size, val_size, test_size phải bằng 1."
        
        train_df, temp_df = train_test_split(df, train_size=train_size, random_state=random_state)
        val_ratio = val_size / (val_size + test_size)  # Tỉ lệ validation so với phần còn lại
        val_df, test_df = train_test_split(temp_df, train_size=val_ratio, random_state=random_state)
        
        if is_save:
            train_df.to_csv("train.csv", index=index)
            val_df.to_csv("val.csv", index=index)
            test_df.to_csv("test.csv", index=index)
            logging.info("Saved data successfully")
            
        return train_df, val_df, test_df

    else:
        assert train_size + test_size == 1, "Tổng train_size và test_size phải bằng 1."
        
        train_df, test_df = train_test_split(df, train_size=train_size, test_size=test_size, random_state=random_state)
        if is_save:
            train_df.to_csv("train.csv", index=index)
            test_df.to_csv("test.csv", index=index)
            logging.info("Saved data successfully")
        
        return train_df, test_df
