import logging
from .csvloader import CSVLoader
from tabulate import tabulate

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class CSVColumn:
    """
    Wrapper class for column data to provide additional functionalities.
    """

    def __init__(self, data, column_name):
        self.data = data
        self.column_name = column_name

    def get_values(self):
        """Returns all values in the column with automatic type conversion."""
        values = [row[self.column_name] for row in self.data]

        # Chuyển kiểu dữ liệu nếu có thể
        converted_values = [self._convert_value(v) for v in values]
        return converted_values

    def _convert_value(self, value):
        """Convert value to int, float, or keep as string."""
        try:
            return int(value)  # Thử ép kiểu sang integer
        except ValueError:
            try:
                return float(value)  # Nếu không phải int, thử ép kiểu sang float
            except ValueError:
                return value  # Nếu không phải số, giữ nguyên kiểu string


    def get_unique(self):
        """Returns unique values in the column."""
        return list(set(self.get_values()))

    def __repr__(self):
        return f"CSVColumn({self.column_name})"
    
    def __str__(self):
        """Returns a string representation of the column's values."""
        return str(self.get_values())  # Trả về danh sách các giá trị trong cột dưới dạng chuỗi
    
    def get_dtype(self):
        """Determines the most common data type in the column without using numpy."""
        values = self.get_values()

        int32_min, int32_max = -2**31, 2**31 - 1
        float32_min, float32_max = -3.4e38, 3.4e38  # Giới hạn gần đúng của float32

        types = set()

        for v in values:
            if isinstance(v, int):
                if int32_min <= v <= int32_max:
                    types.add("int32")
                else:
                    types.add("int64")
            elif isinstance(v, float):
                if float32_min <= v <= float32_max:
                    types.add("float32")
                else:
                    types.add("float64")
            elif isinstance(v, str):
                types.add("str")
            else:
                types.add("object")  # Trường hợp giá trị không thuộc kiểu nào

        if len(types) == 1:
            return types.pop()  # Trả về kiểu dữ liệu duy nhất nếu có


class CSVGetter(CSVLoader):
    """
    Class extending CSVLoader to provide additional data retrieval functionalities.
    """

    def __getitem__(self, column_name):
        """
        Allows accessing a column using dictionary-like syntax: data["column_name"].

        Args:
            column_name (str): The name of the column.

        Returns:
            CSVColumn: An object representing the column with additional functionalities.
        """
        if not self.data:
            logging.warning("No data loaded.")
            return CSVColumn([], column_name)
        if column_name not in self.data[0]:
            logging.error(f"Column '{column_name}' not found.")
            raise KeyError(f"Column '{column_name}' does not exist.")
        return CSVColumn(self.data, column_name)

    def get_row(self, index):
        """
        Returns a specific row by index.

        Args:
            index (int): The index of the row.

        Returns:
            dict: The row data as a dictionary.
        """
        if not self.data:
            logging.warning("No data loaded.")
            return None
        if index < 0 or index >= len(self.data):
            logging.error("Row index out of range.")
            return None
        return self.data[index]

    def get_value(self, row_index, column_name):
        """
        Returns a specific value from a given row and column.

        Args:
            row_index (int): The index of the row.
            column_name (str): The name of the column.

        Returns:
            str: The value at the specified row and column.
        """
        row = self.get_row(row_index)
        if row is None:
            return None
        if column_name not in row:
            logging.error(f"Column '{column_name}' not found.")
            return None
        return row[column_name]

    def get_head(self, n=5):
        """
        Returns the first 'n' rows of the data in a table-like format, similar to pandas' df.head().
        
        Args:
            n (int, optional): Number of rows to return. Defaults to 5.

        Returns:
            str: A formatted table-like string.
        """
        if not self.data:
            logging.warning("No data loaded.")
            return "No data available."

        head_data = self.data[:n]
        
        # Nếu có tabulate, dùng nó để hiển thị đẹp hơn
        if "tabulate" in globals():
            return tabulate(head_data, headers="keys", tablefmt="grid")  # Kiểu hiển thị giống pandas
        else:
            # Nếu không có tabulate, format thủ công
            headers = self.columns
            rows = [[row[col] for col in headers] for row in head_data]
            
            # Tạo header row
            header_row = " | ".join(headers)
            separator = "-" * len(header_row)
            data_rows = "\n".join([" | ".join(map(str, row)) for row in rows])

            return f"{header_row}\n{separator}\n{data_rows}"
    
    def get_tail(self, n=5):
        """
        Returns the last 'n' rows of the data.

        Args:
            n (int, optional): Number of rows to return. Defaults to 5.

        Returns:
            list[dict]: A list of dictionaries containing the last 'n' rows.
        """
        if not self.data:
            logging.warning("No data loaded.")
            return []
        return self.data[-n:]
