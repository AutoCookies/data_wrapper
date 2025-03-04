from .csvfilter import CSVFilter

class CSVAggregator(CSVFilter):
    """
    Class extending CSVGetter to perform aggregation on numeric columns.
    """

    def sum(self, column_name):
        """Calculate sum of a numeric column."""
        values = self[column_name].get_values()
        return sum(v for v in values if isinstance(v, (int, float)))

    def mean(self, column_name):
        """Calculate mean of a numeric column."""
        values = self[column_name].get_values()
        numeric_values = [v for v in values if isinstance(v, (int, float))]
        return sum(numeric_values) / len(numeric_values) if numeric_values else None

    def min(self, column_name):
        """Find minimum value in a numeric column."""
        values = self[column_name].get_values()
        numeric_values = [v for v in values if isinstance(v, (int, float))]
        return min(numeric_values) if numeric_values else None

    def max(self, column_name):
        """Find maximum value in a numeric column."""
        values = self[column_name].get_values()
        numeric_values = [v for v in values if isinstance(v, (int, float))]
        return max(numeric_values) if numeric_values else None
