import certifi
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = "mongodb+srv://seanfwarr14_db_user:IAv0UU1RGfuMs3lf@outfit-db.6ko6uho.mongodb.net/?appName=outfit-db"
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["outfits"]
clothes_collection = db["clothes"]

VALID_ACTIVITIES = {"school", "work", "going_out"}
VALID_WEATHER = {"hot", "warm", "cold", "rainy"}



def recommend_items(activity, weather):
    """Build a coherent outfit by picking the best item for each clothing slot."""
    items = list(clothes_collection.find({
        "weather_tags": weather,
        "$or": [
            {"activity_tags": activity},
            {"activity_tags": "any"},
        ]
    }))

    candidates = {}
    for item in items:
        score = 2 if activity in item["activity_tags"] else 1
        candidates.setdefault(item["type"], []).append((score, item))

    for slot in candidates:
        candidates[slot].sort(key=lambda x: x[0], reverse=True)

    outfit = []
    for slot in ["top", "bottom", "shoes", "outerwear"]:
        if slot not in candidates:
            continue
        best = candidates[slot][0][1]
        outfit.append({"name": best["name"], "type": best["type"], "image": best.get("image", "")})

    return outfit


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/recommend")
def api_recommend():
    activity = request.args.get("activity", "").strip().lower()
    weather = request.args.get("weather", "").strip().lower()

    if activity not in VALID_ACTIVITIES:
        return jsonify({"error": f"Invalid activity. Choose from: {', '.join(sorted(VALID_ACTIVITIES))}"}), 400
    if weather not in VALID_WEATHER:
        return jsonify({"error": f"Invalid weather. Choose from: {', '.join(sorted(VALID_WEATHER))}"}), 400

    items = recommend_items(activity, weather)
    return jsonify({"activity": activity, "weather": weather, "items": items})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
