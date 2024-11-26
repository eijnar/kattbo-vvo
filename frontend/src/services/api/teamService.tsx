import axios from 'axios';
import { Team } from '../../types/Team'
import { API_BASE_URL, API_VERSION } from '../../utils/constants';

export const getTeams = async (): Promise<Team[]> => {
    const response = await axios.get<Team[]>(`${API_BASE_URL}/${API_VERSION}/teams`)
    return response.data;
}
