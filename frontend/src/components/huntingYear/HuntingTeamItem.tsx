// src/components/huntingYear/HuntingTeamItem.tsx

import React from "react";
import useFetch from "../../hooks/useFetch";
import { Team, User } from "../../types/HuntingYear";
import UserList from "./UserList";

interface HuntingTeamItemProps {
  team: Team;
  huntingYear: number;
}

const HuntingTeamItem: React.FC<HuntingTeamItemProps> = ({ team, huntingYear }) => {
  const { data: users, loading, error } = useFetch<User[]>(`/team/${team.id}/users?huntingYear=${huntingYear}`);

  return (
    <div className="mb-4 p-4 border border-gray-300 rounded shadow">
      <h3 className="text-xl font-semibold mb-2">{team.name}</h3>
      {loading ? (
        <div>Loading users...</div>
      ) : error ? (
        <div className="text-red-500">Error loading users: {error}</div>
      ) : (
        <UserList users={users} />
      )}
    </div>
  );
};

export default HuntingTeamItem;
