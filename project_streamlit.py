"""
Olympics and Economics/Climate — A Streamlit Dashboard
=====================================================

This app lets you explore Olympics and Economics/Climate data across different countries.
It loads data from a CSV file, lets you filter by country, and displays the
results in three tabs: two scatter plots showing relationships between temperature and medal counts, a cluster heatmap, and an interactive world map depicting GDP per capita data, average yearly temperature, medal data, and cluster classification.

Required files:
    - project_clean_data.xlsx  (must be in the same folder as this script)

Dependencies (install once):
    %pip install streamlit 
    %pip install pandas 
    %pip install folium

How to run:
    1. Open a terminal and navigate (cd) to the folder containing this file.
    2. Run:  streamlit run new_app_documented.py
    3. A browser tab will open automatically with the app.
    4. To stop the app, press Ctrl+C in the terminal.
"""

# --- Imports ---
import streamlit as st   # Streamlit: turns Python scripts into interactive web apps
import pandas as pd       # Pandas: used for loading, filtering, and analyzing tabular data
import folium             # Folium: creates interactive Leaflet.js maps from Python
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components #ChatGPT. We put in our jupyter notebook code into ChatGPT as well as this python code shell to figure out what we needed to do to build the streamlit app. However, we ended up reverting a lot to copying and pasting code from the notebook and adjusting as necessary. The following ChatGPT in-line code has the same description. The link is provided at the end of this code.
from plotnine import *
from streamlit_folium import st_folium

# --- Page Title & Instructions ---
# st.title() renders large header text at the top of the page.
st.title('Olympics, Economics, and Climate Dashboard')

# st.write() can render plain text, Markdown, DataFrames, and more.
# Double asterisks (**) make text bold in Streamlit's Markdown support.
st.write(
    "Use the **sidebar** on the left to filter by one or more countries. "
    "Then explore the tabs below: **Data** shows the filtered table, "
    "**Scatter Plots** shows scatter plots of temperature and medal data, **Cluster Heatmap** displays cluster information, and **Map** displays "
    "countries on an interactive map."
)

# --- Load Data ---
# pd.read_excel() reads an Excel file into a Pandas DataFrame (a table of rows and columns).
olympics = pd.read_excel('project_clean_data.xlsx')

country = st.sidebar.multiselect(
    "Select a country:",
    sorted(olympics["country_name"].dropna().unique())
)

if country:
    display = olympics[olympics['country_name'].isin(country)]
else:
    display = olympics.copy()




# --- Tabs ---
# st.tabs() creates a row of clickable tabs. It returns one container per tab name..
tab_data, tab_scatter, tab_heatmap, tab_map = st.tabs(['Data', 'Scatter Plots', 'Cluster Heatmap', "Map"]) #ChatGPT. See in-line code above. Link to conversation is at the end of this file.

# --- Tab 1: Data Table ---
with tab_data:
    st.dataframe(display)

# --- Tab 2: Scatter Plots --- 
with tab_scatter: #ChatGPT. See in-line code above. Link to conversation is at the end of this file.
    p = (
    ggplot(display, aes(
        x='avg_yearly_temp_f',
        y='winter_total_medals',
        color='factor(cluster)'
    ))
    + geom_point(size=3, alpha=0.6)
    + geom_smooth(color='black', se=False)
    + labs(
        title="Temperature vs Winter Medals by Cluster",
        x="Avg Yearly Temp (°F)",
        y="Winter Medals",
        color="Cluster"
    )
    )
    
    q = (
    ggplot(display, aes(x='avg_yearly_temp_f', y='summer_total_medals'))
    + geom_point(alpha=0.4)
    + geom_smooth(color='red', se=True)
    + labs(title="Average Yearly Temperature vs. Summer Total Medal Count",
           x="Average Yearly Temperature (°F)", y="Summer Total Medals")
    )
    st.pyplot(p.draw())
    st.pyplot(p.draw())

# --- Tab 3: Interactive Map ---
with tab_heatmap:
    cluster_means = display.groupby("cluster")[[
        "most_recent_gdp",
        "avg_yearly_temp_f",
        "summer_total_medals",
        "winter_total_medals"
    ]].mean()

    plt.figure(figsize=(10,6))

    sns.heatmap(
        cluster_means,
        annot=True,
        linewidths=0.5,
        cmap="YlGnBu",
        fmt=".0f"
    )

    plt.title("Cluster Means Heatmap")
    plt.xlabel("Variables")
    plt.ylabel("Cluster")
    plt.tight_layout()
    plt.show()
    st.pyplot(plt)

#--- Tab 4: interactive map ---
with tab_map:
    m = folium.Map(location = [20,0], zoom_start = 2)
    cluster_colors = {
        0: "blue",
        1: "green",
        2: "orange",
        3: "red",
        4: "purple"
    }
    for i in range(0,len(display)):
        folium.CircleMarker(
            location = [display.iloc[i]['latitude'], display.iloc[i]['longitude']],
            radius = 2,
            color = cluster_colors[display.iloc[i]['cluster']],
            fill = True,
            fill_color = cluster_colors[display.iloc[i]['cluster']],
            fill_opacity = 0.6,
            popup = display.iloc[i]["country_name"] + ':' + display.iloc[i]["cluster_name"] + ', Most Recent GDP per Capita: $' + str(display.iloc[i]["most_recent_gdp"].round(2)) + ', Avg Yearly Temperature:' + str(display.iloc[i]["avg_yearly_temp_f"]) + '°F' + ', Summer Total Medals: ' + str(display.iloc[i]["summer_total_medals"]) + ', Winter Total Medals: ' + str(display.iloc[i]["winter_total_medals"]) + ' Winter Medals'
            ).add_to(m)
    m
    st_folium(m)
#Link to Chat conversation: https://chatgpt.com/share/69f113e9-3a34-83ea-8f09-e282d53c06c6
