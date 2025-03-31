const urlBase = 'http://127.0.0.1:5000';

async function obtenerEstadoCajeros() {
    try {
        const response = await fetch(`${urlBase}/cajeros`);
        const data = await response.json();

        data.forEach(cajero => {
            const estadoElement = document.getElementById(`estado-${cajero.id}`);
            const actualizacionElement = document.getElementById(`actualizacion-${cajero.id}`);
            estadoElement.textContent = cajero.estado;
            estadoElement.className = cajero.estado.toLowerCase().replace(/\s+/g, '-');
            actualizacionElement.textContent = `Última actualización: ${formatearFecha(cajero.ultima_actualizacion)}`;
        });
    } catch (error) {
        console.error('Error al obtener el estado de los cajeros:', error);
    }
}

async function actualizarEstado(idCajero, nuevoEstado) {
    try {
        const response = await fetch(`${urlBase}/cajeros/${idCajero}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ estado: nuevoEstado })
        });

        if (response.ok) {
            obtenerEstadoCajeros(); // Volver a obtener el estado actualizado
        } else {
            console.error('Error al actualizar el estado del cajero');
        }
    } catch (error) {
        console.error('Error al actualizar el estado del cajero:', error);
    }
}

function formatearFecha(fechaISO) {
    const fecha = new Date(fechaISO);
    return fecha.toLocaleString(); // Formato local de fecha y hora
}

obtenerEstadoCajeros();
