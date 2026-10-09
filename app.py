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
from repositorio import usuario_repository
from repositorio import bitacora_repository, seguranca_repository, vulnerabilidade_repository, usuario_repository

app = Flask(__name__)
app.secret_key = 'seguridadderedes@5.$%@'

def login_required(funcao):
    @wraps(funcao)
    def verificar(*args, **kwargs):
        if 'id_usuario' not in session:
            return redirect(url_for('login'))
        else:
            return(*args, *kwargs)
    return verificar
    
@app.route('/cadastro', methods = ['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome  = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        usuario_existente = usuario_repository.buscar_usuario_por_email(email)
        if usuario_existente:
            return render_template('cadastro.html', error = 'Este e-mail já esta cadastrado!')
        senha = generate_password_hash(senha)
        usuario_existente = Usuario(nome, email, senha)
        usuario_repository.salvar_usuario(nome, email, senha)
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request['email']
        senha = request['senha']
        usuario = usuario_repository.buscar_usuario_por_email(email)
        if usuario and check_password_hash(usuario.senha, senha):
            session['id_usuario'] = usuario.id
            return redirect(url_for('panel'))
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

@app.route('/panel')
@login_required
def painel():
    usuario = usuario_repository.buscar_usuario_por_email(session['usuario.id'])
    return render_template('painel.html', usuario = usuario)

@app.route('/seguranca_cibernetica')
@login_required
def seguranca_cibernetica():
    listar_seguranca_cibernetica = seguranca_repository.listar_seguranca_cibernetica()
    return render_template('seguranca.html', seguranca_cibernetica = listar_seguranca_cibernetica)

@app.route('/seguranca_cibernetica/<int:id_seguranca>', methods = ['GET', 'POST'])
@login_required
def seguranca_cibernetica(id_seguranca):
    seguranca = seguranca_repository.buscar_seguranca_cibernetica_por_id(id_seguranca)
    if request.method == 'POST':
        senha_forte = request.form['senha_forte']
        autenticacao = request.form['autenticacao']
        seguranca.senha_forte = senha_forte
        seguranca.autenticacao = autenticacao
        seguranca_repository.atualizar_seguranca_cibernetica(seguranca)
        return redirect(url_for('seguranca_cibernetica'))
    return render_template('editar_seguranca.html', seguranca = seguranca)

@app.route('/seguranca_cibernetica/deletar/<int:id_seguramca>', methods = ['GET', 'POST'])
@login_required
def deletar_seguranca_cibernetica(id_seguranca):
    if request.method == 'POST':
        seguranca_repository.deletar_seguranca_cibernetica(id_seguranca)
        return redirect(url_for('seguranca_cibernetica'))
    return redirect(url_for('seguranca_cibernetica'))

@app.route('/bitacora/<int:id_bitacora>', methods = ['GET', 'POST'])
@login_required
def editar_bitacora(id_bitacora):
    bitacora = bitacora_repository.buscar_bitacora_por_id(id_bitacora)
    if request.method == 'POST':
        usuario = request.form['usuario']
        acao = request.form['acao']
        data = request.form['data']
        bitacora.usuario = usuario
        bitacora.acao = acao
        bitacora.data = data
        bitacora = Bitacora(usuario,acao, data)
        bitacora_repository.actualizar_bitacora(bitacora)
        return redirect(url_for('bitacora'))
    return render_template('editar_bitacora.html', bitacora = bitacora)


@app.route('/vulnerabilidade/<int:id_vulnerabilidade>', methods = ['GET', 'POST'])
@login_required
def editar_vulnerabilidad(id_vulnerabilidade):
    vulnerabilidade = vulnerabilidade_repository.buscar_vulnerabilidade_por_id(id_vulnerabilidade)
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form ['descricao']
        impacto = request.form['impacto']
        vulnerabilidade.nome = nome
        vulnerabilidade.descricao = descricao
        vulnerabilidade.impacto = impacto
        vulnerabilidade = Vulnerabilidade(nome, descricao, impacto)
        vulnerabilidade_repository.atualizar_vulnerabilidade(vulnerabilidade)
        return redirect(url_for('vulnerabilidade'))
    return render_template('editar_vulnerabilidade.html', vulnerabilidade = vulnerabilidade)

@app.route('/seguranca_cibernetica/<int:id_seguranca_cibernetica>/defesa_guardiao_da_red', methods=['GET', 'POST'])
@login_required
def defesa_guardiao_da_red(id_seguranca_cibernetica):

    seguranca = seguranca_repository.buscar_seguranca_cibernetica_por_id(id_seguranca_cibernetica)
    
    if seguranca is None:
        return redirect(url_for('seguranca_cibernetica'))
    
    if request.method == 'POST':
        seguranca.localizacao = request.form.get('localizacao')
        seguranca.monitoreo_de_patrones_de_inyeccao = request.form.get('monitoreo_de_patrones_de_inyeccao')
        seguranca.shadow_IT = request.form.get('shadow_IT')
        seguranca.registro = request.form.get('registro')
        seguranca.alerta_de_tempo_real = request.form.get('alerta_de_tempo_real')
        seguranca.linha_de_tempo = request.form.get('linha_de_tempo')
        seguranca.ponto_cego = request.form.get('ponto_cego')
        seguranca.rastreador = request.form.get('rastreador')
        seguranca.seguro = request.form.get('seguro')
    
        seguranca_repository.atualizar_seguranca_cibernetica(seguranca)
        
        return redirect(url_for('seguranca_cibernetica'))

    return render_template('defesa_guardiao_da_red.html', seguranca=seguranca)

if __name__ == '__main__':
    bitacora_repository.tabela_bitacora()
    seguranca_repository.tabela_seguranca_cibernetica()
    usuario_repository.tabela_usuario()
    vulnerabilidade_repository.tabela_vulnerabilidade()
    app.run(debug=True)