import base64
import os
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_leaflet as dl
import plotly.express as px
import pandas as pd

from CRUD_Python_Module_Enhanced import AnimalShelter

###########################
# Data Manipulation / Model
###########################
username = "aacuser"
password = "verySecurePassword"

# Initialize local MongoDB connection
db = AnimalShelter(username, password)

# Load initial data and clean the ObjectID for Dash compatibility
df = pd.DataFrame.from_records(db.read({}))
if not df.empty and '_id' in df.columns:
    df.drop(columns=['_id'], inplace=True)

#########################
# Dashboard Layout / View
#########################
app = dash.Dash(__name__)

# Load branding image locally
image_filename = 'Grazioso Salvare Logo.png'
try:
    with open(image_filename, 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode()
    img_src = f'data:image/png;base64,{encoded_image}'
except FileNotFoundError:
    img_src = "" 

app.layout = html.Div(style={'fontSize': '18px', 'fontFamily': 'sans-serif'}, children=[
    html.Center(html.B(html.H1('OnlyDogs.com', style={'fontSize': '40px'}))),
    html.Center([
        html.Img(src=img_src, style={'width': '250px'}),
        html.P("Dashboard by: Cody Stuart", style={'fontSize': '20px', 'fontWeight': 'bold'})
    ]),
    html.Hr(),
    
    # Filter selection for specific rescue types
    dcc.RadioItems(
        id='filter-type',
        options=[
            {'label': 'Water Rescue', 'value': 'water'},
            {'label': 'Mountain or Wilderness Rescue', 'value': 'mountain'},
            {'label': 'Disaster Rescue or Individual Tracking', 'value': 'disaster'},
            {'label': 'Reset', 'value': 'reset'}
        ],
        value='reset',
        labelStyle={'display': 'inline-block', 'margin-right': '20px', 'fontSize': '20px'}
    ),
    html.Hr(),
    
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": "Animal ID", "id": "animal_id"},
            {"name": "Name", "id": "name"},
            {"name": "Breed", "id": "breed"},
            {"name": "Age (Weeks)", "id": "age_upon_outcome_in_weeks"},
            {"name": "Sex", "id": "sex_upon_outcome"},
            {"name": "Outcome", "id": "outcome_type"}
        ],
        style_cell={'fontSize': '16px', 'fontFamily': 'sans-serif', 'padding': '10px'},
        style_header={'backgroundcolor': 'rgb(230,230,230)', 'fontWeight': 'bold', 'fontSize': '18px'},
        data=df.to_dict('records'),
        page_size=10,
        row_selectable="single",
        selected_rows=[0],
        filter_action="native",
        sort_action="native"
    ),
    
    html.Div(style={'display': 'flex'}, children=[
        html.Div(id='graph-id', style={'flex': '1'}),
        html.Div(id='map-id', style={'flex': '1'}),
        html.Div(id='hist-id', style={'flex': '1'})
    ])
])

#############################################
# Controller / Callbacks
#############################################
@app.callback(Output('datatable-id', 'data'), [Input('filter-type', 'value')])
def update_dashboard(filter_type):
    if filter_type == 'reset':
        data = db.read({})
    else:
        data = db.read_rescue(filter_type)

    dff = pd.DataFrame.from_records(data)
    if not dff.empty and '_id' in dff.columns:
        dff.drop(columns=['_id'], inplace=True)
    return dff.to_dict('records')

@app.callback(Output('graph-id', 'children'), [Input('datatable-id', 'derived_virtual_data')])
def update_graphs(viewData):
    if not viewData: return []
    dff = pd.DataFrame(viewData)
    fig = px.pie(dff, names='breed', title='Breed Distribution')
    return [dcc.Graph(figure=fig)]

@app.callback(Output('map-id', 'children'), 
              [Input('datatable-id', 'derived_virtual_data'), 
               Input('datatable-id', 'derived_virtual_selected_rows')])
def update_map(viewData, index):
    if not viewData or index is None: return []
    dff = pd.DataFrame(viewData)

    if dff.empty:
        return [dl.Map(style={'height': '400px'}, center=[30.75, -97.48], zoom=10, children=[dl.TileLayer()])]
    row = index[0] if index else 0

    lat = dff.iloc[row]['location_lat']
    long = dff.iloc[row]['location_long']
    animal_name = dff.iloc[row]['name']
    breed_name = dff.iloc[row]['breed']

    return [
        dl.Map(style={'height': '400px'},
               center=[lat,long], zoom=12, children=[
                dl.TileLayer(),
                dl.Marker(position=[lat,long],
                          children=[
                              dl.Tooltip(breed_name),
                              dl.Popup([
                                  html.H3("Animal Name"),
                                  html.P(animal_name)
                              ])
                          ])
            ])
    ]
    """
    # Center map on the animal's coordinates
    return [dl.Map(style={'height': '400px'}, center=[30.75, -97.48], zoom=10, children=[
        dl.TileLayer(),
        dl.Marker(position=[dff.iloc[row, 13], dff.iloc[row, 14]], children=[
            dl.Tooltip(dff.iloc[row, 4]),
            dl.Popup([html.H3(dff.iloc[row, 9])])
        ])
    ])]
    """

if __name__ == "__main__":
    app.run()