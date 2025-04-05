document.addEventListener('DOMContentLoaded', function () {
  const historicoElement = document.getElementById('historico-data');
  console.log('historicoElement', historicoElement)

  if (!historicoElement) {
    console.error("No se encontró el elemento con id 'historico-data'");
    return;
  }

  let historico = [];

  try {
    historico = JSON.parse(historicoElement.textContent);
  } catch (e) {
    console.error("Error al parsear el JSON del histórico de precios:", e);
    return;
  }

  if (Array.isArray(historico)) {
    // ya está en array, sigue normal
  } else if (typeof historico === 'object') {
    // Convertimos el objeto en array y lo ordenamos cronológicamente
    const meses = {
      "enero": 1,
      "febrero": 2,
      "marzo": 3,
      "abril": 4,
      "mayo": 5,
      "junio": 6,
      "julio": 7,
      "agosto": 8,
      "septiembre": 9,
      "octubre": 10,
      "noviembre": 11,
      "diciembre": 12,
    };

    historico = Object.entries(historico).map(([fecha, precio]) => {
      const [mesStr, anio] = fecha.split("_");
      const orden = parseInt(anio) * 100 + meses[mesStr];
      return { fecha, precio, orden };
    });

    historico.sort((a, b) => a.orden - b.orden);
  }

  // Suponiendo que cada entrada del histórico tiene formato:
  // { "fecha": "marzo_2025", "precio": 1200000 }
  const labels = historico.map(entry => entry.fecha);
  const data = historico.map(entry => entry.precio);

  const ctx = document.getElementById('graficoPrecios').getContext('2d');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Precio',
        data: data,
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: false,
          title: {
            display: true,
            text: 'Precio en COP'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Mes'
          }
        }
      },
      plugins: {
        legend: {
          display: true,
          position: 'top'
        }
      }
    }
  });
});
