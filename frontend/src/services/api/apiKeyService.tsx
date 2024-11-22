// src/services/api/apiKeyService.ts

import axios from "axios";
import { ApiKeyResponse, ApiKey } from "../../types/ApiKey";
import { API_BASE_URL, API_VERSION } from '../../utils/constants';

interface CreateApiKeyPayload {
  permissions: string[];
  expires_in?: string; // e.g., "30d"
}


export const fetchApiKeys = async (token: string): Promise<ApiKey[]> => {
  const response = await axios.get<ApiKey[]>(
    `${API_BASE_URL}/${API_VERSION}/users/me/api-keys/`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
  return response.data;
};

export const revokeApiKey = async (
  token: string,
  apiKeyId: string
): Promise<void> => {
  await axios.delete(
    `${API_BASE_URL}/${API_VERSION}/users/me/api-keys/${apiKeyId}/`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
};

export const createApiKey = async (
  token: string,
  permissions: string[],
  expires_in: string
): Promise<ApiKeyResponse> => {
  const payload: CreateApiKeyPayload = { permissions, expires_in };

  const response = await axios.post<ApiKeyResponse>(
    `${API_BASE_URL}/${API_VERSION}/users/me/api-keys/`,
    payload,
    {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    }
  );
  return response.data;
};
