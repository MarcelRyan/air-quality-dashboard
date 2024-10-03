import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

air_quality = pd.read_csv('all_data.csv')
air_quality['datetime'] = pd.to_datetime(air_quality['datetime'])

# Sidebar for date range filter
st.sidebar.header("Filter")

min_date = air_quality['datetime'].min()
max_date = air_quality['datetime'].max()

with st.sidebar:
    start_date, end_date = st.date_input(
            label='Date range',min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )

# Convert start_date and end_date to datetime64[ns]
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data based on selected date range
filtered_data = air_quality[(air_quality['datetime'] >= start_date) & (air_quality['datetime'] <= end_date)]

# Sidebar for selecting pollutants
selected_pollutants = st.sidebar.multiselect(
    "Select Pollutants",
    options=["PM2.5", "PM10", "CO", "SO2", "NO2", "O3"],
    default=["PM2.5", "PM10"]
)

st.header("Air Quality Dashboard")

# Display selected date range
st.write(f"Displaying data from **{start_date}** to **{end_date}**.")

# Statistics values
st.subheader("Statistic values of data")

col1, col2, col3 = st.columns(3)

with col1:
    total_rows = len(filtered_data)
    st.metric("Total Data", value=total_rows)
    
with col2:
    average_PM2point5 = filtered_data['PM2.5'].mean()
    st.metric("Average PM2.5", value=f"{average_PM2point5:.2f}")

with col3:
    average_PM10 = filtered_data['PM10'].mean()
    st.metric("Average PM10", value=f"{average_PM10:.2f}")
    

col1, col2, col3 = st.columns(3)

with col1:
    average_SO2 = filtered_data['SO2'].mean()
    st.metric("Average SO2", value=f"{average_SO2:.2f}")
    
with col2:
    average_NO2 = filtered_data['NO2'].mean()
    st.metric("Average NO2", value=f"{average_NO2:.2f}")

with col3:
    average_CO = filtered_data['CO'].mean()
    st.metric("Average CO", value=f"{average_CO:.2f}")
    
sns.set_theme(style="whitegrid")

columns_to_plot = ['PM2.5', "PM10", 'NO2', 'SO2', 'O3', 'CO']
st.subheader("Data Distribution for each pollutant column")

# Loop through each column and create histograms, with 3 plots per row
for i, column in enumerate(columns_to_plot):
    if i % 3 == 0:
        cols = st.columns(3) 
    
    col = cols[i % 3]
    
    # Plot the histogram in the appropriate column
    with col:
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.histplot(filtered_data[column], kde=False, bins=30, color="skyblue", edgecolor="black", ax=ax)
        ax.set_title(column)
        st.pyplot(fig)

station_counts = filtered_data['station'].value_counts()

# Identify the station with the highest count
max_station = station_counts.idxmax()
highlight_color = 'skyblue'
default_color = 'lightgray'

# Set the color for all stations, and then highlight the station with the max count
colors = [highlight_color if station == max_station else default_color for station in station_counts.index]

st.subheader('Count of Data by Station')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=station_counts.values, y=station_counts.index, palette=colors, ax=ax)

ax.set_title('Count of Data by Station', fontsize=16, fontweight='bold')
ax.set_xlabel('Count of Data', fontsize=12)
ax.set_ylabel('Station', fontsize=12)

st.pyplot(fig)

# Display boxplot for each selected pollutant across different stations
if selected_pollutants:
    st.subheader("Boxplots for Selected Pollutant Levels Across Different Stations")
    
    # Create boxplots for each selected pollutant in pairs (2 visualizations per row)
    for i, pollutant in enumerate(selected_pollutants):
        # Start a new row every 2 plots
        if i % 2 == 0:
            cols = st.columns(2)
        col = cols[i % 2] 
        
        with col:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.boxplot(data=filtered_data, x='station', y=pollutant, ax=ax)
            plt.xticks(rotation=45)
            ax.set_title(f"{pollutant} Levels Across Different Stations", fontsize=14, fontweight='bold')
            ax.set_xlabel('Station', fontsize=12)
            ax.set_ylabel(f"{pollutant} Concentration (µg/m³ or mg/m³)", fontsize=12)
            st.pyplot(fig)
    

if st.checkbox("Show Correlation Matrix"):
    st.subheader("Correlation Matrix of Pollutants")
    pollutants = filtered_data[["PM2.5", "PM10", "CO", "SO2", "NO2", "O3"]]
    correlation_matrix = pollutants.corr()
    colors = [(1, 1, 1), (0, 1, 0)] 
    cmap = LinearSegmentedColormap.from_list("custom", colors)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap=cmap, ax=ax)
    ax.set_title('Correlation Matrix of Selected Pollutants')
    ax.set_xlabel('Data value', fontsize=12)
    ax.set_ylabel("Data count", fontsize=12)
    st.pyplot(fig)
