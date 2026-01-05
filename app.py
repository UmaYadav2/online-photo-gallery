from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import sqlite3

app = Flask(__name__)

# Cloudinary config
cloudinary.config(
    cloud_name="ddi65y7dzo",
    api_key="7883774377596374",
    api_secret="jhSUCH7l_n-X35e94JL7LVF5IJw"
)

# Database setup
def init_db():
    conn = sqlite3.connect("gallery.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("gallery.db")
    c = conn.cursor()
    c.execute("SELECT url FROM photos")
    images = c.fetchall()
    conn.close()

    return render_template("index.html", images=images)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["photo"]
        if file:
            result = cloudinary.uploader.upload(file)
            image_url = result["secure_url"]

            conn = sqlite3.connect("gallery.db")
            c = conn.cursor()
            c.execute("INSERT INTO photos (url) VALUES (?)", (image_url,))
            conn.commit()
            conn.close()

        return redirect(url_for("index"))

    return render_template("upload.html")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("gallery.db")
    c = conn.cursor()
    c.execute("DELETE FROM photos WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
