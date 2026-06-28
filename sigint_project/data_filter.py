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
    print(" 1. Filter by date            2. Filter by time                       3. Filter by emitter\n\n"
          " 4. Filter by frequency       5. Filter by bandwidth                  6. Filter by modulation\n\n"
          " 7. Filter by site            8. Toggle matching or includes          9. Preview results\n\n"
          "10. Build map                11. Remove filter                       12. Clear filters\n\n"
          "13. Quit                     00. Type back or menu to return\n")

    user_input = input('Select an option:  ').lower().strip()

    if user_input in ['1', 'date']:
        while True:
            filter_date = input('Enter date (YYYY-MM-DD):  ')
            if filter_date in ['back', 'menu', 'quit']:
                break
            filtered_df = filtered_df[filtered_df['date'] == pd.Timestamp(filter_date).date()]
            filtered_df, success = cs.stop_filter(sigint_df, filtered_df, 'date', filter_date, filters)
            if success:
                break

    elif user_input in ['2', 'time']:
        while True:
            try:
                filter_time = input('Enter time (HH:MM or HHMM):  ')
                if filter_time in ['back', 'menu', 'quit']:
                    break
                # Auto-format HHMM input to HH:MM
                if len(filter_time) == 4:
                    filter_time = f'{filter_time[0:2]}:{filter_time[2:4]}'
                hour, minute = filter_time.split(":")
                # Validate hour and minute ranges and ensure two-digit formatting
                if int(hour) > 23 or int(minute) > 59 or len(hour) != 2 or len(minute) != 2:
                    raise ValueError
                filtered_df = filtered_df[(filtered_df['hour'] == int(hour)) & (filtered_df['minute'] == int(minute))]
                filtered_df, success = cs.stop_filter_time(sigint_df, filtered_df, hour, minute, filters)
                if success:
                    break
            except ValueError:
                print(f"\nIncorrect time format entered: {hour}:{minute}")


    elif user_input in ['3', 'emitter', 'soi']:
        while True:
            filter_emitter = input('Enter emitter (EMITTER-XXX):  ').upper()
            if filter_emitter in ['back', 'menu', 'quit']:
                break
            if filter_emitter[0:8] != 'EMITTER-':
                    filter_emitter = f'EMITTER-{filter_emitter}'
            filtered_df = filtered_df[filtered_df['source_id'] == filter_emitter]
            filtered_df, success = cs.stop_filter(sigint_df, filtered_df, 'source_id', filter_emitter, filters)
            if success:
                break

    elif user_input in ['4', 'frequency', 'freq']:
        while True:
            filter_frequency = input('Enter frequency (MHz):  ')
            if filter_frequency in ['back', 'menu', 'quit']:
                break
            filtered_df = filtered_df[filtered_df['frequency_mhz']]
            filtered_df, success = cs.stop_filter(sigint_df, filtered_df, 'frequency_mhz', filter_frequency, filters)
            if success:
                break

    elif user_input in ['5', 'bandwidth', 'bw']:
        while True:
            filter_bandwidth = input('Enter bandwidth (KHz):  ')
            if filter_bandwidth in ['back', 'menu', 'quit']:
                break
            filtered_df = filtered_df[filtered_df['bandwidth_khz'] == float(filter_bandwidth)]
            filtered_df, success = cs.stop_filter(sigint_df, filtered_df, 'bandwidth_khz', filter_bandwidth, filters)
            if success:
                break

    elif user_input in ['6', 'mod type', 'modulation', 'mod']:
        while True:
            filter_modulation = input('Enter modulation type:  ').upper()
            if filter_modulation in ['BACK', 'MENU', 'QUIT']:
                break
            filtered_df = filtered_df[filtered_df['modulation'] == filter_modulation]
            filtered_df, success = cs.stop_filter(sigint_df, filtered_df, 'modulation', filter_modulation, filters)
            if success:
                break

    elif user_input in ['7', 'site']:
        while True:
            filter_site = input('Enter site:  ')
            if filter_site in ['back', 'menu', 'quit']:
                break
            filtered_df = filtered_df[filtered_df['site_name'] == filter_site]
            filtered_df, success = cs.stop_filter(sigint_df, filtered_df, 'site_name', filter_site, filters)
            if success:
                break

    elif user_input in ['9', 'preview']:
        print(filtered_df)

    elif user_input in ['10', 'map', 'build map']:
        map_name = input('Enter file name:  ')
        cs.build_map(filtered_df, f'{map_name}')
        print(f'{map_name}.html created')

    elif user_input in ['11', 'remove filter', 'remove']:
        print(filters)
        filter_remove = input("Enter filter to remove:  ")
        if filter_remove in ['back', 'menu', 'quit']:
            continue
        filters.pop(filter_remove)
        filtered_df = sigint_df
        for column, value in filters.items():
            filtered_df = filtered_df[filtered_df[column] == value]

    elif user_input in ['12', 'clear']:
        filters.clear()
        filtered_df = sigint_df

    elif user_input in ['13', 'quit', 'exit', 'close']:
        break