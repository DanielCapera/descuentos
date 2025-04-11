document.addEventListener("DOMContentLoaded", function () {
    let skip = 9;
    let button = document.getElementById("ver-mas");

    function formatPrice(number) {
        return new Intl.NumberFormat("es-CO", {
            style: "currency",
            currency: "COP",
            minimumFractionDigits: 0,
        }).format(number);
    }

    button.addEventListener("click", function () {
        fetch("/load_more", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ skip: skip }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.productos.length > 0) {
                let container = document.getElementById("productos-container");
                data.productos.forEach(producto => {
                    let div = document.createElement("div");
                    div.classList.add("product");

                    const precioFormateado = formatPrice(producto.precio_actual);

                    div.innerHTML = `
                        <img src="${producto.imagen}" alt="${producto.descripcion}">
                        <h3>${producto.descripcion}</h3>
                        <p>Precio: ${precioFormateado}</p>
                        <a href="/detalle/${encodeURIComponent(producto.descripcion)}" class="btn">Ver Detalle</a>
                    `;
                    container.appendChild(div);
                });

                skip += data.productos.length;
            }

            if (!data.has_more) {
                button.style.display = "none";
            }
        });
    });
});
