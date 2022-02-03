# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

#Create a list of all lauch sites 
unique_launch_sites = spacex_df['Launch Site'].unique().tolist()
#Create an empty place used as Dictionary
launch_sites = []
#Append the first object as 'label': 'All Sites', 'value': 'All Sites'
launch_sites.append({'label': 'All Sites', 'value': 'All Sites'})
#Append the other objects in the unique_launch_sites dictionary 
for launch_site in unique_launch_sites:
 launch_sites.append({'label': launch_site, 'value': launch_site})
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site_dropdown',
                                options=launch_sites,
                                placeholder='Select a Launch Site here', 
                                searchable = True , 
                                value = 'All Sites'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload_slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={
                                            0: '0 kg',
                                            1000: '1000 kg',
                                            2000: '2000 kg',
                                            3000: '3000 kg',
                                            4000: '4000 kg',
                                            5000: '5000 kg',
                                            6000: '6000 kg',
                                            7000: '7000 kg',
                                            8000: '8000 kg',
                                            9000: '9000 kg',
                                            10000: '10000 kg'
                                    },

                                    value=[min_payload,max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site_dropdown', component_property='value'))
def get_pie_chart(site_dropdown):
    if (site_dropdown == 'All Sites'):
        allsites_df  = spacex_df[spacex_df['class'] == 1] #All sites with Success only
        fig = px.pie(allsites_df, names = 'Launch Site',title = 'Total Success Launches By all sites')
    else:
        specificsite_df  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(specificsite_df, names = 'class',title = 'Total Success Launches for site '+site_dropdown)
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
     Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
     [Input(component_id = 'site_dropdown', component_property = 'value'),
     Input(component_id = "payload_slider", component_property = "value")]
)
def get_scattergraph(site_dropdown,payload_slider):
    if (site_dropdown == 'All Sites'):
        low, high = payload_slider
        allsites_df  = spacex_df
        inrange = (allsites_df['Payload Mass (kg)'] > low) & (allsites_df['Payload Mass (kg)'] < high)
        fig = px.scatter(
                allsites_df[inrange],
                x = "Payload Mass (kg)",
                y = "class",
                title = 'Correlation Between Payload and Success for All Sites',
                color="Booster Version Category",
                size='Payload Mass (kg)',
                hover_data=['Payload Mass (kg)']
            )
    else:
        low, high = payload_slider
        specificsite_df  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        inrange = (specificsite_df['Payload Mass (kg)'] > low) & (specificsite_df['Payload Mass (kg)'] < high)
        fig = px.scatter(
                specificsite_df[inrange],
                x = "Payload Mass (kg)",
                y = "class",
                title = 'Correlation Between Payload and Success for Site &#8608; '+site_dropdown,
                color="Booster Version Category",
                size='Payload Mass (kg)',
                hover_data=['Payload Mass (kg)']
            )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()