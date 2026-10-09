from models.bitacora import Bitacora
from models.defensa_guardiao_da_red.rastreador import Alerta_automatica

class Seguranca_Cibernetica:
    segurança_cibernetica = []
    def __int__(self, bitacora, olho_do_sistema, radar_de_acesso, alerta_de_riesgo, porta_dos_fundos, vulnerabilidade):
        self.bitacora = bitacora
        self.olho_do_sistema = olho_do_sistema
        self.radar_de_acesso = radar_de_acesso
        self.alerta_de_riesgo = alerta_de_riesgo
        self.porta_dos_fundos = porta_dos_fundos
        self.vulnerabilidade = vulnerabilidade
        self._status = False
        self._bitacora = []
        self._vulnerabilidade = []
        Seguranca_Cibernetica.segurança_cibernetica.append(self)

    def __str__(self):
        return f"Bitacora: {self.bitacora} \n |Defensa_do_diário_de_borde: {self.olho_do_sistema} \n |Guardião_da_red: {self.radar_de_acesso} \n |Falhas_de_vulnerabilidade: {self.alerta_de_riesgo} \n |Guardião_da_red: {self.porta_dos_fundos} \n |Vulnerabilidade: {str(self.vulnerabilidade)} \n |Status: {self.ativo}"
    @classmethod
    def listar_cibernetica(cls):
        for cibernetica in cls.segurança_cibernetica:
            print(f"Bitacora: {cibernetica.bitacora} \n |Defensa_do_diário_de_borde: {cibernetica.olho_do_sistema} \n |Guardião_da_red:{cibernetica.radar_de_acesso} \n |Falhas_de_vulnerabilidade: {cibernetica.alerta_de_riesgo} \n |Guardião_da_red: {cibernetica.porta_dos_fundos} \n |Vulnerabiliade: {str(cibernetica.vulnerabilidade)} \n |Status: {cibernetica.ativo} \n |Bitacora: {cibernetica.media_bitacora}")
    @property
    def ativo(self):
        return 'Ativo' if self._status else 'Inativo'
    @property
    def exibir_vulnerabilidade(self):
        print(f"Vulnerabilidade de segurança cibernetica: {self.localiçao}")
        for i, item in enumerate(self._vulnerabilidade, start=1):
            
            if hasattr (item, 'alerta_de_tempo_real'):
                mensagem_seguro = f"{i}. Localizacao: {item._localizacao} |Monitoreo_de_patrones_de_inyeccao: {item._monitoreo_de_patrones_de_inyeccao} |Alerta_de_tempo_real: {item.alerta_de_tempo_real}"
                print(mensagem_seguro)
            elif hasattr(item, 'registro'):
                mensagem_linha_do_tempo = f"{i}. Localizacao: {item._localizacao} |Monitoreo_de_patrones_de_inyeccao: {item._monitoreo_de_patrones_de_inyeccao} |Registro: {item.registro}"
                print(mensagem_linha_do_tempo)
            else:
                mensagem_ponto_cego = f"{i}. Localizacao: {item._localizacao} |Monitoreo_de_patrones_de_inyeccao: {item._monitoreo_de_patrones_de_inyeccao} |Shadow_IT: {item.shadow_IT}"
                print(mensagem_ponto_cego)

    def media_bitacora(self):
        if not self._bitacora:
            return 0
        monitoreo = sum(self._bitacora) / len(self._bitacora)
        return monitoreo
    
    def alterar_estado (self):
        self._status = not self._status

    def receber_bitacora(self, usuario, acao, data ):
        bitacora = Bitacora(usuario, acao, data)
        self._bitacora.append(bitacora)

    def adicionar_vulnerabilidade(self, item):
        if isinstance(item, Alerta_automatica):
            self._vulnerabilidade.append(item)

        else:
            raise ValueError("O item não pode ser None")