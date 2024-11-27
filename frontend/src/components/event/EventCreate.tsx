import React, { useState } from 'react';
import axios from 'axios';

interface EventDayGatheringPlace {
  gathering_place_id: string;
  team_id: string;
}

interface EventDay {
  start_datetime: string;
  end_datetime: string;
  event_day_gathering_places: EventDayGatheringPlace[];
}

interface EventData {
  name: string;
  event_category_id: string;
  days: EventDay[];
  creator_id: string;
}

const CreateEventForm: React.FC = () => {
  const [eventData, setEventData] = useState<EventData>({
    name: '',
    event_category_id: '',
    days: [
      {
        start_datetime: '',
        end_datetime: '',
        event_day_gathering_places: [
          {
            gathering_place_id: '',
            team_id: '',
          },
        ],
      },
    ],
    creator_id: '',
  });

  const handleEventDataChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    field: keyof EventData
  ) => {
    setEventData({ ...eventData, [field]: e.target.value });
  };

  const handleDayChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    dayIndex: number,
    field: keyof EventDay
  ) => {
    const newDays = [...eventData.days];
    (newDays[dayIndex] as any)[field] = e.target.value;
    setEventData({ ...eventData, days: newDays });
  };

  const handleGatheringPlaceChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    dayIndex: number,
    gpIndex: number,
    field: keyof EventDayGatheringPlace
  ) => {
    const newDays = [...eventData.days];
    (newDays[dayIndex].event_day_gathering_places[gpIndex] as any)[
      field
    ] = e.target.value;
    setEventData({ ...eventData, days: newDays });
  };

  const addDay = () => {
    setEventData({
      ...eventData,
      days: [
        ...eventData.days,
        {
          start_datetime: '',
          end_datetime: '',
          event_day_gathering_places: [
            {
              gathering_place_id: '',
              team_id: '',
            },
          ],
        },
      ],
    });
  };

  const removeDay = (dayIndex: number) => {
    const newDays = eventData.days.filter((_, index) => index !== dayIndex);
    setEventData({ ...eventData, days: newDays });
  };

  const addGatheringPlace = (dayIndex: number) => {
    const newDays = [...eventData.days];
    newDays[dayIndex].event_day_gathering_places.push({
      gathering_place_id: '',
      team_id: '',
    });
    setEventData({ ...eventData, days: newDays });
  };

  const removeGatheringPlace = (dayIndex: number, gpIndex: number) => {
    const newDays = [...eventData.days];
    newDays[dayIndex].event_day_gathering_places = newDays[
      dayIndex
    ].event_day_gathering_places.filter((_, index) => index !== gpIndex);
    setEventData({ ...eventData, days: newDays });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await axios.post('https://dev-api.kattbovvo.se/v1/events', eventData);
      console.log('Event created:', response.data);
      // Reset the form or redirect as needed
    } catch (error) {
      console.error('Error creating event:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create Event</h2>
      <div>
        <label>
          Name:
          <input
            type="text"
            value={eventData.name}
            onChange={(e) => handleEventDataChange(e, 'name')}
            required
          />
        </label>
      </div>
      <div>
        <label>
          Event Category ID:
          <input
            type="text"
            value={eventData.event_category_id}
            onChange={(e) => handleEventDataChange(e, 'event_category_id')}
            required
          />
        </label>
      </div>
      <div>
        <label>
          Creator ID:
          <input
            type="text"
            value={eventData.creator_id}
            onChange={(e) => handleEventDataChange(e, 'creator_id')}
            required
          />
        </label>
      </div>
      <h3>Days</h3>
      {eventData.days.map((day, dayIndex) => (
        <div key={dayIndex} style={{ border: '1px solid #ccc', padding: '10px' }}>
          <div>
            <label>
              Start Datetime:
              <input
                type="datetime-local"
                value={day.start_datetime}
                onChange={(e) => handleDayChange(e, dayIndex, 'start_datetime')}
                required
              />
            </label>
          </div>
          <div>
            <label>
              End Datetime:
              <input
                type="datetime-local"
                value={day.end_datetime}
                onChange={(e) => handleDayChange(e, dayIndex, 'end_datetime')}
                required
              />
            </label>
          </div>
          <h4>Gathering Places</h4>
          {day.event_day_gathering_places.map((gp, gpIndex) => (
            <div key={gpIndex} style={{ marginLeft: '20px' }}>
              <div>
                <label>
                  Gathering Place ID:
                  <input
                    type="text"
                    value={gp.gathering_place_id}
                    onChange={(e) =>
                      handleGatheringPlaceChange(
                        e,
                        dayIndex,
                        gpIndex,
                        'gathering_place_id'
                      )
                    }
                    required
                  />
                </label>
              </div>
              <div>
                <label>
                  Team ID:
                  <input
                    type="text"
                    value={gp.team_id}
                    onChange={(e) =>
                      handleGatheringPlaceChange(e, dayIndex, gpIndex, 'team_id')
                    }
                    
                  />
                </label>
              </div>
              <button
                type="button"
                onClick={() => removeGatheringPlace(dayIndex, gpIndex)}
              >
                Remove Gathering Place
              </button>
            </div>
          ))}
          <button type="button" onClick={() => addGatheringPlace(dayIndex)}>
            Add Gathering Place
          </button>
          <button type="button" onClick={() => removeDay(dayIndex)}>
            Remove Day
          </button>
        </div>
      ))}
      <button type="button" onClick={addDay}>
        Add Day
      </button>
      <div>
        <button type="submit">Create Event</button>
      </div>
    </form>
  );
};

export default CreateEventForm;
