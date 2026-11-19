from flask import Flask, render_template, redirect, url_for, request
from db import db
from models import Produto, Categoria

from routes.routes import produtos_bp

app = Flask(__name__)

# CONFIGURAÇÕES
app.secret_key = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"

# BANCO DE DADOS
db.init_app(app)


# =========================
# BLUEPRINTS
# =========================

app.register_blueprint(produtos_bp)


# PÁGINA INICIAL
@app.route('/')
def home():

    produtos = Produto.query.all()
    categorias = Categoria.query.all()

    return render_template(
        'index.html',
        produtos=produtos,
        categorias=categorias,
        busca=''
    )


# INICIAR SISTEMA
if __name__ == '__main__':
    app.run(debug=True)