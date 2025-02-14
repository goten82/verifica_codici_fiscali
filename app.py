import re
from flask import Flask, render_template, request, jsonify
import codice_fiscale
import comune
from werkzeug.wrappers import Request
app = Flask(__name__)


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Set 16MB max content length
app.config['MAX_FORM_MEMORY_SIZE'] = 1024 * 1024  # 1MB max form size


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
    
@app.route('/calcola_cf', methods=['POST'])
def calcola_codice():
    if request.json:
        nome = request.json.get('nome')
        cognome = request.json.get('cognome')
        data_nascita = request.json.get('data_nascita')
        sesso = request.json.get('sesso')
        comune = request.json.get('comune')
        
        if nome and cognome and data_nascita and sesso and comune:
            try:
                cf = codice_fiscale.encode(
                    lastname=cognome,
                    firstname=nome,
                    gender=sesso,
                    birthdate=data_nascita,
                    birthplace=comune
                )
                return jsonify({"codice_fiscale": cf})
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        else:
            return jsonify({"error": "Dati mancanti"}), 400
    else:
        return jsonify({"error": "Dati non forniti"}), 400
    

@app.route('/comune', methods=['POST'])
def trova_comune():
    if request.json:
        codice= request.json.get('codice')
        _comune = comune.get_comune(codice)
        return jsonify({'comune':_comune})
    else:
        return jsonify({"error":"Errore"}), 400



# Esempio di utilizzo
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
    # app.run(debug=True)
