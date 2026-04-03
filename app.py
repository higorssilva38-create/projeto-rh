from flask import Flask, render_template, request, redirect, url_for
import os
from analyzer import analisar_curriculo
from ranking import adicionar_candidato, obter_ranking, limpar_ranking

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 🔥 variável global para guardar os parâmetros
parametros_globais = ""


@app.route("/", methods=["GET", "POST"])
def index():
    global parametros_globais

    if request.method == "POST":
        arquivo = request.files["curriculo"]

        if arquivo:
            caminho = os.path.join(app.config["UPLOAD_FOLDER"], arquivo.filename)
            arquivo.save(caminho)

            resultado = analisar_curriculo(caminho, parametros_globais)
            adicionar_candidato(resultado)

            # 🔥 AGORA MOSTRA MENSAGEM DE SUCESSO
            return render_template("index.html", enviado=True)

    return render_template("index.html", enviado=False)


# 🔥 NOVA ROTA: DASHBOARD (ANÁLISE)
@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        ranking=obter_ranking(),
        parametros=parametros_globais
    )


# 🔥 salvar parâmetros
@app.route("/set_parametros", methods=["POST"])
def set_parametros():
    global parametros_globais
    parametros_globais = request.form["parametros"]
    return redirect(url_for("dashboard"))  # agora vai pro dashboard


# 🔥 limpar parâmetros
@app.route("/reset_parametros", methods=["POST"])
def reset_parametros():
    global parametros_globais
    parametros_globais = ""
    return redirect(url_for("dashboard"))


@app.route("/limpar", methods=["POST"])
def limpar():
    limpar_ranking()
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")