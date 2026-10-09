from asyncio import open_connection

from database.db import connector
from models.bitacora import Bitacora

def tabela_bitacora():
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS bitacora (id INT AUTO_INCREMENT PRIMARY KEY, usuario VARCHAR(255), acao VARCHAR(255), data DATETIME NOT NULL)")
    conexao.commit()
    cursor.close()
    conexao.close()

def criar_bitacora(bitacora):
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO bitacora (usuario, acao, data) VALUES (%s, %s, %s)", (bitacora.usuario, bitacora.acao, bitacora.data))
    conexao.commit()
    id_bitacora = cursor.lastrowid
    cursor.close()
    conexao.close()
    bitacora.id = id_bitacora
    return bitacora

def buscar_bitacora_por_usuario(usuario):
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, usuario, acao, data FROM bitacora WHERE usuario = %s", (usuario,))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [Bitacora(usuario, acao, data) for (id, usuario, acao, data) in resultados]

def buscar_bitacora_por_acao(acao):
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, usuario, acao, data FROM bitacora WHERE acao = %s", (acao,))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [Bitacora(usuario, acao, data) for (id, usuario, acao, data) in resultados]

def buscar_bitacora_por_data(data):
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, usuario, acao, data FROM bitacora WHERE data = %s", (data,))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [Bitacora(usuario, acao, data) for (id, usuario, acao, data) in resultados]

def actualizar_bitacora(self, bitacora):
    conexion = open_connection()
    cursor = conexion.cursor()

    query = "UPDATE bitacora SET usuario = %s, acao = %s, data = %s WHERE id = %s"

    cursor.execute(query,(
        bitacora.usuario,
        bitacora.acao,
        bitacora.data,
        bitacora.id
    ))

    conexion.commit()
    cursor.close()
    conexion.close()

def buscar_bitacora_por_id(id_bitacora):
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, usuario, acao, data FROM bitacora WHERE id = %s", (id_bitacora,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado