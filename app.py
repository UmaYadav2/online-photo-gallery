from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import os
import psycopg2

app = Flask(__name__)

# ---------------- CLOUDINARY CONFIG ----------------
cloudinary.config(
    cloud_name=os.environ.get("di65y7dzo"),
    api_key=os.environ.get("883774377596374"),
    api_secret=os.environ.get("jhSUCH7l_n-X35e94JL7LVF5IJw")
)


def get_db():
    database_url = os.environ.get("DATABASE_URL")
    return psycopg2.connect(database_url, sslmode="require")


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Create table at startup


# ---------------- ROUTES ----------------
@app.route("/")
def index():
    init_db()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, url FROM photos ORDER BY uploaded_at DESC")
    images = cur.fetchall()
    conn.close()
    return render_template("index.html", images=images)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("photo")
        if file:
            result = cloudinary.uploader.upload(file)
            image_url = result["secure_url"]

            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO photos (url) VALUES (%s)",
                (image_url,)
            )
            conn.commit()
            conn.close()

        return redirect(url_for("index"))

    return render_template("upload.html")

@app.route("/delete/<int:image_id>")
def delete(image_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM photos WHERE id = %s", (image_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
