from dash import Dash, dcc, html, Input, Output, State, callback
import pickle
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

loaded_model = pickle.load(open('/root/code/selling_price.model', 'rb'))

list = ['Ambassador', 'Ashok', 'Audi', 'BMW', 'Chevrolet', 'Daewoo',
       'Datsun', 'Fiat', 'Force', 'Ford', 'Honda', 'Hyundai', 'Isuzu',
       'Jaguar', 'Jeep', 'Kia', 'Land', 'Lexus', 'MG', 'Mahindra',
       'Maruti', 'Mercedes-Benz', 'Mitsubishi', 'Nissan', 'Opel',
       'Peugeot', 'Renault', 'Skoda', 'Tata', 'Toyota', 'Volkswagen',
       'Volvo', 'None']
list_owner = ["First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner", "None"]


app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Predicting Car Price System", style={'textAlign': 'center'}),
    html.Br(),
    html.H6("Instruction", style={'color':'Blue'}),
    html.H6("The system needs only 5 values to predict the selling car price including:", style={'color':'Blue', 'margin-left': '50px'}),
    html.H6("1. Brand: User assign the car brand. if you are not sure about the car brand or cannot find your car brand in the list, you can leave it blank or choose None.", style={'color':'Blue', 'margin-left': '50px'}),
    html.H6("2. Year: Users assign the car age. if you are not sure about the age, you can leave it blank.", style={'color':'Blue', 'margin-left': '50px'}),
    html.H6("3. Owner: Users assign an ordering owner in the car. if you are not sure about the car ordering owner,  you can leave it blank or choose None.", style={'color':'Blue', 'margin-left': '50px'}),
    html.H6("4. Mileage: Users assign the mileage of the car. if you are not sure about the mileage of the car, you can leave it blank.", style={'color':'Blue', 'margin-left': '50px'}),
    html.H6("5. Max power: Users assign the max power of the car. if you are not sure about max power of the car, you can leave it blank.", style={'color':'Blue', 'margin-left': '50px'}),
    html.H6("After you fill in all of information that you know, you click the submit button, and the website will show the selling price of this car at the bottom of the page.", style={'color':'Blue', 'margin-left': '50px'}),
    html.Br(),
    html.H6("Brand : ",  style={'display':'inline-block', 'margin-left': '300px'}),
    dcc.Dropdown(id='input-brand-state', options=[{'label': list[i], 'value': i} for i in range(len(list))], style={'display':'inline-block','width':'50%'}),
    html.Br(),
    html.H6("Year : ",  style={'display':'inline-block', 'margin-left': '300px'}),
    dcc.Input(id='input-year-state', type='number',min='0'),
    html.Br(),
    html.H6("Owner : ",  style={'display':'inline-block', 'margin-left': '300px'}),
    dcc.Dropdown(id='input-owner-state', options=[{'label': list_owner[i], 'value': i+1} for i in range(len(list_owner))], style={'display':'inline-block','width':'50%'}),
    html.Br(),
    html.H6("Mileage : ",  style={'display':'inline-block', 'margin-left': '300px'}),
    dcc.Input(id='input-mileage-state', type='number'),
    html.Br(),
    html.H6("Max Power : ",  style={'display':'inline-block', 'margin-left': '300px'}),
    dcc.Input(id='input-max_power-state', type='number'),
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
              State('input-brand-state', 'value'),
              State('input-year-state', 'value'),
              State('input-owner-state', 'value'),
              State('input-mileage-state', 'value'),
              State('input-max_power-state', 'value'),
)
              

def update_output(n_clicks, brand, year,owner, mileage, max_power):  
    
    if n_clicks>=1:
        if year == None:
            year = 2015
        if mileage == None:
            mileage = 19.38
        if max_power == None:
            max_power = 82.85
        if brand == None or brand == 32:
            brand = 20
        if owner == None or owner == 5:
            owner = 1
        sample = np.array([[max_power, mileage, year, brand, owner]])
        return f'The selling price of this car = {int(np.exp(loaded_model.predict(sample)))} baht'
        

if __name__ == '__main__':
    app.run(debug=True)