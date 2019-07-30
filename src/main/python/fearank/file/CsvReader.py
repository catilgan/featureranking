import pandas as pd


class CsvReader:

    @staticmethod
    def read_csv(file_name, cols):
        if -1 in cols:
            CsvReader.get_max_column_range(cols, file_name)

        data = pd.read_csv(file_name, usecols=cols)

        return data

    @staticmethod
    def get_max_column_range(cols, file_name):
        first_row = pd.read_csv(file_name, nrows=1)
        max_cols = len(first_row.columns)
        cols.remove(-1)
        last = cols[-1]

        if last < max_cols:
            cols.extend(list(range(last, max_cols)))
