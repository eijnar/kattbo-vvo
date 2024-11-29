export interface EventDayGatheringPlace {
    team_id: string | null;
    is_joint: boolean;
    id: string;
    name: string;
    longitude: number;
    latitude: number;
  }
  
  export interface EventDay {
    id: string;
    start_datetime: string; // ISO 8601 string
    end_datetime: string;   // ISO 8601 string
    registration_count: number;
    cancelled: boolean;
    event_day_gathering_places: EventDayGatheringPlace[];
  }
  
  export interface Event {
    id: string;
    name: string;
    creator_id: string;
    creator_name: string;
    event_category_id: string;
    category: string;
    event_days: EventDay[];
  }