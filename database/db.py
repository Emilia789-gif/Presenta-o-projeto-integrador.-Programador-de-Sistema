from asyncio import open_connection

import mysql.connector

def connector():
    conexao = mysql.connector.connect(
        host="localhost",
        user= "root",
        password= "root",
        database= "projeto"
    )
    return conexao

def tabela_segurança_cibernetica():
    conexao = connector()
    cursor = conexao.cursor()
    criar_tabela_segurança_cibernetica = "CREATE TABLE IF NOT EXISTS segurança_cibernetica(id INT AUTO_INCREMENT PRIMARY KEY, senha_forte VARCHAR(100) NOT NULL, autenticaçao VARCHAR(100) NOT NULL, ativo BOOLEAN DEFAULT FALSE NOT NULL)"
    cursor.execute(criar_tabela_segurança_cibernetica)
    conexao.commit()
    conexao.close()

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
    return resultados

def buscar_bitacora_por_acao(acao):
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, usuario, acao, data FROM bitacora WHERE acao = %s", (acao,))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def buscar_bitacora_por_data(data):
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, usuario, acao, data FROM bitacora WHERE data = %s", (data,))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def buscar_bitacora_por_id(id_bitacora):
    conexao = connector()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, usuario, acao, data FROM bitacora WHERE id = %s", (id_bitacora,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado

def actualizar_bitacora(id_bitacora, usuario, acao, data):
    conexao = connector()
    cursor = conexao.cursor()
    sql = "UPDATE bitacora SET usuario = %s, acao = %s, data = %s WHERE id = %s" 
    valores = (usuario, acao, data, id_bitacora)
    cursor.execute(sql, valores)
    conexao.commit()
    cursor.close()
    conexao.close()

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

def buscar_vulnerabilidade_por_descricao(descripcao):
    conexao = connector()
    cursor = conexao.cursor(dictionary = True)
    query = "SELECT * FROM vulnerabilidade WHERE descricao LIKE %s"
    cursor.execute(query, ('%' + descripcao + '%',))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado

def atualizar_vulnerabilidade(vulnerabilidade):
    conexion = open_connection()
    cursor = conexion.cursor()
    query = "UPDATE vulnerabilidade SET nome = %s, descricao = %s, impacto = %s WHERE id = %s"
    cursor.execute(query(
        vulnerabilidade.nome,
        vulnerabilidade.descricao,
        vulnerabilidade.impacto,
        vulnerabilidade.id
    ))
    conexion.commit()
    cursor.close()
    conexion.close()