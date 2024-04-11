from flask import Flask, request, render_template, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "db"

mysql = MySQL(app)

def init_db():
    cur = mysql.connection.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS wishlist(id INT AUTO_INCREMENT PRIMARY KEY, content TEXT)
        """
    )
    mysql.connection.commit()
    cur.close()

@app.route("/", methods=["GET"])
def get_wishes():
    init_db()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wishlist")
    wishes = cur.fetchall()
    cur.close()
    return render_template("wishes.html", wishes=wishes)

@app.route("/wish/<int:wish_id>", methods=["GET"])
def get_wish(wish_id):
    init_db()
    cur = mysql.connection.cursor()
    cur.execute("SELECT content FROM wishlist WHERE id = %s", (wish_id,))
    wish = cur.fetchone()
    cur.close()
    if wish:
        return jsonify(wish)
    else:
        return jsonify({"error": "Wish not found"}), 404
    
@app.route("/add/<string:wish_content>", methods=["POST"])
def add_wish(wish_content):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO wishlist (content) VALUES (%s)", (wish_content,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Your wish has been added"})


@app.route("/delete/<int:wish_id>", methods=["DELETE"])
def delete_wish(wish_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM wishlist WHERE id = %s", (wish_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Wish deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
