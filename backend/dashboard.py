import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from backend.handlers.mongo_handler import MongoHandler
from backend.ia_analysis import RealEstateAnalyzer

# Initialize MongoDB handler and AI analyzer
mongo_handler = MongoHandler()
analyzer = RealEstateAnalyzer()

def clean_numeric_string(value):
    if isinstance(value, str):
        return float(value.replace('.', '').replace(',', '.'))
    return value

def load_data(collection_name):
    data = mongo_handler.get_collection(collection_name)
    if data is None:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    df['cidade'] = df['localizacao'].str.split(' - ').str[-1]
    df['valor'] = df['valor'].apply(clean_numeric_string)
    df['area_m_quadrados'] = df['area_m_quadrados'].apply(clean_numeric_string)
    df['preco_m'] = df['preco_m'].apply(clean_numeric_string)
    return df

def init_dashboard(flask_app):
    dash_app = Dash(
        __name__,
        server=flask_app,
        routes_pathname_prefix='/dash/',
    )

    TEAL = "#00797A"
    BEGE = "#F8E9DD"
    WHITE = "#FFFFFF"
    SHADOW = "0 4px 12px rgba(0,0,0,0.08)"

    dash_app.layout = html.Div([
        html.H1("Dashboard Imobiliário com IA", style={
            'textAlign': 'center', 'color': TEAL, 'margin': '20px', 'fontWeight': 'bold', 'fontFamily': 'Montserrat, Arial, sans-serif'
        }),

        html.Div([
            html.Div([
                html.Label("Tipo de Imóvel:", style={'fontWeight': 'bold', 'color': TEAL}),
                dcc.Dropdown(
                    id='collection-dropdown',
                    options=[
                        {'label': 'Apartamentos', 'value': 'apartamentos'},
                        {'label': 'Lotes', 'value': 'lotes'}
                    ],
                    value='apartamentos',
                    searchable=False,
                    clearable=False,
                )
            ], style={'width': '48%', 'padding': '20px', 'backgroundColor': BEGE}),

            html.Div([
                html.Label("Selecione a Cidade:", style={'fontWeight': 'bold', 'color': TEAL}),
                dcc.Dropdown(
                    id='city-dropdown',
                    options=[
                        {'label': 'Americana', 'value': 'Americana'},
                        {'label': 'Campinas', 'value': 'Campinas'},
                        {'label': 'Paulínia', 'value': 'Paulínia'}
                    ],
                    value='Campinas',
                    searchable=False,
                    clearable=False,
                )
            ], style={'width': '48%', 'padding': '20px', 'backgroundColor': BEGE})
        ], style={'display': 'flex', 'justifyContent': 'center'}),

        html.Div(id='summary-cards', style={'display': 'flex', 'justifyContent': 'space-around'}),
        dcc.Graph(id='cluster-scatter'),
        html.Div(id='cluster-stats'),
        html.Div(id='prediction-results'),
        dcc.Graph(id='price-by-area'),
        dcc.Graph(id='price-distribution'),
        dcc.Graph(id='area-distribution'),
    ])

    @dash_app.callback(
        [Output('price-by-area', 'figure'),
         Output('price-distribution', 'figure'),
         Output('area-distribution', 'figure'),
         Output('summary-cards', 'children'),
         Output('cluster-scatter', 'figure'),
         Output('cluster-stats', 'children'),
         Output('prediction-results', 'children')],
        [Input('city-dropdown', 'value'),
         Input('collection-dropdown', 'value')]
    )
    def update_graphs(selected_city, selected_collection):
        df = load_data(selected_collection)
        city_df = df[df['cidade'] == selected_city]
        analysis_results = analyzer.analyze_city_data(city_df, selected_city)
        processed_df = analysis_results['processed_data']

        avg_price = processed_df['preco_m'].mean()
        avg_area = processed_df['area_m_quadrados'].mean()
        total_properties = len(processed_df)

        summary_cards = [
            html.Div([html.H3(f"R$ {avg_price:,.2f}"), html.P("Preço Médio por m²")]),
            html.Div([html.H3(f"{avg_area:,.2f} m²"), html.P("Área Média")]),
            html.Div([html.H3(f"{total_properties}"), html.P("Total de Imóveis")]),
        ]

        cluster_scatter = px.scatter(processed_df, x='area_m_quadrados', y='preco_m', color='cluster')

        cluster_stats = []
        for char in analysis_results['cluster_characteristics']:
            cluster_stats.append(html.Div([
                html.H4(f"Cluster {char['cluster']} - {char['tipo']}"),
                html.P(f"{char['tamanho']} imóveis"),
                html.P(f"Área média: {char['area_media']:.2f}"),
                html.P(f"Preço médio/m²: R$ {char['preco_medio_m2']:.2f}"),
            ]))

        prediction_results = html.Div("Previsões serão exibidas aqui")

        price_by_area = px.scatter(processed_df, x='area_m_quadrados', y='preco_m')
        price_distribution = px.histogram(processed_df, x='preco_m')
        area_distribution = px.histogram(processed_df, x='area_m_quadrados')

        return (price_by_area, price_distribution, area_distribution,
                summary_cards, cluster_scatter, cluster_stats, prediction_results)

    return dash_app
