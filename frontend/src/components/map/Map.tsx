// src/components/map/Map.tsx
import React from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import 'leaflet/dist/leaflet.css';

const Map: React.FC = () => {
  return (
    <div className="relative h-screen w-full">
      {/* Map Container */}
      <MapContainer
        center={[60.83288410381268, 14.197291277599767]}
        zoom={13}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>'
        />
      </MapContainer>
    </div>
  );
};

export default Map;
