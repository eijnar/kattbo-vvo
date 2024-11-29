import React from 'react';
import { EventDayGatheringPlace } from '../../types/Event';

interface GatheringPlaceItemProps {
  place: EventDayGatheringPlace;
}

const GatheringPlaceItem: React.FC<GatheringPlaceItemProps> = ({ place }) => {
  return (
    <li key={place.id}>
      <p>
        <strong>Samlingsplats:</strong> {place.name}
      </p>
      <p>
        <strong>Koordinater:</strong> {place.latitude}, {place.longitude}
      </p>
      <p>
        <strong>Jaktlag:</strong> {place.team_id || 'Alla'}
      </p>
      <p>
        <strong>Gemensam samling:</strong> {place.is_joint ? 'Ja' : 'Nej'}
      </p>
    </li>
  );
};

export default GatheringPlaceItem;
