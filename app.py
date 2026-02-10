# app.py
from flask import Flask, request, jsonify, render_template
from calculo import calcular

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    # GET: só renderiza a página
    if request.method == "GET":
        return render_template("index.html")

    # POST: vem do seu <form method="post">
    data = request.form

    try:
        resultado = calcular(
            peca=data.get("peca"),
            servico=data.get("servico"),
            forma=data.get("forma"),
            bandeira=data.get("bandeira", "elo"),
            parcelas=data.get("parcelas", 1),
        )
        # Renderiza o mesmo template com resultado (Jinja)
        return render_template("index.html", resultado=resultado)

    except Exception as e:
        # Renderiza erro na página (se você colocar {% if erro %} no index)
        return render_template("index.html", erro=str(e)), 400


@app.route("/calcular", methods=["POST"])
def calcular_api():
    # API: aceita JSON ou form
    data = request.get_json(silent=True) or request.form

    try:
        r = calcular(
            peca=data.get("peca"),
            servico=data.get("servico"),
            forma=data.get("forma"),
            bandeira=data.get("bandeira", "elo"),
            parcelas=data.get("parcelas", 1),
        )
        return jsonify(r)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
