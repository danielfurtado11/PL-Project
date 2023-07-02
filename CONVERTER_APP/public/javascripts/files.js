
function showFile(fname, ftype){
    console.log("Aqui!")
    
    if(ftype == "image/png" || ftype == "image/jpeg"){// Para imagens
        var file = $('<img src="/images/' + fname + '" width="400px"/>')
    }else{ // Sem ser imagens
        var file = $('<p>' + fname + ', ' + ftype + '</p>')
    }

    // Limpa tudo o que poderia ter no modal
    $("#display").empty()
    $("#display").append(file)
    $("#display").modal()
}