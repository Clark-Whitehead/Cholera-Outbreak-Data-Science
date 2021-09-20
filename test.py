import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('./cholera/choleraDeaths.tsv', sep="\t")

df['total'] = df['Attack'] + df['Death']

df['Attack_cumsum'] = df['Attack'].cumsum()
df['Death_cumsum'] = df['Death'].cumsum()

app = dash.Dash(__name__)

app.layout = html.Div([
	html.H1(
		children="Cholera Data-Table",
		style={
			'textAlign': 'center'
		}
	),
	dash_table.DataTable(
		id='table',
		columns=[
			{"name": i, "id": i} 
			for i in df.columns
		],
		data=df.to_dict('records'),
		style_cell={
			'maxWidth': 50,
			'fontWeight': 'bold'
		},
		style_table={
			'height': '300px', 'overflowY': 'auto', 'width': '1200px', 'margin-left': 'auto', 'margin-right': 'auto'
		},
		style_header={
			'backgroundColor': 'green',
			'fontWeight': 'bold',
			'color': 'white'
		},	
	),
	html.Br(),
	html.Hr(),
	html.Br(),


	dcc.Graph(
        id='Line Graph',
        figure={
            'data': [
                {'x': df['Date'], 'y': df['Attack'], 'type': 'line', 'name': 'Attacks'},
                {'x': df['Date'], 'y': df['Death'], 'type': 'line', 'name': 'Deaths'},
                {'x': df['Date'], 'y': df['Attack_cumsum'], 'type': 'line', 'name': 'Deaths_total'},
                {'x': df['Date'], 'y': df['Death_cumsum'], 'type': 'line', 'name': 'Deaths_total'}
            ],
            'layout': {
                'title': 'Line Graph of Attacks and Deaths'
            }
        }
    ),


])



if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=3030)
