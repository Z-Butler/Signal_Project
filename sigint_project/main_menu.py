import pandas as pd
import map_builder as mb
from data_filter import DataFilter

sigint_df = pd.read_csv('sigint_sample.csv')
sigint_df['timestamp'] = pd.to_datetime(sigint_df['timestamp'])
sigint_df['date'] = sigint_df['timestamp'].dt.date
sigint_df['hour'] = sigint_df['timestamp'].dt.hour
sigint_df['minute'] = sigint_df['timestamp'].dt.minute

mb.signal_power(sigint_df)

pd.set_option('display.max_columns', None)
return_to_menu = ['back', 'menu', 'quit', 'return']

filters = {}
data_filter = DataFilter(sigint_df)

while True:
    data_filter.print_filtered()
    print(" 1. Filter by date            2. Filter by time                       3. Filter by emitter\n\n"
          " 4. Filter by frequency       5. Filter by bandwidth                  6. Filter by modulation\n\n"
          " 7. Filter by site            8. Toggle matching or includes          9. Preview results\n\n"
          "10. Build map                11. Remove filter                       12. Clear filters\n\n"
          "13. Quit                     00. Type back or menu to return\n")

    user_input = input('Select an option:  ').lower().strip()

    if user_input in ['1', 'date']:
        while True:
            filter_date = input('Enter date (YYYY-MM-DD):  ')
            if filter_date in return_to_menu:
                break
            success = data_filter.date_filter('date', filter_date)
            if success:
                break

    elif user_input in ['2', 'time']:
        while True:
            try:
                filter_time = input('Enter time (HH:MM or HHMM):  ')
                if filter_time in return_to_menu:
                    break
                # Auto-format HHMM input to HH:MM
                if len(filter_time) == 4:
                    filter_time = f'{filter_time[0:2]}:{filter_time[2:4]}'
                hour, minute = filter_time.split(":")
                # Validate hour and minute ranges and ensure two-digit formatting
                if int(hour) > 23 or int(minute) > 59 or len(hour) != 2 or len(minute) != 2:
                    raise ValueError
                success = data_filter.time_filter(int(hour), int(minute))
                if success:
                    break
            except ValueError:
                print(f"\nIncorrect time format entered: {filter_time}")


    elif user_input in ['3', 'emitter', 'soi']:
        while True:
            filter_emitter = input('Enter emitter (EMITTER-XXX):  ').upper()
            if filter_emitter in ['BACK', 'MENU', 'QUIT', 'RETURN']:
                break
            elif filter_emitter[0:8] != 'EMITTER-':
                filter_emitter = f'EMITTER-{filter_emitter}'
            success = data_filter.input_filter('source_id', filter_emitter)
            if success:
                break

    elif user_input in ['4', 'frequency', 'freq']:
        while True:
            filter_frequency = input('Enter frequency (MHz):  ')
            if filter_frequency in return_to_menu:
                break
            success = data_filter.input_filter('frequency_mhz', float(filter_frequency))
            if success:
                break

    elif user_input in ['5', 'bandwidth', 'bw']:
        while True:
            filter_bandwidth = input('Enter bandwidth (KHz):  ')
            if filter_bandwidth in return_to_menu:
                break
            success = data_filter.input_filter('bandwidth_khz', float(filter_bandwidth))
            if success:
                break

    elif user_input in ['6', 'mod type', 'modulation', 'mod']:
        while True:
            filter_modulation = input('Enter modulation type:  ').upper()
            if filter_modulation in ['BACK', 'MENU', 'QUIT', 'RETURN']:
                break
            success = data_filter.input_filter('modulation', filter_modulation)
            if success:
                break

    elif user_input in ['7', 'site']:
        while True:
            filter_site = input('Enter site:  ')
            if filter_site in return_to_menu:
                break
            success = data_filter.input_filter('site_name', filter_site)
            if success:
                break

    # elif user_input in ['8', 'include', 'match']:
    #     if 'matching' in filters and 'includes' not in filters:
    #         confirm = input('Do you want to switch to includes? Y/N:    ').lower()
    #         if confirm in ['no', 'n']:
    #             break
    #         if confirm in ['yes', 'y']:
    #             df.toggle_mi(filters, 'includes')

    elif user_input in ['9', 'preview']:
        print(data_filter.filtered_dataframe)

    elif user_input in ['10', 'map', 'build map']:
        map_name = input('Enter file name:  ')
        mb.build_map(data_filter.filtered_dataframe, f'{map_name}')
        print(f'{map_name}.html created')

    elif user_input in ['11', 'remove filter', 'remove']:
        print(data_filter.filters)
        filter_remove = input("Enter filter to remove:  ")
        if filter_remove in return_to_menu:
            continue
        data_filter.remove_filter(filter_remove)

    elif user_input in ['12', 'clear']:
        data_filter.clear_filter()

    elif user_input in ['13', 'quit', 'exit', 'close']:
        break