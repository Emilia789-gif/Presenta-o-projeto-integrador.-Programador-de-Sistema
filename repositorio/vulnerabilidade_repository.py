from database.db import connector
from models.vulnerabilidade import Vulnerabilidade


def tabela_vulnerabilidade():
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS vulnerabilidade (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), descricao TEXT, impacto VARCHAR(255))"
    )
    conexao.commit()
    cursor.close()
    conexao.close()

def criar_vulnerabilidade(vulnerabilidade):
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO vulnerabilidade (nome, descricao, impacto) VALUES (%s, %s, %s)",
        (vulnerabilidade.nome, vulnerabilidade.descricao, vulnerabilidade.impacto),
    )
    conexao.commit()
    id_vulnerabilidade = cursor.lastrowid
    cursor.close()
    conexao.close()
    vulnerabilidade.id = id_vulnerabilidade
    return vulnerabilidade


def buscar_vulnerabilidade_por_nome(nome):
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, descricao, impacto FROM vulnerabilidade WHERE nome = %s", (nome,)
    )
    vulnerabilidades = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [Vulnerabilidade(id, nome, descricao, impacto) for (id, nome, descricao, impacto) in vulnerabilidades]

def buscar_vulnerabilidade_por_descricao(descripcao):
    conexao = connector()
    cursor = conexao.cursor(dictionary = True)
    query = "SELECT * FROM vulnerabilidade WHERE descricao LIKE %s"
    cursor.execute(query, ('%' + descripcao + '%',))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado

def buscar_vulnerabilidade_por_impacto(impacto):
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, descricao, impacto FROM vulnerabilidade WHERE impacto = %s", (impacto,)
    )
    vulnerabilidades = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [Vulnerabilidade(id, nome, descricao, impacto) for (id, nome, descricao, impacto) in vulnerabilidades]

def listar_vulnerabilidades():
    conexao = connector()
    cursor = conexao.cursor()
    # Asegúrate de que los nombres de las columnas coincidan con tu tabla
    cursor.execute("SELECT id, nome, descricao, impacto FROM vulnerabilidade")
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def buscar_vulnerabilidade_por_id(id_vulnerabilidade):
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, descricao, impacto FROM vulnerabilidade WHERE id = %s", (id_vulnerabilidade,))
    linha = cursor.fetchone()
    cursor.close()
    conexao.close()
    return linha

def actualizar_vulnerabilidade(id_vulnerabilidade, nome, descricao, impacto):
    conexao = connector()
    cursor = conexao.cursor()
    query = "UPDATE vulnerabilidade SET nome = %s, descricao = %s, impacto = %s WHERE id = %s"
    cursor.execute(query, (nome, descricao, impacto, id_vulnerabilidade))
    conexao.commit()
    cursor.close()
    conexao.close()

def inserir_vulnerabilidade(nome, descricao, impacto):
    conexao = connector()
    cursor = conexao.cursor()
    query = "INSERT INTO vulnerabilidade (nome, descricao, impacto) VALUES (%s, %s, %s)"
    cursor.execute(query, (nome, descricao, impacto))
    conexao.commit()
    cursor.close()
    conexao.close()