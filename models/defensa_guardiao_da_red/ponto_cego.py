from models.defensa_guardiao_da_red.rastreador import Alerta_automatica

class Pontocego(Alerta_automatica):
    def __init__(self, localizacao, monitoreo_de_patrones_de_inyeccao, shadow_IT):
        super().__init__(localizacao, monitoreo_de_patrones_de_inyeccao)
        self.shadow_IT = shadow_IT
    def __str__(self):
        return self._localiçao