// src/components/huntingYear/HuntingTeamList.tsx

import React from "react";
import useFetch from "../../hooks/useFetch";
import { Team } from "../../types/HuntingYear";
import HuntingTeamItem from "./HuntingTeamItem";

interface HuntingTeamListProps {
  huntingYear: number;
}

const HuntingTeamList: React.FC<HuntingTeamListProps> = ({ huntingYear }) => {
  const { data: teams, loading, error } = useFetch<Team[]>(`/teams?huntingYear=${huntingYear}`);

  if (loading) {
    return <div>Loading teams for {huntingYear}...</div>;
  }

  if (error) {
    return <div className="text-red-500">Error loading teams: {error}</div>;
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Teams for {huntingYear}</h2>
      {teams && teams.length > 0 ? (
        teams.map((team) => (
          <HuntingTeamItem key={team.id} team={team} huntingYear={huntingYear} />
        ))
      ) : (
        <div>No teams found for this hunting year.</div>
      )}
    </div>
  );
};

export default HuntingTeamList;
