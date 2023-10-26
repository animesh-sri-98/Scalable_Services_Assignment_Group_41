from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
print("connecting to mongodb server")
client = MongoClient("mongodb://mongodb-service:27017/")
db = client["users_db"]
collection = db["users"]

# Get the last used user_id from the database
last_user = collection.find_one(sort=[("user_id", -1)])
if last_user:
    last_user_id = last_user["user_id"]
else:
    last_user_id = 0

@app.route('/users', methods=['POST'])
def create_user():
    global last_user_id
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    # Validate input fields
    if not username or not isinstance(username, str) or not email or not isinstance(email, str):
        return jsonify({"message": "Invalid input data"}), 400

    # Increment the user_id and insert new user into MongoDB
    last_user_id += 1
    user_data = {
        "user_id": last_user_id,
        "username": username,
        "email": email
    }
    collection.insert_one(user_data)

    response = {
        "message": "User created successfully",
        "user_id": last_user_id
    }
    return jsonify(response), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Retrieve user details from MongoDB based on user_id
    user = collection.find_one({"user_id": user_id})

    if user:
        response = {
            "user_id": user["user_id"],
            "username": user["username"],
            "email": user["email"]
        }
        return jsonify(response), 200
    else:
        # User not found, return 404 response
        return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9998)
