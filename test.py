import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('./cholera/choleraDeaths.tsv', sep="\t")


df['total'] = df['Attack'] + df['Death']

app = dash.Dash(__name__)

app.layout = html.Div([
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
		}
	),
	html.Br(),
	html.Hr(),
	html.Br(),

	dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )

])



if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=3030)
