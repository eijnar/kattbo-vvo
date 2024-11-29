import { useState, useEffect } from "react";
import { Event } from "../types/Event";
import { fetchEvents } from "../services/api/eventService";

export const useEvents = () => {
  const [events, setEvents] = useState<Event[]>([]);
  const [isLoading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const getEvents = async () => {
      setLoading(true);
      setError(null);

      // Calculate dates
      const today = new Date();
      const twoMonthsAhead = new Date();
      twoMonthsAhead.setMonth(today.getMonth() + 2);
      const startDate = today.toISOString().split("T")[0]; // Format: YYYY-MM-DD
      const endDate = twoMonthsAhead.toISOString().split("T")[0];

      try {
        const data = await fetchEvents(startDate, endDate);
        setEvents(data);
      } catch (err: any) {
        setError(err.message || "Failed to fetch events.");
      } finally {
        setLoading(false);
      }
    };

    getEvents();
  }, []);

  return { events, isLoading, error };
};
