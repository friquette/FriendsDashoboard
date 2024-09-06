from flask import request, jsonify

from app import app, db
from models import Friend


@app.route("/api/friends", methods=["GET"])
def get_friends():
    friends = Friend.query.all()
    result = [friend.to_json() for friend in friends]

    return jsonify(result)


@app.route("/api/friends", methods=["POST"])
def create_friend():
    try:
        data = request.json

        required_fields = ["name", "role", "description", "gender"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        name = data.get("name")
        role = data.get("role")
        description = data.get("description")
        gender = data.get("gender")
        img_url = f"https://api.multiavatar.com/{name}.png"

        new_friend = Friend(name=name, role=role, description=description, gender=gender, img_url=img_url)
        db.session.add(new_friend)
        db.session.commit()

        return jsonify({"msg": "Friend created successfully !"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": 500})


@app.route("/api/friends/<int:id>", methods=["DELETE"])
def delete_friend(id):
    try:
        friend = Friend.query.get(id)

        if friend is None:
            return jsonify({"error": "Friend not found."}), 404

        db.session.delete(friend)
        db.session.commit()
        return jsonify({"msg": "Friend deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
