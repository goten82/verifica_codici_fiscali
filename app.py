import re
from flask import Flask, render_template, request, jsonify
import codice_fiscale

app = Flask(__name__)

@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/verifica', methods=['POST'])
def verifica():
    if request.json and 'codice_fiscale' in request.json:
        codici_fiscali = request.json['codice_fiscale']
        # Split the string into an array of codes
        codici_array = codici_fiscali.split('\n')
        risultati = []
        for codice in codici_array:
            risultati.append(codice_fiscale.is_valid(codice))        
        return risultati
    else:
        return jsonify({"error": "Codice fiscale non fornito"}), 400


# Esempio di utilizzo
if __name__ == "__main__":
    app.run(debug=True)
