####################################################### LIBRARIES ########################################################
import pandas as pd
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit import components
#########################################################################################################################

######################################################### LOAD THE MALARIA DATASET #################################################
df = pd.read_csv('Malaria.csv')

st.set_page_config(page_title = 'Malaria Dashboard',
                    page_icon = 'bar_chart:',
                    layout = 'wide'
)

st.set_option('deprecation.showPyplotGlobalUse', False)
##################################################################################################################################




######################################################### TABS AND SESSIONS #################################################
# Create a dictionary to store the session state
session_state = st.session_state

# Initialize the current tab if not set
if 'current_tab' not in session_state:
    session_state.current_tab = "World Map"

# Create tabs with icons
tabs = {
    "🌍 World Map": "World Map",
    "📊 Bar chart": "Bar Chart",
    "📈 Line Chart": "Line Chart",
    "🥧 Pie Chart": "Pie Chart",
    "📄 Data Statistics": "Data Statistics"
}
############################################################################################################################


# Set the page title
st.title('Malaria Dataset Dashboard')

######################################################### CREATING THE SIDEBAR ###############################################################
# Sidebar for filtering options
st.sidebar.title('Filter Data')

selected_year = st.sidebar.selectbox('Select Year', ['All'] + df['Year'].unique().tolist())

selected_country = st.sidebar.selectbox('Select Country', ['All'] + df['Country'].unique().tolist())

selected_region = st.sidebar.selectbox('Select WHO Region', ['All'] + df['WHO Region'].unique().tolist())

selected_min_cases = st.sidebar.number_input('Minimum Number of Deaths', min_value=0)

selected_max_cases = st.sidebar.number_input('Maximum Number of Deaths', max_value=1000000)

# Display the tabs in the sidebar
selected_tab = st.sidebar.radio("Select a tab", list(tabs.keys()), index=list(tabs.values()).index(session_state.current_tab))
session_state.current_tab = tabs[selected_tab]
##############################################################################################################################################




######################################################### FILTERING THE DATA ##################################################################
# Filter the data based on selected options
if selected_year == 'All' and selected_country == 'All' and selected_region == 'All' and selected_min_cases == 0 and selected_max_cases == 0:
    filtered_df = df  # No filter applied
elif selected_year == 'All' and selected_country == 'All' and selected_region == 'All':
    filtered_df = df[(df['No. of deaths_min'] >= selected_min_cases) & (df['No. of deaths_max'] <= selected_max_cases)]
elif selected_year == 'All' and selected_country == 'All':
    filtered_df = df[(df['WHO Region'] == selected_region) & (df['No. of deaths_min'] >= selected_min_cases) & (df['No. of deaths_max'] <= selected_max_cases)]
elif selected_year == 'All' and selected_region == 'All':
    filtered_df = df[(df['Country'] == selected_country) & (df['No. of deaths_min'] >= selected_min_cases) & (df['No. of deaths_max'] <= selected_max_cases)]
elif selected_country == 'All' and selected_region == 'All':
    filtered_df = df[(df['Year'] == selected_year) & (df['No. of deaths_min'] >= selected_min_cases) & (df['No. of deaths_max'] <= selected_max_cases)]
elif selected_year == 'All':
    filtered_df = df[(df['Country'] == selected_country) & (df['WHO Region'] == selected_region) & (df['No. of deaths_min'] >= selected_min_cases) & (df['No. of deaths_max'] <= selected_max_cases)]
elif selected_country == 'All':
    filtered_df = df[(df['Year'] == selected_year) & (df['WHO Region'] == selected_region) & (df['No. of deaths_min'] >= selected_min_cases) & (df['No. of deaths_max'] <= selected_max_cases)]
elif selected_region == 'All':
    filtered_df = df[(df['Year'] == selected_year) & (df['Country'] == selected_country) & (df['No. of deaths_min'] >= selected_min_cases) & (df['No. of deaths_max'] <= selected_max_cases)]
else:
    filtered_df = df[(df['Year'] == selected_year) & (df['Country'] == selected_country) & (df['WHO Region'] == selected_region) & (df['No. of deaths_min'] >= selected_min_cases) & (df['No. of deaths_max'] <= selected_max_cases)]
####################################################################################################################################################################################################################################


############################################################ GROUPING THE DATA FOR VISUALIZATION ###################################################
# Filter and sort the data to get the top 10 countries with the highest number of malaria cases
top_10_countries = filtered_df.sort_values("No. of cases", ascending=False).head(10)
# Reverse the order to have the top 1 at the top
top_10_countries = top_10_countries[::-1]  

# Filter and sort the data to get the top 10 countries with the highest number of malaria deaths cases
top_10_countries_d = filtered_df.sort_values("No. of deaths", ascending=False).head(10)
# Reverse the order to have the top 1 at the top
top_10_countries_d = top_10_countries_d[::-1] 

# Group the data by organization and calculate the total deaths
organization_cases = filtered_df.groupby('WHO Region')['No. of cases'].sum().reset_index()

# Group the data by organization and calculate the total deaths
organization_deaths = filtered_df.groupby('WHO Region')['No. of deaths'].sum().reset_index()

# Group the data by year and calculate the total number of cases
cases_per_year = filtered_df.groupby('Year')['No. of cases'].sum().reset_index()

# Group the data by year and calculate the total number of cases
cases_of_deaths_year = filtered_df.groupby('Year')['No. of deaths'].sum().reset_index()
############################################################################################################################################################


#################################### TABS SELECTION ##########################################################################
#################################### WORLD MAP VISUALIZATION #################################################################
if session_state.current_tab == "World Map":
# Calculate the death rate as a percentage
    filtered_df['Death Rate'] = (filtered_df['No. of deaths'] / filtered_df['No. of cases']) * 100

    st.title("Malaria Cases Worldwide")

    fig = px.choropleth(
    data_frame=filtered_df,
    locations='Country',  # Column containing the country names
    locationmode='country names',
    color='No. of cases',  # Column to determine the color of the regions
    hover_name='Country',  # Column to display on hover

    color_continuous_scale='Viridis',  # Choose a color scale
    projection='natural earth'  # Choose a map projection
)

# Format hover data
    fig.update_traces(hovertemplate='<b>%{hovertext}</b><br>' +
                                'Cases: %{customdata[0]}<br>' +
                                'Deaths: %{customdata[1]}<br>' +
                                'Death Rate: %{customdata[2]:.2f}%'
                 )

# Set customdata for hover details
    fig.data[0].customdata = filtered_df[['No. of cases', 'No. of deaths', 'Death Rate']]


    fig.update_layout(
    width=1000,  # Set the width of the figure in pixels
    height=600  # Set the height of the figure in pixels
)

    st.plotly_chart(fig)

    st.markdown("World map chart showing the total number of malaria cases around the world") 
    st.markdown("Most of the cases are centered in Africa")
    st.markdown("Nigeria has the highest number of cases 53 million cases in 2017")

#################################### BAR CHART VISUALIZATION #######################################
elif session_state.current_tab == "Bar Chart":
    st.title("Top 10 Countries with the Highest Number of Malaria Cases ")

# Create the bar chart using Streamlit
    st.bar_chart(
    top_10_countries.set_index('Country')['No. of cases'],
    use_container_width=True
    )

    st.title("Top 10 Countries with the Highest Number of Malaria Deaths Cases ")

# Create the bar chart using Streamlit
    st.bar_chart(
    top_10_countries_d.set_index('Country')['No. of deaths'],
    use_container_width=True
    )

    st.markdown("Two bar charts showing the top 10 countries with number of cases and number of deaths") 
    st.markdown("Most of the countries are located in Africa")

    st.title("Number of Malaria Cases Per Region ")
# Create the bar chart using Streamlit
    # Create the bar chart using st.bar_chart
    chart_data = pd.Series(organization_cases['No. of cases'].values, index=organization_cases['WHO Region'])
    st.bar_chart(chart_data)

    st.title("Number of Malaria Deaths Per Region ")
# Create the bar chart using Streamlit
    # Create the bar chart using st.bar_chart
    chart_data = pd.Series(organization_deaths['No. of deaths'].values, index=organization_deaths['WHO Region'])
    st.bar_chart(chart_data)


    #st.markdown("Two bar charts showing the top 10 countries with number of cases and number of deaths") 
    #st.markdown("Most of the countries are located in Africa")

#################################### LINE CHART VISUALIZATION ###################################################
elif session_state.current_tab == "Line Chart":
    # Create the line chart
    fig = go.Figure(data=go.Scatter(x=cases_per_year['Year'], y=cases_per_year['No. of cases'], mode='lines'))

    # Update the chart layout
    fig.update_layout(
        title="Number of Cases Over Time",
        xaxis_title="Year",
        yaxis_title="Number of Cases",
        template="plotly_dark"
)
    fig.update_layout(
    width=500,  # Set the width of the figure in pixels
    height=500  # Set the height of the figure in pixels
)
    # Display the chart using Streamlit
    #st.plotly_chart(fig)

    # Create the line chart
    fig1 = go.Figure(data=go.Scatter(x=cases_of_deaths_year['Year'], y=cases_of_deaths_year['No. of deaths'], mode='lines',line=dict(color='red')))

    # Update the chart layout
    fig1.update_layout(
        title="Number of Deaths Over Time",
        xaxis_title="Year",
        yaxis_title="Number of Cases",
        template="plotly_dark"
)
    fig1.update_layout(
    width=500,  # Set the width of the figure in pixels
    height=500  # Set the height of the figure in pixels
)
    # Display the chart using Streamlit
    #st.plotly_chart(fig1)
# Display the charts side by side using Streamlit
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig)

    with col2:
        st.plotly_chart(fig1)


    st.markdown("Two line charts showing the number of cases and the number of deaths from 2010 till 2018") 
    st.markdown("Throughout the years both the number of cases and number of deaths is decreasing")
    st.markdown("WHO efforts contributed to this impact.")

#################################### PIE CHART VISUALIZATION #####################################        
elif session_state.current_tab == "Pie Chart":
    st.title("Number of Malaria Deaths Per WHO (2000 to 2018)")

    # Plotting the pie chart
    fig = px.pie(organization_deaths, values='No. of deaths', names='WHO Region')


    # Display the chart in Streamlit
    st.plotly_chart(fig)

    st.markdown("A pie chart showing the malaria death percentage per WHO region.")
    st.markdown("Africa contribute to 92% of malaria deaths in the world")
#################################### STATISTICS ##################################################
elif session_state.current_tab == "Data Statistics":
    # Display the filtered data
    st.subheader('Filtered Data')
    st.dataframe(filtered_df)

    # Summary statistics for filtered data
    st.subheader('Summary Statistics')
    st.write(filtered_df.describe())
#########################################################################################################################################













