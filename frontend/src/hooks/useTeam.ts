import { useQuery } from "@tanstack/react-query";
import { Team } from "../types/Team";
import { getTeams } from "../services/api/teamService";

export const useTeams = () => {
  return useQuery<Team[], Error>({
    queryKey: ["huntingYears"],
    queryFn: getTeams,
    staleTime: 1000 * 60 * 5, // 5 minutes
    refetchOnWindowFocus: true,
  });
};
