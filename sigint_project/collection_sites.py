import numpy as np
import pandas as pd
import folium
from folium import plugins
import folium.plugins as fp
import geopy as gp
from geopy.distance import distance

def signal_power(data_frame):
    """                     ESTIMATED TX POWER AND DISTANCE CALCULATIONS
                            REQUIRES DATAFRAME                     """
    # Sample dictionary for assigning transmit power to a modulation type.
    mod_tx_power = {'CW': 52, 'AM': 66, 'FM': 43, 'FSK': 45, 'PSK': 38, 'QAM': 35}

    # Assigning transmit power dictionary to modulation column in sigint dataframe
    data_frame['tx_power_dbm'] = data_frame['modulation'].map(mod_tx_power)

    # Equation for calculating free space path loss. transmit power(dbm) - receive power(dbm)
    path_loss_db = data_frame['tx_power_dbm'] - data_frame['signal_strength_dbm']

    # Equation for finding estimated distance of collected signal.
    distance_km = 10 ** ((path_loss_db - 20 * np.log10(data_frame['frequency_mhz']) - 32.44) / 20)

    # Creating a new column in sigint dataframe for estimated distance.
    data_frame['estimated_distance_km'] = distance_km + 1000


def build_map(data_frame, output_file = 'signal_map') -> None:
    """                 Takes filtered signal data from a CSV file and adds:
                        Collection Sites, Lines of bearing, and DF ellipses.                    """
    # MAP CREATION AND PLUGIN CONFIGURATION
    collection_map = folium.Map([39, -77], zoom_start = 12, control_scale = True,
                            tiles= 'https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/'
                                   'MapServer/tile/{z}/{y}/{x}',
                            attr='Tiles &copy; Esri &mdash; National Geographic, Esri, DeLorme, NAVTEQ, UNEP-WCMC, '
                                 'USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, iPC',
                            max_zoom = 16
)

    # Adds search function to map.
    folium.plugins.Geocoder().add_to(collection_map)

    # Adds measuring tool
    collection_map.add_child(fp.MeasureControl())

    # Adds minimap and makes it collapsible
    fp.MiniMap(toggle_display = True).add_to(collection_map)

    # Adds coordinates on mouse position
    fp.MousePosition().add_to(collection_map)

    #                       MARKER CREATION AND PLOTTING
    # Pulling latitude, longitude, and site name from signal DataFrame and
    # removes duplicates so hundreds of markers aren't created.
    coordinates_df = data_frame[['collection_lat', 'collection_lon', 'site_name']].drop_duplicates()

    # Create site number variable to track number of sites in marker loop.
    site_number = 0

    # MARKER LOOP: creates collection site markers from coordinates DataFrame and
    # labels them with their corresponding site names.
    categories = ['Bearings']
    fp.TagFilterButton(categories).add_to(collection_map)

    for index, row in coordinates_df.iterrows():
        site_number = site_number + 1
        folium.Marker(
            location = [row['collection_lat'], row['collection_lon']],
            tooltip = f'Site {row['site_name'].split(',')[0]}', # [0] Pulls city name from site_name
            popup = f'{row['site_name']}'
        ).add_to(collection_map)

    #                       ESTIMATED TX POWER AND DISTANCE CALCULATIONS
    signal_power(data_frame)

    #                       CREATING BEARING LINE
    for index, row in data_frame.iterrows():
        start = gp.Point(row['collection_lat'], row['collection_lon'])
        end = distance(kilometers = row['estimated_distance_km']).destination(start, bearing = row['bearing_deg'])
        folium.PolyLine(locations = [[row['collection_lat'], row['collection_lon']], [end.latitude, end.longitude]],
                        color = '#FF0000',
                        weight = 3,
                        tags = ['Bearings']
                        ).add_to(collection_map)

    # Saves map
    collection_map.save(f'{output_file}.html')
if __name__ == "__main__":
    sigint_df = pd.read_csv('sigint_sample.csv')
    build_map(sigint_df)

def print_filtered(filtered_df, filters):
    emitters = ", ".join(sorted(filtered_df['source_id'].unique()))
    modulation = ", ".join(sorted(filtered_df['modulation'].unique()))
    sites = ", ".join(sorted(filtered_df['site_name'].unique()))
    print(f"""
{'=' * 45}
  Rows:         {len(filtered_df)}
  Emitters:     {emitters}
  Modulation:   {modulation}
  Site:         {sites}
  Filters:      {', '.join(filters.values()) if filters else 'None'}
{'=' * 45}""")


def stop_filter(original_dataframe, filtered_dataframe, filtered_column, filter_var, filter_dict):
    """         Stops filter from applying if 0 matches are found.          """
    if len(filtered_dataframe) == 0:
        while True:
            print(f"No matching results for {filter_var}")
            filtered_dataframe = original_dataframe
            for column, value in filter_dict.items():
                filtered_dataframe = filtered_dataframe[filtered_dataframe[column] == value]
            return filtered_dataframe
    else:
        filter_dict[filtered_column] = filter_var
        return filtered_dataframe


def stop_filter_time(original_dataframe, filtered_dataframe, filter_hour, filter_min, filter_dict):
    """         Special function for time.
                Stops filter from applying if 0 matches are found.          """
    if len(filtered_dataframe) == 0:
        print(f"\nNo matching results for {filter_hour}{filter_min}")
        filtered_dataframe = original_dataframe
        for column, value in filter_dict.items():
            filtered_dataframe = filtered_dataframe[(filtered_dataframe['hour'] == int(filter_hour)) &
                                                    (filtered_dataframe['minute'] == int(filter_min))]
        return filtered_dataframe, False
    else:
        filter_dict['time'] = f'{filter_hour}{filter_min}'
        return filtered_dataframe, True
