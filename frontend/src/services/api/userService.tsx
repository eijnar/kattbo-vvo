// src/services/api/userService.ts
import axios from 'axios';
import { UserProfile, User } from '../../types/User';
import { API_BASE_URL } from '../../utils/constants';

export const fetchUserProfile = async (token: string): Promise<UserProfile> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/users/me/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error: any) {
    console.error('Error fetching user profile:', error);
    throw error;
  }
};

export const updateUserProfile = async (token: string, data: Partial<UserProfile>): Promise<UserProfile> => {
  try {
    const response = await axios.put(`${API_BASE_URL}/users/me/`, data, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error: any) {
    console.error('Error updating user profile:', error);
    throw error;
  }
};

export const fetchUsers = async (): Promise<User[]> => {
  const response = await fetch(`${API_BASE_URL}/users/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      // Include authorization headers if required
    },
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || 'Failed to fetch users');
  }

  const data: User[] = await response.json();
  return data;
};