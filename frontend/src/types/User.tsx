export interface UserProfile {
  id: number;
  email: string;
  first_name?: string;
  last_name?: string;
  phone_number?: string;
  disabled: boolean;
}

export interface User {
  first_name: string;
  last_name: string;
  email: string;
  phone_number?: string;
}
