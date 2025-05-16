import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

class RealEstateAnalyzer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.kmeans = None
        self.price_model = None
        
    def remove_outliers(self, df, columns=['preco_m', 'area_m_quadrados']):
        """Remove outliers usando o método IQR"""
        df_clean = df.copy()
        
        for column in columns:
            # Calcula os quartis
            Q1 = df_clean[column].quantile(0.25)
            Q3 = df_clean[column].quantile(0.75)
            IQR = Q3 - Q1
            
            # Define os limites
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Remove os outliers
            df_clean = df_clean[
                (df_clean[column] >= lower_bound) & 
                (df_clean[column] <= upper_bound)
            ]
        
        return df_clean
        
    def prepare_data(self, df):
        """Prepara os dados para análise"""
        # Seleciona features numéricas para clustering
        features = ['area_m_quadrados', 'preco_m']
        X = df[features].copy()
        
        # Normaliza os dados
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, features
    
    def perform_clustering(self, df, n_clusters=2):
        """Realiza clustering dos imóveis"""
        if len(df) < 2:
            df = df.copy()
            df.loc[:, 'cluster'] = 0
            return df, pd.DataFrame()
            
        X_scaled, features = self.prepare_data(df)
        
        # Aplica K-means com 2 clusters (alto e baixo preço)
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = self.kmeans.fit_predict(X_scaled)
        
        # Adiciona os clusters ao DataFrame
        df = df.copy()
        df.loc[:, 'cluster'] = clusters
        
        # Calcula estatísticas por cluster
        cluster_stats = df.groupby('cluster').agg({
            'area_m_quadrados': ['mean', 'std'],
            'preco_m': ['mean', 'std'],
            'valor': ['mean', 'std']
        }).round(2)
        
        return df, cluster_stats
    
    def train_price_model(self, df):
        """Treina modelo para prever preços"""
        if len(df) < 2:
            return {
                'mse': 0,
                'r2': 0,
                'feature_importance': {'area_m_quadrados': 1.0}
            }
            
        # Prepara features para o modelo
        features = ['area_m_quadrados']
        X = df[features]
        y = df['preco_m']
        
        # Divide em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Treina o modelo
        self.price_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.price_model.fit(X_train, y_train)
        
        # Faz previsões
        y_pred = self.price_model.predict(X_test)
        
        # Calcula métricas
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        return {
            'mse': mse,
            'r2': r2,
            'feature_importance': dict(zip(features, self.price_model.feature_importances_))
        }
    
    def get_cluster_characteristics(self, df):
        """Retorna características de cada cluster"""
        if len(df) < 2:
            return [{
                'cluster': 0,
                'tipo': 'Único',
                'tamanho': len(df),
                'area_media': df['area_m_quadrados'].mean() if len(df) > 0 else 0,
                'preco_medio_m2': df['preco_m'].mean() if len(df) > 0 else 0,
                'valor_medio': df['valor'].mean() if len(df) > 0 else 0,
                'tipologias': df['tipologia'].value_counts().to_dict() if len(df) > 0 else {}
            }]
            
        characteristics = []
        preco_medio_geral = df['preco_m'].mean()
        
        for cluster in sorted(df['cluster'].unique()):
            cluster_data = df[df['cluster'] == cluster].copy()
            preco_medio_cluster = cluster_data['preco_m'].mean()
            
            # Define o tipo do cluster baseado no preço médio
            cluster_type = "Alto Preço" if preco_medio_cluster > preco_medio_geral else "Baixo Preço"
            
            char = {
                'cluster': int(cluster),
                'tipo': cluster_type,
                'tamanho': len(cluster_data),
                'area_media': cluster_data['area_m_quadrados'].mean(),
                'preco_medio_m2': preco_medio_cluster,
                'valor_medio': cluster_data['valor'].mean(),
                'tipologias': cluster_data['tipologia'].value_counts().to_dict()
            }
            characteristics.append(char)
        
        return characteristics
    
    def analyze_city_data(self, df, city):
        """Analisa dados de uma cidade específica"""
        city_df = df[df['cidade'] == city].copy()
        
        if len(city_df) < 2:
            return {
                'cluster_stats': pd.DataFrame(),
                'model_metrics': {
                    'mse': 0,
                    'r2': 0,
                    'feature_importance': {'area_m_quadrados': 1.0}
                },
                'cluster_characteristics': [{
                    'cluster': 0,
                    'tipo': 'Único',
                    'tamanho': len(city_df),
                    'area_media': city_df['area_m_quadrados'].mean() if len(city_df) > 0 else 0,
                    'preco_medio_m2': city_df['preco_m'].mean() if len(city_df) > 0 else 0,
                    'valor_medio': city_df['valor'].mean() if len(city_df) > 0 else 0,
                    'tipologias': city_df['tipologia'].value_counts().to_dict() if len(city_df) > 0 else {}
                }],
                'processed_data': city_df
            }
        
        # Remove outliers
        city_df = self.remove_outliers(city_df)
        
        # Realiza clustering
        city_df, cluster_stats = self.perform_clustering(city_df)
        
        # Treina modelo de preços
        model_metrics = self.train_price_model(city_df)
        
        # Obtém características dos clusters
        cluster_chars = self.get_cluster_characteristics(city_df)
        
        return {
            'cluster_stats': cluster_stats,
            'model_metrics': model_metrics,
            'cluster_characteristics': cluster_chars,
            'processed_data': city_df
        } 