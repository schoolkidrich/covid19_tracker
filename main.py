import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import requests
import pandas as pd


app = dash.Dash(__name__)

url = 'https://covid19.schoolkidrich.repl.co/api/state=cases'
req = requests.get(url)
states = list(req.json().get('valid_states'))
options = ['ALL'] + sorted(states)
choices = [{'label': i, 'value': i} for i in options]

app.layout = html.Div(children=[
    html.H1(children='Covid 19 Tracker'),
    html.H3(children='Daily Plot'),
    html.Label('Select Plot'),
    dcc.RadioItems(
        id='plot_type',
        options=[
            {'label': 'Cases', 'value': 'Cases'},
            {'label': 'Deaths', 'value': 'Deaths'}
        ],
        value='Cases'
    ),
    html.Br(),
    html.Label('Select State'),
    dcc.Dropdown(
        id='case_state',
        options=choices,
        value='ALL',
        clearable=False
    ),
    dcc.Graph(
        id='daily_plot'
    ),
    html.Br(),
    html.H3(children='Cumulative Plot'),
    html.Label('Select Plot'),
    dcc.RadioItems(
        id='plot_type2',
        options=[
            {'label': 'Cases', 'value': 'Cases'},
            {'label': 'Deaths', 'value': 'Deaths'}
        ],
        value='Cases'
    ),
    html.Br(),
    html.Label('Select State'),
    dcc.Dropdown(
        id='cumulative_state',
        options=choices,
        value='ALL',
        clearable=False
    ),
    dcc.Graph(
        id='cumulative_plot'
    )
])


def get_data(state):
    link = f'https://covid19.schoolkidrich.repl.co/api/state={state}'
    request = requests.get(link)
    df = pd.DataFrame(request.json())
    return df


def get_cumulative(df):
    df = df.set_index('date').cumsum()
    return df.reset_index()


#fig 1 (num cases)
@app.callback(
    Output('daily_plot', 'figure'),
    [Input('case_state', 'value'),
     Input('plot_type', 'value')]
)
def plot_daily(case_state, plot_type):
    if plot_type == 'Cases':
        color = '#2ca02c'
    else:
        color = '#d62728'

    df = get_data(case_state)
    fig = px.line(df, title=f'Daily Number of {plot_type} [{case_state}]',
                  x='date', y=plot_type.lower())
    fig.update_traces(line_color=color)
    return fig


#fig 2 (cumulative cases)
@app.callback(
    Output('cumulative_plot', 'figure'),
    [Input('cumulative_state', 'value'),
     Input('plot_type2', 'value')]
)
def plot_cumulative(cumulative_state, plot_type2):
    if plot_type2 == 'Cases':
        color = '#2ca02c'
    else:
        color = '#d62728'

    df = get_data(cumulative_state)
    cumulative = get_cumulative(df)
    fig = px.line(cumulative, title=f'Total Number of {plot_type2} [{cumulative_state}]',
                  x='date', y=plot_type2.lower())
    fig.update_traces(line_color=color)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
