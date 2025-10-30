import utils.logs as logs
from config.env.env import Env

from flask import Flask, request, jsonify
from flask_cors import CORS
from rest.handler import Handler

app = Flask(__name__)
env = Env()
handler = Handler()
CORS(app) 

@app.route("/generate_report", methods=['POST'])
def generate_report():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON provided"}), 400
    
    prompt = data.get("prompt", None)
    if prompt is None:
        return jsonify({
            "error": "you have no prompt to execute"
        }), 400
    else:
        try:
            res = handler.nl2sql(prompt)
            return jsonify(res), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 400
        

@app.route("/change_context", methods=['POST'])
def change_context():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON provided"}), 400
    
    # get data body
    body = {
        "id": data.get("id", None),
        "filters": data.get("filters", None),
        "order_by": data.get("order_by", None),
        "page": data.get("page", 1),
        "size": data.get("size", 10),
    }

    if body.get("id") is None:
        return jsonify({
            "error": "missing id-ctx, please check your payload"
        }), 400
    else:
        try:
            res = handler.change_context(body)
            return jsonify(res), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 400


if __name__ == "__main__":
    logs.write("info", "server is running..")
    app.run(host="0.0.0.0", port=env.APP_PORT, debug=True)
