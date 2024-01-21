from flask import Flask, render_template, redirect, url_for, request
import config
from apps import auth
from apps.contractUs import contractUs_bp
from apps.gifts import gifts_bp
from apps.home import home_bp
from apps.movies import movies_bp
from apps.promotions import promotions_bp

app = Flask(__name__)
app.config.from_object(config)
auth.init_app(app)
app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(promotions_bp, url_prefix='/promotions')
app.register_blueprint(movies_bp, url_prefix='/movies')
app.register_blueprint(gifts_bp, url_prefix='/gifts')
app.register_blueprint(contractUs_bp, url_prefix='/contractUs')


# Homepage
@app.route('/')
def home():
    return redirect(url_for('home.index'))

@app.context_processor
def inject_globals():
    return dict(req=request)


if __name__ == '__main__':
    app.run()
