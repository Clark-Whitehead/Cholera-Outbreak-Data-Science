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

df_pumps = pd.read_csv('./cholera/choleraPumpLocations.csv')

df_death_loc = pd.read_csv('./cholera/choleraDeathLocations.csv')

df_death_loc['color'] = "#FF7F0E"
df_pumps['color'] = "#1F77B4"
df_pumps['num'] = 4

df_combine = df_death_loc.append(df_pumps)

df['Total'] = df['Attack'] + df['Death']

attack_cumsum = df['Attack'].cumsum()
death_cumsum = df['Death'].cumsum()

fig = px.scatter_mapbox(df_combine, lat="lat", lon="lon", size="num", height=700, zoom=15, color_discrete_sequence=[df_combine['color']])

fig.update_layout(mapbox_style="carto-positron")



colors_female = ['#ffe5cf', '#ffcb9f', '#ffb26e', '#ff983e', '#e6710d', '#b3580a', '#803f07', '#4d2604', '#190d01']
pie_female = go.Figure(data=[go.Pie(labels=df_UK['Age'], values=df_UK['Female'])])
pie_female.update_layout(
	title_text="Female",
	title_x=0.5
)
pie_female.update_traces(marker=dict(colors=colors_female))

colors_male = ['#d2e4f0', '#a5c8e1', '#79add2', '#4c91c3', '#1c6aa2', '#16537e', '#103b5a', '#092336', '#030c12']
pie_male = go.Figure(data=[go.Pie(labels=df_UK['Age'], values=df_UK['Male'])])
pie_male.update_layout(
	title_text="Male",
	title_x=0.5
)
pie_male.update_traces(marker=dict(colors=colors_male))

colors_combine = ['#1F77B4', '#FF7F0E']
pie_combine = go.Figure(data=[go.Pie(labels=['Male','Female'], values=[df_UK['Male'].sum(), df_UK['Female'].sum()])]) 
pie_combine.update_layout(
	title_text="Male vs Female",
	title_x=0.5
)
pie_combine.update_traces(marker=dict(colors=colors_combine))

app = dash.Dash(__name__)

app.layout = html.Div([
	html.Div([
		html.Button('Who created this project?', id='button', n_clicks=0),
		html.H1(
			id = "text",
			children = "",
			style={
				'color': 'white',
				'font-family': 'arial'
			}
		),
		html.H1(
			children="A Visualization of the 1854 Cholera Outbreak",
			style={
				'textAlign': 'center',
				'font-family': 'arial',
				'color': '#FF7F0E'
			}
		),
		html.Img(
			src='https://imgix.ranker.com/list_img_v2/16601/2776601/original/1832-england-cholera-epidemic-facts',
			style={'display': 'block',
					'margin-left': 'auto',
					'margin-right': 'auto',
					'width': '50%'
			}
		)
	],
	style={
		'textAlign': 'center',
		'font-family': 'arial',
		'background-color': '#1F77B4'
	}
	),
	html.Hr(),
	html.H1(
		children="Attacks & Deaths",
		style={
			'textAlign': 'center',
			'font-family': 'arial',
			'color': '#FF7F0E'
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
			'backgroundColor': '#1F77B4',
			'fontWeight': 'bold',
			'color': 'white'
		},	
	),
	html.Br(),
	html.Br(),


	dcc.Graph(
        id='Line Graph',
        figure={
            'data': [
                {'x': df['Date'], 'y': df['Attack'], 'type': 'line', 'name': 'Attacks', 'line':dict(color='#1F77B4')},
                {'x': df['Date'], 'y': df['Death'], 'type': 'line', 'name': 'Deaths', 'line':dict(color='#FF7F0E')},
                {'x': df['Date'], 'y': attack_cumsum, 'type': 'line', 'name': 'Attacks_total', 'line':dict(color='#1F77B4', dash='dash')},
                {'x': df['Date'], 'y': death_cumsum, 'type': 'line', 'name': 'Deaths_total', 'line':dict(color='#FF7F0E', dash='dash')}
            ],
            'layout': {
                'title': 'Line Graph of Attacks and Deaths'
            }
        }
    ),
	html.Br(),
	html.Hr(),
	html.H1(
		children=["Naples in the Time of Cholera 1884-1911", html.Br(), "Deaths per 10,000 inhabitants of that age group"],
		style={
			'textAlign': 'center',
			'font-family': 'arial',
			'color': '#FF7F0E'
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
			'backgroundColor': '#1F77B4',
			'fontWeight': 'bold',
			'color': 'white'
		},	
	),
	dcc.Graph(
		id='naples_graph',
		figure={
			'data': [
				{'x': df_AS['Age'], 'y': df_AS['Male'], 'type': 'bar', 'name': 'Male'},
				{'x': df_AS['Age'], 'y': df_AS['Female'], 'type': 'bar', 'name': 'Female'},
			],
			'layout': {
				'title': 'Naples Cholera Deaths per 10,000 of Age Group'
			}
		}
	),
	html.Br(),
	html.Hr(),
	html.H1(
		children="UK Census Population 1851 - By Sex and Age",
		style={
			'textAlign': 'center',
			'font-family': 'arial',
			'color': '#FF7F0E'
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
			'backgroundColor': '#1F77B4',
			'fontWeight': 'bold',
			'color': 'white'
		},	
	),
	dcc.Graph(
		id='pie_chart_female',
		figure=pie_female
	),

	dcc.Graph(
		id='pie_chart_male',
		figure=pie_male
	),

	dcc.Graph(
		id='UK_bar_graph',
		figure={
			'data': [
				{'x': df_UK['Age'], 'y': df_UK['Male'], 'type': 'bar', 'name': 'Male'},
				{'x': df_UK['Age'], 'y': df_UK['Female'], 'type': 'bar', 'name': 'Female'},
			],
			'layout': {
				'title': 'UK Populatin by Age and Sex'
			}
		}
	),
	dcc.Graph(
		id='pie_chart_female_vs_male',
		figure=pie_combine
	),
	html.Hr(),
	html.H1(
		children="Map of the Deaths and Water Pumps",
		style={
			'textAlign': 'center',
			'font-family': 'arial',
			'color': '#FF7F0E'
		}
	),
	dcc.Graph(
		figure=fig
	),

])

@app.callback(Output('text', 'children'),
	Input('button', 'n_clicks'))
def display_output(n_clicks):
	if n_clicks % 2 == 0:
		return ''
	else:
		return "Created by Clark Whitehead: clark37@hawaii.edu", html.Br(), "Created using Dash Python, plotly, and pandas", html.Br(), "Data from Robin Wilson (robin@rtwilson.com, www.rtwilson.com/academic) - Jan 2011."


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=3030)
