from database.db import conectar
from models.seguranca_cibernetica import SegurancaCibernetica

def tabela_seguranca_cibernetica():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS seguranca_cibernetica(id INT AUTO_INCREMENT PRIMARY KEY, senha_forte VARCHAR(255), autenticacao VARCHAR(255), ativo BOOLEAN DEFAULT FALSE NOT NULL)")
    conexao.commit()
    cursor.close()
    conexao.close()

def criar_seguranca_cibernetica(seguranca_cibernetica):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("CREATE INTO seguranca_cibernetica (senha_forte, autenticacao) VALUES (%s, %s)", (seguranca_cibernetica.senha_forte, seguranca_cibernetica.autenticacao))
    conexao.commit()
    id_seguranca_cibernetica = cursor.lastrowid
    cursor.close()
    conexao.close()
    seguranca_cibernetica.id = id_seguranca_cibernetica
    return SegurancaCibernetica

def listar_seguranca_cibernetica():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM seguranca_cibernetica")
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def buscar_seguranca_cibernetica_por_id(id_seguranca):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM seguranca_cibernetica WHERE id = %s", (id_seguranca,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado

def atualizar_seguranca_cibernetica(seguranca_cibernetica):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE seguranca_cibernetica SET senha_forte = %s, autenticacao = %s WHERE id = %s", (seguranca_cibernetica.senha_forte, seguranca_cibernetica.autenticacao, seguranca_cibernetica.id))
    conexao.commit()
    cursor.close()
    conexao.close()
    return SegurancaCibernetica

def deletar_seguranca_cibernetica(id_seguranca):
    conexao = conectar
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM seguranca_cibernetica WHERE id = %s", (id_seguranca,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return True