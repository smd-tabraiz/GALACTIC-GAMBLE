from flask import Flask, jsonify, render_template, request
import json

app = Flask(__name__)

def load_data():
    with open("data.json") as f:
        return json.load(f)

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scores")
def scores():
    data = load_data()
    data.sort(key=lambda x: (-x["gold"], -x["points"]))
    return jsonify(data)

@app.route("/update", methods=["POST"])
def update():
    name = request.json["name"]
    bid = request.json["bid"]
    correct = request.json["correct"]

    data = load_data()

    for p in data:
        if p["name"] == name:
            p["points"] -= bid
            if correct:
                p["gold"] += 1
            break

    save_data(data)
    return {"status": "updated"}

if __name__ == "__main__":
    app.run(debug=True)
