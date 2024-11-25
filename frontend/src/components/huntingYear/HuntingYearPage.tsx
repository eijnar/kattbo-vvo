// src/components/huntingYear/HuntingYearPage.tsx

import React, { useState, useEffect } from "react";
import HuntingYearList from "./HuntingYearList";
import HuntingTeamList from "./HuntingTeamList";
import useFetch from "../../hooks/useFetch";
import { HuntingYear } from "../../types/HuntingYear";

const HuntingYearPage: React.FC = () => {
  const { data: huntingYears, loading, error } = useFetch<HuntingYear[]>("/hunting_years");
  const [selectedYear, setSelectedYear] = useState<number | null>(null);

  // Determine the current hunting year when huntingYears data is fetched
  useEffect(() => {
    if (huntingYears && huntingYears.length > 0) {
      const currentYearObj = huntingYears.find((year) => year.is_current);
      if (currentYearObj) {
        setSelectedYear(currentYearObj.year);
      } else {
        // Fallback to the latest year if no current year is marked
        const latestYear = Math.max(...huntingYears.map((year) => year.year));
        setSelectedYear(latestYear);
      }
    }
  }, [huntingYears]);

  const handleYearSelect = (year: number) => {
    setSelectedYear(year);
  };

  if (loading) {
    return <div>Loading hunting years...</div>;
  }

  if (error) {
    return <div className="text-red-500">Error loading hunting years: {error}</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <HuntingYearList
        huntingYears={huntingYears!}
        selectedYear={selectedYear}
        onYearSelect={handleYearSelect}
      />
      {selectedYear && <HuntingTeamList huntingYear={selectedYear} />}
    </div>
  );
};

export default HuntingYearPage;
