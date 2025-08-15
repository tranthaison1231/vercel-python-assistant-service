from flask import Flask
from api.controllers.youtube_controller import youtube_bp
from api.controllers.crypto_controller import crypto_bp
from api.controllers.tech_controller import tech_bp
from api.controllers.gold_controller import gold_bp
from api.controllers.real_estate_controller import real_estate_bp
from api.controllers.github_controller import github_bp

app = Flask(__name__)

app.register_blueprint(youtube_bp)
app.register_blueprint(crypto_bp)
app.register_blueprint(tech_bp)
app.register_blueprint(gold_bp)
app.register_blueprint(real_estate_bp)
app.register_blueprint(github_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
