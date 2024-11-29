// src/components/EventsList.tsx

import React from "react";
import { useEvents } from "../../hooks/useEvents";
import EventItem from "./EventItem";
import Spinner from "../common/Spinner";
import { Heading } from "../catalyst/heading";

const EventsList: React.FC = () => {
  const { events, isLoading, error } = useEvents();

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Spinner size="lg" color="text-blue-500" />
      </div>
    );
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (

    <div>
      <Heading>Kommande händelser</Heading>
      {events.length === 0 ? (
        <p>Inga händelser hittades för det valda datumintervallet.</p>
      ) : (
        <div className="pt-4">
          {events.map((event) => (
            <EventItem key={event.id} event={event} />
          ))}
        </div>
      )}
    </div>
  );
};

export default EventsList;
