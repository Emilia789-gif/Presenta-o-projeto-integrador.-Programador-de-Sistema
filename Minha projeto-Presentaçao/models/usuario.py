class Usuario:
    def __init__(self, nome, email, senha):
        self.id = None
        self.nome = nome
        self.email = email
        self._senha = senha