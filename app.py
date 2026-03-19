from flask import Flask, render_template_string, request
import os
import psycopg2

app = Flask("Benim uygulamam")

# Veritabanı bağlantı adresi (Çevre değişkeninden al)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://bulut_proje_user:NwqSCQV8KCfKJmvghYiTAIHp7Xba2Fk6@dpg-d6ttgqshg0os7381hnpg-a.oregon-postgres.render.com/bulut_proje")

HTML = """
<!doctype html>
<html>
<head>
    <title>Buluttan Selam!</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #eef2f3; }
        h1 { color: #333; }
        form { margin: 20px auto; }
        input { padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #ccc; }
        button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
        button:hover { background: #45a049; }
        ul { list-style: none; padding: 0; }
        li { background: white; margin: 5px auto; width: 250px; padding: 8px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
      </style>
</head>
<body> 
      <h1>Buluttan Selam!</h1>
      <p>Adını yaz, selamını bırak</p>
      <form method="POST">
          <input type="text" name="isim" placeholder="Adını yaz" required>
          <button type="submit">Gönder</button>
      </form>
     <h3>Ziyaretçiler:</h3>
<ul>
    {% if isimler %}
        {% for ad in isimler %}
            <li>{{ ad }}</li>
        {% endfor %}
    {% else %}
        <li>Henüz kimse yok.</li>
    {% endif %}
</ul>
"""

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Tabloyu oluştur (Eğer yoksa)
    cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT)")
    conn.commit()

    if request.method == "POST":
        isim = request.form.get("isim")
        if isim:
            cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
            conn.commit()

    # Son 10 ismi çek
    cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    isimler = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()
    
    return render_template_string(HTML, isimler=isimler)

if "Benim uygulamam" == "Benim uygulamam":
    app.run(host="0.0.0.0", port=5000, debug=True)