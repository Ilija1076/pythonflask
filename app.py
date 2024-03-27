from flask import Flask, request, render_template
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


@app.route("/add", methods=["POST"])
def add_wish():
    data = request.form["content"]
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO wishlist (content) VALUES (%s)", (data,))
    mysql.connection.commit()
    cur.close()
    return "Your wish has been added"

@app.route("/")
def wishes():
    init_db()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wishlist")
    wishes = cur.fetchall()
    cur.close()
    return render_template("wishes.html", wishes=wishes)


if __name__ == "__main__":
    app.run(debug=True)