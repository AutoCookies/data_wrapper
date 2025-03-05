from .csvaggregator import CSVAggregator
import logging

class CSVInteractor (CSVAggregator):
    
    def drop_columns(self, columns_to_drop: list):
        """
        Drops specified columns from the CSV data.

        Args:
            columns_to_drop (list): A list of column names to drop.
        """
        if not isinstance(columns_to_drop, list):
            logging.error("columns_to_drop must be a list.")
            return

        # Kiểm tra xem các cột cần xóa có tồn tại không
        for column in columns_to_drop:
            if column not in self.columns:
                logging.warning(f"Column '{column}' not found. Skipping.")
                continue

        # Xóa các cột khỏi dữ liệu
        for row in self.data:
            for column in columns_to_drop:
                if column in row:
                    del row[column]

        # Cập nhật danh sách cột
        self.columns = [col for col in self.columns if col not in columns_to_drop]
        logging.info(f"Dropped columns: {columns_to_drop}")
    
    def join(self, other_csv, on_column, how="inner"):
        """
        Joins the current CSV data with another CSV based on a common column.

        Args:
            other_csv (CSVInteractor): Another CSVInteractor instance.
            on_column (str): The column to join on.
            how (str): The type of join. Options: "inner", "left", "right", "outer".

        Returns:
            list: A list of joined rows.
        """
        if on_column not in self.columns or on_column not in other_csv.columns:
            logging.error(f"Column '{on_column}' not found in one or both CSVs.")
            return []

        # Tạo bản đồ dữ liệu từ other_csv để tối ưu hóa việc tìm kiếm
        other_data_map = {}
        for row in other_csv.data:
            key = row[on_column]
            if key not in other_data_map:
                other_data_map[key] = []
            other_data_map[key].append(row)

        joined_data = []
        for row in self.data:
            key = row[on_column]
            if key in other_data_map:
                for other_row in other_data_map[key]:
                    joined_row = {**row, **other_row}
                    joined_data.append(joined_row)
            elif how in ["left", "outer"]:
                joined_row = {**row}
                joined_data.append(joined_row)

        if how in ["right", "outer"]:
            for row in other_csv.data:
                key = row[on_column]
                if key not in other_data_map:
                    joined_row = {**row}
                    joined_data.append(joined_row)

        logging.info(f"Joined data using '{how}' join on column '{on_column}'.")
        return joined_data

    def group_by(self, group_column, aggregate_column=None, agg_func="count"):
        """
        Groups data by a column and applies an aggregate function.

        Args:
            group_column (str): The column to group by.
            aggregate_column (str, optional): The column to apply the aggregate function on.
            agg_func (str): The aggregate function to apply. Options: "count", "sum", "mean", "min", "max".

        Returns:
            dict: A dictionary with grouped results.
        """
        if group_column not in self.columns:
            logging.error(f"Column '{group_column}' not found.")
            return {}

        if aggregate_column and aggregate_column not in self.columns:
            logging.error(f"Column '{aggregate_column}' not found.")
            return {}

        grouped_data = {}
        for row in self.data:
            key = row[group_column]
            if key not in grouped_data:
                grouped_data[key] = []

            grouped_data[key].append(row)

        result = {}
        for key, group in grouped_data.items():
            if agg_func == "count":
                result[key] = len(group)
            elif agg_func == "sum":
                result[key] = sum(float(row[aggregate_column]) for row in group)
            elif agg_func == "mean":
                values = [float(row[aggregate_column]) for row in group]
                result[key] = sum(values) / len(values) if values else 0
            elif agg_func == "min":
                result[key] = min(float(row[aggregate_column]) for row in group)
            elif agg_func == "max":
                result[key] = max(float(row[aggregate_column]) for row in group)
            else:
                logging.error("Invalid aggregate function.")
                return {}

        logging.info(f"Grouped data by '{group_column}' with '{agg_func}' function.")
        return result
    
    def reshape(self, id_vars, value_vars, var_name="variable", value_name="value"):
        """
        Reshapes the CSV data from wide to long format.

        Args:
            id_vars (list): Columns to use as identifier variables.
            value_vars (list): Columns to unpivot (reshape) into a single column.
            var_name (str): Name of the new column that will contain the variable names.
            value_name (str): Name of the new column that will contain the values.

        Returns:
            list: A list of reshaped rows.
        """
        if not isinstance(id_vars, list) or not isinstance(value_vars, list):
            logging.error("id_vars and value_vars must be lists.")
            return []
        
        if not id_vars or len(id_vars) == 0:
            logging.error("require id_vars but got empty")
        else:
            logging.error("Require value_vars but got empty")

        # Kiểm tra xem các cột có tồn tại không
        for col in id_vars + value_vars:
            if col not in self.columns:
                logging.error(f"Column '{col}' not found.")
                return []

        reshaped_data = []
        for row in self.data:
            for value_col in value_vars:
                reshaped_row = {col: row[col] for col in id_vars}
                reshaped_row[var_name] = value_col
                reshaped_row[value_name] = row[value_col]
                reshaped_data.append(reshaped_row)

        # Cập nhật danh sách cột
        self.columns = id_vars + [var_name, value_name]
        self.data = reshaped_data

        logging.info(f"Reshaped data from wide to long format.")
        return reshaped_data