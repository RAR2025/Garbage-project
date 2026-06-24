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
const edgesLayer = L.layerGroup().addTo(map);
const routeLayer = L.layerGroup().addTo(map);
let shopsData = {};

function loadShops() {
    fetch("/api/shops/")
        .then(response => response.json())
        .then(data => {
            shopsLayer.clearLayers();
            data.forEach(shop => {
                shopsData[shop.id] = shop;
                const radius = Math.max(5, shop.garbage_weight / 10);
                const marker = L.circleMarker([shop.lat, shop.lng], {
                    radius: radius,
                    color: 'blue',
                    fillColor: '#3388ff',
                    fillOpacity: 0.6
                });
                const popupContent = `
                    <b>${shop.name}</b><br>
                    Weight: <span id="weight-text-${shop.id}">${shop.garbage_weight}</span> kg<br>
                    <input type="number" id="weight-input-${shop.id}" value="${shop.garbage_weight}" style="width: 60px;">
                    <button onclick="updateShopWeight(${shop.id})">Update</button><br>
                    <a href="/shops/${shop.id}/">View Details</a>
                `;
                marker.bindPopup(popupContent);
                shopsLayer.addLayer(marker);
            });
        })
        .catch(error => console.error("Error loading shops:", error));
}

function updateShopWeight(shopId) {
    const input = document.getElementById(`weight-input-${shopId}`);
    const newWeight = parseFloat(input.value);
    
    fetch(`/api/shops/${shopId}/update_weight/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ garbage_weight: newWeight })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "ok") {
            loadShops(); // Refresh the map
        } else {
            console.error("Failed to update weight:", data.errors);
        }
    })
    .catch(error => console.error("Error updating shop:", error));
}

function loadEdges() {
    fetch("/api/edges/")
        .then(response => response.json())
        .then(data => {
            edgesLayer.clearLayers();
            data.forEach(edge => {
                const latlngs = [
                    [edge.from_shop__lat, edge.from_shop__lng],
                    [edge.to_shop__lat, edge.to_shop__lng]
                ];
                const polyline = L.polyline(latlngs, {color: 'gray', weight: 2});
                polyline.bindTooltip(`${edge.distance_km} km`);
                edgesLayer.addLayer(polyline);
            });
        })
        .catch(error => console.error("Error loading edges:", error));
}

loadShops();
loadEdges();

document.getElementById('compute-route-btn').addEventListener('click', () => {
    fetch("/api/route/")
        .then(response => response.json())
        .then(data => {
            routeLayer.clearLayers();
            if (data.route && data.route.length > 0) {
                const latlngs = data.route.map(id => [shopsData[id].lat, shopsData[id].lng]);
                
                const routePolyline = L.polyline(latlngs, {color: 'red', weight: 5, opacity: 0.8});
                routeLayer.addLayer(routePolyline);
                
                data.route.forEach((id, index) => {
                    const shop = shopsData[id];
                    const icon = L.divIcon({
                        className: 'custom-div-icon',
                        html: `<div style="background-color: white; border: 2px solid red; border-radius: 50%; width: 20px; height: 20px; text-align: center; font-weight: bold; line-height: 18px;">${index + 1}</div>`,
                        iconSize: [20, 20],
                        iconAnchor: [10, 10]
                    });
                    const marker = L.marker([shop.lat, shop.lng], {icon: icon});
                    routeLayer.addLayer(marker);
                });
            }
        })
        .catch(error => console.error("Error loading route:", error));
});