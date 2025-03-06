import pandas as pd
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def data_split(df: pd.DataFrame, train_size=0.7, val_size=None, test_size=0.15, random_state=None, is_save=False, index = False):
    """
    Split the DataFrame inot 3 parts: train, validation, test.
    Can use this when there are only a single csv file
    Args:
        df (pd.DataFrame): DataFrame cần chia.
        train_size (float): Tỉ lệ dữ liệu train (mặc định 70%).
        val_size (float): Tỉ lệ dữ liệu validation (mặc định 15%).
        test_size (float): Tỉ lệ dữ liệu test (mặc định 15%).
        random_state (int, optional): Seed để tái lập kết quả.
        is_save (bool, optional): Nếu True, lưu các tập dữ liệu vào file CSV.
    Returns:
        tuple: (train_df, val_df, test_df)
    """
    if val_size:
        assert train_size + val_size + test_size == 1, "Tổng train_size, val_size, test_size phải bằng 1."
        
        train_df, temp_df = train_test_split(df, train_size=train_size, random_state=random_state)
        val_ratio = val_size / (val_size + test_size)  # Tỉ lệ validation so với phần còn lại
        val_df, test_df = train_test_split(temp_df, train_size=val_ratio, random_state=random_state)
        
        if is_save:
            train_df.to_csv("./train.csv", index=index)
            val_df.to_csv("./val.csv", index=index)
            test_df.to_csv("./test.csv", index=index)
            logging.info("Saved data succesfully")
            
        return train_df, val_df, test_df

    elif not val_size:
        assert train_size + test_size == 1
        
        train_df, test_df = train_test_split(df, train_size=train_size, test_size=test_size)
        if is_save:
            train_df.to_csv("./train.csv", index = index)
            test_df.to_csv("./test.csv", index = index)
            logging.info("Saved data succesfully")
        
        return train_df, test_df
    
            
        

