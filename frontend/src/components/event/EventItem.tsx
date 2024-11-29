import React from "react";
import { Event } from "../../types/Event";
import EventDayItem from "./EventDayItem";

interface EventItemProps {
  event: Event;
}

const EventItem: React.FC<EventItemProps> = ({ event }) => {
  return (
    <div className="py-2">
      <div
        className="divide-y divide-gray-200 border border-gray-200 verflow-hidden rounded-lg bg-white shadow "
        key={event.id}
      >
        <div className="border-b border-gray-200 bg-gray-100 px-4 py-3 sm:px-6">
          <div className="-ml-4 -mt-4 flex flex-wrap items-center justify-between sm:flex-nowrap">
            <div className="ml-4 mt-3">
              <h2 className="text-base font-semibold text-gray-900">
                {event.name}
              </h2>
              <p className="mt-1 text-sm text-gray-500">
                {event.category} {event.creator_name}
              </p>
            </div>
            <div className="ml-4 mt-4 shrink-0">
              <button
                type="button"
                className="relative inline-flex items-center rounded-md bg-green-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Anmäl dig
              </button>
            </div>
          </div>
        </div>
        <div className="px-4 py-5 sm:p-6">
          {event.event_days.map((day) => (
            <EventDayItem key={day.id} day={day} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default EventItem;
