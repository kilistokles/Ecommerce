from mercado import app
from flask import render_template, redirect, url_for, flash, request
from mercado.models import Item, User
from mercado.forms import CadastroForm, LoginForm, CompraProdutoForm, VendaProdutoForm, CadastroProd
from mercado import db
from flask_login import login_user, logout_user, login_required, current_user
import os

#Decorator
@app.route('/')
def page_home():
   return render_template("home.html")

@app.route('/produtos', methods=["GET", "POST"])
@login_required
def page_produtos(): # renderizar produtos
    compra_form = CompraProdutoForm()
    venda_form = VendaProdutoForm()
    if request.method == "POST":
        # Compra Produto
        compra_form = request.form.get("compra_produto")
        produto_obj = Item.query.filter_by(nome=compra_form).first() # criar um filtro do banco para procurar o nome do produto.
        if produto_obj:
            if current_user.compra_disponivel(produto_obj):
                produto_obj.compra(current_user)
                flash(f"Parabes! voce efetuou a compra {produto_obj.nome}", category="success")
            else:
                flash(f"Voce nao possui saldo suficiente para comprar o produto {produto_obj.nome}", category="danger")
        # Venda Produto
        venda_form = request.form.get('venda_produto')
        produto_obj_venda = Item.query.filter_by(nome=venda_form).first()
        if produto_obj_venda:
            if current_user.venda_disponivel(produto_obj_venda):
                produto_obj_venda.venda(current_user)
                flash(f"Parabes! voce efetuou a venda {produto_obj_venda.nome}", category="success")
            else:
                flash(f"Algo deu erro na transação {produto_obj_venda.nome}", category="danger")
        return redirect(url_for('page_produtos'))
    if request.method == "GET":
        itens = Item.query.filter_by(dono=None)
        dono_itens = Item.query.filter_by(dono=current_user.id)
        return render_template("produtos.html", itens=itens, compra_form=compra_form, dono_itens=dono_itens, venda_form=venda_form)


@app.route('/cadastro', methods=['GET', 'POST'])
def page_cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        usuario = User(
            usuario = form.usuario.data,
            email = form.email.data,
            senhacrip = form.senha1.data
        )
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('page_produtos'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"Erro ao cadastrar usuario {err}", category="danger")
    return render_template("cadastro.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def page_login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario_logado = User.query.filter_by(usuario=form.usuario.data).first()
        if usuario_logado and usuario_logado.converte_senha(senha_texto_claro=form.senha.data):
            login_user(usuario_logado)
            flash(f'Sucesso! seu login e: {usuario_logado.usuario}', category='success')
            return redirect(url_for('page_produtos'))
        else:
            flash(f'Usuario ou senha estão incorretos! Tente novamente.', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def page_logout():
    logout_user()
    flash("Você fez o logout", category="info")
    return redirect(url_for("page_home"))

@app.route('/cadastro_prod', methods=['GET', 'POST'])
@login_required
def page_cadastroprod():
    form = CadastroProd()
    if form.validate_on_submit():
        item = Item(
            nome = form.nome.data,
            preco = form.preco.data,
            cod_barra = form.cod_barra.data,
            descricao = form.descricao.data
        )
        db.session.add(item)
        db.session.commit()


        return redirect(url_for('page_produtos'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"Erro ao cadastrar produto {err}", category="danger")
    return render_template("cadastro_prod.html", form=form)

@app.route('/exibir')
def page_exibir():
    return render_template("exibir.html")

@app.route('/conversor')
def page_conversor():
    return render_template("conversor.html")


# tudo que vim do banco de dados, para filtra usar o .first no final da consulta.
# Para finalizar a sessao dentro do banco de dados e usado o db.session.commit para salvar as alteracoes