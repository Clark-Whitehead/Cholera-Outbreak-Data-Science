import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

#app = dash.Dash(__name__)

#app.layout = dash_table.DataTable(
#    id='table',
#    columns=[{"name": i, "id": i} for i in df.columns],
#    data=df.to_dict('records'),
#)

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
	data=df.to_dict('records')
	)
])

#app.layout = html.Div([
#    dcc.Graph(id='graph-with-slider'),
#    dcc.Slider(
#        id='year-slider',
#        min=df['year'].min(),
#        max=df['year'].max(),
#        value=df['year'].min(),
#        marks={str(year): str(year) for year in df['year'].unique()},
#        step=None
#    )
#])
#
#@app.callback(
#    Output('graph-with-slider', 'figure'),
#    Input('year-slider', 'value'))
#def update_figure(selected_year):
#
#    # Filter the data frame (df) on the Year where Year is selected_year
#    filtered_df = df[df.year == selected_year]
#
#    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
#                     size="pop", color="continent", hover_name="country",
#                     log_x=True, size_max=55)
#
#    fig.update_layout(transition_duration=500)
#
#    return fig


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=3030)