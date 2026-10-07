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
from models.repositorio import seguranca_repository, usuario_repository, bitacora_repository, vulnerabilidade_repository

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
        senha = generate_password_hash(request.form['senha'])
        if usuario_repository.buscar_usuario_por_email(email) is not None:
            return render_template('cadastro.html', error= 'Este e-mail já esta cadastro.')
        else:
            usuario = Usuario(nome, email, senha)
            usuario_repository.criar_usuario(usuario)
            return redirect(url_for('login'))
    else:
        return render_template('cadastro.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request['email']
        senha = request['senha']
        usuario = usuario_repository.buscar_usuario_por_email(email)
        if usuario and check_password_hash(usuario._senha, senha):
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
def editar_seguranca_cibernetica(id_seguranca):
    seguranca = seguranca_repository.buscar_seguranca_cibernetica_por_id(id_seguranca)
    if request.method == 'POST':
        senha_forte = request.form['senha_forte']
        autenticacao = request.form['autenticacao']
        seguranca.senha_forte = senha_forte
        seguranca.autenticacao = autenticacao
        seguranca_repository.atualizar_seguranca_cibernetica(seguranca)
        return redirect(url_for('seguranca_cibernetica'))
    return render_template('editar_seguranca.html', seguranca = seguranca)

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
        bitacora_repository.actualizar_bitacora(id_bitacora)
        return redirect(url_for('Bitacora'))
    return render_template('editar_bitacora.html')

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

@app.route('/seguraca_cibernetica/<int:id_seguranza_cibernetica>/defensa_guardiao_da_red')
@login_required
def defensa_guardiao_da_red(id_seguranca_cibernetica):
    seguranca = seguranca_repository.buscar_seguranca_cibernetica_por_id(id_seguranca_cibernetica)
    if seguranca is None:
        return redirect(url_for('seguranca_cibernetica'))
    if request.method == 'POST':
        localizacao = request.form.get('localizacao')
        monitoreo_de_patrones_de_inyeccao = request.form.get('monitoreo_de_patrones_de_inyeccao')
        shadow_IT = request.form.get('shadow_IT')
        registro = request.form.get('registro')
        alerta_de_tempo_real = request.form.get('alerta_de_tempo_real')
        linha_de_tempo = request.form.get('linha_de_tempo')
        ponto_cego = request.form.get('ponto_cego')
        rastreador = request.form.get('rastreador')
        seguro = request.form.get('seguro')

        seguranca.linha_de_tempo = linha_de_tempo
        seguranca.ponto_cego = ponto_cego
        seguranca.rastreador = rastreador
        seguranca.seguro = seguro
        seguranca = Linha_de_tempo(localizacao, monitoreo_de_patrones_de_inyeccao, registro)
        seguranca = Pontocego(localizacao, monitoreo_de_patrones_de_inyeccao, shadow_IT)
        seguranca = Seguro(localizacao, monitoreo_de_patrones_de_inyeccao, alerta_de_tempo_real)
        seguranca = Alerta_automatica(localizacao, monitoreo_de_patrones_de_inyeccao)
        seguranca_repository.atualizar_seguranca_cibernetica(seguranca_cibernetica)
        return redirect(url_for('seguranca_cibernetica'))
    return render_template('defensa_guardiao_da_red.html', seguranca = seguranca)

if __name__ == '__main__':
    bitacora_repository.tabela_bitacora()
    seguranca_repository.tabela_seguranca_cibernetica()
    usuario_repository.tabela_usuario()
    vulnerabilidade_repository.tabela_vulnerabilidade()
    app.run(debug=True)