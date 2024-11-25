// src/types/index.ts

export interface HuntingYear {
    id: string;
    name: number;
    start_date: Date;
    end_date: Date;
    is_locked: boolean;
    is_current: boolean;
    // Add other fields if necessary
  }
  
  export interface Team {
    id: string;
    name: string;
    // Add other team-related fields if necessary
  }
  
  export interface User {
    id: string;
    name: string;
    email: string;
    // Add other user-related fields if necessary
  }
  