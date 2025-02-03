# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZGds1oLiu3kFhwI0gMezaD8ZIgcdao5j
"""

import dash
from dash import dcc, html, Output, Input
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv("Freedom in the World 2013-2022 Dataset (Ver 2.18.23).csv")
df_yearly = df[df["Edition"].isin(range(2013, 2023))]
df_map = df_yearly[["Country/Territory", "Edition", "Total"]].copy()
df_map.columns = ["Country", "Year", "Freedom Score"]


initial_year = 2013
df_initial = df_map[df_map["Year"] == initial_year]

# Harita için başlangıç figürü
fig_map = go.Figure(go.Choropleth(
    locations=df_initial['Country'],
    z=df_initial['Freedom Score'],
    locationmode='country names',
    colorbar_title="Freedom Score",
    colorscale='Viridis',
    showscale=True,
    hoverinfo='location+z+text',
    text=df_initial['Country'] + ': ' + df_initial['Freedom Score'].astype(str),
    marker_line_width=0.5,
))

# Uygulama düzeni
app.layout = html.Div([
    html.H1("Freedom Scores Over Time", style={'text-align': 'center', 'margin-bottom': '20px'}),

    html.Div([  # Renk Paleti Seçimi
        dcc.Dropdown(
            id='colorscale-dropdown',
            options=[
                {'label': 'Viridis', 'value': 'Viridis'},
                {'label': 'Cividis', 'value': 'Cividis'},
                {'label': 'Plasma', 'value': 'Plasma'},
                {'label': 'Inferno', 'value': 'Inferno'},
                {'label': 'Rainbow', 'value': 'Rainbow'},
                {'label': 'Jet', 'value': 'Jet'}
            ],
            value='Viridis',
            style={'width': '45%', 'display': 'inline-block', 'margin': '20px auto'}
        ),
    ], style={'text-align': 'center'}),

    html.Div([  # Ülkeler Arası Karşılaştırma
        dcc.Dropdown(
            id='country1-dropdown',
            options=[{'label': country, 'value': country} for country in df_map['Country'].unique()],
            value='United States',
            style={'width': '45%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='country2-dropdown',
            options=[{'label': country, 'value': country} for country in df_map['Country'].unique()],
            value='India',
            style={'width': '45%', 'display': 'inline-block', 'margin-left': '10px'}
        ),
    ], style={'text-align': 'center', 'margin-top': '30px'}),

    html.Div([  # Harita
        dcc.Graph(id="world-map", figure=fig_map, style={'height': '70vh', 'width': '75%', 'display': 'inline-block'})
    ], style={'margin-bottom': '30px'}),

    html.Div([  # Karşılaştırma grafiği
        dcc.Graph(id="comparison-graph", style={'height': '50vh', 'width': '75%', 'display': 'inline-block'})
    ], style={'margin-top': '30px'}),

], style={'padding': '20px', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})

@app.callback(
    Output("world-map", "figure"),
    [Input("colorscale-dropdown", "value")]
)
def update_map_colorscale(colorscale):
    # Yeni renk paleti seçildiğinde harita figürünü güncelle
    fig_map = go.Figure(go.Choropleth(
        locations=df_initial['Country'],
        z=df_initial['Freedom Score'],
        locationmode='country names',
        colorbar_title="Freedom Score",
        colorscale=colorscale,
        showscale=True,
        hoverinfo='location+z+text',
        text=df_initial['Country'] + ': ' + df_initial['Freedom Score'].astype(str),
        marker_line_width=0.5,
    ))
    return fig_map  # Güncellenmiş harita figürünü döndür

@app.callback(
    Output("comparison-graph", "figure"),
    [Input("country1-dropdown", "value"), Input("country2-dropdown", "value")]
)
def update_comparison_graph(country1, country2):
    # İki ülkenin verilerini alalım
    country1_data = df_map[df_map['Country'] == country1]
    country2_data = df_map[df_map['Country'] == country2]

    fig_comparison = go.Figure()

    fig_comparison.add_trace(go.Scatter(
        x=country1_data['Year'],
        y=country1_data['Freedom Score'],
        mode='lines+markers',
        name=country1
    ))

    fig_comparison.add_trace(go.Scatter(
        x=country2_data['Year'],
        y=country2_data['Freedom Score'],
        mode='lines+markers',
        name=country2
    ))

    fig_comparison.update_layout(
        title=f"{country1} vs {country2} Freedom Score Comparison",
        xaxis_title="Year",
        yaxis_title="Freedom Score",
        title_x=0.5
    )

    return fig_comparison  # Karşılaştırma grafiği döndür

if __name__ == "__main__":
    app.run_server(debug=True)



!pip install dash



!pip install plotly pandas



from google.colab import files
files.upload()



!kaggle datasets download -d justin2028/freedom-in-the-world-2013-2022

import dash
from dash import dcc, html, Output, Input
import plotly.graph_objects as go
import pandas as pd


app = dash.Dash(__name__)

df = pd.read_csv("Freedom in the World 2013-2022 Dataset (Ver 2.18.23).csv")


df_yearly = df[df["Edition"].isin(range(2013, 2023))]


df_map = df_yearly[["Country/Territory", "Edition", "Total"]].copy()


df_map.columns = ["Country", "Year", "Freedom Score"]


df_map = df_map.dropna(subset=["Country", "Freedom Score"])


df_map["Country"] = df_map["Country"].str.strip()


initial_year = 2013
df_initial = df_map[df_map["Year"] == initial_year]


fig_map = go.Figure(go.Choropleth(
    locations=df_initial['Country'],
    z=df_initial['Freedom Score'],
    locationmode='country names',
    colorbar_title="Freedom Score",
    colorscale='Viridis',
    showscale=True,
    hoverinfo='location+z+text',  # Hoverda ülke adı ve özgürlük puanı gösterilecek
    text=df_initial['Country'] + ': ' + df_initial['Freedom Score'].astype(str),  # Country ismi ve skoru
    marker_line_width=0.5,
))

# Uygulama düzeni
app.layout = html.Div([
    html.H1("Freedom Scores Over Time", style={'text-align': 'center', 'margin-bottom': '30px', 'font-size': '32px'}),

    # Üstte renk paleti seçimi
    html.Div([
        dcc.Dropdown(
            id='colorscale-dropdown',
            options=[
                {'label': 'Viridis', 'value': 'Viridis'},
                {'label': 'Cividis', 'value': 'Cividis'},
                {'label': 'Plasma', 'value': 'Plasma'},
                {'label': 'Inferno', 'value': 'Inferno'},
                {'label': 'Rainbow', 'value': 'Rainbow'},
                {'label': 'Jet', 'value': 'Jet'}
            ],
            value='Viridis',
            style={'width': '50%', 'margin': '0 auto'}
        ),
    ], style={'margin-bottom': '30px', 'text-align': 'center'}),

    # Ülkeler Arası Karşılaştırma
    html.Div([
        dcc.Dropdown(
            id='country1-dropdown',
            options=[{'label': country, 'value': country} for country in df_map['Country'].unique()],
            value='United States',
            style={'width': '45%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='country2-dropdown',
            options=[{'label': country, 'value': country} for country in df_map['Country'].unique()],
            value='India',
            style={'width': '45%', 'display': 'inline-block', 'margin-left': '10px'}
        ),
    ], style={'text-align': 'center', 'margin-bottom': '40px'}),

    # Harita
    html.Div([
        dcc.Graph(id="world-map", figure=fig_map, style={'height': '75vh', 'width': '100%'})
    ], style={'margin-bottom': '30px'}),

    # Karşılaştırma grafiği
    html.Div([
        dcc.Graph(id="comparison-graph", style={'height': '50vh', 'width': '100%'})
    ], style={'margin-top': '30px'}),

], style={'padding': '20px', 'backgroundColor': '#f4f6f7'})

# Callback for updating map colorscale
@app.callback(
    Output("world-map", "figure"),
    [Input("colorscale-dropdown", "value")]
)
def update_map_colorscale(colorscale):
   
    fig_map = go.Figure(go.Choropleth(
        locations=df_initial['Country'],
        z=df_initial['Freedom Score'],
        locationmode='country names',
        colorbar_title="Freedom Score",
        colorscale=colorscale,
        showscale=True,
        hoverinfo='location+z+text', 
        text=df_initial['Country'] + ': ' + df_initial['Freedom Score'].astype(str),  
        marker_line_width=0.5,
    ))
    return fig_map 

@app.callback(
    Output("comparison-graph", "figure"),
    [Input("country1-dropdown", "value"), Input("country2-dropdown", "value")]
)
def update_comparison_graph(country1, country2):
    # İki ülkenin verilerini alalım
    country1_data = df_map[df_map['Country'] == country1]
    country2_data = df_map[df_map['Country'] == country2]

    fig_comparison = go.Figure()

    fig_comparison.add_trace(go.Scatter(
        x=country1_data['Year'],
        y=country1_data['Freedom Score'],
        mode='lines+markers',
        name=country1
    ))

    fig_comparison.add_trace(go.Scatter(
        x=country2_data['Year'],
        y=country2_data['Freedom Score'],
        mode='lines+markers',
        name=country2
    ))

    fig_comparison.update_layout(
        title=f"{country1} vs {country2} Freedom Score Comparison",
        xaxis_title="Year",
        yaxis_title="Freedom Score",
        title_x=0.5,
        plot_bgcolor="#f4f6f7"  
    )

    return fig_comparison  
if __name__ == "__main__":
    app.run_server(debug=True)
