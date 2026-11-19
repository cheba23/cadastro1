from db import db

class Produto(db.Model):
    __tablename__ = 'produto'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)

    # Nome do arquivo do prouduto
    imagem = db.Column(
        db.String(255),
        nullable=False,
        default='padrao.png'
    )

    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey('categoria.id'),
        nullable=False
    )

    categoria = db.relationship(
        'Categoria',
        backref='produto'
    )


class Categoria(db.Model):
    __tablename__ = 'categoria'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)

