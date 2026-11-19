
import os
import uuid

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, current_app
)

from werkzeug.utils import secure_filename

from sqlalchemy.exc import SQLAlchemyError

from models import Produto, Categoria
from db import db


produtos_bp = Blueprint('produtos', __name__)

EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'webp'}


# VERIFICAR EXTENSÃO DA IMAGEM
def extensao_permitida(nome_arquivo):

    return (
        '.' in nome_arquivo
        and nome_arquivo.rsplit('.', 1)[1].lower()
        in EXTENSOES_PERMITIDAS
    )


# CAMINHO DA PASTA DE UPLOADS
def pasta_uploads():

    pasta = os.path.join(
        current_app.root_path,
        'static',
        'uploads'
    )

    os.makedirs(pasta, exist_ok=True)

    return pasta


# CADASTRAR PRODUTO
@produtos_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():

    categorias = Categoria.query.all()

    if request.method == 'GET':
        return render_template(
            'index.html',
            categorias=categorias
        )

    nome = request.form.get('nomeForm', '').strip()
    preco_form = request.form.get('precoForm', '').strip()
    categoria_form = request.form.get('categoria_id', '').strip()

    if not nome or not preco_form or not categoria_form:

        flash('Preencha todos os campos obrigatórios.', 'erro')

        return redirect(url_for('home'))

    try:

        preco = float(preco_form)
        categoria_id = int(categoria_form)

    except ValueError:

        flash('Preço ou categoria inválidos.', 'erro')

        return redirect(url_for('home'))

    if preco < 0:

        flash('O preço não pode ser negativo.', 'erro')

        return redirect(url_for('home'))

    categoria = db.session.get(Categoria, categoria_id)

    if not categoria:

        flash('Categoria não encontrada.', 'erro')

        return redirect(url_for('home'))

    arquivo = request.files.get('campo_imagem')

    nome_imagem = 'padrao.png'

    caminho_imagem = None

    if arquivo and arquivo.filename:

        if not extensao_permitida(arquivo.filename):

            flash('Formato inválido! Envie PNG, JPG, JPEG ou WEBP.', 'erro')

            return redirect(url_for('home'))

        nome_seguro = secure_filename(arquivo.filename)

        if not nome_seguro:

            flash('Nome de arquivo inválido.', 'erro')

            return redirect(url_for('home'))

        nome_imagem = f'{uuid.uuid4().hex}_{nome_seguro}'

        caminho_imagem = os.path.join(
            pasta_uploads(),
            nome_imagem
        )

        try:
            arquivo.save(caminho_imagem)

        except OSError:

            flash('Erro ao salvar a imagem.', 'erro')

            return redirect(url_for('home'))

    novo_produto = Produto(
        nome=nome,
        preco=preco,
        categoria_id=categoria_id,
        imagem=nome_imagem
    )

    try:

        db.session.add(novo_produto)
        db.session.commit()

    except SQLAlchemyError:

        db.session.rollback()

        if caminho_imagem and os.path.exists(caminho_imagem):
            os.remove(caminho_imagem)

        flash('Erro ao cadastrar produto.', 'erro')

        return redirect(url_for('home'))

    flash('Produto cadastrado com sucesso!', 'sucesso')

    return redirect(url_for('home'))


# EDITAR PRODUTO
@produtos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):

    produto = db.session.get(Produto, id)

    if not produto:

        flash('Produto não encontrado.', 'erro')

        return redirect(url_for('home'))

    categorias = Categoria.query.all()

    if request.method == 'GET':

        return render_template(
            'editar_produtos.html',
            produto=produto,
            categorias=categorias
        )

    nome = request.form.get('nomeForm', '').strip()
    preco_form = request.form.get('precoForm', '').strip()
    categoria_form = request.form.get('categoria_id', '').strip()

    if not nome or not preco_form or not categoria_form:

        flash('Preencha todos os campos obrigatórios.', 'erro')

        return redirect(url_for('produtos.editar', id=id))

    try:

        preco = float(preco_form)
        categoria_id = int(categoria_form)

    except ValueError:

        flash('Preço ou categoria inválidos.', 'erro')

        return redirect(url_for('produtos.editar', id=id))

    if preco < 0:

        flash('O preço não pode ser negativo.', 'erro')

        return redirect(url_for('produtos.editar', id=id))

    categoria = db.session.get(Categoria, categoria_id)

    if not categoria:

        flash('Categoria não encontrada.', 'erro')

        return redirect(url_for('produtos.editar', id=id))

    produto.nome = nome
    produto.preco = preco
    produto.categoria_id = categoria_id

    arquivo = request.files.get('campo_imagem')

    caminho_nova_imagem = None
    imagem_antiga = produto.imagem

    if arquivo and arquivo.filename:

        if not extensao_permitida(arquivo.filename):

            flash('Formato de imagem inválido.', 'erro')

            return redirect(url_for('produtos.editar', id=id))

        nome_seguro = secure_filename(arquivo.filename)

        if not nome_seguro:

            flash('Nome de arquivo inválido.', 'erro')

            return redirect(url_for('produtos.editar', id=id))

        nome_imagem = f'{uuid.uuid4().hex}_{nome_seguro}'

        caminho_nova_imagem = os.path.join(
            pasta_uploads(),
            nome_imagem
        )

        try:
            arquivo.save(caminho_nova_imagem)

        except OSError:

            flash('Erro ao salvar a nova imagem.', 'erro')

            return redirect(url_for('produtos.editar', id=id))

        produto.imagem = nome_imagem

    try:

        db.session.commit()

    except SQLAlchemyError:

        db.session.rollback()

        if caminho_nova_imagem and os.path.exists(caminho_nova_imagem):
            os.remove(caminho_nova_imagem)

        flash('Erro ao atualizar produto.', 'erro')

        return redirect(url_for('produtos.editar', id=id))

    # REMOVER IMAGEM ANTIGA APÓS SALVAR
    if caminho_nova_imagem and imagem_antiga and imagem_antiga != 'padrao.png':

        caminho_antigo = os.path.join(
            pasta_uploads(),
            imagem_antiga
        )

        if os.path.exists(caminho_antigo):

            try:
                os.remove(caminho_antigo)

            except OSError:
                current_app.logger.exception(
                    'Não foi possível remover a imagem antiga.'
                )

    flash('Produto atualizado com sucesso!', 'sucesso')

    return redirect(url_for('home'))


# EXCLUIR PRODUTO
@produtos_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):

    produto = db.session.get(Produto, id)

    if not produto:

        flash('Produto não encontrado.', 'erro')

        return redirect(url_for('home'))

    imagem = produto.imagem

    try:

        db.session.delete(produto)
        db.session.commit()

    except SQLAlchemyError:

        db.session.rollback()

        flash('Erro ao excluir produto.', 'erro')

        return redirect(url_for('home'))

    # REMOVER IMAGEM DO PRODUTO
    if imagem and imagem != 'padrao.png':

        caminho_imagem = os.path.join(
            pasta_uploads(),
            imagem
        )

        if os.path.exists(caminho_imagem):

            try:
                os.remove(caminho_imagem)

            except OSError:
                current_app.logger.exception(
                    'Não foi possível remover a imagem do produto.'
                )

    flash('Produto excluído com sucesso!', 'sucesso')

    return redirect(url_for('home'))


# BUSCAR PRODUTOS
@produtos_bp.route('/buscar', methods=['GET'])
def buscar():

    busca = request.args.get('busca', '').strip()

    produtos = Produto.query.filter(
        Produto.nome.ilike(f'%{busca}%')
    ).all()

    categorias = Categoria.query.all()

    return render_template(
        'index.html',
        produtos=produtos,
        categorias=categorias,
        busca=busca
    )
