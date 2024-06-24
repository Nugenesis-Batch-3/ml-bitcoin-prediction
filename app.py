from flask import Flask
from api.routes.predict import predict_bp
from api.routes.train import train_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(predict_bp, url_prefix="/predict")
app.register_blueprint(train_bp, url_prefix="/train")


@app.route("/")
def home():
    return "Welcome to the Bitcoin Prediction API!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
