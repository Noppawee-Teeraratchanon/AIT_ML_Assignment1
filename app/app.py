from dash import Dash, dcc, html, Input, Output, State, callback
import pickle
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# load the model
loaded_model = pickle.load(open('/root/code/selling_price.model', 'rb'))

# make a list of owner
list_owner = ["First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner", "None"]

# make a list of transmission
list_transmission = ["Automatic", "Manual", "None"]

# make a list of fuel
list_fuel = ["Diesel", "Petrol", "None"]


app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Predicting Car Price System", style={'textAlign': 'center'}),
    html.Br(),
    html.P("Instruction", style={'color':'Blue'}),
    html.P("The system needs only 7 values to predict the selling car price including:", style={'color':'Blue', 'margin-left': '50px'}),
    html.P("1. Max power: Users assign the max power of the car. If you are not sure about max power of the car, you can leave it blank.", style={'color':'Blue', 'margin-left': '50px'}),
    html.P("2. Mileage: Users assign the mileage of the car. If you are not sure about the mileage of the car, you can leave it blank.", style={'color':'Blue', 'margin-left': '50px'}),
    html.P("3. Owner: Chaky company sell only the new car which is first hand. so I assign the system to set the first hand as default value", style={'color':'Blue', 'margin-left': '50px'}),
    html.P("4. Km_driven: Chaky company sell only the new car which mean the kilometer driven need to be 0. so I assign the system to set 0 as default value", style={'color':'Blue', 'margin-left': '50px'}),
    html.P("5. Transmission: Users assign the type of transmission of the car. If you are not sure about the transmission type of the car, you can leave it blank or choose None.", style={'color':'Blue', 'margin-left': '50px'}),
    html.P("6. Seats: Users assign the seat number of the car. If you are not sure about the seat number of the car, you can leave it blank.", style={'color':'Blue', 'margin-left': '50px'}),
    html.P("7. Fuel: Users assign the type of fuel that the car use. If you are not sure about the transmission type of the car, you can leave it blank or choose None.", style={'color':'Blue', 'margin-left': '50px'}),
    html.P("After you fill in all of information that you know, you click the submit button, and the website will show the selling price of this car at the bottom of the page.", style={'color':'Blue', 'margin-left': '50px'}),
    html.Br(),
    html.H6("Max Power : ",  style={'display':'inline-block', 'margin-left': '300px'}),
    dcc.Input(id='input-max_power-state', type='number'),
    html.Br(),
    html.H6("Mileage : ",  style={'display':'inline-block', 'margin-left': '300px'}),
    dcc.Input(id='input-mileage-state', type='number'),
    html.Br(),
    html.H6("Owner : ",  style={'display':'inline-block', 'margin-left': '300px'}),
    dcc.Dropdown(id='input-owner-state', options=[{'label': list_owner[i], 'value': i+1} for i in range(len(list_owner))], style={'display':'inline-block','width':'50%'}, value=1 ),
    html.Br(),
    html.H6("km_driven : ",  style={'display':'inline-block', 'margin-left': '300px'}),
    dcc.Input(id='input-km_driven-state', type='number', value=0),
    html.Br(),
    html.H6("transmission : ",  style={'display':'inline-block', 'margin-left': '300px'}),
    dcc.Dropdown(id='input-transmission-state', options=[{'label': list_transmission[i], 'value': i} for i in range(len(list_transmission))], style={'display':'inline-block','width':'50%'}),
    html.Br(),
    html.H6("seats : ",  style={'display':'inline-block', 'margin-left': '300px'}),
    dcc.Input(id='input-seats-state', type='number'),
    html.Br(),
    html.H6("fuel : ",  style={'display':'inline-block', 'margin-left': '300px'}),
    dcc.Dropdown(id='input-fuel-state', options=[{'label': list_fuel[i], 'value': i} for i in range(len(list_fuel))], style={'display':'inline-block','width':'50%'}),
    html.Br(),
    html.Br(),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit', style={'width': '200px', 'margin-left': '625px', 'color': 'Red', 'background': 'White'}),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H4(id='output-selling_price', style={'color':'Blue', 'margin-left': '50px'})
    ], style = { 'background': 'Silver'})



@callback(Output('output-selling_price', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-max_power-state', 'value'),
              State('input-mileage-state', 'value'),
              State('input-owner-state', 'value'),
              State('input-km_driven-state', 'value'),
              State('input-transmission-state', 'value'),
              State('input-seats-state', 'value'),
              State('input-fuel-state', 'value')
)
              
# create output function to predict the selling price of a car
def update_output(n_clicks,max_power,mileage,owner, km_driven, transmission, seats, fuel):  
    
    if n_clicks>=1:
        if max_power == None:
            max_power = 82.85 #default of max power is median of training data which is 82.85
        if mileage == None:
            mileage = 19.38  #default of mileage is mean of training data which is 19.38
        if owner == None or owner == 5:
            owner = 1     #default of owner is mode of training data which is 1 (First Owner)
        if km_driven == None:
            km_driven = 60000   #default of km_driven is median of training data which is 60000 (First Owner)
        if transmission == None or transmission == 2:
            transmission = 1    #default of transmission is mode of training data which is 1 (Manual)
        if seats == None:
            seats = 5        #default of seats is median of training data which is 5
        if fuel == None or fuel ==2:
            fuel = 0        #default of fuel is mode of training data which is 0 (Diesel)
        sample = np.array([[max_power,mileage,owner, km_driven, transmission, seats, fuel]])
        return f'The selling price of this car = {int(np.exp(loaded_model.predict(sample)))} baht'

if __name__ == '__main__':
    app.run(debug=True)