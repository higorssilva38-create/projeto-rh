from flask import Flask, render_template, request, redirect, url_for
import os
from analyzer import analisar_curriculo
from ranking import adicionar_candidato, obter_ranking, limpar_ranking

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        arquivo = request.files["curriculo"]

        if arquivo:
            caminho = os.path.join(app.config["UPLOAD_FOLDER"], arquivo.filename)
            arquivo.save(caminho)

            resultado = analisar_curriculo(caminho)
            adicionar_candidato(resultado)

            return redirect(url_for("index"))

    return render_template("index.html", ranking=obter_ranking())

@app.route("/limpar", methods=["POST"])
def limpar():
    limpar_ranking()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")