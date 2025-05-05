class document:
    def __init__(self, valor, localizacao, tipologia, area_m_quadrados, preco_m):
        self.valor = valor
        self.localizacao = localizacao
        self.tipologia = tipologia
        self.area_m_quadrados = area_m_quadrados
        self.preco_m = preco_m

    def to_dict (self):
        return {
            'valor': self.valor,
            'localizacao': self.localizacao,
            'tipologia': self.tipologia,
            'area_m_quadrados': self.area_m_quadrados,
            'preco_m': self.preco_m
        }