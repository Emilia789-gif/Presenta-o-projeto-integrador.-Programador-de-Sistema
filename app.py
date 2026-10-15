from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.usuario import Usuario
from models.bitacora import Bitacora
from models.vulnerabilidade import Vulnerabilidade
from models.defensa_guardiao_da_red.linha_do_tempo import Linha_de_tempo
from models.defensa_guardiao_da_red.ponto_cego import Pontocego
from models.defensa_guardiao_da_red.seguro import Seguro
from models.defensa_guardiao_da_red.rastreador import Alerta_automatica
from repositorio import bitacora_repository, seguranca_repository, vulnerabilidade_repository, usuario_repository

app = Flask(__name__)
app.secret_key = 'seguridadderedes@5.$%@'

def login_required(funcao):
    @wraps(funcao)
    def verificar(*args, **kwargs):
        if 'id_usuario' not in session:
            return redirect(url_for('login'))
        else:
            return funcao(*args, **kwargs)
    return verificar
    
@app.route('/cadastro', methods = ['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome  = request.form ['nome']
        email = request.form ['email']
        senha = request.form ['senha']
        usuario_existente = usuario_repository.buscar_usuario_por_email(email)
        if usuario_existente is not None:
            return render_template('cadastro.html', error = 'Este e-mail já esta cadastrado!')
        senha_hash = generate_password_hash(senha)
        usuario_existente = Usuario(nome, email, senha_hash)
        usuario_repository.criar_usuario(usuario_existente)
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form ['email']
        senha = request.form ['senha']
        usuario = usuario_repository.buscar_usuario_por_email(email)
        print(f"DEBUG 2-Usuario encontrado: '{usuario}'")
        if usuario and check_password_hash(usuario.senha, senha):
            session['id_usuario'] = usuario.id
            return redirect(url_for('painel'))
        else:
            return render_template('login.html', error = 'E-mail ou senha inválido.')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('id_usuario', None)
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    id_usuario = session.get('id_usuario')
    usuario = usuario_repository.buscar_usuario_por_id(id_usuario)
    listar_usuarios = usuario_repository.listar_todos_usuarios()
    return render_template('admin.html', usuario = usuario, usuarios = listar_usuarios)

@app.route('/painel')
@login_required
def painel():
    print("SESSION:", dict(session))
    usuario = usuario_repository.buscar_usuario_por_email(session['id_usuario'])
    print("USUARIO:", usuario)
    return render_template('painel.html', usuario = usuario)

@app.route('/editar_usuario/<int:id_usuario>', methods = ['GET', 'POST'])
@login_required
def  editar_usuario(id_usuario):
    usuario = usuario_repository.buscar_usuario_por_id(id_usuario)
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        usuario_repository.atualizar_usuario(id_usuario, nome, email, senha)
        return redirect(url_for('painel'))
    return render_template('editar_usuario.html', usuario = usuario)

@app.route('/excluir_usuario/<int:id_usuario>')
@login_required
def excluir_usuario(id_usuario):
    usuario_repository.deletar_usuario(id_usuario)
    return redirect(url_for('admin'))

# --- 1. RUTA PARA LISTAR (Não leva ID) ---
@app.route('/seguranca')
@login_required
def seguranca():
    lista_segurancas = seguranca_repository.listar_segurancas()
    # Nota: En el HTML usaremos el nombre de variable 'seguranca_cibernetica'
    return render_template('seguranca.html', seguranca_cibernetica=lista_segurancas)

@app.route('/seguranca/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_seguranca():
    if request.method == 'POST':
        senha_forte = request.form['senha_forte']
        autenticacao = request.form['autenticacao']
        
        # Capturamos el texto del formulario
        ativo_texto = request.form.get('ativo', 'Não')
        # Convertimos a número: 1 si es 'Sim', 0 si es 'Não'
        ativo = 1 if ativo_texto == 'Sim' else 0
        
        seguranca_repository.inserir_seguranca(senha_forte, autenticacao, ativo)
        return redirect(url_for('seguranca'))
        
    return render_template('cadastrar_seguranca.html')

@app.route('/seguranca/<int:id_seguranca>', methods=['GET', 'POST'])
@login_required
def editar_seguranca(id_seguranca):
    registro = seguranca_repository.buscar_seguranca_cibernetica_por_id(id_seguranca)
    
    if request.method == 'POST':
        senha_forte = request.form['senha_forte']
        autenticacao = request.form['autenticacao']
        
        # Capturamos el texto y lo convertimos a número
        ativo_texto = request.form.get('ativo', 'Não')
        ativo = 1 if ativo_texto == 'Sim' else 0
        
        seguranca_repository.actualizar_seguranca(id_seguranca, senha_forte, autenticacao, ativo)
        return redirect(url_for('seguranca'))
        
    return render_template('editar_seguranca.html', seguranca=registro)

@app.route('/seguranca/deletar/<int:id_seguranca>')
@login_required
def deletar_seguranca(id_seguranca):
    # Llama al repositorio para borrar el registro
    seguranca_repository.deletar_seguranca(id_seguranca)
    # Redirige de vuelta a la lista general
    return redirect(url_for('seguranca'))

# --- 1. RUTA PARA LISTAR (No lleva ID) ---
@app.route('/bitacora')
@login_required
def bitacora():
    # Llama al repositorio sin pasarle argumentos
    lista_bitacoras = bitacora_repository.listar_bitacoras()
    return render_template('bitacora.html', bitacoras=lista_bitacoras)

# --- 2. RUTA PARA EDITAR (Sí lleva ID en la URL) ---
@app.route('/bitacora/<int:id_bitacora>', methods=['GET', 'POST'])
@login_required
def editar_bitacora(id_bitacora):
    # Busca el registro específico
    bitacora = bitacora_repository.buscar_bitacora_por_id(id_bitacora)
    
    if request.method == 'POST':
        usuario = request.form['usuario']
        acao = request.form['acao']
        data = request.form['data']
        
        # Actualiza usando el ID directamente
        bitacora_repository.actualizar_bitacora(id_bitacora, usuario, acao, data)
        
        # Redirige a la lista general
        return redirect(url_for('bitacora'))
        
    # Si es GET, muestra el formulario con los datos
    return render_template('editar_bitacora.html', bitacora=bitacora)

@app.route('/bitacora/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_bitacora():
    if request.method == 'POST':
        usuario = request.form['usuario']
        acao = request.form['acao']
        data = request.form['data']
        
        # Llama al repositorio para guardar los datos
        bitacora_repository.inserir_bitacora(usuario, acao, data)
        
        # Redirige a la lista general
        return redirect(url_for('bitacora'))
        
    # Si es GET, muestra el formulario vacío
    return render_template('cadastrar_bitacora.html')

# --- 1. FUNCIÓN PARA LISTAR (Esta NO lleva ID) ---
@app.route('/vulnerabilidade')
@login_required
def vulnerabilidade():
    lista_vulnerabilidades = vulnerabilidade_repository.listar_vulnerabilidades()
    return render_template('vulnerabilidade.html', vulnerabilidades=lista_vulnerabilidades)

# --- 2. FUNCIÓN PARA EDITAR (Esta SÍ lleva ID) ---
@app.route('/vulnerabilidade/<int:id_vulnerabilidade>', methods=['GET', 'POST'])
@login_required
def editar_vulnerabilidade(id_vulnerabilidade):
    vulnerabilidade = vulnerabilidade_repository.buscar_vulnerabilidade_por_id(id_vulnerabilidade)
    
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        impacto = request.form['impacto']
        
        vulnerabilidade.nome = nome
        vulnerabilidade.descricao = descricao
        vulnerabilidade.impacto = impacto
        
        vulnerabilidade_repository.actualizar_vulnerabilidade(vulnerabilidade)
        return redirect(url_for('vulnerabilidade'))
        
    return render_template('editar_vulnerabilidade.html', vulnerabilidade=vulnerabilidade)

@app.route('/vulnerabilidade/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_vulnerabilidade():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        impacto = request.form['impacto']
        
        # Llama al repositorio para guardar los datos
        vulnerabilidade_repository.inserir_vulnerabilidade(nome, descricao, impacto)
        
        # Redirige a la lista general
        return redirect(url_for('vulnerabilidade'))
        
    # Si es GET, muestra el formulario vacío
    return render_template('cadastrar_vulnerabilidade.html')

@app.route('/defensa_guardiao_da_red/<int:id_seguranca_cibernetica>', methods=['GET', 'POST'])
@login_required
def defensa_guardiao_da_red(id_seguranca_cibernetica):
    # 1. Busca el registro en la base de datos
    seguranca = seguranca_repository.buscar_seguranca_cibernetica_por_id(id_seguranca_cibernetica)
    
    if seguranca is None:
        return redirect(url_for('seguranca'))

    # 2. Si el usuario envió el formulario (POST), actualiza
    if request.method == 'POST':
        senha_forte = request.form.get('senha_forte')
        autenticacao = request.form.get('autenticacao')
        
        # ⚠️ AQUÍ ESTÁ LA CORRECCIÓN: Convertimos el texto a número
        ativo_texto = request.form.get('ativo', 'Não').strip().lower() # Quita espacios y pone en minúscula
        ativo = 1 if ativo_texto == 'sim' else 0
        
        # Guardamos en la base de datos (ahora 'ativo' es 1 o 0)
        seguranca_repository.actualizar_seguranca(id_seguranca_cibernetica, senha_forte, autenticacao, ativo)
        
        return redirect(url_for('seguranca'))

    # 3. Si es GET, muestra el formulario con los datos actuales
    return render_template('defensa_guardiao_da_red.html', seguranca=seguranca)



if __name__ == '__main__':
    bitacora_repository.tabela_bitacora()
    seguranca_repository.tabela_seguranca_cibernetica()
    usuario_repository.tabela_usuario()
    vulnerabilidade_repository.tabela_vulnerabilidade()
    app.run(debug=True)