from flask import Flask, render_template, request, redirect, flash
import csv
import requests
from notificacoes import enviar_email

GOOGLE_SHEET_URL = 'https://script.google.com/macros/s/AKfycbwTW92LG6p8y2DS_VO1NIOd3a8lrwTPNyXtR-gncm8orNFrnCk3fwcjJYpQdGJJbOXa/exec'

app = Flask(__name__)
app.secret_key = 'chave-secreta'  # Necessário para mensagens flash

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        whatsapp = request.form.get("whatsapp")
        sugestao = request.form.get("sugestao")

        # Salvar localmente no CSV
        with open("interessados.csv", "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([nome, email, whatsapp, sugestao])

        # Enviar para Google Sheets
        payload = {
            "nome": nome,
            "email": email,
            "whatsapp": whatsapp,
            "sugestao": sugestao
        }
        try:
            response = requests.post(GOOGLE_SHEET_URL, data=payload)
            print("Status:", response.status_code)
            print("Resposta:", response.text)

            if response.status_code == 200:
                flash("Mensagem enviada com sucesso!")
            else:
                flash("Erro ao enviar para a planilha.")
        except Exception as e:
            flash(f"Erro ao enviar: {e}")

        enviar_email(email, nome)

        return redirect("/obrigado")

    return render_template("index.html")

@app.route("/obrigado")
def obrigado():
    return render_template("obrigado.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

