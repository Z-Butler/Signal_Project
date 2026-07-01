import pandas as pd

class DataFilter:
    def __init__(self, original_dataframe):
        self.original_dataframe = original_dataframe
        self.filtered_dataframe = original_dataframe
        self.filters = {}

    def print_filtered(self):
        """         Prints filters and matching parameters          """
        emitters = ", ".join(sorted(self.filtered_dataframe['source_id'].unique()))
        modulation = ", ".join(sorted(self.filtered_dataframe['modulation'].unique()))
        sites = ", ".join(sorted(self.filtered_dataframe['site_name'].unique()))
        print(f"""
        {'=' * 45}
          Rows:         {len(self.filtered_dataframe)}
          Emitters:     {emitters}
          Modulation:   {modulation}
          Site:         {sites}
          Filters:      {f', '.join(self.filters.values()) if self.filters else 'None'}
        {'=' * 45}""")

    def stop_filter(self, filtered_column, filter_variable):
        """         Stops filter from applying if 0 matches are found.           """
        if len(self.filtered_dataframe) == 0:
            print(f"\nNo matching results found for {filter_variable}")
            self.filtered_dataframe = self.original_dataframe
            for column, value in self.filters.items():
                self.filtered_dataframe = self.filtered_dataframe[self.filtered_dataframe[column] == value]
            return False
        else:
            self.filters[filtered_column] = filter_variable
            return True

    def stop_filter_time(self, filter_hour, filter_minute):
        """         Special function for time. Stops filter from applying if 0 matches are found           """
        if len(self.filtered_dataframe) == 0:
            print(f"\nNo matching results found for {filter_hour}{filter_minute}")
            self.filtered_dataframe = self.original_dataframe
            for column, value in self.filters.items():
                self.filtered_dataframe = self.filtered_dataframe[self.filtered_dataframe[column] == value]
            return False
        else:
            self.filters['time'] = f'{filter_hour}{filter_minute}'
            return True

    def date_filter(self, filter_column, filter_date: str):
        self.filtered_dataframe = self.filtered_dataframe[self.filtered_dataframe[filter_column] == pd.Timestamp(filter_date).date()]
        success = self.stop_filter(filter_column, filter_date)
        return success

    def time_filter(self, filter_hour, filter_minute):
        self.filtered_dataframe = self.filtered_dataframe[(self.filtered_dataframe['hour'] == filter_hour) &
                                                          (self.filtered_dataframe['minute'] == filter_minute)]
        success = self.stop_filter_time(filter_hour, filter_minute)
        return success

    def input_filter(self, filter_column, filter_variable):
        self.filtered_dataframe = self.filtered_dataframe[self.filtered_dataframe[filter_column] == filter_variable]
        success = self.stop_filter(filter_column, str(filter_variable))
        return success

    def clear_filter(self):
        self.filters.clear()
        self.filtered_dataframe = self.original_dataframe

    def remove_filter(self, filter_variable):
        self.filters.pop(filter_variable)
        self.filtered_dataframe = self.original_dataframe
        for column, value in self.filters.items():
            self.filtered_dataframe = self.filtered_dataframe[self.filtered_dataframe[column] == value]