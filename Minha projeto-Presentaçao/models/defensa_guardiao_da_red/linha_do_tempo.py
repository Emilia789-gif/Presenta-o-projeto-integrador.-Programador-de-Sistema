from models.defensa_guardiao_da_red.rastreador import Alerta_automatica

class Linha_de_tempo(Alerta_automatica):
    def __init__(self, localizacao, monitoreo_de_patrones_de_inyeccao, registro):
        super().__init__(localizacao, monitoreo_de_patrones_de_inyeccao)
        self.resgistrom = registro
    def __str__(self):
        return self._localiçao