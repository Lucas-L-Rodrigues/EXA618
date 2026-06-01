import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import { useState } from "react";

function ClickHandler({ setPosicao, setMarker }) {
  useMapEvents({
    click(e) {
      const pos = {
        lat: e.latlng.lat,
        lng: e.latlng.lng,
      };

      setPosicao(pos);
      setMarker(pos);
    },
  });

  return null;
}

export default function Mapa({ setPosicao }) {
  const [marker, setMarker] = useState(null);

  return (
    <MapContainer
      center={[-12.266, -38.966]}
      zoom={13}
      style={{
        height: "500px",
        width: "100%",
      }}
    >
      <TileLayer
        attribution="OpenStreetMap"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <ClickHandler
        setPosicao={setPosicao}
        setMarker={setMarker}
      />

      {marker && <Marker position={marker} />}
    </MapContainer>
  );
}