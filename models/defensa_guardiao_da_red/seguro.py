from models.defensa_guardiao_da_red.rastreador import Alerta_automatica

class Seguro(Alerta_automatica):
    def __init__(self, localizacao, monitoreo_de_patrones_de_inyeccao, alerta_de_tempo_real):
        super().__init__(localizacao, monitoreo_de_patrones_de_inyeccao)
        self.alerta_de_tempo_real = alerta_de_tempo_real
    def __str__(self):
        return self._localiçao