import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('./cholera/choleraDeaths.tsv', sep="\t")

df_AS = pd.read_csv('./cholera/naplesCholeraAgeSexData.tsv', sep="\t")

df_UK = pd.read_csv('./cholera/UKcensus1851.csv')

df['total'] = df['Attack'] + df['Death']

attack_cumsum = df['Attack'].cumsum()
death_cumsum = df['Death'].cumsum()

app = dash.Dash(__name__)

app.layout = html.Div([
	html.Div([
	html.Button('Who created this project? Click to show and hide', id='button', n_clicks=0),
	html.H1(
		id = "text",
		children = ""
	)],
	style={
		'textAlign': 'center'
	}
	),
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
                {'x': df['Date'], 'y': attack_cumsum, 'type': 'line', 'name': 'Attacks_total'},
                {'x': df['Date'], 'y': death_cumsum, 'type': 'line', 'name': 'Deaths_total'}
            ],
            'layout': {
                'title': 'Line Graph of Attacks and Deaths'
            }
        }
    ),
	html.Br(),
	html.Hr(),
	html.H1(
		children="Naples Cholera Data Table",
		style={
			'textAlign': 'center'
		}
	),
	dash_table.DataTable(
		id='table2',
		columns=[
			{"name": i, "id": i} 
			for i in df_AS.columns
		],
		data=df_AS.to_dict('records'),
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
	html.Hr(),
	dcc.Graph(
		id='naples_graph',
		figure={
			'data': [
				{'x': df_AS['age'], 'y': df_AS['male'], 'type': 'bar', 'name': 'male'},
				{'x': df_AS['age'], 'y': df_AS['female'], 'type': 'bar', 'name': 'female'},
			],
			'layout': {
				'title': 'Naples Cholera Deaths per 10,000 of age group'
			}
		}
	),
	html.Br(),
	html.Hr(),
	html.H1(
		children="UK Census 1851",
		style={
			'textAlign': 'center'
		}
	),
	dash_table.DataTable(
		id='table3',
		columns=[
			{"name": i, "id": i} 
			for i in df_UK.columns
		],
		data=df_UK.to_dict('records'),
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
	dcc.Graph(
		id='pie_chart_female',
		figure={
			'data':[
				go.Pie(labels=df_UK['age'], values=df_UK['female'])
			],
			'layout': {
				'title': 'Female'
			}
		}
	),

	dcc.Graph(
		id='pie_chart_male',
		figure={
			'data':[
				go.Pie(labels=df_UK['age'], values=df_UK['male'])
			],
			'layout': {
				'title': 'Male'
			}
		}
	),

	dcc.Graph(
		id='UK_bar_graph',
		figure={
			'data': [
				{'x': df_UK['age'], 'y': df_UK['male'], 'type': 'bar', 'name': 'male'},
				{'x': df_UK['age'], 'y': df_UK['female'], 'type': 'bar', 'name': 'female'},
			],
			'layout': {
				'title': 'UK census population'
			}
		}
	),
	dcc.Graph(
		id='pie_chart_female_vs_male',
		figure={
			'data':[
				go.Pie(labels=['male','female'], values=[df_UK['male'].sum(), df_UK['female'].sum()])
			],
			'layout': {
				'title': 'UK Census population Male vs Female'
			}
		}
	),
])

@app.callback(Output('text', 'children'),
	Input('button', 'n_clicks'))
def display_output(n_clicks):
	if n_clicks % 2 == 0:
		return ''
	else:
		return "Created by Clark Whitehead", html.Br(), "Created using Dash Python, plotly, and pandas", html.Br(), "Data from Robin Wilson (robin@rtwilson.com, www.rtwilson.com/academic) - Jan 2011."


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=3030)
