"""
Class: CS230-1
Name: Mya Rivard
Description: Final Project
I pledge that I have completed the programming assignment independently.
I have not copied the code from a student or any source.
I have not given my code to any student.
"""
import pandas as pd
import streamlit as st
import plotly_express as px
import folium
from streamlit_folium import st_folium

VOLCANOES_DATA = 'volcanoes1.csv'
# reading in the data
df = pd.read_csv(VOLCANOES_DATA, index_col='Volcano Number')

# creating a navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio('Pages', options=['Home', 'Volcanoes Sorted By Elevation', 'Volcanoes Above Sea Level', 'Map',
                                             'Frequency of Eruptions Per Era Bar Chart',
                                             'Rock Type Pie Chart', 'Volcano Type Pie Chart', 'Interactive Plot'])



# adding the Eruption Eras to the dataset
eruption_era = []
for x in df['Last Known Eruption']:
    if x == 'Unknown':
        eruption_era.append('Unknown')
    elif x[-3:] == ' CE':
        if x[3] == ' ' or x[2] == ' ' or x[0] == '0':
            eruption_era.append('0 CE - 999 CE')
        else:
            if x[:2] == '10' or x[:2] == '11' or x[:2] == '12':
                eruption_era.append('1000 CE - 1299 CE')
            elif x[:2] == '13' or x[:2] == '14' or x[:2] == '15':
                eruption_era.append('1300 CE - 1599 CE')
            elif x[:2] == '16' or x[:2] == '17' or x[:2] == '18':
                eruption_era.append('1600 CE - 1899 CE')
            elif x[:2] == '19' or x[:2] == '20':
                eruption_era.append('1900 CE - Present')
    elif x[-3:] == 'BCE':
        if x[3] == ' ' or x[2] == ' ':
            eruption_era.append('0 BCE - 999 BCE')
        else:
            if x[:2] == '10' or x[:2] == '11' or x[:2] == '12' or x[:2] == '13' or x[:2] == '14' or x[:2] == '15':
                eruption_era.append('1000 BCE - 1599 BCE')
            else:
                eruption_era.append('1600 BCE or earlier')
    else:
        eruption_era.append('Unknown')
df['Eruption Era'] = eruption_era


# creating a home page
def data_header():
    st.title("Exploring Volcano's Across The World")
    st.write("The purpose of this website is to explore volcanoes across the world through data visualization.")
    st.write(df)                # displaying the data


# displaying the data sorted by elevation
def sorted_data():
    st.title("Exploring Volcano's Across The World")
    df_sorted = df.sort_values('Elevation (m)')
    st.write(df_sorted)


# displaying the volcanoes above sea level based on the country the user inputs
def sort_volcanoes():
    st.title("Volcanoes Above Sea Level by Country")
    li = []
    for x in df['Country'].unique():
        li.append(x)        # adding each country to an empty list
    country = st.text_input('Enter a Country')
    dat = df[(df['Elevation (m)'] > 0) & (df.Country == country)]
    st.write(dat if country in li else 'Country not found')     # displaying if the country exists in the data


# assigning each eruption time frame a color for the map
def select_marker_color(row):
    if row['Eruption Era'] == 'Unknown':
        return 'black'
    elif row['Eruption Era'] == '0 CE - 999 CE':
        return 'red'
    elif row['Eruption Era'] == '1600 BCE or earlier':
        return 'orange'
    elif row['Eruption Era'] == '1000 BCE - 1599 BCE':
        return 'yellow'
    elif row['Eruption Era'] == '0 BCE - 999 BCE':
        return 'green'
    elif row['Eruption Era'] == '1000 CE - 1299 CE':
        return 'blue'
    elif row['Eruption Era'] == '1300 CE - 1599 CE':
        return 'purple'
    elif row['Eruption Era'] == '1600 CE - 1899 CE':
        return 'pink'
    elif row['Eruption Era'] == '1900 CE - Present':
        return "lightgreen"
    return None


# stacked bar chart comparing eruption era and primary volcano type
def bar_chart():
    st.title("Bar Chart Comparing the Frequency Eruptions in Each Time Frame")
    sort_val = st.selectbox('Select a 3rd Variable To Sort By', options=df.columns)
    fig = px.bar(df, x='Eruption Era', y=range(1, 1413+1), color=sort_val, barmode='stack',
                 title='Frequency of Eruptions in Each Era',
                 labels={'y': 'Frequency'})
    st.plotly_chart(fig)


# creating a pie chart of each volcano type
def pie1():
    count = df.groupby('Primary Volcano Type').size()           # counting how many volcanoes fall into each category
    print(count)
    fig = px.pie(df, names=df['Primary Volcano Type'].unique(), values=count,
                 title='Primary Volcano Types')
    st.plotly_chart(fig)


# bar chart displaying frequency of each dominant rock type
def pie2():
    df2 = df.dropna()                                         # removing missing values
    count = df2.groupby('Dominant Rock Type').size()          # counting how many volcanoes fall into each category
    fig = px.pie(df2, names=df2['Dominant Rock Type'].unique(), values=count,
                 title='Dominant Rock Types')
    st.plotly_chart(fig)


# creating an interactive plot that allows you to compare any two variables
def interactive_plot():
    st.title('Interactive Plot')
    st.write('Compare any two variables')
    x_axis_val = st.selectbox('Select X-Axis Value', options=df.columns)
    y_axis_val = st.selectbox('Select Y-Axis Value', options=df.columns)
    col = st.color_picker("Select a plot color")                            # allowing the user to choose any color
    plots = px.scatter(df, x=x_axis_val, y=y_axis_val)
    plots.update_traces(marker=dict(color=col))
    st.plotly_chart(plots)


# creating a map that displays each volcano color coded by eruption era
def maps():
    df['Color'] = df.apply(select_marker_color, axis=1)
    map1 = folium.Map(location=[20, 0], zoom_start=1.5)
    st.header('Volcanoes Mapped Across the World')
    st.text('========================Color Based on Date of Last Eruption========================')
    st.text('Black: Unknown                                        Light Green: 1900 CE - Present')
    st.text('Red: 0 CE - 999 CE                                           Pink: 1600 CE - 1899 CE')
    st.text('Orange: 1600 BCE or earlier                                   Green: 0 BCE - 999 BCE')
    st.text('Yellow: 1000 BCE - 1599 BCE                                  Blue: 1000 CE - 1299 CE')
    st.text('Purple: 1300 CE - 1599 CE')

    for index, location in df.iterrows():
        folium.Marker(location=[location['Latitude'], location['Longitude']], popup=location['Volcano Name'],
                      icon=folium.Icon(color=location['Color'])).add_to(map1)
    st_map = st_folium(map1)


# loop that displays which data goes where on streamlit
if options == 'Home':
    data_header()
elif options == 'Volcanoes Sorted By Elevation':
    sorted_data()
elif options == 'Volcanoes Above Sea Level':
    sort_volcanoes()
elif options == 'Map':
    maps()
elif options == 'Rock Type Pie Chart':
    pie2()
elif options == 'Volcano Type Pie Chart':
    pie1()
elif options == 'Frequency of Eruptions Per Era Bar Chart':
    bar_chart()
elif options == "Interactive Plot":
    interactive_plot()

