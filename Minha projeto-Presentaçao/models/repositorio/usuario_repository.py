from database.db import conectar
from models.usuario import Usuario 

def tabela_usuario():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS usuario (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), email VARCHAR(255) UNIQUE, senha VARCHAR(255)NOT NULL)")
    conexao.commit()
    cursor.close()
    conexao.close()

def criar_usuario(usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)", (usuario.nome, usuario.email, usuario.senha))
    conexao.commit()
    id_usuario = cursor.lastrowid
    cursor.close()
    usuario.id = id_usuario
    return usuario

def buscar_usuario_por_email(email):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, email, senha FROM usuario WHERE email = %s", (email,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    if resultado:
        id_usuario, nome, email, senha = resultado
        usuario = Usuario(nome, email, senha)
        usuario.id = id_usuario
        return usuario
    return None

def buscar_senha_por_email(email):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT senha FROM usuario WHERE email = %s", (email,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    if resultado:
        return resultado[0]
    return None

def buscar_usuario_por_id(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, email, senha FROM usuario WHERE id = %s", (id_usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    if resultado is None:
        return None
    else:
        id_usuario, nome, email, senha = resultado
        usuario = Usuario(nome, email, senha)
        usuario.id = id_usuario
        return usuario 