document.addEventListener('DOMContentLoaded', function() {
    const campoRicerca = document.getElementById('searchInput');
    const pulsanteRicerca = document.getElementById('searchButton');
    const risultatiRicerca = document.getElementById('searchResults');
    const nessunRisultato = document.getElementById('noResults');
    const messaggioIniziale = document.getElementById('initialMessage');
    
    function eseguiRicerca() {
        const query = campoRicerca.value.trim();
        
        if (!query) {
            risultatiRicerca.innerHTML = '';
            nessunRisultato.classList.add('d-none');
            messaggioIniziale.classList.remove('d-none');
            return;
        }
        
        messaggioIniziale.classList.add('d-none');
        
        fetch(`/api/ricerca?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    risultatiRicerca.innerHTML = '';
                    nessunRisultato.classList.remove('d-none');
                } else {
                    nessunRisultato.classList.add('d-none');
                    mostraRisultati(data);
                }
            })
            .catch(error => {
                risultatiRicerca.innerHTML = `
                    <div class="col-12">
                        <div class="alert alert-danger">
                            Si è verificato un errore durante la ricerca. Riprova.
                        </div>
                    </div>
                `;
            });
    }
    
    function mostraRisultati(articoli) {
        risultatiRicerca.innerHTML = '';
        
        articoli.forEach(articolo => {
            const cardArticolo = document.createElement('div');
            cardArticolo.className = 'col';
            
            const htmlImmagine = articolo.immagine_data 
                ? `<div class="card-img-top article-image" style="background-image: url('${articolo.immagine_data}');"></div>`
                : `<div class="card-img-top article-image article-no-image">
                      <i class="fas fa-newspaper"></i>
                   </div>`;
            
            cardArticolo.innerHTML = `
                <div class="card h-100">
                    ${htmlImmagine}
                    <div class="card-body">
                        <h5 class="card-title">${articolo.titolo}</h5>
                        <p class="card-text text-truncate">${articolo.contenuto}</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">${articolo.data}</small>
                            <a href="/articolo/${articolo.id}" class="btn btn-sm btn-outline-primary">Leggi di più</a>
                        </div>
                    </div>
                </div>
            `;
            
            risultatiRicerca.appendChild(cardArticolo);
        });
    }
    
    pulsanteRicerca.addEventListener('click', eseguiRicerca);
    
    campoRicerca.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            eseguiRicerca();
        }
    });
    
    campoRicerca.focus();
});
