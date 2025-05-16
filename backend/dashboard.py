import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from handlers.mongo_handler import MongoHandler
from ia_analysis import RealEstateAnalyzer

# Initialize MongoDB handler and AI analyzer
mongo_handler = MongoHandler()
analyzer = RealEstateAnalyzer()

def clean_numeric_string(value):
    """Converte string numérica com vírgula para float"""
    if isinstance(value, str):
        return float(value.replace('.', '').replace(',', '.'))
    return value

# Function to load and process data from MongoDB
def load_data(collection_name):
    # Buscar dados da collection específica
    data = mongo_handler.get_collection(collection_name)
    if data is None:
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Extract city from location
    df['cidade'] = df['localizacao'].str.split(' - ').str[-1]
    
    # Clean numeric columns
    df['valor'] = df['valor'].apply(clean_numeric_string)
    df['area_m_quadrados'] = df['area_m_quadrados'].apply(clean_numeric_string)
    df['preco_m'] = df['preco_m'].apply(clean_numeric_string)
    
    return df

# Initialize the Dash app
app = Dash(__name__)

# Layout
TEAL = "#00797A"
BEGE = "#F8E9DD"
WHITE = "#FFFFFF"
SHADOW = "0 4px 12px rgba(0,0,0,0.08)"

app.layout = html.Div([
    html.H1("Dashboard Imobiliário com IA", style={
        'textAlign': 'center', 'color': TEAL, 'margin': '20px', 'fontWeight': 'bold', 'fontFamily': 'Montserrat, Arial, sans-serif'
    }),
    
    # Selectors
    html.Div([
        html.Div([
            html.Label("Tipo de Imóvel:", style={
                'fontWeight': 'bold',
                'color': TEAL,
                'fontFamily': 'Montserrat, Arial, sans-serif',
                'marginBottom': '8px',
                'display': 'block'
            }),
            dcc.Dropdown(
                id='collection-dropdown',
                options=[
                    {'label': 'Apartamentos', 'value': 'apartamentos'},
                    {'label': 'Lotes', 'value': 'lotes'}
                ],
                value='apartamentos',
                searchable=False,
                clearable=False,
                style={
                    'backgroundColor': 'white',
                    'borderRadius': '12px',
                    'boxShadow': SHADOW,
                    'border': 'none'
                }
            )
        ], style={
            'width': '48%',
            'display': 'inline-block',
            'padding': '20px',
            'backgroundColor': BEGE,
            'borderRadius': '16px',
            'margin': '10px'
        }),
        html.Div([
            html.Label("Selecione a Cidade:", style={
                'fontWeight': 'bold',
                'color': TEAL,
                'fontFamily': 'Montserrat, Arial, sans-serif',
                'marginBottom': '8px',
                'display': 'block'
            }),
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
                style={
                    'backgroundColor': 'white',
                    'borderRadius': '12px',
                    'boxShadow': SHADOW,
                    'border': 'none'
                }
            )
        ], style={
            'width': '48%',
            'display': 'inline-block',
            'padding': '20px',
            'backgroundColor': BEGE,
            'borderRadius': '16px',
            'margin': '10px'
        })
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'stretch',
        'margin': '20px',
        'gap': '20px'
    }),
    
    # Summary cards
    html.Div([
        html.Div(id='summary-cards', style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px'})
    ]),
    
    # AI Analysis Section
    html.Div([
        html.H2("Análise de IA", style={'textAlign': 'center', 'color': TEAL, 'margin': '20px', 'fontWeight': 'bold', 'fontFamily': 'Montserrat, Arial, sans-serif'}),
        html.Div([
            html.H3("Análise de Clusters", style={'textAlign': 'center', 'color': TEAL, 'fontWeight': 'bold', 'fontFamily': 'Montserrat, Arial, sans-serif'}),
            dcc.Graph(id='cluster-scatter', style={'backgroundColor': WHITE, 'borderRadius': '16px', 'boxShadow': SHADOW}),
            html.Div(id='cluster-stats', style={'margin': '20px', 'display': 'flex', 'justifyContent': 'space-around'})
        ], style={'borderRadius': '16px', 'padding': '20px', 'margin': '20px', 'backgroundColor': WHITE, 'boxShadow': SHADOW}),
        html.Div([
            html.H3("Análise Preditiva", style={'textAlign': 'center', 'color': TEAL, 'fontWeight': 'bold', 'fontFamily': 'Montserrat, Arial, sans-serif'}),
            html.Div(id='prediction-results', style={'margin': '20px'})
        ], style={'borderRadius': '16px', 'padding': '20px', 'margin': '20px', 'backgroundColor': WHITE, 'boxShadow': SHADOW})
    ]),
    
    # Distribution Graphs
    html.Div([
        html.H2("Análise de Distribuição", style={'textAlign': 'center', 'color': TEAL, 'margin': '20px', 'fontWeight': 'bold', 'fontFamily': 'Montserrat, Arial, sans-serif'}),
        html.Div([
            html.Div([
                dcc.Graph(id='price-distribution', style={'width': '100%', 'backgroundColor': WHITE, 'borderRadius': '16px', 'boxShadow': SHADOW})
            ], style={'width': '50%', 'display': 'inline-block'}),
            html.Div([
                dcc.Graph(id='area-distribution', style={'width': '100%', 'backgroundColor': WHITE, 'borderRadius': '16px', 'boxShadow': SHADOW})
            ], style={'width': '50%', 'display': 'inline-block'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'})
    ], style={'borderRadius': '16px', 'padding': '20px', 'margin': '20px', 'backgroundColor': BEGE, 'boxShadow': SHADOW}),
    
    # Price Analysis Graphs
    html.Div([
        html.H2("Análise de Preços", style={'textAlign': 'center', 'color': TEAL, 'margin': '20px', 'fontWeight': 'bold', 'fontFamily': 'Montserrat, Arial, sans-serif'}),
        html.Div([
            dcc.Graph(id='price-by-area', style={'width': '100%', 'backgroundColor': WHITE, 'borderRadius': '16px', 'boxShadow': SHADOW})
        ], style={'width': '100%'})
    ], style={'borderRadius': '16px', 'padding': '20px', 'margin': '20px', 'backgroundColor': BEGE, 'boxShadow': SHADOW})
], style={'backgroundColor': BEGE, 'minHeight': '100vh'})

# Callback to update graphs based on selected city and collection
@app.callback(
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
    # Load data from MongoDB
    df = load_data(selected_collection)
    
    # Filter data for selected city
    city_df = df[df['cidade'] == selected_city]
    original_count = len(city_df)
    
    # Perform AI analysis (this will remove outliers)
    analysis_results = analyzer.analyze_city_data(city_df, selected_city)
    processed_df = analysis_results['processed_data']
    
    # Calculate summary statistics after outlier removal
    avg_price = processed_df['preco_m'].mean()
    avg_area = processed_df['area_m_quadrados'].mean()
    total_properties = len(processed_df)
    removed_outliers = original_count - total_properties
    
    # Create summary cards
    summary_cards = [
        html.Div([
            html.H3(f"R$ {avg_price:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')),
            html.P("Preço Médio por m²")
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        html.Div([
            html.H3(f"{avg_area:,.2f} m²".replace(',', 'X').replace('.', ',').replace('X', '.')),
            html.P("Área Média")
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        html.Div([
            html.H3(f"{total_properties}"),
            html.P("Total de Imóveis")
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
    ]
    
    # Cluster scatter plot
    cluster_scatter = px.scatter(
        processed_df,
        x='area_m_quadrados',
        y='preco_m',
        color='cluster',
        title=f'Clusters de Imóveis em {selected_city}',
        labels={'area_m_quadrados': 'Área (m²)', 'preco_m': 'Preço por m²'}
    )
    cluster_scatter.update_layout(
        yaxis=dict(
            tickformat="R$ ,.2f"
        ),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # Cluster statistics
    cluster_stats = []
    for char in analysis_results['cluster_characteristics']:
        cluster_stats.append(html.Div([
            html.H4(f"Cluster {char['cluster']} - {char['tipo']}", style={'color': '#2c3e50'}),
            html.P(f"Quantidade de imóveis: {char['tamanho']}"),
            html.P(f"Área média: {char['area_media']:,.2f} m²".replace(',', 'X').replace('.', ',').replace('X', '.')),
            html.P(f"Preço médio por m²: R$ {char['preco_medio_m2']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')),
            html.P(f"Valor médio: R$ {char['valor_medio']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')),
        ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}))
    
    # Price predictions
    prediction_results = []
    if len(city_df) >= 2:
        # Generate predictions for different areas
        areas = [50, 100, 150, 200, 250]
        predictions = []
        
        for area in areas:
            pred_price = analyzer.price_model.predict([[area]])[0]
            predictions.append({
                'area': area,
                'preco_previsto': pred_price
            })
        
        prediction_results = html.Div([
            html.H4("Previsões de Preço por m²", style={'color': '#2c3e50', 'textAlign': 'center'}),
            html.Div([
                html.Div([
                    html.H5(f"{pred['area']} m²", style={'color': '#34495e'}),
                    html.P(f"R$ {pred['preco_previsto']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                          style={'fontSize': '1.2em', 'fontWeight': 'bold'})
                ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '10px', 'textAlign': 'center', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'})
                for pred in predictions
            ], style={'display': 'flex', 'justifyContent': 'space-around', 'flexWrap': 'wrap'})
        ])
    else:
        prediction_results = html.Div([
            html.H4("Previsões de Preço", style={'color': '#2c3e50', 'textAlign': 'center'}),
            html.P("Dados insuficientes para gerar previsões", style={'textAlign': 'center', 'color': '#7f8c8d'})
        ])
    
    # Price by area scatter chart
    price_by_area = px.scatter(
        processed_df,
        x='area_m_quadrados',
        y='preco_m',
        title=f'Relação entre Área e Preço por m² em {selected_city}',
        labels={'area_m_quadrados': 'Área (m²)', 'preco_m': 'Preço por m²'},
    )
    price_by_area.update_traces(marker=dict(color=TEAL, size=12, line=dict(width=2, color=WHITE)))
    price_by_area.update_layout(
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        xaxis=dict(
            showgrid=False,
            linecolor=TEAL,
            linewidth=2,
            title=dict(
                font=dict(size=14, color=TEAL),
                standoff=10
            )
        ),
        yaxis=dict(
            tickformat="R$ ,.2f",
            showgrid=True,
            gridcolor=BEGE,
            zerolinecolor=TEAL,
            zerolinewidth=2,
            title=dict(
                font=dict(size=14, color=TEAL),
                standoff=10
            )
        ),
        title=dict(
            font=dict(size=18, color=TEAL),
            x=0.5,
            y=0.95
        )
    )

    # Price distribution histogram
    price_distribution = px.histogram(
        processed_df,
        x='preco_m',
        title=f'Distribuição de Preços por m² em {selected_city}',
        labels={'preco_m': 'Preço por m²'},
        color_discrete_sequence=[TEAL]
    )
    price_distribution.update_layout(
        xaxis=dict(
            tickformat="R$ ,.2f",
            showgrid=False,
            linecolor=TEAL,
            linewidth=2
        ),
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        bargap=0.3,
        bargroupgap=0.15,
        yaxis=dict(showgrid=True, gridcolor=BEGE, zerolinecolor=TEAL, zerolinewidth=2)
    )

    # Area distribution histogram
    area_distribution = px.histogram(
        processed_df,
        x='area_m_quadrados',
        title=f'Distribuição de Áreas em {selected_city}',
        labels={'area_m_quadrados': 'Área (m²)'},
        color_discrete_sequence=[TEAL]
    )
    area_distribution.update_layout(
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        xaxis=dict(showgrid=False, linecolor=TEAL, linewidth=2),
        bargap=0.3,
        bargroupgap=0.15,
        yaxis=dict(showgrid=True, gridcolor=BEGE, zerolinecolor=TEAL, zerolinewidth=2)
    )

    return (price_by_area, price_distribution, area_distribution,
            summary_cards, cluster_scatter, cluster_stats, prediction_results)

if __name__ == '__main__':
    app.run(debug=True) 