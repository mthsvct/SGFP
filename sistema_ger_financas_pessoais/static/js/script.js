window.onload = function colcocaCor(){
    
    let todas = document.getElementsByClassName('opcao')
    let i, cor;
    let tam = todas.length;
    let botaoCor;

    for(i=0; i<tam; i++){
        cor = todas[i].getElementsByClassName('corzinha')[0].textContent;
        botaoCor = todas[i].getElementsByClassName('botaoCor')[0]
        botaoCor.style.backgroundColor = cor;
    }
}