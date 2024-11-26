// src/components/TeamSelector.tsx

import React from "react";
import { useTeams } from "../../hooks/useTeam";
import Spinner from "../common/Spinner";

const TeamSelector: React.FC = () => {
  const {
    data: teams,
    isLoading: isTeamsLoading,
    error: teamsError,
  } = useTeams();

  if (isTeamsLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Spinner size="lg" color="text-blue-500" />
      </div>
    );
  }

  if (teamsError) {
    return <div>Error loading data.</div>;
  }

  return (
    <div>
      <h2>Select Team</h2>
      <div>
        <label htmlFor="team">Team:</label>
        <select id="team">
          {teams?.map((team) => (
            <option key={team.id} value={team.id}>
              {team.name}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default TeamSelector;
