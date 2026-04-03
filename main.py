import psycopg2
import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)

def get_db():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn


@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if "username" not in data or "password" not in data:
            return jsonify({"error": "username and password are required"}), 400
    
        hashed_password = generate_password_hash(data["password"])
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                      (data["username"], hashed_password))
        conn.commit()
        conn.close()
        return jsonify({"message": "user registered successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if "username" not in data or "password" not in data:
            return jsonify({"error": "username and password are required"}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (data["username"],))
        user = cursor.fetchone()
        conn.close()
        
        if user is None:
            return jsonify({"error": "user not found"}), 404
        
        if not check_password_hash(user[2], data["password"]):
            return jsonify({"error": "incorrect password"}), 401
        
        token = create_access_token(identity=data["username"])
        return jsonify({"token": token})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Welcome to TASK API!"


@app.route("/tasks", methods=["GET", "POST"])
@jwt_required()

def get_tasks():
        conn = get_db()
        cursor = conn.cursor()
    
        if request.method == "GET":
            try:
                username = get_jwt_identity()
                cursor.execute("SELECT * FROM tasks WHERE username = %s",(username,))
                rows = cursor.fetchall()
                conn.close()
                tasks = [{"id": row[0], "title": row[1],  "username": row[2],"status": row[3]} for row in rows]
                return jsonify(tasks)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
    
        elif request.method == "POST":
            try:
                new_task = request.get_json()
                if "title" not in new_task:
                    return jsonify({"error": "title is required"}), 400
                username = get_jwt_identity()
                cursor.execute("INSERT INTO tasks (title, username) VALUES (%s, %s)",
                          (new_task["title"], username))
                conn.commit()
                conn.close()
                return jsonify({"message": "task added successfully"})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
@app.route("/tasks/<title>", methods=["PUT","DELETE"])
@jwt_required()
def update_task(title):
        conn = get_db()
        cursor = conn.cursor()
        if request.method == "PUT":
                try:
                    update_data = request.get_json()
                    cursor.execute("UPDATE tasks SET status = %s WHERE title = %s",
                    (update_data["status"],title))
                    conn.commit()
                    conn.close()
                    return jsonify({"message":"task status updated successfully"})
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            
        elif request.method =="DELETE":
            try:
                cursor.execute("DELETE FROM tasks WHERE title = %s",(title,))
                conn.commit()
                conn.close()
                return jsonify({"message":"task deleted successfully"})
            except Exception as e:
                return jsonify({"error": str(e)}), 500


       
if __name__ == "__main__":
    app.run(debug=True)