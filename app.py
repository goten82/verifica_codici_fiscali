import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Tabelle per il calcolo del carattere di controllo
pari_tabella = {
    "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9,
    "K": 10, "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18,
    "T": 19, "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25
}

dispari_tabella = {
    "0": 1, "1": 0, "2": 5, "3": 7, "4": 9, "5": 13, "6": 15, "7": 17, "8": 19, "9": 21,
    "A": 1, "B": 0, "C": 5, "D": 7, "E": 9, "F": 13, "G": 15, "H": 17, "I": 19, "J": 21,
    "K": 2, "L": 4, "M": 18, "N": 20, "O": 11, "P": 3, "Q": 6, "R": 8, "S": 12, "T": 14,
    "U": 16, "V": 10, "W": 22, "X": 25, "Y": 24, "Z": 23
}

def calcola_carattere_controllo(codice_base):
    somma = 0
    for i, c in enumerate(codice_base):
        if i % 2 == 0:  # Indice dispari (0-based)
            somma += dispari_tabella.get(c, 0)
        else:  # Indice pari
            somma += pari_tabella.get(c, 0)
    return chr((somma % 26) + 65)  # Conversione in lettera A-Z

def verifica_codice_fiscale(codice_fiscale):

     # Converte in maiuscolo
    codice_fiscale = codice_fiscale.upper()

     # Verifica formato: 6 lettere, 2 numeri, 1 lettera, 2 numeri, 1 lettera, 3 numeri, 1 lettera
    if not (
        codice_fiscale[0:6].isalpha() and
        codice_fiscale[6:8].isdigit() and
        codice_fiscale[8].isalpha() and
        codice_fiscale[9:11].isdigit() and
        codice_fiscale[11].isalpha() and
        codice_fiscale[12:15].isdigit() and
        codice_fiscale[15].isalpha()
    ):
        return f"{codice_fiscale} - Formato non valido"
    
    # Verifica lunghezza e formato
    if not re.fullmatch(r"[A-Z0-9]{16}", codice_fiscale):
        return f"{codice_fiscale} - Formato non valido"
    
    codice_base = codice_fiscale[:15]
    carattere_controllo = codice_fiscale[15]
    
    # Calcolo del carattere di controllo
    carattere_calcolato = calcola_carattere_controllo(codice_base)
    
    if carattere_calcolato == carattere_controllo:
        return f"{codice_fiscale} - Codice fiscale valido"
    else:
        return f"{codice_fiscale} - Carattere di controllo errato: previsto {carattere_calcolato}, trovato {carattere_controllo}"

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
            risultati.append(verifica_codice_fiscale(codice))        
        return risultati
    else:
        return jsonify({"error": "Codice fiscale non fornito"}), 400


# Esempio di utilizzo
if __name__ == "__main__":
    app.run(debug=True)
