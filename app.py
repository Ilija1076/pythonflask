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


@app.route("/")
def wishes():
    init_db()
    cur = mysql.connection.cursor()
    cur.close()
    return render_template("wishes.html")

if __name__ == "__main__":
    app.run(debug=True)