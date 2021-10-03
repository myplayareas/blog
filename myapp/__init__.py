import os

from flask import Flask
from . import db
from . import auth
from . import blog

def create_app(teste_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'blog.sqlite')
    )

    if (teste_config is None):
        # Carrega a instancia de configuracao
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Carrega a configuracao de teste
        app.config.from_mapping(teste_config)

    # garante que a pasta da instancia existe
    try:
        print(f'app.instance_path: {app.instance_path}')
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializa a conexao com o banco
    db.init_app(app)

    # Registra o blueprint de autenticao (auth)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    @app.route('/')
    def hello_page():
        return 'Hello flask via __init__'

    return app