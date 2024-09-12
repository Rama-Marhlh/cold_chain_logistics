import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt # type: ignore
import folium # type: ignore
from streamlit_folium import st_folium # type: ignore
from fastkml import kml # type: ignore
from shapely.geometry import shape # type: ignore

# Load data functions (unchanged)
@st.cache_data
def load_room_data(room_number):
    return pd.read_csv(f'room{room_number}.csv')

@st.cache_data
def load_transport_data():
    return pd.read_csv('modified_sensor_data.csv')

@st.cache_data
def load_supermarket_data(file_name):
    return pd.read_csv(file_name)

@st.cache_data
def load_kml():
    k = kml.KML()
    with open('map.kml', 'rb') as f:
        k.from_string(f.read())
    features = list(k.features())
    placemarks = list(features[0].features())
    polygon_geom = placemarks[0].geometry
    shapely_polygon = shape(polygon_geom)
    return shapely_polygon

@st.cache_data
def load_warehouse_data():
    room_files = [f'room{i}.csv' for i in range(1, 5)]
    dfs = [pd.read_csv(file) for file in room_files]
    return pd.concat(dfs)




# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a Page", ["Home", "Transport", "Warehouse", "Supermarket", "City View", "Alerts"])

if page == "Home":
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.title("Cold Chain Logistics Dashboard")
    st.write("Explore the different aspects of the cold chain logistics system.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Transport")
        st.image('https://img.icons8.com/ios/50/000000/truck.png', width=60)
        st.write("Monitor transport data and alerts.")
       # if st.button("Go to Transport"):
        #    st.query_params = {"page": "Transport"}

    with col2:
        st.subheader("Warehouse")
        st.image('https://img.icons8.com/ios/50/000000/home.png', width=60)
        st.write("Track warehouse temperature and alerts.")
       # if st.button("Go to Warehouse"):
        #    st.query_params = {"page": "Warehouse"}

    with col3:
        st.subheader("Supermarket")
        st.image('https://img.icons8.com/ios/50/000000/building.png', width=60)
        st.write("Check supermarket room conditions.")
        #if st.button("Go to Supermarket"):
         #   st.query_params = {"page": "Supermarket"}

    col4, col5 = st.columns(2)

    with col4:
        st.subheader("City View")
        st.image('https://img.icons8.com/ios/50/000000/map-pin.png', width=60)
        st.write("View city maps with geographical constraints.")
        #if st.button("Go to City View"):
         #   st.query_params = {"page": "City View"}

    with col5:
        st.subheader("Alerts")
        st.image('https://img.icons8.com/ios/50/000000/bell.png', width=60)
        st.write("View recent alerts across all categories.")
       # if st.button("Go to Alerts"):
        #    st.query_params = {"page": "Alerts"}

    st.markdown('</div>', unsafe_allow_html=True)



elif page == "City View":
    st.write("### City View Map")
    shapely_polygon = load_kml()
    bounds = shapely_polygon.bounds
    center_lat = (bounds[1] + bounds[3]) / 2
    center_lon = (bounds[0] + bounds[2]) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    folium.Polygon(
        locations=[[point[1], point[0]] for point in shapely_polygon.exterior.coords],
        color='blue', fill=True, fill_opacity=0.3
    ).add_to(m)
    st_folium(m)

elif page == "Transport":
    st.write("### Transport Data")
    
    # Load the data
    df_transport = load_transport_data()
    
    if not df_transport.empty:
        # Plot temperature data for individual sensors
        st.write("#### Temperature Data for Individual Sensors")
        sensors = df_transport['SensorID'].unique()
        for sensor_id in sensors:
            sensor_data = df_transport[df_transport['SensorID'] == sensor_id]
            st.write(f"##### Sensor ID: {sensor_id}")
            st.line_chart(sensor_data[['Timestamp', 'Temperature']].set_index('Timestamp'))
        
       
        # Plot average temperature for each sensor
        st.write("#### Average Temperature for Each Sensor")
        avg_temps = df_transport.groupby('SensorID')['Temperature'].mean().reset_index()
        avg_temps = avg_temps.sort_values(by='Temperature', ascending=False)
        st.bar_chart(avg_temps.set_index('SensorID'))

         # Display recent events with descriptions
        st.write("### Recent Events")
        recent_events = df_transport[['Event', 'Timestamp', 'Temperature']].drop_duplicates().sort_values(by='Timestamp', ascending=False)
        recent_events = recent_events[recent_events['Event'] != 'Normal']  # Filter out 'Normal' events
        st.write(recent_events.head(20))  # Display recent 20 events

        
        # Calculate and plot average temperature across all sensors
        st.write("#### Overall Truck Behavior")
        avg_temp_per_time = df_transport.groupby('Timestamp')['Temperature'].mean().reset_index()
        avg_temp_per_time['Timestamp'] = pd.to_datetime(avg_temp_per_time['Timestamp'])  # Ensure timestamp is datetime type
        st.line_chart(avg_temp_per_time.set_index('Timestamp')['Temperature'])
        
    else:
        st.write("No data available. Please go back and load data.")

elif page == "Warehouse":
    st.write("### Warehouse Monitoring")
    
    # Room selection
    room_selection = st.selectbox("Select Room", ['Room 1', 'Room 2', 'Room 3', 'Room 4'])
    room_number = int(room_selection.split()[1])
    
    # Load data for the selected room
    df_room = load_room_data(room_number)
    
    if not df_room.empty:
        st.write(f"#### Temperature Data for {room_selection}")
        
        # Line plots for each sensor
        sensors = df_room['SensorID'].unique()
        for sensor_id in sensors:
            sensor_data = df_room[df_room['SensorID'] == sensor_id]
            st.write(f"##### Sensor ID: {sensor_id}")
            st.line_chart(sensor_data[['Timestamp', 'Temperature']].set_index('Timestamp'))
        
         
        
        # Plot average temperature for each sensor
        st.write(f"#### Average Temperature for Sensors in {room_selection}")
        avg_temps = df_room.groupby('SensorID')['Temperature'].mean().reset_index()
        avg_temps = avg_temps.sort_values(by='Temperature', ascending=False)
        st.bar_chart(avg_temps.set_index('SensorID'))
        
        # Display recent events for the selected room
        st.write(f"### Recent Events in {room_selection}")
        recent_events = df_room[['Event', 'Timestamp', 'Temperature']].drop_duplicates().sort_values(by='Timestamp', ascending=False)
        recent_events = recent_events[recent_events['Event'] != 'Normal']  # Filter out 'Normal' events
        st.write(recent_events.head(10))  # Display recent 10 events
        
        # Calculate and display overall average temperature for the room
        avg_temp_room = df_room.groupby('Timestamp')['Temperature'].mean().reset_index()
        avg_temp_room['Timestamp'] = pd.to_datetime(avg_temp_room['Timestamp'])
        st.write(f"#### Overall Average Temperature in {room_selection}")
        st.line_chart(avg_temp_room.set_index('Timestamp')['Temperature'])

       
    else:
        st.write("No data available for the selected room.")

    # Calculate and plot average temperature across all rooms
    st.write("#### Overall Temperature Across the Building")
    
    # Load data for all rooms
    df_all_rooms = pd.concat([load_room_data(i) for i in range(1, 5)])
    
    if not df_all_rooms.empty:
        avg_temp_building = df_all_rooms.groupby('Timestamp')['Temperature'].mean().reset_index()
        avg_temp_building['Timestamp'] = pd.to_datetime(avg_temp_building['Timestamp'])
        
        # Line plot for overall building temperature
        st.line_chart(avg_temp_building.set_index('Timestamp')['Temperature'])
    else:
        st.write("No data available for the entire building.")

elif page == "Supermarket":
    st.write("### Supermarket Data")

    # Supermarkets and Rooms mapping
    supermarket_options = {
        "Supermarket 1": {"Room 1": "sm1room1.csv", "Room 2": "sm1room2.csv"},
        "Supermarket 2": {"Room 1": "sm2room1.csv", "Room 2": "sm2room2.csv"}
    }

    selected_supermarket = st.selectbox("Select Supermarket", list(supermarket_options.keys()))
    rooms = supermarket_options[selected_supermarket]
    selected_room = st.selectbox("Select Room", list(rooms.keys()))

    # Load the data for the selected room
    df_supermarket = load_supermarket_data(rooms[selected_room])

    if not df_supermarket.empty:
        # Plot temperature data for individual sensors
        st.write(f"#### Temperature Data for {selected_room} in {selected_supermarket}")
        sensors = df_supermarket['SensorID'].unique()
        for sensor_id in sensors:
            sensor_data = df_supermarket[df_supermarket['SensorID'] == sensor_id]
            st.write(f"##### Sensor ID: {sensor_id}")
            st.line_chart(sensor_data[['Timestamp', 'Temperature']].set_index('Timestamp'))

        # Plot average temperature for each sensor in the room
        st.write(f"#### Average Temperature for Each Sensor in {selected_room}")
        avg_temp_per_sensor = df_supermarket.groupby('SensorID')['Temperature'].mean().reset_index()
        avg_temp_per_sensor = avg_temp_per_sensor.sort_values(by='Temperature', ascending=False)
        st.bar_chart(avg_temp_per_sensor.set_index('SensorID'))

         # Display recent events
        st.write("### Recent Events")
        recent_events = df_supermarket[['Event', 'Timestamp', 'Temperature']].drop_duplicates().sort_values(by='Timestamp', ascending=False)
        recent_events = recent_events[recent_events['Event'] != 'Normal']  # Filter out 'Normal' events
        st.write(recent_events.head(20))  # Display recent 20 events

        # Calculate and display overall average temperature for the room
        avg_temp_in_room = df_supermarket.groupby('Timestamp')['Temperature'].mean().reset_index()
        avg_temp_in_room['Timestamp'] = pd.to_datetime(avg_temp_in_room['Timestamp'])
        st.write(f"#### Overall Average Temperature in {selected_room}")
        st.line_chart(avg_temp_in_room.set_index('Timestamp')['Temperature'])

        # Calculate and display overall average temperature for the supermarket (all rooms)
        st.write(f"#### Overall Average Temperature in {selected_supermarket}")
        combined_df = pd.concat([load_supermarket_data(rooms[room]) for room in rooms])
        avg_temp_supermarket = combined_df.groupby('Timestamp')['Temperature'].mean().reset_index()
        avg_temp_supermarket['Timestamp'] = pd.to_datetime(avg_temp_supermarket['Timestamp'])
        st.line_chart(avg_temp_supermarket.set_index('Timestamp')['Temperature'])


       

    else:
        st.write("No data available for the selected room.")

elif page == "Alerts":
    st.write("### Alerts")

    # Define options for selection
    alert_options = {
        "Warehouse": [f"Room {i}" for i in range(1, 5)],
        "Supermarket 1": ["Room 1", "Room 2"],
        "Supermarket 2": ["Room 1", "Room 2"],
        "Transportation": ["All"]
    }

    # User selection
    selected_category = st.selectbox("Select Category", list(alert_options.keys()))
    selected_room = st.selectbox("Select Room", alert_options[selected_category])

    # Load data based on selection
    if selected_category == "Warehouse":
        room_number = int(selected_room.split()[1])
        df_room = load_room_data(room_number)
        if not df_room.empty:
            st.write(f"#### Alerts for {selected_room}")
            room_events = df_room[['Event', 'Timestamp', 'Temperature']]
            room_events = room_events[room_events['Event'] != 'Normal']
            room_events = room_events.sort_values(by='Timestamp', ascending=False)
            st.write(room_events.head(10))  # Display recent 10 alerts for the selected room
        else:
            st.write(f"No data available for {selected_room}.")

    elif selected_category == "Supermarket 1":
        supermarket_file = "sm1room1.csv" if selected_room == "Room 1" else "sm1room2.csv"
        df_room = load_supermarket_data(supermarket_file)
        if not df_room.empty:
            st.write(f"#### Alerts for {selected_room} in {selected_category}")
            room_events = df_room[['Event', 'Timestamp', 'Temperature']]
            room_events = room_events[room_events['Event'] != 'Normal']
            room_events = room_events.sort_values(by='Timestamp', ascending=False)
            st.write(room_events.head(10))  # Display recent 10 alerts for the selected room
        else:
            st.write(f"No data available for {selected_room} in {selected_category}.")

    elif selected_category == "Supermarket 2":
        supermarket_file = "sm2room1.csv" if selected_room == "Room 1" else "sm2room2.csv"
        df_room = load_supermarket_data(supermarket_file)
        if not df_room.empty:
            st.write(f"#### Alerts for {selected_room} in {selected_category}")
            room_events = df_room[['Event', 'Timestamp', 'Temperature']]
            room_events = room_events[room_events['Event'] != 'Normal']
            room_events = room_events.sort_values(by='Timestamp', ascending=False)
            st.write(room_events.head(10))  # Display recent 10 alerts for the selected room
        else:
            st.write(f"No data available for {selected_room} in {selected_category}.")

    elif selected_category == "Transportation":
        df_transport = load_transport_data()
        if not df_transport.empty:
            st.write("#### Alerts for Transportation")
            transport_events = df_transport[['Event', 'Timestamp', 'Temperature']]
            transport_events = transport_events[transport_events['Event'] != 'Normal']
            transport_events = transport_events.sort_values(by='Timestamp', ascending=False)
            st.write(transport_events.head(20))  # Display recent 20 alerts for transportation
        else:
            st.write("No data available for transportation.")