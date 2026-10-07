from database.db import conectar
from models.bitacora import Bitacora

def tabela_bitacora():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS bitacora (id INT AUTO_INCREMENT PRIMARY KEY, usuario VARCHAR(255), acao VARCHAR(255), data DATETIME NOT NULL)")
    conexao.commit()
    cursor.close()
    conexao.close()

def criar_bitacora(bitacora):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO bitacora (usuario, acao, data) VALUES (%s, %s, %s)", (bitacora.usuario, bitacora.acao, bitacora.data))
    conexao.commit()
    id_bitacora = cursor.lastrowid
    cursor.close()
    conexao.close()
    bitacora.id = id_bitacora
    return bitacora

def buscar_bitacora_por_usuario(usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, usuario, acao, data FROM bitacora WHERE usuario = %s", (usuario,))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [Bitacora(usuario, acao, data) for (id, usuario, acao, data) in resultados]

def buscar_bitacora_por_acao(acao):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, usuario, acao, data FROM bitacora WHERE acao = %s", (acao,))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [Bitacora(usuario, acao, data) for (id, usuario, acao, data) in resultados]

def buscar_bitacora_por_data(data):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, usuario, acao, data FROM bitacora WHERE data = %s", (data,))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [Bitacora(usuario, acao, data) for (id, usuario, acao, data) in resultados]

def actualizar_bitacora(id_bitacora, usuario, acao, data):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "UPDATE bitacora SET usuario = %s, acao = %s, data = %s WHERE id = %s" 
    valores = (usuario, acao, data, id_bitacora)
    cursor.execute(sql, valores)
    conexao.commit()
    cursor.close()
    conexao.close()

def buscar_bitacora_por_id(id_bitacora):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, usuario, acao, data FROM bitacora WHERE id = %s", (id_bitacora,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado