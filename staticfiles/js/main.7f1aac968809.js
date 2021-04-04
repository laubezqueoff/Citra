function añadir (id) {
    var nombre = document.getElementById('nombre'+id).innerHTML
    var precio = document.getElementById('precio'+id).innerHTML
    var table = document.getElementById('tbody');
    var nombres = []
    for (let i = 0; i < document.getElementsByClassName('nombreProducto').length; i++) {
            nombres.push(document.getElementsByClassName('nombreProducto')[i].innerText)
        }
    if(!nombres.includes(nombre)) {
        var row = table.insertRow(-1);
        var cell1 = row.insertCell(-1);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        cell1.innerHTML = nombre;
        cell1.classList.add('nombreProducto');
        cell2.innerHTML = precio;
        cell2.setAttribute('id','precioProducto' + id);
        cell3.innerHTML = 1;
        cell3.setAttribute('id','cantidadProducto' + id);
        cell3.classList.add('cantidadProducto');
        cell4.innerHTML = id;
        cell4.setAttribute('id','idProducto' + id);
        cell4.classList.add('idProducto');
        document.getElementById("idProducto" + id).style.display = "none";
    } else {
        document.getElementById('cantidadProducto' + id).innerText = parseInt(document.getElementById('cantidadProducto' + id).innerText) + 1
        document.getElementById('precioProducto' + id).innerText = Number(precio) * Number(document.getElementById('cantidadProducto' + id).innerText)
    }
}

function vaciarCarrito() {
    if (confirm("多Quieres vaciar el carrito?")) {
        document.getElementById('tbody').remove();
        var table = document.getElementById('table');
        var tbody = document.createElement('tbody');
        tbody.setAttribute('id','tbody')
        table.appendChild(tbody)
    }
}

function reserva() {
    var array = []
    var objeto = {}
    console.log(document.getElementsByClassName('idProducto'))
    console.log(document.getElementsByClassName('cantidadProducto'))
    for (let i = 0; i < document.getElementsByClassName('idProducto').length; i++) {
        objeto.id = parseInt(document.getElementsByClassName('idProducto')[i].innerText)
        objeto.cantidad = parseInt(document.getElementsByClassName('cantidadProducto')[i].innerText)
        array.push(objeto)
        objeto = {}
    }
    data = {
        key_1_string: JSON.stringify(array),
        csrfmiddlewaretoken: '{{ csrf_token }}',
    }
    $.ajax({
        url: 'booking/',
        data: data,
        type: 'POST',
        success: function (data) {
            confirm("Reserva realizada")
            window.location.replace(window.location.origin+ data.url);
        }
    });
};