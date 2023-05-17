import os

from flask import Flask
from flask import render_template
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)


    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route("/")
    def index():
        return render_template("base.html")

    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(410)
    def page_not_found(e):
        return "ERROR, please login again"

    from banker import db
    db.init_app(app)
    from banker import auth,bank
    app.register_blueprint(auth.bp)
    app.register_blueprint(bank.bp)
    app.add_url_rule("/", endpoint="index")

    return app
