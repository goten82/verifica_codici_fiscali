function verificaCodici() {
    const codici = document.getElementById('codiciFiscali').value;
    fetch('/verifica', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ codice_fiscale: codici })
    })
        .then(response => response.json())
        .then(data => {
            const risultatoDiv = document.getElementById('risultato');
            risultatoDiv.innerHTML = '';
            data.forEach(item => {
                risultatoDiv.innerHTML += `${item}<br>`;
            });
        })
        .catch(error => {
            console.error('Errore:', error);
        });
}

function copiaTesto() {
    const risultatoDiv = document.getElementById('risultato');
    const testo = risultatoDiv.innerText;
    navigator.clipboard.writeText(testo).then(() => {
        alert('Testo copiato negli appunti!');
    }).catch(err => {
        console.error('Errore durante la copia:', err);
    });
}


function calcolaCF(event) {
    event.preventDefault();

    const nome = document.getElementById('nome').value;
    const cognome = document.getElementById('cognome').value;
    const dataNascita = document.getElementById('dataNascita').value;
    const sesso = document.getElementById('sesso').value;
    const comune = document.getElementById('comune').value;

    fetch('/calcola_cf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            nome: nome,
            cognome: cognome,
            data_nascita: dataNascita,
            sesso: sesso,
            comune: comune
        })
    })
        .then(response => response.json())
        .then(data => {
            const risultatoDiv = document.getElementById('risultatoCF');
            risultatoDiv.innerHTML = `Codice Fiscale: ${data.codice_fiscale}`;
            risultatoDiv.display.style.border = '3px solid black;'
        })
        .catch(error => {
            console.error('Errore:', error);
        });
}
window.onload = function () {
    const radioVerifica = document.getElementById('verifica');
    if (radioVerifica) {
        radioVerifica.checked = true;
        visualizzaFieldset();
    }
}


function visualizzaFieldset() {
    const radioVerifica = document.getElementById('verifica');
    const radioCalcola = document.getElementById('calcola');
    const fieldsetVerifica = document.getElementById('fieldsetVerifica');
    const fieldsetCalcola = document.getElementById('fieldsetCalcola');
    const radioTrova = document.getElementById('trova');
    const fieldsetTrova = document.getElementById('fieldsetTrova')

    if (radioVerifica.checked) {
        fieldsetVerifica.style.display = 'block';
        fieldsetCalcola.style.display = 'none';
        fieldsetTrova.style.display = 'none';
    } else if (radioCalcola.checked) {
        fieldsetVerifica.style.display = 'none';
        fieldsetCalcola.style.display = 'block';
        fieldsetTrova.style.display = 'none';
    } else if (radioTrova.checked) {
        fieldsetVerifica.style.display = 'none';
        fieldsetCalcola.style.display = 'none';
        fieldsetTrova.style.display = 'block';
    }
}


function trovaComune() {
    let codice = document.getElementById('codice').value;
    if (!/\d/.test(codice)) {
        codice = codice.toLowerCase();
    }

    fetch('/comune', {
        method: 'POST',
        body: JSON.stringify({ codice: codice }),
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            const risultatoDiv = document.getElementById('risCalcolaComuni');
            risultatoDiv.innerHTML = `<strong>Comune: ${data.comune.name} (${data.comune.province})</strong> con codice Belfiore <strong>${data.comune.code}</strong>`;
        })
        .catch(error => {
            console.error('Errore:', error);
            alert('Comune non trovato!')
        });
}