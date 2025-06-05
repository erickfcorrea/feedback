from flask import Flask, render_template, request, redirect
import psycopg2
import os

DATABASE_URL = os.environ.get("DATABASE_URL")  # ou use direto a string da URL
conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)

# Função para obter a conexão com o banco de dados via DATABASE_URL
def get_conn():
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        conn.set_client_encoding('UTF8')
        return conn
    except Exception as e:
        print("Erro na conexão com o banco:", e)
        raise
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        mensagem = request.form['mensagem']
        cur.execute("INSERT INTO feedback (nome, mensagem) VALUES (%s, %s)", (nome, mensagem))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/')

    cur.execute("SELECT nome, mensagem FROM feedback ORDER BY id DESC")
    feedbacks = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index.html', feedbacks=feedbacks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
