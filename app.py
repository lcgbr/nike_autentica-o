import os
import pandas as pd
from flask import Flask, render_template, request, redirect, session, send_file
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import timedelta
from relatorio import gerar_excel_precos
from utils import parse_skus


load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecret")
app.permanent_session_lifetime = timedelta(minutes=30)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

AUTHORIZED_USERS = os.environ.get("AUTHORIZED_USERS", "").split(",")
DEFAULT_PASSWORD = os.environ.get("DEFAULT_PASSWORD", "1234")

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("user"):
        return redirect("/login")

    if request.method == "POST":
        canal = request.form.get("canal") or request.form.get("outro_canal")
        skus_texto = request.form.get("skus")
        arquivo = request.files.get("arquivo")

        if skus_texto and arquivo:
            return "⚠️ Escolha apenas uma forma de entrada de SKUs.", 400
        if request.form.get("canal") and request.form.get("outro_canal"):
            return "⚠️ Escolha apenas uma opção de canal.", 400

        try:
            skus_list = []
            if arquivo:
                if arquivo.filename.endswith(".csv"):
                    df = pd.read_csv(arquivo)
                elif arquivo.filename.endswith(".xlsx"):
                    df = pd.read_excel(arquivo)
                else:
                    return "⚠️ Formato de arquivo não suportado.", 400

                if not df.empty:
                    primeira_coluna = df.columns[0]
                    skus_list = df[primeira_coluna].dropna().astype(str).tolist()
            else:
                skus_list = parse_skus(skus_texto)

            if not skus_list:
                return "⚠️ Nenhum SKU foi fornecido.", 400

            output_path = gerar_excel_precos(skus_list, canal)
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return f"⚠️ Erro ao gerar o relatório: {e}", 500

    return render_template("form.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        if email in AUTHORIZED_USERS and senha == DEFAULT_PASSWORD:
            session.permanent = True
            session["user"] = email
            return redirect("/")
        return "Acesso negado", 403

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
