import pandas as pd
import collection_sites as cs

sigint_df = pd.read_csv('sigint_sample.csv')
sigint_df['timestamp'] = pd.to_datetime(sigint_df['timestamp'])
sigint_df['date'] = sigint_df['timestamp'].dt.date
sigint_df['hour'] = sigint_df['timestamp'].dt.hour
sigint_df['minute'] = sigint_df['timestamp'].dt.minute

cs.signal_power(sigint_df)

pd.set_option('display.max_columns', None)

filters = {}
filtered_df = sigint_df
while True:
    cs.print_filtered(filtered_df, filters)
    print("1. Filter by date            2. Filter by time                       3. Filter by emitter\n\n"
          "4. Filter by frequency       5. Filter by bandwidth                  6. Filter by modulation\n\n"
          "7. Filter by site            8. Toggle matching or includes          9. Preview results\n\n"
          "10. Build map                11. Remove filter                       12. Clear filters\n\n"
          "13. Quit\n")

    user_input = input('Select an option:  ').lower().strip()

    if user_input in ['1', 'date']:
        filter_date = input('Enter date (YYYY-MM-DD):  ')
        filtered_df = filtered_df[filtered_df['date'] == pd.Timestamp(filter_date).date()]
        filters['date'] = filter_date


    elif user_input in ['2', 'time']:
        while True:
            try:
                filter_time = input('Enter time (HH:MM or HHMM):  ')
                if filter_time in ['back', 'menu']:
                    break
                # Auto-format HHMM input to HH:MM
                elif len(filter_time) == 4:
                    filter_time = f'{filter_time[0:2]}:{filter_time[2:4]}'
                hour, minute = filter_time.split(":")
                # Validate hour and minute ranges and ensure two-digit formatting
                if int(hour) > 23 or int(minute) > 59 or len(hour) != 2 or len(minute) != 2:
                    raise ValueError
                filtered_df = filtered_df[(filtered_df['hour'] == int(hour)) & (filtered_df['minute'] == int(minute))]
                filtered_df = cs.stop_filter(sigint_df, filtered_df, 'time', filter_time, filters)
                break
            except ValueError:
                print(f"\nIncorrect time format entered: {filter_time}")


    elif user_input in ['3', 'emitter', 'soi']:
        filter_emitter = input('Enter emitter (EMITTER-XXX):  ').upper()
        if filter_emitter[0:8] != 'EMITTER-':
                filter_emitter = f'EMITTER-{filter_emitter}'
        filtered_df = filtered_df[filtered_df['source_id'] == filter_emitter]
        filters['source_id'] = filter_emitter

    elif user_input in ['4', 'frequency', 'freq']:
        filter_frequency = input('Enter frequency (MHz):  ')
        filtered_df = filtered_df[filtered_df['frequency_mhz']]
        filters['frequency_mhz'] = filter_frequency

    elif user_input in ['5', 'bandwidth', 'bw']:
        filter_bandwidth = input('Enter bandwidth (KHz):  ')
        filtered_df = filtered_df[filtered_df['bandwidth_khz'] == filter_bandwidth]
        filters['bandwidth_khz'] = filter_bandwidth

    elif user_input in ['6', 'mod type', 'modulation', 'mod']:
        filter_modulation = input('Enter modulation type:  ').upper()
        filtered_df = filtered_df[filtered_df['modulation'] == filter_modulation]
        filters['modulation'] = filter_modulation

    elif user_input in ['7', 'site']:
        filter_site = input('Enter site:  ')
        filtered_df = filtered_df[filtered_df['site_name'] == filter_site]
        filters['site_name'] = filter_site

    elif user_input in ['8', 'preview']:
        print(filtered_df)

    elif user_input in ['9', 'map', 'build map']:
        map_name = input('Enter file name:  ')
        cs.build_map(filtered_df, f'{map_name}')
        print(f'{map_name}.html created')

    elif user_input in ['10', 'remove filter', 'remove']:
        print(filters)
        filters.pop(input("Enter filter to remove:  ").strip().lower())
        filtered_df = sigint_df
        for column, value in filters.items():
            filtered_df = filtered_df[filtered_df[column] == value]

    elif user_input in ['12', 'clear']:
        filters.clear()
        filtered_df = sigint_df

    elif user_input in ['13', 'quit', 'exit', 'close']:
        break