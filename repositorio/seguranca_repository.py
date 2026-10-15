from database.db import connector
from models.seguranca_cibernetica import Seguranca_Cibernetica

def tabela_seguranca_cibernetica():
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS seguranca_cibernetica(id INT AUTO_INCREMENT PRIMARY KEY, senha_forte VARCHAR(255), autenticacao VARCHAR(255), ativo BOOLEAN DEFAULT FALSE NOT NULL)")
    conexao.commit()
    cursor.close()
    conexao.close()

def criar_seguranca_cibernetica(seguranca_cibernetica):
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO seguranca_cibernetica (senha_forte, autenticacao) VALUES (%s, %s)", (seguranca_cibernetica.senha_forte, seguranca_cibernetica.autenticacao))
    conexao.commit()
    id_seguranca_cibernetica = cursor.lastrowid
    cursor.close()
    conexao.close()
    seguranca_cibernetica.id = id_seguranca_cibernetica
    return Seguranca_Cibernetica

def listar_segurancas():
    conexao = connector()
    cursor = conexao.cursor()
    # CAMBIO: Usamos seguranca_cibernetica y agregamos la columna 'ativo'
    cursor.execute("SELECT id, senha_forte, autenticacao, ativo FROM seguranca_cibernetica")
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def buscar_seguranca_cibernetica_por_id(id_seguranca_cibernetica):
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, senha_forte, autenticacao, ativo FROM seguranca_cibernetica WHERE id = %s", (id_seguranca_cibernetica,))
    linha = cursor.fetchone()
    cursor.close()
    conexao.close()
    return linha

def actualizar_seguranca(id_seguranca, senha_forte, autenticacao, ativo):
    conexao = connector()
    cursor = conexao.cursor()
    query = "UPDATE seguranca_cibernetica SET senha_forte = %s, autenticacao = %s, ativo = %s WHERE id = %s"
    cursor.execute(query, (senha_forte, autenticacao, ativo, id_seguranca))
    conexao.commit()
    cursor.close()
    conexao.close()

def inserir_seguranca(senha_forte, autenticacao, ativo):
    conexao = connector()
    cursor = conexao.cursor()
    # CAMBIO: Agregamos el campo 'ativo' al INSERT
    query = "INSERT INTO seguranca_cibernetica (senha_forte, autenticacao, ativo) VALUES (%s, %s, %s)"
    cursor.execute(query, (senha_forte, autenticacao, ativo))
    conexao.commit()
    cursor.close()
    conexao.close()

def deletar_seguranca(id_seguranca):
    conexao = connector()
    cursor = conexao.cursor()
    # CAMBIO: Usamos la tabla correcta
    cursor.execute("DELETE FROM seguranca_cibernetica WHERE id = %s", (id_seguranca,))
    conexao.commit()
    cursor.close()
    conexao.close()