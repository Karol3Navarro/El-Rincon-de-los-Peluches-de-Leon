
$(document).ready(function() {
    // Mensajes que desaparecen automáticamente
    $("#idMensajes").delay(2000).fadeOut("slow");

    // Previsualizar imágenes seleccionadas
    $("#imagenesInput").on("change", function() {
        $("#preview").html(""); // limpiar previsualización
        let files = this.files;

        for (let i = 0; i < files.length; i++) {
            let reader = new FileReader();
            reader.onload = function(e) {
                let img = $("<img>")
                    .attr("src", e.target.result)
                    .css({
                        "width": "120px",
                        "margin": "5px",
                        "border": "1px solid #ccc"
                    });
                $("#preview").append(img);
            }
            reader.readAsDataURL(files[i]);
        }
    });
});