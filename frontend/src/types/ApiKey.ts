// src/types/ApiKey.ts

export interface ApiKey {
  id: string;
  name: string;
  created_at: string;
  expires_in: string | null;
  permissions: string[];
}

export interface ApiKeyResponse {
  api_key: string; // The actual key string (only returned upon creation)
  api_key_data: ApiKey; // Metadata about the key
}
