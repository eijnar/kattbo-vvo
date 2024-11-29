import { Event } from '../../types/Event';
import { API_BASE_URL, API_VERSION } from '../../utils/constants';

export const fetchEvents = async (startDate: string, endDate: string): Promise<Event[]> => {
  const apiUrl = `${API_BASE_URL}/${API_VERSION}/events/?start=${startDate}&end=${endDate}`;

  const response = await fetch(apiUrl);
  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }
  const data: Event[] = await response.json();
  return data;
};
