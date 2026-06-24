const THANE_NAUPADA = [19.1947, 72.9730];

const map = L.map('map').setView(THANE_NAUPADA, 15);

L.tileLayer(
    'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }
).addTo(map);

const shopsLayer = L.layerGroup().addTo(map);

function loadShops() {
    fetch("/api/shops/")
        .then(response => response.json())
        .then(data => {
            shopsLayer.clearLayers();
            data.forEach(shop => {
                const radius = Math.max(5, shop.garbage_weight / 10);
                const marker = L.circleMarker([shop.lat, shop.lng], {
                    radius: radius,
                    color: 'blue',
                    fillColor: '#3388ff',
                    fillOpacity: 0.6
                });
                marker.bindPopup(`<b>${shop.name}</b><br>Weight: ${shop.garbage_weight} kg`);
                shopsLayer.addLayer(marker);
            });
        })
        .catch(error => console.error("Error loading shops:", error));
}

loadShops();