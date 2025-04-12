document.addEventListener('DOMContentLoaded', function() {
    const inputImmagine = document.getElementById('immagine');
    const anteprimaImmagine = document.getElementById('imagePreview');
    const contenitoreAnteprima = document.getElementById('imagePreviewContainer');
    const pulsanteRimuovi = document.getElementById('removeImage');
    const inputDatiImmagine = document.getElementById('immagine_data');
    const formArticolo = document.getElementById('articleForm');
    
    inputImmagine.addEventListener('change', function() {
        const file = this.files[0];
        
        if (file) {
            const lettore = new FileReader();
            
            lettore.onload = function(e) {
                anteprimaImmagine.src = e.target.result;
                inputDatiImmagine.value = e.target.result;
                contenitoreAnteprima.classList.remove('d-none');
            };
            
            lettore.readAsDataURL(file);
        }
    });
    
    pulsanteRimuovi.addEventListener('click', function() {
        inputImmagine.value = '';
        anteprimaImmagine.src = '';
        inputDatiImmagine.value = '';
        contenitoreAnteprima.classList.add('d-none');
    });
    
    formArticolo.addEventListener('submit', function(e) {
        const titolo = document.getElementById('titolo').value.trim();
        const contenuto = document.getElementById('contenuto').value.trim();
        
        if (!titolo || !contenuto) {
            e.preventDefault();
            alert('Inserisci sia il titolo che il contenuto.');
            return false;
        }
    });
});
