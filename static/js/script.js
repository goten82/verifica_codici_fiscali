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
