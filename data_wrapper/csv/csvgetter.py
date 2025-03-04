import logging
from .csvloader import CSVLoader
import os
from datetime import datetime

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
        datetime_formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M:%S"]

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
                is_datetime = False
                for fmt in datetime_formats:
                    try:
                        datetime.strptime(v, fmt)
                        types.add("datetime")
                        is_datetime = True
                        break
                    except ValueError:
                        continue
                if not is_datetime:
                    types.add("str")
            elif isinstance(v, datetime):
                types.add("datetime")
            else:
                types.add("object")  # Giá trị không thuộc kiểu nào khác

        if len(types) == 1:
            return types.pop()  # Trả về kiểu dữ liệu duy nhất nếu có
        return types  # Trả về tập hợp kiểu dữ liệu nếu có nhiều loại


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
            CSVColumn: An object that provides functionalities for the column.
        """
        if not self.data:
            logging.warning("No data loaded.")
            return None
        if column_name not in self.data[0]:
            logging.error(f"Column '{column_name}' not found.")
            raise KeyError(f"Column '{column_name}' does not exist.")

        return CSVColumn(self.data, column_name)  # Trả về đối tượng CSVColumn


    def _convert_value(self, value):
        """Convert value to int, float, or keep as string."""
        try:
            return int(value)  # Thử ép kiểu sang integer
        except ValueError:
            try:
                return float(value)  # Nếu không phải int, thử ép kiểu sang float
            except ValueError:
                return value  # Nếu không phải số, giữ nguyên kiểu string

    def get_head(self, n=5):
        """
        Returns the first 'n' rows of the data in a table-like format.
        
        Args:
            n (int, optional): Number of rows to return. Defaults to 5.

        Returns:
            str: A formatted table-like string.
        """
        return self._format_table(self.data[:n])

    def get_tail(self, n=5):
        """
        Returns the last 'n' rows of the data.

        Args:
            n (int, optional): Number of rows to return. Defaults to 5.

        Returns:
            str: A formatted table-like string.
        """
        return self._format_table(self.data[-n:])


    def get_row(self, index):
        """
        Returns a specific row by index in a formatted table.

        Args:
            index (int): The index of the row.

        Returns:
            str: A formatted string representation of the row.
        """
        if not self.data:
            logging.warning("No data loaded.")
            return "No data available."
        if index < 0 or index >= len(self.data):
            logging.error("Row index out of range.")
            return "Invalid index."
        return self._format_table([self.data[index]], f"Row {index}")

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
        if row == "Invalid index." or row == "No data available.":
            return None
        if column_name not in self.data[0]:
            logging.error(f"Column '{column_name}' not found.")
            return None
        return self._convert_value(self.data[row_index][column_name])

    def _format_table(self, rows):
        """
        Helper function to format a list of dictionaries into a table.

        Args:
            rows (list[dict]): The list of dictionaries representing rows.
            title (str): The title for the table.

        Returns:
            str: Formatted table string.
        """
        if not rows:
            return "No data available."

        # Lấy danh sách cột từ dictionary đầu tiên
        headers = list(rows[0].keys())

        # Tính độ rộng tối đa của mỗi cột
        column_widths = {col: max(len(col), *(len(str(row[col])) for row in rows)) for col in headers}

        # Tạo dòng tiêu đề
        header_row = "  ".join(col.ljust(column_widths[col]) for col in headers)
        separator = " ".join(" " * column_widths[col] for col in headers)

        # Tạo dòng dữ liệu
        data_rows = "\n".join("   ".join(str(row[col]).ljust(column_widths[col]) for col in headers) for row in rows)

        # Ghép thành bảng hoàn chỉnh
        table = f"{header_row}\n{separator}\n{data_rows}"
        
        return table
    
    def get_info(self):
        """
        Returns information about the CSV file, including column names, data types, and file size.

        Returns:
            str: A formatted string containing the information.
        """
        if not self.data:
            logging.warning("No data loaded.")
            return "No data available."

        # Lấy thông tin về các cột
        column_info = []
        for column_name in self.data[0].keys():
            column = self[column_name]  # Sử dụng __getitem__ để lấy đối tượng CSVColumn
            dtype = column.get_dtype()  # Lấy kiểu dữ liệu của cột
            column_info.append((column_name, dtype))

        # Lấy dung lượng file
        file_size = self._get_file_size()

        # Định dạng thông tin
        info_str = "CSV File Information:\n"
        info_str += "-" * 50 + "\n"
        info_str += "Columns:\n"

        # Tính độ rộng tối đa của tên cột và kiểu dữ liệu
        max_col_name_width = max(len(col_name) for col_name, _ in column_info)
        max_dtype_width = max(len(str(dtype)) for _, dtype in column_info)

        # Định dạng từng dòng thông tin
        for col_name, col_type in column_info:
            # Căn chỉnh tên cột và kiểu dữ liệu với khoảng cách nhất định
            info_str += f"  {col_name.ljust(max_col_name_width)} : {str(col_type).ljust(max_dtype_width)}\n"

        info_str += "-" * 50 + "\n"
        info_str += f"File Size: {file_size}\n"

        return info_str

    def _get_file_size(self):
        """
        Helper function to get the size of the CSV file.

        Returns:
            str: The file size in a human-readable format.
        """
        if not hasattr(self, 'csv_path') or not self.csv_path:
            return "File size not available (file path not provided)."

        try:
            size_bytes = os.path.getsize(self.csv_path)
            # Chuyển đổi dung lượng sang định dạng dễ đọc (KB, MB, GB)
            if size_bytes < 1024:
                return f"{size_bytes} bytes"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.2f} KB"
            elif size_bytes < 1024 * 1024 * 1024:
                return f"{size_bytes / (1024 * 1024):.2f} MB"
            else:
                return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
        except FileNotFoundError:
            return "File size not available (file not found)."
