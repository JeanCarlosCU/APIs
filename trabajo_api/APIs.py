from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "TU_API_KEY"

API_URL = "https://api.calorieninjas.com/v1/nutrition"

HEADERS = {
    "X-Api-Key": API_KEY
}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calcular", methods=["POST"])
def calcular():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Por favor ingresa un alimento."}), 400

    try:
        response = requests.get(API_URL, headers=HEADERS, params={"query": query})
        response.raise_for_status()
        result = response.json()

        if not result["items"]:
            return jsonify({"error": "No se encontraron alimentos."}), 404

        calorias_total = 0
        detalles = []

        for item in result["items"]:
            detalles.append({
                "nombre": item["name"].title(),
                "calorias": round(item["calories"], 2),
                "proteina": round(item["protein_g"], 2),
                "grasa": round(item["fat_total_g"], 2),
                "carbohidratos": round(item["carbohydrates_total_g"], 2)
            })
            calorias_total += item["calories"]

        return jsonify({
            "total": round(calorias_total, 2),
            "alimentos": detalles
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
