const THANE_NAUPADA = [19.1947, 72.9730];

const map = L.map('map').setView(THANE_NAUPADA, 15);

L.tileLayer(
    'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }
).addTo(map);

console.log("Script loaded");

if (navigator.geolocation) {

    console.log("Geolocation supported");

    navigator.geolocation.getCurrentPosition(

        function(position) {

            console.log("Location found", position);

            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            map.setView([lat, lng], 16);

            L.marker([lat, lng])
                .addTo(map)
                .bindPopup("You are here")
                .openPopup();

        },

        function(error) {

            console.error("Geolocation error:", error);
            console.log("Code:", error.code);
            console.log("Message:", error.message);

            L.marker(THANE_NAUPADA)
                .addTo(map)
                .bindPopup("Could not get current location. Showing Naupada, Thane.")
                .openPopup();
        },

        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 300000
        }
    );

} else {

    console.log("Geolocation not supported");

    L.marker(THANE_NAUPADA)
        .addTo(map)
        .bindPopup("Geolocation not supported. Showing Naupada, Thane.")
        .openPopup();
}